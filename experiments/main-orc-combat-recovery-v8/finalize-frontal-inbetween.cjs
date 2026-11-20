const fs=require('fs'),crypto=require('crypto'),{PNG}=require('pngjs');
const base='characters/orc-v1/source/',exp='experiments/main-orc-combat-recovery-v8/';
const times=[30,65,35,50,45,35,30,35,35,100,55,80,45,90];
const phases=['rest','body-preparation','establish-grip','anticipation','coil-behind','apex-hold','apex-descent','slash-release','contact','follow-through','recoil','settle-grip','release-grip','return-to-guard'];
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const png=p=>PNG.sync.read(fs.readFileSync(p));
function bright(p){let n=0;const a=png(p).data;for(let i=0;i<a.length;i+=4)if(a[i+3]&&.2126*a[i]+.7152*a[i+1]+.0722*a[i+2]>=160)n++;return n;}
const results=[];
for(const d of ['front_r','front_l']){
 const src=base+(d==='front_r'?'combat-recovery-v7/frontal/full-front-r-sword':'combat-recovery-v8/frontal-armpit/front_l-sword');
 const out=base+'combat-recovery-v8/frontal-inbetween/'+d+'-sword';
 const c=JSON.parse(fs.readFileSync(src+'/clip.json','utf8'));const old=c.frames;
 c.frames=times.map((t,i)=>{
  const oi=i<6?i:i===6?5:i-1,ix=String(i).padStart(2,'0');const f=structuredClone(old[oi]);
  Object.assign(f,{index:i,phase:phases[i],durationMs:t,png:out+'/'+ix+'.png',nativePng:out+'/native/'+ix+'.png',weaponVisible:i>=2&&i<=11});
  f.sha256=hash(f.png);f.nativeSha256=hash(f.nativePng);
  for(const n of c.layerOrder)f.layers[n]={png:out+'/layers/'+n+'/'+ix+'.png',sha256:hash(out+'/layers/'+n+'/'+ix+'.png')};
  if(i===6){delete f.rightGrip;Object.assign(f,{grip:[d==='front_r'?127:128,101],rotationDeg:d==='front_r'?16:344,handSource:'Aseprite Lua: rigid same-view glove placed at newly authored descending forearm; no pixel blend',bodyRgbaDeltaReference:'New authored pose; not an unchanged source frame'});delete f.weaponBbox;delete f.handFrontPixels;delete f.unwrappedAngleDeg;}
  return f;
 });
 Object.assign(c,{revision:'main-orc-combat-recovery-v8-frontal-inbetween',frameCount:14,durationsMs:times,totalDurationMs:730,visibleInterval:[2,11],contactEvent:{frame:8,timeMs:325,phase:'contact',status:'CANDIDATE_VISUAL_ONLY',appliesDamage:false},technicalStatus:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',artisticApproval:'PENDING_CREATOR',eligibleForIntegration:false,checkpoint:'V8_FRONTAL_INBETWEEN_LOCAL_CANDIDATE',sourceParentClip:src+'/clip.json',sourceParentClipSha256:hash(src+'/clip.json')});
 for(const [key,file] of Object.entries({master:'source/composite.aseprite',bodyMaster:'source/body.aseprite',nativeMaster:'source/native.aseprite',handMaster:'source/hand.aseprite',strip:'native-strip.png',nativeStrip:'native-strip.png',compositeStrip:'composite-strip.png'})){c[key]=out+'/'+file;c[key+'Sha256']=hash(c[key]);}
 c.inheritedProvenance=c.provenance;c.provenance={authoring:'Programmatic Lua authorship in Aseprite: same-view torso restoration, repositioned limb clusters, explicitly contoured/shaded forearm bridge and independently rotated rigid Sword/glove. No generative AI, cross-fade or body pixel interpolation.',script:exp+'author-frontal-inbetween.lua',scriptSha256:hash(exp+'author-frontal-inbetween.lua'),editor:'Aseprite 1.3.18.6 batch --noinapp; isolated profile',newPixelLabCalls:0,runtimeImplemented:false,verification:exp+'frontal-inbetween-verification.json'};
 c.provenance.timingCorrection={authority:'Explicit creator correction: follow-through 100 ms; F05 to F06 centroid limit 45 px; inherited steps preserved',script:exp+'retime-frontal-inbetween.lua',scriptSha256:hash(exp+'retime-frontal-inbetween.lua'),savedMasterVerification:exp+'frontal-inbetween-retime-result.json',pixelsPreserved:true};
 const centers=c.frames.map(f=>{let sx=0,sy=0,n=0;for(const l of ['weaponFront','weaponBack']){const p=png(f.layers[l].png);for(let y=0;y<256;y++)for(let x=0;x<256;x++){const k=(y*256+x)*4,a=p.data;if(a[k+3]&&.2126*a[k]+.7152*a[k+1]+.0722*a[k+2]>=160){sx+=x;sy+=y;n++;}}}return n?[sx/n,sy/n]:null;});
 const steps=[];for(let i=3;i<=11;i++)steps.push({from:i-1,to:i,distance:Math.hypot(centers[i][0]-centers[i-1][0],centers[i][1]-centers[i-1][1])});
 const preserved=[];for(let i=0;i<14;i++){if(i===6)continue;let oi=i<6?i:i-1;for(const l of c.layerOrder){let a=png(c.frames[i].layers[l].png),b=png(src+'/layers/'+l+'/'+String(oi).padStart(2,'0')+'.png');if(!a.data.equals(b.data))throw Error('Source pixel drift '+d+i+l);}preserved.push(i);}
 const counts=c.frames.map(f=>bright(f.layers.body.png));const sourceCounts=old.map((_,i)=>bright(src+'/layers/body/'+String(i).padStart(2,'0')+'.png'));
 const r={direction:d,frames:14,durationsMs:times,totalDurationMs:times.reduce((a,b)=>a+b),contactTimeMs:times.slice(0,8).reduce((a,b)=>a+b),bladeCentroids:centers,bladeSteps:steps,maxBladeStep:Math.max(...steps.map(x=>x.distance)),bodyBrightPixels:counts,sourceBodyBrightPixels:sourceCounts,unchangedFramesRgba:preserved,newPoseBrightFloor:sourceCounts[5],newPoseBrightPass:counts[6]>=sourceCounts[5],noDuplicateArmedFrames:c.frames.slice(3,12).every((f,j)=>!png(f.png).data.equals(png(c.frames[j+2].png).data))};
 r.newTransitionStep=steps.find(x=>x.from===5&&x.to===6).distance;
 r.newTransitionLimitPx=45;
 r.contractPass=r.newTransitionStep<=45&&r.newPoseBrightPass&&r.noDuplicateArmedFrames&&r.totalDurationMs===730&&r.contactTimeMs===325;
 if(!r.contractPass)c.technicalStatus='NOT_VERIFIED';
 fs.writeFileSync(out+'/clip.json',JSON.stringify(c,null,2)+'\n');results.push(r);
}
fs.writeFileSync(exp+'frontal-inbetween-verification.json',JSON.stringify({status:results.every(x=>x.contractPass)?'TECHNICALLY_COMPLETE':'NOT_VERIFIED',results},null,2)+'\n');
console.log(JSON.stringify(results.map(({direction,maxBladeStep,newPoseBrightFloor,bodyBrightPixels,newPoseBrightPass,contractPass})=>({direction,maxBladeStep,newPoseBrightFloor,newBright:bodyBrightPixels[6],newPoseBrightPass,contractPass})),null,2));
