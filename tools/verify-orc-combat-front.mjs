import fs from 'node:fs';import path from 'node:path';
import {ROOT,loadCharacter,approval,hash,json,readJSON,slash} from '../src/core.mjs';import {decode,measure} from '../src/images.mjs';
if(fs.existsSync(path.join(ROOT,'characters/orc-basic-complete-validation-v1.json')))throw Error('Complete inventory exists: run tools/verify-orc-basic-complete.mjs; do not reset progress to the partial front batch.');
const batches=readJSON(path.join(ROOT,'characters/orc-combat-front-batch-v1.json')),previous=readJSON(path.join(ROOT,'characters/orc-locomotion-directions-validation-v1.json')),editor=readJSON(path.join(ROOT,'characters/orc-combat-front-editor-v1.json')).clips;
const stamp=file=>hash(fs.readFileSync(path.resolve(ROOT,file))),classes=[],clips=[];
if(editor.length!==21)throw Error(`Need21 actual editor exports, got${editor.length}`);
for(const b of batches){
 const {spec,dir}=loadCharacter(b.id),base=approval(spec,dir,'base');if(!base||base.digest!==b.baseApprovalDigest||!approval(spec,dir,'concept'))throw Error('Concept/base gate mismatch');
 const reviewed=readJSON(path.join(dir,'source/locomotion-directions-v1/review.json'));if(reviewed.status!=='APPROVED_BY_CREATOR')throw Error('Locomotion approval missing');
 let approvedFrames=0;for(const c of previous.clips.filter(c=>c.id===b.id)){
  for(const f of c.frameFiles){if(stamp(`characters/${b.id}/${f.file}`)!==f.sha256)throw Error('Approved locomotion changed');approvedFrames++;}
  if(stamp(`characters/${b.id}/${c.editable}`)!==c.editableSha256)throw Error('Approved locomotion editable changed');
 }
 if(approvedFrames!==40||fs.readdirSync(path.join(dir,'sprites'),{recursive:true}).filter(p=>p.endsWith('.png')).length!==58)throw Error('Native inventory mismatch');
 const g=readJSON(path.join(ROOT,b.folder,'generation.json'));
 for(const call of [g,...(g.corrections??[])]){
  if(stamp(`${b.folder}/${call.source}`)!==call.sourceSha256||stamp(`${b.folder}/${call.promptFile}`)!==call.promptSha256)throw Error('Generation source/prompt mismatch');
  for(const ref of call.references)if(stamp(ref.file)!==ref.sha256)throw Error('Generation reference changed');
 }
 const palette=new Set(),pal=decode(path.join(ROOT,b.palette)).image;for(let p=0;p<pal.data.length;p+=4)if(pal.data[p+3])palette.add(pal.data.subarray(p,p+3).toString('hex'));
 const assets=readJSON(path.join(dir,'assets.json')),classClips=[];
 for(const [state,count,ms] of [['Attack',5,90],['Hit',3,80],['Defeat',5,120]]){
  const rel=`source/animations-v1/${state}/front_r`,folder=path.join(dir,rel),clip=readJSON(path.join(folder,'clip.json')),selection=readJSON(path.join(folder,'row-selection.json')),call=(g.corrections??[]).find(c=>c.state===state)??g;
  if(stamp(selection.origin)!==selection.originSha256||selection.originSha256!==call.sourceSha256||stamp(`characters/${b.id}/${rel}/sheet.png`)!==selection.selectedSheetSha256||stamp(`characters/${b.id}/${rel}/sheet.prompt.md`)!==call.promptSha256)throw Error('Row provenance mismatch');
  const e=editor.find(e=>e.id===b.id&&e.state===state),editable=`${rel}/${state.toLowerCase()}_front_r.aseprite`;
  if(!e||stamp(e.editable)!==e.editableSha256||stamp(`characters/${b.id}/${editable}`)!==e.editableSha256)throw Error('Editable SHA mismatch');
  const exported=decode(path.join(ROOT,e.editorSheet)).image,ed=readJSON(path.join(ROOT,e.editorData)),strip=decode(path.join(folder,'native-strip.png')).image;
  if(ed.frames.length!==count||clip.frames!==count||clip.uniqueRgbaFrames!==count||strip.width!==128*count||strip.height!==128||clip.loop!==false)throw Error('Clip count/strip/one-shot mismatch');
  const frames=[];
  for(let i=0;i<count;i++){
   const name=`${state.toLowerCase()}_front_r_${String(i).padStart(2,'0')}.png`,file=`sprites/Animations/${state}/${name}`,d=decode(path.join(dir,file)),m=measure(d.image);
   if(d.colorType!==6||d.image.depth!==8||m.width!==128||m.height!==128||m.partial||m.bottom!==126||stamp(`characters/${b.id}/${rel}/${name}`)!==d.sha256)throw Error('Native RGBA contract/source divergence');
   for(let p=0;p<d.image.data.length;p+=4)if(d.image.data[p+3]&&!palette.has(d.image.data.subarray(p,p+3).toString('hex')))throw Error('Palette drift');
   const a=assets.findLast(a=>a.file===file&&a.sha256===d.sha256);if(!a)throw Error('Missing import evidence');
   const processing=readJSON(path.join(dir,a.processingReport));if(processing.outputSha256!==d.sha256||stamp(processing.source)!==processing.sourceSha256)throw Error('Processing source/output mismatch');
   const f=ed.frames[i];if(f.duration!==ms||f.frame.w!==128||f.frame.h!==128)throw Error('Editor timing/canvas');
   for(let y=0;y<128;y++){const row=d.image.data.subarray(y*512,(y+1)*512),ss=(y*strip.width+i*128)*4,es=((f.frame.y+y)*exported.width+f.frame.x)*4;if(!row.equals(strip.data.subarray(ss,ss+512))||!row.equals(exported.data.subarray(es,es+512)))throw Error('Native/strip/editor RGBA mismatch');}
   Object.assign(a,{generationReferences:call.references,originSource:slash(path.relative(dir,path.join(ROOT,b.folder,call.source))),originSourceSha256:call.sourceSha256,sourceSelection:`${rel}/row-selection.json`,sourceSelectionSha256:stamp(`characters/${b.id}/${rel}/row-selection.json`),sourceKind:'Independent authored image_gen pose; exact component selection, explicit native grid and own palette, integer registration',editableSource:editable,editableSourceSha256:e.editableSha256,artisticApproval:'PENDING_CREATOR_COMBAT_FRONT_REVIEW'});
   frames.push({file,sha256:d.sha256,top:m.top,bottom:m.bottom,contentHeight:m.contentHeight,partialAlpha:m.partial});
  }
  if(new Set(frames.map(f=>f.sha256)).size!==count)throw Error('Duplicate frames');
  if(state==='Defeat'&&(frames.at(-1).contentHeight>=frames[0].contentHeight||frames.some((f,i)=>i&&f.contentHeight>frames[i-1].contentHeight+2)))throw Error('Defeat does not progressively collapse');
  const sourceRel=slash(path.relative(dir,path.join(ROOT,b.folder,call.source)));if(!assets.some(a=>a.kind==='source'&&a.file===sourceRel))assets.push({kind:'source',file:sourceRel,sha256:call.sourceSha256,provider:call.provider,model:call.model,generationReferences:call.references,status:'COMBAT_FRONT_SOURCE'});
  const rowAsset=assets.findLast(a=>a.kind==='source'&&a.file===`${rel}/sheet.png`);if(rowAsset)Object.assign(rowAsset,{provider:'Local RGBA row selection of image_gen source',originSource:sourceRel,originSourceSha256:call.sourceSha256});
  const r={id:b.id,job:b.job,state,direction:'front_r',frames:count,durationMs:ms,loop:false,action:state==='Attack'?b.action:{label:state},editable,editableSha256:e.editableSha256,sourceRow:`${rel}/sheet.png`,sourceRowSha256:selection.selectedSheetSha256,sourceOrigin:`${b.folder}/${call.source}`,sourceOriginSha256:call.sourceSha256,paletteColors:palette.size,nativeContract:'PASS',paletteSubset:'PASS',sourceProvenanceHashes:'PASS',editorRoundtrip:'ALL_RGBA_AND_DURATIONS_IDENTICAL',artisticReview:'PENDING_CREATOR',frameFiles:frames};classClips.push(r);clips.push(r);
 }
 json(path.join(dir,'assets.json'),assets);json(path.join(dir,'reports/combat-front-v1.json'),{scope:'Attack/Hit/Defeat front_r only',clips:classClips,newFrames:13,approvedLocomotionUnchanged:40,FAIL:0,fullInventoryComplete:false});
 const plan=readJSON(path.join(dir,'source/production-plan.json'));Object.assign(plan,{status:'COMBAT_FRONT_REVIEW',completedNativePng:58,animationFrames:53,animatedEditables:11,remainingAnimationPng:39,locomotion:'APPROVED_BY_CREATOR_FOUR_VIEWS',next:'Review Attack/Hit/Defeat front_r before other combat directions',weaponAssets:'SEPARATE_REQUIRES_EXTENSION',unityIntegration:'NOT_RUN'});json(path.join(dir,'source/production-plan.json'),plan);
 classes.push({id:b.id,job:b.job,action:b.action,nativePng:58,animationFrames:53});
}
json(path.join(ROOT,'characters/orc-combat-front-validation-v1.json'),{scope:'First combat batch: Attack/Hit/Defeat front_r only, seven classes',classes,clips,summary:{newAnimationFrames:91,newAnimatedEditables:21,totalVariantNativePng:406,totalVariantEditableSources:105,approvedLocomotionFramesUnchanged:280,approvedLocomotionEditablesUnchanged:56,remainingAnimationFrames:273,fullInventoryComplete:false,FAIL:0},artisticReview:'PENDING_CREATOR_COMBAT_FRONT_REVIEW',weaponsAndVfx:'Separate assets/runtime extension pending',unityIntegration:'NOT_RUN'});
const group=readJSON(path.join(ROOT,'characters/orc-basic-classes-plan.json'));Object.assign(group,{status:'COMBAT_FRONT_REVIEW',completedVariantPng:406,completedAnimationFrames:371,remainingAnimationPng:273,nextReview:'characters/review-orc-combat-front-v1.html'});for(const v of group.variants)Object.assign(v,{nativeStage:'COMBAT_FRONT_REVIEW',completedNativePng:58,animationFrames:53,locomotion:'APPROVED_BY_CREATOR_FOUR_VIEWS'});json(path.join(ROOT,'characters/orc-basic-classes-plan.json'),group);
console.log('91 combat frames/21 editable clips PASS;280 approved locomotion frames/56 editables unchanged;406 total PNGs,273 remaining.');
