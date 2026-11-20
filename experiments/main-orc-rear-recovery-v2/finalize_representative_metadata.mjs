import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { ROOT } from '../../src/core.mjs';
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT,p))).digest('hex');
const rel=(base,sub)=>`${base}/${sub}`;
const base='characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2';
const source='characters/orc-v1/source/aseprite/rear-recovery-v2';
const durations=[90,80,90,80,100,80,100,110];
const grips=[[0,0],[175,106],[166,76],[164,84],[183,92],[181,121],[170,127],[0,0]];
const angles=[0,325,20,345,60,100,135,0];
const phases=['guard-start','reach-close-fist','cock-high','load-back','slash-release','impact-follow-through','lowered-recovery','return-guard'];
const visible=[false,true,true,true,true,true,true,false];
const behind=[false,false,true,true,false,false,false,false];
const clip={schemaVersion:1,revision:'main-orc-rear-recovery-v2-representative-generated-body',id:'basic.sword-slash',character:'orc-v1',category:'Sword',state:'Attack',direction:'back_r',loop:false,oneShot:true,terminal:false,canvas:[256,256],bodyOffset:[64,64],groundY:190,nativeCanvas:[128,128],nativeGroundY:126,ppu:100,frameCount:8,durationsMs:durations,totalDurationMs:730,
 master:`${source}/composite/back_r/sword-attack-representative-v2.aseprite`,bodyMaster:`${source}/composite/back_r/sword-body-representative-v2.aseprite`,nativeMaster:`${source}/native/sword-body-representative-v2-back_r.aseprite`,strip:`${base}/native-strip.png`,layerOrder:['weaponBack','body','weaponFront','handFront'],visibleInterval:[1,6],weaponVisible:true,weaponOverlay:true,
 weapon:{id:'recruit-sword',name:'Espada do Recruta',grip:[48,66],canvas:[96,96],source:'assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png',sourceSha256:sha('assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png')},
 contactEvent:{frame:4,timeMs:340,status:'CANDIDATE_VISUAL_ONLY',appliesDamage:false},technicalStatus:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',artisticApproval:'PENDING_CREATOR',provenance:{body:'PixelLab skeleton_v3 job 31e61c4b-39ea-4932-9024-07dc9639f4f7, locally imported and refined in Aseprite',weapon:'unchanged independent Espada do Recruta PNG; transformed in Aseprite Lua',approvalDeviation:'The 3-generation call executed before explicit Root approval; see cost-provenance-ledger.json. Local use/import/refinement only authorized afterward; no further call used.'},frames:[]};
for(const [p,k] of [[clip.master,'masterSha256'],[clip.bodyMaster,'bodyMasterSha256'],[clip.nativeMaster,'nativeMasterSha256'],[clip.strip,'stripSha256']])clip[k]=sha(p);
for(let i=0;i<8;i++){
 const n=String(i).padStart(2,'0'); const f={index:i,png:rel(base,`${n}.png`),durationMs:durations[i],phase:phases[i],weaponVisible:visible[i],rightGrip:grips[i],rotationDeg:angles[i],weaponBehindBody:behind[i],layers:{}};
 for(const layer of ['weaponBack','body','weaponFront','handFront']){const p=rel(base,`layers/${layer}/${n}.png`);f.layers[layer]={png:p,sha256:sha(p)}}
 f.sha256=sha(f.png);f.nativePng=rel(base,`native/${n}.png`);f.nativeSha256=sha(f.nativePng);clip.frames.push(f);
}
const clipPath=`${base}/clip.json`;fs.writeFileSync(path.join(ROOT,clipPath),JSON.stringify(clip,null,2)+'\n');
for(const d of ['front_r','front_l']){
 const p=`characters/orc-v1/source/rear-recovery-v2/${d}/Unarmed/clip.json`;
 const c=JSON.parse(fs.readFileSync(path.join(ROOT,p),'utf8'));
 c.technicalStatus='TECHNICALLY_COMPLETE';c.artisticStatus='VISUAL_REVIEW_REQUIRED';c.artisticApproval='PENDING_CREATOR';
 c.integrationStatus='PASS_FOR_INTERNAL_INTEGRATION';c.integrationFinalQA='PENDING_ARGON';
 c.durationsMs=[80,110,50,90,120];c.totalDurationMs=450;
 c.masterSha256=sha(c.master);c.nativeMasterSha256=sha(c.nativeMaster);c.stripSha256=sha(c.strip);
 for(let i=0;i<c.frames.length;i++){const f=c.frames[i];f.sha256=sha(f.png);f.nativeSha256=sha(f.nativePng);f.durationMs=c.durationsMs[i];}
 fs.writeFileSync(path.join(ROOT,p),JSON.stringify(c,null,2)+'\n');
}
console.log(`Wrote ${clipPath} and synchronized both 450ms F02 candidate manifests.`);
