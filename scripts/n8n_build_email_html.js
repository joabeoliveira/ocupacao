// n8n Code node (Run Once for All Items)
// Entrada esperada: payload enviado pelo endpoint /api/relatorios/webhook-send
// Saida: { subject, emailHtml, event, generated_at }

function esc(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function formatBlockTitle(id) {
  return String(id || '')
    .replace(/_/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase());
}

function renderKpis(kpis) {
  if (!Array.isArray(kpis) || !kpis.length) return '';

  const cards = kpis.map((kpi) => {
    const label = esc(kpi.label || formatBlockTitle(kpi.id));
    const value = esc(kpi.value ?? '-');
    return `
      <div class="kpi-card">
        <div class="kpi-label">${label}</div>
        <div class="kpi-value">${value}</div>
      </div>
    `;
  }).join('');

  return `
    <section class="section">
      <h2>Indicadores</h2>
      <div class="kpi-grid">${cards}</div>
    </section>
  `;
}

function renderCharts(charts) {
  if (!Array.isArray(charts) || !charts.length) return '';

  const cards = charts.map((chart) => {
    const title = esc(chart.title || formatBlockTitle(chart.id));
    const type = esc(chart.type || 'chart');
    const labels = Array.isArray(chart.labels) ? chart.labels : [];
    const data = Array.isArray(chart.data) ? chart.data : [];

    const rows = labels.map((label, idx) => {
      const value = data[idx] ?? '-';
      return `
        <tr>
          <td>${esc(label)}</td>
          <td class="num">${esc(value)}</td>
        </tr>
      `;
    }).join('');

    return `
      <div class="panel">
        <div class="panel-title">${title}</div>
        <div class="panel-subtitle">Tipo: ${type}</div>
        <table class="table compact">
          <thead>
            <tr>
              <th>Categoria</th>
              <th class="num">Valor</th>
            </tr>
          </thead>
          <tbody>
            ${rows || '<tr><td colspan="2">Sem dados</td></tr>'}
          </tbody>
        </table>
      </div>
    `;
  }).join('');

  return `
    <section class="section">
      <h2>Graficos (resumo em tabela)</h2>
      <div class="panel-grid">${cards}</div>
    </section>
  `;
}

function renderTables(tables) {
  if (!Array.isArray(tables) || !tables.length) return '';

  const blocks = tables.map((tb) => {
    const title = esc(tb.title || formatBlockTitle(tb.id));
    const columns = Array.isArray(tb.columns) ? tb.columns : [];
    const rows = Array.isArray(tb.rows) ? tb.rows : [];

    const thead = columns.map(c => `<th>${esc(c)}</th>`).join('');
    const tbody = rows.map((row) => {
      const cells = (Array.isArray(row) ? row : []).map((cell) => {
        return `<td>${esc(cell)}</td>`;
      }).join('');
      return `<tr>${cells}</tr>`;
    }).join('');

    return `
      <div class="table-wrap">
        <h3>${title}</h3>
        <table class="table">
          <thead><tr>${thead}</tr></thead>
          <tbody>${tbody || '<tr><td colspan="99">Sem dados</td></tr>'}</tbody>
        </table>
      </div>
    `;
  }).join('');

  return `
    <section class="section">
      <h2>Tabelas</h2>
      ${blocks}
    </section>
  `;
}

function renderFilters(filters) {
  const entries = Object.entries(filters || {});
  if (!entries.length) return '<p class="muted">Sem filtros aplicados</p>';

  const items = entries.map(([k, v]) => {
    const key = esc(formatBlockTitle(k));
    const val = esc(typeof v === 'object' ? JSON.stringify(v) : v);
    return `<li><span>${key}:</span> ${val}</li>`;
  }).join('');

  return `<ul class="filters">${items}</ul>`;
}

const root = $input.first().json || {};
const input = (root.body && typeof root.body === 'object') ? root.body : root;
const report = input.report || {};

const eventName = input.event || 'nir_relatorio_manual';
const generatedAt = report.generated_at || input.generated_at || new Date().toISOString();
const customMessage = input.message || 'Relatorio gerado manualmente no dashboard NIR.';

const kpisHtml = renderKpis(report.kpis || []);
const chartsHtml = renderCharts(report.charts || []);
const tablesHtml = renderTables(report.tables || []);
const filtersHtml = renderFilters(report.filters || {});

const emailHtml = `
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Relatorio NIR</title>
  <style>
    body { margin:0; background:#eef2ff; font-family: 'Segoe UI', Arial, sans-serif; color:#0f172a; }
    .container { max-width:980px; margin:0 auto; padding:28px 16px; }
    .hero {
      background: linear-gradient(130deg, #0b3a84 0%, #0f766e 100%);
      color:#fff; border-radius:16px; padding:24px;
      box-shadow: 0 10px 28px rgba(2, 6, 23, 0.20);
    }
    .hero h1 { margin:0 0 8px; font-size:24px; }
    .hero p { margin:4px 0; opacity:0.95; }
    .badge {
      display:inline-block; margin-top:8px; font-size:12px; letter-spacing:0.04em;
      text-transform:uppercase; background:rgba(255,255,255,0.18);
      border:1px solid rgba(255,255,255,0.24); border-radius:999px; padding:6px 10px;
    }
    .section {
      margin-top:18px; background:#fff; border-radius:16px; padding:18px;
      border:1px solid #dbe5ff; box-shadow: 0 4px 10px rgba(15, 23, 42, 0.05);
    }
    .section h2 { margin:0 0 12px; color:#1e3a8a; font-size:18px; }
    .section h3 { margin:8px 0 10px; color:#334155; }
    .kpi-grid {
      display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr));
      gap:10px;
    }
    .kpi-card {
      background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
      border:1px solid #cbd5e1; border-radius:12px; padding:12px;
    }
    .kpi-label { color:#334155; font-size:12px; text-transform:uppercase; letter-spacing:0.03em; }
    .kpi-value { color:#0f172a; font-size:24px; font-weight:700; margin-top:6px; }
    .panel-grid {
      display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
      gap:10px;
    }
    .panel {
      border:1px solid #dbe5ff; border-radius:12px; padding:12px; background:#f8fafc;
    }
    .panel-title { font-weight:700; color:#0f172a; }
    .panel-subtitle { color:#64748b; font-size:12px; margin:2px 0 10px; }
    .table-wrap { margin-top:12px; overflow-x:auto; }
    .table { width:100%; border-collapse:collapse; min-width:420px; }
    .table th, .table td { border-bottom:1px solid #e2e8f0; text-align:left; padding:8px; font-size:13px; }
    .table th { background:#eff6ff; color:#1e3a8a; }
    .table .num { text-align:right; }
    .compact th, .compact td { padding:6px; font-size:12px; }
    .filters { margin:0; padding-left:18px; }
    .filters li { margin:4px 0; color:#334155; }
    .filters span { color:#0f172a; font-weight:600; }
    .muted { color:#64748b; }
    .footer { margin-top:14px; font-size:12px; color:#64748b; text-align:center; }
  </style>
</head>
<body>
  <div class="container">
    <div class="hero">
      <h1>Central de Relatorios NIR</h1>
      <p><strong>Data de geracao:</strong> ${esc(generatedAt)}</p>
      <p><strong>Mensagem:</strong> ${esc(customMessage)}</p>
      <span class="badge">Evento: ${esc(eventName)}</span>
    </div>

    <section class="section">
      <h2>Filtros Aplicados</h2>
      ${filtersHtml}
    </section>

    ${kpisHtml}
    ${chartsHtml}
    ${tablesHtml}

    <div class="footer">
      Relatorio enviado automaticamente via n8n.
    </div>
  </div>
</body>
</html>
`;

const subject = `NIR | Relatorio ${generatedAt}`;

return [{
  json: {
    subject,
    emailHtml,
    event: eventName,
    generated_at: generatedAt
  }
}];