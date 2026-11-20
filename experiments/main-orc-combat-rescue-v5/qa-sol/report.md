# QA independente — três chaves corporais back_r/Axe

Atualização posterior: o freeze repair1 recebeu **READY_FOR_INTERMEDIATES**, limitado ao reparo BODY-01, em [impact-repair1-report.md](impact-repair1-report.md) e [impact-repair1-result.json](impact-repair1-result.json). O parecer abaixo permanece histórico da versão original identificada por seus hashes.

**Veredito: REVISIONS_REQUIRED · ARTISTIC_REVISION_REQUIRED · PENDING_CREATOR.** Revisão limitada ao freeze do especialista corporal, sem produção, propagação ou alteração da matriz. Preparação e ápice são estruturalmente utilizáveis; a leitura da mão dominante no impacto precisa de correção antes de expandir os intermediários.

## Inspeção e freeze

Foram abertas as três imagens AFTER nativas sem marcações e a base canônica real. Foram inspecionadas no tamanho nativo apresentado pela ferramenta e em ampliações nearest-neighbor construídas diretamente dos exports finais em `qa-sol`, sem anotações. O composto256 de impacto também foi aberto. As ampliações diagnósticas antigas do produtor foram vistas inicialmente, mas não fundamentam o parecer final: diferem dos exports finais em acabamento/registro. Os BEFORE não foram necessários. Nenhum artefato de opinião de outro QA foi consultado; o relatório do produtor contém referência histórica a um QA anterior de F06, que não fundamenta esta revisão.

`input-freeze.json` registra caminhos e SHA-256 efetivamente calculados, incluindo fontes Aseprite, exports, metadados e entradas. Seu SHA-256 é `1124ffb3e415cadd801a3370509b654c8114bfe6f0a60034618f70ff7921896a`. Os hashes declarados comparados coincidem; isso identifica a versão, não comprova anatomia. O QA não reabriu/reexportou Aseprite: a verificação de reexportação do produtor foi lida, sem ser apresentada como execução independente.

| Chave | SHA-256 do PNG nativo final | Parecer estático |
|---|---|---|
| 01-hoist | `d8378297cbba9a41ee7c47262d266acf92477b53ab1c02bc6b62d9e8f9cf1490` | Estrutura aceitável |
| 02-apex | `3cbfe50f246621f6d7222fd80fb4b4567c11bc2f22fe72968e7b027f4c76e3ba` | Estrutura aceitável, margem superior apertada |
| 03-impact | `a6317e94aa2e50aaaa23bdc8bd2e0483f27bd59201d1d2ec91e3aadb2197c5c5` | Revisão da extremidade dominante |

## Achados por quadro

**01-hoist.** Braço direito anatômico elevado à direita da imagem; ombreira, braço, cotovelo flexionado, antebraço retornando para dentro e luva fechada formam uma cadeia legível. Não se vê antebraço duplicado ou arma pintada no corpo. O braço esquerdo desce à esquerda e termina em mão própria, com separação da cintura; não é arma disfarçada. Crânio occipital verde, gola, dorsal escura, couro vinho, cota e grevas mantêm a leitura da base V1. Quadris ficam entre botas apoiadas e joelhos flexionados. A pose permite ler carga/preparação overhead; não prova por si só torque ou peso em movimento.

**02-apex.** A mão direita retorna mais para dentro da silhueta superior; cotovelo e antebraço permanecem conectados à ombreira. A mão esquerda se afasta, com punho e volume de luva reconhecíveis. Tronco/pelve e base mudam discretamente em relação à preparação. O punho superior tem contorno fechado, mas está muito próximo do topo nativo. Isso é uma observação de enquadramento, não reprovação por falta de uma altura universal do punho. Reserva para equipamento precisa ser resolvida no composto256, sem cortar ou encolher a arma. Identidade e lateralidade não apresentam contradição visível nesta chave.

**03-impact — BODY-01, MEDIUM, bloqueia intermediários.** A inclinação conjunta de cabeça/placa dorsal, a queda da cintura escapular, a pelve mais baixa e a abertura dos apoios produzem uma direção corporal plausível para a entrega do golpe. O braço esquerdo e sua mão baixa continuam autênticos e legíveis. No lado direito, ombreira, braço e cotovelo chegam a um antebraço contínuo; porém a extremidade distal termina numa cunha escura junto à cintura/quadril, aproximadamente x89..98/y75..85 no nativo128. Não há volume de luva fechada/palma suficientemente distinguível da braçadeira e do quadril, em contraste com as luvas das chaves elevadas e com a mão inativa deste próprio quadro. A leitura fica mais fraca no tamanho nativo. **Não afirmo amputação anatômica provada:** pode haver mão ocluída ou comprimida na projeção; a falha observada é não conseguir rastrear visualmente punho e mão dominante como término articulado seguro para uma pegada. Overlay de arma não deve ser usado para esconder essa ambiguidade.

Correção solicitada: tornar legível no próprio corpo layers-off a transição antebraço–pulso–mão direita e o volume terminal da luva no impacto, preservando a entrega de tronco/pelve/joelhos e os apoios que funcionam. Reavaliar o export exato corrigido antes de gerar intermediários. Não é necessário regenerar as duas chaves elevadas por este achado. Não se prescreve cor, fórmula de punho acima da coroa ou compra de geração.

Evidência direta: `03-impact-exact-unmarked-6x.png` e `03-impact-right-chain-exact-unmarked-15x.png`, obtidas do PNG final sem edição artística. As demais ampliações finais são `01-hoist-exact-unmarked-6x.png` e `02-apex-exact-unmarked-6x.png`.

## Limitações e portão

Este é um parecer visual estático de três chaves, sem player Chromium, animação completa, intermediários, descida contínua ou recuperação. A ferramenta exibiu imagens reais; não houve bloqueio de leitura visual. A resolução128 limita a discriminação de dedos e não permite provar anatomia tridimensional escondida. A ausência de arma permite julgar o corpo e procurar contaminação visível; não permite provar trajetória, arco, torque, contato ou pegada do machado. Os160ms de cada arquivo são holds de inspeção, não timing de combate validado. Não se declara ciclo1× demonstrado.

O empacotamento continua **TECHNICALLY_COMPLETE conforme a entrega técnica do produtor**, com hashes conferidos neste escopo. Arte permanece **ARTISTIC_REVISION_REQUIRED / PENDING_CREATOR**. Sem aprovação do criador, sem autorização de intermediários por este QA, sem Unity. Root mantém a decisão e a orquestração.

## Marco separado de pegada

O checkpoint `GRIP_F02_F08_READY` apareceu durante a revisão. As duas pegadas foram examinadas separadamente; parecer em `grip-F02-F08-result.json` e `grip-F02-F08-report.md`. Nenhum resultado de pegada altera o veredito corporal acima.
