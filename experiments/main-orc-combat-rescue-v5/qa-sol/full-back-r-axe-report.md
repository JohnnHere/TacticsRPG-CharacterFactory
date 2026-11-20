# QA independente — ciclo corporal back_r/Axe, 12f/1100ms

**INCONCLUSIVE para liberação do ciclo completo · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR.** Não foi identificado defeito estático bloqueante nos12 quadros. O parecer positivo `BODY_CYCLE_READY_FOR_EQUIPMENT_AND_REAR_EXPANSION` não é emitido porque a naturalidade contínua em1× não pôde ser observada perceptualmente nesta interface. Isso é uma limitação da revisão, não um achado de arte que justifique regeneração ou uma nova reprovação BODY-01. Global permanece **ARTISTIC_REVISION_REQUIRED**.

## Versão e observação real

Clip: `characters/orc-v1/source/combat-rescue-v5/body-specialist/full-back-r-axe/clip.json`, SHA-256 **`2ab5ae40d7a11c0b4b271ca41f090608c3d721366da90ee1c6d1ebce9c1321c3`**. Representative SHA-256 `50eb4b78aa86a51ea8ea6e81ebaa563f30043a6ca0c306cd2b1d82900b39bb85`. Mestres256/128: `2d89c3c2565d4ac31b11ee9cbed4c35c3b8faaf641aa1ebf7ee79ce12e19317e` e `f789d6b90d520ba1b9a809d00a2f02ec8941746439365863b29e66d0dc15e918`.

Foram vistos exports reais nativos, a sequência completa sem marcações e capturas próprias do player original em Chromium, sem equipamento. As interfaces CUA não tinham navegador registrado; a abertura de uma aba Paseo expirou sem responder. Como alternativa foi usado o Microsoft Edge Chromium instalado, headless, com perfil e evidências exclusivamente em `qa-sol`.

O player original `review.html` foi aberto por file://. O QA executou reprodução1× e0,5×, passo a quadro e capturas de F05/F06/F07, exibindo simultaneamente128px nativo,64px tático e384px diagnóstico. O relógio percorreu F00..F11 e parou em F11: aproximadamente1103ms de parede para1100ms em1× e2212ms em0,5×. Os registros são verificações funcionais de reprodução e capturas discretas. **Não equivalem a assistir à animação contínua como jogador; não afirmo ter percebido fluidez, peso ou eventuais pops em1×.**

## Achados visuais por quadro

| Quadros | O que foi observado nas imagens reais |
|---|---|
|F00|Guarda original, ambas as mãos próprias e baixas, crânio occipital e dorsal traseira coerentes.|
|F01|Início sutil da carga; braço direito muda sem desaparecer, braço esquerdo termina em luva independente.|
|F02|Braço direito elevado à direita da imagem, cotovelo flexionado e antebraço/punho para cima; apoio completo preservado.|
|F03|Hoist aceito anteriormente, reutilizado byte-exato; cadeia direita fechada sobre a coroa, mão inativa baixa legível.|
|F04|Ápice aceito anteriormente, byte-exato; mão direita fechada e contornada. Margem superior apertada continua exigindo espaço no futuro composto equipado.|
|F05|Início da descida: mão ainda alta e cotovelo dobrado; cabeça/dorsal começam a acompanhar a queda, sem arma ou membro duplicado visível.|
|F06|Passagem com antebraço direito projetado à frente/lado, punho vinho próprio e tronco já inclinado. É uma pose transitória de descida, não prova isolada de ápice ou arco pesado.|
|F07|Impacto repair1 byte-exato; pulso e luva direita distinguíveis, cintura escapular/pelve baixas, joelhos dobrados e base aberta. BODY-01 permanece resolvido neste quadro.|
|F08|Braço dominante retorna para baixo junto à lateral; mão inativa preservada, tronco começa a subir. Não se observa extremidade flutuante.|
|F09|Dorsal/pelve mais altas, joelhos e braços retornando ao guarda; botas continuam no plano de apoio.|
|F10|Acomodação próxima ao guarda, duas mãos próprias e silhueta traseira mantida.|
|F11|Retorno ao corpo de guarda, sem arma persistente.|

Identidade: crânio verde occipital, gola traseira, placa dorsal, couro vinho, cota, grevas e botas mantêm a linguagem V1. Não se observa rosto frontal emprestado, haste/lâmina pintada no corpo, antebraço duplo ou mão inativa usada como arma nos quadros examinados. Não se vê franja branca/cinza na coroa. Não há novo achado estático acionável que sustente `REVISIONS_REQUIRED`.

Ponto temporal ainda aberto: F05→F06→F07 combina grande deslocamento da mão/antebraço com queda do tronco em holds de50/60/110ms. As poses permitem reconstruir uma entrega descendente, mas a hipótese de leitura natural, pesada e contínua nesse trecho precisa de observação perceptual em1×. A subida F07→F08 e o retorno F10→F11 também precisam dessa checagem. Sem arma, trajetória do item, torque, pegada, encaixe e espaço do machado permanecem não demonstrados.

## Verificação independente focada

Os24 exports128/256 conferem com os hashes do clip; os12 recortes64,64 coincidem pixel a pixel com os nativos. Todos os nativos atingem chão126. Há zero pixels de corpo com RGB simultaneamente acima de190; esse teste apoia a ausência de pixels muito claros, sem substituir a inspeção visual de halos. F03/F04/F07 são byte-idênticos às três chaves já avaliadas. Cabeçalhos dos dois mestres confirmam12 quadros e tempos `[70,80,90,100,110,50,60,110,100,100,100,130]ms`, total1100ms.

Detalhes em `full-cycles-input-freeze.json`, `full-cycles-pixel-checks.json` e `full-back-r-axe-browser-check.json`; o resultado separado contém todos os caminhos e hashes. Os39 arquivos deste escopo foram identificados; não se repetiu a auditoria dos80 arquivos históricos nem auditoria global. Não se reexportaram os mestres no Aseprite; a reexportação relatada pelo produtor não é atribuída ao QA.

## Portão e parada

**TECHNICALLY_COMPLETE** no empacotamento conferido; **VISUAL_REVIEW_REQUIRED** para completar a revisão temporal. Este parecer não libera expansão traseira/equipamento como ciclo artisticamente validado. O que falta é a observação contínua1×/escala de jogo do freeze exato, não uma correção de pixels indicada pelo QA. Sem indicação de regeneração, sem aprovação do criador ou Unity. Escritas apenas em `qa-sol`; Root mantém a decisão e recebe o limite explícito deste revisor.
