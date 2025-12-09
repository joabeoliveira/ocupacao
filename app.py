import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text, inspect
import sys
from dotenv import load_dotenv

# Carrega .env se existir (apenas local)
load_dotenv()

app = Flask(__name__)
# Chave secreta definida pelo usuário
app.secret_key = os.getenv('SECRET_KEY', '114211Jo@')

print("\n" + "="*40, flush=True)
print("--- DIAGNÓSTICO DE INICIALIZAÇÃO (V7 - FIX DATA BRASIL) ---", flush=True)

# Lógica de Prioridade: DATABASE_URL > Variáveis Separadas
db_url = os.getenv('DATABASE_URL')

if db_url:
    print("AVISO: Encontrada variável DATABASE_URL. Ela terá prioridade.", flush=True)
    if db_url.startswith("mysql://"):
        db_url = db_url.replace("mysql://", "mysql+pymysql://")
    print(f"      URL em uso: {db_url.split('@')[-1]}", flush=True)
else:
    print("INFO: Usando variáveis separadas (DB_HOST, DB_NAME...)", flush=True)
    DB_HOST = os.getenv('DB_HOST', 'site_nir')
    DB_USER = os.getenv('DB_USER', 'joabeoliveira')
    DB_PASS = os.getenv('DB_PASSWORD', '114211Jo')
    DB_NAME = os.getenv('DB_NAME', 'nir')
    DB_PORT = os.getenv('DB_PORT', '3306')
    
    print(f"      Host: {DB_HOST}", flush=True)
    print(f"      Banco Alvo: {DB_NAME}", flush=True)
    
    db_url = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print("="*40 + "\n", flush=True)

# Variáveis globais
engine = None
db_status = False

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        db_atual = conn.execute(text("SELECT DATABASE()")).scalar()
        print(f">>> CONECTADO COM SUCESSO! Banco Atual: '{db_atual}' <<<", flush=True)
        db_status = True
except Exception as e:
    print(f">>> FALHA DE CONEXÃO: {e}", flush=True)

# --- MAPEAMENTO DE COLUNAS ---
DE_PARA = {
    'NUM ENF': 'num_enf', 'LEITO': 'leito', 'NOME ENFERMARIA': 'nome_enfermaria', 
    'STATUS': 'status_leito', 'AIH GERADA PARA O PACIENTE': 'aih_paciente', 
    'NÚMERO DO CNS DO PACIENTE': 'cns_paciente', 'NOME PACIENTE': 'nome_paciente', 
    'SEXO': 'sexo', 'DATA NASC': 'data_nasc', 'IDADE': 'idade', 
    'DATA INTERN': 'data_internacao', 'DATA INTERN LEITO': 'data_internacao_leito', 
    'SUSPEITA COVID': 'suspeita_covid', 'PÓS COVID': 'pos_covid', 
    'MOTIVO IMPEDIMENTO': 'motivo_impedimento', 'DATA IMPEDIMENTO': 'data_impedimento', 
    'DATA SOL. RESERVA': 'data_sol_reserva', 'PREVISÃO INTERN. RESERVA': 'previsao_intern_reserva', 
    'ACOMPANHAMENTO DATA / HORA': 'acompanhamento_data_hora', 'PRONTUÁRIO': 'prontuario', 
    'CID 10': 'cid_10', 'CÓDIGO SER': 'codigo_ser', 'PERFIL': 'perfil', 
    'BOMBA INFUSORA': 'bomba_infusora', 'SUPORTE CIRÚRGICO': 'suporte_cirurgico', 
    'SUPORTE ALIMENTAR': 'suporte_alimentar', 'MODO VENTILATÓRIO': 'modo_ventilatorio', 
    'OBSERVAÇÃO': 'observacao', 'CRÔNICO': 'cronico', 'LONGA PERMANÊNCIA': 'longa_permanencia', 
    'SITUAÇÃO / MOTIVO PERMANÊNCIA': 'situacao_motivo_permanencia', 'GESTANTE': 'gestante', 
    'INDUÇÃO AO PARTO': 'inducao_parto', 'ARBOVIROSE': 'arbovirose', 
    'VIABILIDADE PARA DIÁLISE PERITONEAL': 'viabilidade_dialise_peritoneal', 
    'INFECÇÃO ATIVA E/OU USO DE ANTIBIOTICO': 'infeccao_ativa_antibiotico', 
    'HISTÓRICO DE CIRURGIAS INTRA-ABDOMINAIS': 'historico_cirurgias_abdominais', 
    'DOENÇA NEOPLÁSICA AVANÇADA': 'doenca_neoplasica_avancada', 
    'HÉRNIA INGUINAL A REPARAR': 'hernia_inguinal_reparar', 
    'CONDIÇÕES DE ALTA COM DIÁLISE': 'condicoes_alta_dialise', 
    'ESTÁ INSERIDO NO TRS': 'inserido_no_trs'
}

