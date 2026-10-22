import fs from 'node:fs';
import path from 'node:path';
import {ROOT,loadCharacter,approval,hash,json,readJSON,slash} from '../src/core.mjs';
import {decode,measure} from '../src/images.mjs';
if(fs.existsSync(path.join(ROOT,'characters/orc-front-locomotion-approval-v2.json')))throw Error('Front clips are approved and production has advanced. Use verify-orc-locomotion-directions.mjs; do not downgrade reviews/counts with this historical stage verifier.');
const batches=readJSON(path.join(ROOT,'characters/orc-front-locomotion-batch-v1.json'));
const editor=readJSON(path.join(ROOT,'characters/orc-front-locomotion-editor-verification-v1.json'));
const stamp=(file,base=ROOT)=>({file:slash(file),sha256:hash(fs.readFileSync(path.resolve(base,file)))});
const normRefs=refs=>refs.map(r=>{const s=stamp(typeof r==='string'?r:r.file);if(typeof r!=='string'&&r.sha256!==s.sha256)throw Error('Input reference changed');return s;});
const all=[],classes=[];
for(const b of batches){
 const {spec,dir}=loadCharacter(b.id),base=approval(spec,dir,'base');
 if(base?.digest!==b.baseApprovalDigest||!approval(spec,dir,'concept'))throw Error(`Approval mismatch ${b.id}`);
 const metaFile=path.join(dir,'source/locomotion-front-v1/generation.json'),g=readJSON(metaFile);
 g.references=normRefs(g.references);g.sourceSha256=stamp(g.source,dir).sha256;g.promptSha256=stamp(g.promptFile,dir).sha256;
 for(const c of g.corrections){c.references=normRefs(c.references);c.sourceSha256=stamp(c.source,dir).sha256;c.promptSha256=stamp(c.promptFile,dir).sha256;}
 json(metaFile,g);
 for(const rej of ['rejected-attempt-01.json','rejected-walk-correction-01.json']){
  const file=path.join(dir,'source/locomotion-front-v1',rej);if(!fs.existsSync(file))continue;
  const r=readJSON(file);r.references=normRefs(r.references);r.sourceSha256=stamp(r.source,path.dirname(file)).sha256;r.promptSha256=stamp(r.promptFile,path.dirname(file)).sha256;json(file,r);
 }
 if(b.id==='orc-01-scout'){
  const folder=path.join(dir,'source/locomotion-front-v1');
  const crop=readJSON(path.join(folder,'walk-row-to-edit.json'));Object.assign(crop,{sourceSha256:g.sourceSha256,croppedSourceSha256:stamp('walk-row-to-edit.png',folder).sha256});json(path.join(folder,'walk-row-to-edit.json'),crop);
  const guide=readJSON(path.join(folder,'walk-roll-placement-guide.json'));Object.assign(guide,{source:'walk-row-to-edit.png',sourceSha256:crop.croppedSourceSha256,guideSha256:stamp('walk-roll-placement-guide.png',folder).sha256});json(path.join(folder,'walk-roll-placement-guide.json'),guide);
 }
 const paletteImage=decode(path.join(ROOT,b.palette)).image,palette=new Set();
 for(let i=0;i<paletteImage.data.length;i+=4)if(paletteImage.data[i+3])palette.add(paletteImage.data.subarray(i,i+3).toString('hex'));
 const assets=readJSON(path.join(dir,'assets.json')),classClips=[];
 for(const [state,count,ms] of [['Idle',4,240],['Walk',6,73]]){
  const rel=`source/animations-v1/${state}/front_r`,folder=path.join(dir,rel),clip=readJSON(path.join(folder,'clip.json')),selection=readJSON(path.join(folder,'row-selection.json'));
  const correction=g.corrections.find(c=>c.state===state),call=correction??g;
  if(stamp(selection.origin).sha256!==selection.originSha256||selection.originSha256!==call.sourceSha256||stamp('sheet.png',folder).sha256!==selection.selectedSheetSha256)throw Error('Source row/origin hashes mismatch');
  if(stamp('sheet.prompt.md',folder).sha256!==call.promptSha256)throw Error('Copied actual prompt mismatch');
  const rowAsset=assets.findLast(a=>a.kind==='source'&&a.file===`${rel}/sheet.png`);
  if(rowAsset)Object.assign(rowAsset,{provider:'Local RGBA row selection of OpenAI image_gen source',sourceKind:'Exact source-row crop, not direct generator output',originSource:call.source,originSourceSha256:call.sourceSha256,generationReferences:call.references});
  const e=editor.clips.find(e=>e.id===b.id&&e.state===state),editable=`${rel}/${state.toLowerCase()}_front_r.aseprite`;
  if(!e||e.frames!==count||e.durationMs!==ms||stamp(editable,dir).sha256!==e.editableSha256)throw Error('Editable verification evidence mismatch');
  const exportSheet=decode(path.join(ROOT,e.editorSheet)).image,exportData=readJSON(path.join(ROOT,e.editorData));
  const strip=decode(path.join(folder,'native-strip.png')).image;
  if(strip.width!==128*count||strip.height!==128||exportData.frames.length!==count)throw Error('Strip/editor frame count');
  const frames=[];
  for(let i=0;i<count;i++){
   const file=`sprites/Animations/${state}/${state.toLowerCase()}_front_r_${String(i).padStart(2,'0')}.png`,d=decode(path.join(dir,file)),m=measure(d.image);
   const a=assets.findLast(a=>a.file===file&&a.sha256===d.sha256);if(!a)throw Error('Imported provenance missing');
   const processing=readJSON(path.join(dir,a.processingReport));
   if(processing.outputSha256!==d.sha256||stamp(processing.source).sha256!==processing.sourceSha256)throw Error('Processing source/output SHA mismatch');
   if(d.colorType!==6||d.image.depth!==8||m.width!==128||m.height!==128||m.partial||m.bottom!==126)throw Error('Native contract');
   for(let p=0;p<d.image.data.length;p+=4)if(d.image.data[p+3]&&!palette.has(d.image.data.subarray(p,p+3).toString('hex')))throw Error('Palette drift');
   const f=exportData.frames[i];if(f.duration!==ms||f.frame.w!==128||f.frame.h!==128)throw Error('Editor timing/canvas mismatch');
   for(let y=0;y<128;y++){
    const row=d.image.data.subarray(y*128*4,(y+1)*128*4);
    const stripStart=(y*strip.width+i*128)*4,editorStart=((f.frame.y+y)*exportSheet.width+f.frame.x)*4;
    if(!row.equals(strip.data.subarray(stripStart,stripStart+128*4))||!row.equals(exportSheet.data.subarray(editorStart,editorStart+128*4)))throw Error('Native/strip/editor RGBA divergence');
   }
   Object.assign(a,{generationReferences:call.references,originSource:call.source,originSourceSha256:call.sourceSha256,sourceSelection:`${rel}/row-selection.json`,sourceSelectionSha256:stamp('row-selection.json',folder).sha256,sourceKind:'Exact RGBA row crop of actual image_gen source; native target-grid reconstruction',editableSource:editable,editableSourceSha256:e.editableSha256,artisticApproval:'PENDING_CREATOR_FRONT_LOCOMOTION_REVIEW'});
   const revised=path.join(dir,'source/idle-subtle-v2/generation.json');
   if(state==='Idle'&&i===2&&fs.existsSync(revised)){
    const revision=readJSON(revised);
    if(stamp(revision.source,dir).sha256!==revision.sourceSha256||stamp(revision.promptFile,dir).sha256!==revision.promptSha256)throw Error('Idle correction provenance mismatch');
    for(const ref of revision.references)if(stamp(ref.file).sha256!==ref.sha256)throw Error('Idle correction reference mismatch');
    Object.assign(a,{generationReferences:revision.references,originSource:revision.source,originSourceSha256:revision.sourceSha256,sourceKind:'image_gen chest correction + native palette finishing and local torso composition; other pixels preserved',sourceSelection:'source/idle-subtle-v2/revision.json',sourceSelectionSha256:stamp('source/idle-subtle-v2/revision.json',dir).sha256,artisticApproval:'PENDING_CREATOR_REVISED_IDLE_REVIEW'});
   }
   const partialReview=path.join(dir,'source/locomotion-front-v1/review.json');
   if(state==='Walk'&&fs.existsSync(partialReview)){
    const review=readJSON(partialReview);if(review.Walk.frames[file]!==d.sha256)throw Error('Approved Walk changed');
    a.artisticApproval='APPROVED_BY_CREATOR_FRONT_R_WALK';
   }
   frames.push({file,sha256:d.sha256,top:m.top,bottom:m.bottom,contentHeight:m.contentHeight,partialAlpha:m.partial});
  }
  if(new Set(frames.map(f=>f.sha256)).size!==count||clip.uniqueRgbaFrames!==count)throw Error('Duplicate frames');
  const bob=Math.max(...frames.map(f=>f.top))-Math.min(...frames.map(f=>f.top));if(state==='Idle'&&bob>2)throw Error('Excess Idle bob');
  const report={id:b.id,job:b.job,state,direction:'front_r',frames:count,durationMs:ms,editable,editableSha256:e.editableSha256,paletteColors:palette.size,sourceOrigin:call.source,sourceOriginSha256:call.sourceSha256,sourceRow:`${rel}/sheet.png`,sourceRowSha256:stamp('sheet.png',folder).sha256,sourcePrompt:`${rel}/sheet.prompt.md`,sourcePromptSha256:call.promptSha256,baseApprovalDigest:base.digest,uniqueFrames:true,nativeContract:'PASS',paletteSubset:'PASS',sourceProvenanceHashes:'PASS',editorRoundtrip:'ALL_RGBA_AND_DURATIONS_IDENTICAL',idleTopVariation:state==='Idle'?bob:null,frameFiles:frames};
  if(fs.existsSync(path.join(dir,'source/idle-subtle-v2/revision.json'))){
   report.artisticReview=state==='Walk'?'APPROVED_BY_CREATOR':'PENDING_CREATOR_REVISED_IDLE_REVIEW';
   if(state==='Idle')report.frameSourceOverrides={'02':'source/idle-subtle-v2/generation.json'};
  }
  classClips.push(report);all.push(report);
 }
 for(const source of [{file:g.source,sha256:g.sourceSha256},...g.corrections.map(c=>({file:c.source,sha256:c.sourceSha256}))])if(!assets.some(a=>a.kind==='source'&&a.file===source.file&&a.sha256===source.sha256))assets.push({kind:'source',...source,provider:g.provider,model:g.model,status:'LOCOMOTION_SOURCE'});
 json(path.join(dir,'assets.json'),assets);
 const result={scope:'Idle and Walk front_r ONLY; not full inventory',clips:classClips,summary:{animationFrames:10,animatedEditables:2,FAIL:0},allOtherAnimationClips:'NOT_YET_PRODUCED',artisticReview:'PENDING_CREATOR_FRONT_LOCOMOTION_REVIEW',unityIntegration:'NOT_RUN'};
 if(classClips.some(c=>c.frameSourceOverrides)){
  result.artisticReview={Walk:'APPROVED_BY_CREATOR_FRONT_R',Idle:'PENDING_CREATOR_REVISED_IDLE_REVIEW',evidence:'source/locomotion-front-v1/review.json'};
 }
 json(path.join(dir,'reports/front-locomotion-validation-v1.json'),result);
 const p=readJSON(path.join(dir,'source/production-plan.json'));Object.assign(p,{status:'FRONT_LOCOMOTION_REVIEW',completedNativePng:15,animationFrames:10,animatedEditables:2,remainingAnimationPng:82,next:'Review Idle/Walk front_r before remaining views; job actions after locomotion review'});json(path.join(dir,'source/production-plan.json'),p);
 if(classClips.some(c=>c.frameSourceOverrides)){Object.assign(p,{status:'REVISED_IDLE_REVIEW',walkFrontR:'APPROVED_BY_CREATOR',idleFrontR:'REVISED_V2_PENDING_REVIEW',next:'Review only revised Idle v2; Walk front_r already approved. Then remaining views.'});json(path.join(dir,'source/production-plan.json'),p);}
 classes.push({id:b.id,job:b.job,nativePng:15,animationFrames:10,clippaths:classClips.map(c=>({state:c.state,folder:path.dirname(c.sourceRow)}))});
}
const group=readJSON(path.join(ROOT,'characters/orc-basic-classes-plan.json'));Object.assign(group,{status:'FRONT_LOCOMOTION_REVIEW',completedVariantPng:105,completedAnimationFrames:70,remainingAnimationPng:574,nextReview:'characters/review-orc-front-locomotion-v1.html'});for(const v of group.variants)Object.assign(v,{nativeStage:'FRONT_LOCOMOTION_REVIEW',completedNativePng:15,animationFrames:10,baseApproval:'APPROVED_BY_CREATOR'});json(path.join(ROOT,'characters/orc-basic-classes-plan.json'),group);
json(path.join(ROOT,'characters/orc-front-locomotion-validation-v1.json'),{scope:'First reviewed animation batch, front_r only',classes,clips:all,summary:{newAnimationFrames:70,newAnimatedEditables:14,totalVariantNativePng:105,totalVariantEditableSources:42,FAIL:0,fullInventoryComplete:false,remainingAnimationFrames:574},baseApprovalsCurrent:true,artisticReview:'PENDING_CREATOR_FRONT_LOCOMOTION_REVIEW',unityIntegration:'NOT_RUN'});
console.log('70 native frames, 14 editable clips: contract/palette/provenance/editor RGBA+duration PASS; 105 total PNGs. Full inventory remains incomplete.');
if(all.filter(c=>c.frameSourceOverrides).length===7){
 const file=path.join(ROOT,'characters/orc-front-locomotion-validation-v1.json'),result=readJSON(file);
 result.artisticReview={WalkFrontR:'APPROVED_BY_CREATOR',IdleFrontR:'REVISED_V2_PENDING_CREATOR',evidence:'Each source/locomotion-front-v1/review.json'};json(file,result);
 group.status='REVISED_IDLE_REVIEW';group.nextReview='characters/review-orc-front-locomotion-v2.html';
 for(const v of group.variants)Object.assign(v,{nativeStage:'REVISED_IDLE_REVIEW',walkFrontR:'APPROVED_BY_CREATOR',idleFrontR:'REVISED_V2_PENDING_REVIEW'});
 json(path.join(ROOT,'characters/orc-basic-classes-plan.json'),group);
}
