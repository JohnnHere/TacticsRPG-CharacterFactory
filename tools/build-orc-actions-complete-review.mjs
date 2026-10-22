import fs from 'node:fs';
import path from 'node:path';
import {ROOT,readJSON,json} from '../src/core.mjs';
const read=f=>readJSON(path.join(ROOT,f));
const legacy=read('characters/orc-basic-complete-validation-v1.json'),unarmed=read('characters/orc-unarmed-complete-validation-v1.json'),warrior=read('characters/orc-basic-shared-source-index.json');
const counts={Idle:4,Walk:6,Attack:5,Unarmed:5,Hit:3,Defeat:5},durations={Idle:240,Walk:73,Attack:90,Unarmed:90,Hit:80,Defeat:120};
const labels={'orc-01':'Soco físico original','orc-01-squire':'Golpe corpo a corpo','orc-01-archer':'Preparar e soltar disparo','orc-01-apprentice-mage':'Conjuração ofensiva','orc-01-acolyte':'Invocação de suporte','orc-01-rogue':'Estocada rápida','orc-01-scout':'Arremesso rápido','orc-01-brawler':'Soco de direita'};
const url=f=>f.replace(/^characters\//,''),esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
const classes=unarmed.classes.map(c=>{
 const clips={};
 if(c.id==='orc-01')for(const e of warrior.editables){const {state,direction}=e;clips[state+'_'+direction]={durationMs:durations[state],frames:Array.from({length:counts[state]},(_,i)=>`orc-01/sprites/Animations/${state}/${state.toLowerCase()}_${direction}_${String(i).padStart(2,'0')}.png`),strip:url(path.posix.dirname(e.file)+'/native-strip.png'),editable:url(e.file)};}
 else for(const r of legacy.clips.filter(r=>r.id===c.id))clips[r.state+'_'+r.direction]={durationMs:r.durationMs,frames:r.frameFiles.map(f=>`${c.id}/${f.file}`),strip:`${c.id}/${path.posix.dirname(r.sourceRow)}/native-strip.png`,editable:`${c.id}/${r.editable}`};
 for(const r of unarmed.clips.filter(r=>r.id===c.id))clips['Unarmed_'+r.direction]={durationMs:90,frames:r.frames.map(f=>url(f.file)),strip:url(r.strip),editable:url(r.editable)};
 for(const [key,clip]of Object.entries(clips))for(const f of [...clip.frames,clip.strip,clip.editable])if(!fs.existsSync(path.join(ROOT,'characters',f)))throw Error('Missing preview asset '+key+' '+f);
 if(Object.keys(clips).length!==24)throw Error('Incomplete preview');
 return {id:c.id,job:c.job,label:labels[c.id],base:`${c.id}/sprites/Directions/${c.id.replaceAll('-','_')}_dir_front_l.png`,clips};
});
const data={classes,counts,durations};
// Reuse the previously exercised viewer controls; retain the historical review as evidence.
let html=fs.readFileSync(path.join(ROOT,'characters/review-orc-basic-complete-v1.html'),'utf8');
html=html.replace(/<title>.*?<\/title>/,'<title>Orc — revisão final de corpo e ataques desarmados</title>');
html=html.replace(/<h1>.*?<nav>/s,`<h1>Orc — revisão final das animações</h1><p><strong>Sete variantes completas e ataque básico desarmado nas quatro vistas.</strong> Warrior aparece como referência aprovada. Este lote acrescenta 90 PNGs e 18 fontes editáveis; os ataques desarmados somam 160 referências de quadro em 32 clipes: 120 PNGs novos e 40 reutilizados de Warrior/Brawler. As animações anteriores e o primeiro lote desarmado aprovado foram preservados.</p><p>Compare os socos em <strong>Ataque básico sem arma</strong> com os gestos de cada classe em <strong>Gesto do Job</strong>. Revise as quatro vistas, o braço direito, o capuz do Rogue, o retorno à guarda e a consistência entre animações. Armas, projéteis, efeitos, encaixes e seleção de ações no jogo continuam pendentes; esta prévia mostra corpo e roupa.</p><nav>`);
html=html.replace(/<select id="state">.*?<\/select>/,'<select id="state"><option value="Idle">Idle</option><option value="Walk">Walk</option><option value="Attack">Gesto do Job (legado)</option><option value="Unarmed" selected>Ataque básico sem arma</option><option value="Hit">Hit</option><option value="Defeat">Defeat</option></select>');
html=html.replace(/<select id="classFilter">.*?<\/select>/,`<select id="classFilter"><option value="all">Todas</option>${classes.map(c=>`<option value="${c.id}">${esc(c.job)}</option>`).join('')}</select>`);
html=html.replace(/<main>.*?<\/main>/s,`<main>${classes.map(c=>`<article data-id="${c.id}"><h2>${esc(c.job)}</h2><p class="action">Ataque básico desarmado — soco físico</p><canvas width="128" height="128" id="canvas-${c.id}" aria-label="${esc(c.job)} animação"></canvas><p>${c.id==='orc-01'?'Warrior aprovado — referência de reuso':'Consistência final pendente'}</p><details><summary>Base aprovada e fontes do clipe</summary><img class="base" src="${c.base}" alt="Base aprovada ${esc(c.job)}"><p><a class="editable" href="${c.clips.Unarmed_front_l.editable}">Fonte editável do clipe</a></p><img class="strip" src="${c.clips.Unarmed_front_l.strip}" alt="Quadros ${esc(c.job)}"></details></article>`).join('')}</main>`);
html=html.replace(/<\/main>.*?<script>/s,'</main><p><a href="orc-unarmed-complete-validation-v1.json">Inventário desarmado e hashes</a> · <a href="orc-basic-complete-validation-v1.json">Animações anteriores</a> · <a href="../docs/EQUIPMENT_AND_ACTIONS.md">Contrato de equipamentos e ações</a></p><p>A repetição facilita a revisão; ataques, impacto e derrota são ações únicas. Gate 2 de consistência final aguarda o criador antes da exportação local. Integração Unity é uma etapa separada.</p><script>');
html=html.replace(/const data=.*?,images=new Map;/,`const data=${JSON.stringify(data)},images=new Map;`);
html=html.replace("let current='Attack'","let current='Unarmed'");
html=html.replace("current==='Attack'?c.label:","current==='Unarmed'?'Ataque básico desarmado — soco físico':current==='Attack'?c.label:");
if(!html.includes("current==='Unarmed'?"))throw Error('Viewer template changed');
if(unarmed.artisticConsistency==='APPROVED_BY_CREATOR')html=html.replaceAll('Consistência final pendente','Conjunto aprovado pelo criador').replace('Gate 2 de consistência final aguarda o criador antes da exportação local.','Gate 2 registrado; pacotes exportados localmente. <a href="../reports/orc-actions-export-v1.json">Inventário da exportação</a>.');
fs.writeFileSync(path.join(ROOT,'characters/review-orc-actions-complete-v1.html'),html);
json(path.join(ROOT,'characters/orc-actions-complete-preview-data-v1.json'),data);
console.log('Combined review:8 appearances,6 states,4 directions,192 clip references,896 animation frame references (856 unique).');
