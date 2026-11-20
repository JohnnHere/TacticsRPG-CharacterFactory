// Read-only proof for the four accepted rear weapon representatives.
// `--check` performs no writes. `--write-report` writes only the proof report;
// canonical clip metadata is authored separately by author_back_l_axe_metadata.mjs.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {PNG} from 'pngjs';
import {ROOT} from '../../src/core.mjs';
import {inspectAseprite} from '../../src/aseprite.mjs';

const args=new Set(process.argv.slice(2));
const readOnly=args.has('--check');
const writeReport=args.has('--write-report');
if(readOnly&&writeReport)throw new Error('--check is read-only and cannot be combined with --write-report');
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT,p))).digest('hex');
const read=p=>PNG.sync.read(fs.readFileSync(path.join(ROOT,p)));
const counts=img=>{let n=0;for(let i=3;i<img.data.length;i+=4)if(img.data[i])n++;return n};
const same=(a,b)=>a.width===b.width&&a.height===b.height&&a.data.equals(b.data);
function over(base,top){
 const out=Buffer.from(base.data);
 for(let i=0;i<out.length;i+=4){
  const ta=top.data[i+3]/255;if(!ta)continue;
  const ba=out[i+3]/255,oa=ta+ba*(1-ta);
  for(let c=0;c<3;c++)out[i+c]=Math.round((top.data[i+c]*ta+out[i+c]*ba*(1-ta))/oa);
  out[i+3]=Math.round(oa*255);
 }
 return {width:base.width,height:base.height,data:out};
}
function gifDelays(p){
 const b=fs.readFileSync(path.join(ROOT,p));let i=13;
 if(b.toString('ascii',0,6)!=='GIF89a'&&b.toString('ascii',0,6)!=='GIF87a')throw new Error(`${p}: not GIF`);
 const packed=b[10];if(packed&0x80)i+=3*(2**((packed&7)+1));
 const delays=[];let pending;
 while(i<b.length){
  const tag=b[i++];if(tag===0x3b)break;
  if(tag===0x21){const label=b[i++];if(label===0xf9){const n=b[i++];if(n!==4)throw new Error(`${p}: invalid GCE`);i++;pending=b.readUInt16LE(i)*10;i+=2;i++;if(b[i++]!==0)throw new Error(`${p}: invalid GCE terminator`)}else{while(true){const n=b[i++];if(!n)break;i+=n}}}
  else if(tag===0x2c){i+=8;const flags=b[i++];if(flags&0x80)i+=3*(2**((flags&7)+1));i++;while(true){const n=b[i++];if(!n)break;i+=n}delays.push(pending??0);pending=undefined}
  else throw new Error(`${p}: unknown GIF block 0x${tag.toString(16)}`);
 }
 return delays;
}
function expectedDelays(ms,scale){
 if(scale==='1x')return ms;
 const factor=scale==='075x'?1/0.75:2;
 return ms.map(v=>Math.round((v*factor)/10)*10);
}

