import fs from 'node:fs';
import path from 'node:path';
import {run} from '../src/cli.mjs';
import {ROOT,loadCharacter,approval,hash,json,readJSON} from '../src/core.mjs';
import {decode,measure} from '../src/images.mjs';
const batches=readJSON(path.join(ROOT,'characters/orc-native-base-batch-v1.json'));
for(const b of batches){
 const {spec,dir}=loadCharacter(b.id),gate=approval(spec,dir,'concept');
 if(gate?.digest!==b.conceptApprovalDigest)throw Error(`Concept changed: ${b.id}`);
 const source=path.join(ROOT,b.folder,'front_r-native.png'),d=decode(source),m=measure(d.image);
 if(d.colorType!==6||d.image.depth!==8||m.width!==128||m.height!==128||m.bottom!==126||m.contentHeight!==100||m.partial)throw Error(`Native contract failed: ${b.id}`);
 const prefix=b.id.replaceAll('-','_');
 const slots=[`${prefix}_mvp1_static_128.png`,`Directions/${prefix}_dir_front_r.png`];
 for(const slot of slots){
  const dest=path.join(dir,'sprites',slot);
  if(fs.existsSync(dest)){if(hash(fs.readFileSync(dest))!==d.sha256)throw Error(`Existing art preserved: ${dest}`);}
  else run(['import','--id',b.id,'--input',source,'--kind','sprite','--slot',slot,'--provider','OpenAI image_gen + local Pixel Art Fixer','--model','not exposed by image_gen; pixelfixer ef376e57e1c272633ca2dbf5f29ec3fcf6596465']);
 }
 const gPath=path.join(ROOT,b.folder,'generation.json'),g=readJSON(gPath);
 for(const ref of b.references)if(hash(fs.readFileSync(path.join(ROOT,ref.file)))!==ref.sha256)throw Error('Reference changed');
 Object.assign(g,{sourceSha256:hash(fs.readFileSync(path.join(ROOT,b.folder,'front_r-generated.png'))),nativeSha256:d.sha256,promptSha256:hash(fs.readFileSync(path.join(ROOT,b.promptFile))),processingReport:'source/native-base-v1/front_r-native.json',method:'New sprite source; explicit forced target grid, palette quantization and native registration. Not resized concept.'});
 json(gPath,g);
 const assets=readJSON(path.join(dir,'assets.json'));
 for(const slot of slots){const a=assets.findLast(a=>a.file===`sprites/${slot}`&&a.sha256===d.sha256);Object.assign(a,{generationPromptFile:g.promptFile,generationPromptSha256:g.promptSha256,generationReferences:b.references,sourceRaster:g.source,sourceSha256:g.sourceSha256,processingReport:g.processingReport,editableSource:'source/native-base-v1/front_r.aseprite',artisticApproval:'PENDING_CREATOR_BASE_REVIEW'});}
 if(!assets.some(a=>a.kind==='source'&&a.sha256===g.sourceSha256))assets.push({kind:'source',file:g.source,sha256:g.sourceSha256,provider:g.provider,model:g.model,generationPromptFile:g.promptFile,generationPromptSha256:g.promptSha256});
 json(path.join(dir,'assets.json'),assets);
 run(['validate','--id',b.id,'--stage','base']);
 fs.copyFileSync(path.join(dir,'reports/validation.json'),path.join(dir,'reports/front-r-base-validation-v1.json'));
 const report=readJSON(path.join(dir,'reports/validation.json'));if(report.summary.FAIL)throw Error(`Base validation failed: ${b.id}`);
 const plan=readJSON(path.join(dir,'source/production-plan.json'));
 Object.assign(plan,{status:'FRONT_R_BASE_REVIEW',completedNativePng:2,uniqueNativePoses:1,next:'Creator review of first native front_r base before expanding other views. Full base gate only after four directions.'});json(path.join(dir,'source/production-plan.json'),plan);
}
console.log('7 first native bases imported; 14 PNGs including fallbacks. No base artistic approval recorded.');
