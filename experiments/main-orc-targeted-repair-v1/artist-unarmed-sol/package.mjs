import fs from 'node:fs';
import crypto from 'node:crypto';
import {PNG} from 'pngjs';
const E='experiments/main-orc-targeted-repair-v1/artist-unarmed-sol',S='characters/orc-v1/source/targeted-repair-unarmed-sol-v1';
const read=p=>JSON.parse(fs.readFileSync(p)),write=(p,x)=>fs.writeFileSync(p,JSON.stringify(x,null,2)+'\n');
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const im=p=>PNG.sync.read(fs.readFileSync(p));
const same=(a,b)=>a.width===b.width&&a.height===b.height&&a.data.equals(b.data);
const inventory=read(`${E}/before-inventory.json`),old=read(`${E}/before/clip.json`),docs=read(`${E}/source-proof/document.json`);
const result={status:'PASS',productionInputsUnchanged:[],frames:[],freshSourceComparisons:0,failures:[]};
for(const r of inventory.files){const unchanged=sha(r.source)===r.sha256&&sha(r.backup)===r.sha256;result.productionInputsUnchanged.push({path:r.source,sha256:r.sha256,unchanged});if(!unchanged)result.failures.push(`Source/backup changed: ${r.source}`)}
const frames=[];
for(let i=0;i<5;i++){
 const n=String(i).padStart(2,'0'),native=`${S}/native/${n}.png`,png=`${S}/composite/${n}.png`,b=im(`${E}/before/native/${n}.png`),v=im(native),c=im(png);
 const changes=[];for(let y=0;y<128;y++)for(let x=0;x<128;x++){const j=(y*128+x)*4;if(!b.data.subarray(j,j+4).equals(v.data.subarray(j,j+4)))changes.push([x,y])}
 if(i!==3&&changes.length)result.failures.push(`Protected candidate F${i} changed`);
 const crop=Buffer.alloc(128*128*4);for(let y=0;y<128;y++)c.data.copy(crop,y*128*4,((y+64)*256+64)*4,((y+64)*256+192)*4);
 if(!v.data.equals(crop))result.failures.push(`Native/composite registration F${i}`);
 for(const [key,p]of [['before-native',`${E}/before/native/${n}.png`],['before-composite',`${E}/before/composite/${n}.png`],['candidate-native',native],['candidate-composite',png]]){
  if(!same(im(p),im(`${E}/source-proof/${key}/${n}.png`)))result.failures.push(`Fresh source mismatch ${key}/F${i}`);result.freshSourceComparisons++;
 }
 for(const doc of docs)if(doc.frames[i].durationMs!==old.durationsMs[i])result.failures.push(`Source timing mismatch ${doc.key}/F${i}`);
 result.frames.push({index:i,changedRgbaPixels:changes.length,nativeChangeBbox:changes.length?[Math.min(...changes.map(p=>p[0])),Math.min(...changes.map(p=>p[1])),Math.max(...changes.map(p=>p[0])),Math.max(...changes.map(p=>p[1]))]:null,nativeSha256:sha(native),compositeSha256:sha(png)});
 frames.push({...old.frames[i],png,sha256:sha(png),nativePng:native,nativeSha256:sha(native),phase:i===3?'candidate-visible-fist-retraction':old.frames[i].phase});
}
result.oldTrimCoordinates=[66,67,68,69,70,71].map(y=>({native:[46,y],beforeAlpha:im(`${E}/before/native/03.png`).data[(y*128+46)*4+3],candidateAlpha:im(`${S}/native/03.png`).data[(y*128+46)*4+3]}));
if(result.oldTrimCoordinates.some(p=>p.candidateAlpha))result.failures.push('Traced draft01 old sleeve trim remains');
const master=`${S}/source/unarmed-back_l-f03-retraction-composite.aseprite`,nativeMaster=`${S}/source/unarmed-back_l-f03-retraction-native.aseprite`;
const clip={schemaVersion:1,character:'orc-v1',action:'Unarmed',direction:'back_l',canvas:[256,256],nativeCanvas:[128,128],bodyOffset:[64,64],groundY:190,nativeGroundY:126,frameCount:5,durationsMs:old.durationsMs,totalDurationMs:450,loop:false,oneShot:true,weaponVisible:false,master,masterSha256:sha(master),nativeMaster,nativeMasterSha256:sha(nativeMaster),frames,technicalStatus:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',artisticApproval:'PENDING_CREATOR',integrationStatus:'ISOLATED_REPRESENTATIVE_POSE_CHECKPOINT',parentClip:'characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed/clip.json',provenance:{authoring:'programmatic local Aseprite Lua, same-view same-individual same-clip F02 gauntlet donor + local elbow clusters',script:`${E}/author_f03.lua`,scriptSha256:sha(`${E}/author_f03.lua`),wrapper:`${E}/aseprite.mjs`,wrapperSha256:sha(`${E}/aseprite.mjs`),nativeDonorTranslation:[24,25],sourceInventory:`${E}/before-inventory.json`,freshSourceProof:`${E}/verification.json`,paidGenerationCalls:0,canonicalMutation:false,claim:'Candidate retraction interpretation, not a proven repair of deleted pixels'}};
result.status=result.failures.length?'FAIL':'PASS';write(`${E}/verification.json`,result);if(result.failures.length)throw Error(result.failures.join('\n'));write(`${S}/clip.json`,clip);
console.log(JSON.stringify({status:result.status,freshSourceComparisons:result.freshSourceComparisons,frames:result.frames,originalSourceFilesPreserved:result.productionInputsUnchanged.length,masterSha256:clip.masterSha256,nativeMasterSha256:clip.nativeMasterSha256},null,2));
