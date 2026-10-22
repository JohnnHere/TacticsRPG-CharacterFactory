import fs from 'node:fs';
import path from 'node:path';
import {loadCharacter,inside,hash,readJSON,json,approval} from '../src/core.mjs';
const id=process.argv[2]??'orc-01',{dir,spec}=loadCharacter(id),assets=readJSON(path.join(dir,'assets.json'));
const stamp=file=>({file,sha256:hash(fs.readFileSync(inside(dir,file)))});
const refs={front_r:'front-r-native-4x.png',front_l:'front_l-native-4x.png',back_r:'back_r-native-v2-4x.png',back_l:'back_l-native-4x.png'};
const clips=[];
for(const[state,count]of Object.entries(spec.profile.counts))for(const direction of Object.keys(refs)){
  const prefix=`${state.toLowerCase()}_${direction}`,first=`sprites/Animations/${state}/${prefix}_00.png`;
  const current=assets.findLast(a=>a.file===first&&a.sha256===hash(fs.readFileSync(path.join(dir,first))));
  if(!current)throw Error('Current frame record missing');
  const folder=path.posix.dirname(current.processingReport),sheet=folder+'/sheet.png';
  let inputs=[stamp('source/pixel-grid-v1/'+refs[direction])],originSources=[],generationPrompts=[stamp(folder+'/sheet.prompt.md')],sourceKind='image_gen output';
  if(state==='Walk'&&direction==='front_r'){
    sourceKind='local chronological RGBA curation of two image_gen outputs';
    originSources=[stamp('source/animations-v1/Walk/front_r/sheet.png'),stamp('source/animations-v1/Walk/front_r/opposite-guided.png')];
    generationPrompts=[stamp('source/animations-v1/Walk/front_r/sheet.prompt.md'),stamp('source/animations-v1/Walk/front_r/opposite-guided.prompt.md')];
    inputs.push(stamp('source/animations-v1/Walk/front_r/opposite-pose-guide.png'));
  }else if(state==='Walk'){
    inputs.unshift(stamp(`source/animations-v1/Walk/${direction}/pose-guide.png`));
  }else if(state==='Attack'&&direction==='back_l'){
    inputs=[stamp('source/animations-v1/Attack/back_l/sheet.png')];
    originSources=inputs;
  }
  const editable=stamp(folder+'/'+prefix+'.aseprite');
  const finishing=fs.existsSync(path.join(dir,folder,'material-finishing.json'))?stamp(folder+'/material-finishing.json'):null;
  const frames=[];
  for(let i=0;i<count;i++){
    const file=`sprites/Animations/${state}/${prefix}_${String(i).padStart(2,'0')}.png`,currentSha=hash(fs.readFileSync(path.join(dir,file)));
    const a=assets.findLast(a=>a.file===file&&a.sha256===currentSha);
    Object.assign(a,{generationReferences:inputs.map(i=>({...i,role:'actual image_gen input; see prompt for reference/pose-guide/edit-target role'})),generationSourceKind:sourceKind,originSources,generationPromptFiles:generationPrompts,editableSource:editable.file,editableSourceSha256:editable.sha256,nativeMaterialFinishing:finishing,
      artisticApproval:approval(spec,dir,'consistency')?'APPROVED_BY_CREATOR':'PENDING_CREATOR_CONSISTENCY_REVIEW'});
    frames.push({file,sha256:currentSha,processingReport:stamp(a.processingReport)});
  }
  const sourceRecord=assets.findLast(a=>a.kind==='source'&&a.file===sheet);
  if(sourceRecord)Object.assign(sourceRecord,{provider:sourceKind==='image_gen output'?'OpenAI image_gen built-in':'Local RGBA curation of OpenAI image_gen outputs',sourceKind,originSources,generationReferences:inputs});
  clips.push({state,direction,count,sheet:stamp(sheet),sourceKind,originSources,generationReferences:inputs,generationPrompts,editable,nativeMaterialFinishing:finishing,frames});
}
const calls=readJSON(path.join(dir,'source/animations-v1/generation-calls.json'));
for(const call of calls.calls){
  call.sourceSha256=stamp(call.source).sha256;call.promptSha256=stamp(call.promptFile).sha256;
  if(call.usage.startsWith('rejected:')&&!assets.some(a=>a.kind==='source'&&a.file===call.source))assets.push({at:new Date().toISOString(),kind:'source',file:call.source,sha256:call.sourceSha256,provider:call.provider,model:call.model,generationPromptFile:call.promptFile,status:'REJECTED_VISUAL',reason:call.usage});
}
json(path.join(dir,'assets.json'),assets);
json(path.join(dir,'source/animations-v1/generation-calls.json'),calls);
json(path.join(dir,'source/animations-v1/manifest.json'),{character:id,conceptApproval:approval(spec,dir,'concept')?.digest,baseApproval:approval(spec,dir,'base')?.digest,consistencyApproval:approval(spec,dir,'consistency')?.digest??null,model:'not exposed by image_gen',generationCalls:23,sourceArt:'Newly authored image_gen poses, not resized concepts or transformed Hero sprites',processing:'Explicit target grid reconstruction, native palette/registration, documented RGB finishing',clips});
console.log(`${clips.length} clips, ${clips.reduce((n,c)=>n+c.count,0)} frames: source/prompt/editable hashes recorded`);
