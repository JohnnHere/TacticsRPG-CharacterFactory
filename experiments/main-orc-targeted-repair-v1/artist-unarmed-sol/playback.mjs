import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{chromium}=require('C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const E='experiments/main-orc-targeted-repair-v1/artist-unarmed-sol';
const S='characters/orc-v1/source/targeted-repair-unarmed-sol-v1';
const timings=[80,110,60,90,110];
const data={before:Array.from({length:5},(_,i)=>`before/native/${String(i).padStart(2,'0')}.png`),candidate:Array.from({length:5},(_,i)=>`../../../${S}/native/${String(i).padStart(2,'0')}.png`)};
const html=`<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>back_l / Unarmed — F03 candidata isolada</title><style>body{background:#182229;color:#e0e5e7;font:16px system-ui;margin:22px}h1{font-size:23px}a{color:#9dd8ff}button,select{padding:8px;margin:4px}canvas,img{image-rendering:pixelated}canvas{background:#26323a}.views{display:flex;gap:30px;flex-wrap:wrap}.card{border:1px solid #45515b;padding:12px}.card h2{font-size:18px;margin:2px 0 8px}.small{max-width:950px;font-size:14px;color:#b9c4cc}#film{width:1280px;max-width:100%;height:auto}summary{cursor:pointer}</style>
<h1>back_l / Unarmed — checkpoint F03</h1><p><b>VISUAL_REVIEW_REQUIRED · PENDING_CREATOR</b> · Candidata isolada, sem promoção.</p>
<p class="small">Hipótese: retração com punho visível entre a extensão alta F02 e a recuperação baixa F04. Apenas F03 alterada; cinco quadros/450ms preservados. F03 original não foi amputada na importação: coincide com a baseline. Este player permite inspeção contínua pelo revisor; as provas do agente usam capturas temporais, não percepção contínua de reprodução1×.</p>
<div><button id="play">Reproduzir</button><button id="reset">Início</button><button id="prev">◀ Quadro</button><button id="next">Quadro ▶</button><select id="speed"><option value="1">1× —450ms</option><option value="0.75">0,75×</option><option value="0.5">0,5×</option></select><label><input id="loop" type="checkbox" checked>Repetir para revisão</label></div><p id="info"></p>
<div class="views"><div class="card"><h2>Antes — fonte atual</h2><canvas id="before128" width="128" height="128"></canvas> <canvas id="before64" width="64" height="64"></canvas><p>128px e64px reais</p><canvas id="before384" width="384" height="384"></canvas></div><div class="card"><h2>Depois — somente F03 proposta</h2><canvas id="candidate128" width="128" height="128"></canvas> <canvas id="candidate64" width="64" height="64"></canvas><p>128px e64px reais</p><canvas id="candidate384" width="384" height="384"></canvas></div></div>
<p><a href="F03-before-after-detail.png">Detalhe F03 antes/depois</a> · <a href="before-after-ordered.png">Sequência completa antes/depois</a> · <a href="report.md">Relatório e limitações</a> · <a href="verification.json">Provas técnicas/hashes</a> · <a href="../../../${S}/clip.json">Clip candidato</a></p>
<details><summary>Captura temporal do teste local RAF (não é vídeo)</summary><canvas id="film" width="1280" height="310"></canvas></details>
<script>
const files=${JSON.stringify(data)},times=${JSON.stringify(timings)},images={before:[],candidate:[]};let frame=3,playing=false,speed=1,stamp=0,run=null;
function draw(){for(const kind of ['before','candidate'])for(const size of [128,64,384]){const c=document.getElementById(kind+size),ctx=c.getContext('2d');ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,size,size);ctx.drawImage(images[kind][frame],0,0,size,size)}document.getElementById('info').textContent='F'+String(frame).padStart(2,'0')+' / F04 · '+times[frame]+'ms · '+(frame===3?'F03 alterada na candidata':'RGBA idêntico nos dois lados')+' · '+speed+'×'}
function step(d){playing=false;frame=(frame+d+5)%5;draw();document.getElementById('play').textContent='Reproduzir'}
document.getElementById('prev').onclick=()=>step(-1);document.getElementById('next').onclick=()=>step(1);document.getElementById('reset').onclick=()=>{frame=0;stamp=performance.now();draw()};document.getElementById('play').onclick=()=>{playing=!playing;stamp=performance.now();document.getElementById('play').textContent=playing?'Pausar':'Reproduzir'};document.getElementById('speed').onchange=e=>{speed=Number(e.target.value);stamp=performance.now()};document.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')step(-1);if(e.key==='ArrowRight')step(1)});
function capture(t){if(!run||run.stopped||frame===run.last)return;run.samples.push({frame,elapsedMs:Math.round(t-run.start)});if(!run.seen.includes(frame)){run.seen.push(frame);const ctx=document.getElementById('film').getContext('2d');ctx.imageSmoothingEnabled=false;for(const [j,k]of ['before','candidate'].entries()){ctx.drawImage(document.getElementById(k+'128'),frame*256,j*150,128,128);ctx.drawImage(document.getElementById(k+'64'),frame*256+145,j*150,64,64);ctx.fillStyle='#eee';ctx.font='12px monospace';ctx.fillText(k+' F'+frame+' '+Math.round(t-run.start)+'ms',frame*256+3,j*150+145)}}run.last=frame}
function tick(t){if(playing){while(t-stamp>=times[frame]/speed){stamp+=times[frame]/speed;if(frame===4&&!document.getElementById('loop').checked){playing=false;break}frame=(frame+1)%5}draw();capture(t)}requestAnimationFrame(tick)}
window.startRun=s=>{speed=s;frame=0;stamp=performance.now();playing=true;document.getElementById('speed').value=String(s);document.getElementById('loop').checked=true;document.getElementById('film').getContext('2d').clearRect(0,0,1280,310);run={speed:s,start:performance.now(),seen:[],samples:[],last:-1};draw()};window.stopRun=()=>{run.stopped=true;playing=false;return {...run}};
Promise.all(Object.entries(files).flatMap(([key,ps])=>ps.map((p,i)=>new Promise((yes,no)=>{const im=new Image();im.onload=()=>{images[key][i]=im;yes()};im.onerror=no;im.src=p})))).then(()=>{document.body.dataset.ready='true';draw();requestAnimationFrame(tick)});
</script></html>`;
fs.writeFileSync(`${E}/index.html`,html);
const result={status:'PASS',scope:'Local ART before/after RAF capture, not independent QA',continuous1xPerceptionClaimed:false,runs:[],failures:[]};
fs.mkdirSync(`${E}/playback`,{recursive:true});
const browser=await chromium.launch({executablePath:'C:/Users/João Orlando/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe',headless:true,args:['--allow-file-access-from-files']});
try{
 const p=await browser.newPage({viewport:{width:1600,height:1200}});p.on('pageerror',e=>result.failures.push(e.message));p.on('requestfailed',r=>result.failures.push(r.url()));
 await p.goto(pathToFileURL(path.resolve(`${E}/index.html`)).href);await p.waitForSelector('body[data-ready="true"]');
 await p.screenshot({path:`${E}/F03-at-128-and-64.png`});
 await p.locator('summary').click();
 for(const speed of [1,0.75,0.5]){
  await p.evaluate(s=>window.startRun(s),speed);await p.waitForTimeout(Math.ceil(450*3.1/speed)+80);
  const r=await p.evaluate(()=>window.stopRun());r.all5Frames=r.seen.length===5;r.loopBoundary=r.samples.some((s,i)=>i&&s.frame<r.samples[i-1].frame);if(!r.all5Frames||!r.loopBoundary)result.failures.push(`Playback ${speed}`);result.runs.push(r);
  await p.locator('#film').screenshot({path:`${E}/playback/paired-${speed}.png`});
 }
 await p.close();
}catch(e){result.failures.push(e.stack??String(e))}finally{await browser.close()}
result.status=result.failures.length?'FAIL':'PASS';fs.writeFileSync(`${E}/playback.json`,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));if(result.failures.length)process.exitCode=1;
