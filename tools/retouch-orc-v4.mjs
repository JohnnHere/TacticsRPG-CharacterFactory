// Metadata, orchestration and read-only analysis; all art edits run in Aseprite.
import fs from 'node:fs';import path from 'node:path';
import {ROOT,hash,loadCharacter,approval} from '../src/core.mjs';
import {findAseprite,executeAseprite,exportAseprite,verifyEditorBuild} from '../src/aseprite.mjs';
import {decode,measure} from '../src/images.mjs';
const base='characters/orc-01-aseprite-v4',source=base+'/source/aseprite',out=source+'/retouched';
const read=p=>JSON.parse(fs.readFileSync(path.join(ROOT,p),'utf8'));
const save=(p,v)=>{fs.mkdirSync(path.dirname(path.join(ROOT,p)),{recursive:true});fs.writeFileSync(path.join(ROOT,p),JSON.stringify(v,null,2)+'\n');};
const stamp=p=>hash(fs.readFileSync(path.join(ROOT,p)));
const v2=read('reports/orc-refinement-candidates-v2.json');
const sources=['characters/orc-01-refinement-v2/concepts/warrior-refinement-v2.png',...v2.clips.flatMap(c=>c.after),'characters/orc-01/source/aseprite/combat-refinement-v2/Attack/attack_front_r.aseprite','characters/orc-01/source/aseprite/combat-refinement-v2/Hit/hit_front_r.aseprite'];
const before=sources.map(file=>({file,sha256:stamp(file)}));
const parent=loadCharacter('orc-01-refinement-v2');if(!approval(parent.spec,parent.dir,'concept'))throw Error('V2 concept approval is not current.');
const script=source+'/retouch-v2-to-v4.lua',executable=findAseprite();
const start=performance.now();
executeAseprite(executable,['--script-param','root='+ROOT,'--script-param','output='+path.join(ROOT,out),'--script',path.join(ROOT,script)]);
executeAseprite(executable,['--script-param','root='+ROOT,'--script',path.join(ROOT,'tools/aseprite/export-v4-working.lua')]);
const referenceCheck=executeAseprite(executable,['--script-param','root='+ROOT,'--script',path.join(ROOT,'tools/aseprite/verify-v4-reference.lua')]).stdout.trim();
if(!referenceCheck.startsWith('PASS: 9 hidden V2 reference cels'))throw Error('Preserved reference verification did not pass');
const elapsedMs=Math.round(performance.now()-start),retouch=read(out+'/retouch-report.json');
const jobs=[],clips=[],analysis=[];
for(const doc of retouch.documents){
 const native=doc.width===128;
 const compare=doc.frames.map(f=>`${out}/${doc.id}/${f.file}`);
 jobs.push({id:doc.id+'-front-r',source:out+'/'+doc.id+'.aseprite',sourceSha256:stamp(out+'/'+doc.id+'.aseprite'),profile:{width:doc.width,height:doc.height,frames:doc.frames.length,durationsMs:doc.frames.map(f=>f.durationMs),groundY:native?126:null,alpha:native?'binary':'any',requireContent:true,requireTransparency:true},compare});
 const originalFiles=native?v2.clips.find(c=>c.state.toLowerCase()===doc.id).after:[v2.concept];
 const frameAnalysis=compare.map((file,i)=>{
  const old=decode(originalFiles[i]).image,image=decode(file).image,metrics=measure(image);
  let changed=0,alphaChanged=0,opaque=0,absoluteRgbDelta=0;
  const oldPalette=new Set(),newPalette=new Set();
  for(let p=0;p<image.data.length;p+=4){
   if(old.data[p+3])oldPalette.add(old.data.subarray(p,p+3).toString('hex'));
   if(image.data[p+3]){opaque++;newPalette.add(image.data.subarray(p,p+3).toString('hex'));}
   if(!old.data.subarray(p,p+4).equals(image.data.subarray(p,p+4)))changed++;
   if(old.data[p+3]!==image.data[p+3])alphaChanged++;
   for(let k=0;k<3;k++)absoluteRgbDelta+=Math.abs(old.data[p+k]-image.data[p+k]);
  }
  if(changed!==doc.frames[i].changedPixels||alphaChanged!==doc.frames[i].changedAlphaPixels)throw Error('Aseprite pixel difference report diverges');
  const canonical=doc.frames[i].edits.canonicalNeutralReuse===true;
  if(native&&metrics.partial!==0)throw Error('Partial alpha native frame');
  if(native&&!canonical&&alphaChanged)throw Error('Unplanned native silhouette change');
  return {file,sha256:stamp(file),rgbaSha256:hash(image.data),...metrics,changedPixels:changed,alphaChanged,opaquePixels:opaque,meanRgbDelta:absoluteRgbDelta/(image.width*image.height*3),oldPaletteColors:oldPalette.size,newPaletteColors:newPalette.size,newColors:[...newPalette].filter(c=>!oldPalette.has(c)),edits:doc.frames[i].edits};
 });
 analysis.push({id:doc.id,frames:frameAnalysis});
 if(native){const c=v2.clips.find(c=>c.state.toLowerCase()===doc.id);clips.push({state:c.state,direction:'front_r',before:originalFiles,after:compare,beforeDurationsMs:c.afterDurationsMs,afterDurationsMs:doc.frames.map(f=>f.durationMs),deltas:compare.map((_,i)=>`${out}/${doc.id}/delta_${String(i).padStart(2,'0')}.png`),analysis:frameAnalysis});}
}
const manifest={schemaVersion:1,id:'orc-v2-to-v4-retouch',kind:'character',characterId:'orc-01-aseprite-v4',jobs};save(source+'/editor.json',manifest);
const build=exportAseprite(manifest);verifyEditorBuild(build.path);
const originalsChanged=before.filter(f=>stamp(f.file)!==f.sha256);if(originalsChanged.length)throw Error('V2 approved file modified');
const previous=read('reports/orc-assets-audit-v2.json');const changed=previous.protectedFiles.filter(f=>stamp(f.file)!==f.sha256);if(changed.length)throw Error('Original production changed');
const d=decode(clips[0].after[0]).image.data;
if(!decode(clips[0].after[4]).image.data.equals(d)||!decode(clips[1].after[2]).image.data.equals(d))throw Error('Neutral rest pose is not shared');
const report={status:'TECHNICAL_PASS_ART_REVIEW_PENDING',createdAt:new Date().toISOString(),masterTool:'Aseprite Steam',method:'Fork approved V2; preserve original cels in hidden reference layer; copy approved neutral into action return; local pixel retouch inside editor.',externalImageGenerationCalls:0,externalRasterEditing:0,inheritedPixels:'V2 image_gen origin retained; V4 is a retouch, not a wholly new Aseprite drawing.',script:{file:script,sha256:stamp(script)},sourceFiles:before,protectedProductionFiles:previous.protectedFiles.length,sourceFilesUnchanged:true,referenceCheck,elapsedMs,analysis,build:{path:build.path,preview:build.path+'/preview.html',summary:build.summary},sameFrameCountsAndDurations:true,canonicalNeutralExact:true,approval:'PENDING_CREATOR',UnityIntegration:'NOT_RUN'};
save('reports/orc-aseprite-retouch-v4.json',report);save(source+'/provenance.json',report);
const conceptAnalysis=analysis.find(c=>c.id==='concept');
save('reports/orc-aseprite-comparison-v4.json',{status:'PENDING_CREATOR',baseline:'V2 approved',candidate:'V4 Aseprite localized retouch of V2',concept:{before:v2.concept,after:out+'/concept/concept_front_r_00.png',delta:out+'/concept/delta_00.png',width:conceptAnalysis.frames[0].width,height:conceptAnalysis.frames[0].height,analysis:conceptAnalysis.frames[0]},clips,build:report.build,report:'reports/orc-aseprite-retouch-v4.json',scope:'Concept same resolution + Attack5/Hit3 front_r, same timings, original V2 preserved.'});
console.log(JSON.stringify({status:report.status,build:report.build,changed:analysis.map(c=>({id:c.id,frames:c.frames.map(f=>({pixels:f.changedPixels,alpha:f.alphaChanged,edits:f.edits}))})),canonicalNeutralExact:true},null,2));
