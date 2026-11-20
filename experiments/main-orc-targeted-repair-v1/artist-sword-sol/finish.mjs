import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const E='experiments/main-orc-targeted-repair-v1/artist-sword-sol',S='characters/orc-v1/source/targeted-repair-sword-sol-v1';
const read=p=>JSON.parse(fs.readFileSync(p)),write=(p,x)=>fs.writeFileSync(p,JSON.stringify(x,null,2)+'\n');
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const inv=read(`${E}/before-inventory.json`),v=read(`${E}/verification.json`),c=read(`${S}/clip.json`);
for(const r of inv.files)if(sha(r.source)!==r.sha256||sha(r.backup)!==r.sha256)throw Error(`Original/backup changed:${r.source}`);
for(const r of inv.protectedUnarmed)if(sha(r.path)!==r.sha256)throw Error(`Unarmed changed:${r.path}`);
const report=`# back_r / Sword — uma tentativa F05 encerrada

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

[Clip isolado completo e explicitamente rejeitado](../../../${S}/clip.json), com referências e SHA-256 reais. eligibleForIntegration=false; integrationStatus=DO_NOT_INTEGRATE.

- Master composto: ${c.master}
- Master body: ${c.bodyMaster}
- Master nativo: ${c.nativeMaster}

Hashes dos masters, respectivamente:

    ${c.masterSha256}
    ${c.bodyMasterSha256}
    ${c.nativeMasterSha256}

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
`;
fs.writeFileSync(`${E}/report.md`,report);
write(`${E}/checkpoint.json`,{state:'CLOSED_REJECTED_NO_MORE_ITERATIONS',artisticStatus:'ARTISTIC_REVISION_REQUIRED',proposalStatus:'REJECTED_LOCAL_HYPOTHESIS',creatorApproval:'PENDING_CREATOR',eligibleForIntegration:false,scope:'back_r/Sword F05 only',testedHypotheses:1,report:`${E}/report.md`,review:`${E}/index.html`,isolatedClip:`${S}/clip.json`,unchangedFrames:[0,1,2,3,4,6,7],timingsMs:c.durationsMs,totalMs:730,continuous1xPerception:false,independentQA:false,canonicalMutation:false,unarmedModified:false,newGenerationCalls:0});
const hashes={schemaVersion:1,files:[]};function walk(d){for(const e of fs.readdirSync(d,{withFileTypes:true})){if(e.name==='batch-profile'||e.name==='hashes.json')continue;const p=path.posix.join(d,e.name);if(e.isDirectory())walk(p);else hashes.files.push({path:p,bytes:fs.statSync(p).size,sha256:sha(p)})}}walk(E);walk(S);write(`${E}/hashes.json`,hashes);
console.log(JSON.stringify({state:'CLOSED_REJECTED_NO_MORE_ITERATIONS',artisticStatus:'ARTISTIC_REVISION_REQUIRED',report:`${E}/report.md`,review:`${E}/index.html`,inputFilesPreserved:53,unarmedFilesPreserved:96,hashes:hashes.files.length},null,2));
