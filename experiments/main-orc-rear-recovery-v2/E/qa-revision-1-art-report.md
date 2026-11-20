# QA revision 1 — ART checkpoint parcial

**Estado:** `ARTISTIC_REVISION_REQUIRED`; não é checkpoint aceito, não é aprovação artística. A tarefa para neste handoff. Nenhuma arma foi composta e nenhum mestre, PNG, `clip.json` ou metadado canônico foi alterado nesta execução. Total de geração permanece 78 unidades / 17 jobs; chamadas novas: zero.

## Preservação e saídas

Root verificou a cópia anterior ao freeze em `experiments/main-orc-rear-recovery-v2/rejected/qa-revision-1-before/backup-manifest.json` (192 arquivos comparados com o freeze `6fa4653e…`). A cópia adicional criada antes deste handoff em `E/rejected/qa-revision-1-before/` permanece preservada.

Os scripts de autoria e exportação Aseprite estão em `E/qa-revision-1/author_body_checkpoint.lua` e `E/qa-revision-1/export_body_checkpoint.lua`. Mestres body-only staged, salvos em Aseprite e reexportados do próprio mestre:

- `E/qa-revision-1/body-checkpoint/source/back_l-sword-body-revision-1.aseprite` e `back_l-sword-native-body-revision-1.aseprite`.
- `E/qa-revision-1/body-checkpoint/source/back_r-axe-body-revision-1.aseprite` e `back_r-axe-native-body-revision-1.aseprite`.
- `E/qa-revision-1/body-checkpoint/source/back_l-axe-body-revision-1.aseprite` e `back_l-axe-native-body-revision-1.aseprite`.

Folhas e frames derivados dos mestres salvos estão em `E/qa-revision-1/body-checkpoint/exports/{back_l-sword,back_r-axe,back_l-axe}/`. São evidência staged parcial; não devem ser integradas como arte aceita.

## Registro corrigido e limites visuais

As imagens estáticas `characters/orc-v1/source/complete-v1/back_l/Idle/00.png` e `back_r/Idle/00.png` têm **256×256**, não 128×128. A primeira versão do script as deslocou mais 64 px; isso amputou a mão não atacante de SwordL. A função de carregamento foi corrigida para validar dimensões e usar PNG 256×256 diretamente, ou deslocar 64 px apenas quando a fonte for 128×128. Essa correção de registro está no script staged.

O Root rejeitou a folha anterior e localizou corretamente a tira branca de SwordL F05 no **ombro esquerdo da imagem, junto ao punho atacante/colo**. A máscara staged anterior atingia o lado errado e não resolve QA-01. A mão não atacante também não recebeu aprovação visual. QA-01 continua aberto.

Na última exportação body-only inspecionada, permanecem defeitos visíveis: QA-02, cabeça curva em AxeR F01 e haste em F02–F03; QA-03, a cadeia F04/F05 ainda exige revisão visual do punho e da remoção completa do membro antigo; QA-04, o gancho claro de AxeL F02–F03 não foi removido satisfatoriamente. As máscaras locais tentadas estão preservadas no Lua e não constituem correção aceita. Não usar seus contadores de pixels como evidência de anatomia ou limpeza.

Folhas efetivamente exportadas que servem apenas de checkpoint parcial:

- `E/qa-revision-1/body-checkpoint/exports/back_l-sword/body-only-sheet-qa.png`
- `E/qa-revision-1/body-checkpoint/exports/back_r-axe/body-only-sheet-qa.png`
- `E/qa-revision-1/body-checkpoint/exports/back_l-axe/body-only-sheet-qa.png`

Nenhuma composição, export final de clipe, atualização de hash/metadata, execução de validator ou alteração do manifesto canônico foi feita. As fontes originais e as cópias de backup permanecem intactas. O próximo responsável deve retomar a autoria no Aseprite com o mapa 256×256 confirmado e as coordenadas QA originais, começando pela tira de SwordL no ombro image-left indicada pelo Root; manter as três células em `ARTISTIC_REVISION_REQUIRED` até revisão visual real. Não propagar pixels staged, não promover candidato e manter `PENDING_CREATOR`.
