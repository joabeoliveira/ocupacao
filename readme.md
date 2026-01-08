### Em 29/12/2025

#### Correções de Interface e Funcionalidade

1. **Correção do botão de importar arquivo (página Importação e Histórico)**
   - Problema: Formulário de upload quebrado devido ao form de exclusão estar aninhado incorretamente dentro do form de upload
   - Solução: Reorganizados os forms de upload, delete e fix_date como seções independentes
   - Resultado: Botão "Importar Arquivo" agora funciona corretamente

2. **Correção do fundo da página Tempo de Permanência**
   - Problema: Background estava branco ao invés do tema escuro
   - Solução: Alterado de classe `.bg-theme` para `style="background-color: var(--bg-primary)"` 
   - Resultado: Fundo agora exibe a cor correta #0F1724 (tema escuro padrão)

3. **Padronização dos filtros em Tempo de Permanência**
   - Problema: Filtros ficavam sempre visíveis, diferente das outras páginas (Painel e Disponibilidade)
   - Solução: 
     - Adicionado botão "Filtros" no header (ao lado do botão de tema)
     - Painel de filtros agora começa escondido (classe `hidden`)
     - Implementada função `toggleFilters()` para abrir/fechar
     - Painel fecha automaticamente após aplicar filtros
   - Resultado: Comportamento consistente em todas as páginas do dashboard

4. **Correção da exibição de data na página Importação**
   - Problema: Data exibida em "Visualizando" mostrava 1 dia a menos (ex: dados do dia 17/12 apareciam como 16/12)
   - Causa: `new Date()` interpretava string ISO como UTC, causando diferença ao converter para timezone local
   - Solução: Implementado parsing manual da data sem conversão de timezone:
     ```javascript
     const dateParts = stats.data_referencia.split('-');
     const date = new Date(dateParts[0], dateParts[1] - 1, dateParts[2]);
     ```
   - Resultado: Data agora é exibida corretamente sem diferença de timezone

#### Melhorias Anteriores (incluídas no commit)

5. **Padronização completa de UI em todos os templates**
   - CSS e variáveis de tema padronizadas (12 variáveis: --bg-primary, --chart-text, etc)
   - Tailwind config estendida consistente
   - Responsividade mobile uniformizada
   - Animações e hover effects padronizados

6. **Correção do filtro de mês em impedimentos**
   - Endpoint `/api/painel/impedimentos` com lógica reorganizada
   - Três casos tratados: período definido, apenas mês, ou padrão (últimos 14 dias)
   - Filtro de mês agora funciona corretamente isolado ou combinado

7. **Cards KPI melhorados em Tempo de Permanência**
   - Gradientes coloridos aplicados (azul, roxo, laranja, vermelho, rosa)
   - Ícone adicionado ao card principal (Total Pacientes)
   - Layout e espaçamento aprimorados

#### Tecnologias e Versão

- **Versão atual:** 3.3.7
- **Stack:** Python Flask, MySQL, Jinja2, Tailwind CSS, Chart.js
- **Commit:** 21e3373
- **Branch:** master
- **Repositório:** https://github.com/joabeoliveira/ocupacao.git 