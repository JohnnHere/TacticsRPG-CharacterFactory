import fs from 'node:fs';import path from 'node:path';import {ROOT,hash,json,readJSON} from '../src/core.mjs';
const read=f=>readJSON(path.join(ROOT,f)),stamp=f=>hash(fs.readFileSync(path.join(ROOT,f)));
const old=read('characters/orc-unarmed-front-batch-v1.json');json(path.join(ROOT,'characters/orc-unarmed-front-initial-attempts-v1.json'),old);
const active=old.filter(b=>b.id!=='orc-01');for(const b of active)if(b.id==='orc-01-squire'){b.folder=b.folder.replace('action-clips-v1','action-clips-v2');b.supplementVersion='v2';const g=read(`${b.folder}/generation.json`);for(const ref of g.references)ref.sha256=stamp(ref.file);json(path.join(ROOT,b.folder,'generation.json'),g);}
json(path.join(ROOT,'characters/orc-unarmed-front-batch-v1.json'),active);
const registry=read('characters/orc-equipment-actions-v1.json'),warrior=registry.characters.find(c=>c.id==='orc-01');
for(const d of ['front_r','front_l','back_r','back_l'])warrior.unarmed[d]={status:'REUSE_EXISTING_BODY',bodyProfile:'basic.unarmed',frames:Array.from({length:5},(_,i)=>{const file=`characters/orc-01/sprites/Animations/Attack/attack_${d}_${String(i).padStart(2,'0')}.png`;return {file,sha256:stamp(file)};}),durationMs:90,loop:false,artisticReview:'APPROVED_EXISTING_WARRIOR_ATTACK',weaponOverlay:false,reuseEvidence:'Actual four native strips visually inspected; closed-fist physical punch, original approved costume and hashes preserved'};
warrior.legacyAttackSemantics='Verified closed-fist unarmed punch; all four approved clips reused directly';
registry.feedbackIsFinalConsistencyApproval=false;registry.extensionStatus='UNARMED_FIRST_FRONT_BATCH_REVIEW';json(path.join(ROOT,'characters/orc-equipment-actions-v1.json'),registry);
for(const id of ['orc-01','orc-01-squire']){const file=`characters/${id}/source/action-clips-v1/basic-unarmed/front_r/generation.json`,g=read(file);g.status='NOT_SELECTED_ASYMMETRIC_ARMOR_DRIFT';json(path.join(ROOT,file),g);}
const unused=read('characters/orc-01/source/action-clips-v2/basic-unarmed/front_r/generation.json');for(const r of unused.references)r.sha256=stamp(r.file);unused.status='NOT_SELECTED_REUSE_APPROVED_ORIGINAL_WARRIOR_PUNCH';json(path.join(ROOT,'characters/orc-01/source/action-clips-v2/basic-unarmed/front_r/generation.json'),unused);
console.log('Warrior four approved clips reused; six new front_r clips selected, Squire corrected sourcev2.');
