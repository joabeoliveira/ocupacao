# Design Skills - NIR Dashboard

## Identidade Visual

### Paleta de Cores

#### Modo Escuro (Padrão)
- **Fundo Primário**: `#0f1724` (azul muito escuro)
- **Fundo Secundário**: `#111827` (cinza escuro)
- **Fundo Terciário**: `#0b1a2a` (azul escuro)
- **Sidebar**: `#071025` (azul muito escuro)
- **Texto Primário**: `#e6eef8` (cinza claro)
- **Texto Secundário**: `#9fb6d8` (azul claro)
- **Borda**: `#111827` (cinza escuro)

#### Modo Claro
- **Fundo Primário**: `#f7fbff` (azul muito claro)
- **Fundo Secundário**: `#ffffff` (branco)
- **Fundo Terciário**: `#f1f5f9` (cinza muito claro)
- **Sidebar**: `#1E3A8A` (azul escuro)
- **Texto Primário**: `#0b1724` (azul muito escuro)
- **Texto Secundário**: `#4b5563` (cinza escuro)
- **Borda**: `#E5E7EB` (cinza claro)

### Cores de Acento
- **Azul Primário**: `#0b72d9` (ações, botões principais)
- **Verde**: `rgba(22, 163, 74, 0.85)` (sucesso, métricas positivas)
- **Laranja**: `rgba(249, 115, 22, 0.85)` (atenção, avisos)
- **Vermelho**: `#ef4444` (erro, impedimentos)
- **Azul Charts**: `rgba(11, 114, 217, 0.85)` (gráficos)

## Layout & Estrutura

### Componentes Principais

#### 1. Sidebar
```html
<aside class="sidebar w-64 h-screen text-white flex flex-col fixed left-0 top-0 z-10 shadow-2xl">
```
- Largura fixa: `w-64` (256px)
- Posição: fixa no lado esquerdo
- Responsiva: hidden em mobile, visível em md+

#### 2. Main Content
```html
<div class="main-content flex-1 md:ml-64">
  <div class="container mx-auto mt-16 md:mt-8 px-4 pb-12">
```
- **NÃO usar** `max-w-*` (deve ocupar toda largura)
- Padding: `px-4` (lateral), `pb-12` (inferior)
- Margin-top: `mt-16` (mobile), `md:mt-8` (desktop)

#### 3. Cards
```html
<div class="bg-gray-800 p-6 rounded-lg shadow-2xl card-hover animate-fade-in border border-gray-700">
```
- Background: `bg-gray-800` (ou gradiente `from-blue-600 to-blue-800` para KPIs)
- Padding: `p-6`
- Border: `border border-gray-700`
- Shadow: `shadow-2xl`
- Animação: `animate-fade-in`
- Hover: classe `card-hover`

#### 4. Gráficos
```html
<div class="bg-gray-800 p-6 rounded-lg shadow-2xl card-hover animate-fade-in border border-gray-700">
  <h3 class="font-bold text-white mb-4 text-lg">
    <i class="fas fa-chart-bar mr-2 text-blue-400"></i>
    Título do Gráfico
  </h3>
  <div style="height: 300px; position: relative;">
    <canvas id="chart-id"></canvas>
  </div>
</div>
```
- **IMPORTANTE**: Sempre incluir TITLE com icone
- Height: `300px` a `420px` dependendo do tipo
- Position: `relative` no container
- Canvas sem `max-w-*`

### KPI Cards (Métrica)
```html
<div class="md:col-span-2 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg p-6 shadow-lg text-white card-hover">
  <div class="flex items-center justify-between">
    <div>
      <div class="text-sm font-semibold uppercase mb-2">Métrica</div>
      <div class="text-3xl font-bold">-</div>
    </div>
    <div class="text-4xl opacity-50">
      <i class="fas fa-icon"></i>
    </div>
  </div>
</div>
```
- Gradiente: `from-[cor] to-[cor]` (diferentes cores por métrica)
- Texto: `text-white`
- Ícone: `opacity-50`

## Chart.js - Cores Resolvidas

