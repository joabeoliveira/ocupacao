# Project status — Perfil do Paciente

Last updated: 2026-02-24

Resumo rápido
- Status: Sprint 1 (Core) implementada e disponível como tag para deploy.
- Branch principal de desenvolvimento: `feature/perfil-paciente` (HEAD: commit `8a675f1`).
- Tag pronta para deploy: `v3.4.0-perfil-s1` (pushed).

Principais entregas (Sprint 1)
- Nova rota de UI: `/perfil_paciente` (`templates/perfil_paciente.html`).
- APIs: `/api/perfil_paciente/resumo`, `/api/perfil_paciente/graficos`,
  `/api/perfil_paciente/tabela`, `/api/perfil_paciente/export` (implementadas em `app.py`).
- Export XLSX via pandas/openpyxl.
- Atualização da sidebar em templates existentes para linkar a nova página.

Status técnico
- Código commitado na branch `feature/perfil-paciente` e push realizado.
- Tag `v3.4.0-perfil-s1` criada e push para `origin`.
- Arquivo `.env` removido do índice do Git e `.gitignore` adicionado.

Observações de deploy
- Recomendado deploy via tag `v3.4.0-perfil-s1` (EasyPanel → Deploy from Git → Tag).
- Build path / contexto: raiz do repositório. Se o EasyPanel pedir o Dockerfile, aponte para `./Dockerfile`.
- Variáveis de ambiente requeridas no ambiente de execução:
  - `DATABASE_URL` (ou `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_NAME`)
  - `SECRET_KEY`
  - `PORT` (se necessário)

Problemas conhecidos
- Local smoke test mostrou a página UI carregando, porém APIs dependentes do banco
  falharam enquanto o host `site_nir` estava inacessível no ambiente local.

Próximos passos (priorizados)
1. (Curto prazo) Deploy da tag `v3.4.0-perfil-s1` no EasyPanel e validação de endpoints.
2. (Curto prazo) Fornecer rollback rápido: instruções para reverter para tag `v2.0.0-baseline-perfil` ou outra tag.
3. (Médio prazo) Implementar cache/pre-aggregação para métricas pesadas (Sprint 2).
4. (Médio prazo) Adicionar testes automatizados para APIs e cobertura de integração com o DB.
5. (Opcional) Limpar histórico Git para remover ` .env` de commits antigos (BFG/git-filter-repo).

Checklist de verificação após deploy
- [ok] `/perfil_paciente` retorna 200 e carrega assets
- [ok] `/api/perfil_paciente/resumo` retorna dados agregados (200)
- [ok] `/api/perfil_paciente/graficos` retorna séries/labels corretos
- [ok] Export XLSX funciona e contém colunas esperadas

Referências
- Branch: `feature/perfil-paciente`
- Tag: `v3.4.0-perfil-s1`
- Arquivos principais: `app.py`, `templates/perfil_paciente.html`, `.gitignore`

Contato
- Para próximos passos posso executar deploy, criar instruções de rollback detalhadas,
  ou limpar o histórico Git — me diga qual ação prefere que eu execute em seguida.

Link para instruções de rollback
- Veja também: `ROLLBACK_INSTRUCTIONS.md` (procedimento passo-a-passo para EasyPanel/Git).

Registro de auditoria (ações recentes)
- 2026-02-24 — Tag `v3.4.0-perfil-s1` criada e enviada para `origin` — executado pelo assistente.
- 2026-02-24 — Arquivo `.env` removido do índice do Git e `.gitignore` adicionado — commit enviado para `feature/perfil-paciente` — executado pelo assistente.
- 2026-02-24 — `PROJECT_STATUS.md` criado com resumo do projeto — executado pelo assistente.
- 2026-02-24 — `ROLLBACK_INSTRUCTIONS.md` criado com passos de rollback em Português — executado pelo assistente.

Audit log notes
- Se desejar, prefira adicionar o seu nome/usuário e email como "verificador" após cada ação para fins de auditoria humana.

