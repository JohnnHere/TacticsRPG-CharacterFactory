import fs from 'node:fs';import {PNG} from 'pngjs';
const E='experiments/main-orc-hybrid-weapon-04';const read=p=>PNG.sync.read(fs.readFileSync(p));const clip=JSON.parse(fs.readFileSync('characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_l-sword/clip.json'));
const rows=[];
for(const f of clip.frames){const fn=`F${String(f.index).padStart(2,'0')}.png`;const src=read(f.png),a=read(`${E}/full/a/composite/${fn}`),b=read(`${E}/full/b/composite/${fn}`),wb=read(`${E}/full/b/weapon-only/${fn}`);let deltaA=0,partial=0,newNeutralBright=0,weaponPixels=0;
 for(let i=0;i<a.data.length;i+=4){if(!a.data.subarray(i,i+4).equals(src.data.subarray(i,i+4)))deltaA++;if(b.data[i+3]>0&&b.data[i+3]<255)partial++;if(wb.data[i+3])weaponPixels++;const p=b.data.subarray(i,i+3),q=a.data.subarray(i,i+3);if(b.data[i+3]&&Math.min(...p)>=225&&Math.max(...p)-Math.min(...p)<=20&&!(a.data[i+3]&&Math.min(...q)>=225&&Math.max(...q)-Math.min(...q)<=20))newNeutralBright++;}
 rows.push({frame:f.index,recompositionADeltaPixels:deltaA,partialAlphaB:partial,newNearWhiteNeutralB:newNeutralBright,weaponPixelsB:weaponPixels});
}
const bounds=im=>{let ys=[];for(let y=0;y<55;y++)for(let x=0;x<96;x++)if(im.data[(y*96+x)*4+3])ys.push(y);return {minY:Math.min(...ys),maxY:Math.max(...ys),length:Math.max(...ys)-Math.min(...ys)+1}};
const boundsA=bounds(read(E+'/variants/sword-a/sword.png')),boundsB=bounds(read(E+'/variants/sword-b/sword.png'));
const wd=JSON.parse(fs.readFileSync(E+'/weapon-diff.json'));Object.assign(wd,{bladeA:boundsA,bladeB:boundsB,lengthA:boundsA.length,lengthB:boundsB.length,lengthChangePercent:(boundsB.length/boundsA.length-1)*100});fs.writeFileSync(E+'/weapon-diff.json',JSON.stringify(wd,null,2));
fs.writeFileSync(E+'/edge-diagnostics.json',JSON.stringify({threshold:'near-white = min RGB>=225, max-min<=20; diagnostic only; preserve legitimate metal highlights',frames:rows},null,2));
// Review raster only: unchanged source pixels enlarged by integer nearest-neighbour.
const out=new PNG({width:1536,height:1024});out.data.fill(0);
for(let vi=0;vi<2;vi++)for(let k=0;k<3;k++){const im=read(`${E}/representative/${['a','b'][vi]}/composite/F${[2,8,11][k].toString().padStart(2,'0')}.png`);for(let y=0;y<256;y++)for(let x=0;x<256;x++)for(let dy=0;dy<2;dy++)for(let dx=0;dx<2;dx++){let i=((vi*512+y*2+dy)*1536+k*512+x*2+dx)*4;im.data.copy(out.data,i,(y*256+x)*4,(y*256+x)*4+4)}}fs.writeFileSync(E+'/representative-review-2x.png',PNG.sync.write(out));
console.log({boundsA,boundsB,rows});
