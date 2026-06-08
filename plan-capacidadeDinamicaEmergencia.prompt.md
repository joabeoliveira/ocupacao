## Plan: Analisar start.md e preparar mudanças

TL;DR - Ler e mapear o conteúdo de `atualizacaoSMSRio/start.md`, identificar decisões de negócio pendentes, listar arquivos e endpoints impactados, e propor passos concretos para implementar e testar as mudanças (pré-parto, capacidade dinâmica, UI e auditoria).

Steps
1. Ler `atualizacaoSMSRio/start.md` e resumir os objetivos e pendências (completo).
2. Identificar referências e arquivos impactados: `app.py`, `templates/emergencia.html`, `atualizacaoSMSRio/STATUS.md`, `calculos-formulas.md`, CSVs na pasta `atualizacaoSMSRio` (dependência direta).
3. Priorizar dúvidas de negócio listadas em `duvidas.md` e marcar reunião/decisão com PO.
4. Definir tratamento para pré-parto (251): cenário separado vs agregado; documentar impacto em endpoints/API e frontend.
5. Implementar/ajustar endpoints necessários (`/api/emergencia/stats`, possivelmente `/api/prepart/stats`) e constantes em `app.py` (paralelo a criação de branch no GitHub).
6. Atualizar frontend (`templates/emergencia.html`, `painel.html`) para distinguir `taxa_nominal` vs `taxa_dinamica` e exibir alertas quando taxa >100%.
7. Criar/atualizar testes automatizados (unit e integração) cobrindo taxa dinâmica, pré-parto, e logs de auditoria.
8. Auditar logs em staging, criar PR na branch `feature/capacidade-dinamica-emergencia` e proceder com revisão/merge/deploy seguindo `DEPLOY_EASYPANEL_RELATORIOS.md`.

Relevant files
- `atualizacaoSMSRio/start.md` — documento mestre de atualização
- `atualizacaoSMSRio/duvidas.md` — dúvidas de negócio a resolver
- `atualizacaoSMSRio/STATUS.md` — rastreamento de implementação
- `app.py` — backend principal, endpoints e constantes
- `templates/emergencia.html` — frontend de emergência
- `atualizacaoSMSRio/calculos-formulas.md` — fórmulas esperadas

Verification
1. Executar `python -m pytest tests/test_capacidade_emergencia.py` (ou criar equivalente) para validar comportamento.
2. Validar que `/api/emergencia/stats` retorna `taxa_dinamica` e `taxa_nominal` com CSVs de teste importados.
3. Conferir que alertas visuais aparecem em `templates/emergencia.html` quando taxa >100% e que logs `[AUDITORIA NIR]` são gerados.
4. Revisão em staging: importar `2026-05-01.csv` e `dados de ocupacao de 15-05-2026.csv` para validar cenários.

Decisions / Assumptions
- Implementação técnica baseada em `app.py` v3.5.0 (já contém constantes iniciais e rota `/api/emergencia/stats`).
- Necessário decidir mapeamento de nomes e se pré-parto (251) é separado.

Further Considerations
1. Perguntar ao PO: opção de mapeamento de nomes (Manter novos nomes / Abstrair / Mostrar histórico + novo). Recomendo opção que preserve histórico (tooltip) para auditoria.
2. Confirmar se Pré-parto (251) deve ter cenário próprio. Recomendo cenário próprio para relatórios clínicos.

Branch analysis
- Branch `feature/capacidade-dinamica-emergencia` confirmada e ativa (.git/HEAD aponta para ela).
- Commit atual: `2c91a9706f694f4eb498f8e7a2e8ec94375fcd60`.
- Alterações principais: `app.py` (constantes, endpoints), `VERSION.py` (3.5.0), testes em `tests/test_capacidade_emergencia.py`.
- Pendências críticas: frontend (`templates/emergencia.html`) não atualizado; `pytest` não está em `requirements.txt`.

Ações recomendadas imediatas
1. Adicionar `pytest` a `requirements.txt` e rodar testes localmente.
2. Atualizar `templates/emergencia.html` (suggestedMax, card vermelho, tooltip) e validar visualmente.
3. Comparar `/api/emergencia/stats` com query SQL em DB para validar números.
4. Criar PR com checklist (testes, validação API, frontend, logs de auditoria).
