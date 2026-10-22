import fs from 'node:fs';
import path from 'node:path';
import {run} from '../src/cli.mjs';
import {ROOT,loadCharacter,approval,hash,json,readJSON,slash} from '../src/core.mjs';
import {decode,measure} from '../src/images.mjs';
const batch=readJSON(path.join(ROOT,'characters/orc-direction-batch-v1.json'));
const stamp=(file,base=ROOT)=>({file:slash(file),sha256:hash(fs.readFileSync(path.resolve(base,file)))});
const reports=[];
for(const b of batch){
 const {spec,dir}=loadCharacter(b.id),prefix=b.id.replaceAll('-','_');
 if(approval(spec,dir,'concept')?.digest!==b.conceptDigest)throw Error(`Concept changed ${b.id}`);
 const front=readJSON(path.join(dir,b.frontReview));
 if(front.decision!=='approved'||front.sha256!==b.frontSha256)throw Error('Creator front approval missing');
 for(const file of [`source/native-base-v1/front_r-native.png`,`sprites/${prefix}_mvp1_static_128.png`,`sprites/Directions/${prefix}_dir_front_r.png`])if(hash(fs.readFileSync(path.join(dir,file)))!==front.sha256)throw Error(`Approved front modified: ${b.id}`);
 const sourceMetaPath=path.join(dir,'source/directions-v1/generation.json'),g=readJSON(sourceMetaPath);
 Object.assign(g,{sourceSha256:stamp(g.source,dir).sha256,promptSha256:stamp(g.promptFile,dir).sha256});
 for(const ref of g.references)if(stamp(ref.file).sha256!==ref.sha256)throw Error('Generation reference changed');
 for(const correction of g.corrections){correction.sourceSha256=stamp(correction.source,dir).sha256;correction.promptSha256=stamp(correction.promptFile,dir).sha256;correction.references=correction.references.map(file=>typeof file==='string'?stamp(file):file);}
 const extracted=readJSON(path.join(dir,'source/directions-v1/extraction.json'));
 const paletteImage=decode(path.join(dir,'source/native-base-v1/front_r-native.png')).image;
 const palette=new Set();for(let i=0;i<paletteImage.data.length;i+=4)if(paletteImage.data[i+3])palette.add(paletteImage.data.subarray(i,i+3).toString('hex'));
 const rows=[];
 for(const e of extracted.directions){
  const input=path.resolve(e.native),d=decode(input),m=measure(d.image),slot=`Directions/${prefix}_dir_${e.direction}.png`;
  if(m.width!==128||m.height!==128||m.partial||m.bottom!==126||m.contentHeight!==100||d.colorType!==6||d.image.depth!==8||d.sha256!==e.nativeSha256)throw Error('Native contract/hash failed');
  for(let i=0;i<d.image.data.length;i+=4)if(d.image.data[i+3]&&!palette.has(d.image.data.subarray(i,i+3).toString('hex')))throw Error('Palette drift');
  const dest=path.join(dir,'sprites',slot);
  if(fs.existsSync(dest)){if(hash(fs.readFileSync(dest))!==d.sha256)throw Error(`Existing art preserved ${dest}`);}
  else run(['import','--id',b.id,'--input',input,'--kind','sprite','--slot',slot,'--provider','OpenAI image_gen + local Pixel Art Fixer','--model','not exposed by image_gen; pixelfixer ef376e57e1c272633ca2dbf5f29ec3fcf6596465']);
  rows.push({direction:e.direction,file:`sprites/${slot}`,sha256:d.sha256,source:slash(path.relative(dir,path.resolve(e.source))),sourceSha256:e.sourceSha256,processingReport:slash(path.relative(dir,path.resolve(e.processingReport))),measurement:m,editable:`source/directions-v1/${e.direction}/view.aseprite`});
 }
 const assets=readJSON(path.join(dir,'assets.json'));
 for(const r of rows){
  const correction=g.corrections.find(c=>c.direction===r.direction),promptFile=correction?.promptFile??g.promptFile;
  const a=assets.findLast(a=>a.file===r.file&&a.sha256===r.sha256);
  Object.assign(a,{generationPromptFile:promptFile,generationPromptSha256:stamp(promptFile,dir).sha256,generationReferences:correction?.references??g.references,sourceRaster:r.source,sourceSha256:r.sourceSha256,processingReport:r.processingReport,editableSource:r.editable,sourceSelection:'individually drawn view; component crop, no mirroring',artisticApproval:'PENDING_CREATOR_FOUR_VIEWS'});
 }
 for(const source of [{file:g.source,sha256:g.sourceSha256,promptFile:g.promptFile},...g.corrections.map(c=>({file:c.source,sha256:c.sourceSha256,promptFile:c.promptFile}))])if(!assets.some(a=>a.kind==='source'&&a.file===source.file&&a.sha256===source.sha256))assets.push({kind:'source',file:source.file,sha256:source.sha256,provider:g.provider,model:g.model,generationPromptFile:source.promptFile,selection:g.sourceSelectionStatus});
 json(path.join(dir,'assets.json'),assets);json(sourceMetaPath,g);
 run(['validate','--id',b.id,'--stage','directions']);
 const validation=readJSON(path.join(dir,'reports/validation.json'));if(validation.summary.FAIL)throw Error(`Direction validation failed ${b.id}`);
 json(path.join(dir,'reports/directions-validation-v1.json'),validation);
 const plan=readJSON(path.join(dir,'source/production-plan.json'));Object.assign(plan,{status:'DIRECTIONS_REVIEW',completedNativePng:5,uniqueNativePoses:4,frontBaseApproval:front,remainingAnimationPng:92,next:'Creator review of four views; register full base gate only after explicit decision, then animation batches'});json(path.join(dir,'source/production-plan.json'),plan);
 reports.push({id:b.id,job:b.job,approvedFrontSha256:front.sha256,newViews:rows,validation:validation.summary,baseGate:approval(spec,dir,'base')?'APPROVED':'PENDING_CREATOR_FOUR_VIEWS'});
}
json(path.join(ROOT,'characters/orc-directions-import-verification-v1.json'),{characters:reports,newNativeViews:21,totalNativePng:35,approvedFrontsUnchanged:true,palette:'ALL_SUBSETS_OF_OWN_APPROVED_FRONT',mirroring:'NONE',unityIntegration:'NOT_RUN'});
console.log('21 new views imported; 35 native PNGs total. All seven approved fronts unchanged.');
