import fs from 'node:fs';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {PNG} from 'pngjs';
const E='experiments/main-orc-combat-recovery-v8/rear-inbetween';
const base='characters/orc-v1/source/combat-recovery-v8';
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const image=p=>PNG.sync.read(fs.readFileSync(p));
const rgba=p=>{const im=image(p);for(let i=0;i<im.data.length;i+=4)if(!im.data[i+3])im.data.fill(0,i,i+4);return im.data;};
const durations=[30,65,35,50,45,35,30,35,35,100,55,80,45,90];
const phases=['rest','body-preparation','establish-grip','anticipation','coil-behind','apex-hold','apex-descent','slash-release','contact','follow-through','recoil','settle-grip','release-grip','return-to-guard'];
const names=['weaponBack','body','weaponFront','handFront'];
function bright(p){const im=image(p);let n=0;for(let i=0;i<im.data.length;i+=4)if(im.data[i+3]&&.2126*im.data[i]+.7152*im.data[i+1]+.0722*im.data[i+2]>=160)n++;return n;}
function centroid(f){let n=0,x=0,y=0;for(const name of ['weaponBack','weaponFront']){const im=image(f.layers[name].png);for(let i=0;i<im.data.length;i+=4)if(im.data[i+3]&&.2126*im.data[i]+.7152*im.data[i+1]+.0722*im.data[i+2]>=160){n++;x+=(i/4)%256;y+=Math.floor(i/4/256);}}return n?[x/n,y/n]:null;}
const results=[];
for(const [direction,src] of [['back_r','rear-fix/back_r-sword'],['back_l','rear/back_l-sword']]){
 const parent=`${base}/${src}/clip.json`,old=read(parent),dst=`${base}/rear-inbetween/${direction}-sword`;
 const clip=structuredClone(old);Object.assign(clip,{revision:'main-orc-combat-recovery-v8-rear-inbetween',checkpoint:'V8_SWORD_APEX_DESCENT',frameCount:14,durationsMs:durations,totalDurationMs:730,visibleInterval:[2,11],sourceParentClip:parent,sourceParentClipSha256:hash(parent),phaseGridAuthority:'experiments/main-orc-combat-recovery-v8/sword-inbetween-spec.md',contactEvent:{...old.contactEvent,frame:8,timeMs:325,phase:'contact'},technicalStatus:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',creatorApproval:'PENDING_CREATOR'});
 clip.creatorScopeDecision={timing:'Explicit creator instruction: 30,65,35,50,45,35,30,35,35,100,55,80,45,90; 730 ms',inheritedPoses:'Preserve all thirteen inherited poses intact',preservedStep:'slash-release to contact (~60 px) predates this round and is deliberately outside the apex-descent repair scope',artisticApprovalGranted:false};clip.provenance={method:'Autoria programática real no Aseprite Lua: plano articular explícito, manga/cota desenhada em clusters, luva doadora da mesma vista articulada; arma independente vinculada à palma. Sem geração IA ou interpolação temporal de pixels.',authorScript:`${E}/author.lua`,authorScriptSha256:hash(`${E}/author.lua`),generationCalls:0,mastersSavedReopened:true,timingVerified:true,inheritedFramesPreservedRGBA:13};
 let start=0;clip.frames=durations.map((durationMs,index)=>{const oi=index<6?index:index>6?index-1:null;const f=oi===null?{}:structuredClone(old.frames[oi]);const id=String(index).padStart(2,'0');Object.assign(f,{index,phase:phases[index],durationMs,startMs:start,endMs:start+durationMs,png:`${dst}/frames/${id}.png`,nativePng:`${dst}/native/${id}.png`,weaponVisible:index>=2&&index<=11,sourceClip:parent,sourceClipSha256:hash(parent),sourceFrame:oi,sourcePhase:oi===null?'apex-descent':old.frames[oi].phase,sourceMode:oi===null?'ASEPRITE_AUTHORED_JOINT_PLAN':'REUSE_LAYER_PIXELS'});start+=durationMs;
 f.layers=Object.fromEntries(names.map(n=>{const png=`${dst}/layers/${n}/${id}.png`;return[n,{png,sha256:hash(png)}];}));f.sha256=hash(f.png);f.nativeSha256=hash(f.nativePng);
 if(oi===null){Object.assign(f,{rightGrip:direction==='back_r'?[172,105]:[170,103],rotationDeg:direction==='back_r'?25:22,poseProvenance:'Novo quadro autorado em Aseprite Lua; construção explícita da manga e articulação do antebraço/luva da própria vista. Plano em source/authorship.json.'});}
 else {for(const n of names)assert.deepEqual(rgba(f.layers[n].png),rgba(old.frames[oi].layers[n].png),`${direction}/${index}/${n} preserved`);assert.deepEqual(rgba(f.png),rgba(old.frames[oi].png));assert.deepEqual(rgba(f.nativePng),rgba(old.frames[oi].nativePng));assert.equal(bright(f.layers.body.png),bright(old.frames[oi].layers.body.png));}
 return f;});assert.equal(start,730);assert.equal(clip.frames[8].startMs,325);
 for(const [key,file]of [['master','source/composite.aseprite'],['nativeMaster','source/native.aseprite'],['strip','native-strip.png'],['nativeStrip','native-strip.png'],['compositeStrip','composite-strip.png']]){clip[key]=`${dst}/${file}`;clip[`${key}Sha256`]=hash(clip[key]);}
 // Obsolete pose-index assertions belong to the parent version, not this grid.
 delete clip.validatedV7Apex;
 const centroids=clip.frames.map(centroid),steps=[];
 for(let i=3;i<=11;i++){assert.notDeepEqual(rgba(clip.frames[i-1].png),rgba(clip.frames[i].png));steps.push({from:i-1,to:i,distance:Math.hypot(centroids[i][0]-centroids[i-1][0],centroids[i][1]-centroids[i-1][1])});}
 const max=Math.max(...steps.map(x=>x.distance));const globalBladeStepPass=max<55;assert(steps.filter(s=>s.from===5||s.from===6).every(s=>s.distance<55));
 for(const f of clip.frames){for(const n of ['weaponBack','weaponFront']){const im=image(f.layers[n].png);let count=0;for(let i=0;i<im.data.length;i+=4)if(im.data[i+3]){count++;assert(Math.floor(i/4/256)<190,'weapon above ground');}assert.equal(count>0,f.weaponVisible,`${direction}/${f.index} weapon visibility`);}}
 assert(bright(clip.frames[6].layers.body.png)>=bright(old.frames[5].layers.body.png),'new body retains bright armour count');
 fs.writeFileSync(`${dst}/clip.json`,JSON.stringify(clip,null,2)+'\n');
 const r={direction,clip:`${dst}/clip.json`,clipSha256:hash(`${dst}/clip.json`),frames:14,durationsMs:durations,totalDurationMs:730,contactEvent:clip.contactEvent,inheritedFramesRGBAIdentical:13,consecutiveArmedDuplicates:0,bladeLuminanceThreshold:160,bladeCentroids:centroids,bladeSteps:steps,maxBladeStepPx:max,globalBladeStepPass,timingDecisionPending:false,contractViolations:[],creatorAuthorizedException:'Inherited slash-release to contact (~60 px) deliberately preserved: outside apex-descent repair scope; creator explicitly required all thirteen inherited poses intact.',newBodyBrightPixels:bright(clip.frames[6].layers.body.png),apexBodyBrightPixels:bright(old.frames[5].layers.body.png),savedReopenedExport:true};results.push(r);console.log(JSON.stringify(r));
}
fs.writeFileSync(`${E}/validation.json`,JSON.stringify({technicalStatus:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',generationCalls:0,results},null,2)+'\n');