@app.route('/')
def index():
    if not db_status:
        return render_template('index.html', stats=None, chart_data=[], 
                             error_msg="O servidor não conseguiu conectar no banco na inicialização. Veja os logs.")

    try:
        insp = inspect(engine)
        if not insp.has_table('historico_ocupacao_completo'):
             return render_template('index.html', stats=None, chart_data=[], 
                                   error_msg=f"Conexão OK. A tabela 'historico_ocupacao_completo' ainda não existe. Faça o primeiro upload.")

        with engine.connect() as conn:
            # 1. Busca Histórico
            sql_history = text("""
                SELECT 
                    data_referencia,
                    DATE_FORMAT(data_referencia, '%d/%m/%Y') as data_formatada,
                    COUNT(*) as total,
                    COALESCE(SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END), 0) as ocupados
                FROM historico_ocupacao_completo
                GROUP BY data_referencia
                ORDER BY data_referencia DESC
            """)
            history_list = conn.execute(sql_history).mappings().all()

            # 2. Decide qual data mostrar
            selected_date = request.args.get('data')
            
            if not selected_date and history_list:
                selected_date = history_list[0]['data_referencia']
            
            if not selected_date:
                return render_template('index.html', stats=None, chart_data=[], history=[])

            # 3. Estatísticas
            sql_stats = text("""
                SELECT 
                    COUNT(*) as total,
                    COALESCE(SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END), 0) as ocupados,
                    COALESCE(SUM(CASE WHEN status_leito LIKE '%IMPEDIDO%' OR status_leito LIKE '%BLOQUEADO%' THEN 1 ELSE 0 END), 0) as impedidos,
                        COALESCE(SUM(CASE WHEN status_leito = 'LIVRE' THEN 1 ELSE 0 END), 0) as vagos
                FROM historico_ocupacao_completo
                WHERE data_referencia = :data
            """)
            stats = conn.execute(sql_stats, {"data": selected_date}).mappings().fetchone()
            
            # 4. Gráfico
            sql_chart = text("""
                SELECT 
                    DATE_FORMAT(data_referencia, '%d/%m') as dia,
                    COUNT(*) as total,
                    COALESCE(SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END), 0) as ocupados
                FROM historico_ocupacao_completo
                WHERE data_referencia <= :data
                GROUP BY data_referencia
                ORDER BY data_referencia DESC
                LIMIT 7
            """)
            chart_data = conn.execute(sql_chart, {"data": selected_date}).mappings().all()
            chart_data = list(reversed(chart_data))

            return render_template('index.html', stats=stats, data_ref=selected_date, chart_data=chart_data, history=history_list)
            
    except Exception as e:
        return render_template('index.html', stats=None, chart_data=[], error_msg=f"Erro Geral: {str(e)}")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    data_ref_input = request.form.get('data_referencia') 

    if not file or not data_ref_input:
        flash('Arquivo e Data são obrigatórios.', 'error')
        return redirect(url_for('index'))

    try:
        # --- CORREÇÃO DE DATA (V2) ---
        # Força dayfirst=True para evitar que 05/01 (Jan) vire 01/05 (Maio)
        try:
            dt_obj = pd.to_datetime(data_ref_input, dayfirst=True)
            data_banco = dt_obj.strftime('%Y-%m-%d')  # Formato MySQL (Ano-Mês-Dia)
            data_visual = dt_obj.strftime('%d/%m/%Y') # Formato Visual (Dia/Mês/Ano)
            print(f"Data recebida: {data_ref_input} -> Interpretada como: {data_visual}", flush=True)
        except:
            flash(f'Formato de data inválido: {data_ref_input}', 'error')
            return redirect(url_for('index'))

        # Leitura do CSV
        try:
            df = pd.read_csv(file, encoding='utf-8', sep=',')
        except:
            file.seek(0)
            df = pd.read_csv(file, encoding='latin1', sep=';')

        # ETL
        df_banco = df.rename(columns=DE_PARA)
        cols_uteis = [c for c in df_banco.columns if c in DE_PARA.values()]
        df_banco = df_banco[cols_uteis]
        
        # Usa a data formatada e segura
        df_banco['data_referencia'] = data_banco
        
        # --- LIMPEZA BLINDADA ---
        if 'num_enf' in df_banco.columns:
            df_banco['num_enf'] = pd.to_numeric(df_banco['num_enf'], errors='coerce')
            df_banco = df_banco.dropna(subset=['num_enf'])

        for col in ['cns_paciente', 'prontuario', 'aih_paciente']:
            if col in df_banco.columns:
                df_banco[col] = df_banco[col].astype(str).str.replace(r'\.0$', '', regex=True).replace('nan', None)
        
        for col in df_banco.columns:
            if 'data' in col or 'previsao' in col:
                df_banco[col] = pd.to_datetime(df_banco[col], dayfirst=True, errors='coerce')

        # Gravação
        insp = inspect(engine)
        tabela_existe = insp.has_table('historico_ocupacao_completo')
        
        with engine.begin() as conn:
            if tabela_existe:
                # Remove dados antigos dessa data específica
                conn.execute(text(f"DELETE FROM historico_ocupacao_completo WHERE data_referencia = '{data_banco}'"))
            
            df_banco.to_sql('historico_ocupacao_completo', con=conn, if_exists='append', index=False)

        # MENSAGEM MELHORADA: Mostra a data no formato brasileiro para confirmação
        flash(f'Sucesso! {len(df_banco)} registros importados para o dia {data_visual}.', 'success')
        return redirect(url_for('index', data=data_banco))
        
    except Exception as e:
        print(f"ERRO DE UPLOAD: {e}", flush=True)
        flash(f'Erro técnico: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

# NOVA ROTA PARA O PAINEL
@app.route('/painel')
def painel():
    if not db_status:
        return render_template('painel.html', stats=None, chart_data=[], error_msg="Não conectado ao banco.")
    # Recebe filtros do GET
    periodo_inicio = request.args.get('periodo_inicio')
    periodo_fim = request.args.get('periodo_fim')
    mes = request.args.get('mes')
    dia = request.args.get('dia')
    clinica = request.args.get('clinica')
    predio = request.args.get('predio')
    # Monta cláusulas de filtro
    filtros = []
    params = {}
    if periodo_inicio:
        filtros.append('data_referencia >= :periodo_inicio')
        params['periodo_inicio'] = periodo_inicio
    if periodo_fim:
        filtros.append('data_referencia <= :periodo_fim')
        params['periodo_fim'] = periodo_fim
    if mes:
        filtros.append('MONTH(data_referencia) = :mes')
        params['mes'] = mes
    if dia:
        filtros.append('DAY(data_referencia) = :dia')
        params['dia'] = dia
    if clinica:
        filtros.append('nome_enfermaria = :clinica')
        params['clinica'] = clinica
    if predio:
        filtros.append('predio = :predio')
        params['predio'] = predio
    where_clause = ('WHERE ' + ' AND '.join(filtros)) if filtros else ''
    try:
        with engine.connect() as conn:
            # Indicadores principais com filtros
            sql_stats = text(f"""
                SELECT 
                    COALESCE(SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END), 0) as ocupados,
                    COALESCE(SUM(CASE WHEN status_leito = 'LIVRE' THEN 1 ELSE 0 END), 0) as livres,
                    COALESCE(SUM(CASE WHEN status_leito = 'CEDIDO' THEN 1 ELSE 0 END), 0) as cedidos,
                    COALESCE(SUM(CASE WHEN status_leito LIKE '%IMPEDIDO%' THEN 1 ELSE 0 END), 0) as impedidos,
                    COALESCE(SUM(CASE WHEN status_leito = 'RESERVADO' THEN 1 ELSE 0 END), 0) as reservados,
                    COUNT(*) as total
                FROM historico_ocupacao_completo
                {where_clause}
            """)
            stats = conn.execute(sql_stats, params).mappings().fetchone()

            # Evolução mensal das taxas de ocupação geral
            sql_evolucao = text(f"""
                SELECT DATE_FORMAT(data_referencia, '%Y-%m') as mes,
                    SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END) as ocupados,
                    COUNT(*) as total
                FROM historico_ocupacao_completo
                {where_clause}
                GROUP BY mes
                ORDER BY mes
            """)
            evolucao = conn.execute(sql_evolucao, params).mappings().all()

            # Taxa de ocupação por clínica
            sql_clinica = text(f"""
                SELECT nome_enfermaria,
                    SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END) as ocupados,
                    COUNT(*) as total
                FROM historico_ocupacao_completo
                {where_clause}
                GROUP BY nome_enfermaria
                ORDER BY nome_enfermaria
            """)
            clinicas = conn.execute(sql_clinica, params).mappings().all()

            # Taxa de ocupação por prédio
            sql_predio = text(f"""
                SELECT predio,
                    SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END) as ocupados,
                    COUNT(*) as total
                FROM historico_ocupacao_completo
                {where_clause}
                GROUP BY predio
                ORDER BY predio
            """)
            predios = conn.execute(sql_predio, params).mappings().all()

            return render_template('painel.html', stats=stats, filtros=request.args, evolucao=evolucao, clinicas=clinicas, predios=predios)
    except Exception as e:
        return render_template('painel.html', stats=None, chart_data=[], error_msg=f"Erro: {str(e)}")