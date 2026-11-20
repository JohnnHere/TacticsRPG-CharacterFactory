import fs from 'node:fs';
import path from 'node:path';
import {ROOT} from '../../src/core.mjs';
const p=path.join(ROOT,'characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json');
const m=JSON.parse(fs.readFileSync(p,'utf8'));
for(const d of ['front_r','front_l']){
 const c=m.cells.find(x=>x.direction===d&&x.action==='Unarmed');
 c.status='ACTIVE_CANDIDATE';c.reviewStatus='PASS_FOR_INTERNAL_INTEGRATION';c.clipJson=`characters/orc-v1/source/rear-recovery-v2/${d}/Unarmed/clip.json`;
 c.notes='Localized F02 closed-gauntlet donor restoration only. Root passed these two candidates for internal integration. Creator approval remains PENDING_CREATOR; final integrated Argon QA remains pending.';
}
const swordR=m.cells.find(x=>x.direction==='back_r'&&x.action==='Sword');
swordR.status='ACTIVE_CANDIDATE';swordR.reviewStatus='PASS_FOR_INTERNAL_EXPANSION';swordR.clipJson='characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json';
swordR.notes='Corrected 8-pose representative cycle; Root passed for internal expansion after actual composites, grip closeups, and normal-speed playback. Creator approval and integrated Argon QA remain pending.';
const counts={ACTIVE_CANDIDATE:0,ARTISTIC_REVISION_REQUIRED:0,IN_PRODUCTION:0,UNCHANGED_ALIAS:0};
for(const c of m.cells){if(!(c.status in counts))throw Error(`Unknown production status ${c.status} at ${c.cellId}`);counts[c.status]++;}
m.activeCandidatesCount=counts.ACTIVE_CANDIDATE;m.inRevisionCount=counts.ARTISTIC_REVISION_REQUIRED;m.inProductionCount=counts.IN_PRODUCTION;m.unchangedAliasesCount=counts.UNCHANGED_ALIAS;
m.passEvidenceTaxonomyNote='Root review decisions are recorded in reviewStatus. Production cells.status uses only ACTIVE_CANDIDATE, ARTISTIC_REVISION_REQUIRED, IN_PRODUCTION, or UNCHANGED_ALIAS.';
fs.writeFileSync(p,JSON.stringify(m,null,2)+'\n');
console.log(JSON.stringify({counts,total:Object.values(counts).reduce((a,b)=>a+b,0),affected:m.cells.filter(c=>c.isAffected).length,aliases:counts.UNCHANGED_ALIAS}));
