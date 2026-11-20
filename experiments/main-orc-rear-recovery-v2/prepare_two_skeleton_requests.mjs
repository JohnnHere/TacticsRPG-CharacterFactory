import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { ROOT } from '../../src/core.mjs';
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const labels=['NOSE','NECK','RIGHT SHOULDER','RIGHT ELBOW','RIGHT ARM','LEFT SHOULDER','LEFT ELBOW','LEFT ARM','RIGHT HIP','RIGHT KNEE','RIGHT LEG','LEFT HIP','LEFT KNEE','LEFT LEG','RIGHT EYE','LEFT EYE','RIGHT EAR','LEFT EAR'];
function skeleton(pose,near='right'){
 const pts={
  'NOSE':[64,17],'NECK':[64,29],
  'RIGHT SHOULDER':[near==='right'?76:52,36],'RIGHT ELBOW':[near==='right'?86:42,50],'RIGHT ARM':[near==='right'?96:32,63],
  'LEFT SHOULDER':[near==='right'?52:76,36],'LEFT ELBOW':[near==='right'?42:86,50],'LEFT ARM':[near==='right'?32:96,63],
  'RIGHT HIP':[71,73],'RIGHT KNEE':[75,96],'RIGHT LEG':[75,118],
  'LEFT HIP':[57,73],'LEFT KNEE':[53,96],'LEFT LEG':[51,118],
  'RIGHT EYE':[67,15],'LEFT EYE':[61,15],'RIGHT EAR':[73,21],'LEFT EAR':[55,21]
 };
 for(const [k,v] of Object.entries(pose||{}))pts[k]=v;
 return labels.map(label=>({label,x:pts[label][0]/128,y:pts[label][1]/128,z_index:(label.includes('RIGHT ELBOW')||label==='RIGHT ARM')?165:(label.includes('LEFT ELBOW')||label==='LEFT ARM')?105:128}));
}
const configs=[
 {
  id:'back_l-sword',direction:'north-west',dominant:'left',
  action:'one-handed sword attack',
  description:'Verde Warcraft Orc warrior in dark plate armor with muted red-brown straps, seen from his own back-left (northwest) direction, empty-handed body pose; preserve this direction and its original lighting.',
  path:'experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png',near:'left',
  poses:[
   {'RIGHT ELBOW':[44,48],'RIGHT ARM':[34,54],'NECK':[64,29]},
   {'RIGHT ELBOW':[45,25],'RIGHT ARM':[38,12],'NECK':[64,28]},
   {'RIGHT ELBOW':[52,27],'RIGHT ARM':[62,18],'NECK':[65,28]},
   {'RIGHT ELBOW':[39,30],'RIGHT ARM':[25,19],'NECK':[63,28],'RIGHT HIP':[58,73],'LEFT HIP':[58,74]},
   {'RIGHT ELBOW':[34,42],'RIGHT ARM':[21,36],'NECK':[62,29],'RIGHT HIP':[58,73]},
   {'RIGHT ELBOW':[40,52],'RIGHT ARM':[29,63],'NECK':[64,30]},
   {'RIGHT ELBOW':[44,51],'RIGHT ARM':[35,63]}
  ],
  sequence:['reach with closed fist','cock sword hand high over shoulder','load across dorsal line','release forward toward northwest','slashing follow-through','lowered recovery','return to empty-hand guard']
 },
 {
  id:'back_r-axe',direction:'north-east',dominant:'right',
  action:'one-handed heavy axe chop',
  description:'Verde Warcraft Orc warrior in dark plate armor with muted red-brown straps, seen from his own back-right (northeast) direction, empty-handed body pose; preserve this direction and its original lighting.',
  path:'experiments/main-orc-rear-recovery-v2/inputs/back_r-axe-native128.png',near:'right',
  poses:[
   {'RIGHT ELBOW':[91,43],'RIGHT ARM':[105,48],'NECK':[64,29]},
   {'RIGHT ELBOW':[89,24],'RIGHT ARM':[100,10],'NECK':[64,28]},
   {'RIGHT ELBOW':[96,27],'RIGHT ARM':[108,15],'NECK':[65,28],'RIGHT SHOULDER':[78,35],'RIGHT HIP':[70,73],'LEFT HIP':[57,74]},
   {'RIGHT ELBOW':[88,43],'RIGHT ARM':[103,60],'NECK':[63,30],'RIGHT SHOULDER':[77,37],'RIGHT HIP':[70,74],'LEFT HIP':[57,75]},
   {'RIGHT ELBOW':[84,54],'RIGHT ARM':[96,72],'NECK':[62,32],'RIGHT HIP':[69,76],'LEFT HIP':[56,77],'RIGHT KNEE':[74,99],'LEFT KNEE':[52,99]},
   {'RIGHT ELBOW':[82,59],'RIGHT ARM':[92,78],'NECK':[62,33],'RIGHT HIP':[68,76],'LEFT HIP':[56,77]},
   {'RIGHT ELBOW':[89,47],'RIGHT ARM':[101,62],'NECK':[64,30],'RIGHT HIP':[70,73],'LEFT HIP':[57,73]}
  ],
  sequence:['brief load with fist forward','cocked shoulder, fist high','hold heavy chop above shoulder','commit torso and arm downward','impact with bent knees and weight drop','follow through low and heavy','recover to guard']
 }
];
for(const c of configs){
 const first=skeleton({},c.near),frames=c.poses.map(p=>skeleton(p,c.near));
 const source=path.join(ROOT,c.path);
 const req={schemaVersion:1,jobTarget:c.id,action:c.action,description:c.description,direction:c.direction,view:'low top-down',frameCount:7,no_background:true,first_frame_keypoints:first,keypoints:frames,estimatedCostGenerations:3,estimateBasis:'animate_with_skeleton_v3 schema: 4–14 frames = 3 generations; verified before call; cap requires <=3',sequence:c.sequence,inputPng:c.path,inputSha256:sha(source),startingSkeleton:first,poses:frames};
 const out=path.join(ROOT,'experiments/main-orc-rear-recovery-v2/inputs',`${c.id}-request.json`);
 fs.writeFileSync(out,JSON.stringify(req,null,2)+'\n');
}
console.log('Wrote both exact seven-pose COCO-18 request descriptions and skeleton arrays; each schema cost estimate is 3.');
