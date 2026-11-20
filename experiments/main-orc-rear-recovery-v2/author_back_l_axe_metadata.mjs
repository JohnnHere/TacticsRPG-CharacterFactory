import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {PNG} from 'pngjs';
import {ROOT} from '../../src/core.mjs';

const sha = p => crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT,p))).digest('hex');
const out='characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1';
const master='characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/axe-attack-representative-v1.aseprite';
const bodyMaster='characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/axe-body-representative-v1.aseprite';
const nativeMaster='characters/orc-v1/source/aseprite/rear-recovery-v2/native/axe-body-representative-v1-back_l.aseprite';
const durations=[90,80,90,80,100,80,100,110];
const phases=['guard-start','left-hand-reach','cocked-overhead','overhead-hold','downward-commit','impact','low-follow-through','recovery'];
const grips=[[0,0],[92,108],[104,78],[104,78],[86,118],[96,141],[99,145],[0,0]];
const angles=[0,270,315,350,315,270,235,0];
const visible=durations.map((_,i)=>i>=1&&i<=6);
const layerNames=['weaponBack','body','weaponFront','handFront'];
const item='assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png';
const jobId='5296ac98-b253-4133-8468-155f7e90c68e';
const auth='experiments/main-orc-rear-recovery-v2/root-authorization-back_l-axe-2026-10-26T191359Z.json';
const ledger='experiments/main-orc-rear-recovery-v2/cost-provenance-ledger.json';
const request='experiments/main-orc-rear-recovery-v2/inputs/back_l-axe-request.json';
const raw='experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l_axe';
const layersByFrame=[];
for(let i=0;i<8;i++){
 const n=String(i).padStart(2,'0');
 const layers=Object.fromEntries(layerNames.map(name=>[name,{png:`${out}/layers/${name}/${n}.png`,sha256:sha(`${out}/layers/${name}/${n}.png`)}]));
 const composite=`${out}/${n}.png`,native=`${out}/native/${n}.png`;
 layersByFrame.push({index:i,durationMs:durations[i],phase:phases[i],weaponVisible:visible[i],rightGrip:grips[i],rotationDeg:angles[i],layers,png:composite,sha256:sha(composite),nativePng:native,nativeSha256:sha(native)});
}
const gifExports={};
for(const [key,delays] of Object.entries({
 '1x':durations,
 '075x':[120,110,120,110,130,110,130,150],
 '05x':[180,160,180,160,200,160,200,220]
})){
 const p=`experiments/main-orc-rear-recovery-v2/back_l-axe-representative-${key}.gif`;
 gifExports[key]={path:p,sha256:sha(p),frameDelaysMs:delays,totalMs:delays.reduce((a,b)=>a+b,0)};
}
const input='experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png';
const clip={
 schemaVersion:1,revision:'main-orc-rear-recovery-v2-authorized-skeleton-v3-representative-v1',
 id:'basic.axe-chop',character:'orc-v1',category:'Axe',state:'Attack',direction:'back_l',loop:false,oneShot:true,terminal:false,
 canvas:[256,256],bodyOffset:[64,64],groundY:190,nativeCanvas:[128,128],nativeGroundY:126,ppu:100,
 frameCount:8,durationsMs:durations,totalDurationMs:730,master,bodyMaster,nativeMaster,strip:`${out}/native-strip.png`,
 layerOrder:layerNames,visibleInterval:[1,6],weaponVisible:true,weaponOverlay:true,
 weapon:{id:'militia-axe',name:'Machado de Milícia',grip:[36,55],canvas:[96,96],source:item,sourceSha256:sha(item)},
 technicalStatus:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',artisticApproval:'PENDING_CREATOR',
 provenance:{
  generationJobId:jobId,assetId:'42cb4114-2fe0-5310-a3e7-79b640105256',tool:'mcp__pixellab__animate_with_skeleton_v3',model:'PixelLab skeleton-v3',
  estimatedCostGenerations:3,actualCostGenerations:3,experimentTotalGenerations:78,input,inputSha256:sha(input),skeletonRequest:request,
  sourceFrames:Array.from({length:7},(_,i)=>`${raw}/${String(i).padStart(2,'0')}.png`),
  weaponArt:'unchanged independent militia axe PNG; transform authored in Aseprite only',
  generationBudgetLedger:ledger,rootAuthorization:auth,localRepair:'experiments/main-orc-rear-recovery-v2/axeL-local-repair-provenance.json',
  bodyCleanup:'Aseprite-only; see axeL-local-repair-provenance.json. Generated opposite-side axe and detached shaft removed; clipped old-arm residue removed by exact component mask; same-view SwordL overhead forearm/closed gauntlet adapted for AxeL frames 01/02.'
 },
 reviewEvidence:{
  gripCloseups:'experiments/main-orc-rear-recovery-v2/back_l-axe-grip-closeups-qa.png',
  weaponLayersOff:`${out}/weapon-layers-off-qa.png`,compositeSheet:`${out}/composite-sheet-qa.png`,
  rootPlayback:'experiments/main-orc-rear-recovery-v2/diagnosis/root-axeL-final-playback.json',
  gifExports,rootReview:'PASS_FOR_INTERNAL_INTEGRATION',integratedArgonQA:'PENDING',creatorApproval:'PENDING_CREATOR'
 },
 frames:layersByFrame
};
const target=path.join(ROOT,out,'clip.json');
fs.writeFileSync(target,JSON.stringify(clip,null,2)+'\n');

