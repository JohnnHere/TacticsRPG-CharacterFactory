// Immutable staging of the active V4 body+unarmed sources. No Unity writes.
import fs from 'node:fs';import path from 'node:path';
import {ROOT,inside,readJSON,json,hash,now,loadCharacter,approval,digest,expectedSlots,write,files,slash} from '../src/core.mjs';
import {planUnarmedExport} from '../src/action-export.mjs';import {decode,validate} from '../src/images.mjs';
const read=f=>readJSON(inside(ROOT,f)),stamp=f=>hash(fs.readFileSync(inside(ROOT,f)));
if(fs.existsSync(inside(ROOT,'reports/orc-production-current.json'))&&read('reports/orc-production-current.json').revision!=='aseprite-v4')throw Error('V4 discarded by creator: historical approvals cannot reactivate or export it as current production.');
const active=read('reports/orc-production-current.json'),prepared=read('reports/orc-production-v4-prepared.json'),registry=read('characters/orc-equipment-actions-v1.json');
if(read(active.applied).status!=='APPLIED')throw Error('V4 not applied');
const packages=[];
for(const p of prepared.packages){
 const {dir,spec}=loadCharacter(p.id),gates=Object.fromEntries(['concept','base','consistency'].map(g=>[g,approval(spec,dir,g)]));
 if(Object.values(gates).some(v=>!v))throw Error('Current gate absent '+p.id);
 if(validate(spec,dir,'full').summary.FAIL)throw Error('Native validation failed');
 const review=read(active.supplementReviews.find(r=>r.id===p.id).file),c=registry.characters.find(r=>r.id===p.id);
 for(const clip of review.clips){const selected=c.unarmed[clip.direction];if(JSON.stringify(clip.frames)!==JSON.stringify(selected.frames)||clip.editableSha256!==selected.editableSha256||JSON.stringify(clip.durationsMs)!==JSON.stringify(selected.durationsMs))throw Error('Supplement registry stale');}
 const action=planUnarmedExport(ROOT,p.id,review,review.clips),manifest=read(p.fork);
 const native=expectedSlots(spec).map(t=>({source:`characters/${p.id}/sprites/${t}`,path:t})).concat(action.copies.map(f=>({source:f.source,path:f.path})));
 for(const f of native)f.sha256=stamp(f.source);
 const sources=manifest.jobs.map(j=>({original:j.source,path:'Source/'+slash(path.relative(path.join(dir,'source'),inside(ROOT,j.source))),sha256:j.sourceSha256}));
 for(const s of sources)if(stamp(s.original)!==s.sha256)throw Error('Selected source changed');
 const animationClips=prepared.jobs.filter(j=>j.characterId===p.id).map(j=>({state:j.state,direction:j.direction,source:j.source,sourceSha256:stamp(j.source),frames:j.before.map((_,n)=>({path:j.targets?.[n]??`Actions/basic-unarmed/v1/${j.direction}/attack_${j.direction}_${String(n).padStart(2,'0')}.png`,durationMs:j.durationsMs[n]})),durationsMs:j.durationsMs,loop:['Idle','Walk'].includes(j.state),closingPoseRepeat:['Attack','Unarmed'].includes(j.state)}));
 for(const clip of animationClips)for(const f of clip.frames){const n=native.find(n=>n.path===f.path);if(!n)throw Error('Animation frame missing');f.sha256=n.sha256;}
 const contracts=['config/equipment-actions-v1.json','src/action-contract.mjs','src/action-export.mjs'].map(file=>({file,sha256:stamp(file)}));
 const build='aseprite-v4-'+hash(JSON.stringify({digest:digest(spec,dir,'consistency'),review,native,sources,animationClips,contracts,exporter:stamp('tools/export-orc-production-v4.mjs')})).slice(0,16);
 const dest=`dist/${p.id}/${build}`,target=`${dest}/Assets/Resources/Characters/${p.id}`;
 if(!fs.existsSync(inside(ROOT,dest))){
  for(const f of native)write(inside(ROOT,`${target}/${f.path}`),fs.readFileSync(inside(ROOT,f.source)));
  for(const s of sources)write(inside(ROOT,`${dest}/${s.path}`),fs.readFileSync(inside(ROOT,s.original)));
  json(inside(ROOT,`${dest}/source-manifest.json`),sources);
  json(inside(ROOT,`${target}/factory-actions.json`),{...action.manifest,id:p.id,build,artRevision:'aseprite-v4',hitReaction:{state:'Hit',directions:['front_r','front_l','back_r','back_l'],durationsMs:[50,100,90],loop:false,equipmentIndependent:true},legacyAttackScope:'Original Job body gesture; weapon/cast bindings not implemented'});
  json(inside(ROOT,`${target}/factory-animations.json`),{schemaVersion:1,artRevision:'aseprite-v4',clips:animationClips,timingAuthority:'Aseprite frames. Unity fixed playback has not been extended to consume these durations.'});
  json(inside(ROOT,`${target}/factory-manifest.json`),{schemaVersion:1,id:p.id,build,ppu:spec.profile.ppu,profile:spec.profile,sourceDigest:digest(spec,dir,'consistency'),gate1:gates.concept,gate2:gates.consistency,gateBase:gates.base,artRevision:'aseprite-v4',files:native.map(({path,sha256})=>({path,sha256})),supplement:'factory-actions.json',animationTiming:'factory-animations.json',runtimeImplemented:false,runtimeRegistration:'REQUIRES_EXTENSION: Orc registry, equipment action selection, variable frame timing; Gate3 NOT_RUN'});
  json(inside(ROOT,`${dest}/character.json`),spec);json(inside(ROOT,`${dest}/reviews.json`),read(`characters/${p.id}/reviews.json`));json(inside(ROOT,`${dest}/v4-approval.json`),read(active.approval));
  write(inside(ROOT,`${dest}/Authoring/propagate-orc-v4.lua`),fs.readFileSync(inside(ROOT,'tools/aseprite/propagate-orc-v4.lua')));
  json(inside(ROOT,`${dest}/Authoring/lineage.json`),{method:prepared.artisticMethod,originalSources:prepared.jobs.filter(j=>j.characterId===p.id).map(j=>({file:j.original,sha256:j.originalSha256,directApprovedV4:j.directV4})),legacyOrigin:'Original source provenance retained; V4 is edited/reused artwork, not all art created from scratch in Aseprite',newExternalArtCalls:0});
  json(inside(ROOT,`${dest}/Authoring/contracts.json`),contracts);
  write(inside(ROOT,`${dest}/Authoring/equipment-actions-v1.json`),fs.readFileSync(inside(ROOT,'config/equipment-actions-v1.json')));
  write(inside(ROOT,`${dest}/README.md`),`# ${p.id} — Aseprite V4\n\nComplete local body and basic.unarmed staging. PNGs derived from selected .aseprite masters in Source/. Variable frame timings in factory-animations.json and factory-actions.json. Original Job attack gestures preserved; weapon/VFX/socket bindings remain pending. No Unity integration or Gate3. Review: reports/orc-production-v4/review.html in CharacterFactory.\n`);
  const inventory=files(inside(ROOT,dest)).map(f=>({path:slash(path.relative(inside(ROOT,dest),f)),sha256:hash(fs.readFileSync(f))}));json(inside(ROOT,dest+'/package-hashes.json'),inventory);
 }
 const inventory=read(dest+'/package-hashes.json');const actual=files(inside(ROOT,dest)).filter(f=>path.basename(f)!=='package-hashes.json').map(f=>({path:slash(path.relative(inside(ROOT,dest),f)),sha256:hash(fs.readFileSync(f))}));if(JSON.stringify(actual)!==JSON.stringify(inventory))throw Error('Immutable package mismatch '+p.id);
 for(const f of native)if(stamp(`${target}/${f.path}`)!==f.sha256)throw Error('Staging pixels changed');
 for(const j of manifest.jobs){for(let n=0;n<j.compare.length;n++){const actualPath=j.targets?.[n]?`${target}/${j.targets[n]}`:`${target}/Actions/basic-unarmed/v1/${prepared.jobs.find(x=>x.id===j.id).direction}/attack_${prepared.jobs.find(x=>x.id===j.id).direction}_${String(n).padStart(2,'0')}.png`;if(!decode(inside(ROOT,actualPath)).image.data.equals(decode(inside(ROOT,j.compare[n])).image.data))throw Error('Staged frame differs from source export');}}
 packages.push({id:p.id,job:p.job,path:dest,build,nativePng:native.length,editables:sources.length,animationSourceFiles:animationClips.length,unarmedFrameReferences:20,sha256Verified:true});console.log(p.id+': '+native.length+' PNGs and '+sources.length+' selected masters verified');
}
const groupHash=hash(JSON.stringify(packages)).slice(0,16),index=`dist/orc-production-v4/${groupHash}/index.html`;
write(inside(ROOT,index),`<!doctype html><meta charset="utf-8"><title>Orcs Aseprite V4</title><style>body{font:18px system-ui;margin:40px;background:#1d2430;color:#eee}a{color:#9bd0ff}li{margin:15px}</style><h1>Orcs Aseprite V4</h1><p>Oito pacotes locais, 896 PNGs e 216 fontes mestre. Corpo e ataque desarmado. Tempos por quadro nos manifestos; integração Unity e Gate3 pendentes.</p><a href="../../../reports/orc-production-v4/review.html">Comparação animada antes × V4</a><ul>${packages.map(p=>`<li><a href="../../${p.id}/${p.build}/README.md">${p.job}</a> — ${p.nativePng} PNGs, ${p.editables} fontes</li>`).join('')}</ul><a href="orcs-aseprite-v4.zip">ZIP completo</a>`);
json(inside(ROOT,'reports/orc-production-v4-export.json'),{status:'PASS',createdAt:now(),packages,index,zip:index.replace('index.html','orcs-aseprite-v4.zip'),summary:{characters:packages.length,nativePng:packages.reduce((n,p)=>n+p.nativePng,0),editables:packages.reduce((n,p)=>n+p.editables,0),animationSourceFiles:184,unarmedFrameReferences:160,FAIL:0},unityIntegration:'NOT_RUN',timingRuntime:'REQUIRES_EXTENSION'});
console.log(index);
