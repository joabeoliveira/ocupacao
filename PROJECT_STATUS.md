# Project Status — NIR Dashboard: Perfil do Paciente

Last updated: 2026-02-25

## Resumo Executivo

| Aspecto | Status |
|--------|--------|
| **Atual** | Sprint 3 (Export PDF) **EM ANDAMENTO** ⚠️ |
| **Branch** | `feature/perfil-paciente` |
| **Commits** | +Sprint 3 (PDF export + ajustes infra) |
| **Deploy** | Em teste (EasePanel) |

---

## Sprint 1 (Core) — CONCLUÍDO ✅

### Entregas
- **UI:** Nova página `/perfil_paciente` com 3 tabs (Geral, Complementares, Avançados)
- **Backend APIs (4):**
  - `/api/perfil_paciente/resumo` — KPIs principais
  - `/api/perfil_paciente/graficos` — 6 gráficos de análise
  - `/api/perfil_paciente/tabela` — Dados paginados de pacientes
  - `/api/perfil_paciente/export` — Download XLSX

### Componentes
- 8 KPI cards no tab "Geral"
- 6 gráficos: série temporal, sexo, faixa etária, histograma permanência, top clínicas, permanência por clínica
- Filtros: prédio, clínica (dropdown), período, mês
- Exportação de dados para Excel

---

## Sprint 2 (KPIs Avançados) — CONCLUÍDO ✅

### Entregas Backend (6 novos endpoints)
1. **`/api/perfil_paciente/kpis-complementares`** — 5 novos KPIs
   - Impedidos (%), Top 3 enfermarias, % Crônicos, % Ventilação Mecânica, % TRS
2. **`/api/perfil_paciente/kpis-avancados`** — 3 KPIs estratégicos
   - Rotatividade/leito, Motivo permanência (%), Tempo médio reserva
3. **`/api/perfil_paciente/impedimentos-serie`** — Série temporal taxa impedimento
4. **`/api/perfil_paciente/status-serie`** — Série multi-status leitos
5. **`/api/perfil_paciente/impedimentos-top`** — Ranking top 10 motivos
6. **`/api/perfil_paciente/longa-permanencia-ranking`** — Pacientes > 30 dias por clínica
7. **`/api/perfil_paciente/rotatividade-serie`** — Série rotatividade semanal
8. **`/api/perfil_paciente/reserva-serie`** — Série tempo médio reserva

### Entregas Frontend
- **KPIs Complementares Tab:** 5 cards (impedidos %, enfermarias, crônicos, ventilação, TRS)
- **KPIs Avançados Tab:** 3 cards (rotatividade, motivo permanência, tempo reserva)
- **Gráficos Avançados:** 3 novos charts (rotatividade série, longa permanência ranking, reserva série)
- **Lazy Loading:** Abas carregam dados sob demanda com loading states
- **Heatmap:** Ocupação por dia × clínica (grid visual)

### Melhorias UI/UX
- ✅ Botões "Filtros" padronizados (ícone + texto, hover azul-900)
- ✅ Campos de input brancos (cores consistentes em todas as páginas)
- ✅ Dropdown clínica carregado via API `/api/painel/clinicas`
- ✅ Remoção de texto "Sprint 2/3" dos cards
- ✅ Layout reorganizado (painel: evolucao top, clinica 380px bottom)
- ✅ Gráfico clinica: horizontal → **vertical bars**

### ChartDataLabels (Todos os Gráficos)
- ✅ Plugin instalado em todas as 4 páginas (painel, disponibilidade, tempo_permanencia, perfil_paciente)
- ✅ Dado label em cada barra/ponto/fatia para leitura rápida
- ✅ Valores formatados: % para taxas, números para quantidade
- ✅ 17 gráficos com labels habilitados:
  - **perfil_paciente:** 12 charts
  - **disponibilidade:** 2 charts
  - **tempo_permanencia:** 2 charts
  - **painel:** já estava funcionando

---

## Arquitetura Técnica

### Backend (app.py)
```python
# Endpoints Perfil Paciente
@app.route('/api/perfil_paciente/resumo')           # GET
@app.route('/api/perfil_paciente/graficos')         # GET
@app.route('/api/perfil_paciente/tabela')           # GET
@app.route('/api/perfil_paciente/export')           # GET
@app.route('/api/perfil_paciente/kpis-complementares')
@app.route('/api/perfil_paciente/kpis-avancados')
@app.route('/api/perfil_paciente/impedimentos-serie')
@app.route('/api/perfil_paciente/status-serie')
@app.route('/api/perfil_paciente/impedimentos-top')
@app.route('/api/perfil_paciente/longa-permanencia-ranking')
@app.route('/api/perfil_paciente/rotatividade-serie')
@app.route('/api/perfil_paciente/reserva-serie')
```

### Frontend (templates/)
- **perfil_paciente.html:** 3 tabs, 20 KPI cards, 12 charts, lazy loading
- **painel.html:** Melhorado — layout reorganizado, datalabels
- **disponibilidade.html:** Adicionado datalabels
- **tempo_permanencia.html:** Adicionado datalabels
- **index.html:** Menu atualizado (removido submenu perfil_paciente)

