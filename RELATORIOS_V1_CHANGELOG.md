# Relatorios V1 - Resumo da Implementacao

## Entregas

1. Nova pagina `relatorios` com selecao manual de blocos (graficos, tabelas e KPIs).
2. Preview de dados via API para composicao do relatorio personalizado.
3. Exportacao em PDF com graficos e tabelas selecionadas.
4. Exportacao em PowerPoint (PPTX) com slides por secao.
5. Integracao manual com webhook n8n (salvar URL, testar conexao e enviar payload JSON).

## Endpoints novos

1. `GET /relatorios`
2. `POST /api/relatorios/preview`
3. `GET /api/relatorios/webhook-config`
4. `POST /api/relatorios/webhook-config`
5. `POST /api/relatorios/webhook-test`
6. `POST /api/relatorios/webhook-send`
7. `POST /api/export/pptx`

## Endpoints alterados

1. `POST /api/export/pdf` (agora aceita tabelas no payload)

## Parametros de ambiente (opcionais)

1. `N8N_WEBHOOK_URL`
2. `MAX_RELATORIO_BLOCKS` (padrao 12)
3. `MAX_TABELA_ROWS` (padrao 100)
4. `WEBHOOK_TIMEOUT_SECONDS` (padrao 20)

## Arquivo de deploy

1. Ver checklist em `DEPLOY_EASYPANEL_RELATORIOS.md`.
