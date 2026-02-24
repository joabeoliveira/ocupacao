# Sprint 2 — Plano: Performance & Confiabilidade

Última atualização: 2026-02-24

Objetivo do Sprint
- Reduzir latência e carga nas APIs do `perfil_paciente` e tornar as consultas mais robustas para produção. Entregáveis principais: cache para endpoints core, jobs de pré-agregação, testes automatizados e métricas básicas.

Escopo (priorizado)
1. Cache em memória (core): implementar cache (Redis) para `/api/perfil_paciente/resumo` e `/api/perfil_paciente/graficos` com TTLs configuráveis.
2. Pré-agregação: criar job agendado (cron) que popula tabelas/materialized views com métricas por dia/clinica/idade/sexo para consultas rápidas.
3. API: melhorar paginação (keyset), limitar tamanho de export e usar streaming para downloads grandes.
4. Testes: adicionar testes unitários e de integração para as APIs (pytest) e um teste que valida export XLSX.
5. Observabilidade: adicionar logs estruturados e métricas (tempo de resposta, taxa de erro); exportar para Prometheus/Grafana (ou serviço compatível).

Backlog técnico (detalhado)
- 2.1. Escolher infra de cache: Redis (recomendado). Adapter simples em `app.py` para ler/gravar cache por chave (params hash).
- 2.2. TTLs por endpoint: resumo=60s, graficos=300s (configurável via ENV). Invalidação manual quando se fizer ETL diário.
- 2.3. Job de pré-agregação: script em `scripts/preagg.py` e agendamento via cron container ou Celery beat (opção). Armazenar em tabela `agg_perfil_paciente_daily`.
- 2.4. Migração/DDL: criar SQL para tabela de agregados (`estrutura_db_preagg.sql`). Incluir índices em (data, clinica, sexo).
- 2.5. Export otimizado: usar `pandas` em chunk ou generator para escrever XLSX sem carregar tudo em memória.

Critérios de aceitação
- Latência do endpoint `/api/perfil_paciente/resumo` < 250ms média sob carga leve (dados agregados em cache).
- `/api/perfil_paciente/graficos` responde com séries pré-agregadas e correto formato JSON.
- Testes automatizados passam com cobertura mínima para novos módulos.
- Métricas básicas visíveis no painel (requests, errors, 95th perc latency).

Risco e mitigação
- Risco: Inconsistência entre dados em cache e origem. Mitigação: TTL curto para resumo, invalidação explícita após jobs de ETL.
- Risco: Migrations para tabelas de pre-agg podem exigir janela de manutenção. Mitigação: aplicar em janela de baixa movimentação e ter backups.

Estimativa e resumo de tarefas (sugestão de divisão)
- Dia 1: Design e setup Redis + cache wrapper (`app.py`) — 1 dia
- Dia 2: Implementar cache para endpoints core + testes unitários básicos — 1 dia
- Dia 3: Criar job de pré-agregação e SQL DDL + teste local do job — 1 dia
- Dia 4: Instrumentação de métricas e logs + integração em dashboard — 1 dia
- Dia 5: Testes de integração, ajustes e documentações (README) — 1 dia

Branch e entregáveis
- Branch sugerida: `feature/perfil-paciente-sprint2`
- Arquivos a criar/alterar principais:
  - `scripts/preagg.py`
  - `migrations/` (DDL para `agg_perfil_paciente_daily`)
  - `app.py` (cache wrapper + TTL config via ENV)
  - `tests/test_perfil_paciente_api.py`
  - `SPRINT_2_PLAN.md` (este arquivo)

Variáveis de ambiente novas sugeridas
- `REDIS_URL` (ex: redis://:pass@redis.example.com:6379/0)
- `CACHE_TTL_RESUMO` (default 60)
- `CACHE_TTL_GRAFICOS` (default 300)

Próximos passos imediatos (o que faço agora se autorizar)
1. Criar a branch `feature/perfil-paciente-sprint2` e fazer um commit inicial com o `SPRINT_2_PLAN.md` e esqueleto de `scripts/preagg.py`.
2. Implementar o cache wrapper e configurar `REDIS_URL` como variável de ambiente no ambiente de teste.

Decisão necessária do Product Owner
- Priorizar cache em memória (Redis) ou começar direto pela pré-agregação no banco? (recomendo começar pelo cache — entrega mais rápida e impacto imediato).
