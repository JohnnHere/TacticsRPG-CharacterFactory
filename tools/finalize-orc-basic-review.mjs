import fs from 'node:fs';import path from 'node:path';
import {ROOT,hash,json,readJSON} from '../src/core.mjs';
const read=f=>readJSON(path.join(ROOT,f)),stamp=f=>hash(fs.readFileSync(path.join(ROOT,f)));
const full=read('characters/orc-basic-complete-validation-v1.json'),front=read('characters/orc-combat-front-validation-v1.json');
const quote='Aprovo o combate front_r; continue as outras vistas.';
front.artisticReview='APPROVED_BY_CREATOR';front.evidence=quote;for(const c of front.clips)c.artisticReview='APPROVED_BY_CREATOR';json(path.join(ROOT,'characters/orc-combat-front-validation-v1.json'),front);
for(const c of full.classes){
 const prefix=`characters/${c.id}`,clips=full.clips.filter(r=>r.id===c.id),staticSources=read('characters/orc-directions-editor-verification-v1.json').sources.filter(s=>s.id===c.id);
 const nativeFiles=fs.readdirSync(path.join(ROOT,prefix,'sprites'),{recursive:true}).filter(f=>f.endsWith('.png')).map(f=>({file:'sprites/'+f.replaceAll('\\','/'),sha256:stamp(`${prefix}/sprites/${f}`)})).sort((a,b)=>a.file.localeCompare(b.file));
 const editables=[...staticSources.map(s=>({file:s.editable.slice(prefix.length+1),sha256:s.editableSha256})),...clips.map(r=>({file:r.editable,sha256:r.editableSha256}))];
 const fingerprint=hash(Buffer.from(JSON.stringify({nativeFiles,editables})));
 json(path.join(ROOT,prefix,'source/complete-v1/review.json'),{status:'PENDING_CREATOR_COMPLETE_REVIEW',preview:'characters/review-orc-basic-complete-v1.html',scope:'Body/clothing: four static views and Idle/Walk/Attack/Hit/Defeat in four views',candidateFingerprint:fingerprint,nativeFiles,editables,clips:clips.map(r=>({state:r.state,direction:r.direction,previousArtisticReview:r.artisticReview,frames:Object.fromEntries(r.frameFiles.map(f=>[f.file,f.sha256])),editable:r.editable,editableSha256:r.editableSha256})),notIncluded:['Independent weapon/projectile/VFX assets','Runtime overlays/casts/shooting extensions','Unity integration and Gate3']});
 json(path.join(ROOT,prefix,'source/complete-v1/reuse.json'),{sourceCharacter:'orc-01',individual:'SAME_INDIVIDUAL',REUSE_DIRECT:['Approved concept and four-view native bases','Own-outfit47/48-color palette','Approved40 locomotion frames and13 front combat frames, bytes unchanged','128px canvas, ground126, timing, naming, editor writer and verified extraction pipeline'],REUSE_ADAPTED:clips.filter(r=>r.direction==='back_l'&&r.state==='Attack'&&c.id!=='orc-01-archer').map(r=>({component:r.state+'/'+r.direction,evidence:r.sourceOrigin,adaptation:'New image_gen clothing rendering from the valid Squire motion reference where applicable; no assumed shared body layer',validation:'Actual independent drawings, own palette, editor RGBA and durations verified; creator consistency pending'})),CREATE_NEW:'273 directional combat poses across seven outfits; exact generated source selection and reference hashes recorded per frame',REQUIRES_EXTENSION:['Layered clothing runtime','Independent weapons/projectiles/VFX','Synchronized casting/shooting and UnitVisuals integration'],risk:'Flattened raster cels; AI motion-reference reuse does not guarantee pixel-identical anatomy or a clothing rig'});
}
const selected=new Map(full.clips.filter(c=>c.direction!=='front_r'&&['Attack','Hit','Defeat'].includes(c.state)).map(c=>[c.sourceOrigin,true]));
const calls=new Map();
for(const c of full.classes){
 const source=path.join(ROOT,'characters',c.id,'source');
 for(const rel of fs.readdirSync(source,{recursive:true}).filter(f=>/combat-directions-v[12]/.test(f)&&(/(^|[\\/])generation\.json$/.test(f)||f.endsWith('.generation.json')))){
  const file=path.join(source,rel),g=readJSON(file);if(!g.source||!g.promptFile)continue;const folder=path.dirname(file),sourceFile=path.join(folder,g.source),prompt=path.join(folder,g.promptFile);if(!fs.existsSync(sourceFile))continue;
  g.sourceSha256=hash(fs.readFileSync(sourceFile));g.promptSha256=hash(fs.readFileSync(prompt));for(const r of g.references??[])r.sha256=stamp(r.file);json(file,g);
  const origin=path.relative(ROOT,sourceFile).replaceAll('\\','/');calls.set(origin,{id:c.id,direction:g.direction,source:origin,sha256:g.sourceSha256,prompt:path.relative(ROOT,prompt).replaceAll('\\','/'),promptSha256:g.promptSha256,references:g.references,provider:g.provider,model:g.model,selection:selected.has(origin)?'USED_IN_NATIVE_CANDIDATE':'NOT_SELECTED_FOR_ANY_NATIVE_FRAME'});
 }
}
json(path.join(ROOT,'characters/orc-combat-directions-generation-audit-v1.json'),{actualReturnedCalls:calls.size,calls:[...calls.values()],notReturned:{initialInterruptedBatch:'Only six actual returned images from initial21 requests are recorded; canceled calls have no fabricated output',brawlerHandV3:'Tool rejected generated output (other); no source was returned; succeeded with the distinct Squire-reference clothing adaptation prompt'},creatorApproval:'PENDING_COMPLETE_REVIEW'});
console.log('Seven complete review candidates with97 PNG/24 active editables fingerprinted; actual generation calls audited.');
