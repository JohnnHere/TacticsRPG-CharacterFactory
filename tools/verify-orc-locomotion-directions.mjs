import fs from 'node:fs';
import path from 'node:path';
import {ROOT,loadCharacter,approval,hash,json,readJSON,slash} from '../src/core.mjs';
import {decode,measure} from '../src/images.mjs';
if(fs.existsSync(path.join(ROOT,'characters/orc-combat-front-validation-v1.json')))throw Error('Combat assets now exist. Use verify-orc-combat-front.mjs; this historical stage assumes45 PNGs per outfit.');
const batches=readJSON(path.join(ROOT,'characters/orc-locomotion-single-view-batch-v1.json'));
const oldEditor=readJSON(path.join(ROOT,'characters/orc-front-locomotion-editor-verification-v1.json')).clips;
const newEditor=readJSON(path.join(ROOT,'characters/orc-locomotion-directions-editor-v1.json')).clips;
if(newEditor.length!==42)throw Error(`Need42 new editable clips, got${newEditor.length}`);
const stamp=file=>hash(fs.readFileSync(path.resolve(ROOT,file)));
const classes=[],clips=[];
for(const id of [...new Set(batches.map(b=>b.id))]){
 const {spec,dir}=loadCharacter(id),base=approval(spec,dir,'base');if(!base||!approval(spec,dir,'concept'))throw Error('Current base/concept gate missing');
 if(fs.readdirSync(path.join(dir,'sprites'),{recursive:true}).filter(file=>file.endsWith('.png')).length!==45)throw Error('Unexpected production PNG inventory');
 const prior=readJSON(path.join(dir,'source/locomotion-front-v1/review.json'));
 if(prior.Idle.status!=='APPROVED_BY_CREATOR'||prior.Walk.status!=='APPROVED_BY_CREATOR')throw Error('Approved front clip reviews missing');
 const assets=readJSON(path.join(dir,'assets.json')),palette=new Set(),nativePalette=decode(path.join(dir,'source/native-base-v1/front_r-native.png')).image;
 for(let p=0;p<nativePalette.data.length;p+=4)if(nativePalette.data[p+3])palette.add(nativePalette.data.subarray(p,p+3).toString('hex'));
 const classClips=[];
 for(const direction of ['front_r','front_l','back_r','back_l'])for(const [state,count,ms] of [['Idle',4,240],['Walk',6,73]]){
  const b=batches.find(b=>b.id===id&&b.direction===direction),rel=`source/${b?.animationVersion??'animations-v1'}/${state}/${direction}`,folder=path.join(dir,rel);
  const clip=readJSON(path.join(folder,'clip.json')),editor=(direction==='front_r'?oldEditor:newEditor).find(e=>e.id===id&&e.direction===direction&&e.state===state);
  const editable=`${rel}/${state.toLowerCase()}_${direction}.aseprite`;
  if(!editor||stamp(editor.editable)!==editor.editableSha256||stamp(`characters/${id}/${editable}`)!==editor.editableSha256)throw Error('Editable evidence mismatch');
  const exported=decode(path.join(ROOT,editor.editorSheet)).image,ed=readJSON(path.join(ROOT,editor.editorData)),strip=decode(path.join(folder,'native-strip.png')).image;
  let generation=null,selection=null;
  if(b){
   generation=readJSON(path.join(ROOT,b.folder,'generation.json'));selection=readJSON(path.join(folder,'row-selection.json'));
   if(base.digest!==b.baseApprovalDigest||stamp(`${b.folder}/${generation.source}`)!==generation.sourceSha256||stamp(`${b.folder}/${generation.promptFile}`)!==generation.promptSha256)throw Error('Actual source/prompt/base hash mismatch');
   for(const ref of generation.references)if(stamp(ref.file)!==ref.sha256)throw Error('Reference changed');
   if(stamp(selection.origin)!==selection.originSha256||selection.originSha256!==generation.sourceSha256||stamp(`characters/${id}/${rel}/sheet.png`)!==selection.selectedSheetSha256||stamp(`characters/${id}/${rel}/sheet.prompt.md`)!==generation.promptSha256)throw Error('Selected row/source origin mismatch');
   const sourceRel=slash(path.relative(dir,path.join(ROOT,b.folder,generation.source)));
   if(!assets.some(a=>a.kind==='source'&&a.file===sourceRel))assets.push({kind:'source',file:sourceRel,sha256:generation.sourceSha256,provider:generation.provider,model:generation.model,generationReferences:generation.references,status:'LOCOMOTION_DIRECTION_SOURCE'});
   const rowAsset=assets.findLast(a=>a.kind==='source'&&a.file===`${rel}/sheet.png`);if(rowAsset)Object.assign(rowAsset,{provider:'Local RGBA row selection of image_gen source',originSource:sourceRel,originSourceSha256:generation.sourceSha256});
  }
  if(ed.frames.length!==count||strip.width!==128*count||strip.height!==128||clip.uniqueRgbaFrames!==count)throw Error('Counts/uniqueness mismatch');
  const frames=[];
  for(let i=0;i<count;i++){
   const name=`${state.toLowerCase()}_${direction}_${String(i).padStart(2,'0')}.png`,file=`sprites/Animations/${state}/${name}`,decoded=decode(path.join(dir,file)),m=measure(decoded.image);
   if(decoded.colorType!==6||decoded.image.depth!==8||m.width!==128||m.height!==128||m.bottom!==126||m.partial)throw Error(`Native contract ${id}/${file}`);
   if(stamp(`characters/${id}/${rel}/${name}`)!==decoded.sha256)throw Error('Runtime/source divergence');
   for(let p=0;p<decoded.image.data.length;p+=4)if(decoded.image.data[p+3]&&!palette.has(decoded.image.data.subarray(p,p+3).toString('hex')))throw Error('Palette drift');
   const a=assets.findLast(a=>a.file===file&&a.sha256===decoded.sha256);if(!a)throw Error('Native import evidence missing');
   const processing=readJSON(path.join(dir,a.processingReport));if(processing.outputSha256!==decoded.sha256||stamp(processing.source)!==processing.sourceSha256)throw Error('Processing source/output mismatch');
   const frame=ed.frames[i];if(frame.duration!==ms||frame.frame.w!==128||frame.frame.h!==128)throw Error('Timing/canvas');
   for(let y=0;y<128;y++){
    const row=decoded.image.data.subarray(y*512,(y+1)*512),ss=(y*strip.width+i*128)*4,es=((frame.frame.y+y)*exported.width+frame.frame.x)*4;
    if(!row.equals(strip.data.subarray(ss,ss+512))||!row.equals(exported.data.subarray(es,es+512)))throw Error('Editor/strip/native RGBA mismatch');
   }
   if(direction==='front_r'){
    if(prior[state].frames[file]!==decoded.sha256||prior[state].editableSha256!==editor.editableSha256)throw Error('Approved front clip changed');
   }else Object.assign(a,{generationReferences:generation.references,originSource:slash(path.relative(dir,path.join(ROOT,b.folder,generation.source))),originSourceSha256:generation.sourceSha256,sourceSelection:`${rel}/row-selection.json`,sourceSelectionSha256:stamp(`characters/${id}/${rel}/row-selection.json`),sourceKind:'Actual independent image_gen pose; exact row crop, target grid reconstruction and own native palette',editableSource:editable,editableSourceSha256:editor.editableSha256,artisticApproval:'PENDING_CREATOR_LOCOMOTION_DIRECTIONS_REVIEW'});
   frames.push({file,sha256:decoded.sha256,top:m.top,bottom:m.bottom,contentHeight:m.contentHeight,partialAlpha:m.partial});
  }
  if(new Set(frames.map(f=>f.sha256)).size!==count)throw Error('Duplicate frames');
  const bob=Math.max(...frames.map(f=>f.top))-Math.min(...frames.map(f=>f.top));if(state==='Idle'&&bob>2)throw Error('Excess Idle bob');
  const result={id,job:spec.job.name,state,direction,frames:count,durationMs:ms,editable,editableSha256:editor.editableSha256,sourceRow:`${rel}/sheet.png`,sourceRowSha256:stamp(`characters/${id}/${rel}/sheet.png`),sourcePrompt:`${rel}/sheet.prompt.md`,sourceOrigin:b?`${b.folder}/${generation.source}`:'See front_r approved mixed-source provenance',paletteColors:palette.size,nativeContract:'PASS',paletteSubset:'PASS',sourceProvenanceHashes:'PASS',editorRoundtrip:'ALL_RGBA_AND_DURATIONS_IDENTICAL',artisticReview:direction==='front_r'?'APPROVED_BY_CREATOR':'PENDING_CREATOR',frameFiles:frames};classClips.push(result);clips.push(result);
 }
 json(path.join(dir,'assets.json'),assets);json(path.join(dir,'reports/locomotion-directions-v1.json'),{clips:classClips,newFrames:30,frontApprovedUnchanged:true,FAIL:0,fullInventoryComplete:false});
 const plan=readJSON(path.join(dir,'source/production-plan.json'));Object.assign(plan,{status:'LOCOMOTION_DIRECTIONS_REVIEW',completedNativePng:45,animationFrames:40,animatedEditables:8,remainingAnimationPng:52,walkFrontR:'APPROVED_BY_CREATOR',idleFrontR:'APPROVED_BY_CREATOR_V2',next:'Review new Idle/Walk front_l,back_r,back_l before job-specific combat batches'});json(path.join(dir,'source/production-plan.json'),plan);
 classes.push({id,job:spec.job.name,nativePng:45,animationFrames:40});
}
json(path.join(ROOT,'characters/orc-locomotion-directions-validation-v1.json'),{scope:'Idle and Walk four directions, seven same-individual outfits',classes,clips,summary:{newAnimationFrames:210,newAnimatedEditables:42,allLocomotionFrames:280,allAnimatedEditables:56,totalVariantNativePng:315,totalVariantEditableSources:84,approvedFrontFramesUnchanged:70,remainingAnimationFrames:364,fullInventoryComplete:false,FAIL:0},artisticReview:'New42 directional clips pending creator;14 front_r clips already approved',unityIntegration:'NOT_RUN'});
const group=readJSON(path.join(ROOT,'characters/orc-basic-classes-plan.json'));Object.assign(group,{status:'LOCOMOTION_DIRECTIONS_REVIEW',completedVariantPng:315,completedAnimationFrames:280,remainingAnimationPng:364,nextReview:'characters/review-orc-locomotion-directions-v1.html'});for(const v of group.variants)Object.assign(v,{nativeStage:'LOCOMOTION_DIRECTIONS_REVIEW',completedNativePng:45,animationFrames:40,walkFrontR:'APPROVED_BY_CREATOR',idleFrontR:'APPROVED_BY_CREATOR_V2'});json(path.join(ROOT,'characters/orc-basic-classes-plan.json'),group);
console.log('280 native frames /56 clips validated;210 new frames;70 approved front frames unchanged;315 total PNGs. Remaining364 combat frames.');
