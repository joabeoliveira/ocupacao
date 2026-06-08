## Atualização/Refatoração

## Objetivo
- Implementar uma atualização no sistema após mudança promovida na base de dados da Plataforma SMSRio.

## Resumo
- Incialmente cumpre destacar que recetemente a plataforma SMSRio promoveu uma alteração no sistema, em que buscamos os dados para alimentar o nosso sistema de ocupação do Hospital Federal de Bonsucesso.

*** Detalhes ***

1) Alguns nomes de enfermarias na emergência foram alterados.

a) 111 DE CLINICA REFERENCIADA PARA SALA VERMELHA
b) 113 DE CIRURGIA REFERENCIADA PARA SALA AMARELA
c) 114 DE CIRURGIA REFERENCIADA - FEMININA PARA OBSERVAÇÃO
d) 115 DE CIRURGIA REFERENCIADA - MASCULINA PARA OBSERVAÇÃO
e) 116 DE CLINICA REFERENCIADA - PED PARA SALA AMARELA - PEDIÁTRICA
f) 117 DE CLINICA REFERENCIADA - PED PARA OBSERVAÇÃO - PEDIÁTRICA


2) Agora estão incluindo as macas, ocupadas por pacientes na emergência, que ficam aguardando vaga de leitos, quando necessário, como leitos (macas) ocupados. 

- Quantidade instalada mudou de 50 para 62 na emergência e antes possuiam um quantitativo de leitos fixos, agora estão sendo computados como leitos as macas instaladas e podem variar os quantitativos.

- Os dados da enfermaria 251 leitos 1 ao 11 antes não eram controlados, agora estamos incluindo no banco apenas com o intuito de alimentar o banco com esses dados. Futuramente poderão ser usados para fins de análise. Outra questão é que esses leitos não são estáticos podendo ter leitos extra dependendo da demanda.

3) O arquivo em csv/excel que é extraído agora considera como macas os leitos das, antes, enfermarias referenciadas, que são as da emergência e com novos nomes e, além disso, não é mais um quantitativo fixo que, pode ser alterado a cada dia, a depender da quantidade de pacientes em macas nas dependências da emergência do HFB.

Leitos da emergencia: 111, 113, 114, 115, 116, 117
Leitos do parto/pre parto: 251, 1 ao 11
Leitos Eletivos: todos os outros leitos que não estão nas categorias acima (emergencia + parto e pré parto) e que totalizam 373 leitos.

Quantidade de leitos:
- Eletivos total = 373
- Emergência total = 61 sendo 50 de antes + 11 do parto e pré-parto (podendo variar a cada dia) 
- Pré parto total = 11 (podendo variar a cada dia)

4) Em resumo os leitos da emergência sofreram alteração de nome e agora são dinâmicos podendo ser maior que o número fixo de 50 leitos anteriormente o que pode reverberar em taxas acima de 100% na emergência e consequente ocupação geral da emergência.

5) Essa mudança aprimora a realidade da ocupação diária do hospital na emergência que por vezes vem apresentando mais pacientes que o previsto. Assim quando esse número ultrapassa os 50 passa a ser considerado percentual acima de 100%

6) Na pasta `atualizacaoSMSRio` coloquei o novo modelo de planilha extraída para importação com os novos nomes das enfermarias e novos leitos/macas que preciso importar e consequentemente ajustar o código e o banco se for necessário, no entanto, não houve mudança nas colunas do banco somente um aumento de linhas por data a partir de 01/05/2026 e mudança nos nomes das clinícas referenciadas para outros nomes.

7) Vale ressaltar que agora a taxa de ocupação da emergência (prédio 1) não é mais limitada a 100% devido a possibilidade de aumentar a quantidade das macas/leitos, acima dos 50 existentes;

8) Importante também destacar que antes não era realizado nesse projeto o controle dos leitos existentes no pre parto, no entanto, como agora esses dados também estão sendo fornecidos pela plataforma SMSRio, podemos alimentar o nosso bando de dados com esses leitos, e apresentar no painel KPIs e Gráficos para essas informações, o que pode ser interessante para análises futuras.

## Próximos Passos

- Sanar as seguintes dúvidas:
1)  Mapeamento de Nomes: No arquivo `atualizacaoSMSRio\dados_SMSRio pos mudanca.csv`, as novas enfermarias devem ser tratadas como entidades separadas no banco ou devem ser mapeadas para as categorias antigas de "Emergência"?

2) Lógica de Negócio (Taxa de Ocupação): Atualmente, o sistema possui uma trava ou limite de 100% no código (Python/app.py ou SQL) ou no Looker Studio? Preciso saber se o ajuste deve ser feito na camada de ingestão de dados ou se há scripts de validação que precisam ser alterados para aceitar valores dinâmicos.

3) Criação de agent: Após sanar as dúvidas e conversar com a LLM, criar um agent para essa tarefa.

4) Antes de começar qualquer mudança iniciar uma Branch no github

5) Ajustar e auditar as mudanças

## Observação
- Novos nomes 
111 = SALA VERMELHA (LEITOS 1 EM DIANTE) (ANTES ERA = CLINICA REFERENCIADA LEITOS 1 A 4)
113	= SALA AMARELA (LEITOS 1 EM DIANTE) (ANTES ERA = CIRURGICA REFERENCIADA LEITOS 1 A 10)
114	= OBSERVAÇÃO (LEITOS 1 EM DIANTE) (ANTES ERA CIRURGICA REFERENCIADA - FEMININA LEITOS 1 A 9)
115	= OBSERVAÇÃO (LEITOS 1 EM DIANTE) (ANTES ERA CIRURGICA REFERENCIADA - MASCULINA LEITOS 1 A 9)
116	= SALA AMARELA PEDIÁTRICA (LEITOS 1 EM DIANTE) (ANTES ERA CLINICA REFERENCIADA - PED LEITOS 1 A 10)
117	= OBSERVAÇÃO - PEDIÁTRICA (LEITOS 1 EM DIANTE) (ANTES ERA CLINICA REFERENCIADA - PED LEITOS 1 A 8)
251	= PRÉ-PARTO (LEITOS 1 EM DIANTE) (ANTES NÃO CONTROLADOS)

Mudanças sugeridas no painel de ocupação:
- Criar 3 cenários para taxa de ocupação:
1) Leitos Eletivos (considerando somente os 373 leitos eletivos);
2) Emergência (considerando somente os leitos da emergência, incluindo as macas, e sem limite de 100% + os leitos do pré parto);
3) Parte e pré-parto (considerando os leitos do pré-parto)

### KPIS e Gráficos sugeridos para cada cenário:
- KPIs: Taxa de ocupação geral, Taxa de ocupação operacional, Total de leitos, Total de leitos ocupados, Total de leitos impedidos, Total de leitos livres, Total de leitos cedidos, Total de leitos reservados.

- Gráficos: gráfico de evolução da taxa de ocupação (média mensal).



Data de início da atualização 06/05/2026

Por Joabe Oliveira