const fs=require('fs'),path=require('path'),{spawn}=require('child_process'),{pathToFileURL}=require('url');
const out=path.resolve(__dirname),target=process.argv[2],label=process.argv[3]||'body-cycle';
const isGrip=label.includes('front-r-sword');
if(!target)throw Error('Expected exact local review HTML');
const profile=path.join(out,'chromium-profile');
const proc=spawn('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',['--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'],{windowsHide:true,stdio:['ignore','ignore','pipe']});
let stderr='';proc.stderr.on('data',b=>stderr+=b.toString());
const delay=ms=>new Promise(r=>setTimeout(r,ms));
let ws,seq=0;const pending=new Map();
async function call(method,params={}){const id=++seq;return new Promise((resolve,reject)=>{pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));setTimeout(()=>{if(pending.has(id)){pending.delete(id);reject(Error('CDP timeout '+method));}},10000).unref();});}
async function evaluate(expression){const r=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;}
(async()=>{try{
 let port;for(let i=0;i<100;i++){const m=stderr.match(/DevTools listening on ws:\/\/127\.0\.0\.1:(\d+)/);if(m){port=m[1];break;}await delay(100);}if(!port)throw Error('Edge debug endpoint unavailable: '+stderr.slice(-1000));
 const tabs=await(await fetch('http://127.0.0.1:'+port+'/json/list')).json();const page=tabs.find(t=>t.type==='page');
 ws=new WebSocket(page.webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j;});ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result);}};
 await call('Page.enable');await call('Runtime.enable');await call('Emulation.setDeviceMetricsOverride',{width:1280,height:960,deviceScaleFactor:1,mobile:false});
 await call('Page.navigate',{url:pathToFileURL(path.resolve(target)).href});
 for(let i=0;i<100;i++){try{if(await evaluate(isGrip?"document.readyState==='complete'&&window.reviewReady":"document.readyState==='complete'&&typeof window.reviewState!=='undefined'"))break;}catch{}await delay(50);}
 const stateExpr=isGrip?'window.reviewApi.state()':'window.reviewState';
 const initial=await evaluate(`({url:location.href,title:document.title,state:${stateExpr},images:[...document.images].map(i=>({src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0})),scales:${isGrip?"['before','after','grip']":"['main','native','tactical']"}.map(id=>({id,width:document.getElementById(id)?.getBoundingClientRect().width,height:document.getElementById(id)?.getBoundingClientRect().height}))})`);
 const traces=[];
 for(const speed of [1,0.5]){
  const startCode=isGrip?`window.reviewApi.setSpeed(${speed});window.reviewApi.setLoop(false);window.reviewApi.restart();`:`document.getElementById('speed').value='${speed}';document.getElementById('loop').checked=false;document.getElementById('replay').click();`;
  const trace=await evaluate(`new Promise(resolve=>{${startCode}const start=performance.now(),samples=[];let old=-1;function sample(){const s=${stateExpr};const index=s.index??s.frame;if(index!==old){samples.push({wallMs:performance.now()-start,...s,index});old=index;}if(!s.playing&&performance.now()-start>30)resolve({speed:${speed},wallMs:performance.now()-start,samples,terminal:s});else if(performance.now()-start>5000)resolve({speed:${speed},timeout:true,samples,terminal:s});else requestAnimationFrame(sample);}requestAnimationFrame(sample);})`);
  traces.push(trace);
 }
 const steps=[];
 for(const frame of (isGrip?[2,3,4,5,6,7,8,9,10,11,12]:[2,4,5,6,7,8,10,11])){const state=await evaluate(`${isGrip?'window.reviewApi.seek':'setFrame'}(${frame});${stateExpr}`);steps.push(state);if((isGrip?[3,4,5,7,9,10]:[5,6,7]).includes(frame)){const shot=await call('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(out,label+'-F'+String(frame).padStart(2,'0')+'-chromium.png'),Buffer.from(shot.data,'base64'));}}
 let tactical=null;
 if(isGrip){await evaluate("window.reviewApi.seek(7);document.getElementById('scale').value='0.5';document.getElementById('scale').dispatchEvent(new Event('change'))");tactical=await evaluate("({state:window.reviewApi.state(),canvasWidth:document.getElementById('after').getBoundingClientRect().width,canvasHeight:document.getElementById('after').getBoundingClientRect().height})");const shot=await call('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(out,label+'-F07-tactical-chromium.png'),Buffer.from(shot.data,'base64'));}
 const result={checkedAtUtc:new Date().toISOString(),engine:'Installed Microsoft Edge Chromium headless via CDP',initial,traces,steps,tactical,limitation:'Functional playback traces and discrete PNG screenshots only; no continuous visual 1x perception is claimed.'};
 fs.writeFileSync(path.join(out,label+'-browser-check.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({file:label+'-browser-check.json',title:initial.title,scales:initial.scales,traces:traces.map(t=>({speed:t.speed,wallMs:t.wallMs,frames:t.samples.map(x=>x.index),terminal:t.terminal})),steps:steps.map(s=>s.index??s.frame),tactical,limitation:result.limitation},null,2));
 }finally{try{await call('Browser.close');}catch{}if(ws)ws.close();proc.kill();}
})().catch(e=>{console.error(e.stack);process.exitCode=1;});
