// Prepare reviewable candidates. Source art is edited only by Aseprite Lua.
import fs from 'node:fs';import path from 'node:path';
import {ROOT,inside,readJSON,json,hash,now,loadCharacter,approval,files,slash} from '../src/core.mjs';
import {decode} from '../src/images.mjs';
import {forkEditorSources,executeAseprite,findAseprite,exportAseprite,verifyEditorBuild} from '../src/aseprite.mjs';
const read=f=>readJSON(inside(ROOT,f)),stamp=f=>hash(fs.readFileSync(inside(ROOT,f)));
const reportFile='reports/orc-production-v4-prepared.json';
if(fs.existsSync(inside(ROOT,reportFile)))throw Error('V4 already prepared: verify current report; never overwrite manual edits.');
const original=read('reports/aseprite-production-manifest-v1.json'),registry=read('characters/orc-equipment-actions-v1.json');
const evidence={at:now(),reviewer:'Criador',quote:'legal, vamos aplicar a V4 do Aseprite nas animações de todos os Orcs que criamos, para sedimentarmos as pequenas melhorias e podermos partir para as próximas implementações com uma ótima referência de arte',scope:'Approval of V4 animation study and authorization to propagate compatible retouches to all eight Orc outfits/four views; preserve individual/outfit/action; no in-game approval',type:'CREATOR_AUTHORIZED_PROPAGATION'};
const protectedFiles=new Map();
for(const j of original.jobs){if(stamp(j.source)!==j.sourceSha256)throw Error('Historical source changed: '+j.source);protectedFiles.set(j.source,j.sourceSha256);}
for(const c of registry.characters){const {spec,dir}=loadCharacter(c.id);for(const gate of ['concept','base','consistency'])if(!approval(spec,dir,gate))throw Error(c.id+' stale '+gate);
 for(const f of files(dir).filter(f=>/\.(json|png)$/.test(f)&&!f.includes(path.sep+'aseprite-history'+path.sep))){const rel=slash(path.relative(ROOT,f));if(rel.includes('/sprites/')||rel.includes('/concepts/')||rel.includes('/actions/')||['character.json','reviews.json','assets.json'].includes(path.basename(f)))protectedFiles.set(rel,stamp(rel));}
}
const snapshot='reports/orc-production-v4-before';
for(const [file,sha256]of protectedFiles){if(!file.endsWith('.aseprite')){const dest=inside(ROOT,snapshot+'/'+file);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.copyFileSync(inside(ROOT,file),dest);}if(stamp(file)!==sha256)throw Error('Changed during snapshot');}
json(inside(ROOT,snapshot+'/equipment-registry.json'),registry);
const jobs=[],allJobs=[],packages=[];
for(const c of registry.characters){
 const selected=original.jobs.filter(j=>j.compare[0].startsWith(`characters/${c.id}/`));
 const fork=forkEditorSources('reports/aseprite-production-manifest-v1.json','orc-production-v4',{characterId:c.id});
 const forked=read(fork.manifest),palette=new Set();
 for(const j of selected)for(const png of j.compare){const a=decode(inside(ROOT,png)).image.data;for(let k=0;k<a.length;k+=4)if(a[k+3])palette.add(a.subarray(k,k+3).toString('hex'));}
 const distance=h=>[0,2,4].reduce((n,k,i)=>n+(parseInt(h.slice(k,k+2),16)-[8,6,4][i])**2,0);
 const ink=[...palette].filter(h=>Math.max(...[0,2,4].map(k=>parseInt(h.slice(k,k+2),16)))<=16&&h!=='000000').sort((a,b)=>distance(a)-distance(b)||a.localeCompare(b))[0];
 for(const j of selected){
  const copy=forked.jobs.find(x=>x.id===j.id);const supplement=j.source.includes('/basic-unarmed/');
  const match=path.basename(j.source).match(/^(idle|walk|attack|hit|defeat)_(front_[rl]|back_[rl])\./i);
  if(!match){allJobs.push({...j,source:copy.source,sourceSha256:stamp(copy.source),characterId:c.id});continue;}
  const state=supplement?'Unarmed':match[1][0].toUpperCase()+match[1].slice(1).toLowerCase(),direction=match[2];
  const directV4=c.id==='orc-01'&&direction==='front_r'&&['Attack','Hit'].includes(state)?`characters/orc-01-aseprite-v4/source/aseprite/retouched/${state.toLowerCase()}.aseprite`:null;
  const directory=`characters/${c.id}/source/aseprite/orc-production-v4/clips/${state.toLowerCase()}-${direction}`;
  const returnSource=directV4?null:['Attack','Unarmed'].includes(state)?j.source:state==='Hit'?selected.find(x=>path.basename(x.source)===`attack_${direction}.aseprite`&&!x.source.includes('/basic-unarmed/')).source:null;
  const durationsMs=['Attack','Unarmed'].includes(state)?[80,110,50,90,120]:state==='Hit'?[50,100,90]:j.profile.durationsMs;
  const job={id:j.id,characterId:c.id,state,direction,original:j.source,originalSha256:j.sourceSha256,source:copy.source,directory,ink,directV4,returnSource,durationsMs,before:j.compare,targets:j.targets??null};jobs.push(job);
  allJobs.push({id:j.id,characterId:c.id,source:copy.source,profile:{...j.profile,durationsMs},compare:durationsMs.map((_,i)=>`${directory}/frames/${String(i).padStart(2,'0')}.png`),...(j.targets?{targets:j.targets}:{})});
 }
 packages.push({id:c.id,job:c.job,ink,fork:fork.manifest});
}
const plan={schemaVersion:1,result:'reports/orc-production-v4-lua.json',jobs};json(inside(ROOT,'reports/orc-production-v4-plan.json'),plan);
console.log(`Aseprite: ${jobs.length} animated sources; ${allJobs.length-jobs.length} static sources reused unchanged`);
executeAseprite(findAseprite(),['--script-param',`root=${ROOT}`,'--script-param','plan=reports/orc-production-v4-plan.json','--script',inside(ROOT,'tools/aseprite/propagate-orc-v4.lua')],300000);
const results=read(plan.result);
let changed=0,alphaChanges=0,referenceChecks=0;
for(const j of jobs){const r=results.find(x=>x.id===j.id);for(let n=0;n<j.before.length;n++){
 const before=decode(inside(ROOT,j.before[n])).image,after=decode(inside(ROOT,`${j.directory}/frames/${String(n).padStart(2,'0')}.png`)).image;
 const reference=decode(inside(ROOT,`${j.directory}/reference/${String(n).padStart(2,'0')}.png`)).image;
 if(!before.data.equals(reference.data))throw Error('Reference changed '+j.id);referenceChecks++;
 let count=0,alpha=0;for(let k=0;k<before.data.length;k+=4){if(!before.data.subarray(k,k+4).equals(after.data.subarray(k,k+4)))count++;if(before.data[k+3]!==after.data[k+3])alpha++;}
 if(count!==r.frames[n].changedPixels||alpha!==r.frames[n].changedAlphaPixels)throw Error('Delta count mismatch');
 if(!j.directV4&&!r.frames[n].canonicalReturn&&alpha)throw Error('Unplanned silhouette edit');if(count)changed++;alphaChanges+=alpha;
 }
}
for(const j of allJobs)j.sourceSha256=stamp(j.source);
json(inside(ROOT,'reports/aseprite-production-manifest-v4.json'),{schemaVersion:1,id:'orc-production-aseprite-v4',kind:'character',jobs:allJobs});
for(const p of packages){const manifest={schemaVersion:1,id:p.id+'-production-v4',kind:'character',characterId:p.id,jobs:allJobs.filter(j=>j.characterId===p.id).map(({characterId,...j})=>j)};
 json(inside(ROOT,p.fork),manifest);const build=exportAseprite(manifest,{onProgress:r=>{if(r.completed===r.total)console.log(`${p.id}: ${r.completed} sources exported`);}});verifyEditorBuild(build.path);Object.assign(p,{build:build.path,summary:build.summary});}
for(const [f,h]of protectedFiles)if(stamp(f)!==h)throw Error('Original changed while preparing: '+f);
json(inside(ROOT,reportFile),{schemaVersion:1,status:'PREPARED_NOT_APPLIED',createdAt:now(),evidence,packages,jobs,referenceChecks,changedFrames:changed,alphaChanges,protectedFiles:[...protectedFiles].map(([file,sha256])=>({file,sha256})),beforeSnapshot:snapshot,manifest:'reports/aseprite-production-manifest-v4.json',luaReport:plan.result,artisticMethod:'Approved V4 direct for Warrior front_r Attack/Hit; other animations reuse their own outfit/view, V4 near-black consolidation mapped to nearest existing own ink, action closing-pose reuse and V4 timing. Local V4 eye/material coordinates not copied to other anatomy/poses.',externalArtCalls:0,unityAssetsChanged:false});
console.log(JSON.stringify({status:'PREPARED',packages:packages.length,jobs:jobs.length,changed,referenceChecks}));
