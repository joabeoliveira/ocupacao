import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from sqlalchemy import create_engine, text, inspect
import sys
from io import BytesIO
from dotenv import load_dotenv
from VERSION import get_version

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
    return render_template('index.html')

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

# ===== ROTAS API REST =====
@app.route('/api/version')
def api_version():
    """Retorna versão do sistema"""
    return {"version": get_version()}

@app.route('/api/stats')
def api_stats():
    """Retorna estatísticas gerais em JSON"""
    if not db_status:
        return {"error": "Banco não conectado"}, 500
    
    try:
        selected_date = request.args.get('data')
        with engine.connect() as conn:
            # Busca histórico para pegar última data se necessário
            if not selected_date:
                sql_last = text("SELECT data_referencia FROM historico_ocupacao_completo ORDER BY data_referencia DESC LIMIT 1")
                result = conn.execute(sql_last).scalar()
                if result:
                    selected_date = result
                else:
                    return {"error": "Sem dados disponíveis"}, 404
            
            # Estatísticas
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
            
            return {
                "total": int(stats['total']),
                "ocupados": int(stats['ocupados']),
                "impedidos": int(stats['impedidos']),
                "vagos": int(stats['vagos']),
                "data_referencia": str(selected_date)
            }
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/api/chart')
def api_chart():
    """Retorna dados para gráfico de evolução em JSON"""
    if not db_status:
        return {"error": "Banco não conectado"}, 500
    
    try:
        selected_date = request.args.get('data')
        with engine.connect() as conn:
            if not selected_date:
                sql_last = text("SELECT data_referencia FROM historico_ocupacao_completo ORDER BY data_referencia DESC LIMIT 1")
                result = conn.execute(sql_last).scalar()
                if result:
                    selected_date = result
                else:
                    return {"error": "Sem dados disponíveis"}, 404
            
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
            
            return {
                "labels": [row['dia'] for row in chart_data],
                "data": [int(row['ocupados']) for row in chart_data]
            }
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/api/history')
def api_history():
    """Retorna histórico de importações em JSON"""
    if not db_status:
        return {"error": "Banco não conectado"}, 500
    
    try:
        with engine.connect() as conn:
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
            
            return {
                "history": [
                    {
                        "data_referencia": str(row['data_referencia']),
                        "data_formatada": row['data_formatada'],
                        "total": int(row['total']),
                        "ocupados": int(row['ocupados'])
                    }
                    for row in history_list
                ]
            }
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/api/painel/stats')
def api_painel_stats():
    """Retorna estatísticas do painel de ocupação com suporte a filtros"""
    if not db_status:
        return {"error": "Banco não conectado"}, 500
    
    try:
        # Captura filtros da query string
        predio = request.args.get('predio')
        periodo_inicio = request.args.get('periodo_inicio')
        periodo_fim = request.args.get('periodo_fim')
        mes = request.args.get('mes')
        clinica = request.args.get('clinica')
        
        with engine.connect() as conn:
            # Monta condições WHERE dinamicamente
            where_conditions = []
            params = {}
            
            # Filtro de prédio (baseado no num_enf)
            if predio == '1':
                where_conditions.append("num_enf BETWEEN 111 AND 199")
            elif predio == '2':
                where_conditions.append("num_enf BETWEEN 200 AND 299")
            
            # Filtro de período
            if periodo_inicio and periodo_fim:
                where_conditions.append("data_referencia BETWEEN :periodo_inicio AND :periodo_fim")
                params['periodo_inicio'] = periodo_inicio
                params['periodo_fim'] = periodo_fim
            elif not periodo_inicio and not periodo_fim and not mes:
                # Se não tem filtros de data, usa última data
                sql_last_date = text("SELECT MAX(data_referencia) as ultima_data FROM historico_ocupacao_completo")
                ultima_data = conn.execute(sql_last_date).scalar()
                if not ultima_data:
                    return {"error": "Sem dados disponíveis"}, 404
                where_conditions.append("data_referencia = :ultima_data")
                params['ultima_data'] = ultima_data
            
            # Filtro de mês
            if mes:
                where_conditions.append("MONTH(data_referencia) = :mes")
                params['mes'] = mes
            
            # Filtro de clínica
            if clinica:
                where_conditions.append("nome_enfermaria = :clinica")
                params['clinica'] = clinica
            
            # Monta SQL com WHERE dinâmico
            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
            
            sql_stats = text(f"""
                SELECT 
                    COALESCE(SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END), 0) as ocupados,
                    COALESCE(SUM(CASE WHEN status_leito = 'LIVRE' THEN 1 ELSE 0 END), 0) as livres,
                    COALESCE(SUM(CASE WHEN status_leito = 'CEDIDO' THEN 1 ELSE 0 END), 0) as cedidos,
                    COALESCE(SUM(CASE WHEN status_leito LIKE '%IMPEDIDO%' THEN 1 ELSE 0 END), 0) as impedidos,
                    COALESCE(SUM(CASE WHEN status_leito = 'RESERVADO' THEN 1 ELSE 0 END), 0) as reservados,
                    COUNT(*) as total
                FROM historico_ocupacao_completo
                WHERE {where_clause}
            """)
            stats = conn.execute(sql_stats, params).mappings().fetchone()
            
            return {
                "ocupados": int(stats['ocupados']),
                "livres": int(stats['livres']),
                "cedidos": int(stats['cedidos']),
                "impedidos": int(stats['impedidos']),
                "reservados": int(stats['reservados']),
                "total": int(stats['total'])
            }
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/api/painel/evolucao')
def api_painel_evolucao():
    """Retorna evolução mensal para gráfico com suporte a filtros"""
    if not db_status:
        return {"error": "Banco não conectado"}, 500
    
    try:
        # Captura filtros
        predio = request.args.get('predio')
        periodo_inicio = request.args.get('periodo_inicio')
        periodo_fim = request.args.get('periodo_fim')
        mes = request.args.get('mes')
        clinica = request.args.get('clinica')
        
        with engine.connect() as conn:
            # Monta condições WHERE
            where_conditions = []
            params = {}
            
            # Filtro de prédio
            if predio == '1':
                where_conditions.append("num_enf BETWEEN 111 AND 199")
            elif predio == '2':
                where_conditions.append("num_enf BETWEEN 200 AND 299")
            
            if periodo_inicio and periodo_fim:
                where_conditions.append("data_referencia BETWEEN :periodo_inicio AND :periodo_fim")
                params['periodo_inicio'] = periodo_inicio
                params['periodo_fim'] = periodo_fim
            
            if mes:
                where_conditions.append("MONTH(data_referencia) = :mes")
                params['mes'] = mes
            
            if clinica:
                where_conditions.append("nome_enfermaria = :clinica")
                params['clinica'] = clinica
            
            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
            
            sql_evolucao = text(f"""
                SELECT DATE_FORMAT(data_referencia, '%Y-%m') as mes,
                    SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END) as ocupados,
                    COUNT(*) as total
                FROM historico_ocupacao_completo
                WHERE {where_clause}
                GROUP BY mes
                ORDER BY mes
            """)
            evolucao = conn.execute(sql_evolucao, params).mappings().all()
            
            return {
                "labels": [row['mes'] for row in evolucao],
                "data": [round((int(row['ocupados']) / int(row['total'])) * 100, 1) for row in evolucao]
            }
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/api/painel/clinicas')
def api_painel_clinicas():
    """Retorna dados por clínica com suporte a filtros"""
    if not db_status:
        return {"error": "Banco não conectado"}, 500
    
    try:
        # Captura filtros
        predio = request.args.get('predio')
        periodo_inicio = request.args.get('periodo_inicio')
        periodo_fim = request.args.get('periodo_fim')
        mes = request.args.get('mes')
        clinica = request.args.get('clinica')
        
        with engine.connect() as conn:
            # Monta condições WHERE
            where_conditions = []
            params = {}
            
            # Filtro de prédio
            if predio == '1':
                where_conditions.append("num_enf BETWEEN 111 AND 199")
            elif predio == '2':
                where_conditions.append("num_enf BETWEEN 200 AND 299")
            
            where_conditions = []
            params = {}
            
            if periodo_inicio and periodo_fim:
                where_conditions.append("data_referencia BETWEEN :periodo_inicio AND :periodo_fim")
                params['periodo_inicio'] = periodo_inicio
                params['periodo_fim'] = periodo_fim
            
            if mes:
                where_conditions.append("MONTH(data_referencia) = :mes")
                params['mes'] = mes
            
            if clinica:
                where_conditions.append("nome_enfermaria = :clinica")
                params['clinica'] = clinica
            
            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
            
            sql_clinica = text(f"""
                SELECT nome_enfermaria,
                    SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END) as ocupados,
                    COUNT(*) as total
                FROM historico_ocupacao_completo
                WHERE {where_clause}
                GROUP BY nome_enfermaria
                ORDER BY nome_enfermaria
            """)
            clinicas = conn.execute(sql_clinica, params).mappings().all()
            
            return {
                "labels": [row['nome_enfermaria'] for row in clinicas],
                "data": [round((int(row['ocupados']) / int(row['total'])) * 100, 1) for row in clinicas]
            }
    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/api/tempo_permanencia')
