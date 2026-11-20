// Small QA-only native-coordinate detail crops from the canonical body cels.
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';
import { ROOT } from '../../src/core.mjs';
import { decode } from '../../src/images.mjs';
const out=path.join(ROOT,'experiments/main-orc-rear-recovery-v2/E/qa-revision-1-inspection/details');fs.mkdirSync(out,{recursive:true});
const cases=[
 ['swordL-f01-right-hand','back_l','Sword',1,146,112,34,48],
 ['swordL-f05-shoulder','back_l','Sword',5,120,80,65,45],
 ['swordL-f07-right-hand','back_l','Sword',7,146,112,34,48],
 ['axeR-f01-fist-head','back_r','Axe',1,140,68,48,54],
 ['axeR-f02-shaft','back_r','Axe',2,142,24,48,58],
 ['axeR-f03-shaft','back_r','Axe',3,142,24,48,58],
 ['axeR-f04-arm','back_r','Axe',4,128,72,68,76],
 ['axeR-f05-arm','back_r','Axe',5,128,72,68,76],
 ['axeL-f02-hook','back_l','Axe',2,142,70,52,45],
 ['axeL-f03-hook','back_l','Axe',3,142,70,52,45]
];
for(const [name,d,a,n,x0,y0,w,h] of cases){const file=`characters/orc-v1/source/rear-recovery-v2/${d}/${a}/Attack-representative-v1/layers/body/${String(n).padStart(2,'0')}.png`;const src=decode(path.join(ROOT,file)).image,scale=8,dst=new PNG({width:w*scale,height:h*scale});for(let y=0;y<h;y++)for(let x=0;x<w;x++){const si=((y+y0)*src.width+x+x0)*4,a=src.data[si+3],bg=((Math.floor((x+x0)/4)+Math.floor((y+y0)/4))%2)?84:118;for(let sy=0;sy<scale;sy++)for(let sx=0;sx<scale;sx++){const di=((y*scale+sy)*dst.width+x*scale+sx)*4;if(a){for(let c=0;c<3;c++)dst.data[di+c]=Math.round(src.data[si+c]*(a/255)+bg*(1-a/255))}else dst.data[di]=dst.data[di+1]=dst.data[di+2]=bg;dst.data[di+3]=255;if(((x+x0)%4===0&&sx===0)||((y+y0)%4===0&&sy===0)){dst.data[di]=Math.round(dst.data[di]*.55);dst.data[di+1]=Math.round(dst.data[di+1]*.72);dst.data[di+2]=Math.round(dst.data[di+2]*.85)}}}fs.writeFileSync(path.join(out,`${name}.png`),PNG.sync.write(dst));}
fs.writeFileSync(path.join(out,'coordinates.json'),JSON.stringify({coordinateConvention:'Each image pixel maps to its native 256x256 source pixel; filename ROI origin is retained in script case list.',crops:cases.map(([name,d,a,frame,x,y,width,height])=>({name,direction:d,action:a,frame,x,y,width,height}))},null,2)+'\n');
console.log(JSON.stringify({status:'PASS',qaOnly:true,crops:cases.length,scale:8,output:path.relative(ROOT,out)},null,2));
