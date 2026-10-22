import fs from 'node:fs';import path from 'node:path';import {ROOT,readJSON,json} from '../src/core.mjs';import {decode,measure} from '../src/images.mjs';import {checkFrameHashes} from '../src/action-contract.mjs';
const registry=readJSON(path.join(ROOT,'characters/orc-equipment-actions-v1.json')),contract=readJSON(path.join(ROOT,registry.contract)),results=[];let available=0,missing=0;
for(const c of registry.characters){
 for(const direction of contract.directions){
  const clip=c.unarmed[direction];if(clip.weaponOverlay!==false||clip.bodyProfile!==contract.unarmedProfile)throw Error('Unarmed must use physical body profile and no overlay');
  if(clip.status==='MISSING_BODY_CLIP'){if(clip.frames.length)throw Error('Missing clip has misleading frame inventory');missing++;results.push({id:c.id,direction,status:'MISSING_BODY_CLIP'});continue;}
  checkFrameHashes(ROOT,clip.frames);if(clip.loop!==false||clip.durationMs!==90)throw Error('Unarmed timing must match Orc contract');
  for(const f of clip.frames){const d=decode(path.join(ROOT,f.file)),m=measure(d.image);if(d.colorType!==6||d.image.depth!==8||m.width!==128||m.height!==128||m.partial||m.bottom!==126)throw Error('Unarmed native RGBA contract failed');}
  available++;results.push({id:c.id,direction,status:'NATIVE_BODY_VERIFIED',sourceStatus:clip.status,artisticReview:clip.artisticReview});
 }
}
const report={contract:registry.contract,summary:{requiredUnarmedDirections:32,availableNativeDirections:available,missingNativeDirections:missing,availableFrameReferences:available*5,missingFrames:missing*5,technicalFAIL:0,weaponBindingsProven:0,runtimeImplemented:registry.runtimeImplemented,readyForUnity:false},results,limits:['Body PNGs do not prove weapon grip/occlusion compatibility','Legacy export excludes action supplements','Creator approval is checked separately; no weapon binding or runtime approval is implied','Unity requires equipment-aware selection and explicit unarmed gameplay']};
json(path.join(ROOT,'reports/orc-equipment-readiness-v1.json'),report);console.log(JSON.stringify(report.summary,null,2));
