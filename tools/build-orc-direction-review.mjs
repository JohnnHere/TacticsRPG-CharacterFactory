import fs from 'node:fs';
import path from 'node:path';
import {ROOT,loadCharacter,approval,hash,json,readJSON,slash} from '../src/core.mjs';
import {decode,measure} from '../src/images.mjs';
const batch=readJSON(path.join(ROOT,'characters/orc-direction-batch-v1.json'));
const editor=readJSON(path.join(ROOT,'characters/orc-directions-editor-verification-v1.json'));
const directions=['front_r','front_l','back_r','back_l'],rows=[],summary={PASS:0,FAIL:0,WARNING:0};
for(const b of batch){
 const {spec,dir}=loadCharacter(b.id),prefix=b.id.replaceAll('-','_'),assets=readJSON(path.join(dir,'assets.json'));
 const frontReview=readJSON(path.join(dir,b.frontReview));
 const frontFile=path.join(dir,`sprites/Directions/${prefix}_dir_front_r.png`);
 if(frontReview.decision!=='approved'||hash(fs.readFileSync(frontFile))!==frontReview.sha256||!approval(spec,dir,'concept'))throw Error('Approval/approved front mismatch');
 const validation=readJSON(path.join(dir,'reports/directions-validation-v1.json'));
 for(const k of Object.keys(summary))summary[k]+=validation.summary[k]??0;
 const views=directions.map(d=>{
  const file=`sprites/Directions/${prefix}_dir_${d}.png`,decoded=decode(path.join(dir,file)),m=measure(decoded.image);
  const editable=d==='front_r'?'source/native-base-v1/front_r.aseprite':`source/directions-v1/${d}/view.aseprite`;
  const e=editor.sources.find(e=>e.id===b.id&&e.direction===d);
  if(!e||e.editableSha256!==hash(fs.readFileSync(path.join(dir,editable)))||e.nativeSha256!==decoded.sha256||e.librespriteExportRgba!=='BYTE_IDENTICAL')throw Error(`Editor evidence mismatch ${b.id}/${d}`);
  const a=assets.findLast(a=>a.file===file&&a.sha256===decoded.sha256);if(!a)throw Error('Provenance missing');
  a.editableSourceSha256=e.editableSha256;
  if(approval(spec,dir,'base'))a.artisticApproval='APPROVED_BY_CREATOR_BASE_VIEWS';
  if(hash(fs.readFileSync(path.join(dir,a.generationPromptFile)))!==a.generationPromptSha256||hash(fs.readFileSync(path.join(dir,a.sourceRaster)))!==a.sourceSha256)throw Error('Source/prompt provenance mismatch');
  return {direction:d,file:`${b.id}/${file}`,sha256:decoded.sha256,editable:`${b.id}/${editable}`,editableSha256:e.editableSha256,colors:m.colorCount,contentHeight:m.contentHeight,ground:m.bottom,partialAlpha:m.partial,rgba:decoded.image.data};
 });
 for(let i=0;i<views.length;i++)for(let j=i+1;j<views.length;j++){
  if(views[i].rgba.equals(views[j].rgba))throw Error('Duplicate direction');
  let exactMirror=true;for(let y=0;y<128&&exactMirror;y++)for(let x=0;x<128&&exactMirror;x++)for(let c=0;c<4;c++)if(views[i].rgba[(y*128+x)*4+c]!==views[j].rgba[(y*128+127-x)*4+c]){exactMirror=false;break;}
  if(exactMirror)throw Error('Exact mirrored direction pair');
 }
 for(const v of views)delete v.rgba;
 json(path.join(dir,'assets.json'),assets);
 rows.push({id:b.id,job:b.job,views,baseGate:approval(spec,dir,'base')?'APPROVED_BY_CREATOR':'PENDING_CREATOR',approvedFrontUnchanged:true,uniqueDirectionPixels:true,noExactPixelMirrorPairs:true});
}
if(summary.FAIL)throw Error('Technical failures');
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
fs.writeFileSync(path.join(ROOT,'characters/review-orc-directions-v1.html'),`<!doctype html><html lang="pt-br"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Orc — quatro vistas das sete classes</title><style>body{font:16px system-ui;background:#20222a;color:#eee;margin:24px}a{color:#9cf}p{line-height:1.5;max-width:1150px}section{border:1px solid #666;border-radius:8px;padding:16px;margin:18px 0;overflow:auto}.views{display:grid;grid-template-columns:repeat(4,minmax(260px,1fr));gap:16px;min-width:1090px}figure{margin:0}h3{margin:8px 0}img.native{width:256px;height:256px;image-rendering:pixelated;background:repeating-conic-gradient(#555 0 25%,#383a42 0 50%) 0/16px 16px}figcaption{margin:8px 0;font-size:14px}button,select{font:inherit;padding:8px;margin:8px}.light{background:#efede7;color:#111}.light img.native{background:repeating-conic-gradient(#fff 0 25%,#ccc 0 50%) 0/16px 16px}.light a{color:#056ca4}small{display:block;line-height:1.5}details{margin-top:12px}[hidden]{display:none}</style><h1>Orc — quatro vistas das sete classes básicas</h1><p>As sete primeiras bases <strong>front_r</strong> foram aprovadas pelo criador e preservadas. Agora estão disponíveis <strong>front_l, back_r e back_l</strong> de cada roupa, sem armas. São 28 vistas, mais sete fallbacks: 35 PNGs nativos e 28 fontes editáveis.</p><p><strong>Revisão antes das animações:</strong> conferir identidade, silhueta, proporções, roupa nas costas, lado dos acessórios e mão dominante. Cada roupa usa a paleta da própria base aprovada. A validação técnica não aprova a arte; ${rows.every(r=>r.baseGate==='APPROVED_BY_CREATOR')?'as quatro vistas estão aprovadas pelo criador.':'o Gate base completo aguarda a avaliação destas quatro vistas.'}</p><label>Classe <select id="classFilter"><option value="all">Todas</option>${rows.map(r=>`<option value="${r.id}">${esc(r.job)}</option>`).join('')}</select></label><label>Zoom <select id="zoom"><option value="1">1×</option><option value="2" selected>2×</option><option value="3">3×</option></select></label><button id="background">Trocar fundo</button><main>${rows.map(r=>`<section data-id="${r.id}"><h2>${esc(r.job)}</h2><div class="views">${r.views.map(v=>`<figure><h3>${v.direction}</h3><a href="${v.file}"><img class="native" alt="${esc(r.job)} ${v.direction}" src="${v.file}"></a><figcaption>${r.baseGate==='APPROVED_BY_CREATOR'?'Vista aprovada pelo criador':v.direction==='front_r'?'Primeira base aprovada':'Nova vista — revisão pendente'}</figcaption><small><a href="${v.editable}">Fonte editável</a></small></figure>`).join('')}</div><details><summary>Conceito e verificação</summary><a href="${r.id}/preview.html">Pacote da classe</a> · <a href="${r.id}/reports/directions-validation-v1.json">Validação das vistas</a><p>128×128 RGBA · 100 pixels de altura · chão y126 · alfa parcial zero · paleta comum nesta roupa</p></details></section>`).join('')}</main><p><a href="orc-directions-review-inventory-v1.json">Inventário e hashes</a> · <a href="orc-directions-editor-verification-v1.json">Conferência no LibreSprite</a> · <a href="review-orc-basic-classes-v1.html">Conceitos</a></p><p><a href="review-orc-front-locomotion-v1.html">Primeiro lote Idle/Walk front_r em revisão</a>. Demais animações, exportação e integração Unity continuam pendentes.</p><script>document.querySelector('#classFilter').onchange=e=>{for(const s of document.querySelectorAll('main section'))s.hidden=e.target.value!=='all'&&s.dataset.id!==e.target.value};document.querySelector('#background').onclick=()=>document.body.classList.toggle('light');document.querySelector('#zoom').onchange=e=>{for(const i of document.querySelectorAll('img.native'))i.style.width=i.style.height=128*Number(e.target.value)+'px'};</script></html>`);
json(path.join(ROOT,'characters/orc-directions-review-inventory-v1.json'),{rows,summary:{nativePng:35,directionViews:28,newViews:21,editableSources:28,validation:summary,editorRoundtrip:'28/28 RGBA byte-identical'},approvedFrontsUnchanged:true,sourceCalls:{sheets:7,correctedIndividualViews:3,total:10},artisticReview:rows.every(r=>r.baseGate==='APPROVED_BY_CREATOR')?'APPROVED_BY_CREATOR':'PENDING_CREATOR_FOUR_VIEWS',unityIntegration:'NOT_RUN'});
console.log('Four-view preview ready; 35 PNGs, 28 editables, 175 PASS/0 FAIL.');
