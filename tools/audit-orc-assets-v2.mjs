// Read-only audit of active Orc art. Writes only this audit's reports/preview data.
import fs from 'node:fs';import path from 'node:path';
import {ROOT,readJSON,json,hash,loadCharacter,approval,digest,pngFiles,slash,inside,now} from '../src/core.mjs';
import {decode,measure,validate} from '../src/images.mjs';
import {inspectAseprite} from '../src/aseprite.mjs';
const read=f=>readJSON(inside(ROOT,f)),stamp=f=>hash(fs.readFileSync(inside(ROOT,f)));
const registry=read('characters/orc-equipment-actions-v1.json'),exports=read('reports/orc-actions-export-v1.json').packages;
const production=read('reports/aseprite-production-manifest-v1.json');
const protectedFiles=new Map(),classes=[],clips=[],checks=[];
function protect(file){protectedFiles.set(file,stamp(file));return protectedFiles.get(file);}
function delta(a,b){let changed=0,union=0;for(let i=0;i<a.data.length;i+=4){if(a.data[i+3]||b.data[i+3]){union++;if(!a.data.subarray(i,i+4).equals(b.data.subarray(i,i+4)))changed++;}}return union?changed/union:0;}
function components(image){const {width:w,height:h,data}=image,seen=new Uint8Array(w*h),sizes=[];for(let i=0;i<seen.length;i++){if(seen[i]||!data[i*4+3])continue;let size=0,stack=[i];seen[i]=1;while(stack.length){const k=stack.pop();size++;const x=k%w,y=Math.floor(k/w);for(let yy=Math.max(0,y-1);yy<=Math.min(h-1,y+1);yy++)for(let xx=Math.max(0,x-1);xx<=Math.min(w-1,x+1);xx++){const n=yy*w+xx;if(!seen[n]&&data[n*4+3]){seen[n]=1;stack.push(n);}}}sizes.push(size);}return sizes.sort((a,b)=>b-a);}
for(const c of registry.characters){
 const {dir,spec}=loadCharacter(c.id),prefix=c.id.replaceAll('-','_'),technical=validate(spec,dir,'full'),relative=f=>slash(path.relative(ROOT,f));
 protect(`characters/${c.id}/character.json`);protect(`characters/${c.id}/reviews.json`);protect(`characters/${c.id}/assets.json`);
 for(const png of pngFiles(path.join(dir,'concepts')))protect(relative(png));
 for(const png of pngFiles(path.join(dir,'sprites')))protect(relative(png));
 const gates=Object.fromEntries(['concept','base','consistency','in-game'].map(g=>[g,!!approval(spec,dir,g)]));
 const views=['front_r','front_l','back_r','back_l'],classClips=[];
 for(const state of ['Idle','Walk','Attack','Hit','Defeat','Unarmed'])for(const direction of views){
  let files,durationMs,editable;
  if(state==='Unarmed'){const a=c.unarmed[direction];files=a.frames.map(f=>f.file);durationMs=a.durationMs;editable=a.editable;for(const f of a.frames)if(stamp(f.file)!==f.sha256)checks.push({id:c.id,check:'unarmed-sha',status:'FAIL',file:f.file});}
  else{files=Array.from({length:spec.profile.counts[state]},(_,i)=>`characters/${c.id}/sprites/Animations/${state}/${state.toLowerCase()}_${direction}_${String(i).padStart(2,'0')}.png`);}
  const timing=production.jobs.find(j=>j.compare?.[0]===files[0])?.profile;
  durationMs=durationMs??timing?.durationMs??timing?.durationsMs?.[0];
  const images=files.map(file=>{protect(file);const d=decode(inside(ROOT,file)),m=measure(d.image);return {file,sha256:d.sha256,rgbaSha256:hash(d.image.data),...m,components:components(d.image),image:d.image};});
  const transitions=images.map((f,i)=>delta(f.image,images[(i+1)%images.length].image));
  const sorted=transitions.slice(0,-1).sort((a,b)=>a-b),median=sorted[Math.floor(sorted.length/2)];
  const record={id:c.id,state,direction,frames:images.map(({image,...r})=>r),durationMs:durationMs??null,editable:editable??null,loop:['Idle','Walk'].includes(state),transitions,seamRatio:median?transitions.at(-1)/median:null,uniqueFrames:new Set(images.map(f=>f.rgbaSha256)).size,detachedTinyComponents:images.reduce((n,f)=>n+f.components.filter(s=>s<=2).length,0),topRange:Math.max(...images.map(f=>f.top))-Math.min(...images.map(f=>f.top)),maxColors:Math.max(...images.map(f=>f.colorCount))};
  clips.push(record);classClips.push(record);
 }
 const pkg=exports.find(e=>e.id===c.id),sourceRecords=read(pkg.path+'/source-manifest.json');
 const sources=sourceRecords.map(s=>{protect(s.original);if(stamp(s.original)!==s.sha256)checks.push({id:c.id,check:'editable-sha',status:'FAIL',file:s.original});return {file:s.original,sha256:s.sha256,...inspectAseprite(inside(ROOT,s.original))};});
 const packageFiles=read(pkg.path+'/package-hashes.json');let mismatches=0;for(const f of packageFiles)if(stamp(pkg.path+'/'+f.path)!==f.sha256)mismatches++;
 if(mismatches)checks.push({id:c.id,check:'staging',status:'FAIL',mismatches});
 classes.push({id:c.id,job:spec.job.name,identityId:spec.identityId,concepts:pngFiles(path.join(dir,'concepts')).map(relative),selectedConcept:spec.selectedConcept??null,gates,baselinePng:pngFiles(path.join(dir,'sprites')).length,baselineTechnical:technical.summary,activeSources:sources.length,sourceFrames:sources.reduce((n,s)=>n+s.frames,0),sources,staging:{path:pkg.path,files:packageFiles.length,mismatches},clips:classClips.map(x=>({state:x.state,direction:x.direction,frames:x.frames.length,seamRatio:x.seamRatio,detachedTinyComponents:x.detachedTinyComponents}))});
 for(const direction of views)protect(`characters/${c.id}/sprites/Directions/${prefix}_dir_${direction}.png`);
}
const sourcePaths=['Docs/ART_DIRECTION.md','Docs/Art/CHARACTER_PIPELINE.md','Docs/GameDesign/DESIGN_DECISIONS.md','Assets/Scripts/Presentation/UnitVisuals.cs','Assets/Scripts/Presentation/UnitView.cs'];
const referenceDrift=sourcePaths.map(p=>{const snapshot=path.join(ROOT,'references/tacticsrpg',p),original=path.resolve(ROOT,'../TacticsRPG',p);return {path:p,snapshotSha256:fs.existsSync(snapshot)?hash(fs.readFileSync(snapshot)):null,originalSha256:fs.existsSync(original)?hash(fs.readFileSync(original)):null,unchanged:fs.existsSync(snapshot)&&fs.existsSync(original)&&hash(fs.readFileSync(snapshot))===hash(fs.readFileSync(original))};});
const report={schemaVersion:1,createdAt:now(),status:checks.some(c=>c.status==='FAIL')||classes.some(c=>c.baselineTechnical.FAIL)?'TECHNICAL_FAIL':'TECHNICAL_PASS_VISUAL_REVIEW_REQUIRED',scope:'Eight active Orc body/clothing packages, concepts, legacy clips, unarmed supplements, editable sources and immutable staging; original Unity read-only',summary:{characters:classes.length,baselinePng:classes.reduce((n,c)=>n+c.baselinePng,0),uniqueNativePng:protectedFiles.size,clipReferences:clips.length,activeEditableSources:classes.reduce((n,c)=>n+c.activeSources,0),creatorConceptApprovals:classes.filter(c=>c.gates.concept).length,creatorBaseApprovals:classes.filter(c=>c.gates.base).length,creatorConsistencyApprovals:classes.filter(c=>c.gates.consistency).length,inGameApprovals:classes.filter(c=>c.gates['in-game']).length,technicalFails:checks.filter(c=>c.status==='FAIL').length+classes.reduce((n,c)=>n+c.baselineTechnical.FAIL,0)},classes,clips,checks,referenceDrift,readiness:read('reports/orc-equipment-readiness-v1.json').summary,limitations:['Metrics do not prove handedness/anatomy/style/loop quality. Detached components may be intentional; inspect before classifying as defects.','Four directions are independently authored; no mirror test can substitute visual review.'],protectedFiles:[...protectedFiles].map(([file,sha256])=>({file,sha256}))};
report.summary.uniqueNativePng=[...protectedFiles.keys()].filter(f=>f.endsWith('.png')&&!f.includes('/concepts/')).length;
json(path.join(ROOT,'reports/orc-assets-audit-v2.json'),report);console.log(JSON.stringify({status:report.status,summary:report.summary,loopSeams:clips.filter(c=>c.loop&&c.seamRatio>1.7).map(c=>({id:c.id,state:c.state,direction:c.direction,seamRatio:c.seamRatio})),tinyComponents:clips.filter(c=>c.detachedTinyComponents).map(c=>({id:c.id,state:c.state,direction:c.direction,count:c.detachedTinyComponents})),referenceDrift},null,2));
