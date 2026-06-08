Status da atualização SMSRio — 2026-06-03

Resumo do estado atual
- Branch ativa: `feature/capacidade-dinamica-emergencia`.
- Importação do CSV `2026-05-01.csv` já foi considerada na análise da mudança.
- Backend já contempla a capacidade dinâmica da emergência e a capacidade nominal de referência.
- API `/api/emergencia/stats` expõe `taxa_ocupacao`, `taxa_nominal` e `capacidade_nominal`.
- KPIs de relatório incluem `emerg_taxa_dinamica` e `emerg_taxa_nominal`.
- Logs de auditoria (`[AUDITORIA NIR]`) registram casos acima de 100%.

O que já está planejado
- Mostrar histórico + novo no tratamento de nomes das enfermarias.
- Tratar pré-parto (251) como cenário separado.
- Atualizar o frontend de emergência para destacar a taxa nominal nos alertas visuais.
- Manter a taxa dinâmica para auditoria e comparação operacional.

Onde paramos
- O backend e os cálculos centrais já estão alinhados com a nova lógica.
- O frontend ainda precisa ser ajustado para refletir a diferença entre taxa dinâmica e taxa nominal.
- A validação em produção e a revisão dos logs ainda estão pendentes.
- Os testes ficam para a próxima etapa, não devem ser executados agora.

Arquivos alterados relevantes
- `app.py` — cálculos e payloads de API/KPI atualizados.
- `VERSION.py` — versão já ajustada para a linha 3.5.0.
- `Procfile` — start command para deploy.

Próximos passos
1. Atualizar `templates/emergencia.html` para exibir `taxa_nominal` como alerta principal e ajustar `suggestedMax`/cor do card.
2. Revisar se o painel precisa de optgroups para separar nomes históricos e novos nomes SMSRio.
3. Validar em produção o JSON de `/api/emergencia/stats` e comparar com o comportamento esperado no banco.
4. Rever os logs `[AUDITORIA NIR]` depois do deploy.
5. Depois disso, incluir os testes automatizados e a validação de cobertura.

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
- Branch de trabalho: `feature/capacidade-dinamica-emergencia`.
- Responsável: você, com apoio para ajustes e revisão.

Observações finais
- A mudança mantém duas medições: a dinâmica, para auditoria, e a nominal, para alerta operacional.
- Este status foi atualizado para refletir o plano atual, sem incluir a execução de testes por enquanto.

Atualização de implementação — 2026-06-08
- Página `templates/painel.html` ajustada para modelo executivo com 3 cenários:
  1. Eletivos (373)
  2. Emergência + Parto/Pré-parto (61)
  3. Parto/Pré-parto (11, enfermaria 251)
- Filtros simplificados na tela: cenário + período (início/fim) + mês.
- KPIs alinhados ao desenho aprovado:
  - Ocupados, Livres, Cedidos, Impedidos, Reservados
  - Taxa de Ocupação Geral
  - Taxa de Ocupação Operacional (capacidade fixa - impedidos)
  - % Leitos Impedidos
  - Total de Leitos (fixo por cenário)
  - Extras em uso (ocupados acima da capacidade fixa)
- Gráfico mantido como solicitado: evolução mensal da taxa de ocupação geral média.
- Backend atualizado em `app.py`:
  - `/api/painel/stats` agora calcula por cenário fixo e retorna taxas executivas + extras.
  - `/api/painel/evolucao` agora retorna média mensal da taxa geral por cenário.

Pendências imediatas
1. Validar visualmente o comportamento dos 3 cenários na página `Painel de Ocupação de Leitos`.
2. Conferir com dados reais se os cenários refletem corretamente as enfermarias esperadas.
3. Ajustar textos/rótulos finais para apresentação executiva, se necessário.
