import csv, os
from datetime import datetime, date
fn = os.path.join(os.getcwd(), 'api_looker_studio', 'taxa de ocupacao - dados brutos geral copia - dados_SMSRio (1).csv')
SNAPSHOT_DATE = date(2026,4,8)

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

count_le17 = 0
lines = []
with open(fn, encoding='utf-8', errors='replace', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    h = [x.strip().upper() for x in header]
    idx_idade = None
    idx_datanasc = None
    for i,name in enumerate(h):
        if name == 'IDADE': idx_idade = i
        if name == 'DATA NASC': idx_datanasc = i
    for lineno, row in enumerate(reader, start=2):
        age = None
        if idx_idade is not None and idx_idade < len(row):
            try:
                age = int(row[idx_idade])
            except Exception:
                age = None
        if age is None and idx_datanasc is not None and idx_datanasc < len(row):
            dn = try_parse_date(row[idx_datanasc])
            if dn is not None:
                bdate = dn.date()
                ay = SNAPSHOT_DATE.year - bdate.year - ((SNAPSHOT_DATE.month, SNAPSHOT_DATE.day) < (bdate.month, bdate.day))
                age = ay
        if age is not None and age <= 17:
            count_le17 += 1
            lines.append((lineno, age, row))

print('total registros com idade <=17:', count_le17)
# opcional: mostrar primeiras linhas
for item in lines[:20]:
    print(item[0], item[1])
os.makedirs('outputs', exist_ok=True)
outf = os.path.join('outputs','pacientes_le17.csv')
with open(outf, 'w', encoding='utf-8', newline='') as of:
    import csv
    w = csv.writer(of)
    # escrever header original + coluna LINENO + IDADE_CALCULADA
    with open(fn, encoding='utf-8', errors='replace', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
    w.writerow(['LINENO','IDADE_CALCULADA'] + header)
    for lineno, age, row in lines:
        w.writerow([lineno, age] + row)
print('exportado para', outf)
