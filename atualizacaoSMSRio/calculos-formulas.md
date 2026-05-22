# Demonstrativo de Cálculos e Fórmulas usadas no sistema

## Status da validação

- Situação: parcialmente aderente ao sistema atual.
- Base de validação: backend em app.py e frontend do painel/emergência.
- Observação: há fórmulas no documento que ainda não estão implementadas no painel principal.

## Fórmulas atualmente em produção

- Pacientes-dia (ocupados no recorte): soma de status_leito = "OCUPADO".
- Total de leitos no recorte: contagem de todos os registros do recorte (COUNT(*)).
- Taxa de ocupação geral (painel de ocupação):
	- taxa_ocupacao_geral = (ocupados / total) * 100
- Percentual de leitos impedidos (painel de ocupação):
	- percentual_impedidos = (impedidos / total) * 100
- Taxa de ocupação geral (relatórios dinâmicos V1):
	- leitos_ativos = total - impedidos
	- taxa_ocupacao_geral = (ocupados / leitos_ativos) * 100
- Emergência (página dedicada):
	- taxa_dinamica = (ocupados / total_emergencia_no_dia) * 100
	- taxa_nominal = (ocupados / capacidade_nominal_emergencia) * 100
	- capacidade_nominal_emergencia padrão: 50 (env EMERGENCY_NOMINAL_CAPACITY)

## Itens do documento que não condizem 100% com o sistema atual

- "Taxa de ocupação ajustada" e "taxa de ocupação operacional ajustada": não existem como KPIs explícitos no painel principal hoje.
- "Capacidade instalada ajustada" e "capacidade operacional ajustada": não estão materializadas com essas nomenclaturas no backend do painel principal.
- "Capacidade instalada ajustada = total - emergência e hospital dia": a regra está documentada, porém não foi localizada como cálculo ativo no app.py para o painel de ocupação.

## Estado dos leitos

- OCUPADO = paciente no leito.
- LIVRE = sem paciente no leito.
- CEDIDO = leito cedido (não computado como ocupado).
- IMPEDIDO/BLOQUEADO = leito indisponível temporariamente.
- RESERVADO = leito reservado para internação.

## Recomendação para alinhamento com a chefia

- Definir oficialmente qual denominador será padrão institucional para taxa de ocupação:
	- opção A: total de leitos do recorte (inclui impedidos)
	- opção B: leitos ativos (total - impedidos)
- Definir se o painel principal terá KPI de "taxa dinâmica" e "taxa nominal" para emergência.
- Definir se "pré-parto (251)" entra apenas em base histórica/relatórios ou também em indicadores de tela.