// Audits explicitly selected sources from immutable production source manifests.
// Historical/rejected sources are deliberately not discovered by glob.
import fs from 'node:fs';
import path from 'node:path';
import { ROOT, inside, readJSON, json, hash, loadCharacter, approval, pngFiles, slash, now } from '../src/core.mjs';
import { decode } from '../src/images.mjs';
import { inspectAseprite, exportAseprite } from '../src/aseprite.mjs';

const stamp=f=>hash(fs.readFileSync(inside(ROOT,f)));
if(fs.existsSync(inside(ROOT,'reports/orc-production-current.json'))){
  await import('./audit-orc-production-v4.mjs');
}else{
const packages=readJSON(inside(ROOT,'reports/orc-actions-export-v1.json')).packages;
const equipment=readJSON(inside(ROOT,'characters/orc-equipment-actions-v1.json'));
const manifest={schemaVersion:1,id:'orc-production-aseprite-v1',kind:'character',jobs:[]};
const protectedFiles=new Map(), fallbacks=[], reviews=[];
for(const pkg of packages) {
  const {dir,spec}=loadCharacter(pkg.id);
  for(const gate of ['concept','base','consistency'])if(!approval(spec,dir,gate))throw Error(`${pkg.id}: gate ${gate} invalido.`);
  reviews.push({id:pkg.id,sha256:stamp(`characters/${pkg.id}/reviews.json`)});
  const action=equipment.characters.find(c=>c.id===pkg.id);
  const prefix=pkg.id.replaceAll('-','_');
  for(const png of pngFiles(path.join(dir,'sprites'))) {const rel=slash(path.relative(ROOT,png));protectedFiles.set(rel,stamp(rel));}
  let index=0;
  for(const source of readJSON(inside(ROOT,pkg.path+'/source-manifest.json'))) {
    if(stamp(source.original)!==source.sha256)throw Error('Fonte selecionada alterada: '+source.original);
    protectedFiles.set(source.original,source.sha256);
    const profile={...inspectAseprite(inside(ROOT,source.original)),groundY:spec.profile.groundY,alpha:'binary',requireTransparency:true};
    const unarmed=Object.values(action.unarmed).find(c=>c.editable===source.original);
    let compare,targets;
    if(unarmed&&source.original.includes('/basic-unarmed/')) compare=unarmed.frames.map(f=>f.file);
    else {
      const clip=path.basename(source.original).match(/^(idle|walk|attack|hit|defeat)_(front_[rl]|back_[rl])\./i);
      if(clip) {const state=clip[1][0].toUpperCase()+clip[1].slice(1).toLowerCase();targets=Array.from({length:profile.frames},(_,i)=>`Animations/${state}/${state.toLowerCase()}_${clip[2]}_${String(i).padStart(2,'0')}.png`);}
      else {
        const direction=source.original.match(/(?:front[_-][rl]|back[_-][rl])/g)?.at(-1)?.replace('-','_');
        if(!direction||profile.frames!==1)throw Error('Fonte sem mapeamento: '+source.original);
        targets=[`Directions/${prefix}_dir_${direction}.png`];
      }
      compare=targets.map(t=>`characters/${pkg.id}/sprites/${t}`);
    }
    for(const file of compare)protectedFiles.set(file,stamp(file));
    manifest.jobs.push({id:`${pkg.id}-${String(index++).padStart(2,'0')}`,source:source.original,sourceSha256:source.sha256,profile,compare,...(targets?{targets}:{})});
  }
  const fallback=`characters/${pkg.id}/sprites/${prefix}_mvp1_static_128.png`,direction=`characters/${pkg.id}/sprites/Directions/${prefix}_dir_front_r.png`;
  const a=decode(inside(ROOT,fallback)).image,b=decode(inside(ROOT,direction)).image;
  if(a.width!==b.width||a.height!==b.height||!a.data.equals(b.data))throw Error('Fallback diferente da frente: '+pkg.id);
  fallbacks.push({file:fallback,sha256:stamp(fallback),equivalentTo:direction});
}
json(inside(ROOT,'reports/aseprite-production-manifest-v1.json'),manifest);
const start=performance.now();
const build=exportAseprite(manifest,{onProgress:p=>{if(p.completed%12===0||p.completed===p.total)console.log(`${p.completed}/${p.total}: ${p.id}`);}});
for(const [file,sha256] of protectedFiles)if(stamp(file)!==sha256)throw Error('Original alterado: '+file);
for(const r of reviews)if(stamp(`characters/${r.id}/reviews.json`)!==r.sha256)throw Error('Revisao alterada.');
const report={schemaVersion:1,status:'PASS',createdAt:now(),tool:build.tool,build:build.path,preview:build.path+'/preview.html',summary:{...build.summary,fallbacks: fallbacks.length,productionPng:build.summary.comparedFrames+fallbacks.length,originalFilesPreserved:protectedFiles.size,creatorReviewFilesPreserved:reviews.length},elapsedMs:Math.round(performance.now()-start),reused:build.reused,fallbacks,characterReviews:reviews,unityIntegration:'NOT_RUN',artisticApprovalsChanged:false};
json(inside(ROOT,'reports/aseprite-production-audit-v1.json'),report);console.log(JSON.stringify(report,null,2));
}
