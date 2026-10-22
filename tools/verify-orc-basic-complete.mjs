import fs from 'node:fs';import path from 'node:path';
import {ROOT,loadCharacter,approval,hash,json,readJSON,slash} from '../src/core.mjs';
import {decode,measure} from '../src/images.mjs';
const read=f=>readJSON(path.resolve(ROOT,f)),stamp=f=>hash(fs.readFileSync(path.resolve(ROOT,f)));
const batches=read('characters/orc-combat-directions-batch-v2.json');
const prior=[...read('characters/orc-locomotion-directions-validation-v1.json').clips,...read('characters/orc-combat-front-validation-v1.json').clips];
const editors=['orc-front-locomotion-editor-verification-v1','orc-locomotion-directions-editor-v1','orc-combat-front-editor-v1','orc-combat-directions-editor-v1'].flatMap(n=>read(`characters/${n}.json`).clips);
if(editors.length!==140)throw Error(`Need140 editor exports, found${editors.length}`);
const staticSources=read('characters/orc-directions-editor-verification-v1.json').sources;
if(staticSources.length!==28)throw Error('Need28 static editable sources');
for(const s of staticSources)if(stamp(s.editable)!==s.editableSha256)throw Error('Approved static editable changed');
for(const c of prior){for(const f of c.frameFiles)if(stamp(`characters/${c.id}/${f.file}`)!==f.sha256)throw Error('Approved native changed');if(stamp(`characters/${c.id}/${c.editable}`)!==c.editableSha256)throw Error('Approved editable changed');}
const warrior=read('characters/orc-basic-shared-source-index.json');
for(const f of [...warrior.files,...warrior.editables])if(stamp(f.file)!==f.sha256)throw Error('Approved Warrior source changed');
const classes=[],clips=[];
for(const id of [...new Set(batches.map(b=>b.id))]){
 const bs=batches.filter(b=>b.id===id),{spec,dir}=loadCharacter(id),base=approval(spec,dir,'base');
 if(!base||base.digest!==bs[0].baseApprovalDigest||!approval(spec,dir,'concept'))throw Error('Approved concept/base changed');
 if(read(`characters/${id}/source/combat-front-v1/review.json`).status!=='APPROVED_BY_CREATOR')throw Error('Front combat approval missing');
 if(fs.readdirSync(path.join(dir,'sprites'),{recursive:true}).filter(p=>p.endsWith('.png')).length!==97)throw Error(`${id}: expected97 native PNGs`);
 const assets=read(`characters/${id}/assets.json`),palette=new Set(),pal=decode(path.join(ROOT,bs[0].palette)).image;
 for(let p=0;p<pal.data.length;p+=4)if(pal.data[p+3])palette.add(pal.data.subarray(p,p+3).toString('hex'));
 for(const direction of ['front_r','front_l','back_r','back_l'])for(const [state,count,ms] of [['Idle',4,240],['Walk',6,73],['Attack',5,90],['Hit',3,80],['Defeat',5,120]]){
  const e=editors.find(e=>e.id===id&&e.state===state&&e.direction===direction);if(!e||stamp(e.editable)!==e.editableSha256)throw Error('Editor evidence mismatch');
  const editable=slash(path.relative(dir,path.join(ROOT,e.editable))),rel=slash(path.dirname(editable)),folder=path.join(dir,rel),clip=read(`${e.editable.slice(0,e.editable.lastIndexOf('/'))}/clip.json`);
  const ed=read(e.editorData),exported=decode(path.join(ROOT,e.editorSheet)).image,strip=decode(path.join(folder,'native-strip.png')).image;
  if(ed.frames.length!==count||clip.frames!==count||clip.uniqueRgbaFrames!==count||strip.width!==count*128||strip.height!==128)throw Error('Count/strip mismatch');
  const isNew=direction!=='front_r'&&['Attack','Hit','Defeat'].includes(state);let call,b,selection;
  if(isNew){
   b=bs.find(b=>b.direction===direction);const g=read(`${b.folder}/generation.json`);call=(g.corrections??[]).find(c=>c.state===state)??g;
   for(const gcall of [g,...(g.corrections??[])]){if(stamp(`${b.folder}/${gcall.source}`)!==gcall.sourceSha256||stamp(`${b.folder}/${gcall.promptFile}`)!==gcall.promptSha256)throw Error('Generation source/prompt mismatch');for(const r of gcall.references)if(stamp(r.file)!==r.sha256)throw Error('Generation reference changed');}
   selection=read(`characters/${id}/${rel}/row-selection.json`);
   if(stamp(selection.origin)!==selection.originSha256||selection.originSha256!==call.sourceSha256||stamp(`characters/${id}/${rel}/sheet.png`)!==selection.selectedSheetSha256||stamp(`characters/${id}/${rel}/sheet.prompt.md`)!==call.promptSha256)throw Error('Row provenance mismatch');
  }
  const frameFiles=[];
  for(let i=0;i<count;i++){
   const name=`${state.toLowerCase()}_${direction}_${String(i).padStart(2,'0')}.png`,file=`sprites/Animations/${state}/${name}`,d=decode(path.join(dir,file)),m=measure(d.image);
   if(d.colorType!==6||d.image.depth!==8||m.width!==128||m.height!==128||m.partial||m.bottom!==126||stamp(`characters/${id}/${rel}/${name}`)!==d.sha256)throw Error(`${id}/${name}: native RGBA/source mismatch`);
   for(let p=0;p<d.image.data.length;p+=4)if(d.image.data[p+3]&&!palette.has(d.image.data.subarray(p,p+3).toString('hex')))throw Error('Palette drift');
   const a=assets.findLast(a=>a.file===file&&a.sha256===d.sha256);if(!a)throw Error('Missing import');
   const processing=read(`characters/${id}/${a.processingReport}`);if(processing.outputSha256!==d.sha256||stamp(processing.source)!==processing.sourceSha256)throw Error('Processing source/output mismatch');
   const f=ed.frames[i];if(f.duration!==ms||f.frame.w!==128||f.frame.h!==128)throw Error('Editor timing/canvas mismatch');
   for(let y=0;y<128;y++){const row=d.image.data.subarray(y*512,(y+1)*512),ss=(y*strip.width+i*128)*4,es=((f.frame.y+y)*exported.width+f.frame.x)*4;if(!row.equals(strip.data.subarray(ss,ss+512))||!row.equals(exported.data.subarray(es,es+512)))throw Error('Native/strip/editor RGBA mismatch');}
   if(isNew)Object.assign(a,{generationReferences:call.references,originSource:slash(path.relative(dir,path.join(ROOT,b.folder,call.source))),originSourceSha256:call.sourceSha256,sourceSelection:`${rel}/row-selection.json`,sourceSelectionSha256:stamp(`characters/${id}/${rel}/row-selection.json`),sourceKind:'Independent authored image_gen pose; exact component selection, native grid, own palette and integer registration',editableSource:editable,editableSourceSha256:e.editableSha256,artisticApproval:'PENDING_CREATOR_COMPLETE_REVIEW'});
   frameFiles.push({file,sha256:d.sha256,top:m.top,bottom:m.bottom,contentHeight:m.contentHeight,partialAlpha:m.partial});
  }
  if(new Set(frameFiles.map(f=>f.sha256)).size!==count)throw Error('Duplicate poses');
  if(state==='Defeat'&&frameFiles.at(-1).contentHeight>=frameFiles[0].contentHeight)throw Error('Defeat does not collapse');
  const old=prior.find(c=>c.id===id&&c.state===state&&c.direction===direction);
  const r={...old,id,job:spec.job?.name??bs[0].job,state,direction,frames:count,durationMs:ms,loop:['Idle','Walk'].includes(state),editable,editableSha256:e.editableSha256,sourceRow:`${rel}/sheet.png`,nativeContract:'PASS',paletteSubset:'PASS',editorRoundtrip:'ALL_RGBA_AND_DURATIONS_IDENTICAL',artisticReview:isNew?'PENDING_CREATOR':'APPROVED_BY_CREATOR',frameFiles};
  if(isNew){Object.assign(r,{sourceRowSha256:selection.selectedSheetSha256,sourceOrigin:`${b.folder}/${call.source}`,sourceOriginSha256:call.sourceSha256,sourceProvenanceHashes:'PASS'});const sourceRel=slash(path.relative(dir,path.join(ROOT,b.folder,call.source)));if(!assets.some(a=>a.kind==='source'&&a.file===sourceRel))assets.push({kind:'source',file:sourceRel,sha256:call.sourceSha256,provider:call.provider,model:call.model,generationReferences:call.references,status:'COMBAT_DIRECTION_SOURCE'});const row=assets.findLast(a=>a.kind==='source'&&a.file===`${rel}/sheet.png`);if(row)Object.assign(row,{provider:'Local RGBA row selection of image_gen source',originSource:sourceRel,originSourceSha256:call.sourceSha256});}
  clips.push(r);
 }
 json(path.join(dir,'assets.json'),assets);
 const classClips=clips.filter(c=>c.id===id);json(path.join(dir,'reports/complete-v1.json'),{scope:'Body/clothing: five animation states, four independent views',clips:classClips,nativePng:97,animationFrames:92,activeEditableSources:24,FAIL:0,artisticConsistency:'PENDING_CREATOR',weaponsAndVfx:'SEPARATE_REQUIRES_EXTENSION',unityIntegration:'NOT_RUN'});
 const plan=read(`characters/${id}/source/production-plan.json`);Object.assign(plan,{status:'COMPLETE_BODY_CONSISTENCY_REVIEW',completedNativePng:97,animationFrames:92,animatedEditables:20,remainingAnimationPng:0,next:'Creator full consistency review before export',weaponAssets:'SEPARATE_REQUIRES_EXTENSION',unityIntegration:'NOT_RUN'});json(path.join(dir,'source/production-plan.json'),plan);
 classes.push({id,job:bs[0].job,action:bs[0].action,nativePng:97,animationFrames:92,activeEditableSources:24});
}
json(path.join(ROOT,'characters/orc-basic-complete-validation-v1.json'),{scope:'Seven Orc classes: complete body/clothing baseline',classes,clips,summary:{newAnimationFrames:273,newAnimatedEditables:63,totalVariantNativePng:679,totalAnimationFrames:644,totalAnimatedEditables:140,totalVariantEditableSources:168,approvedAnimationFramesUnchanged:371,approvedEditableSourcesUnchanged:105,remainingBodyAnimationFrames:0,fullBodyInventoryComplete:true,FAIL:0},warriorSourceConsistencyDigest:warrior.sourceConsistencyDigest,artisticConsistency:'PENDING_CREATOR',weaponsAndVfx:'Separate assets/runtime extensions pending',unityIntegration:'NOT_RUN'});
const group=read('characters/orc-basic-classes-plan.json');Object.assign(group,{status:'COMPLETE_BODY_CONSISTENCY_REVIEW',completedVariantPng:679,completedAnimationFrames:644,remainingAnimationPng:0,nextReview:'characters/review-orc-basic-complete-v1.html'});for(const v of group.variants)Object.assign(v,{nativeStage:'COMPLETE_BODY_CONSISTENCY_REVIEW',completedNativePng:97,animationFrames:92});json(path.join(ROOT,'characters/orc-basic-classes-plan.json'),group);
console.log('679 PNG /168 active editables PASS;371 approved animation frames and105 approved editables unchanged; full body consistency requires creator review.');
