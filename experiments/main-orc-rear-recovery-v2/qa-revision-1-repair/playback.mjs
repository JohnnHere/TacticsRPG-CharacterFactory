import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require('C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const O='experiments/main-orc-rear-recovery-v2/qa-revision-1-repair';
const definitions=[['SwordL','back_l','Sword'],['AxeR','back_r','Axe'],['AxeL','back_l','Axe']];
const clips=definitions.map(([key,d,a])=>({key,...JSON.parse(fs.readFileSync(`characters/orc-v1/source/rear-recovery-v2/${d}/${a}/Attack-representative-v1/clip.json`))}));
const html=`<!doctype html><meta charset="utf-8"><title>ART local repaired sources — VISUAL_REVIEW_REQUIRED</title><style>body{background:#1e282f;color:#eee;font:14px monospace}canvas{image-rendering:pixelated;background:#303b44}#film{display:block;margin-top:16px}button,select{padding:6px}a{color:#9de}</style><h1>ART local check — VISUAL_REVIEW_REQUIRED / PENDING_CREATOR</h1><p>Three repaired saved-master exports. Review loop only; runtime remains oneShot. Full256, native128 BODY, full composite half-scale (body approximately64).</p><select id="clip"></select><select id="speed"><option>1</option><option>0.75</option><option>0.5</option></select><button id="reset">Reset</button><button id="play">Pause</button><div id="info"></div><canvas id="full" width="256" height="256"></canvas><canvas id="body" width="128" height="128"></canvas><canvas id="game" width="128" height="128"></canvas><canvas id="film" width="2048" height="290"></canvas><script>
const clips=${JSON.stringify(clips)};const images=new Map();let clip=clips[0],speed=1,frame=0,playing=true,stamp=0,run=null;
const sel=document.querySelector('#clip');for(const c of clips){const op=document.createElement('option');op.value=c.key;op.textContent=c.key;sel.append(op)}
function reset(){frame=0;stamp=performance.now();draw()}
function draw(){const f=clip.frames[frame];for(const [id,p]of [['full',f.png],['body',f.nativePng],['game',f.png]]){const can=document.getElementById(id),ctx=can.getContext('2d');ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,can.width,can.height);ctx.drawImage(images.get(p),0,0,can.width,can.height)}document.querySelector('#info').textContent=clip.key+' F'+frame+' / 7 @'+speed+' — 730ms; weapon frames01..06'}
sel.onchange=()=>{clip=clips.find(c=>c.key===sel.value);reset()};document.querySelector('#speed').onchange=e=>{speed=Number(e.target.value);reset()};document.querySelector('#reset').onclick=reset;document.querySelector('#play').onclick=()=>{playing=!playing;stamp=performance.now()};
function observe(t){if(!run||run.stopped||run.last===frame)return;run.samples.push({frame,elapsedMs:Math.round(t-run.start)});if(!run.seen.includes(frame)){run.seen.push(frame);const ctx=document.querySelector('#film').getContext('2d');ctx.imageSmoothingEnabled=false;ctx.drawImage(document.querySelector('#full'),frame*256,0);ctx.fillStyle='#fff';ctx.font='14px monospace';ctx.fillText('F'+frame+' '+Math.round(t-run.start)+'ms',frame*256+5,280)}run.last=frame}
function tick(t){if(playing){while(t-stamp>=clip.frames[frame].durationMs/speed){stamp+=clip.frames[frame].durationMs/speed;frame=(frame+1)%8}draw();observe(t)}requestAnimationFrame(tick)}
window.startRun=(key,s)=>{clip=clips.find(c=>c.key===key);sel.value=key;speed=s;document.querySelector('#speed').value=String(s);document.querySelector('#film').getContext('2d').clearRect(0,0,2048,290);reset();playing=true;run={key,speed:s,start:performance.now(),last:-1,seen:[],samples:[]};};
window.stopRun=()=>{run.stopped=true;playing=false;return {...run}};
Promise.all([...new Set(clips.flatMap(c=>c.frames.flatMap(f=>[f.png,f.nativePng])))].map(p=>new Promise((ok,no)=>{const im=new Image();im.onload=()=>{images.set(p,im);ok()};im.onerror=no;im.src='../../../'+p}))).then(()=>{document.body.dataset.ready='true';reset();requestAnimationFrame(tick)});
</script>`;
fs.writeFileSync(`${O}/review.html`,html);
const result={role:'Sole ART local verification; not independent QA',status:'PASS',source:'canonical saved-master exports',runs:[],failures:[]};
fs.mkdirSync(`${O}/playback`,{recursive:true});
const browser=await chromium.launch({executablePath:'C:/Users/João Orlando/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe',headless:true,args:['--allow-file-access-from-files']});
try{
 const page=await browser.newPage({viewport:{width:2100,height:800}});
 page.on('pageerror',e=>result.failures.push(e.message));page.on('requestfailed',r=>result.failures.push(r.url()));
 await page.goto(pathToFileURL(path.resolve(`${O}/review.html`)).href);await page.waitForSelector('body[data-ready="true"]');
 for(const c of clips)for(const speed of [1,0.75,0.5]){
  await page.evaluate(({key,speed})=>window.startRun(key,speed),{key:c.key,speed});
  await page.waitForTimeout(Math.ceil(730*2.2/speed)+120);
  const r=await page.evaluate(()=>window.stopRun());
  r.all8FramesObserved=r.seen.length===8;r.loopBoundaryObserved=r.samples.some((v,i)=>i&&v.frame<r.samples[i-1].frame);
  if(!r.all8FramesObserved||!r.loopBoundaryObserved)result.failures.push(`${c.key}@${speed}: playback coverage`);
  await page.screenshot({path:`${O}/playback/${c.key}-${speed}.png`});result.runs.push(r);console.log(`ART actual RAF playback ${c.key}@${speed}:8frames=${r.all8FramesObserved} loop=${r.loopBoundaryObserved}`);
 }
 await page.close();
}catch(e){result.failures.push(e.stack??String(e))}finally{await browser.close()}
result.status=result.failures.length?'FAIL':'PASS';
fs.writeFileSync(`${O}/playback-verification.json`,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:result.status,runs:result.runs.length,failures:result.failures}));if(result.failures.length)process.exitCode=1;
