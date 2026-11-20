import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {PNG} from 'pngjs';
const E='experiments/main-orc-hybrid-weapon-04';const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');const read=p=>PNG.sync.read(fs.readFileSync(p)).data;
const source=JSON.parse(fs.readFileSync('characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_l-sword/clip.json'));const pipeline=JSON.parse(fs.readFileSync(E+'/pipeline-result.json'));const build=E+'/pipeline/'+pipeline.path;
const checks=[];
for(const v of ['a','b']){
 for(const section of ['representative','full']){
  const frames=section==='full'?source.frames:source.frames.filter(f=>[2,8,11].includes(f.index));
  for(const f of frames){const nn=String(f.index).padStart(2,'0');for(const folder of ['body-only','weapon-only','composite',...source.layerOrder.map(n=>'layers/'+n)]){const p=`${E}/${section}/${v}/${folder}/F${nn}.png`;fs.copyFileSync(p,`${E}/${section}/${v}/${folder}/${nn}.png`)}
   if(section==='representative')for(const n of ['body','handFront']){const p=`${E}/${section}/${v}/layers/${n}/F${nn}.png`;checks.push({variant:v,frame:f.index,layer:n,representativeByteIdenticalSource:sha(p)===sha(f.layers[n].png)})}
  }
 }
 const files=fs.readdirSync(`${build}/jobs/sword-${v}/frames`).sort();
 for(let i=0;i<14;i++){const ok=read(`${build}/jobs/sword-${v}/frames/${files[i]}`).equals(read(`${E}/full/${v}/composite/F${String(i).padStart(2,'0')}.png`));checks.push({variant:v,frame:i,pipelinePixelsMatch:ok});}
 const c={schemaVersion:1,technicalStatus:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',artisticApproval:'PENDING_CREATOR',master:'composite.aseprite',masterSha256:sha(`${E}/full/${v}/composite.aseprite`),frameCount:14,durationsMs:source.durationsMs,totalDurationMs:730,canvas:[256,256],visibleInterval:[2,11],contactEvent:source.contactEvent,layerOrder:source.layerOrder,frames:source.frames.map(f=>({index:f.index,durationMs:f.durationMs,png:`composite/${String(f.index).padStart(2,'0')}.png`,sha256:sha(`${E}/full/${v}/composite/F${String(f.index).padStart(2,'0')}.png`)}))};fs.writeFileSync(`${E}/full/${v}/clip.json`,JSON.stringify(c,null,2));
}
if(checks.some(c=>c.representativeByteIdenticalSource===false||c.pipelinePixelsMatch===false))throw Error('Final verification failed');
fs.writeFileSync(E+'/delivery-verification.json',JSON.stringify({status:'PASS',checks},null,2));
const walk=p=>fs.readdirSync(p,{withFileTypes:true}).flatMap(d=>d.isDirectory()?walk(path.join(p,d.name)):[path.join(p,d.name)]);
for(const v of ['a','b']){const p=`${E}/variants/sword-${v}`;fs.writeFileSync(p+'/hashes.json',JSON.stringify(Object.fromEntries(walk(p).filter(f=>!f.endsWith('hashes.json')).map(f=>[path.basename(f),sha(f)])),null,2));}
console.log({status:'PASS',checks:checks.length,preview:build+'/preview.html'});
