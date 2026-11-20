import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const E='experiments/main-orc-targeted-repair-v1/artist-unarmed-sol',S='characters/orc-v1/source/targeted-repair-unarmed-sol-v1';
const read=p=>JSON.parse(fs.readFileSync(p)),write=(p,x)=>fs.writeFileSync(p,JSON.stringify(x,null,2)+'\n');
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const c=read(`${S}/clip.json`),v=read(`${E}/verification.json`),b=read(`${E}/before-inventory.json`),play=read(`${E}/playback.json`);
if(v.status!=='PASS'||play.status!=='PASS')throw Error('Technical checkpoint verification failed');
for(const r of b.files)if(sha(r.source)!==r.sha256||sha(r.backup)!==r.sha256)throw Error(`Original input changed: ${r.source}`);
const report=`# back_l / Unarmed — checkpoint cirúrgico F03

**TECHNICALLY_COMPLETE para o pacote isolado. VISUAL_REVIEW_REQUIRED. PENDING_CREATOR.** Não integrado, sem QA independente, sem aprovação artística. Trabalho encerrado neste checkpoint; não propagado.

[Abrir comparação antes/depois](index.html) — funciona por file://, sem servidor. Reprodução sincronizada em1×/0,75×/0,5×, pausa, quadro anterior/próximo e apresentações128/64px reais. [F03 antes/depois](F03-before-after-detail.png) · [cinco poses ordenadas](before-after-ordered.png) · [captura em128/64px](F03-at-128-and-64.png).

## Diagnóstico confirmado e hipótese

As seções10–13 do pedido original foram lidas. Esta responsabilidade permaneceu exclusivamente em back_l/Unarmed; front, back_r, Walk, Sword e Axe não foram modificados.

Os cinco quadros atuais têm RGBA distintos, referências distintas e tempos80/110/60/90/110ms, total450ms. Não foi encontrada duplicação exata. Repetições aproximadas não foram usadas como diagnóstico automático. F03 composto é byte-idêntico à baseline complete-v1/back_l/Unarmed/03.png; os cinco PNGs nativos são crops centrais exatos do composto. Os20 renders frescos de fontes anteriores/candidatas também coincidem com seus exports. **Amputação na importação não está comprovada.**

O salto de leitura está entre a extensão alta F02, a pose recolhida pouco legível F03 e a recuperação baixa F04. A camada é achatada; não há decomposição anatômica original que prove qual parte está oculta. A proposta é uma **interpretação nova de retração**, não recuperação demonstrada de pixels perdidos: manter o ombro/torso de F03 e mostrar o punho recolhendo para a esquerda, antes de baixar em F04.

## Pose candidata e delimitação

**Somente F03 alterada:465 posições RGBA visíveis no nativo e as mesmas465 posições no composto.** Caixa dos deltas nativos: x30..57,y44..79; registro composto correspondente:(+64,+64), x94..121,y108..143. **F00/F01/F02/F04 têm zero pixels RGBA alterados.** Esses quatro quadros compostos também mantiveram os bytes do PNG; os derivados nativos usam nova codificação Aseprite, com pixels idênticos. Os13 arquivos originais de entrada (masters, clip e PNGs) permanecem byte-idênticos.

A manopla/antebraço usa apenas um contorno recortado de F02 do mesmo indivíduo, mesma vista e mesmo clipe, transladado(+24,+25) dentro do Aseprite. Não houve interpolação, espelhamento ou deformação do corpo. Pequenos clusters locais de tinta/couro refazem a costura do cotovelo. O ombro/placa permanece no lugar; o braço superior vem da manga própria de F03, e o antebraço dobra para o punho visível à esquerda. Cabeça, costas, cintura central, pernas, braço oposto e demais poses não foram redesenhados.

**Correção do primeiro rascunho:** a máscara inicial deixou a borda da manga antiga sob o cotovelo. A inspeção por coordenadas comprovou que x46,y66..71 conservava os mesmos pixels metálicos do original (RGB153/154/155 e171/173/173), com couro antigo ligado abaixo. Isso era material legítimo na pose antiga, transformado em resíduo pela minha substituição incompleta — não um defeito de exportação. O contorno antigo foi traçado até a junção com a placa do quadril e substituído antes do novo antebraço; a placa à direita foi preservada. Aquelas seis posições agora têm alpha0. [Traçado do rascunho](F03-elbow-source-coordinate-trace.png) e [pixels examinados](elbow-bright-pixels.json) registram a falha; são evidência do rascunho rejeitado, não da candidata atual. O rascunho e seu Lua estão preservados em rejected/attempt-01/.

Na inspeção estática do corpo inteiro, a manopla candidata fica ligada à região do cotovelo e à manga sob a ombreira. Em64px, permanece uma projeção de punho/antebraço à esquerda; o detalhamento de aço/couro perde resolução. Isso sustenta apresentar a pose para revisão, mas **não demonstra que o movimento de450ms ficou satisfatório**. A orientação do corpo e os saltos entre as outras poses foram preservados e ainda podem limitar o resultado. Não proponho corrigir isso por thresholds ou contagens espaciais.

## Fontes, registro e autoria

- [Clip isolado completo](../../../${S}/clip.json): cinco frames, referências e SHA-256 reais de PNGs/masters, tempos, canvas/ground, pai, procedência e status.
- [Master nativo](../../../${c.nativeMaster}):128×128, cinco cels, apenas F03 substituída.
- [Master composto](../../../${c.master}):256×256; F03 contém imagem128×128 em cel.position(64,64). Os outros cels conservam suas imagens256×256 em(0,0).
- [Lua autoral](author_f03.lua): renderiza a imagem de origem aplicando cel.position explicitamente, usa coordenadas nativas e reabre os forks salvos antes de exportar.
- [Wrapper](aseprite.mjs): Aseprite1.3.18.6, oculto --batch --noinapp com perfil exclusivo em artist-unarmed-sol/batch-profile/. Não carrega o perfil GUI nem compartilha o perfil de outro ART.
- [Metadados de fonte/cel](source-proof/document.json), [inventário anterior](before-inventory.json), [provas técnicas](verification.json), [hashes](hashes.json).

Hash do master nativo: ${c.nativeMasterSha256}.

Hash do master composto: ${c.masterSha256}.

Hash F03 nativo: ${c.frames[3].nativeSha256}.

Hash F03 composto: ${c.frames[3].sha256}.

Toda alteração raster de produção ocorreu em Lua dentro do Aseprite. Python apenas copiou/validou arquivos e montou pranchas diagnósticas. O script rejeitado artist-unarmed/restore_backl_unarmed_f03.lua foi lido para entender a falha e **nunca executado**.

## Verificação e limites de reprodução

- 20/20 comparações frescas de render Aseprite: fontes anteriores/candidatas × nativo/composto × cinco quadros. Durações e posições reais dos cels registradas.
- Cinco crops centrais candidatos128→256 exatos, com o deslocamento(+64,+64); nenhuma inferência baseada na largura crua do cel.
- Zero alterações em F00/F01/F02/F04;465 em F03. Nenhuma alteração nos13 arquivos originais protegidos.
- [Player local](index.html) testado em Chromium headless por file://, sem requisições falhas ou erros JS. Três execuções RAF sincronizadas(1/0,75/0,5) observaram todos os cinco quadros e a passagem de loop. [Transições capturadas](playback.json), [1×](playback/paired-1.png), [0,75×](playback/paired-0.75.png), [0,5×](playback/paired-0.5.png).

**Não percebi reprodução contínua1× em uma sessão visual ao vivo.** Inspecionei capturas estáticas e amostras temporais completas do player RAF. A existência de playback automatizado não é aprovação de movimento. Não reivindico QA independente, aprovação visual, teste Unity ou escala real da câmera do jogo;64px é apresentação diagnóstica aproximada. O checkbox de loop serve à revisão e não muda o contrato oneShot do candidato.

## Reprodução local e handoff

Executar na raiz do repositório:

    node experiments/main-orc-targeted-repair-v1/artist-unarmed-sol/aseprite.mjs --script experiments/main-orc-targeted-repair-v1/artist-unarmed-sol/author_f03.lua
    node experiments/main-orc-targeted-repair-v1/artist-unarmed-sol/aseprite.mjs --script experiments/main-orc-targeted-repair-v1/artist-unarmed-sol/export_proof.lua
    node experiments/main-orc-targeted-repair-v1/artist-unarmed-sol/package.mjs
    node experiments/main-orc-targeted-repair-v1/artist-unarmed-sol/playback.mjs

O Lua lê os snapshots byte-verificados em before/, não o candidato que ele mesmo escreveu; pode reproduzir a pose sem reempilhar doadores. Para atualizar pranchas externas, usar tmp/pixel-venv/Scripts/python.exe com compare.py. O inventário de hashes exclui o perfil batch temporário e a si mesmo.

Todas as escritas desta tarefa ficaram nos dois diretórios exclusivos autorizados. Nenhum manifesto/página canônica, baseline, fonte de outro DEV, documentação compartilhada ou célula adicional foi alterado. Sem agentes, QA adicional, geração paga, Unity ou commit. A mudança apresentada é um checkpoint de **uma pose**, não a entrega de correção aprovada do clipe completo. A avaliação independente após eventual integração pertence ao fluxo já definido pelo Root.

**TECHNICALLY_COMPLETE / VISUAL_REVIEW_REQUIRED / PENDING_CREATOR. Checkpoint encerrado; sem propagação.**
`;
fs.writeFileSync(`${E}/report.md`,report);
write(`${E}/checkpoint.json`,{status:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',creatorApproval:'PENDING_CREATOR',scope:'back_l/Unarmed,F03 representative pose only',state:'CHECKPOINT_RETURNED_NO_PROPAGATION',review:`${E}/index.html`,report:`${E}/report.md`,isolatedClip:`${S}/clip.json`,changedFrames:[3],preservedFrames:[0,1,2,4],changedVisibleRgbaPixels:{native:465,composite:465},timingsMs:c.durationsMs,totalMs:450,freshSavedSourceComparisons:20,productionSourcesUnchanged:13,continuous1xPerception:false,independentQAClaimed:false,canonicalMutation:false,paidGenerationCalls:0});
const hashes={schemaVersion:1,files:[]};
function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){if(e.name==='batch-profile'||e.name==='hashes.json')continue;const p=path.posix.join(dir,e.name);if(e.isDirectory())walk(p);else hashes.files.push({path:p,bytes:fs.statSync(p).size,sha256:sha(p)})}}
walk(E);walk(S);write(`${E}/hashes.json`,hashes);
console.log(JSON.stringify({status:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',checkpoint:`${E}/index.html`,report:`${E}/report.md`,clip:`${S}/clip.json`,hashEntries:hashes.files.length,changedPixels:465,preservedFrames:[0,1,2,4]},null,2));
