"""
Sistema de Ocupação de Leitos - NIR Dashboard
Controle de Versão
"""

VERSION = "3.5.0"
VERSION_NAME = "Capacidade Dinâmica Emergência Edition"
RELEASE_DATE = "2026-05-06"

# Histórico de Versões
CHANGELOG = """
# Changelog

## [3.5.0] - 2026-05-06 - Capacidade Dinâmica Emergência Edition
### 🆕 Compatibilidade SMSRio (atualização 01/05/2026)
- Filtros de emergência migrados de nome_enfermaria IN para num_enf IN (estável entre mudanças de nome)
- Suporte simultâneo a nomes históricos (até 30/04/2026) e novos nomes (a partir de 01/05/2026)
- Taxa de ocupação pode exceder 100% legitimamente (macas extras como leitos dinâmicos)
- Log [AUDITORIA NIR] no servidor quando taxa_ocupacao > 100%
- Constantes EMERGENCY_WARDS_NUM_ENF e PEDIATRIC_WARDS_NUM_ENF adicionadas
- Filtro pediátrico migrado de nome hardcoded para num_enf IN (116, 117)
- Exclusão automática de pré-parto (num_enf=251) dos cálculos de emergência

### 🎨 Frontend (emergencia.html)
- Eixo Y do gráfico de evolução: max:100 → suggestedMax:100 (escala dinâmica)
- Card #stat-taxa fica vermelho quando taxa > 100%, com tooltip explicativo
- Dropdown de filtro separado em optgroups: nomes históricos e novos nomes SMSRio

### 🔧 Rotas atualizadas
- api_emergencia_stats, api_emergencia_evolucao, api_emergencia_enfermarias
- api_emergencia_perfil_paciente, api_emergencia_longa_permanencia, api_emergencia_longa_permanencia_ranking
- _get_emergencia_range_context, _get_emergencia_profile_snapshot_context, _get_emergencia_profile_range_context
- kpi_emergencia (bloco de relatórios)

### 🧪 Testes
- 14 testes unitários: taxa 80%/100%/120%, divisão por zero, constantes num_enf, exclusão pré-parto, mapeamento de nomes

## [3.4.0] - 2026-03-26 - Relatórios & Webhooks Edition
### 🆕 Nova Funcionalidade
- Dashboard "Relatórios" com seleção dinâmica de blocos de dados
- Exportação PDF com suporte a tabelas dinâmicas e HTML escaping
- Exportação PowerPoint (PPTX) com slides: título, filtros, KPIs, gráficos e tabelas
- Integração webhook n8n com endpoints de configuração, teste e envio
- Endpoints: POST /api/relatorios/preview, /api/relatorios/webhook-config, /api/relatorios/webhook-test, /api/relatorios/webhook-send
- Endpoint novo: POST /api/export/pptx para geração de apresentações

### 📊 Blocos de Relatório Disponíveis
- KPI Ocupação Geral
- Gráfico Ocupação por Clínica
- Gráfico Evolução de Ocupação
- Tabela Longa Permanência
- KPI Emergência

### 🔒 Segurança & Hardening
- HTML escaping em todos os campos de texto (PDF/PPTX/HTML)
- Limite de blocos por relatório: 12 blocos máximo
- Limite de linhas por tabela: 100 linhas máximo
- Timeout configurável para webhooks (padrão: 20s)
- Validação de entrada e whitelist de blocos permitidos
- Sanitização de parâmetros em filtros (prédio, clínica, período, mês)

### 🔧 Melhorias Técnicas
- Novas dependências: requests==2.32.3 (webhook HTTP), python-pptx==0.6.23 (PowerPoint)
- Configuração de webhook salva em memória (V1); persistência em DB planejada para V2
- Integração com variáveis de ambiente: N8N_WEBHOOK_URL, MAX_RELATORIO_BLOCKS, MAX_TABELA_ROWS, WEBHOOK_TIMEOUT_SECONDS
- Deduplicação de blocos selecionados no backend
- Branch de feature: feature/approved-reports-webhook
- Documentação: DEPLOY_EASYPANEL_RELATORIOS.md, RELATORIOS_V1_CHANGELOG.md

### 🎨 Interface
- Nova página /relatorios com layout profissional
- Menu de navegação atualizado em 5 dashboards (Painel, Emergência, Perfil Paciente, Tempo Permanência, Disponibilidade)
- Filtros integrados: prédio, clínica, período (datetime range), mês
- Cards de KPI com valores formatados
- Gráficos Chart.js renderizados dinamicamente
- Tabelas responsivas com scroll horizontal
- Status bar com mensagens de sucesso/erro

## [3.3.9] - 2026-01-08 - Tempo de Permanência Edition (Patch)

## [3.2.0] - 2025-12-09 - Tempo de Permanência Edition
### 🆕 Nova Funcionalidade
- Painel "Tempo de Permanência" com métricas de longa permanência
- Endpoint `/api/tempo_permanencia` (JSON com métricas + lista paginada)
- Endpoint `/api/tempo_permanencia/export` (Excel com nomes completos)
- Página `/tempo_permanencia` com filtros, KPIs, gráficos e tabela

### 📊 Métricas Disponíveis
- Total de pacientes internados
- Permanência média e mediana (calculada no backend)
- Contadores: >30 dias, >30d + >=60 anos, >30d pediatria (<18 anos)
- Histograma de distribuição (0-7, 8-14, 15-30, 31-60, 61-90, >90 dias)
- Top 10 clínicas por longa permanência

### 🔒 Segurança & Privacidade
- Nomes mascarados no frontend (ex: "João S.")
- Exportação Excel com nomes completos (apenas para gestão)
- Identificação preferencial por prontuário (NULLIF para valores vazios)

### 🎨 Interface
- Tooltips explicativos em todos os KPIs
- Paginação robusta com estado disabled e contador "X / Y"
- Gráfico horizontal de clínicas (top 10)
- Cards com hover states e estilos consistentes

### 🔧 Melhorias Técnicas
- `requirements.txt` criado com openpyxl, Flask, pandas, SQLAlchemy
- Dockerfile já configurado para instalar dependências automaticamente
- Agrupamento SQL otimizado com COALESCE + NULLIF
- Export Excel in-memory usando pandas + openpyxl

## [3.1.0] - 2025-12-09 - Filters & Themes Edition
### ✨ Novidades
- Sistema de alternância de tema claro/escuro
- Botão toggle de tema no header (☀️/🌙)
- Persistência de tema com localStorage
- Filtros funcionais completos no painel de ocupação

### 🎨 Temas
- Tema Escuro: Fundo preto, sidebar preta, gráficos em azul/verde claro
- Tema Claro: Fundo cinza claro, sidebar azul, gráficos em azul/verde escuro
- Variáveis CSS dinâmicas para transição suave
- Gráficos Chart.js adaptam cores automaticamente

### 🔍 Filtros
- Filtro por Prédio (1 ou 2)
- Filtro por Período (data inicial/final)
- Filtro por Mês (1-12)
- Filtro por Clínica (lista dinâmica)
- Indicador visual de filtros ativos no header
- Backend com suporte a query strings em todas APIs

### 🔧 Melhorias
- APIs /api/painel/* aceitam parâmetros de filtro
- Cards e gráficos respondem aos filtros aplicados
- Taxas recalculadas dinamicamente
- Sincronização de tema entre páginas

## [3.0.0] - 2025-12-09 - Dark Theme Edition
### 🎨 Visual
- Implementado tema escuro moderno com fundo preto
- Cards com gradientes escuros (gray-800 to gray-900)
- Sidebar preta com bordas sutis
- Cores vibrantes nos valores (blue-400, green-400, red-400, etc.)
- Gráficos adaptados para tema escuro

### 📊 Funcionalidades
- Dados do último dia registrado aparecem por padrão
- API `/api/painel/stats` modificada para buscar último dia automaticamente
- Filtros profissionais na página de Ocupação

### 🔧 Melhorias
- Sombras mais pronunciadas (shadow-2xl)
- Bordas e contrastes otimizados para tema escuro
- Animações e hover effects mantidos

## [2.0.0] - 2025-12-08 - REST API Refactoring
### 🏗️ Arquitetura
- Refatoração completa de Jinja2 templates para REST API
- Backend: Flask APIs retornando JSON puro
- Frontend: HTML estático + Vanilla JavaScript + Fetch API
- Eliminação de conflitos Jinja/JavaScript

### 📡 APIs Implementadas
- `/api/stats` - Estatísticas gerais
- `/api/chart` - Evolução últimos 7 dias
- `/api/history` - Histórico de importações
- `/api/painel/stats` - Estatísticas do painel
- `/api/painel/evolucao` - Evolução mensal
- `/api/painel/clinicas` - Dados por clínica

### 🎨 UI/UX
- Loading skeletons
- Fade-in animations
- Progress rings (SVG)
- Responsive grid layouts
- Filtros colapsáveis

### 🐛 Correções
- Removida coluna 'predio' não existente
- Corrigida ordenação de rotas (painel antes de __main__)
- Conversão Decimal para JSON
- Erros de sintaxe JavaScript/Jinja eliminados

## [1.0.0] - 2025-12-07 - Initial Release
### ✨ Funcionalidades Base
- Upload de arquivos CSV
- Visualização de estatísticas
- Gráficos com Chart.js
- Histórico de importações
- Painel de ocupação de leitos
- Paleta de cores GHC (#599E33, #008B8B, #DFE7CF, #FFFFFF)

### 🗄️ Banco de Dados
- Tabela: historico_ocupacao_completo
- Suporte a múltiplas datas de referência
- ETL para normalização de dados CSV

### 🎨 Design
- Tailwind CSS
- Font Awesome icons
- Sidebar navigation
- Responsive design
"""

def get_version():
    """Retorna versão atual do sistema"""
    return VERSION

def get_full_version():
    """Retorna versão completa com nome"""
    return f"{VERSION} - {VERSION_NAME}"

def get_version_info():
    """Retorna dicionário com informações de versão"""
    return {
        "version": VERSION,
        "name": VERSION_NAME,
        "release_date": RELEASE_DATE
    }
