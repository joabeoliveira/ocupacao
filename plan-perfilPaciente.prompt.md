## Plan: Painel de Perfil Agregado do Paciente (DRAFT)

Com base no que existe hoje e nas suas escolhas (visão agregada, chave principal por prontuário, export apenas XLSX e dados identificáveis sem mascaramento), o plano mais seguro é evoluir o padrão já usado em Tempo de Permanência para uma nova página dedicada no menu lateral. A ideia é criar um painel com filtros consistentes com o restante do sistema, priorizando **Sexo, Idade, Tempo de Permanência e Clínica** como eixos centrais de análise para a gestão hospitalar, com KPIs e gráficos derivados de `historico_ocupacao_completo` e tabela analítica exportável em XLSX. Isso reduz risco técnico porque reutiliza Flask + pandas + Chart.js + Tailwind, já presentes, e evita introduzir novas dependências nesta primeira versão.

**Steps**
1. Definir contrato funcional do painel agregado (filtros, KPIs, gráficos e colunas da tabela) com base em [primeiras_linhas.sql](primeiras_linhas.sql), priorizando campos já validados no backend atual em [app.py](app.py).
2. Adicionar nova rota de página `perfil_paciente` em [app.py](app.py), seguindo padrão de renderização usado por `/tempo_permanencia` e `/painel`.
3. Criar template [templates/perfil_paciente.html](templates/perfil_paciente.html) com a mesma sidebar/layout dos templates existentes ([templates/painel.html](templates/painel.html), [templates/tempo_permanencia.html](templates/tempo_permanencia.html)).
4. Incluir item “Perfil do Paciente” em todas as sidebars para manter navegação consistente em [templates/index.html](templates/index.html), [templates/painel.html](templates/painel.html), [templates/disponibilidade.html](templates/disponibilidade.html), [templates/tempo_permanencia.html](templates/tempo_permanencia.html).
5. Implementar endpoint JSON de resumo agregado em [app.py](app.py) (ex.: `api_perfil_resumo`) com KPIs: pacientes únicos (por prontuário), idade média/mediana, % longa permanência, % crônicos, distribuição por sexo, top clínicas, tempo médio de permanência.
6. Implementar endpoint JSON para séries/gráficos em [app.py](app.py) (ex.: evolução diária de ocupação por status e motivos de impedimento) e endpoint para tabela paginada/filtrada do painel agregado.
7. Implementar exportação XLSX do recorte aplicado (ex.: `api_perfil_export`) em [app.py](app.py), reaproveitando estratégia já existente em `/api/tempo_permanencia/export` para manter padrão de naming e performance.
8. Atualizar [readme.md](readme.md) com a nova página, filtros disponíveis, definição dos indicadores e instruções de uso/exportação.

**Verification**
- Validar navegação: novo item da sidebar abre a página em todos os templates.
- Validar filtros (predio, período, mês, clínica) comparando totais com endpoints atuais já existentes.
- Testar endpoints JSON do novo painel com e sem filtros e checar latência em volume real.
- Testar export XLSX com os mesmos filtros da tela e conferir consistência de linhas/colunas.
- Fazer checagem manual dos gráficos no navegador (Chart.js) para casos sem dados e com dados.

**Decisions**
- Escopo: painel agregado (sem drilldown individual nesta fase).
- Chave principal: `cns` e `paciente_id` quando disponíveis, para unicidade de paciente.
- Exportação MVP: somente XLSX por hora mas poderá evoluir para PDF com imagens dos gráficos se possível.
- Privacidade MVP: dados identificáveis exibidos sem mascaramento.
- Estratégia técnica: reutilizar padrões já consolidados em [app.py](app.py) e [templates/tempo_permanencia.html](templates/tempo_permanencia.html).
- Identidade visual: seguir mesma linha visual dos painéis existentes para manter consistência.
- Diretriz analítica: priorizar indicadores de **Sexo, Idade, Tempo de Permanência e Clínica** com leitura clara para decisão gerencial.

**Lista final de KPIs (todos incluídos no produto)**

Todos os KPIs abaixo serão disponibilizados no painel. A diferença entre eles será **como e quando carregam** (imediato, sob demanda ou assíncrono), para preservar performance.

1) **KPIs Core (carregamento imediato na abertura do painel)**
- [ ] Pacientes únicos no período (chave: `cns` + `paciente_id`, com fallback).
- [ ] Distribuição por sexo (% masculino/feminino/não informado).
- [ ] Idade média e mediana.
- [ ] Distribuição por faixa etária.
- [ ] Tempo médio de permanência (dias).
- [ ] Tempo mediano de permanência (dias).
- [ ] % de pacientes de longa permanência.
- [ ] Top 5 clínicas por volume de pacientes.
- [ ] Tempo médio de permanência por clínica.

