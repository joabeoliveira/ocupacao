Memória de Cálculos — versão simples

Objetivo: apresentar as fórmulas usadas nos KPIs e gráficos de forma direta, com exemplos.

1) Taxa de Ocupação Geral
- Fórmula: Taxa de Ocupação Geral = (Total de leitos OCUPADOS / Total geral de leitos) * 100
- Exemplo: se OCUPADOS = 300 e TOTAL GERAL = 423 → Taxa = (300 / 423) * 100 = 70.9%

2) Percentual de Leitos Impedidos
- Fórmula: % Impedidos = (Leitos IMPEDIDOS / Total geral de leitos) * 100
- Exemplo: se IMPEDIDOS = 12 e TOTAL = 423 → % Impedidos = (12 / 423) * 100 = 2.8%
obs: conferido está correto

3) Contagens básicas (KPIs de cartão)
- Ocupados = número de registros com `status_leito` = 'OCUPADO'
  Ex.: 300
- Livres = número de registros com `status_leito` = 'LIVRE'
  Ex.: 90
- Cedidos = número de registros com `status_leito` = 'CEDIDO'
  Ex.: 10
- Reservados = número de registros com `status_leito` = 'RESERVADO'
  Ex.: 11

4) Taxa por Clínica
- Fórmula (por clínica): Taxa Clínica = (Ocupados na clínica / Total de leitos observados na clínica) * 100
- Exemplo: Clínica A: ocupados=45, total_clínica=60 → (45/60)*100 = 75.0%
obs: conferido está correto

5) Evolução Mensal da Ocupação (gráfico)
- Para cada mês: Taxa do mês = (Soma de registros com status 'OCUPADO' no mês / Soma de todos os registros do mês) * 100
- Exemplo: Março: ocupados_mes=1500, total_mes=2100 → (1500/2100)*100 = 71.4%

6) Top motivos de impedimento (percentual)
- Conta ocorrências de `motivo_impedimento` dentro da janela de tempo definida.
- Para percentual: (contagem_do_motivo / soma_de_todos_os_impedimentos) * 100
- Exemplo: Motivo X: 40 ocorrências, total_impedimentos=200 → 20.0%

7) Longa permanência (>15 dias)
- Regra: conta quando `DATEDIFF(data_referencia, data_internacao) >= 15`
- Exemplo: 25 pacientes atendem essa condição → retorno = 25

8) Pacientes 60+
- Regra: conta quando `idade >= 60`
- Exemplo: 78 pacientes → retorno = 78

Observações importantes (práticas recomendadas)
- Padronizar comparações de `status_leito`: use `LOWER(status_leito)` ou `UPPER(status_leito)` nas queries para evitar variações de capitalização.
- Sempre proteger divisões por zero: no SQL use `NULLIF(COUNT(*),0)` ou no Python verifique `if total == 0` antes de dividir.
- Comportamento de filtros padrão:
  - Endpoints de estatísticas (`/api/painel/stats`) usam, por padrão, a "última data disponível" quando não há filtro de período.
  - Endpoint de impedimentos (`/api/painel/impedimentos`) usa um período padrão (últimos 14 dias) quando não há filtros.

Se quiser, eu gero exemplos SQL prontos (com parâmetros) para você executar no banco e validar os números com e sem filtros.

---
Aplicação de filtros (Página "Ocupação de Leitos")
---

Filtros disponíveis (template): `predio`, `periodo_inicio`, `periodo_fim`, `mes`, `clinica`.

- `predio`: mapeado via `num_enf`:
  - `predio=1` => `num_enf BETWEEN 111 AND 199`
  - `predio=2` => `num_enf BETWEEN 200 AND 299`

- `periodo_inicio` / `periodo_fim`: aplica `data_referencia BETWEEN :periodo_inicio AND :periodo_fim` (use datas no formato `YYYY-MM-DD` ou `dd/mm/YYYY` conforme parsing do app).

- `mes`: o backend converte o parâmetro `mes` em ano e mês usando a data mais recente do banco quando necessário; aplica `MONTH(data_referencia) = :mes AND YEAR(data_referencia) = :ano`.

- `clinica`: aplica `nome_enfermaria = :clinica`.

Como os filtros afetam cada KPI / gráfico (resumo simples):

1) Cards (Ocupados, Livres, Cedidos, Impedidos, Reservados, Total)
- Endpoint: `/api/painel/stats`
- WHERE resultante: combinação de condições acima (por exemplo, com `predio=1` e `clinica='CLINICA A'`:
  `WHERE num_enf BETWEEN 111 AND 199 AND nome_enfermaria = 'CLINICA A' AND data_referencia BETWEEN '2026-03-01' AND '2026-03-31'`
- Exemplo prático: se esse filtro reduzir `total` para 60 e `ocupados` para 45 → Taxa de Ocupação Geral = (45 / 60) * 100 = 75.0%

2) Gráfico Evolução Mensal (linha)
- Endpoint: `/api/painel/evolucao`
- WHERE resultante: aplica os mesmos filtros; agrupa por `DATE_FORMAT(data_referencia, '%Y-%m')` e calcula taxa do mês como `(SUM(ocupados)/COUNT(*))*100`.
- Exemplo: com `mes=3` (março de 2026) e `clinica='CLINICA B'` → retorna apenas meses que atendem `MONTH/YEAR` e a taxa será baseada somente nos registros da clínica no mês.

3) Gráfico por Clínica (barras)
- Endpoint: `/api/painel/clinicas`
- WHERE resultante: aplica filtros de período/predio/mes (exceto `clinica`, que normalmente é omitido se desejamos comparação entre clínicas). Se `clinica` for passado, a lista retornada conterá apenas essa clínica.
- Exemplo: sem filtros retorna todas as clínicas; com `predio=2` retorna só clínicas dentro do prédio 2.

4) Top Impedimentos (pie / top)
- Endpoint: `/api/painel/impedimentos`
- Comportamento especial: se não houver `periodo_inicio`/`periodo_fim` nem `mes`, o endpoint usa janela padrão `data_referencia BETWEEN DATE_SUB(:last, INTERVAL 13 DAY) AND :last` (últimos 14 dias).
- WHERE resultante: inclui filtro `status_leito LIKE '%IMPEDIDO%' OR status_leito LIKE '%BLOQUEADO%'` mais demais filtros (predio/mes/clinica/periodo).
- Exemplo: para `clinica='URG'` e janela `2026-04-01` a `2026-04-10`, a contagem e percentuais serão calculados somente sobre impedimentos nessa clínica e intervalo.

Observação técnica final:
- Sempre verifique `total` antes de dividir para evitar divisão por zero (SQL: `NULLIF(COUNT(*),0)` ou checagem no Python).
- Recomendo executar as mesmas consultas com e sem filtros para validar diferenças esperadas.