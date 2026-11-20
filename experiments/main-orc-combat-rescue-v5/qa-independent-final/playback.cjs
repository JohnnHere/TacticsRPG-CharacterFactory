const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url'),{PNG}=require('pngjs');
const {chromium}=require('C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const out=__dirname;
const manifest=JSON.parse(fs.readFileSync('characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json'));
const review=path.resolve('Biblioteca de Arte/Estudos Comparativos/Orc principal - Resgate de combate');
const same=(a,b)=>{if(a.width!==b.width||a.height!==b.height)return false;for(let i=0;i<a.data.length;i+=4){if(a.data[i+3]!==b.data[i+3])return false;if(a.data[i+3])for(let k=0;k<3;k++)if(a.data[i+k]!==b.data[i+k])return false;}return true;};
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Users/João Orlando/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe',headless:true,args:['--allow-file-access-from-files']});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  await page.goto(pathToFileURL(path.join(review,'index.html')).href);
  await page.waitForFunction(()=>document.body.dataset.ready==='true');
  const staged=await page.evaluate(()=>matrix);
  let comparisons=0;const failures=[];
  for(const c of manifest.cells){const clip=JSON.parse(fs.readFileSync(c.clipJson)),s=staged[c.direction][c.action];
   for(let i=0;i<clip.frames.length;i++){
    if(s.frames[i].durationMs!==clip.frames[i].durationMs||!same(PNG.sync.read(fs.readFileSync(path.join(review,s.frames[i].png))),PNG.sync.read(fs.readFileSync(clip.frames[i].png))))failures.push(c.cellId+'/'+i);
    comparisons++;
   }
  }
  console.log('Exact staged pixel/timing comparisons:',comparisons,'failures:',failures.length);
  const runs=[];
  for(const rate of [1,.75,.5])for(const c of manifest.cells.filter(x=>['Sword','Axe'].includes(x.action))){
   const r=await page.evaluate(async({d,a,rate})=>{
    playing=false;selectedDir=d;selectedAction=a;transitionMode='clip';speed=rate;loop=true;resetPlayback();await renderMain();
    const seq=buildSequence(d,a,transitionMode),captures={},order=[];let prev=-1;
    const length=seq.frames.reduce((s,f)=>s+f.durationMs,0);
    playing=true;
    await new Promise(resolve=>{const start=performance.now();function observe(){const n=mainState.n;if(n!==prev){order.push({n,t:performance.now()-start});prev=n;}if(!captures[n])captures[n]=document.getElementById('main-canvas').toDataURL();if(performance.now()-start>(length+160)/rate){resolve();return;}requestAnimationFrame(observe);}requestAnimationFrame(observe);});
    playing=false;return {d,a,rate,frameCount:seq.frames.length,order,captures};
   },{d:c.direction,a:c.action,rate});
   const grid=new PNG({width:1024,height:Math.ceil(r.frameCount/4)*256});
   for(const [n,data]of Object.entries(r.captures)){const im=PNG.sync.read(Buffer.from(data.split(',')[1],'base64'));PNG.bitblt(im,grid,0,0,256,256,(n%4)*256,Math.floor(n/4)*256);}
   fs.writeFileSync(path.join(out,`${r.d}-${r.a}-playback-${rate}.png`),PNG.sync.write(grid));
   delete r.captures;r.allFramesObserved=new Set(r.order.map(x=>x.n)).size===r.frameCount;r.loopCrossed=r.order.some((x,i)=>i&&x.n<r.order[i-1].n);runs.push(r);
  }
  fs.writeFileSync(path.join(out,'playback-result.json'),JSON.stringify({comparisons,failures,runs},null,2));
  console.log(JSON.stringify({runs:runs.length,allFrames:runs.every(x=>x.allFramesObserved),allLoops:runs.every(x=>x.loopCrossed)}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
