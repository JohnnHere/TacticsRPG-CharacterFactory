import fs from 'node:fs';
import path from 'node:path';
import { ROOT } from '../../src/core.mjs';
const p='characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json';
const abs=path.join(ROOT,p),m=JSON.parse(fs.readFileSync(abs,'utf8'));
for(const direction of ['front_r','front_l']){
 const c=m.cells.find(x=>x.direction===direction&&x.action==='Unarmed');
 if(!c)throw Error(`Missing ${direction}/Unarmed cell`);
 c.status='PASS_FOR_INTERNAL_INTEGRATION';c.isAffected=true;
 c.clipJson=`characters/orc-v1/source/rear-recovery-v2/${direction}/Unarmed/clip.json`;
 c.reviewStatus='PASS_FOR_INTERNAL_INTEGRATION';
 c.provenance='main-orc-rear-recovery-v2 F02 localized donor-hand restoration; Root visual checkpoint';
 c.notes='Frame 02 uses the same-view F00 hanging closed-gauntlet donor; Root passed this localized candidate for internal integration. Creator approval remains PENDING_CREATOR; integrated Argon QA remains PENDING.';
}
m.unchangedAliasesCount=16;m.affectedCount=12;m.internalIntegrationPassCount=2;
fs.writeFileSync(abs,JSON.stringify(m,null,2)+'\n');
console.log('Registered front_r/front_l Unarmed F02 as targeted internal-integration passes; four rear weapon cells remain ARTISTIC_REVISION_REQUIRED.');
