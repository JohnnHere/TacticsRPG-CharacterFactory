# back_r / Sword — uma tentativa F05 encerrada

**ARTISTIC_REVISION_REQUIRED · REJECTED_LOCAL_HYPOTHESIS · PENDING_CREATOR. NÃO INTEGRAR.** Uma hipótese foi testada em F05 e rejeitada na inspeção local. O trabalho termina aqui, sem nova iteração, propagação ou promoção. A falha é artística, não falta de autorização para redesenhar a mão.

[Comparador local por file://](index.html) · [F05 em128/64](F05-128-64-review.png) · [quatro representações antes/depois](F05-before-after-four-layers.png) · [vizinhos F04→F05→F06](F04-F05-F06-before-after.png).

## Diagnóstico focal e resultado

Foram relidas as seções5,6,9 do pedido original, o report.md de artist-rear e audit-expansion-bands.txt. Não foram usadas as fontes GLM R1/R2 nem a expansão flood/raio. O experimento de11px do Axe não foi utilizado.

Escolhi **F05**, com F04 como vizinho principal e F06 como referência de saída. A leitura do baseline mostra o pomo cinza sobre a região da manopla/punho e o cabo atravessando a mão sem um fechamento claro dos dedos. A cadeia ombro–cotovelo–punho permanece visível no body original; o problema focal não demonstrou uma amputação. A fonte achatada não contém uma segmentação anatômica que permita chamar todos os pixels opacos próximos ao cabo de dedos. F04 também apresenta sobreposição entre a arma e a região metálica da manopla, mas foi preservada neste teste único.

A espada independente tem lâmina, guarda, empunhadura e pomo discerníveis no próprio asset; o cabo não é apenas uma âncora. A análise foi visual nas fontes compostas/body/arma/handFront e nos respectivos recortes. As coordenadas são evidência de posição, não prova de pegada natural.

## Única hipótese executada

- Recriar localmente o fechamento da luva e sua junção ao punho em F05, mantendo ombro, cotovelo, antebraço principal e restante da pose.
- Reassentar a mesma espada por translação inteira(0,+8), de grip(181,121) para(181,129), mantendo o ângulo100°, escala e pixels originais do item.
- Substituir o handFront quadrado por15 pixels explicitamente desenhados como polegar/dedos na nova luva. Não foi usado flood, raio ou interseção genérica com body.
- Manter weaponBack→body→weaponFront→handFront e os tempos90/80/90/80/100/80/100/110ms=730ms.

Autoria e procedência: [author_f05.lua](author_f05.lua), [paleta/contornos/dedos registrados](hand-authoring.json), [wrapper batch privado](aseprite.mjs). Toda alteração raster ocorreu dentro do Aseprite. Os PNGs/pranchas externos são derivados e diagnósticos. O Lua parte dos snapshots verificados, salva os três forks e [export_saved.lua](export_saved.lua) os reabre, usando as posições reais dos cels antes de renderizar.

## Por que rejeitei a hipótese

A inspeção do corpo inteiro, recortes e captura em128/64 não oferece uma mão agarrando o cabo de forma convincente. O pomo deixou a antiga massa da palma, mas ficou visualmente junto da manga/punho. A luva ficou estreita/alongada em direção ao cabo; a junção com a manga e as poucas marcas dos dedos não sustentam a leitura de contato. Há risco concreto de parecer um cabo/mão separado ou apoiado no fim do antebraço. O desenho não resolveu com segurança a anatomia do punho.

O diagnóstico técnico encontra15 pixels no novo handFront,13 deles sobre pixels opacos do cabo, todos na faixa da empunhadura, zero sobre guarda ou pomo. **Mesmo assim a tentativa é rejeitada.** Esse resultado demonstra apenas que não se repetiu a ocultação da guarda/pomo do experimento anterior; não prova dedos, polegar, contato ou qualidade da pegada.

F04 e F06 permanecem intactos. O novo assento ainda muda o percurso local da raiz da espada em relação a esses vizinhos; manter os tempos e a rotação não demonstra uma transição natural. Não houve correção segura de continuidade neste checkpoint.

As bordas claras do corpo aparecem também no body sem arma. Não foram apagadas por regra de cor, groundY ou luma≥200, nem consideradas ausentes por tais medidas. Highlights metálicos fora da pequena área anatômica testada permanecem. Esta tentativa não resolve ou aprova o problema geral de rebordo dos ataques traseiros.

## Fontes e deltas reais

[Clip isolado completo e explicitamente rejeitado](../../../characters/orc-v1/source/targeted-repair-sword-sol-v1/clip.json), com referências e SHA-256 reais. eligibleForIntegration=false; integrationStatus=DO_NOT_INTEGRATE.

- Master composto: characters/orc-v1/source/targeted-repair-sword-sol-v1/source/sword-f05-grip-composite.aseprite
- Master body: characters/orc-v1/source/targeted-repair-sword-sol-v1/source/sword-f05-grip-body.aseprite
- Master nativo: characters/orc-v1/source/targeted-repair-sword-sol-v1/source/sword-f05-grip-native.aseprite

Hashes dos masters, respectivamente:

    a8f84ec1fa1c1d72c3902f63aff198efc16c7f2302607e029d16c4970e7f9735
    25a9b29ec928afcd3d3706df1ed8a000d99bacfa4ecc31798d0df66615f9e6ea
    e53eb614fcc9b341a55bf85a12685c380b01d65c713891681ee8d9d6f478ee32

Somente **F05** mudou. Deltas RGBA: **192 pixels body;1215 posições weaponFront pela translação;87 posições handFront comparando a máscara antiga à nova;1227 pixels no composto final**. weaponBack permanece idêntico. Estes números não são somáveis como pixels novos de arte.

F00/F01/F02/F03/F04/F06/F07 têm zero diferenças RGBA em todas as quatro camadas e no composto. Tempos e referências do item independente foram preservados. Nativo128 é crop central exato do body256, deslocamento(+64,+64).

## Provas executadas e limites

[verification.json](verification.json) registra recomposição exata das quatro camadas,32 comparações entre camadas baseline e export fresco,16 comparações com os masters body/native reabertos, canvas, crop central, cels/timings e deltas por quadro. [source-document.json](source-document.json) registra camadas e posições reais dos cels. O empacotamento técnico passou; isso não mudou o veredito artístico.

O comparador foi aberto em Chromium headless por **file://**; fontes carregaram sem requisições falhas/erros JS e os controles foram usados em F04/F05/F06. Capturas: [F04](F04-128-64-review.png), [F05](F05-128-64-review.png), [F06](F06-128-64-review.png). [preview-check.json](preview-check.json) registra exatamente esse alcance. O player oferece1×/0,75×/0,5× e passo a quadro.

**Não percebi reprodução contínua1× em uma sessão visual ao vivo.** A avaliação local usa inspeção estática e capturas por quadro; relógio correto, playback disponível ou alpha de contato não resolvem a percepção de movimento. Não reivindico QA independente, aprovação visual, avaliação de câmera Unity ou aprovação do criador.

## Preservação e encerramento

Os53 arquivos de entrada baseline/backup foram reconferidos por SHA-256, incluindo os três masters e o asset independente. Os96 arquivos protegidos do checkpoint Unarmed e seu inventário continuam idênticos. Nenhum arquivo daquele candidato foi escrito.

As escritas ficaram exclusivamente em artist-sword-sol/ e targeted-repair-sword-sol-v1/. Nenhuma matriz, página canônica, outro clipe ou documento compartilhado foi alterado. Não houve agente/QA adicional, PixelLab, Unity, commit ou promoção.

O item, fontes, script e exports da hipótese permanecem preservados para explicar a falha; não são uma sugestão de integração. **ARTISTIC_REVISION_REQUIRED / REJECTED_LOCAL_HYPOTHESIS / PENDING_CREATOR. Relatório fechado; nenhuma iteração adicional será executada.**
