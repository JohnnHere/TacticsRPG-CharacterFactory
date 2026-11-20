// R2 metadata: clip.json for back_r Sword v3 + Axe v2 (hold-angle stabilization + strike timing).
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { ROOT } from '../../src/core.mjs';
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT,p))).digest('hex');
const durations=[90,80,90,100,80,100,100,110];
const defs=[
 {dir:'back_r',category:'Sword',weaponName:'sword',version:'representative-v3',weaponId:'recruit-sword',weaponNameBr:'Espada do Recruta',weaponPng:'assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png',itemGrip:[48,66],itemCanvas:[96,96],
  phases:['guard-start','reach-close-fist','cock-high','load-back','slash-release','impact-follow-through','lowered-recovery','return-guard'],
  grips:[[0,0],[175,106],[166,76],[164,84],[183,92],[181,121],[170,127],[0,0]],angles:[0,325,350,350,60,100,135,0],behind:[false,false,true,true,false,false,false,false],impact:4,
  prev:'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2',
  angleNote:'hold frames F02/F03 normalized 20/345 -> 350/350 (blade no longer jitters between identical overhead holds); all other angles preserved'},
 {dir:'back_r',category:'Axe',weaponName:'axe',version:'representative-v2',weaponId:'militia-axe',weaponNameBr:'Machado de Milícia',weaponPng:'assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png',itemGrip:[36,55],itemCanvas:[96,96],
  phases:['guard-start','reach','cocked-shoulder','overhead-hold','downward-commit','impact','lowered-follow-through','recovery'],
  grips:[[0,0],[175,106],[167,73],[167,78],[173,116],[159,121],[156,139],[0,0]],angles:[0,315,350,0,70,105,135,0],behind:[false,false,true,true,false,false,false,false],impact:5,
  prev:'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1',
  angleNote:'angles preserved (already a monotonic arc); timing only'}
];
for(const d of defs){
 const base=`characters/orc-v1/source/rear-recovery-v2/${d.dir}/${d.category}/Attack-${d.version}`;
 const src='characters/orc-v1/source/aseprite/rear-recovery-v2';
 const visible=[false,true,true,true,true,true,true,false];
 const clip={schemaVersion:1,revision:'main-orc-rear-recovery-v2-r2-hold-stable',id:d.category==='Sword'?'basic.sword-slash':'basic.axe-chop',character:'orc-v1',category:d.category,state:'Attack',direction:d.dir,loop:false,oneShot:true,terminal:false,canvas:[256,256],bodyOffset:[64,64],groundY:190,nativeCanvas:[128,128],nativeGroundY:126,ppu:100,frameCount:8,durationsMs:durations,totalDurationMs:durations.reduce((a,b)=>a+b,0),
  master:`${src}/composite/${d.dir}/${d.weaponName}-attack-${d.version}.aseprite`,bodyMaster:`${src}/composite/${d.dir}/${d.weaponName}-body-${d.version}.aseprite`,nativeMaster:`${src}/native/${d.weaponName}-body-${d.version}-${d.dir}.aseprite`,strip:`${base}/native-strip.png`,layerOrder:['weaponBack','body','weaponFront','handFront'],visibleInterval:[1,6],weaponVisible:true,weaponOverlay:true,
  weapon:{id:d.weaponId,name:d.weaponNameBr,grip:d.itemGrip,canvas:d.itemCanvas,source:d.weaponPng,sourceSha256:sha(d.weaponPng)},
  contactEvent:{frame:d.impact,timeMs:durations.slice(0,d.impact).reduce((a,b)=>a+b,0),status:'CANDIDATE_VISUAL_ONLY',appliesDamage:false},
  technicalStatus:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',artisticApproval:'PENDING_CREATOR',
  provenance:{repair:'R2 hold-stable: creator review 2026-10-27 flagged abrupt reversal/blade jitter; VL round 1 saw coherent swing but hold wobble + hard 03->04 snap. Bodies are the EXACT frozen previous-candidate body layers (pixel-preserved). '+d.angleNote+'. Durations 90/80/90/100/80/100/100/110 (750ms): hold +20ms, strike -20ms so the snap reads as impact speed.',bodies:'previous candidate layers/body/00..07.png (frozen reviewed pixels)',weapon:'unchanged independent weapon PNG; transformed in Aseprite Lua',supersedes:d.prev+'/clip.json',evidence:'experiments/main-orc-rear-recovery-v2/defect-map-and-repairs.md',framesPreserved:8,framesDropped:0,framesRegenerated:0},
  frames:[]};
 for(const [p,k] of [[clip.master,'masterSha256'],[clip.bodyMaster,'bodyMasterSha256'],[clip.nativeMaster,'nativeMasterSha256'],[clip.strip,'stripSha256']])clip[k]=sha(p);
 for(let i=0;i<8;i++){
  const n=String(i).padStart(2,'0');const f={index:i,png:`${base}/${n}.png`,durationMs:durations[i],phase:d.phases[i],weaponVisible:visible[i],rightGrip:d.grips[i],rotationDeg:d.angles[i],weaponBehindBody:d.behind[i],layers:{}};
  for(const layer of ['weaponBack','body','weaponFront','handFront']){const p=`${base}/layers/${layer}/${n}.png`;f.layers[layer]={png:p,sha256:sha(p)}}
  f.sha256=sha(f.png);f.nativePng=`${base}/native/${n}.png`;f.nativeSha256=sha(f.nativePng);clip.frames.push(f);
 }
 const clipPath=`${base}/clip.json`;fs.writeFileSync(path.join(ROOT,clipPath),JSON.stringify(clip,null,2)+'\n');
 console.log(`Wrote ${clipPath}`);
}
