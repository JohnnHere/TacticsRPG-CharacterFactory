// Integration-only digest utility. Does not modify production art or selection.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const E='experiments/main-orc-rear-recovery-v2';
const out=`${E}/delivery-freeze.json`;
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
if(process.argv.includes('--check')){
  const m=JSON.parse(fs.readFileSync(out));
  const changed=Object.entries(m.files).filter(([p,h])=>!fs.existsSync(p)||sha(p)!==h).map(([p])=>p);
  console.log(JSON.stringify({freezeId:m.freezeId,checked:Object.keys(m.files).length,status:changed.length?'FAIL':'PASS',changed},null,2));
  process.exitCode=changed.length?1:0;
}else{
  if(!process.argv.includes('--create'))throw Error('Use --create after final integration, or --check for read-only validation.');
  const files=new Set();
  function add(p){if(/(?:^|\/)(__pycache__|node_modules|\.pytest_cache)(?:\/|$)|\.pyc$/.test(p))return;if(!fs.existsSync(p))throw Error(`Missing freeze input ${p}`);if(fs.statSync(p).isDirectory()){for(const n of fs.readdirSync(p))add(`${p}/${n}`);}else files.add(p.replaceAll('\\','/'));}
  for(const p of ['AGENTS.md','docs','config/artistic-quality-gates-v1.json','recipes/races/orc.candidate.json','handoff/AGENT_CONTEXT.md','tools','test','assets/weapons/recruit-sword','assets/weapons/militia-axe','characters/orc-v1/source/rear-recovery-v2','characters/orc-v1/source/aseprite/rear-recovery-v2','Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira'])add(p);
  const protectedBaseline=JSON.parse(fs.readFileSync(`${E}/production-protection.json`));
  Object.keys(protectedBaseline.files).forEach(add);
  // Include transitive file references, including historical native PNGs outside
  // the composite directories. Do not freeze only the most obvious folders.
  const current=JSON.parse(fs.readFileSync('characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json'));
  function referenced(value){
    if(Array.isArray(value))value.forEach(referenced);
    else if(value&&typeof value==='object')Object.values(value).forEach(referenced);
    else if(typeof value==='string'&&/^(characters\/|assets\/weapons\/|experiments\/main-orc-rear-recovery-v2\/)/.test(value)&&fs.existsSync(value)&&fs.statSync(value).isFile())add(value);
  }
  referenced(current);
  for(const c of current.cells){add(c.clipJson);referenced(JSON.parse(fs.readFileSync(c.clipJson)));}
  for(const n of fs.readdirSync(E)){
    // Freeze implementation scripts and immutable provenance, not regenerated QA outputs.
    if(/\.(lua|mjs|py)$/.test(n)||/^(root-authorization-.*\.json|cost-provenance-ledger\.json|orchestration\.json|production-protection\.json|creator-task\.md|orchestration-request\.md|.*final-report\.md|root-integration-report\.md|root-hit-playback-assessment\.md)$/.test(n))add(`${E}/${n}`);
  }
  add(`${E}/raw`);
  // The post-QA repair owns nested Lua/source/checkpoint evidence as well.
  // Freeze the actual recorded authoring code and saved intermediate masters,
  // rather than only the final export PNGs or top-level scripts.
  for(const p of [`${E}/qa-revision-1-repair`,`${E}/E/qa-revision-1`])if(fs.existsSync(p))add(p);
  for(const p of [`${E}/qa-revision-1-art-escalation-report.md`,`${E}/qa-revision-1-knowledge-report.md`,`${E}/E/qa-revision-1-art-report.md`,`${E}/rejected/qa-revision-1-before/backup-manifest.json`])if(fs.existsSync(p))add(p);
  add(`${E}/preservation-snapshot.json`);
  add(`${E}/qa-final-task.md`);
  add(`${E}/qa-revision-1-rereview-task.md`);
  add(`${E}/root-qa-revision-1-tests.json`);
  add(`${E}/root-qa-revision-1-git-status.txt`);
  add(`${E}/root-qa-revision-1-preservation.json`);
  for(const n of ['root-integration-tests.json','root-final-inventory.json','root-final-preservation.json','root-immutable-build-preservation.json','new-representative-source-export-verification.json','four-early-clips-source-metadata-verification.json'])add(`${E}/${n}`);
  const sourceProof=JSON.parse(fs.readFileSync(`${E}/four-early-clips-source-metadata-verification.json`));
  add(sourceProof.nativeExportBuild);
  add(sourceProof.compositeExportBuild);
  add('dist/editor/orc-v1-complete-v1/b178422e1f7fc19f068c');
  add('Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html');
  add('Biblioteca de Arte/Estudos Comparativos/Orc principal - Biblioteca completa/index.html');
  const hashes=Object.fromEntries([...files].sort().map(p=>[p,sha(p)]));
  const freezeId=crypto.createHash('sha256').update(JSON.stringify(hashes)).digest('hex');
  const m={schemaVersion:1,freezeId,createdAt:new Date().toISOString(),creatorApproval:'PENDING_CREATOR',runtimeImplemented:false,files:hashes,exclusions:'Independent QA outputs and QA-created temporary reexports, regenerated validation reports and root browser samples. The two existing source-proof builds consumed by delivered validators are explicitly included.'};
  if(fs.existsSync(out)){
    const previous=JSON.parse(fs.readFileSync(out));
    if(previous.freezeId!==freezeId){fs.mkdirSync(`${E}/freeze-history`,{recursive:true});fs.copyFileSync(out,`${E}/freeze-history/${previous.freezeId}.json`);}
  }
  fs.writeFileSync(out,JSON.stringify(m,null,2)+'\n');
  console.log(JSON.stringify({freezeId,files:files.size,path:out}));
}
