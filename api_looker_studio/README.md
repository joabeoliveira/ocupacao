Fluxo n8n: Popular Google Sheets para Looker Studio

Objetivo
- Backfill: popular a aba `indicadores` da planilha (ID: 1qz_E5x-f7FXvrauztdYeLyBHx3KCk8HjQkM7Tok9kB0) com dados agregados por dia de 2026-01-01 até 2026-04-09.
- Diário: agendar execução diária que extrai o dia atual e append/update na planilha.

O que foi gerado
- `n8n_workflow_looker_studio.json` — arquivo importável no n8n contendo: Manual Trigger (backfill) + Cron (diário) → MySQL → Format → Split in batches → Wait → Google Sheets Append.

Antes de importar
1. No n8n, importe `n8n_workflow_looker_studio.json` (Workflows → Import). 
2. Configure as credenciais: 
   - MySQL: crie uma credential e substitua `MYSQL_CREDENTIALS_PLACEHOLDER` pelo nome. Use conexão local/localhost se n8n estiver na mesma VPS.
   - Google Sheets OAuth2: crie credential com acesso ao Google Sheets e substitua `GOOGLE_SHEETS_CREDENTIALS_PLACEHOLDER`.
3. Abra o node `Set Backfill Dates` e ajuste `start_date` / `end_date` se quiser outro intervalo. Verifique `sheetId` e `sheetName`.

Como funciona (resumo técnico)
- Backfill (manual): Manual Trigger → Set Backfill Dates → MySQL Backfill (usa :start_date/:end_date) → Format Rows → Split (200 linhas por lote) → Wait 500ms → Google Sheets Append.
- Diário (agendado): Cron → MySQL Daily (WHERE data_referencia = CURDATE()) → Format Rows → Split → Wait → Google Sheets Append.

Notas importantes
- A query no node MySQL retorna porcentagens numéricas (ex.: 88.20). O node `Format Rows` formata para `88,20%` (compatível com CSV/planilha existente).
- O cabeçalho esperado na planilha para menores de idade é `pacientes < 17`.
- Para evitar duplicação diária, duas opções: (A) usar `append` e rodar deduplicação periódica; (B) alterar o fluxo para primeiro buscar se a `data` existe e então `update` a linha. A opção atual usa `append` para simplicidade. Se preferir `upsert`, posso alterar o workflow.
- Batch size e delays: `batchSize = 200`, `wait = 500ms`. Ajuste conforme estabilidade e quotas.

Testes recomendados
1. Importe o workflow e execute Manual Trigger com um intervalo curto (ex.: 2026-04-01 → 2026-04-03) para validar formato e escrita.
2. Verifique a aba `indicadores` e confirme colunas/ordem. Se necessário, ajusto o mapeamento.

Se quiser eu:
- Altero para `upsert` por `data` (checar existência e `update` em vez de `append`).
- Reduzo/incremento `batchSize` e `wait` conforme sua quota/experiência no ambiente.
- Gero um script Python alternativo que escreve direto via Sheets API (conta de serviço).

