// Integration metadata only; run after ART has completed its source writes.
import fs from 'node:fs';
const E='experiments/main-orc-rear-recovery-v2';
const manifestPath='characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json';
const m=JSON.parse(fs.readFileSync(manifestPath));
if(m.activeCandidatesCount!==12||m.inRevisionCount!==0||m.unchangedAliasesCount!==16)throw Error('Repair not ready for integration');
const clips=m.cells.map(c=>({...c,clip:JSON.parse(fs.readFileSync(c.clipJson))}));
const masters=[...new Set(clips.filter(c=>c.isAffected).flatMap(c=>[c.clip.master,c.clip.bodyMaster,c.clip.nativeMaster,c.clip.handMaster]).filter(Boolean))].sort();
const inventory={totalCells:m.cells.length,activeCells:m.activeCandidatesCount,aliases:m.unchangedAliasesCount,totalFrames:clips.reduce((n,c)=>n+c.clip.frames.length,0),activeClipFrames:clips.filter(c=>c.isAffected).reduce((n,c)=>n+c.clip.frames.length,0),referencedActiveMasters:masters.length,masters};
fs.writeFileSync(`${E}/root-final-inventory.json`,JSON.stringify(inventory,null,2)+'\n');
const cp='config/artistic-quality-gates-v1.json';const cfg=JSON.parse(fs.readFileSync(cp));const a=cfg.currentAssessment;
a.setStatus='VISUAL_REVIEW_REQUIRED';a.independentQAStatus='PENDING_REVIEW_OF_REVISED_FREEZE';
a.independentQAVerdict='Previous freeze6fa4653e REVISIONS_REQUIRED is historical; revised sources require the SAME Copilot reviewer on new delivery-freeze.json. Actual version-specific verdict is qa-result.json.';
a.previousRejectedFreeze='6fa4653eabe660992acc422aa32159b48e4971122df0e995b99a19261df4a843';
a.perActionStatus['Sword Attack']='VISUAL_REVIEW_REQUIRED';a.perActionStatus['Axe Attack']='VISUAL_REVIEW_REQUIRED';
Object.assign(a.accounting,{activeCandidatesCount:12,inRevisionCount:0,unchangedAliasesCount:16,matrixStructure:'12 affected ACTIVE_CANDIDATE cells and16 UNCHANGED_ALIAS cells; repaired source delivery pending exact-version independent QA and creator review.'});
a.criticalFindings=[
 'Previous independent Copilot review rejected freeze6fa4653e with QA-01..04; original report/result/freeze retained under experiments/main-orc-rear-recovery-v2/qa-history/. No previous approval is inferred.',
 'Local repair: sole ART GPT6.1 Sol Codex/Paseo b8ca8bb5 replaced rejected Luna partial after Luna returned idle. SwordL body weapon remnants and shoulder strip removed, AxeR empty fist and single connected arm restored, AxeL extraneous hook cleaned in saved Aseprite masters. Actual masks/donors/source hashes in qa-revision-1-repair/provenance.json and source-proof.json. Internal composition checkpoint is not independent QA.',
 'Current matrix12 candidates/16 aliases,210 composite frames including78 in affected clips,28 referenced composite/native masters. Successful9 affected source clips and16 aliases, original independent weapon sources and baseline verified unchanged by root-check-qa-regressions.mjs (1911 files).',
 'Layer algebra and exact body/native/master crops establish structural export consistency only. Semantic absence of painted weapons requires whole-body layers-off visual inspection. Validate continuous shoulder/elbow/wrist/fist before equipment and hand occlusion.',
 'All rear weapon representatives remain8 frames/730ms/four layers; weapons appear onlyF01..F06. No new paid calls:78 units/17jobs total, zero remaining generation authorization. No invented token/USD totals.',
 'Front Unarmed F00/F01/F03/F04 preserve decoded RGBA and timing; candidate PNG encoding differs. Original baseline bytes remain preserved. Front Defeat stages0..3 unchanged; terminal only repaired. Hit pixels/450ms retained after all-view1/.75/.5 observation; Unity calibration deferred.',
 'Preview integration by Root; no current GLM preview owner. New integrated revision must be frozen and reviewed by SAME independent GPT Sol6.1 GitHub Copilot08686; qa-result.json identifies actual reviewed freeze. Creator PENDING_CREATOR; runtimeImplemented:false; no Unity changes.'
];
fs.writeFileSync(cp,JSON.stringify(cfg,null,2)+'\n');
const note='> Atualização de integração — 27/10/2026: o checkpoint pós-QA de9 ativos/3 em reparo descrito abaixo é histórico. Os três reparos locais foram integrados como candidatos: matriz atual12 ativos/16 aliases, sem aprovação do criador. A versão corrigida precisa do parecer do MESMO QA Copilot no novo freeze. Consulte o [relatório corrente]({LINK}) e seu qa-result.json para o veredito da versão exata; não interpretar a rejeição6fa4653e nem o checkpoint interno como aprovação desta versão.\n\n';
for(const p of ['AGENTS.md','handoff/AGENT_CONTEXT.md','docs/ARTISTIC_QUALITY_GATES.md','docs/MAIN_ORC_COMBAT_POLISH.md','docs/ROADMAP.md','docs/WORKFLOW.md',`${E}/knowledge-final-report.md`,`${E}/qa-revision-1-knowledge-report.md`]){
 const link=p==='AGENTS.md'?`${E}/root-integration-report.md`:p.startsWith(E)?'root-integration-report.md':`../${E}/root-integration-report.md`;
 const s=fs.readFileSync(p,'utf8');if(!s.startsWith('> Atualização de integração — 27/10/2026:'))fs.writeFileSync(p,note.replace('{LINK}',link)+s);
}
const op=`${E}/orchestration.json`;const o=JSON.parse(fs.readFileSync(op));o.postQaRevision1.replacement.status='idle_completed_local_repair';o.postQaRevision1.integratedStatus='PENDING_SAME_REVIEWER_NEW_FREEZE';fs.writeFileSync(op,JSON.stringify(o,null,2)+'\n');
console.log(JSON.stringify({status:'INTEGRATED_PENDING_QA',...inventory},null,2));
