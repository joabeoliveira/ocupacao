Trechos SQL relevantes extraídos do repositório

1) Trecho usado em n8n (backfill e diário):

SELECT
  DATE_FORMAT(MIN(data_referencia), '%d/%m/%Y') AS data,
  COUNT(*) AS total_registros,
  SUM(CASE WHEN LOWER(status_leito) = 'ocupado' THEN 1 ELSE 0 END) AS ocupado,
  SUM(CASE WHEN LOWER(status_leito) = 'livre' THEN 1 ELSE 0 END) AS livre,
  SUM(CASE WHEN LOWER(status_leito) = 'cedido' THEN 1 ELSE 0 END) AS cedido,
  SUM(CASE WHEN LOWER(status_leito) = 'impedido' THEN 1 ELSE 0 END) AS impedido,
  SUM(CASE WHEN LOWER(status_leito) = 'reservado' THEN 1 ELSE 0 END) AS reservado,
  ROUND(100.0 * SUM(CASE WHEN LOWER(status_leito) = 'ocupado' THEN 1 ELSE 0 END) / NULLIF(COUNT(*),0),2) AS taxa_ocupacao_pct,
  ROUND(100.0 * SUM(CASE WHEN LOWER(status_leito) = 'impedido' THEN 1 ELSE 0 END) / NULLIF(COUNT(*),0),2) AS percentual_impedidos_pct,
  ...
FROM historico_ocupacao_completo
WHERE DATE(data_referencia) BETWEEN STR_TO_DATE('{{$json.start_date}}', '%Y-%m-%d') AND STR_TO_DATE('{{$json.end_date}}', '%Y-%m-%d')
GROUP BY DATE(data_referencia)
ORDER BY DATE(data_referencia);

2) `/api/painel/stats` (app.py):

SELECT 
    COALESCE(SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END), 0) as ocupados,
    COALESCE(SUM(CASE WHEN status_leito = 'LIVRE' THEN 1 ELSE 0 END), 0) as livres,
    COALESCE(SUM(CASE WHEN status_leito = 'CEDIDO' THEN 1 ELSE 0 END), 0) as cedidos,
    COALESCE(SUM(CASE WHEN status_leito LIKE '%IMPEDIDO%' THEN 1 ELSE 0 END), 0) as impedidos,
    COALESCE(SUM(CASE WHEN status_leito = 'RESERVADO' THEN 1 ELSE 0 END), 0) as reservados,
    COUNT(*) as total
FROM historico_ocupacao_completo
WHERE {where_clause}

3) `/api/painel/evolucao` (app.py):

SELECT DATE_FORMAT(data_referencia, '%Y-%m') as mes,
    SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END) as ocupados,
    COUNT(*) as total
FROM historico_ocupacao_completo
WHERE {where_clause}
GROUP BY mes
ORDER BY mes

4) `/api/painel/clinicas` (app.py):

SELECT nome_enfermaria,
    SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END) as ocupados,
    COUNT(*) as total
FROM historico_ocupacao_completo
WHERE {where_clause}
GROUP BY nome_enfermaria
ORDER BY nome_enfermaria

5) `/api/painel/impedimentos` (app.py):

SELECT COALESCE(NULLIF(TRIM(motivo_impedimento), ''), 'Sem motivo informado') as motivo,
       COUNT(*) as cnt
FROM historico_ocupacao_completo
WHERE {where_clause}
GROUP BY motivo
ORDER BY cnt DESC
LIMIT 20

Observações rápidas:
- n8n usa `LOWER(status_leito)` e `NULLIF(COUNT(*),0)` — práticas que evitam erros de capitalização e divisão por zero.
- app.py costuma usar comparações exatas (`status_leito = 'OCUPADO'`) e em alguns casos `LIKE '%IMPEDIDO%'`.
- Há endpoints no frontend que dependem de `/api/disponibilidade` (não localizado em `app.py`) — verificação necessária.
