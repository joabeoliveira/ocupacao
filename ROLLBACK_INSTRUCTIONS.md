# Instruções de Rollback

Última atualização: 2026-02-24

Objetivo
- Passos para reverter um deploy da release `perfil_paciente` no EasyPanel e via Git, além de verificações e observações.

EasyPanel — Rollback rápido (recomendado quando o deploy é feito pelo EasyPanel)
1. Abra o EasyPanel e selecione a aplicação correspondente a este repositório.
2. Acesse a seção Deployments / Releases.
3. Localize a tag ou deploy anterior que estava funcionando (ex.: `v2.0.0-baseline-perfil`, `v3.3.8`).
4. Selecione essa tag/commit e escolha Deploy (ou Redeploy).
5. Confirme e monitore os logs de build até o término do deploy.
6. Execute a checklist de verificação abaixo.

Rollback via Git (quando o EasyPanel exige referência Git)
1. No GitHub, confirme a tag/commit alvo para a qual deseja reverter.
2. No EasyPanel, escolha Deploy → From Git → selecione a **Tag** desejada (ex.: `v2.0.0-baseline-perfil`) ou o **Branch** no commit desejado.
3. Inicie o deploy e acompanhe os logs.

Rollback manual (substituindo a imagem atualmente implantada)
1. Se o deploy usa imagens Docker, localize a última imagem estável (tag) no registro de imagens.
2. Atualize a configuração de deployment para usar essa tag de imagem e redeploy.

Checklist de verificação (após o rollback)
- [ ] A interface web carrega (`/`) e `/perfil_paciente` retorna 200.
- [ ] `/api/perfil_paciente/resumo` retorna 200 com JSON no formato esperado.
- [ ] `/api/perfil_paciente/graficos` retorna séries/labels consistentes com o baseline.
- [ ] Endpoint de exportação XLSX funciona e os arquivos são baixados.
- [ ] Não há novos erros nos logs da aplicação por 10 minutos após o rollback.

Observações importantes
- Esquema do banco: o rollback do código é seguro apenas se nenhuma alteração de esquema de BD (migrações) tiver sido aplicada pela release com problema. Se houver migrações, o código antigo pode ficar incompatível com o esquema atualizado.
- Dados alterados: se o deploy problemático gravou dados que o código anterior não entende, pode ser necessário limpeza ou migração adicional.
- Segredos / Configurações: confirme que as variáveis de ambiente no EasyPanel estão corretas para a tag alvo (normalmente elas persistem entre deploys, mas vale verificar).
- Backups: antes de qualquer rollback que possa afetar esquema ou dados, faça backup do banco.

Se o rollback falhar
- Verifique os logs do EasyPanel para identificar o passo com erro. Se uma tag antiga falhar ao deployar, pode haver dependências externas (registro de imagens, falha no build, variáveis faltando).
- Se estiver preocupado com o vazamento de `.env`, rotacione as credenciais imediatamente e redeploy a tag de destino com as variáveis atualizadas.

Contato
- Peça suporte ao desenvolvedor que fez o release ou solicite que eu execute o rollback (posso disparar o deploy pela tag Git ou orientar passo a passo no painel).