2) **KPIs Complementares (carregamento sob demanda por seção/aba)**
- [ ] Taxa de leitos impedidos no recorte.
- [ ] Top 5 enfermarias por ocupação de pacientes.
- [ ] % de pacientes crônicos.
- [ ] Pacientes com indicação/uso de suporte ventilatório (quando o campo estiver preenchido).
- [ ] Pacientes com necessidade de TRS/diálise (campos relacionados).

3) **KPIs Avançados (cálculo assíncrono e cacheado)**
- [ ] Índice de rotatividade por leito (entradas distintas por período).
- [ ] Pacientes com internação prolongada por clínica (ranking).
- [ ] Percentual de pacientes com motivo de permanência informado.
- [ ] Tempo médio entre reserva e ocupação (quando houver dados válidos).

**Lista final de gráficos (todos incluídos no produto)**

1) **Gráficos Core (carregamento imediato na abertura do painel)**
- [ ] Série temporal: pacientes ativos por dia.
- [ ] Pizza/rosca: distribuição por sexo.
- [ ] Barras: faixa etária (0-17, 18-39, 40-59, 60-79, 80+).
- [ ] Histograma: distribuição do tempo de permanência.
- [ ] Barras horizontais: Top clínicas por pacientes.
- [ ] Barras: tempo médio de permanência por clínica.

2) **Gráficos Complementares (carregamento sob demanda por seção/aba)**
- [ ] Série temporal: taxa de impedimento por dia.
- [ ] Linha empilhada: status de leito ao longo do tempo (ocupado/livre/impedido).
- [ ] Barras: motivos de impedimento mais frequentes.
- [ ] Heatmap simples: ocupação por dia da semana x clínica.

3) **Gráficos Avançados (cálculo assíncrono e cacheado)**
- [ ] Boxplot de permanência por clínica (com outliers).
- [ ] Curva acumulada de longa permanência no período.
- [ ] Sankey simplificado de movimentação entre clínicas/enfermarias (apenas se dados forem consistentes).

**Arquitetura funcional proposta (todos os KPIs sem travar o banco)**
- Camada 1 (Resumo Executivo): 8 cards de KPI + 6 gráficos Core, carregados na abertura.
- Camada 2 (Análises Complementares): KPIs e gráficos complementares em abas expansíveis (carregam somente ao abrir a aba).
- Camada 3 (Análises Avançadas): KPIs e gráficos avançados via botão `Gerar análise`, com processamento assíncrono e retorno quando pronto.
- Tabela analítica única com paginação server-side e exportação XLSX do recorte aplicado.

**Estratégia de performance e escalabilidade (obrigatória)**
- Pré-agregações diárias em tabela resumo por: data, clínica, sexo, faixa etária e buckets de permanência.
- Cache de endpoints analíticos por combinação de filtros (TTL 5–15 min).
- Lazy loading de widgets: cada bloco consulta dados apenas quando visível/acionado.
- Janela temporal padrão curta (30–90 dias) com ampliação manual para recortes longos.
- Paginação e agregação no servidor para evitar transferência excessiva ao frontend.
- Exportação XLSX desacoplada do carregamento da tela (evitar impacto na navegação).
- Índices direcionados nos campos de filtro e agrupamento (data, clínica, sexo, chaves de paciente e status).

**SLOs de desempenho (meta do projeto)**
- Abertura inicial do painel (Camada 1): até ~1.5s em ambiente de produção.
- Endpoints Core: p95 < 800ms.
- Endpoints Complementares: p95 < 1.2s.
- Endpoints Avançados: execução assíncrona, sem bloquear interface.

**Roadmap de entrega sugerido (com todas as KPIs)**
- Sprint 1: infraestrutura de filtros, Camada 1 completa (KPIs/Gráficos Core), tabela e export XLSX.
- Sprint 2: Camada 2 completa (KPIs/Gráficos Complementares) com lazy loading e cache.
- Sprint 3: Camada 3 completa (KPIs/Gráficos Avançados), jobs assíncronos e ajustes finos de índice/cache.

**Critérios de qualidade de dados e governança analítica**
- Exibir selo de confiabilidade por KPI/gráfico (alto/médio/baixo) conforme completude dos campos no recorte.
- Sinalizar no rodapé quando um indicador usar base parcial ou com alta ausência.
- Padronizar regras de fallback de identidade do paciente para manter consistência entre telas e exportação.
- Priorizar sempre leituras orientadas à decisão de gestão: perfil demográfico, permanência e variação por clínica.

Se quiser, no próximo ciclo eu já transformo este plano em backlog técnico (rotas/API, queries, contratos JSON e ordem exata de implementação por sprint).
