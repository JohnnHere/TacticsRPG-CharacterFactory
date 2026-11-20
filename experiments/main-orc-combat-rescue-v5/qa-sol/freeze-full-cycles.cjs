const fs=require('fs'),crypto=require('crypto');
const qa='experiments/main-orc-combat-rescue-v5/qa-sol/';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,''));
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
function timings(p){const b=fs.readFileSync(p),frames=b.readUInt16LE(6),durations=[];let off=128;for(let i=0;i<frames;i++){if(b.readUInt16LE(off+4)!==0xf1fa)throw Error('Bad Aseprite frame '+p);durations.push(b.readUInt16LE(off+8));off+=b.readUInt32LE(off);}return{path:p,frameCount:frames,durationsMs:durations,totalDurationMs:durations.reduce((a,b)=>a+b,0)};}
const cycles=[];
for(const [name,owner] of [['full-back-r-axe','body-specialist'],['full-front-r-sword','grip-specialist']]){
 const exp='experiments/main-orc-combat-rescue-v5/'+owner+'/'+name+'/',clipPath='characters/orc-v1/source/combat-rescue-v5/'+owner+'/'+name+'/clip.json',clip=read(clipPath),checkpoint=read(exp+'checkpoint.json');
 const evidence=new Map();function add(p,expected,role){if(evidence.has(p))return;const h=sha(p);if(expected&&expected!==h)throw Error('Hash mismatch '+p);evidence.set(p,{path:p,sha256:h,...(expected?{declaredSha256:expected,declaredMatches:true}:{}),role});}
 add(exp+'checkpoint.json',null,'submission checkpoint');add(exp+'report.md',null,'producer report');add(clipPath,name==='full-back-r-axe'?checkpoint.clip.sha256:checkpoint.clipSha256,'exact reviewed full clip');
 add(exp+(name==='full-back-r-axe'?'review.html':'index.html'),null,'original player opened in Chromium');
 if(name==='full-back-r-axe')add(exp+'representative.json',checkpoint.representative.sha256,'submission representative');
 for(const key of ['master','bodyMaster','nativeMaster','handMaster'])if(clip[key])add(clip[key],clip[key+'Sha256'],'saved Aseprite source');
 for(const frame of clip.frames){add(frame.png,frame.sha256,'final full256 export');add(frame.nativePng,frame.nativeSha256,'final native128 body export');if(frame.layers)for(const [layer,file]of Object.entries(frame.layers))add(file.png,file.sha256,'final '+layer+' layer');}
 let aliases=[],parentTimingMatches=null;
 if(name==='full-back-r-axe'){
  const rep=read(exp+'representative.json');for(const row of rep.acceptedKeyReuse){add(row.source.path,row.source.sha256,'previous accepted key');aliases.push({frame:row.frameIndex,byteExact:sha(row.source.path)===sha(row.export.path)});}
  add(exp+'final-sequence-diagnostic.png',null,'producer unmarked sequence diagnostic viewed');
 }else{
  add(clip.sourceParentClip,clip.sourceParentClipSha256,'protected body and timing parent');const parent=read(clip.sourceParentClip);parentTimingMatches=JSON.stringify(parent.durationsMs)===JSON.stringify(clip.durationsMs);
  for(const f of parent.frames)add(f.layers.body.png,f.layers.body.sha256,'protected parent body input');
  add(exp+'anatomy.json',null,'producer anatomical landmarks checked visually');add(exp+'all-body-source.png',null,'producer layers-off sequence viewed');add(exp+'all-final-frames.png',null,'producer unmarked final sequence viewed');add(exp+'new-grips-final.png',null,'producer final grip details viewed');
 }
 add(qa+name+'-browser-check.json',null,'independent functional Chromium playback traces; not continuous perception');
 for(const file of fs.readdirSync(qa).filter(n=>n.startsWith(name+'-F')&&n.endsWith('-chromium.png')))add(qa+file,null,'independent discrete Chromium screenshot viewed');
 const masterTiming=[...new Set(['master','bodyMaster','nativeMaster','handMaster'].map(k=>clip[k]).filter(Boolean))].map(timings);
 cycles.push({name,clip:{path:clipPath,sha256:sha(clipPath)},frameCount:clip.frameCount,durationsMs:clip.durationsMs,totalDurationMs:clip.totalDurationMs,evidenceFiles:[...evidence.values()],declaredHashMismatches:0,masterTiming,allMasterTimingsMatch:masterTiming.every(t=>JSON.stringify(t.durationsMs)===JSON.stringify(clip.durationsMs)),acceptedKeyReuse:aliases,parentTimingMatches});
}
const result={checkedAtUtc:new Date().toISOString(),scope:'Only the two specifically requested full candidate clips and their immediate protected body/key inputs; no global audit',cycles};
fs.writeFileSync(qa+'full-cycles-input-freeze.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({cycles:cycles.map(c=>({name:c.name,files:c.evidenceFiles.length,declaredHashMismatches:c.declaredHashMismatches,allMasterTimingsMatch:c.allMasterTimingsMatch,acceptedKeyReuse:c.acceptedKeyReuse,parentTimingMatches:c.parentTimingMatches})),pixelChecks:read(qa+'full-cycles-pixel-checks.json').cycles.map(c=>({name:c.cycle,rows:c.frames.length,nativeDeltas:c.frames.map(f=>f.body128CropArgbDelta),brightPixels:c.frames.map(f=>f.brightBodyPixels),parentBodyDeltas:c.frames.map(f=>f.parentBodyArgbDelta),hiddenAlpha:c.frames.filter(f=>f.hiddenFrameEquipmentNontransparentPixels!==null).map(f=>[f.frame,f.hiddenFrameEquipmentNontransparentPixels])}))},null,2));