### Dependencies
- Backend: Flask, SQLAlchemy, pandas, openpyxl, weasyprint, pydyf
- Frontend: Tailwind CSS, Chart.js 3.x, chartjs-plugin-datalabels@2
- Database: MySQL (`historico_ocupacao_completo` table)

---

## Sprint 3 (Export PDF) — EM ANDAMENTO ⚠️

### Entregas Backend
- **`/api/export/pdf`** — endpoint para gerar PDF com KPIs + graficos (base64)
- HTML PDF com layout A4, grid de KPIs, blocos de graficos e filtros aplicados
- Logs detalhados para diagnostico de falhas na geracao

### Entregas Frontend
- Botao **Export PDF** em `perfil_paciente`
- Captura de 8 KPIs + 6 graficos com alta resolucao (2x)
- Ajuste temporario de cores para texto dos graficos no PDF
- Botao copiar/baixar grafico por grafico (hover)

### Infra / Deploy
- Dockerfile: dependencias de sistema para WeasyPrint (pango, cairo, gdk-pixbuf, fonts)
- Dependencias fixadas: `weasyprint==58.1`, `pydyf==0.6.0`

### Status
- PDF gerando com sucesso apos ajuste de versoes
- Qualidade de texto/legenda melhorada (cores escuras e 2x)
- Copy/Download por grafico em validacao

---

## Checklist de Validação

### ✅ Backend
- [x] 8 endpoints implementados com filtros corretos
- [x] Null handling robusto
- [x] Paginação funciona (perfil_paciente/tabela)
- [x] Export XLSX inclui todas colunas
- [x] Endpoint PDF responde com arquivo

### ✅ Frontend
- [x] 3 tabs carregam corretamente
- [x] Lazy loading das abas (complementar, avançado)
- [x] Dropdown clínica carrega via API
- [x] Filtros aplicados corretamente
- [x] Todas as cores = branco para inputs
- [x] Botões "Filtros" padronizados todas páginas
- [x] Chart labels visíveis (datalabels enabled)
- [x] Export PDF com graficos e KPIs
- [x] Captura em alta resolucao para PDF

### ✅ UX/UI
- [x] Sem erros de console
- [x] Responsive mobile-friendly
- [x] Temas claro/escuro funciona
- [x] Ícones + textos em botões
- [x] Paginação table funciona

---

## Commits Recentes

| Hash | Mensagem | Data |
|------|----------|------|
| 8e3b203 | Fix: Use dark colors for chart text when exporting to PDF | 2026-02-25 |
| c167600 | Improve: Capture charts in high resolution (2x) for better PDF quality | 2026-02-25 |
| c584801 | Fix: Pin pydyf to 0.6.0 and downgrade WeasyPrint to 58.1 | 2026-02-25 |
| ... | Auth commits Sprint 1 | 2026-02-24 |

---

## Registro de Auditoria

- **2026-02-24** — Sprint 2 finalizado: 6 endpoints + 8 KPI cards + 3 charts + datalabels globais
- **2026-02-24** — Fix: datalabels.enabled adicionado a 17 Chart instances (perfil_paciente, disponibilidade, tempo_permanencia)
- **2026-02-24** — UI/UX: Padronização filtros, inputs brancos, dropdown clínica, layout reorganizado
- **2026-02-24** — CODE QUALITY: Todos os gráficos com valores visíveis para facilitar leitura
- **2026-02-25** — Sprint 3 iniciado: PDF export com KPIs + graficos no perfil_paciente
- **2026-02-25** — Fix: compatibilidade WeasyPrint/pydyf + dependencias de sistema no Dockerfile
- **2026-02-25** — UX: captura de graficos em alta resolucao + texto escuro no PDF

---

## Preparacao para Deploy

### Tag recomendada
```bash
git tag -a v3.5.0-perfil-s3 -m "Sprint 3: Export PDF com graficos e KPIs"
git push origin v3.5.0-perfil-s3
```

### Requerimentos de Ambiente
- `DATABASE_URL` ou (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_NAME`)
- `SECRET_KEY`
- Python 3.8+
- MySQL 5.7+

### Health Checks Pós-Deploy
```bash
curl http://api.example.com/api/perfil_paciente/resumo?predio=X&clinica=Y
curl http://api.example.com/api/perfil_paciente/kpis-complementares?predio=X
curl http://api.example.com/api/perfil_paciente/kpis-avancados?predio=X
curl http://api.example.com/api/version
```

---

## Próximos Passos (Sprint 3+)

1. **Performance:** Implementar cache/redis para métricas agregadas
2. **Alertas:** Notificações quando KPIs excedem thresholds
3. **Export:** Expandir PDF para outras paginas (painel, disponibilidade, tempo_permanencia)
4. **Mobile:** Otimizar responsive para tablets (landscape)
5. **Testes:** Cobertura automatizada (unit + integration)
6. **Analytics:** Dashboard com eventos de uso (user behavior tracking)

---

**Status Final:** README completo, código limpo, pronto para merge e deploy via tag `v3.4.0-perfil-s2`. 🚀

