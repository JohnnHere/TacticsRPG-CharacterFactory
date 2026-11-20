import fs from 'node:fs';
import crypto from 'node:crypto';
const E='experiments/main-orc-rear-recovery-v2',O=`${E}/qa-revision-1-repair`;
const read=p=>JSON.parse(fs.readFileSync(p));
const write=(p,c)=>fs.writeFileSync(p,JSON.stringify(c,null,2)+'\n');
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
for(const p of ['source-proof.json','playback-verification.json'])if(read(`${O}/${p}`).status!=='PASS')throw Error(`Refuse local finalization: ${p} failed`);
const mpath='characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json',m=read(mpath);
const targets=new Map([['back_l/Sword',['QA-01']],['back_r/Axe',['QA-02','QA-03']],['back_l/Axe',['QA-04']]]);
const before=read(`${E}/E/rejected/qa-revision-1-before/backup-inventory.json`);
const oldManifest=before.files.find(x=>x.source===mpath);
const old=read(`${E}/E/rejected/qa-revision-1-before/${oldManifest.backup}`);
for(const cell of m.cells){
 if(!targets.has(cell.cellId)){
  if(JSON.stringify(cell)!==JSON.stringify(old.cells.find(c=>c.cellId===cell.cellId)))throw Error(`Non-target manifest cell changed: ${cell.cellId}`);
  continue;
 }
 cell.status='ACTIVE_CANDIDATE';cell.reviewStatus='VISUAL_REVIEW_REQUIRED';
 cell.qaRevision1={findings:targets.get(cell.cellId),technicalStatus:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',report:`${E}/qa-revision-1-art-escalation-report.md`,independentQA:'PENDING_NEW_FREEZE_SAME_COPILOT_REVIEWER',creatorApproval:'PENDING_CREATOR'};
 cell.notes+=` QA revision 1 authored locally in Aseprite; body checkpoint accepted by Root for composition only, fresh source proof and local1/.75/.5 playback checked. Independent re-review of a new freeze remains pending; PENDING_CREATOR.`;
 const c=read(cell.clipJson);
 c.reviewEvidence.localArtReview='TECHNICALLY_COMPLETE';
 c.reviewEvidence.independentReReview='PENDING_NEW_FREEZE_SAME_COPILOT_REVIEWER';
 write(cell.clipJson,c);
}
const counts={};for(const c of m.cells)counts[c.status]=(counts[c.status]??0)+1;
m.activeCandidatesCount=counts.ACTIVE_CANDIDATE??0;m.inRevisionCount=counts.ARTISTIC_REVISION_REQUIRED??0;m.unchangedAliasesCount=counts.UNCHANGED_ALIAS??0;m.inProductionCount=counts.IN_PRODUCTION??0;
write(mpath,m);
const p=read(`${O}/provenance.json`);for(const c of p.cells)c.clipJsonSha256=sha(c.clipJson);
p.localSourceProof=`${O}/source-proof.json`;p.localPlaybackProof=`${O}/playback-verification.json`;p.localVisualInspection='Whole-body layers-off checkpoint accepted by Root for recomposition; ART directly inspected saved-source composites, actual glove/handle crops, and complete ordered actual-RAF samples at1/.75/.5. No independent verdict or creator approval claimed.';
write(`${O}/provenance.json`,p);
console.log(JSON.stringify({status:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',manifestCounts:counts,nonTargetManifestCellsUnchanged:25},null,2));
