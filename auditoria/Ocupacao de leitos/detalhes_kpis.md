Auditoria detalhada — KPIs e gráficos

Resumo rápido (origem das métricas)
- Frontend: `templates/painel.html` e `templates/disponibilidade.html` fazem fetch para endpoints REST em `app.py`:
  - `/api/painel/stats`  → cards e indicadores principais
  - `/api/painel/evolucao` → gráfico `Evolução Mensal da Ocupação`
  - `/api/painel/clinicas` → gráfico `Taxa de Ocupação por Clínica`
  - `/api/painel/impedimentos` → top motivos (disponibilidade)
  - `/api/disponibilidade` → conjuntos de séries para o gráfico de disponibilidade (frontend)
- Pipeline n8n (`api_looker_studio/n8n_workflow_looker_studio.json`) também gera indicadores e planilha `indicadores` usando a tabela `historico_ocupacao_completo`.

1) KPI: Ocupados (cards)
- Endpoint: `/api/painel/stats`
- SQL (fonte):
  SELECT COALESCE(SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END), 0) as ocupados, ... COUNT(*) as total FROM historico_ocupacao_completo WHERE {where_clause}
- Com filtros: where_clause inclui `num_enf` (prédio), `data_referencia BETWEEN :periodo_inicio AND :periodo_fim` (período), `MONTH/YEAR` (mês), `nome_enfermaria = :clinica` (clínica)
- Sem filtros: aplica `data_referencia = MAX(data_referencia)` (última data disponível)
- Nota: comparação exata com 'OCUPADO' no SQL — sensível a variações de capitalização dos dados.

2) KPI: Livres / Cedidos / Reservados / Impedidos
- Mesma lógica de `/api/painel/stats`:
  - `LIVRE`, `CEDIDO`, `RESERVADO` são comparados por igualdade exata; `IMPEDIDO` é tratado com `LIKE '%IMPEDIDO%'` (no app.py) ou `LIKE '%IMPEDIDO%' OR LIKE '%BLOQUEADO%'` em alguns pontos.
- Sem filtros: mesma regra de usar última data.
- Observação: front-end usa `stats.total` para cálculo de taxas (por exemplo, taxa-geral = ocupados/total). Garantir `total != 0`.

3) KPI: Taxa de Ocupação Geral (card)
- Cálculo: no front-end: `((stats.ocupados / stats.total) * 100)` e no n8n é calculado como `ROUND(100.0 * SUM(CASE WHEN LOWER(status_leito) = 'ocupado' THEN 1 ELSE 0 END) / NULLIF(COUNT(*),0),2)`.
- Diferença: n8n utiliza `LOWER(...)` e `NULLIF(COUNT(*),0)` (proteção contra divisão por zero). Backend Flask usa divisão em Python sem checagem explícita.

4) Gráfico: Evolução Mensal da Ocupação (`/api/painel/evolucao`)
- SQL:
  SELECT DATE_FORMAT(data_referencia, '%Y-%m') as mes, SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END) as ocupados, COUNT(*) as total FROM historico_ocupacao_completo WHERE {where_clause} GROUP BY mes ORDER BY mes
- Retorno: labels = meses; data = round((ocupados / total) * 100, 1)
- Com filtros: predio / periodo / mes / clinica aplicam-se no WHERE
- Sem filtros: `where_clause` = 1=1 → o endpoint retorna toda a série agrupada por mês (sem limitar a última data)

5) Gráfico: Taxa de Ocupação por Clínica (`/api/painel/clinicas`)
- SQL:
  SELECT nome_enfermaria, SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END) as ocupados, COUNT(*) as total FROM historico_ocupacao_completo WHERE {where_clause} GROUP BY nome_enfermaria ORDER BY nome_enfermaria
- Retorno: labels = `nome_enfermaria`; data = percentual = (ocupados/total)*100
- Com/sem filtros: segue mesma lógica dos outros endpoints

6) Disponibilidade (`/api/disponibilidade` — front-end)
- Frontend espera `json.datasets` com arrays para compor séries empilhadas; backend não tem função explícita em `app.py` com esse nome (procurar rota `/api/disponibilidade` pode estar implementada em outro módulo). No template `disponibilidade.html`, `loadDisponibilidade()` chama `/api/disponibilidade` e depois `loadImpedimentosPieChart()`.
- A auditoria precisa confirmar se existe uma rota server-side para `/api/disponibilidade` (não encontrada em `app.py`) ou se é servida por outro serviço/arquivo.

7) Impedimentos Top-10 (`/api/painel/impedimentos`)
- SQL:
  SELECT COALESCE(NULLIF(TRIM(motivo_impedimento), ''), 'Sem motivo informado') as motivo, COUNT(*) as cnt FROM historico_ocupacao_completo WHERE {where_clause} GROUP BY motivo ORDER BY cnt DESC LIMIT 20
- Com filtros: aceita predio, periodo, mes, clinica; sem filtros aplica janela default de últimos 14 dias (no `app.py`) usando `data_referencia BETWEEN DATE_SUB(:last, INTERVAL 13 DAY) AND :last` com `last = MAX(data_referencia)`.

8) Pipeline n8n / Looker Studio
- Arquivo: `api_looker_studio/n8n_workflow_looker_studio.json` contém queries que agregam por `DATE(data_referencia)` e calculam: ocupado, livre, cedido, impedido, reservado, `taxa_ocupacao_pct` (usando LOWER(status_leito) e NULLIF(COUNT(*),0)), além de contagens por faixas etárias e permanência longa.
- Observação: n8n e backend Flask usam formas ligeiramente diferentes de comparar `status_leito` (n8n usa LOWER(...), Flask usa igualdade direta). n8n também usa proteção `NULLIF(COUNT(*),0)` — prática recomendada.

Anexos: exemplos de SQL extraídos (veja `sql_queries.md`).
