// Technical evidence only; the creator owns artistic approval.
import fs from 'node:fs';import path from 'node:path';import {ROOT,hash} from '../src/core.mjs';import {decode,measure} from '../src/images.mjs';import {exportAseprite} from '../src/aseprite.mjs';
const read=p=>JSON.parse(fs.readFileSync(path.join(ROOT,p),'utf8')),sha=p=>hash(fs.readFileSync(path.join(ROOT,p)));
const experiment='experiments/pixellab-orc-refinement-v2',snapshot=read(experiment+'/before-manifest.json');
for(const entry of snapshot.entries)if(sha(entry.snapshot)!==entry.sha256)throw Error('Preserved snapshot changed: '+entry.snapshot);
const jobs=[],idleChecks=[],walkChecks=[];
function footMotion(frames){const first=decode(path.join(ROOT,frames[0].png)).image;let maxAlphaChange=0;for(const f of frames){const im=decode(path.join(ROOT,f.png)).image;let n=0;for(let y=104;y<128;y++)for(let x=0;x<128;x++){const p=(y*128+x)*4+3;if(first.data[p]!==im.data[p])n++;}maxAlphaChange=Math.max(maxAlphaChange,n);}return {region:'y=104..127; boot/lower-leg silhouette, not anatomical tracking',maxAlphaChangedPixels:maxAlphaChange};}
for(const n of ['04','05','06','07','08','09']){
 const id='orc-pixellab-'+n,base='characters/'+id,concept=base+'/concepts/concept-selected.png',master=base+'/source/aseprite/concept-selected.aseprite';
 if(!fs.existsSync(path.join(ROOT,concept)))throw Error('Missing concept '+id);
 jobs.push({id:id+'-concept',source:master,sourceSha256:sha(master),compare:[concept],profile:{width:128,height:128,frames:1,alpha:'any',requireTransparency:true}});
 if(Number(n)>7)continue;
 for(const state of ['Idle','Walk']){
  const clip=read(base+'/source/studies/'+state+'/clip.json');
  jobs.push({id:id+'-'+state.toLowerCase(),source:clip.master,sourceSha256:sha(clip.master),compare:clip.frames.map(f=>f.png),profile:{width:128,height:128,frames:clip.frames.length,durationsMs:clip.frames.map(f=>f.durationMs),alpha:'any',requireTransparency:true}});
  if(state==='Idle'){
   const source=decode(path.join(ROOT,concept)).image;let lockedRegionChanges=0;
   for(const f of clip.frames){const im=decode(path.join(ROOT,f.png)).image;for(let y=0;y<128;y++)if(y<=clip.headLockY||y>=clip.waistCutY)for(let x=0;x<128;x++){const i=(y*128+x)*4;for(let c=0;c<4;c++)if(source.data[i+c]!==im.data[i+c]){lockedRegionChanges++;break;}}}
   if(lockedRegionChanges)throw Error('Idle face/feet changed '+id);
   idleChecks.push({id,lockedRegionChanges,maximumTorsoDisplacementPx:clip.maximumTorsoDisplacementPx,totalMs:clip.frames.reduce((s,f)=>s+f.durationMs,0),heldPoses:'Intentional two-pose shallow breathing; not eight unique generated poses.'});
  }else if(n!=='06'){
   const old=read(experiment+'/before/'+id+'/source/studies/Walk/clip.json');old.frames=old.frames.map(f=>({...f,png:f.png.replace(base,experiment+'/before/'+id)}));
   const after=footMotion(clip.frames),before=footMotion(old.frames);if(after.maxAlphaChangedPixels<30)throw Error('Insufficient visible foot-region change '+id);
   walkChecks.push({id,frames:clip.frames.length,before,after,visualAssessment:'Manual frame contact-sheet review required in addition to this metric.'});
  }
 }
}
const manifest={schemaVersion:1,id:'pixellab-orc-refinement-v2',kind:'enemy',purpose:'Candidate review and exact editable-master export; no Unity integration',jobs};fs.writeFileSync(path.join(ROOT,experiment,'editor.json'),JSON.stringify(manifest,null,2)+'\n');
const exported=exportAseprite(manifest);if(exported.status!=='PASS')throw Error('Editor bridge failed: '+exported.status);
const old05=measure(decode(path.join(ROOT,experiment,'before/orc-pixellab-05/concepts/concept-selected.png')).image),new05=measure(decode(path.join(ROOT,'characters/orc-pixellab-05/concepts/concept-selected.png')).image);
const result={createdAt:new Date().toISOString(),status:'PASS',snapshotFilesPreserved:snapshot.entries.length,masterJobs:jobs.length,comparedFrames:jobs.reduce((s,j)=>s+j.compare.length,0),bridge:{status:exported.status,path:exported.path,summary:exported.summary},idleChecks,walkChecks,infanteConcept:{before:old05,after:new05,note:'Measurements do not establish artistic quality.'},artisticApproval:'PENDING_CREATOR',unityIntegration:'NOT_RUN'};
fs.writeFileSync(path.join(ROOT,'reports/orc-pixellab-refinement-v2-check.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({status:result.status,masters:jobs.length,frames:result.comparedFrames,snapshotFiles:result.snapshotFilesPreserved,bridge:result.bridge.summary}));
