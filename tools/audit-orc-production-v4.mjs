// Validate active production, not historical source selections or old approvals.
import fs from 'node:fs';import path from 'node:path';
import {ROOT,inside,readJSON,json,hash,now,loadCharacter,approval,expectedSlots} from '../src/core.mjs';import {decode,validate} from '../src/images.mjs';
import {verifyEditorBuild,inspectAseprite} from '../src/aseprite.mjs';import {planUnarmedExport} from '../src/action-export.mjs';
const read=f=>readJSON(inside(ROOT,f)),stamp=f=>hash(fs.readFileSync(inside(ROOT,f)));
const active=read('reports/orc-production-current.json'),manifest=read(active.manifest),prepared=read('reports/orc-production-v4-prepared.json'),registry=read('characters/orc-equipment-actions-v1.json');
const historical=read('reports/aseprite-production-manifest-v1.json');for(const j of historical.jobs)if(stamp(j.source)!==j.sourceSha256)throw Error('Historical master changed');
let comparedFrames=0,native=0,gateCount=0,supplements=0;
for(const p of prepared.packages){
 const {spec,dir}=loadCharacter(p.id);for(const g of ['concept','base','consistency']){if(!approval(spec,dir,g))throw Error(p.id+' stale '+g);gateCount++;}if(approval(spec,dir,'in-game'))throw Error('Unexpected Gate3');
 if(validate(spec,dir,'full').summary.FAIL)throw Error('Native validation failed');
 verifyEditorBuild(p.build);
 const c=registry.characters.find(c=>c.id===p.id),review=read(active.supplementReviews.find(r=>r.id===p.id).file);
 planUnarmedExport(ROOT,p.id,review,review.clips);supplements+=review.clips.length;
 const selected=manifest.jobs.filter(j=>j.characterId===p.id);
 for(const j of selected){if(stamp(j.source)!==j.sourceSha256)throw Error('Active source changed');const header=inspectAseprite(inside(ROOT,j.source));if(JSON.stringify(header.durationsMs)!==JSON.stringify(j.profile.durationsMs))throw Error('Master timing changed');
  const plan=prepared.jobs.find(x=>x.id===j.id);const frames=j.targets?.map(t=>`characters/${p.id}/sprites/${t}`)??c.unarmed[plan.direction].frames.map(f=>f.file);
  for(let i=0;i<frames.length;i++){if(!decode(inside(ROOT,frames[i])).image.data.equals(decode(inside(ROOT,j.compare[i])).image.data))throw Error('Selected PNG differs from Aseprite export');comparedFrames++;}
 }
 const prefix=p.id.replaceAll('-','_'),fallback=`characters/${p.id}/sprites/${prefix}_mvp1_static_128.png`,direction=`characters/${p.id}/sprites/Directions/${prefix}_dir_front_r.png`;
 if(!decode(inside(ROOT,fallback)).image.data.equals(decode(inside(ROOT,direction)).image.data))throw Error('Fallback mismatch');native+=expectedSlots(spec).length+(['orc-01','orc-01-brawler'].includes(p.id)?0:20);
}
const approvedV4=prepared.jobs.filter(j=>j.directV4);for(const j of approvedV4)for(let i=0;i<j.targets.length;i++){const actual=`characters/${j.characterId}/sprites/${j.targets[i]}`,ref=`characters/orc-01-aseprite-v4/source/aseprite/retouched/${j.state.toLowerCase()}/${j.state.toLowerCase()}_front_r_${String(i).padStart(2,'0')}.png`;if(!decode(inside(ROOT,actual)).image.data.equals(decode(inside(ROOT,ref)).image.data))throw Error('Approved V4 pixels changed');}
const result={status:'PASS',createdAt:now(),revision:active.revision,characters:prepared.packages.length,selectedMasters:manifest.jobs.length,originalMastersPreserved:historical.jobs.length,exportedFramesExact:comparedFrames,fallbacks:8,activeNativePng:native,currentConceptBaseConsistencyGates:gateCount,unarmedDirections:supplements,approvedV4FramesExact:8,unityIntegration:'NOT_RUN',gate3:'NOT_APPROVED',browser:read('reports/orc-production-v4-check.json')};json(inside(ROOT,'reports/aseprite-production-audit-v4.json'),result);console.log(JSON.stringify(result,null,2));