def api_tempo_permanencia():
    """Retorna métricas e lista de pacientes por tempo de permanência"""
    if not db_status:
        return {"error": "Banco não conectado"}, 500

    try:
        # filtros
        selected_date = request.args.get('data_referencia')
        periodo_inicio = request.args.get('periodo_inicio')
        periodo_fim = request.args.get('periodo_fim')
        clinica = request.args.get('clinica')
        predio = request.args.get('predio')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))

        with engine.connect() as conn:
            # escolhe data se não informada
            if not selected_date:
                sql_last = text("SELECT MAX(data_referencia) FROM historico_ocupacao_completo")
                selected_date = conn.execute(sql_last).scalar()
                if not selected_date:
                    return {"error": "Sem dados disponíveis"}, 404

            # Monta filtros WHERE para a seleção de pacientes ocupados na data
            where_conditions = ["data_referencia = :data_referencia", "status_leito = 'OCUPADO'"]
            params = {"data_referencia": selected_date}

            if clinica:
                where_conditions.append("nome_enfermaria = :clinica")
                params['clinica'] = clinica

            if predio == '1':
                where_conditions.append("num_enf BETWEEN 111 AND 199")
            elif predio == '2':
                where_conditions.append("num_enf BETWEEN 200 AND 299")

            # período filtrado por data_referencia (aplica quando informado)
            if periodo_inicio and periodo_fim:
                where_conditions = ["data_referencia BETWEEN :periodo_inicio AND :periodo_fim", "status_leito = 'OCUPADO'"]
                params = {'periodo_inicio': periodo_inicio, 'periodo_fim': periodo_fim}

            where_clause = " AND ".join(where_conditions)

            # Consulta por paciente (agrupa por identificador preferencialmente pelo prontuário)
            sql_patients = text(f"""
                SELECT
                    COALESCE(prontuario, cns_paciente, nome_paciente) as patient_id,
                    MIN(data_internacao) as data_internacao,
                    MAX(nome_paciente) as nome_paciente,
                    MAX(prontuario) as prontuario,
                    MAX(idade) as idade,
                    MAX(sexo) as sexo,
                    MAX(nome_enfermaria) as nome_enfermaria,
                    TIMESTAMPDIFF(DAY, MIN(data_internacao), :data_referencia) as dias
                FROM historico_ocupacao_completo
                WHERE {where_clause}
                GROUP BY patient_id
                ORDER BY dias DESC
            """)

            rows = conn.execute(sql_patients, params).mappings().all()

            # Transforma em lista python
            patients = []
            dias_list = []
            for r in rows:
                dias = int(r['dias']) if r['dias'] is not None else 0
                dias_list.append(dias)
                patients.append({
                    'patient_id': r['patient_id'],
                    'nome': r['nome_paciente'] or '',
                    'prontuario': r['prontuario'],
                    'idade': int(r['idade']) if r['idade'] is not None else None,
                    'sexo': r['sexo'],
                    'clinica': r['nome_enfermaria'],
                    'data_internacao': str(r['data_internacao']) if r['data_internacao'] is not None else None,
                    'dias': dias
                })

            total = len(patients)
            avg_los = round(sum(dias_list) / total, 1) if total > 0 else 0

            # Mediana em Python
            median_los = 0
            if total > 0:
                sorted_days = sorted(dias_list)
                mid = total // 2
                if total % 2 == 0:
                    median_los = int((sorted_days[mid - 1] + sorted_days[mid]) / 2)
                else:
                    median_los = int(sorted_days[mid])

            # Counters
            long_gt_30 = sum(1 for d in dias_list if d > 30)
            long_gt_30_60 = sum(1 for p, d in zip(patients, dias_list) if d > 30 and (p.get('idade') or 0) >= 60)
            long_gt_30_ped = sum(1 for p, d in zip(patients, dias_list) if d > 30 and (p.get('idade') is not None and p.get('idade') < 18))

            # Histogram buckets
            buckets = {'0-7': 0, '8-14': 0, '15-30': 0, '31-60': 0, '61-90': 0, '>90': 0}
            for d in dias_list:
                if d <= 7:
                    buckets['0-7'] += 1
                elif d <= 14:
                    buckets['8-14'] += 1
                elif d <= 30:
                    buckets['15-30'] += 1
                elif d <= 60:
                    buckets['31-60'] += 1
                elif d <= 90:
                    buckets['61-90'] += 1
                else:
                    buckets['>90'] += 1

            # Paginação
            start = (page - 1) * per_page
            end = start + per_page
            page_items = patients[start:end]

            # Mask names for frontend display (keep full name available only for export endpoint)
            def mask_name(full):
                if not full:
                    return ''
                parts = full.split()
                if len(parts) == 1:
                    s = parts[0]
                    if len(s) <= 2:
                        return s[0] + '*'
                    return s[0] + '*'*(len(s)-2) + s[-1]
                # first name + last initial
                first = parts[0]
                last = parts[-1]
                return f"{first} {last[0]}."

            for it in page_items:
                it['nome_masked'] = mask_name(it['nome'])

            return jsonify({
                'data_referencia': str(selected_date),
                'total_patients': total,
                'avg_los': avg_los,
                'median_los': median_los,
                'long_gt_30': long_gt_30,
                'long_gt_30_60': long_gt_30_60,
                'long_gt_30_ped': long_gt_30_ped,
                'histogram': buckets,
                'page': page,
                'per_page': per_page,
                'patients': page_items
            })

    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/api/tempo_permanencia/export')