const rawHashes=Array.from({length:7},(_,i)=>({path:`${raw}/${String(i).padStart(2,'0')}.png`,sha256:sha(`${raw}/${String(i).padStart(2,'0')}.png`)}));
const cleanup={
 schemaVersion:1,createdAtUtc:new Date().toISOString(),direction:'back_l',action:'Axe',
 generatedBody:{jobId,assetId:'42cb4114-2fe0-5310-a3e7-79b640105256',chargedGenerations:3,rawFrames:rawHashes},
 base:{path:input,sha256:sha(input),identity:'own approved NW/back_l empty-hand base; no rendered-image mirroring'},
 generatedWeaponContamination:[
  {frames:['01','02','03'],sourceMask:{xMin:96,xMax:127,yMin:20,yMax:58},operation:'Restore same-view NW base pixels to erase extra generated axe at stationary viewer-right shoulder',changedPixels:[278,270,39]},
  {frames:['01','02'],sourceMask:{xMin:35,xMax:85,yMin:0,yMax:23},operation:'Restore head/shaft region from NW base, preserving green skull; remove residual detached brown shaft-colored pixels inside Aseprite',restoredRegionPixelDifferences:[167,168],brownPixelsRemoved:[3,3]}
 ],
 adaptedArmReuse:{
  classification:'REUSE_ADAPTED',source:'characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/body/02.png plus layers/handFront/02.png',
  sourceSha256:{body:sha('characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/body/02.png'),handFront:sha('characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/handFront/02.png')},
  frames:['01','02'],translationNativePixels:[0,8],
  donorPolygon:[[28,28],[29,23],[33,19],[34,14],[31,9],[31,4],[34,0],[42,0],[46,5],[47,10],[45,15],[43,19],[43,24],[41,29],[39,34],[34,35],[30,33]],
  targetReplacementPolygon:[[10,0],[43,0],[48,7],[47,14],[44,21],[42,28],[39,34],[33,37],[27,34],[23,29],[19,23],[15,18],[11,12]],
  omittedBrownTopEdgePixels:true,method:'Aseprite Lua mask, same-view own-character arm and handFront pixels only; AxeL torso, legs, armor, perspective, and lighting retained.'
 },
 confirmedDetachedResidue:{frame:'02',connectedComponent8:{pixelCount:26,bbox:[18,22,26,34],coordinates:[[18,22],[18,23],[18,24],[19,24],[19,25],[20,25],[19,26],[20,26],[20,27],[21,27],[20,28],[21,28],[22,28],[21,29],[22,29],[21,30],[22,30],[23,30],[22,31],[23,31],[24,31],[24,32],[25,32],[25,33],[26,33],[26,34]]},isolatedPixel:[28,35],approvedBaseOpaqueAtThoseCoordinates:0,removedPixelCount:27,operation:'Aseprite exact-coordinate transparency mask; no general component-size filtering'},
 cleanupScript:'experiments/main-orc-rear-recovery-v2/clean_generated_axe_and_build_body.lua',armRepairScript:'experiments/main-orc-rear-recovery-v2/repair_back_l_axe_clipped_arm.lua',
 cleanedBodyFrames:Array.from({length:8},(_,i)=>({frame:i,path:`${out}/${String(i).padStart(2,'0')}.png`,sha256:sha(`${out}/${String(i).padStart(2,'0')}.png`)})),
 rawPreserved:true,master,bodyMaster,nativeMaster,technicalStatus:'TECHNICALLY_COMPLETE',visualStatus:'PASS_FOR_INTERNAL_INTEGRATION',creatorApproval:'PENDING_CREATOR'
};
fs.writeFileSync(path.join(ROOT,'experiments/main-orc-rear-recovery-v2/axeL-local-repair-provenance.json'),JSON.stringify(cleanup,null,2)+'\n');
console.log(JSON.stringify({clipJson:`${out}/clip.json`,frames:layersByFrame.length,gifs:Object.fromEntries(Object.entries(gifExports).map(([k,v])=>[k,v.totalMs])),repair:'Aseprite REUSE_ADAPTED; exact detached 27px component removed'},null,2));
