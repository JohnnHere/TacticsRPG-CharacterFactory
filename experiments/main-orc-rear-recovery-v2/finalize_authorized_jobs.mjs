import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const root=process.cwd();
const authPath=path.join(root,'experiments/main-orc-rear-recovery-v2/root-authorization-2026-10-26T182558Z.json');
const auth=JSON.parse(fs.readFileSync(authPath,'utf8'));
const targets={
 '8f0f4e44-0936-4502-8c5e-15b4d57e2449':'back_l',
 '8b6ad151-8708-4431-a606-06b250388fc4':'back_r_axe'
};
for(const r of auth.receipts){
 const dir=targets[r.jobId];
 const folder=`experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/${dir}`;
 const frames=Array.from({length:7},(_,i)=>`${folder}/${String(i).padStart(2,'0')}.png`);
 for(const p of frames) if(!fs.existsSync(path.join(root,p))) throw Error(`Missing returned frame: ${p}`);
 r.status='COMPLETED';
 r.completedAtUtc='2026-10-26T18:41:00Z';
 r.outputs=frames.map(p=>({path:p,sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,p))).digest('hex')}));
 r.outputFrameCount=frames.length;
 r.assetStatus='SAVED';
}
auth.newAuthorization.actualAdditionalJobs=2;
auth.newAuthorization.actualAdditionalGenerations=6;
auth.newAuthorization.finalExperimentConsumedGenerations=75;
auth.newAuthorization.remainingAdditionalAuthorization=0;
fs.writeFileSync(authPath,JSON.stringify(auth,null,2)+'\n');
const ledgerPath=path.join(root,'experiments/main-orc-rear-recovery-v2/cost-provenance-ledger.json');
const ledger=JSON.parse(fs.readFileSync(ledgerPath,'utf8'));
ledger.authorizedRootCheckpoint=authPath.replaceAll('\\','/');
ledger.actualTotalConsumedGenerations=75;
ledger.remainingAuthorizationUnderCheckpoint=0;
ledger.recentAuthorizedJobs=auth.receipts.map(r=>({jobId:r.jobId,target:r.target,chargedGenerations:r.receiptCostGenerations,status:r.status,assetId:r.assetId,outputs:r.outputs}));
fs.writeFileSync(ledgerPath,JSON.stringify(ledger,null,2)+'\n');
console.log('Recorded completed receipts and raw frame hashes; total 75, no further authorization remains.');
