import fs from 'node:fs';
import crypto from 'node:crypto';
import {PNG} from 'pngjs';
const E='experiments/main-orc-targeted-repair-v1/artist-sword-sol',S='characters/orc-v1/source/targeted-repair-sword-sol-v1';
const read=p=>JSON.parse(fs.readFileSync(p)),write=(p,x)=>fs.writeFileSync(p,JSON.stringify(x,null,2)+'\n');
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex'),im=p=>PNG.sync.read(fs.readFileSync(p));
const same=(a,b)=>a.width===b.width&&a.height===b.height&&a.data.equals(b.data);
const original=read(`${E}/before/package/clip.json`),inventory=read(`${E}/before-inventory.json`),docs=read(`${E}/source-document.json`);
const result={technicalStatus:'PASS',artisticStatus:'ARTISTIC_REVISION_REQUIRED',proposalStatus:'REJECTED_LOCAL_HYPOTHESIS',failures:[],sourceFilesVerified:0,unarmedFilesVerified:0,frames:[],freshBodyNativeComparisons:0,baselineSavedLayerComparisons:0};
for(const r of inventory.files){if(sha(r.source)!==r.sha256||sha(r.backup)!==r.sha256)result.failures.push(`Original/backup changed:${r.source}`);result.sourceFilesVerified++}
for(const r of inventory.protectedUnarmed){if(sha(r.path)!==r.sha256)result.failures.push(`Unarmed changed:${r.path}`);result.unarmedFilesVerified++}
const frames=[];
for(let i=0;i<8;i++){
 const n=String(i).padStart(2,'0'),fr=original.frames[i],out={...fr,layers:{}};
 const deltas={};
 for(const layer of original.layerOrder){
  const p=`${S}/layers/${layer}/${n}.png`,b=im(fr.layers[layer].png),v=im(p);let diffs=0;
  for(let j=0;j<v.data.length;j+=4)if(!v.data.subarray(j,j+4).equals(b.data.subarray(j,j+4)))diffs++;
  if(i!==5&&diffs)result.failures.push(`Non-target F${i}/${layer} changed`);
  if(!same(b,im(`${E}/fresh-before/layers/${layer}/${n}.png`)))result.failures.push(`Baseline fresh source F${i}/${layer} mismatch`);
  result.baselineSavedLayerComparisons++;deltas[layer]=diffs;out.layers[layer]={png:p,sha256:sha(p)};
 }
 out.png=`${S}/composite/${n}.png`;out.sha256=sha(out.png);out.nativePng=`${S}/native/${n}.png`;out.nativeSha256=sha(out.nativePng);if(i===5)out.rightGrip=[181,129];
 const body=im(out.layers.body.png),nat=im(out.nativePng),c=im(out.png),b=im(fr.png);let changes=0;
 for(let j=0;j<c.data.length;j+=4)if(!c.data.subarray(j,j+4).equals(b.data.subarray(j,j+4)))changes++;
 if(i!==5&&changes)result.failures.push(`Non-target composite F${i} changed`);
 const crop=Buffer.alloc(128*128*4);for(let y=0;y<128;y++)body.data.copy(crop,y*128*4,((y+64)*256+64)*4,((y+64)*256+192)*4);
 if(!crop.equals(nat.data))result.failures.push(`Native registration mismatch F${i}`);
 for(const [kind,want]of [['body',body],['native',nat]]){if(!same(want,im(`${E}/source-proof/${kind}/${n}.png`)))result.failures.push(`Separate saved ${kind} master F${i} mismatch`);result.freshBodyNativeComparisons++}
 // Binary-alpha exact layer recomposition is structural evidence only.
 const assembled=Buffer.alloc(256*256*4);for(const layer of original.layerOrder){const x=im(out.layers[layer].png);for(let j=0;j<x.data.length;j+=4)if(x.data[j+3])x.data.copy(assembled,j,j,j+4)}
 if(!assembled.equals(c.data))result.failures.push(`Four-layer recomposition F${i}`);
 for(const doc of docs)if(doc.frames[i].durationMs!==original.durationsMs[i])result.failures.push(`Timing changed ${doc.key}/F${i}`);
 result.frames.push({index:i,compositeChangedPixels:changes,layerChangedPixels:deltas});frames.push(out);
}
const hand=im(`${S}/layers/handFront/05.png`),weapon=im(`${S}/layers/weaponFront/05.png`);
const overlap={handFrontPixels:0,onOpaqueWeapon:0,sourceBands:{blade:0,guard:0,grip:0,pommel:0,other:0},note:'Coordinate bands only verify what is being hidden; they do not prove fingers, contact or an acceptable grip.'};
const angle=100*Math.PI/180,co=Math.cos(angle),si=Math.sin(angle);
for(let y=0;y<256;y++)for(let x=0;x<256;x++){
 const j=(y*256+x)*4;if(!hand.data[j+3])continue;overlap.handFrontPixels++;
 if(!weapon.data[j+3])continue;overlap.onOpaqueWeapon++;
 const dx=x-181,dy=y-129,u=Math.floor(co*dx+si*dy+48.5),v=Math.floor(-si*dx+co*dy+66.5);
 const band=v>=7&&v<=54?'blade':v>=55&&v<=59?'guard':v>=60&&v<=70?'grip':v>=71&&v<=78?'pommel':'other';overlap.sourceBands[band]++;
}
result.fingerOverlapDiagnostic=overlap;
result.technicalStatus=result.failures.length?'FAIL':'PASS';write(`${E}/verification.json`,result);if(result.failures.length)throw Error(result.failures.join('\n'));
const c={...original,revision:'isolated-sword-sol-F05-anatomical-hypothesis-REJECTED',master:`${S}/source/sword-f05-grip-composite.aseprite`,bodyMaster:`${S}/source/sword-f05-grip-body.aseprite`,nativeMaster:`${S}/source/sword-f05-grip-native.aseprite`,strip:null,frames,technicalStatus:'TECHNICALLY_COMPLETE',artisticStatus:'ARTISTIC_REVISION_REQUIRED',artisticApproval:'PENDING_CREATOR',proposalStatus:'REJECTED_LOCAL_HYPOTHESIS',eligibleForIntegration:false,integrationStatus:'DO_NOT_INTEGRATE',parentClip:'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json',provenance:{parent:original.provenance,authoring:'single Aseprite F05 hand/wrist redraw and sword translation(0,+8); local hypothesis rejected after source-derived whole-body and grip inspection',script:`${E}/author_f05.lua`,scriptSha256:sha(`${E}/author_f05.lua`),verification:`${E}/verification.json`,weaponSourceUnchanged:true,changedFrames:[5],newGenerationCalls:0,canonicalMutation:false}};
delete c.stripSha256;
for(const k of ['master','bodyMaster','nativeMaster'])c[`${k}Sha256`]=sha(c[k]);
write(`${S}/clip.json`,c);
console.log(JSON.stringify({technicalStatus:result.technicalStatus,artisticStatus:result.artisticStatus,sourceFilesVerified:result.sourceFilesVerified,unarmedFilesVerified:result.unarmedFilesVerified,frameChanges:result.frames,fingerOverlap:overlap},null,2));
