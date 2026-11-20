// R1 metadata: clip.json for back_l Sword/Axe Attack-representative-v2 (7 frames, F01 extension dropped).
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { ROOT } from '../../src/core.mjs';
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT,p))).digest('hex');
const durations=[90,110,90,80,90,110,120];
const defs=[
 {dir:'back_l',category:'Sword',weaponName:'sword',weaponId:'recruit-sword',weaponNameBr:'Espada do Recruta',weaponPng:'assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png',itemGrip:[48,66],itemCanvas:[96,96],
  phases:['guard-start','cock-overhead','load-across-back','NW-release','follow-through','lowered-recovery','return-unarmed'],
  grips:[[0,0],[104,70],[127,72],[93,71],[74,95],[100,118],[82,127]],angles:[0,350,20,240,215,200,0],behind:[false,false,true,true,false,false,false],impact:3,
  sourceCleaned:'experiments/main-orc-rear-recovery-v2/back_l-sword-cleaned-native',base:'experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png',prev:'characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1'},
 {dir:'back_l',category:'Axe',weaponName:'axe',weaponId:'militia-axe',weaponNameBr:'Machado de Milícia',weaponPng:'assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png',itemGrip:[36,55],itemCanvas:[96,96],
  phases:['guard-start','cocked-overhead','overhead-hold','downward-commit','impact','low-follow-through','recovery'],
  grips:[[0,0],[104,78],[104,78],[86,118],[96,141],[99,145],[0,0]],angles:[0,315,350,315,270,235,0],behind:[false,false,true,true,false,false,false],impact:4,
  sourceCleaned:'experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native',base:'experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png',prev:'characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1'}
];
for(const d of defs){
 const base=`characters/orc-v1/source/rear-recovery-v2/${d.dir}/${d.category}/Attack-representative-v2`;
 const src='characters/orc-v1/source/aseprite/rear-recovery-v2';
 const visible=[false,true,true,true,true,true,false];
 const clip={schemaVersion:1,revision:'main-orc-rear-recovery-v2-r1-drop-extension',id:d.category==='Sword'?'basic.sword-slash':'basic.axe-chop',character:'orc-v1',category:d.category,state:'Attack',direction:d.dir,loop:false,oneShot:true,terminal:false,canvas:[256,256],bodyOffset:[64,64],groundY:190,nativeCanvas:[128,128],nativeGroundY:126,ppu:100,frameCount:7,durationsMs:durations,totalDurationMs:durations.reduce((a,b)=>a+b,0),
  master:`${src}/composite/${d.dir}/${d.weaponName}-attack-representative-v2.aseprite`,bodyMaster:`${src}/composite/${d.dir}/${d.weaponName}-body-representative-v2.aseprite`,nativeMaster:`${src}/native/${d.weaponName}-body-representative-v2-${d.dir}.aseprite`,strip:`${base}/native-strip.png`,layerOrder:['weaponBack','body','weaponFront','handFront'],visibleInterval:[1,5],weaponVisible:true,weaponOverlay:true,
  weapon:{id:d.weaponId,name:d.weaponNameBr,grip:d.itemGrip,canvas:d.itemCanvas,source:d.weaponPng,sourceSha256:sha(d.weaponPng)},
  contactEvent:{frame:d.impact,timeMs:durations.slice(0,d.impact).reduce((a,b)=>a+b,0),status:'CANDIDATE_VISUAL_ONLY',appliesDamage:false},
  technicalStatus:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',artisticApproval:'PENDING_CREATOR',
  provenance:{repair:'R1 drop-frame: creator review 2026-10-27 flagged back_l attacks "severe motion inconsistency"; VL round 1 (diag/visual/rear-attacks-inspection.md) confirmed F01 was a full pre-strike extension without wind-up causing a double reversal; body 68%/22% diff vs F04 ruled out duplicate-frame cause. Frame dropped; kept frames reuse the EXACT frozen v1 body layers (pixel-preserved); grips/angles/behind of kept frames preserved; durations retimed 90/110/90/80/90/110/120 (690ms).',bodies:'v1 layers/body/{00,02,03,04,05,06,07}.png of the frozen reviewed candidate (cleaned-native experiment files NOT used: they diverged from frozen pixels)',weapon:'unchanged independent weapon PNG; transformed in Aseprite Lua',supersedes:d.prev+'/clip.json',evidence:'experiments/main-orc-rear-recovery-v2/defect-map-and-repairs.md',framesPreserved:6,framesDropped:1,framesRegenerated:0},
  frames:[]};
 for(const [p,k] of [[clip.master,'masterSha256'],[clip.bodyMaster,'bodyMasterSha256'],[clip.nativeMaster,'nativeMasterSha256'],[clip.strip,'stripSha256']])clip[k]=sha(p);
 for(let i=0;i<7;i++){
  const n=String(i).padStart(2,'0');const f={index:i,png:`${base}/${n}.png`,durationMs:durations[i],phase:d.phases[i],weaponVisible:visible[i],rightGrip:d.grips[i],rotationDeg:d.angles[i],weaponBehindBody:d.behind[i],layers:{}};
  for(const layer of ['weaponBack','body','weaponFront','handFront']){const p=`${base}/layers/${layer}/${n}.png`;f.layers[layer]={png:p,sha256:sha(p)}}
  f.sha256=sha(f.png);f.nativePng=`${base}/native/${n}.png`;f.nativeSha256=sha(f.nativePng);clip.frames.push(f);
 }
 const clipPath=`${base}/clip.json`;fs.writeFileSync(path.join(ROOT,clipPath),JSON.stringify(clip,null,2)+'\n');
 console.log(`Wrote ${clipPath}`);
}
