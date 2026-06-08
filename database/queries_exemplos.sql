-- Arquivo: queries_exemplos.sql
-- Objetivo: consultas exemplo para facilitar análises sobre a tabela
-- `historico_ocupacao_completo` (MySQL)
-- Uso: abra no seu cliente MySQL e substitua parâmetros conforme necessário.

/*
Recomendações de índices (avaliar antes de aplicar em ambiente de produção):
CREATE INDEX idx_prontuario ON historico_ocupacao_completo(prontuario);
CREATE INDEX idx_codigo_ser ON historico_ocupacao_completo(codigo_ser);
CREATE INDEX idx_nome_enfermaria ON historico_ocupacao_completo(nome_enfermaria);
*/

-- 1) Contagem diária de leitos por status
SELECT
  data_referencia,
  status_leito,
  COUNT(*) AS qtd
FROM historico_ocupacao_completo
GROUP BY data_referencia, status_leito
ORDER BY data_referencia DESC, status_leito;

-- 2) Taxa de ocupação por enfermaria (percentual de 'OCUPADO')
SELECT
  data_referencia,
  nome_enfermaria,
  SUM(status_leito = 'OCUPADO') AS ocupados,
  COUNT(*) AS total,
  ROUND(100 * SUM(status_leito = 'OCUPADO') / NULLIF(COUNT(*),0), 2) AS pct_ocupacao
FROM historico_ocupacao_completo
GROUP BY data_referencia, nome_enfermaria
ORDER BY data_referencia DESC, pct_ocupacao DESC;

-- 3) Último registro por leito (estado mais recente por num_enf+leito)
SELECT t.*
FROM historico_ocupacao_completo t
JOIN (
  SELECT num_enf, leito, MAX(data_referencia) AS max_data
  FROM historico_ocupacao_completo
  GROUP BY num_enf, leito
) m ON t.num_enf = m.num_enf AND t.leito = m.leito AND t.data_referencia = m.max_data;

-- 4) Pacientes com longa permanência (ex.: > 14 dias no leito) — calcula diferença entre data_referencia e data_internacao_leito
SELECT
  nome_paciente,
  prontuario,
  num_enf,
  leito,
  data_internacao_leito,
  data_referencia,
  DATEDIFF(data_referencia, DATE(data_internacao_leito)) AS dias_no_leito
FROM historico_ocupacao_completo
WHERE data_internacao_leito IS NOT NULL
  AND DATEDIFF(data_referencia, DATE(data_internacao_leito)) > 14
ORDER BY dias_no_leito DESC
LIMIT 200;

-- 5) Média de permanência por perfil (aproximação usando data_internacao → data_referencia)
SELECT
  perfil,
  ROUND(AVG(DATEDIFF(data_referencia, DATE(data_internacao))),2) AS media_dias
FROM historico_ocupacao_completo
WHERE data_internacao IS NOT NULL
GROUP BY perfil
ORDER BY media_dias DESC;

-- 6) Buscar histórico de um prontuário específico (troque 'PRONT123' pelo valor real)
SELECT *
FROM historico_ocupacao_completo
WHERE prontuario = 'PRONT123'
ORDER BY data_referencia DESC
LIMIT 200;

-- 7) Pacientes únicos atendidos num período
SELECT COUNT(DISTINCT prontuario) AS pacientes_unicos
FROM historico_ocupacao_completo
WHERE data_referencia BETWEEN '2025-01-01' AND '2025-12-31';

-- 8) Distribuição de status por perfil (mais útil para dashboards)
SELECT
  perfil,
  status_leito,
  COUNT(*) AS qtd
FROM historico_ocupacao_completo
GROUP BY perfil, status_leito
ORDER BY perfil, qtd DESC;

-- 9) Exemplo de view para facilitar dashboards: ocupacao diária por enfermaria
-- CREATE OR REPLACE VIEW vw_ocupacao_diaria_enfermaria AS
-- SELECT data_referencia, nome_enfermaria,
--   SUM(status_leito = 'OCUPADO') AS ocupados,
--   COUNT(*) AS total,
--   ROUND(100 * SUM(status_leito = 'OCUPADO') / NULLIF(COUNT(*),0),2) AS pct_ocupacao
-- FROM historico_ocupacao_completo
-- GROUP BY data_referencia, nome_enfermaria;

-- 10) Query de sanity-check: linhas com data_internacao > data_referencia (provável erro)
SELECT *
FROM historico_ocupacao_completo
WHERE data_internacao IS NOT NULL
  AND data_referencia IS NOT NULL
  AND DATE(data_internacao) > data_referencia
LIMIT 200;

-- 11) Consulta por período: nome, idade, sexo, clínica, data_internacao e dias internado
-- Parâmetros: substitua '2025-01-01' e '2025-01-31' pelos valores desejados
-- Observação: usamos `nome_enfermaria` como campo de clínica/enfermaria
SELECT
  h.prontuario,
  h.nome_paciente AS nome,
  h.idade,
  h.sexo,
  h.nome_enfermaria AS clinica,
  MIN(h.data_internacao) AS data_internacao,
  DATEDIFF(
    LEAST(MAX(h.data_referencia), CAST('2026-04-27' AS DATE)),
    MIN(h.data_internacao)
  ) AS dias_internado
FROM historico_ocupacao_completo h
WHERE h.data_referencia BETWEEN CAST('2026-01-01' AS DATE) AND CAST('2026-04-27' AS DATE)
  AND h.data_internacao IS NOT NULL
