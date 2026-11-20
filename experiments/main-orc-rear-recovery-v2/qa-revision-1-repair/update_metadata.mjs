import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const E='experiments/main-orc-rear-recovery-v2',O=`${E}/qa-revision-1-repair`;
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const specs=[['SwordL','back_l','Sword',['QA-01']],[ 'AxeR','back_r','Axe',['QA-02','QA-03']],['AxeL','back_l','Axe',['QA-04']]];
const write=(p,x)=>fs.writeFileSync(p,JSON.stringify(x,null,2)+'\n');
const cp=JSON.parse(fs.readFileSync(`${O}/checkpoint/checkpoint.json`));
cp.rootCheckpoint='ACCEPTED_FOR_LOCAL_COMPOSITION_ONLY';
cp.rootAcceptanceEvidence='Explicit Root instruction in session: checkpoint internally accepted only to continue composition; no QA or creator approval.';
write(`${O}/checkpoint/checkpoint.json`,cp);
const arGrips=[[0,0],[175,106],[167,73],[167,78],[181,118],[181,122],[156,139],[0,0]];
const provenance={schemaVersion:1,createdAtUtc:new Date().toISOString(),status:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',creatorApproval:'PENDING_CREATOR',independentQA:'PENDING_NEW_FREEZE_SAME_COPILOT_REVIEWER',generationCalls:0,experimentGenerationUnits:78,experimentJobs:17,coordinateRegistration:'Masks in native128; +64,+64 registration to256 composite. No mirroring.',backup:`${E}/rejected/qa-revision-1-before/backup-manifest.json`,fullByteBackup:`${E}/E/rejected/qa-revision-1-before/backup-inventory.json`,priorRejectedPartial:`${E}/E/qa-revision-1-art-report.md`,checkpoint:`${O}/checkpoint/checkpoint.json`,scripts:['author_body.lua','compose.lua'].map(n=>({path:`${O}/${n}`,sha256:sha(`${O}/${n}`)})),cells:[]};
for(const [key,d,a,findings] of specs){
 const p=`characters/orc-v1/source/rear-recovery-v2/${d}/${a}/Attack-representative-v1/clip.json`;
 const c=JSON.parse(fs.readFileSync(p));
 for(const k of ['master','bodyMaster','nativeMaster','strip'])c[`${k}Sha256`]=sha(c[k]);
 c.technicalStatus='TECHNICALLY_COMPLETE';c.artisticStatus='VISUAL_REVIEW_REQUIRED';c.artisticApproval='PENDING_CREATOR';
 c.provenance.qaRevision1={record:`${O}/provenance.json`,bodyAuthoring:`${O}/author_body.lua`,compositionAuthoring:`${O}/compose.lua`,findings,rootCheckpoint:'ACCEPTED_FOR_LOCAL_COMPOSITION_ONLY',generationCalls:0};
 c.provenance.bodyCleanup='QA revision 1: bounded Aseprite repairs after independent QA rejection. See qaRevision1.record and preserved rejected freeze; earlier claims of a clean generated body were incomplete.';
 c.reviewEvidence??={};
 c.reviewEvidence.rootReview='BODY_CHECKPOINT_ACCEPTED_FOR_LOCAL_COMPOSITION_ONLY';
 c.reviewEvidence.integratedArgonQA='PENDING_NEW_FREEZE_SAME_COPILOT_REVIEWER';
 c.reviewEvidence.localArtReview='VISUAL_REVIEW_REQUIRED';
 c.reviewEvidence.qaRevision1={report:`${E}/qa-revision-1-art-escalation-report.md`,wholeBody:`${O}/checkpoint/${key}-wholebody.png`,composite:`${O}/final/${key}-composite-wholebody.png`,grips:`${O}/final/${key}-grips.png`,playback:`${O}/playback-verification.json`};
 for(const fr of c.frames){
  fr.sha256=sha(fr.png);fr.nativeSha256=sha(fr.nativePng);
  for(const l of Object.values(fr.layers))l.sha256=sha(l.png);
  if(key==='AxeR')fr.rightGrip=arGrips[fr.index];
 }
 for(const [scale,g] of Object.entries(c.reviewEvidence.gifExports??{}))g.sha256=sha(g.path);
 write(p,c);
 provenance.cells.push({cell:`${d}/${a}`,findings,clipJson:p,clipJsonSha256:sha(p),master:c.master,masterSha256:c.masterSha256,bodyMaster:c.bodyMaster,bodyMasterSha256:c.bodyMasterSha256,nativeMaster:c.nativeMaster,nativeMasterSha256:c.nativeMasterSha256,weapon:{...c.weapon,unchanged:true},changedBodyPixels:cp.cells.find(x=>x.key===key).frames.map(x=>({index:x.index,changedPixels:x.changedPixels,nativeBbox:x.nativeChangeBbox})),grips:c.frames.map(f=>({index:f.index,rightGrip:f.rightGrip,rotationDeg:f.rotationDeg})),donors:[]});
}
const donorPaths=['characters/orc-v1/source/complete-v1/back_l/Idle/00.png','characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/layers/body/01.png','characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/layers/handFront/01.png','characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/layers/body/05.png','characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/layers/handFront/05.png'];
provenance.donors=donorPaths.map(p=>({path:p,sha256:sha(p),classification:'REUSE_ADAPTED',identity:'same Orc V1, same view as target'}));
provenance.methods={SwordL:'Same-view static hanging gauntlet through silhouette mask F01..07; F04 far-shoulder triangle; F05 traced blade removal, local own F04 pauldron rim donor at +6,-3, preserving original bent elbow chain. Six exact detached source pixels removed.',AxeR:'F01 same-view accepted SwordR F01 connected reach/fist; F02/F03 source wood stub erased, F03 knuckle cap locally authored in Aseprite. F04/F05 old distal silhouette cleared to transparency before own accepted SwordR F05 arm+real closed glove at (0,-3)/(0,+1). Existing compact independent axe rerendered to actual fist for F01/F04/F05. HandFront contains actual body glove pixels only.',AxeL:'Only F02/F03 far-shoulder tip/strand contour restored from own static back_l. Its generative origin remains unproven. Earlier raised fist and all27 exact cleanup coordinates preserved.'};
write(`${O}/provenance.json`,provenance);
console.log('Updated only three canonical clip metadata and scoped repair provenance; manifest partition waits for local playback validation.');
