import fs from 'node:fs';
import crypto from 'node:crypto';
import {PNG} from 'pngjs';
const out='experiments/main-orc-artistic-reconstruction-v6/qa-sol/closure-5d68b52d';
const mp='characters/orc-v1/source/artistic-reconstruction-v6/candidate28manifest.json';
const m=JSON.parse(fs.readFileSync(mp));
const parent=JSON.parse(fs.readFileSync(m.parentManifest));
const read=p=>PNG.sync.read(fs.readFileSync(p));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
function sheet(c,layer){
 const w=256,h=256,cols=4,rows=Math.ceil(c.frames.length/cols),p=new PNG({width:w*cols,height:h*rows});
 for(let i=0;i<p.data.length;i+=4){p.data[i]=46;p.data[i+1]=53;p.data[i+2]=59;p.data[i+3]=255;}
 c.frames.forEach((f,n)=>{const a=read(layer?f.layers[layer].png:f.png);const ox=n%cols*w,oy=Math.floor(n/cols)*h;for(let y=0;y<a.height;y++)for(let x=0;x<a.width;x++){let s=(y*a.width+x)*4,d=((oy+y)*p.width+ox+x)*4,t=a.data[s+3]/255;for(let k=0;k<3;k++)p.data[d+k]=Math.round(a.data[s+k]*t+p.data[d+k]*(1-t));}});
 return p;
}
const checks=[];
for(const cell of m.cells.filter(x=>['Sword','Axe'].includes(x.action))){
 const c=JSON.parse(fs.readFileSync(cell.clipJson)),old=JSON.parse(fs.readFileSync(cell.parentCell.clipJson));
 const id=cell.cellId.replace('/','-');
 fs.writeFileSync(`${out}/${id}-composite.png`,PNG.sync.write(sheet(c)));
 fs.writeFileSync(`${out}/${id}-body.png`,PNG.sync.write(sheet(c,'body')));
 const diffs=c.frames.map((f,i)=>{if(!old.frames[i])return null;const a=read(f.layers.body.png),b=read(old.frames[i].layers.body.png);let pixels=0,alpha=0;for(let j=0;j<a.data.length;j+=4){if(a.data.subarray(j,j+4).some((v,k)=>v!==b.data[j+k]))pixels++;if(a.data[j+3]!==b.data[j+3])alpha++;}return{frame:i,pixels,alpha};});
 checks.push({cell:cell.cellId,clipHashMatches:hash(cell.clipJson)===cell.clipSha256,frames:c.frames.length,durations:c.durationsMs,bodyDifferences:diffs,bookends:c.frames.filter((f,i)=>i===0||i===c.frames.length-1).map(f=>({frame:f.index,weaponVisible:f.weaponVisible}))});
}
const unchanged=m.cells.filter(c=>!['Sword','Axe'].includes(c.action)).map(c=>({cell:c.cellId,sameClipPath:c.clipJson===parent.cells.find(p=>p.cellId===c.cellId).clipJson,hashMatches:hash(c.clipJson)===c.clipSha256}));
fs.writeFileSync(`${out}/inspection-checks.json`,JSON.stringify({manifestHash:hash(mp),checks,unchanged},null,2));
function zoom(src,dest,box,scale=4){const a=read(src),[ox,oy,w,h]=box,p=new PNG({width:w*scale,height:h*scale});for(let y=0;y<p.height;y++)for(let x=0;x<p.width;x++){const s=((oy+Math.floor(y/scale))*a.width+ox+Math.floor(x/scale))*4,d=(y*p.width+x)*4,t=a.data[s+3]/255;for(let k=0;k<3;k++)p.data[d+k]=Math.round(a.data[s+k]*t+50*(1-t));p.data[d+3]=255;}fs.writeFileSync(dest,PNG.sync.write(p));}
for(const id of ['back_l-Axe','back_r-Sword','front_l-Sword'])zoom(`${out}/${id}-composite.png`,`${out}/${id}-detail.png`,[0,256,1024,256],2);
for(const cell of m.cells.filter(c=>c.cellId==='front_l/Sword')){const c=JSON.parse(fs.readFileSync(cell.clipJson));for(const i of [1,2,3,4,5]){zoom(c.frames[i].layers.body.png,`${out}/front_l-Sword-F${i}-axilla.png`,[120,85,60,70]);}}
console.log(JSON.stringify({manifestHash:hash(mp),sheets:16,unchanged,frontDifferences:checks.filter(c=>c.cell.startsWith('front')).map(c=>({cell:c.cell,diffs:c.bodyDifferences}))}));

