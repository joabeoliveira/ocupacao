Recomendações rápidas (prioridade)

1) Unificar comparações de `status_leito`
- Use sempre `UPPER(status_leito)` ou `LOWER(status_leito)` nas queries para evitar problemas de capitalização.
- Ex.: `SUM(CASE WHEN LOWER(status_leito) = 'ocupado' THEN 1 ELSE 0 END)`

2) Proteger divisões por zero
- Em SQL use `NULLIF(COUNT(*),0)` antes de dividir; no Python garanta checagem `if total==0: return 0`.

3) Confirmar existência/implementação de `/api/disponibilidade`
- O template chama esse endpoint; não foi encontrado em `app.py`. Se estiver implementado em outro módulo, documentar; caso contrário, implementar para garantir o gráfico funcione com filtros.

4) Habilitar testes de regressão para KPIs
- Criar script de validação que execute as mesmas queries (com e sem filtros) e compare resultados entre `app.py` e o job n8n/Looker (ou planilha `indicadores`).

5) Padronizar filtros de período
- Atualmente há decisões diferentes: "última data" para stats vs. "últimos 14 dias" para impedimentos. Documentar essa regra ou tornar o comportamento consistente conforme necessidade do usuário.

6) Melhorar logs e mensagens de erro
- Ao retornar cálculos, incluir `total` no payload e, se `total==0`, retornar `