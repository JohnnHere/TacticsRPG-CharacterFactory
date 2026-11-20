// R2 verifier: back_r Sword v3 / Axe v2 integrity (read-only).
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { ROOT } from '../../src/core.mjs';
import { decode } from '../../src/images.mjs';
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const checks=[];const check=(name,ok,detail)=>checks.push({name,status:ok?'PASS':'FAIL',detail:detail??''});
const defs=[
 {category:'Sword',version:'representative-v3',prev:'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2',prevMap:[0,1,2,3,4,5,6,7],impact:4},
 {category:'Axe',version:'representative-v2',prev:'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1',prevMap:[0,1,2,3,4,5,6,7],impact:5}
];
for(const d of defs){
 const base=`characters/orc-v1/source/rear-recovery-v2/back_r/${d.category}/Attack-${d.version}`;
 const clip=JSON.parse(fs.readFileSync(path.join(ROOT,base,'clip.json'),'utf8'));
 const tag=`${d.category} ${d.version}`;
 check(`${tag} metadata-hashes`,[clip.masterSha256,clip.bodyMasterSha256,clip.nativeMasterSha256,clip.stripSha256].every((h,i)=>h===sha(path.join(ROOT,[clip.master,clip.bodyMaster,clip.nativeMaster,clip.strip][i]))),'masters+strip');
 let comp=true,nat=true,src=true,ground=true,empty=true,hashes=true;
 for(let i=0;i<8;i++){
  const n=String(i).padStart(2,'0');
  const frame=clip.frames[i];
  for(const layer of Object.keys(frame.layers))if(sha(path.join(ROOT,frame.layers[layer].png))!==frame.layers[layer].sha256)hashes=false;
  if(sha(path.join(ROOT,frame.png))!==frame.sha256)hashes=false;
  if(sha(path.join(ROOT,frame.nativePng))!==frame.nativeSha256)hashes=false;
  const wb=decode(path.join(ROOT,`${base}/layers/weaponBack/${n}.png`)).image;
  const body=decode(path.join(ROOT,`${base}/layers/body/${n}.png`)).image;
  const wf=decode(path.join(ROOT,`${base}/layers/weaponFront/${n}.png`)).image;
  const hand=decode(path.join(ROOT,`${base}/layers/handFront/${n}.png`)).image;
  const flat=decode(path.join(ROOT,`${base}/${n}.png`)).image;
  const nat=decode(path.join(ROOT,`${base}/native/${n}.png`)).image;
  for(let y=0;y<256;y++)for(let x=0;x<256;x++){
   const idx=(y*256+x)*4;
   const A=[wb.data[idx],wb.data[idx+1],wb.data[idx+2],wb.data[idx+3]];
   const B=[body.data[idx],body.data[idx+1],body.data[idx+2],body.data[idx+3]];
   const C=[wf.data[idx],wf.data[idx+1],wf.data[idx+2],wf.data[idx+3]];
   const D=[hand.data[idx],hand.data[idx+1],hand.data[idx+2],hand.data[idx+3]];
   const over=(below,above)=>{const ta=above[3]/255,ba=below[3]/255,oa=ta+ba*(1-ta);if(oa===0)return[0,0,0,0];const c=[0,1,2].map(k=>Math.round((above[k]*ta+below[k]*ba*(1-ta))/oa));c[3]=Math.round(oa*255);return c};
   const got=over(over(over(A,B),C),D);
   const want=[flat.data[idx],flat.data[idx+1],flat.data[idx+2],flat.data[idx+3]];
   if(Math.abs(got[0]-want[0])>1||Math.abs(got[1]-want[1])>1||Math.abs(got[2]-want[2])>1||Math.abs(got[3]-want[3])>1)comp=false;
   if(x>=64&&x<192&&y>=64&&y<192){
    const nidx=((y-64)*128+(x-64))*4;
    if(nat.data[nidx]!==body.data[idx]||nat.data[nidx+1]!==body.data[idx+1]||nat.data[nidx+2]!==body.data[idx+2]||nat.data[nidx+3]!==body.data[idx+3])nat=false;
   }
  }
  if(i===0||i===7){
   for(const im of [wb,wf,hand]){for(let k=3;k<im.data.length;k+=4)if(im.data[k]>0)empty=false}
  }
  const s=decode(path.join(ROOT,`${d.prev}/layers/body/${String(d.prevMap[i]).padStart(2,'0')}.png`)).image;
  for(let k=0;k<body.data.length;k++)if(s.data[k]!==body.data[k])src=false;
  let bottom=0;for(let y=255;y>=0&&bottom===0;y--)for(let x=0;x<256;x++)if(flat.data[(y*256+x)*4+3]>0){bottom=y;break}
  if(bottom!==190)ground=false;
 }
 check(`${tag} alpha-over composition`,comp,'4 layers == composite');
 check(`${tag} native center-crop`,nat,'native128 == body center crop');
 check(`${tag} bodies preserved from previous`,src,'all 8 body layers byte-equal');
 check(`${tag} unarmed boundaries empty`,empty,'F00/F07 weapon+hand layers empty');
 check(`${tag} ground contact`,ground,'composite bottom == 190');
 check(`${tag} file hashes`,hashes,'layers/composite/native');
 check(`${tag} visible interval`,JSON.stringify(clip.visibleInterval)==='[1,6]','contiguous 1..6');
 check(`${tag} durations`,JSON.stringify(clip.durationsMs)==='[90,80,90,100,80,100,100,110]','750ms');
 check(`${tag} impact`,clip.contactEvent.frame===d.impact,`frame ${d.impact}`);
 if(d.category==='Sword')check(`${tag} hold angles stable`,clip.frames[2].rotationDeg===350&&clip.frames[3].rotationDeg===350,'F02=F03=350');
}
const fail=checks.filter(c=>c.status==='FAIL');
console.log(JSON.stringify({status:fail.length?'FAIL':'PASS',summary:{PASS:checks.filter(c=>c.status==='PASS').length,FAIL:fail.length},fail},null,2));
if(fail.length)process.exitCode=1;
