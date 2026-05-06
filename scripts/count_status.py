import csv, os

fn = os.path.join(os.getcwd(), 'api_looker_studio', 'taxa de ocupacao - dados brutos geral copia - dados_SMSRio (1).csv')
counts = {'OCUPADO':0,'LIVRE':0,'CEDIDO':0,'IMPEDIDO':0,'RESERVADO':0}

with open(fn, encoding='utf-8', errors='replace', newline='') as f:
    reader = csv.reader(f)
    import csv, os
    from datetime import datetime, date

    fn = os.path.join(os.getcwd(), 'api_looker_studio', 'taxa de ocupacao - dados brutos geral copia - dados_SMSRio (1).csv')

    # data de snapshot informada pelo usuário
    SNAPSHOT_DATE = date(2026, 4, 8)

    status_counts = {}
    reserved_lines = set()

    # métricas pedidas
    ocupado = 0
    livre = 0
    cedido = 0
    impedido = 0
    reservado = 0

    patients_60_plus = 0
    patients_le_17 = 0
    patients_female = 0
    patients_male = 0
    long_stay_gt15 = 0
    long_stay_gt15_60plus = 0

    def try_parse_date(s):
        s = s.strip()
        if not s:
            return None
        formats = ['%d/%m/%Y %H:%M', '%d/%m/%Y %H:%M:%S', '%d/%m/%Y']
        for fmt in formats:
            try:
                return datetime.strptime(s, fmt)
            except Exception:
                continue
        return None

    with open(fn, encoding='utf-8', errors='replace', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        h = [x.strip().upper() for x in header]

        def idx(name):
            try:
                return h.index(name)
            except ValueError:
                return None

        idx_status = idx('STATUS')
        idx_idade = idx('IDADE')
        idx_sexo = idx('SEXO')
        idx_data_nasc = idx('DATA NASC')
        idx_data_intern = None
        # procurar coluna DATA INTERN (pode ter variações)
        for cname in ('DATA INTERN', 'DATA INTERN LEITO', 'DATA INTERN LEITO'):
            if cname in h:
                idx_data_intern = h.index(cname)
                break
        # columns que indicam reserva
        reserva_idxs = [i for i, name in enumerate(h) if 'RESERVA' in name]

        total_rows = 0
        for lineno, row in enumerate(reader, start=2):
            total_rows += 1
            status = ''
            if idx_status is not None and idx_status < len(row):
                status = row[idx_status].strip().upper()

            status_counts[status] = status_counts.get(status, 0) + 1

            if status == 'OCUPADO':
                ocupado += 1
            elif status == 'LIVRE':
                livre += 1
            elif status == 'CEDIDO':
                cedido += 1
            elif status == 'IMPEDIDO':
                impedido += 1

            # reservado: considerar qualquer coluna de reserva preenchida (contar linha apenas 1 vez)
            for i in reserva_idxs:
                if i < len(row) and row[i].strip() != '':
                    reserved_lines.add(lineno)
                    break

            # métricas por paciente — considerar somente leitos ocupados
            if status == 'OCUPADO':
                # idade
                age = None
                if idx_idade is not None and idx_idade < len(row):
                    try:
                        age = int(row[idx_idade])
                    except Exception:
                        age = None
                # fallback: calcular idade a partir de DATA NASC se disponível
                if age is None and idx_data_nasc is not None and idx_data_nasc < len(row):
                    dn = try_parse_date(row[idx_data_nasc])
                    if dn is not None:
                        bdate = dn.date()
                        # cálculo de anos completos
                        ay = SNAPSHOT_DATE.year - bdate.year - ((SNAPSHOT_DATE.month, SNAPSHOT_DATE.day) < (bdate.month, bdate.day))
                        age = ay
                if age is not None:
                    if age >= 60:
                        patients_60_plus += 1
                    if age <= 17:
                        patients_le_17 += 1

                # sexo
                if idx_sexo is not None and idx_sexo < len(row):
                    sx = row[idx_sexo].strip().upper()
                    if sx == 'F':
                        patients_female += 1
                    elif sx == 'M':
                        patients_male += 1

                # permanência (>15 dias) calculada pela diferença entre SNAPSHOT_DATE e DATA INTERN
                if idx_data_intern is not None and idx_data_intern < len(row):
                    din = try_parse_date(row[idx_data_intern])
                    if din is not None:
                        days = (SNAPSHOT_DATE - din.date()).days
                        if days > 15:
                            long_stay_gt15 += 1
                            if age is not None and age >= 60:
                                long_stay_gt15_60plus += 1

        reservado = len(reserved_lines)

    occupation_rate = (ocupado / total_rows * 100) if total_rows > 0 else 0
    percent_impedido = (impedido / total_rows * 100) if total_rows > 0 else 0

    out_lines = [
        ['metric', 'value'],
        ['data_snapshot', SNAPSHOT_DATE.isoformat()],
        ['total_leitos', str(total_rows)],
        ['ocupado', str(ocupado)],
        ['livre', str(livre)],
        ['cedido', str(cedido)],
        ['impedido', str(impedido)],
        ['reservado', str(reservado)],
        ['taxa_ocupacao_geral_pct', f"{occupation_rate:.2f}"],
        ['percentual_leitos_impedidos_pct', f"{percent_impedido:.2f}"],
        ['pacientes_60_plus', str(patients_60_plus)],
        ['pacientes_le_17', str(patients_le_17)],
        ['pacientes_feminino', str(patients_female)],
        ['pacientes_masculino', str(patients_male)],
        ['longa_permanencia_gt15', str(long_stay_gt15)],
        ['longa_permanencia_gt15_60plus', str(long_stay_gt15_60plus)],
    ]

    os.makedirs('outputs', exist_ok=True)
    outfn = os.path.join('outputs', f'summary_{SNAPSHOT_DATE.isoformat()}.csv')
    with open(outfn, 'w', encoding='utf-8', newline='') as of:
        w = csv.writer(of)
        w.writerows(out_lines)

    print('Resumo salvo em', outfn)
    for k, v in out_lines[2:]:
        print(f"{k}: {v}")