const clips=[
 {path:'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json',direction:'back_r',action:'Sword',reviewStatus:'PASS_FOR_INTERNAL_EXPANSION'},
 {path:'characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/clip.json',direction:'back_l',action:'Sword',reviewStatus:'PASS_FOR_INTERNAL_EXPANSION'},
 {path:'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/clip.json',direction:'back_r',action:'Axe',reviewStatus:'PASS_FOR_INTERNAL_EXPANSION'},
 {path:'characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/clip.json',direction:'back_l',action:'Axe',reviewStatus:'PASS_FOR_INTERNAL_INTEGRATION'}
];
const failures=[],results=[];
for(const spec of clips){
 try{
  const clip=JSON.parse(fs.readFileSync(path.join(ROOT,spec.path),'utf8'));
  const out=path.posix.dirname(spec.path),frames=clip.frames??[],durations=clip.durationsMs??[];
  const weaponName=spec.action.toLowerCase(),expected=[90,80,90,80,100,80,100,110];
  if(clip.character!=='orc-v1'||clip.direction!==spec.direction||clip.category!==spec.action)failures.push(`${spec.direction}/${spec.action}: clip identity mismatch`);
  if(clip.canvas?.[0]!==256||clip.canvas?.[1]!==256||clip.nativeCanvas?.[0]!==128||clip.nativeCanvas?.[1]!==128)failures.push(`${spec.direction}/${spec.action}: canvas/native dimensions mismatch`);
  if(frames.length!==8||JSON.stringify(durations)!==JSON.stringify(expected)||durations.reduce((a,b)=>a+b,0)!==730)failures.push(`${spec.direction}/${spec.action}: metadata frame count/timing mismatch`);
  if(clip.frameCount!==8||clip.totalDurationMs!==730)failures.push(`${spec.direction}/${spec.action}: metadata totals mismatch`);
  if(JSON.stringify(clip.layerOrder)!==JSON.stringify(['weaponBack','body','weaponFront','handFront']))failures.push(`${spec.direction}/${spec.action}: layer order mismatch`);
  if(JSON.stringify(clip.visibleInterval)!==JSON.stringify([1,6]))failures.push(`${spec.direction}/${spec.action}: attack-only visible interval mismatch`);
  if(clip.artisticApproval&&clip.artisticApproval!=='PENDING_CREATOR')failures.push(`${spec.direction}/${spec.action}: creator approval field is not pending`);
  const compInfo=inspectAseprite(path.join(ROOT,clip.master));
  const bodyInfo=inspectAseprite(path.join(ROOT,clip.bodyMaster));
  const nativeInfo=inspectAseprite(path.join(ROOT,clip.nativeMaster));
  for(const [label,info,w] of [['composite',compInfo,256],['body',bodyInfo,256],['native',nativeInfo,128]]){
   if(info.width!==w||info.height!==w||info.frames!==8||JSON.stringify(info.durationsMs)!==JSON.stringify(expected))failures.push(`${spec.direction}/${spec.action}: saved ${label} master dimensions/timing mismatch`);
  }
  const frameRows=[];
  for(let i=0;i<8;i++){
   const f=frames[i],n=String(i).padStart(2,'0');
   if(f.index!==i||f.durationMs!==expected[i])failures.push(`${spec.direction}/${spec.action} f${n}: frame index or duration metadata mismatch`);
   const compPath=f.png,nativePath=f.nativePng;
   if(!compPath||!nativePath||!fs.existsSync(path.join(ROOT,compPath))||!fs.existsSync(path.join(ROOT,nativePath))){failures.push(`${spec.direction}/${spec.action} f${n}: missing composite/native export`);continue;}
   if(sha(compPath)!==f.sha256)failures.push(`${spec.direction}/${spec.action} f${n}: composite hash mismatch`);
   if(sha(nativePath)!==f.nativeSha256)failures.push(`${spec.direction}/${spec.action} f${n}: native hash mismatch`);
   const layerPaths=Object.fromEntries(['weaponBack','body','weaponFront','handFront'].map(k=>[k,f.layers?.[k]?.png]));
   const layerImgs={};
   for(const k of Object.keys(layerPaths)){
    const p=layerPaths[k];if(!p||!fs.existsSync(path.join(ROOT,p))){failures.push(`${spec.direction}/${spec.action} f${n}: missing ${k} layer export`);continue;}
    if(sha(p)!==f.layers[k].sha256)failures.push(`${spec.direction}/${spec.action} f${n}: ${k} layer hash mismatch`);
    layerImgs[k]=read(p);
   }
   if(Object.keys(layerImgs).length===4){
    let assembled=layerImgs.weaponBack;for(const k of ['body','weaponFront','handFront'])assembled=over(assembled,layerImgs[k]);
    const comp=read(compPath),bodyOnly=read(`${out}/body-only/${n}.png`),native=read(nativePath);
    if(!same(assembled,comp))failures.push(`${spec.direction}/${spec.action} f${n}: four-layer recomposition differs from composite`);
    if(!same(layerImgs.body,bodyOnly))failures.push(`${spec.direction}/${spec.action} f${n}: separate body master differs from composite body layer`);
    const crop=Buffer.alloc(128*128*4);for(let y=0;y<128;y++){const a=((y+64)*256+64)*4;layerImgs.body.data.copy(crop,y*128*4,a,a+128*4)}
    if(!crop.equals(native.data))failures.push(`${spec.direction}/${spec.action} f${n}: native 128 PNG is not exact center crop of body layer`);
    const weaponPx=counts(layerImgs.weaponBack)+counts(layerImgs.weaponFront),handPx=counts(layerImgs.handFront),shouldBeVisible=i>=1&&i<=6;
    if(f.weaponVisible!==shouldBeVisible)failures.push(`${spec.direction}/${spec.action} f${n}: clip visibility metadata contradicts attack interval`);
    if(shouldBeVisible&&weaponPx===0)failures.push(`${spec.direction}/${spec.action} f${n}: visible weapon layers empty`);
    if(!shouldBeVisible&&weaponPx!==0)failures.push(`${spec.direction}/${spec.action} f${n}: weapon pixels outside attack interval`);
    if(shouldBeVisible&&handPx===0)failures.push(`${spec.direction}/${spec.action} f${n}: handFront is empty at grip`);
    if(shouldBeVisible&&Array.isArray(f.rightGrip)){
     const gx=Math.round(f.rightGrip[0]),gy=Math.round(f.rightGrip[1]);let nearby=0;
     for(let y=Math.max(0,gy-5);y<=Math.min(255,gy+5);y++)for(let x=Math.max(0,gx-5);x<=Math.min(255,gx+5);x++)if(layerImgs.body.data[(y*256+x)*4+3])nearby++;
     if(nearby===0)failures.push(`${spec.direction}/${spec.action} f${n}: grip anchor has no nearby body pixels`);
    }
    frameRows.push({index:i,phase:f.phase,durationMs:f.durationMs,weaponVisible:shouldBeVisible,composite:compPath,sha256:f.sha256,native:nativePath,nativeSha256:f.nativeSha256,weaponLayerPixels:weaponPx,handFrontPixels:handPx});
   }
  }
  const gifs={};
  for(const scale of ['1x','075x','05x']){
   const p=`experiments/main-orc-rear-recovery-v2/${spec.direction}-${weaponName}-representative-${scale}.gif`;
   const got=gifDelays(p),want=expectedDelays(expected,scale),total=got.reduce((a,b)=>a+b,0);
   if(JSON.stringify(got)!==JSON.stringify(want))failures.push(`${spec.direction}/${spec.action} ${scale}: GIF delays differ from expected ${want.join('/')}`);
   if(got.length!==8)failures.push(`${spec.direction}/${spec.action} ${scale}: GIF has ${got.length} frames, expected 8`);
   gifs[scale]={path:p,sha256:sha(p),frameDelaysMs:got,totalMs:total};
  }
  if(clip.weapon?.source&&clip.weapon.sourceSha256!==sha(clip.weapon.source))failures.push(`${spec.direction}/${spec.action}: independent weapon source hash mismatch`);
  if(spec.direction==='back_l'&&spec.action==='Axe'){
   if(clip.provenance?.generationJobId!=='5296ac98-b253-4133-8468-155f7e90c68e')failures.push('back_l/Axe: provenance points to wrong generation job');
   if(!clip.provenance?.sourceFrames?.some(p=>p.includes('raw/pixellab-skeleton-v3/back_l_axe/')))failures.push('back_l/Axe: raw provenance path is not the back_l_axe job output');
   if(clip.provenance?.actualCostGenerations!==3||clip.provenance?.experimentTotalGenerations!==78)failures.push('back_l/Axe: generation cost metadata mismatch');
  }
  results.push({direction:spec.direction,action:spec.action,clipJson:spec.path,clipJsonSha256:sha(spec.path),master:clip.master,masterSha256:sha(clip.master),bodyMaster:clip.bodyMaster,bodyMasterSha256:sha(clip.bodyMaster),nativeMaster:clip.nativeMaster,nativeMasterSha256:sha(clip.nativeMaster),dimensions:{composite:[256,256],native:[128,128]},frameCount:8,durationsMs:expected,totalDurationMs:730,gifSummary:gifs,frames:frameRows});
 }catch(e){failures.push(`${spec.direction}/${spec.action}: ${e.stack??e.message}`);}
}
const report={schemaVersion:2,status:failures.length?'FAIL':'PASS',sourceOfFinalExports:'Aseprite re-exported PNGs from saved four-layer composite masters and separate body-only masters',checks:{clips:4,frameCount:8,durationsMs:[90,80,90,80,100,80,100,110],totalDurationMs:730,composition:'exact decoded RGBA alpha-over comparison',bodyMaster:'separate saved body master equals composite body layer',native128:'exact center crop from 256 body layer',weaponVisibility:'only frames 01..06',gifScaleProofs:['1x','075x','05x'],clipMetadata:'read-only SHA and provenance checks'},results,failures};
if(writeReport){
 if(failures.length){console.error(JSON.stringify(report,null,2));process.exitCode=1;}
 else{report.createdAtUtc=new Date().toISOString();fs.writeFileSync(path.join(ROOT,'experiments/main-orc-rear-recovery-v2/new-representative-source-export-verification.json'),JSON.stringify(report,null,2)+'\n');}
}
console.log(JSON.stringify({mode:readOnly?'READ_ONLY_CHECK':writeReport?'WRITE_REPORT':'READ_ONLY_CHECK',status:report.status,failedChecks:failures,clips:results.map(r=>({direction:r.direction,action:r.action,gifs:Object.fromEntries(Object.entries(r.gifSummary).map(([k,v])=>[k,v.totalMs]))}))},null,2));
if(failures.length)process.exitCode=1;
