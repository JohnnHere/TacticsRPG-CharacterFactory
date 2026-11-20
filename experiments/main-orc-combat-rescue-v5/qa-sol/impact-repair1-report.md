# Re-QA independente — BODY-01 / impacto back_r/Axe repair1

**READY_FOR_INTERMEDIATES · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR.** O achado BODY-01 está resolvido para o portão das chaves corporais. O parecer anterior permanece histórico da versão anterior; este parecer se aplica somente ao freeze repair1 identificado abaixo. Status global permanece **ARTISTIC_REVISION_REQUIRED**, sem aprovação do criador, ciclo completo ou integração.

## Leitura visual do reparo

O mesmo revisor abriu o PNG nativo128 final, o composto256 final e os BEFORE/AFTER sem marcações de corpo inteiro e mão. A luva direita agora tem massa arredondada vinho, face de nós dos dedos, polegar interno e separações escuras entre dedos. A braçadeira metálica afunila para um pulso identificável e daí para a mão fechada. A extremidade distingue-se do quadril e deixa de terminar na cunha escura ambígua do freeze anterior. Essa mudança também aparece no tamanho nativo; a ampliação confirma a ligação em vez de ser a única escala em que se reconhece uma mão.

O braço direito dominante permanece no lado direito da imagem: ombro e cotovelo conduzem ao mesmo antebraço descendente, e agora a cadeia termina numa luva reconhecível, sem descontinuidade transparente ou membro duplicado. O volume novo acompanha o couro e a armadura existentes. Nenhum overlay de arma encobre a ligação. Não há novo achado bloqueante para este portão.

A entrega do impacto permanece: cabeça/placa dorsal inclinadas, cintura escapular baixa, pelve cedida, joelhos flexionados e base aberta com botas apoiadas. A mão esquerda inativa continua própria e legível. O retoque local não regrediu esses elementos.

## Freeze e verificação focada

| Artefato | SHA-256 calculado e conferido |
|---|---|
| Representative repair1 | `e4434397532c4a42690be0acae5344a5185f0e1fbe19574cf78bd2b1672471c3` |
| Impacto PNG128 | `dcff5167804f57cfcaff22deb0b6cc294c17346e4f41ef925e8b5d24eed60a8a` |
| Impacto PNG256 | `6a035a842c2a2453665fe6dc8b20d9792966754b92c0d3f4582e3dcda24475c4` |
| Mestre128 | `4db32e40a433019ba6e9fa3f0b63ab561f475af1b49ef0814ff353f5bd7cc35f` |
| Mestre256 | `16c239dc7c580a2727cba98af5536eccac278aeee51a9af930d339fe4e9458c4` |

A comparação independente dos PNGs antes/depois confirmou **97 pixels ARGB alterados**, limites inclusivos **x88..98/y75..86**, **zero alterações fora dessa região**. Portanto tronco, pelve, joelhos, apoios, cabeça e cadeia proximal fora da máscara mantêm pixels idênticos. O recorte64,64 do composto256 coincide integralmente com o nativo128. Os cabeçalhos dos dois mestres salvos indicam um frame de160ms. Os oito hashes dos mestres/exports de hoist e ápice conferem com o freeze independente anterior; suas avaliações estruturais permanecem válidas, sem repetir inspeção ou produção dessas chaves.

Dados independentes em `impact-repair1-checks.json`; caminhos, hashes calculados, comparações dos aliases e limitações completas em `impact-repair1-result.json`. Os hashes identificam o alvo do parecer e a preservação local; a aceitação do reparo decorre da inspeção visual da transição pulso–luva. A reexportação Aseprite do produtor foi lida, sem ser reexecutada ou atribuída ao QA. Não se repetiu auditoria ampla.

## Limites e próximo marco

O conjunto de hoist/ápice preservados mais este impacto está **READY_FOR_INTERMEDIATES**. Root pode prosseguir desse freeze para a construção dos intermediários e submeter o movimento completo à revisão em escala nativa e velocidade normal. Três chaves estáticas e holds de160ms não demonstram um ciclo1×, descida contínua, recuperação, transferência dinâmica de peso ou continuidade temporal.

Sem arma presente, não há prova de arco de item, torque, encaixe ou pegada final. Não foi aplicado requisito universal de punho acima da coroa. Não há limitação de acesso às imagens; a anatomia oculta e os detalhes abaixo da resolução continuam limitados pelo próprio raster128. F02/F08 e o trabalho parcial full-front-r-sword não foram revisitados. Escritas exclusivamente em `qa-sol`; arte e matriz permaneceram read-only. Parada neste marco, aguardando Root.
