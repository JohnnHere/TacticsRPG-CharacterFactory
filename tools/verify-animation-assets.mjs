import fs from 'node:fs';
import path from 'node:path';
import {PNG} from 'pngjs';
import {loadCharacter,expectedSlots,approval,hash,readJSON,json,slash} from '../src/core.mjs';
import {decode,measure} from '../src/images.mjs';
const id=process.argv[2]??'orc-01';
const {dir,spec}=loadCharacter(id),assets=readJSON(path.join(dir,'assets.json'));
const dirs=['front_r','front_l','back_r','back_l'];
const paletteImage=decode(path.join(dir,'sprites',`${id.replaceAll('-','_')}_mvp1_static_128.png`)).image;
const palette=new Set();for(let i=0;i<paletteImage.data.length;i+=4)if(paletteImage.data[i+3])palette.add(paletteImage.data.subarray(i,i+3).toString('hex'));
const files=expectedSlots(spec),clips=[];
if(!approval(spec,dir,'concept')||!approval(spec,dir,'base'))throw Error('Approved concept/base hash mismatch');
for(const file of files){
  const decoded=decode(path.join(dir,'sprites',file)),m=measure(decoded.image);
  if(m.width!==128||m.height!==128||m.bottom!==126||m.partial||decoded.colorType!==6)throw Error(`Native contract violation ${file}`);
  for(let i=0;i<decoded.image.data.length;i+=4)if(decoded.image.data[i+3]&&!palette.has(decoded.image.data.subarray(i,i+3).toString('hex')))throw Error(`Palette drift ${file}`);
}
for(const [state,count]of Object.entries(spec.profile.counts))for(const direction of dirs){
  const prefix=state.toLowerCase()+'_'+direction;
  const records=Array.from({length:count},(_,i)=>{
    const file=`sprites/Animations/${state}/${prefix}_${String(i).padStart(2,'0')}.png`,p=path.join(dir,file);
    const sha256=hash(fs.readFileSync(p));const a=assets.findLast(a=>a.file===file&&a.sha256===sha256);
    if(!a?.generationPromptFile||!a.processingReport)throw Error(`Provenance missing ${file}`);
    if(hash(fs.readFileSync(path.join(dir,a.generationPromptFile)))!==a.generationPromptSha256)throw Error(`Prompt changed ${file}`);
    const processing=readJSON(path.join(dir,a.processingReport));
    if(processing.outputSha256!==sha256)throw Error(`Processing/output hash mismatch ${file}`);
    return{file,sha256,processingReport:a.processingReport,...measure(decode(p).image)};
  });
  if(new Set(records.map(r=>r.sha256)).size!==count)throw Error(`Duplicate native frame ${state}/${direction}`);
  const source=path.dirname(path.join(dir,records[0].processingReport));
  const sheet=PNG.sync.read(fs.readFileSync(path.join(source,'native-strip.png')));
  const roundtrip=PNG.sync.read(fs.readFileSync(`tmp/editor-${prefix}.png`));
  if(sheet.width!==128*count||sheet.height!==128||roundtrip.width!==sheet.width||roundtrip.height!==128||!sheet.data.equals(roundtrip.data))throw Error(`Editable RGBA roundtrip failed ${state}/${direction}`);
  const editor=readJSON(`tmp/editor-${prefix}.json`),expectedMs={Idle:240,Walk:73,Attack:90,Hit:80,Defeat:120}[state];
  if(editor.frames.length!==count||editor.frames.some(f=>f.duration!==expectedMs))throw Error(`Editable frame count/timing failed ${prefix}`);
  for(let i=0;i<count;i++){
    const p=decode(path.join(dir,records[i].file)).image;
    for(let y=0;y<128;y++)if(!p.data.subarray(y*128*4,(y+1)*128*4).equals(sheet.data.subarray((y*count*128+i*128)*4,(y*count*128+(i+1)*128)*4)))throw Error(`Sprite/strip divergence ${prefix}/${i}`);
  }
  if(state==='Defeat'&&(records.at(-1).contentHeight>40||records.some((r,i)=>i&&r.contentHeight>records[i-1].contentHeight)))throw Error(`Collapse progression invalid ${direction}`);
  if(state==='Idle'&&Math.max(...records.map(r=>r.top))-Math.min(...records.map(r=>r.top))>2)throw Error(`Idle bob ${direction}`);
  let materialPatch=null;
  if(fs.existsSync(path.join(source,'material-finishing.json'))){
    for(const record of records){
      const report=readJSON(path.join(dir,record.processingReport)),target=decode(path.join(dir,record.file)).image;
      const prior=decode(path.join(source,'before-material-finishing',path.basename(record.file))).image;
      const replay=Buffer.from(prior.data);
      for(const patch of report.nativeMaterialFinishing.pixelPatch){const i=(patch.y*128+patch.x)*4;for(let c=0;c<3;c++)replay[i+c]=patch.after[c];}
      if(!replay.equals(target.data))throw Error(`Native material patch replay failed ${record.file}`);
    }
    materialPatch='RGB patch replay identical; pose/alpha unchanged';
  }
  clips.push({state,direction,count,source:slash(path.relative(dir,source)),editable:`${prefix}.aseprite`,editableSha256:hash(fs.readFileSync(path.join(source,prefix+'.aseprite'))),editorRgbaRoundtrip:'PASS',editorDurationMs:expectedMs,paletteSubset:'PASS',provenanceHashes:'PASS',materialPatch,frames:records.map(r=>({file:r.file,sha256:r.sha256,contentHeight:r.contentHeight,bottom:r.bottom,partial:r.partial}))});
}
const report={character:id,nativePng:files.length,animationFrames:clips.reduce((n,c)=>n+c.count,0),editableClips:clips.length,paletteColors:palette.size,conceptApprovalCurrent:true,baseApprovalCurrent:true,clips,creatorConsistencyReview:approval(spec,dir,'consistency')?'APPROVED_BY_CREATOR':'PENDING',unityPlayMode:'NOT_RUN'};
json(path.join(dir,'reports/animation-assets-verification.json'),report);
console.log(JSON.stringify({nativePng:report.nativePng,animationFrames:report.animationFrames,editableClips:report.editableClips,paletteColors:report.paletteColors,editorRoundtrip:'20/20 RGBA identical',provenance:'PASS',unityPlayMode:'NOT_RUN'},null,2));
