import fs from 'node:fs';
import path from 'node:path';
import {run} from '../src/cli.mjs';
import {ROOT,loadCharacter,inside,slash,hash,readJSON,json} from '../src/core.mjs';
import {decode,measure} from '../src/images.mjs';

const [id,state,direction,folder] = process.argv.slice(2);
const replace=process.argv.includes('--replace');
const {spec,dir} = loadCharacter(id);
const sourceDir=inside(dir,folder);
const clip=readJSON(path.join(sourceDir,'clip.json'));
if(clip.state!==state||clip.direction!==direction||clip.frames!==spec.profile.counts[state]) throw Error('Clip metadata/count mismatch');
if(clip.uniqueRgbaFrames!==clip.frames) throw Error('Duplicate animation frames');
const prompt=path.join(sourceDir,'sheet.prompt.md'),sheet=path.join(sourceDir,'sheet.png');
if(!fs.existsSync(prompt)) throw Error('Exact generation prompt missing');
const pending=[];
for(let i=0;i<clip.frames;i++){
  const file=`${state.toLowerCase()}_${direction}_${String(i).padStart(2,'0')}.png`;
  const input=path.join(sourceDir,file),decoded=decode(input),m=measure(decoded.image);
  if(decoded.colorType!==6||decoded.image.depth!==8||m.width!==128||m.height!==128||m.bottom!==126||m.partial) throw Error(`Invalid native frame ${file}`);
  const slot=`Animations/${state}/${file}`,target=inside(path.join(dir,'sprites'),slot);
  if(fs.existsSync(target)&&hash(fs.readFileSync(target))!==decoded.sha256&&!replace) throw Error(`Different frame already exists: ${slot}; preserve source and review replacement`);
  pending.push({input,file,slot,target,sha256:decoded.sha256,measurement:m});
}
if(state==='Idle'&&Math.max(...pending.map(x=>x.measurement.top))-Math.min(...pending.map(x=>x.measurement.top))>2)throw Error('Idle top variation exceeds 2px');
for(const frame of pending) if(!fs.existsSync(frame.target)||hash(fs.readFileSync(frame.target))!==frame.sha256)run(['import','--id',id,'--input',frame.input,'--kind','sprite','--slot',frame.slot,'--provider','OpenAI image_gen + local Pixel Art Fixer','--model','image model not exposed; pixelfixer ef376e57e1c272633ca2dbf5f29ec3fcf6596465',...(fs.existsSync(frame.target)?['--force']:[])]);
const assets=readJSON(path.join(dir,'assets.json'));
for(const frame of pending){
  const a=assets.findLast(x=>x.file===`sprites/${frame.slot}`&&x.sha256===frame.sha256);
  if(!a)throw Error('Imported asset record missing');
  Object.assign(a,{generationPromptFile:slash(path.relative(dir,prompt)),generationPromptSha256:hash(fs.readFileSync(prompt)),
    artSource:slash(path.relative(dir,sheet)),artSourceSha256:hash(fs.readFileSync(sheet)),
    processingReport:slash(path.relative(dir,path.join(sourceDir,frame.file.replace('.png','.json')))),
    generationReferences:[{path:`sprites/Directions/${id.replaceAll('-','_')}_dir_${direction}.png`,role:'creator-approved directional identity/proportions'}],
    promptUsage:'VERIFIED: exact image_gen prompt preserved; preparedPromptSha256 identifies factory context only',
    artisticApproval:'PENDING_CREATOR_CONSISTENCY_REVIEW'});
}
const sourceRel=slash(path.relative(dir,sheet));
if(!assets.some(a=>a.kind==='source'&&a.file===sourceRel))assets.push({at:new Date().toISOString(),kind:'source',file:sourceRel,sha256:hash(fs.readFileSync(sheet)),provider:'OpenAI image_gen built-in',model:'not exposed',generationPromptFile:slash(path.relative(dir,prompt)),status:'ANIMATION_SOURCE'});
json(path.join(dir,'assets.json'),assets);
json(path.join(sourceDir,'import.json'),{state,direction,frames:pending.map(f=>({file:`sprites/${f.slot}`,sha256:f.sha256})),creatorApproval:'PENDING_CONSISTENCY_REVIEW'});
console.log(`${state}/${direction}: ${pending.length} native frames imported with provenance`);