def api_tempo_permanencia_export():
    """Exporta a lista completa de longa permanência (>30 dias) em Excel (full names)"""
    if not db_status:
        return {"error": "Banco não conectado"}, 500

    try:
        selected_date = request.args.get('data_referencia')
        clinica = request.args.get('clinica')
        predio = request.args.get('predio')

        with engine.connect() as conn:
            if not selected_date:
                sql_last = text("SELECT MAX(data_referencia) FROM historico_ocupacao_completo")
                selected_date = conn.execute(sql_last).scalar()
                if not selected_date:
                    return {"error": "Sem dados disponíveis"}, 404

            where_conditions = ["data_referencia = :data_referencia", "status_leito = 'OCUPADO'"]
            params = {"data_referencia": selected_date}
            if clinica:
                where_conditions.append("nome_enfermaria = :clinica")
                params['clinica'] = clinica
            if predio == '1':
                where_conditions.append("num_enf BETWEEN 111 AND 199")
            elif predio == '2':
                where_conditions.append("num_enf BETWEEN 200 AND 299")

            where_clause = " AND ".join(where_conditions)

            sql_export = text(f"""
                SELECT
                    COALESCE(prontuario, cns_paciente, nome_paciente) as patient_id,
                    MIN(data_internacao) as data_internacao,
                    MAX(nome_paciente) as nome_paciente,
                    MAX(prontuario) as prontuario,
                    MAX(idade) as idade,
                    MAX(sexo) as sexo,
                    MAX(nome_enfermaria) as nome_enfermaria,
                    TIMESTAMPDIFF(DAY, MIN(data_internacao), :data_referencia) as dias
                FROM historico_ocupacao_completo
                WHERE {where_clause}
                GROUP BY patient_id
                HAVING dias > 30
                ORDER BY dias DESC
            """)

            rows = conn.execute(sql_export, params).mappings().all()
            # Converte para DataFrame
            df = pd.DataFrame([{
                'Nome': r['nome_paciente'],
                'Prontuario': r['prontuario'],
                'Idade': int(r['idade']) if r['idade'] is not None else None,
                'Sexo': r['sexo'],
                'Clinica': r['nome_enfermaria'],
                'Data Internacao': r['data_internacao'],
                'Dias Internado': int(r['dias'])
            } for r in rows])

            output = BytesIO()
            # Escreve Excel
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='LongaPermanencia')
            output.seek(0)

            filename = f"longa_permanencia_{selected_date}.xlsx"
            return send_file(output, download_name=filename, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    except Exception as e:
        return {"error": str(e)}, 500

# ROTA PARA O PAINEL (renderiza template estático)
@app.route('/painel')
def painel():
    return render_template('painel.html')


@app.route('/tempo_permanencia')
def tempo_permanencia():
    return render_template('tempo_permanencia.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)