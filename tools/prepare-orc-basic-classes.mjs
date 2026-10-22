import fs from 'node:fs';
import path from 'node:path';
import {run} from '../src/cli.mjs';
import {ROOT,loadCharacter,approval,hash,json,readJSON} from '../src/core.mjs';

const parent=loadCharacter('orc-01');
if(!approval(parent.spec,parent.dir,'consistency'))throw Error('Approved Warrior required');
const designs={
  squire:'Simple quilted russet gambeson, short undyed oat tabard, narrow brown belt, modest small iron shoulder cap on the left, plain leather wrist guards and sturdy brown boots. An inexperienced practical militia squire; no elaborate heavy armor, heraldry or royal uniform.',
  archer:'Fitted moss-green sleeveless leather jerkin, ochre narrow sash, a diagonal leather baldric with small flat utility pouch, compact brown leather trousers and boots, reinforced left forearm archery bracer and right fingerless hand wrap. No quiver, arrows, bow or ammunition. Agile marksman outfit with exposed robust biceps, no hood or cape.',
  'apprentice-mage':'Desaturated indigo knee-length split-front apprentice coat over dark trousers, short broad sleeves with simple faded blue geometric stitched cuffs, ochre cord belt, one small closed leather scroll pouch at hip, plain leather boots. No wizard hat or hood; bald head visible. Modest apprentice, no elaborate archmage armor, no magic effects, staff or wand.',
  acolyte:'Warm off-white split knee-length novice vestment over dark trousers, muted teal shoulder stole with simple angular hem, plain bronze round medallion with an original abstract notch motif, tan rope belt and modest leather boots. Short sleeves show robust green arms. Fantasy healer novice; no real-world religious symbols, no hood, mace, staff or magic effects.',
  rogue:'Fitted charcoal leather short jerkin with a low raised collar, dark wine narrow sash and two short asymmetrical cloth tails, close-fitting charcoal trousers, leather boots and fingerless wraps. Small flat utility belt pouches, restrained leather shoulder protection. No hood over head, no face mask, no daggers, sheath or visible weapons. Compact urban infiltrator silhouette.',
  scout:'Earth-tan reinforced travel vest, short moss-olive shoulder mantle ending above elbows, muted brown split travel skirt over trousers, sturdy boots, small flat map pouch and tightly rolled small blanket at rear belt. Bald head and brutal face remain visible. Rugged outdoors recon silhouette, distinct from the fitted green Archer; no weapon, ammunition, trap, hood or backpack.',
  brawler:'Bare robust olive-green torso with the SAME anatomy and skin tone, worn off-white cloth wraps around wrists, knuckles and lower shins, dark loose knee trousers, a short burnt-red waist sash, simple worn low leather boots. No shoulder plate, chest armor, weapons or new tattoos. Practical unarmed fighter, original proportions, no exaggerated bodybuilder inflation.'
};
const jobs=readJSON(path.join(ROOT,'catalogs/jobs.json')).filter(j=>j.category==='Básica'&&j.id!=='warrior');
const baseRefs=[
 'characters/orc-01/concepts/orc-01-warrior-concept-07.png',
 'characters/orc-01/source/pixel-grid-v1/front-r-native-4x.png',
 'references/tacticsrpg/Docs/Art/References/character_style_anchor_v1.png'
];
const shared='Create ONE full-body outfit concept of the EXACT SAME bald adult Orc individual in reference 1, changing clothing only. Reference 1 is the edit target and authoritative individual (face, heavy brow, flat broad nose, fierce eyes, irregular lower tusks, angular jaw, pointed ears, bald scalp, grey olive skin, compact robust anatomy, hands and feet). Reference 2 is the approved native sprite: preserve its tactical proportions, scale language and facing. Reference 3 is ONLY the global refined pixel-art material/cluster style; do not copy its human anatomy, sword, cape, face, colors or outfit. Preserve the identical three-quarter front-right facing, neutral planted stance and lighting of the Orc reference; keep head fully exposed and expression fierce. Refined readable tactical RPG pixel art, crisp deliberate clusters, restrained medieval fantasy materials, mature brutal face, no smooth painterly rendering. Redraw only clothing to express the requested basic Job. Both empty hands visible and relaxed. Absolutely no held, carried or sheathed weapons, shields, bows, arrows, quivers, knives or staves. No text, labels, ground plane, shadows on background or decorative scene. Isolated full body with transparent background and generous clear margin; this is a CONCEPT candidate, not a native 128px runtime frame. Do not change the individual or simply recolor Warrior plate armor.';
const records=[];
for(const job of jobs){
 const id=`orc-01-${job.id}`,dir=path.join(ROOT,'characters',id);
 if(!fs.existsSync(dir))run(['outfit','--from','orc-01','--id',id,'--job',job.name]);
 const current=loadCharacter(id);
 if(approval(current.spec,current.dir,'concept')||fs.readdirSync(path.join(dir,'concepts')).some(f=>f.endsWith('.png')))throw Error(`Existing art must be preserved: ${id}`);
 run(['refresh-base','--id',id]);
 const {spec}=loadCharacter(id);
 spec.role=`${job.role} (Job ${job.name})`;
 spec.outfit={id:`${job.id}-candidate-v1`,description:designs[job.id],equipmentMode:'weapon-independent-base',weapon:'Assets independentes; nao incluidos na roupa; overlay runtime pendente'};
 spec.reuseAssessment=[
  {component:'individual body/face and reference contract',category:'REUSE_DIRECT',evidence:'orc-01 concept/base/consistency approvals + exact reference hashes',adaptation:'Preserve identityId, face, bald scalp, skin, dominant right hand and robust proportions; no new individual',artRisk:'Image edits may drift identity; compare against approved Warrior',technicalRisk:'Existing Warrior frames are flattened: hidden body beneath armor is unavailable',dependencies:['approved orc-01'],validation:'REFERENCE_APPROVED; VARIANT_PENDING_REVIEW'},
  {component:'Idle Walk Hit Defeat timing, ground and pose references',category:'REUSE_ADAPTED',evidence:'orc-01 97 approved native PNGs and 20 verified editable animation clips',adaptation:'Reuse pose/registration/timing reference; redraw changed clothes per frame. Reuse exact exposed-body pixels only after registered masks demonstrate compatibility',artRisk:'Long robes/mantles alter silhouette and occlusion',technicalRisk:'No layered naked-body source or automatic clothing rig exists',dependencies:['variant concept approval','native base and views approval','registered clothing/body layers'],validation:'PLANNED_NOT_DEMONSTRATED'},
  {component:'job outfit',category:'CREATE_NEW',evidence:job.source,adaptation:designs[job.id],artRisk:'Candidate Job language needs creator approval',technicalRisk:'Keep four independent views and original pixel registration',dependencies:['Gate 1'],validation:'CONCEPT_PENDING'},
  {component:'Attack and job-specific actions',category:job.id==='brawler'?'REUSE_ADAPTED':'CREATE_NEW',evidence:'Warrior has a right-hand body strike; JOB_CATALOG describes different Job roles',adaptation:job.id==='brawler'?'Use approved unarmed strike as reference, adapt outfit and validate rhythm':'Author role-specific body action; Warrior punch is not archery, healing or spellcasting',artRisk:'Action must read correctly without embedded weapons',technicalRisk:'Cast and synchronized shooting require playback/runtime extensions',dependencies:['native base approval','action design'],validation:'NOT_RUN'},
  {component:'Unity registration and separate weapons',category:'REQUIRES_EXTENSION',evidence:'docs/UNITY.md',adaptation:'No changes to sibling game; future separate integration',artRisk:'Validate weapon contact and occlusion in game later',technicalRisk:'UnitVisuals registry/overlays not implemented',dependencies:['authorized integration','PlayMode'],validation:'NOT_RUN'}
 ];
 json(path.join(dir,'character.json'),spec);
 run(['prepare','--id',id,'--purpose','outfit']);
 const prompt=`${shared}\n\nJOB: ${job.name}. CLOTHING DESIGN: ${designs[job.id]}`;
 fs.writeFileSync(path.join(dir,'source','outfit-concept-v1.prompt.md'),prompt+'\n');
 records.push({id,job:job.name,role:job.role,status:'CONCEPT_GENERATION_PENDING',promptFile:`characters/${id}/source/outfit-concept-v1.prompt.md`,references:baseRefs.map(file=>({file,sha256:hash(fs.readFileSync(path.join(ROOT,file)))})),targetNativePng:97,source:parent.spec.id});
}
json(path.join(ROOT,'characters/orc-basic-classes-plan.json'),{date:'2026-10-19',request:'Orc nas outras classes basicas, maximizar reuso para economizar tempo e tokens',sameIndividual:true,sourceCharacter:'orc-01',sourceConsistencyDigest:approval(parent.spec,parent.dir,'consistency').digest,status:'CONCEPTS_PENDING_REVIEW',targetVariantPng:679,completedVariantPng:0,reviewRule:'AGENTS.md Gate 1 before sprites; base gate before animation; no self approval',variants:records});
console.log(`${records.length} variants prepared; approved Warrior unchanged`);
