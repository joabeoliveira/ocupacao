"""
Sistema de Ocupação de Leitos - NIR Dashboard
Controle de Versão
"""

VERSION = "3.2.0"
VERSION_NAME = "Tempo de Permanência Edition"
RELEASE_DATE = "2025-12-09"

# Histórico de Versões
CHANGELOG = """
# Changelog

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
