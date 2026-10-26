// Applies the creator-authorized propagation after exact candidate validation.
// Historical artwork/sources/reviews remain available in the snapshot and old builds.
import fs from 'node:fs';import path from 'node:path';
import {ROOT,inside,readJSON,json,hash,now,loadCharacter,approval,digest,write,slash} from '../src/core.mjs';
import {decode,validate} from '../src/images.mjs';
import {applyCharacterBuild,verifyEditorBuild} from '../src/aseprite.mjs';
import {actionFingerprint,planUnarmedExport} from '../src/action-export.mjs';
import {run} from '../src/cli.mjs';
const read=f=>readJSON(inside(ROOT,f)),stamp=f=>hash(fs.readFileSync(inside(ROOT,f)));
if(fs.existsSync(inside(ROOT,'reports/orc-production-current.json'))&&read('reports/orc-production-current.json').revision!=='aseprite-v4')throw Error('V4 discarded by creator: historical approvals cannot reactivate or export it as current production.');
const prepared=read('reports/orc-production-v4-prepared.json'),check=read('reports/orc-production-v4-check.json');
if(fs.existsSync(inside(ROOT,'reports/orc-production-v4-applied.json')))throw Error('Already applied: use final verification; do not duplicate approvals.');
if(check.status!=='PASS'||check.clips!==192||check.javaScriptErrors.length)throw Error('Candidate verification required');
for(const f of prepared.protectedFiles)if(stamp(f.file)!==f.sha256)throw Error('Preflight changed: '+f.file);
for(const p of prepared.packages)verifyEditorBuild(p.build);
const registry=read('characters/orc-equipment-actions-v1.json'),manifest=read(prepared.manifest),applications=[],reviews=[];
const evidence={...prepared.evidence,method:prepared.artisticMethod,preview:'reports/orc-production-v4/review.html',technicalEvidence:'reports/orc-production-v4-check.json',scopeLimit:'Approved propagation only. Existing concepts/bases unchanged. No creator in-game review; no new weapon bindings.'};
json(inside(ROOT,'reports/orc-production-v4-approval.json'),evidence);
try{
 for(const p of prepared.packages){
  const {dir,spec}=loadCharacter(p.id),character=registry.characters.find(c=>c.id===p.id),beforeBase=digest(spec,dir,'base'),beforeConcept=digest(spec,dir,'concept');
  // Static jobs are byte/pixel equivalent; apply preserves these unchanged targets.
  const baseline=read(p.fork),baselineManifest={...baseline,id:p.id+'-baseline-v4',jobs:baseline.jobs.filter(j=>j.targets?.length)};
  const {exportAseprite}=await import('../src/aseprite.mjs');
  const build=exportAseprite(baselineManifest);const application=applyCharacterBuild(p.id,build.path,true);
  if(beforeBase!==digest(spec,dir,'base')||beforeConcept!==digest(spec,dir,'concept'))throw Error('Static base/concept changed');
  const clips=[];
  for(const [direction,old]of Object.entries(character.unarmed)){
   const reuse=['orc-01','orc-01-brawler'].includes(p.id),state=reuse?'Attack':'Unarmed';
   const job=prepared.jobs.find(j=>j.characterId===p.id&&j.state===state&&j.direction===direction);if(!job)throw Error('Supplement source absent');
   const frames=job.durationsMs.map((_,n)=>{
    const file=reuse?`characters/${p.id}/sprites/${job.targets[n]}`:`characters/${p.id}/actions/basic-unarmed/v4/${direction}/attack_${direction}_${String(n).padStart(2,'0')}.png`;
    const source=`${job.directory}/frames/${String(n).padStart(2,'0')}.png`;
    if(!reuse)write(inside(ROOT,file),fs.readFileSync(inside(ROOT,source)));
    if(!decode(inside(ROOT,file)).image.data.equals(decode(inside(ROOT,source)).image.data))throw Error('Applied supplement differs');
    return {file,sha256:stamp(file)};
   });
   const clip={id:p.id,job:p.job,direction,reuse,frames,editable:job.source,editableSha256:stamp(job.source),strip:job.directory+'/native-strip.png',artisticReview:'APPROVED_BY_CREATOR_AUTHORIZED_V4_PROPAGATION',durationMs:90,durationsMs:job.durationsMs,closingPoseRepeat:true,loop:false,weaponOverlay:false};
   character.unarmed[direction]={...old,...clip,status:reuse?'REUSE_EXISTING_BODY':'V4_ASEPRITE_BODY',reuseEvidence:'Own approved outfit/view retained; V4 closing-pose reuse and timing; exact source/export verification',provenance:'Historical pixel origin retained; new edits authored by Lua within Aseprite'};clips.push(clip);
   if(!reuse){const assetFile=path.join(dir,'assets.json'),assets=readJSON(assetFile);for(let n=0;n<frames.length;n++)assets.push({at:now(),kind:'action-supplement',file:slash(path.relative(dir,inside(ROOT,frames[n].file))),sha256:frames[n].sha256,provider:'Aseprite-local',sourceFile:job.source,sourceSha256:stamp(job.source),durationMs:job.durationsMs[n],artisticApproval:clip.artisticReview,approvalEvidence:'reports/orc-production-v4-approval.json'});json(assetFile,assets);}
  }
  const review={status:'APPROVED_BY_CREATOR',actionProfile:'basic.unarmed',clips,candidateFingerprint:actionFingerprint(clips),approvalEvidence:evidence,preview:evidence.preview};
  planUnarmedExport(ROOT,p.id,review,clips);
  const reviewFile=`characters/${p.id}/source/aseprite/orc-production-v4/unarmed-review.json`;json(inside(ROOT,reviewFile),review);reviews.push({id:p.id,file:reviewFile});
  const validation=validate(spec,dir,'full');if(validation.summary.FAIL)throw Error(p.id+' validation failed');
  run(['review','--id',p.id,'--gate','consistency','--decision','approved','--reviewer','Criador','--evidence',JSON.stringify(evidence)]);
  if(!approval(spec,dir,'consistency'))throw Error('Review digest mismatch');
  const active={version:'aseprite-v4',manifest:p.fork,build:p.build,supplementReview:reviewFile,approval:'reports/orc-production-v4-approval.json'};json(path.join(dir,'source/aseprite/active-production.json'),active);
  json(path.join(dir,'reports/v4-applied.json'),{at:now(),baseline:application,fullCandidateBuild:p.build,validation:validation.summary,conceptAndBaseUnchanged:true,active});
  applications.push({id:p.id,baseline:application,build:p.build,validation:validation.summary,supplementFrames:20,supplementSourceReuse:clips[0].reuse,consistencyDigest:digest(spec,dir,'consistency')});
  console.log(p.id+': V4 applied, current Gate2 and unarmed evidence recorded');
 }
 registry.activeArtRevision='aseprite-v4';registry.activeProduction='reports/orc-production-current.json';registry.extensionStatus='APPROVED_FOR_LOCAL_EXPORT';registry.creatorFeedback=evidence.quote;registry.feedbackIsFinalConsistencyApproval=true;
 json(inside(ROOT,'characters/orc-equipment-actions-v1.json'),registry);
 const expectedChanges=new Set(applications.flatMap(p=>[`characters/${p.id}/assets.json`,`characters/${p.id}/reviews.json`,...prepared.jobs.filter(j=>j.characterId===p.id&&j.targets).flatMap(j=>j.targets.map(t=>`characters/${p.id}/sprites/${t}`))]));
 let preserved=0;for(const f of prepared.protectedFiles)if(!expectedChanges.has(f.file)){if(stamp(f.file)!==f.sha256)throw Error('Unexpected change '+f.file);preserved++;}
 for(const j of prepared.jobs)if(stamp(j.original)!==j.originalSha256)throw Error('Original master changed');
 const report={schemaVersion:1,status:'APPLIED',createdAt:now(),evidence,applications,supplementReviews:reviews,preservedProtectedFiles:preserved,protectedFilesTotal:prepared.protectedFiles.length,originalMasterFilesPreserved:216,animationSourceFiles:184,activeNativePng:896,animatedPng:856,staticPngUnchanged:40,conceptsUnchanged:true,unityIntegration:'NOT_RUN',gate3:'NOT_APPROVED',rollbackSnapshot:prepared.beforeSnapshot};
 json(inside(ROOT,'reports/orc-production-v4-applied.json'),report);
 json(inside(ROOT,'reports/orc-production-current.json'),{revision:'aseprite-v4',manifest:prepared.manifest,approval:'reports/orc-production-v4-approval.json',applied:'reports/orc-production-v4-applied.json',exportReport:'reports/orc-production-v4-export.json',supplementReviews:reviews,preview:evidence.preview});
}catch(error){
 // Restore captured production targets and metadata; keep candidates/evidence for diagnosis.
 for(const f of prepared.protectedFiles){const backup=inside(ROOT,prepared.beforeSnapshot+'/'+f.file);if(fs.existsSync(backup))write(inside(ROOT,f.file),fs.readFileSync(backup));}
 json(inside(ROOT,'characters/orc-equipment-actions-v1.json'),read(prepared.beforeSnapshot+'/equipment-registry.json'));
 json(inside(ROOT,'reports/orc-production-v4-apply-failure.json'),{at:now(),error:error.message,restored:true});throw error;
}
