import csv, os
fn = os.path.join(os.getcwd(), 'api_looker_studio', 'taxa de ocupacao - dados brutos geral copia - dados_SMSRio (1).csv')
rows_with = []
with open(fn, encoding='utf-8', errors='replace', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    h = [x.strip().upper() for x in header]
    reserva_idxs = [i for i,name in enumerate(h) if 'RESERVA' in name]
    print('colunas reserva encontradas:', [header[i] for i in reserva_idxs])
    for lineno, row in enumerate(reader, start=2):
        for i in reserva_idxs:
            if i < len(row) and row[i].strip() != '':
                rows_with.append((lineno, i, row[i].strip(), row))
                break

print('linhas com reserva (count):', len(rows_with))
for lineno, idx, val, row in rows_with:
    print(lineno, header[idx], val)
