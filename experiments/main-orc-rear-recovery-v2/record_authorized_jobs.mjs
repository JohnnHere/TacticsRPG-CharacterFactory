import fs from 'node:fs';
import path from 'node:path';
import { ROOT } from '../../src/core.mjs';
const authPath='experiments/main-orc-rear-recovery-v2/root-authorization-2026-10-26T182558Z.json';
const ledgerPath='experiments/main-orc-rear-recovery-v2/cost-provenance-ledger.json';
const auth=JSON.parse(fs.readFileSync(path.join(ROOT,authPath),'utf8'));
const ledger=JSON.parse(fs.readFileSync(path.join(ROOT,ledgerPath),'utf8'));
const rows=[
 {jobId:'8f0f4e44-0936-4502-8c5e-15b4d57e2449',assetId:'c4ef963d-b1c8-5c79-94a7-2e1b6f63b06f',target:'back_l Sword',input:'experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png',inputSha256:'2677b023bf5fa7e6f372465b5c9c54278e5cd55174577f989c18a6b0205caa8d',request:'experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-request.json',sequence:['reach with closed fist','cock sword hand high over shoulder','load across dorsal line','release forward toward northwest','slashing follow-through','lowered recovery','return to empty-hand guard']},
 {jobId:'8b6ad151-8708-4431-a606-06b250388fc4',assetId:'210f709e-872e-5be2-aba5-2a3a56e379b8',target:'back_r Axe',input:'experiments/main-orc-rear-recovery-v2/inputs/back_r-axe-native128.png',inputSha256:'251998d6cebce682a21d8fafde620200e820ef46301c6743348e331bb47e5d8c',request:'experiments/main-orc-rear-recovery-v2/inputs/back_r-axe-request.json',sequence:['brief load with fist forward','cocked shoulder, fist high','hold heavy chop above shoulder','commit torso and arm downward','impact with bent knees and weight drop','follow through low and heavy','recover to guard']}
];
for(const row of rows){
 const receipt=`id: ${row.jobId}\njob_id: ${row.jobId}\ndescription: seven-frame native128 empty-hand body cycle\nframes: 7\nsize: 128x128px\ntransparent: True\ncost: 3 generations\nstatus: processing (~4 min)\nasset_id: ${row.assetId}\nasset_status: pending`;
 auth.receipts.push({recordedAtUtc:'2026-10-26T18:29:46Z',jobId:row.jobId,assetId:row.assetId,target:row.target,tool:'mcp__pixellab__animate_with_skeleton_v3',model:'PixelLab skeleton-v3',estimatedCostGenerations:3,receiptCostGenerations:3,status:'PROCESSING',input:row.input,inputSha256:row.inputSha256,skeletonRequest:row.request,poseSequence:row.sequence,receipt});
 ledger.jobs.push({index:ledger.jobs.length+1,jobId:row.jobId,tool:'animate_with_skeleton_v3',purpose:`${row.target} representative empty-hand body cycle (7 continuous COCO-18 poses)`,chargedGenerations:3,status:'PROCESSING',input:`${row.request}; ${row.input}`,output:`experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/${row.target.replace(' ','-').toLowerCase()}/`,assetId:row.assetId,chargedReceipt:receipt,technicalNote:'Explicit Root authorization recorded in root-authorization-2026-10-26T182558Z.json before call; estimate and receipt were 3 generations.'});
}
ledger.summary.totalConsumedGenerations=75;
ledger.summary.priorRepresentativeGenerationDeviation=3;
ledger.summary.newlyAuthorizedRepresentativeJobs=2;
ledger.summary.newlyAuthorizedRepresentativeGenerations=6;
ledger.summary.verifiedAccountBalanceRemaining=1418.7;
fs.writeFileSync(path.join(ROOT,authPath),JSON.stringify(auth,null,2)+'\n');
fs.writeFileSync(path.join(ROOT,ledgerPath),JSON.stringify(ledger,null,2)+'\n');
console.log('Recorded both authorized 3-generation receipts and running ledger total 75; first 3-generation call remains explicitly documented as prior deviation.');
