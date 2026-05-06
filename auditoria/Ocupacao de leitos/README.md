Auditoria: Ocupação de Leitos

Objetivo: mapear como cada KPI e gráfico da página "Ocupação de Leitos" é calculado, documentar queries/endpoints, comportamento com e sem filtros, e apontar inconsistências

Arquivos gerados:
- detalhes_kpis.md  : descrição item-a-item (KPI, gráfico) com as queries usadas
- sql_queries.md    : trechos SQL extraídos de `app.py` e do fluxo `api_looker_studio` para referência rápida
- recomendacoes.md  : observações e ações recomendadas para correção/robustez

Próximo passo: revisar `detalhes_kpis.md` e solicitar validação ou execução de testes reproduzindo os cálculos no banco.