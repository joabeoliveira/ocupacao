## Atualização/Refatoração

## Objetivo
- Implementar uma atualização no sistema após mudança promovida na base de dados da Plataforma SMSRio.

## Resumo
Incialmente cumpre destacar que recetemente a plataforma SMSRio promoveu uma alteração no sistema, em que buscamos os dados para alimentar o nosso sistema de ocupação do Hospital Federal de Bonsucesso.

*** Detalhes ***

1) Alguns nomes de enfermarias na emergência foram alterados.

2) Agora estão incluindo as macas, ocupadas por pacientes na emergência, que ficam aguardando vaga de leitos, quando necessário, como leitos (macas) ocupados.

3) O arquivo em csv/excel que é extraído agora considera como macas os leitos das, antes, enfermarias referenciadas, que são as da emergência e com novos nomes e, além disso, não é mais um quantitativo fixo que, pode ser alterado a cada dia, a depender da quantidade de pacientes em macas nas dependências da emergência do HFB.

4) Em resumo os leitos da emergência sofreram alteração de nome e agora são dinâmicos podendo ser maior que o número fixo de 50 leitos anteriormente o que pode reverberar em taxas acima de 100% na emergência e consequente ocupação geral da Unidade.

5) Essa mudança aprimora a realidade da ocupação diária do hospital na emergência que por vezes vem apresentando mais pacientes que o previsto. Assim quando esse número ultrapassa os 50 passa a ser considerado percentual acima de 100%

6) Na pasta `atualizacaoSMSRio` coloquei o novo modelo de planilha extraída para importação com os novos nomes das enfermarias e novos leitos/macas que preciso importar e consequentemente ajustar o código e o banco se for necessário, no entanto, não houve mudança nas colunas do banco somente um aumento de linhas por data a partir de 01/05/2026 e mudança nos nomes das clinícas referenciadas para outros nomes.

7) Vale ressaltar que agora a taxa de ocupação da emergência (prédio 1) não é mais limitada a 100% devido a possibilidade de aumentar a quantidade das macas/leitos, acima dos 50 existentes;

8) Importante também destacar que antes não era realizado nesse projeto o controle dos leitos existentes no pre parto, no entanto, como agora esses dados também estam sendo fornecidos pela SMSRio, podemos alimentar o nosso bando de dados com esses leitos, para futuras consultas e análise de dados, mas por hora acredito que devem permanecer fora do cômputo de leitos da emergência para fins de taxa de ocupação. Leitos 251, 1 até 251, 11

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

Data de início da atualização 06/05/2026

Por Joabe Oliveira