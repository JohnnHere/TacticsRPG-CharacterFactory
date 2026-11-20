// Read-only regression guard against the first independently reviewed delivery.
import fs from 'node:fs';
import crypto from 'node:crypto';
const E='experiments/main-orc-rear-recovery-v2';
const original='6fa4653eabe660992acc422aa32159b48e4971122df0e995b99a19261df4a843';
const freeze=JSON.parse(fs.readFileSync(`${E}/qa-history/${original}/delivery-freeze.json`));
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const bad=/characters\/orc-v1\/source\/rear-recovery-v2\/(back_l\/Sword|back_[rl]\/Axe)\//;
const badMaster=/characters\/orc-v1\/source\/aseprite\/rear-recovery-v2\/(composite\/(back_l\/sword-|back_[rl]\/axe-)|native\/(sword-.*back_l|axe-.*back_[rl]))/;
const protectedFiles=Object.entries(freeze.files).filter(([p])=>
  (/^characters\/orc-v1\/source\/(rear-recovery-v2|aseprite\/rear-recovery-v2)\//.test(p)
    && !bad.test(p) && !badMaster.test(p) && !p.endsWith('candidate28manifest.json'))
  || /^assets\/weapons\/(recruit-sword|militia-axe)\//.test(p)
  || /^characters\/orc-v1\/source\/complete-v1\//.test(p)
  || /^dist\/editor\/orc-v1-complete-v1\/b178422e1f7fc19f068c\//.test(p)
  || p==='characters/orc-v1/source/equipment-current.json');
const changed=protectedFiles.filter(([p,h])=>!fs.existsSync(p)||sha(p)!==h).map(([p])=>p);
console.log(JSON.stringify({referenceFreeze:original,checkedFiles:protectedFiles.length,status:changed.length?'FAIL':'PASS',changed},null,2));
process.exitCode=changed.length?1:0;
