Status da atualização SMSRio — 2026-05-06

Resumo do estado atual
- Importação do CSV 2026-05-01 concluída localmente.
- Backend: adicionada constante `EMERGENCY_NOMINAL_CAPACITY` (env `EMERGENCY_NOMINAL_CAPACITY`, default 50).
- API `/api/emergencia/stats` atualizada para retornar:
  - `taxa_ocupacao` (ocupados / total importado)
  - `taxa_nominal` (ocupados / capacidade nominal)
  - `capacidade_nominal`
- KPIs de relatório atualizados para incluir `emerg_taxa_dinamica` e `emerg_taxa_nominal`.
- Logs de auditoria (`[AUDITORIA NIR]`) adicionados quando ultrapassa 100% (dinâmica e nominal).

Onde paramos
- Confirmar comparação entre o resultado da API e as contagens diretas no banco (SQL).
- Ajustar frontend `/emergencia` para exibir claramente a taxa vs capacidade nominal (se desejar usar a nominal para alertas visuais).
- Revisar logs de aplicação em produção para validar mensagens `[AUDITORIA NIR]` após deploy.

Arquivos alterados relevantes
- `app.py` — cálculos e payloads de API/KPI atualizados.
- `VERSION.py` — já bump para v3.5.0 (commit anterior).
- `Procfile` — start command adicionado (deploy EasyPanel).

Próximos passos recomendados
1. Rodar a query SQL abaixo no banco para confirmar `ocupados` e `total` para 2026-05-01.
2. Executar o curl na URL de produção para comparar o JSON retornado.
3. Se concordar, atualizar `templates/emergencia.html` para mostrar `taxa_nominal` como a métrica de alerta e ajustar `suggestedMax`/cor do card.
4. Rever logs de produção e criar alerta se `taxa_nominal > 100` frequente.

Comandos úteis
- Curl (apontando para seu host):
  curl -s "https://site-painelnirv350.yg64ke.easypanel.host/api/emergencia/stats?periodo_inicio=2026-05-01&periodo_fim=2026-05-01" | jq .

- SQL de verificação (ajuste `num_enf` e `data_registro` conforme seu schema):
  SELECT
    SUM(CASE WHEN status_leito = 'OCUPADO' THEN 1 ELSE 0 END) AS ocupados,
    COUNT(*) AS total
  FROM historico_ocupacao_completo
  WHERE DATE(data_registro) = '2026-05-01'
    AND num_enf IN ( /* lista num_enf emergência */ );

Branch e responsabilidades
- Branch de trabalho: `feature/capacidade-dinamica-emergencia` (código já commitado)
- Responsável: você (confirmações e deploy)

Observações finais
- A mudança mantém duas medições: a dinâmica (por macas importadas) e a nominal (leitos cadastrado). Recomendo usar a nominal para alertas operacionais e manter a dinâmica para auditoria histórica.
- Arquivo gerado automaticamente por assistente; altere conforme necessário.