### ⚠️ ERRO COMUM: Usar `var(--chart-blue)` diretamente no Chart.js
```javascript
// ❌ ERRADO - Chart.js não interpreta variáveis CSS
borderColor: 'var(--chart-blue)'

// ✅ CORRETO - Resolver variáveis CSS antes
function getChartColors() {
    const computed = getComputedStyle(document.documentElement);
    return {
        chartBlue: computed.getPropertyValue('--chart-blue').trim() || 'rgba(11, 114, 217, 0.85)',
        chartGreen: computed.getPropertyValue('--chart-green').trim() || 'rgba(22, 163, 74, 0.85)',
        chartText: computed.getPropertyValue('--chart-text').trim() || '#e6eef8',
        chartGrid: computed.getPropertyValue('--chart-grid').trim() || 'rgba(255, 255, 255, 0.06)'
    };
}

const colors = getChartColors();
borderColor: colors.chartBlue  // ✅ CORRETO
```

## Tipografia

### Tamanhos
- **Títulos (h1-h3)**: `font-bold text-xl` ou `text-lg`
- **Labels**: `text-sm font-medium`
- **Corpo**: `text-base`
- **Pequeno**: `text-xs`

### Cores de Texto
- Primário: `text-white` (dark) / `text-gray-900` (light)
- Secundário: `text-gray-300` (dark) / `text-gray-600` (light)
- Desabilitado: `text-gray-500` / `text-gray-400`

## Componentes Padrão

### Botões
```html
<!-- Primário -->
<button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition">
  Ação
</button>

<!-- Secundário -->
<button class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition">
  Ação
</button>

<!-- Com Ícone -->
<button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition">
  <i class="fas fa-check mr-2"></i>Confirmar
</button>
```

### Inputs & Selects
```html
<input type="date" class="w-full px-3 py-2 bg-gray-900 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">

<select class="w-full px-3 py-2 bg-gray-900 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
  <option>Opção</option>
</select>
```

### Tabelas
```html
<table class="min-w-full table-auto text-sm">
  <thead class="border-b-2 border-gray-700">
    <tr class="text-gray-400">
      <th class="text-left px-2 py-2">Coluna</th>
    </tr>
  </thead>
  <tbody>
    <tr class="hover:bg-white/10 border-b border-gray-700">
      <td class="px-2 py-2 text-gray-300">Dados</td>
    </tr>
  </tbody>
</table>
```

## Animações

### Fade In
```css
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
    animation: fadeIn 0.5s ease-out;
}
```

### Card Hover
```css
.card-hover {
    transition: all 0.3s ease;
}
.card-hover:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}
```

## Responsividade

### Breakpoints Tailwind
- `md`: 768px+
- `lg`: 1024px+
- `xl`: 1280px+

### Padrão de Estrutura
```html
<!-- Mobile First -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Menu Mobile
- Hidden no mobile: `sidebar-hidden` (transform: translateX(-100%))
- Overlay escuro: `menu-overlay`
- Hamburger button: fixed top-left

## Tema Dinâmico (Dark/Light)

### Implementação
```javascript
function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme') || 'dark';
    const next = current === 'light' ? 'dark' : 'light';
    html.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
}

function loadTheme() {
    const saved = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
}
```

### CSS Variables
Todas as cores estão em variáveis CSS no `<style>`:
- `:root` para dark mode
- `[data-theme="light"]` para light mode

## Checklist para Novas Páginas

- [ ] Sidebar incluída e correta
- [ ] Main content sem `max-w-*`
- [ ] Container com `mx-auto mt-16 md:mt-8 px-4 pb-12`
- [ ] KPI cards com gradientes das cores corretas
- [ ] Gráficos com **TITULO VISÍVEL** e ícone
- [ ] Cores Chart.js resolvidas com `getChartColors()`
- [ ] Botões com hover e transição
- [ ] Inputs com background branco (#FFFFFF)
- [ ] Tabelas com hover effect
- [ ] Responsiva (mobile first)
- [ ] Tema dinâmico funcionando
- [ ] Animações fade-in

## Exceções/Notas

⚠️ **NÃO FAZER**:
1. ❌ Usar `max-w-*` no container principal
2. ❌ Usar `var(--chart-*)` direto no Chart.js
3. ❌ Inputs com `!important` para background (já está em HTML)
4. ❌ Gráficos sem titulo visível
5. ❌ Cores hardcoded (usar variáveis CSS)

✅ **FAZER**:
1. ✅ Resolver variáveis CSS em JavaScript
2. ✅ Título + ícone em toda div de gráfico
3. ✅ Height relativa (300px-420px) para gráficos
4. ✅ Hover effects em cards
5. ✅ Animação fade-in em cards
