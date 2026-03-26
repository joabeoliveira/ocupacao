# Deploy EasyPanel - Central de Relatorios

Este checklist foi criado para validar a feature diretamente em producao via branch `feature/approved-reports-webhook`.

## 1. Preparacao

1. Configure o deploy para usar a branch `feature/approved-reports-webhook`.
2. Garanta que o build instala dependencias de `requirements.txt`.
3. Variaveis opcionais recomendadas no EasyPanel:
   - `N8N_WEBHOOK_URL` (opcional, pode configurar na tela)
   - `MAX_RELATORIO_BLOCKS=12`
   - `MAX_TABELA_ROWS=100`
   - `WEBHOOK_TIMEOUT_SECONDS=20`

## 2. Smoke Test de API (apos deploy)

1. Verificar versao:
   - `GET /api/version`
2. Verificar nova tela:
   - `GET /relatorios` (status 200)
3. Verificar preview:
   - `POST /api/relatorios/preview`
   - Body exemplo:

```json
{
  "filters": {
    "predio": "1",
    "periodo_inicio": "2026-03-01",
    "periodo_fim": "2026-03-26"
  },
  "selected_blocks": [
    "kpi_ocupacao",
    "chart_ocupacao_clinica",
    "table_longa_permanencia"
  ]
}
```

4. Verificar exportacao PDF:
   - Em `/relatorios`, clicar em `Exportar PDF`.
5. Verificar exportacao PowerPoint:
   - Em `/relatorios`, clicar em `Exportar PowerPoint`.
6. Verificar webhook:
   - Salvar URL em `Webhook n8n`.
   - Clicar `Testar Conexao`.
   - Clicar `Enviar Dados para n8n`.

## 3. Checklist funcional minimo

1. Selecionar apenas 1 bloco e exportar PDF/PPTX.
2. Selecionar 3 a 5 blocos e exportar PDF/PPTX.
3. Validar que tabela no PDF respeita limite de linhas.
4. Validar que webhook recebe `event=nir_relatorio_manual`.
5. Validar retorno visual de sucesso/erro na tela.

## 4. Rollback rapido

1. Voltar deploy para branch anterior no EasyPanel.
2. Rebuild/restart da aplicacao.
3. Confirmar `GET /api/version` e navegação das paginas antigas.

## 5. Observacoes

1. Configuracao de webhook salva em memoria da aplicacao nesta V1.
2. Em reinicio de container, o ideal e configurar novamente via tela ou por `N8N_WEBHOOK_URL`.