GROUP BY h.prontuario, h.nome_paciente, h.idade, h.sexo, h.nome_enfermaria
ORDER BY dias_internado DESC
LIMIT 500;


-- Versão robusta (calcula apenas os dias dentro do período e filtra resultados sem sobreposição; conta dias inclusivos com +1 — remova +1 se não quiser incluir ambos extremos):

SET @start = '2026-01-01';
SET @end   = '2026-04-27';

SELECT
  h.prontuario,
  h.nome_paciente AS nome,
  h.idade,
  h.sexo,
  h.nome_enfermaria AS clinica,
  GREATEST(DATE(MIN(h.data_internacao)), @start) AS inicio_periodo,
  LEAST(DATE(MAX(h.data_referencia)), @end) AS fim_periodo,
  DATEDIFF(
    LEAST(DATE(MAX(h.data_referencia)), @end),
    GREATEST(DATE(MIN(h.data_internacao)), @start)
  ) + 1 AS dias_internado
FROM historico_ocupacao_completo h
WHERE h.data_referencia BETWEEN @start AND @end
  AND h.data_internacao IS NOT NULL
GROUP BY h.prontuario, h.nome_paciente, h.idade, h.sexo, h.nome_enfermaria
HAVING dias_internado > 0
ORDER BY dias_internado DESC
LIMIT 500;

-- Fim do arquivo

  -- =====================================================
  -- Novas consultas adicionadas em 13/05/2026
  -- 12) Internações por data de internação (01/05/2026 a 08/05/2026) — Painel por prédio (colunas fixas)
  -- Retorna uma linha por dia com totais para Prédio 1 e Prédio 2
  WITH RECURSIVE dias AS (
    SELECT DATE('2026-05-01') AS dia
    UNION ALL
    SELECT DATE_ADD(dia, INTERVAL 1 DAY)
    FROM dias
    WHERE dia < DATE('2026-05-08')
  ),
  internacoes_unicas AS (
    SELECT DISTINCT
      DATE(h.data_internacao) AS dia,
      CASE
        WHEN h.num_enf BETWEEN 111 AND 199 THEN 'Predio 1'
        WHEN h.num_enf BETWEEN 200 AND 299 THEN 'Predio 2'
        ELSE 'Fora'
      END AS predio,
      CONCAT_WS('|',
        COALESCE(h.prontuario, ''),
        COALESCE(h.cns_paciente, ''),
        COALESCE(h.nome_paciente, ''),
        DATE_FORMAT(h.data_internacao, '%Y-%m-%d %H:%i:%s')
      ) AS chave_internacao
    FROM historico_ocupacao_completo h
    WHERE h.data_internacao >= '2026-05-01'
      AND h.data_internacao <  '2026-05-09'
      AND h.num_enf BETWEEN 111 AND 299
  ),
  agregado AS (
    SELECT
      dia,
      SUM(CASE WHEN predio = 'Predio 1' THEN 1 ELSE 0 END) AS predio_1_total,
      SUM(CASE WHEN predio = 'Predio 2' THEN 1 ELSE 0 END) AS predio_2_total
    FROM internacoes_unicas
    GROUP BY dia
  )
  SELECT
    d.dia,
    COALESCE(a.predio_1_total, 0) AS predio_1_total,
    COALESCE(a.predio_2_total, 0) AS predio_2_total,
    COALESCE(a.predio_1_total, 0) + COALESCE(a.predio_2_total, 0) AS total_geral_dia
  FROM dias d
  LEFT JOIN agregado a ON a.dia = d.dia
  ORDER BY d.dia;

  -- 13) Internações diárias por prédio e clínica (detalhado)
  -- Retorna linhas dia x prédio x clínica com total de internados (01/05/2026 a 08/05/2026)
  WITH RECURSIVE dias AS (
    SELECT DATE('2026-05-01') AS dia
    UNION ALL
    SELECT DATE_ADD(dia, INTERVAL 1 DAY)
    FROM dias
    WHERE dia < DATE('2026-05-08')
  ),
  internacoes_unicas AS (
    SELECT DISTINCT
      DATE(h.data_internacao) AS dia,
      CASE
        WHEN h.num_enf BETWEEN 111 AND 199 THEN 'Predio 1'
        WHEN h.num_enf BETWEEN 200 AND 299 THEN 'Predio 2'
        ELSE 'Fora'
      END AS predio,
      h.nome_enfermaria AS clinica,
      CONCAT_WS('|',
        COALESCE(h.prontuario, ''),
        COALESCE(h.cns_paciente, ''),
        COALESCE(h.nome_paciente, ''),
        DATE_FORMAT(h.data_internacao, '%Y-%m-%d %H:%i:%s')
      ) AS chave_internacao
    FROM historico_ocupacao_completo h
    WHERE h.data_internacao >= '2026-05-01'
      AND h.data_internacao <  '2026-05-09'
      AND h.num_enf BETWEEN 111 AND 299
  ),
  agregado AS (
    SELECT
      dia,
      predio,
      clinica,
      COUNT(*) AS total_internados
    FROM internacoes_unicas
    WHERE predio IN ('Predio 1', 'Predio 2')
    GROUP BY dia, predio, clinica
  )
  SELECT
    d.dia,
    a.predio,
    a.clinica,
    COALESCE(a.total_internados, 0) AS total_internados_no_dia
  FROM dias d
  LEFT JOIN agregado a ON a.dia = d.dia
  ORDER BY d.dia, a.predio, a.clinica;

  -- =====================================================
