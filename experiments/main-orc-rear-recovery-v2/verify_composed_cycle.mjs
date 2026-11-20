import fs from 'node:fs';
import path from 'node:path';
import { ROOT, hash } from '../../src/core.mjs';
import { decode } from '../../src/images.mjs';

const d='characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2';
const durations=[90,80,90,80,100,80,100,110];
const byteEqual=(a,b)=>a.length===b.length&&a.every((v,i)=>v===b[i]);
const problems=[]; let bounds=[];
for(let i=0;i<8;i++){
 const n=String(i).padStart(2,'0');
 const comp=decode(path.join(ROOT,d,`${n}.png`)).image;
 const body=decode(path.join(ROOT,d,'layers/body',`${n}.png`)).image;
 const native=decode(path.join(ROOT,d,'native',`${n}.png`)).image;
 if(comp.width!==256||comp.height!==256) problems.push(`${n} composite canvas`);
 if(native.width!==128||native.height!==128) problems.push(`${n} native canvas`);
 const crop=Buffer.alloc(128*128*4);
 for(let y=0;y<128;y++) body.data.copy(crop,y*128*4,((y+64)*256+64)*4,((y+64)*256+192)*4);
 if(!byteEqual(crop,native.data)) problems.push(`${n} native is not exact body-only crop`);
 const layers=['weaponBack','body','weaponFront','handFront'].map(l=>decode(path.join(ROOT,d,'layers',l,`${n}.png`)).image);
 const flat=Buffer.alloc(256*256*4);
 for(let j=0;j<flat.length;j+=4){
   let rgba=[0,0,0,0];
   for(const im of layers){ const sa=im.data[j+3]/255, da=rgba[3]/255, a=sa+da*(1-sa); if(!a) continue;
     for(let c=0;c<3;c++) rgba[c]=Math.round((im.data[j+c]*sa+rgba[c]*da*(1-sa))/a);
     rgba[3]=Math.round(a*255);
   }
   flat.set(rgba,j);
 }
 if(!byteEqual(flat,comp.data)) problems.push(`${n} layer recomposition mismatch`);
 const nativeOpaque=[]; for(let y=0;y<128;y++)for(let x=0;x<128;x++)if(native.data[(y*128+x)*4+3])nativeOpaque.push([x,y]);
 const ground=Math.max(...nativeOpaque.map(p=>p[1])); bounds.push({frame:i,bodyOpaqueBounds:[Math.min(...nativeOpaque.map(p=>p[0])),Math.min(...nativeOpaque.map(p=>p[1])),Math.max(...nativeOpaque.map(p=>p[0])),ground],durationMs:durations[i]});
}
for(const direction of ['front_r','front_l']){
 const dir=`characters/orc-v1/source/rear-recovery-v2/${direction}/Unarmed`;
 for(const i of [0,1,3,4]){
  const n=String(i).padStart(2,'0');
  const a=decode(path.join(ROOT,`characters/orc-v1/source/complete-v1/${direction}/Unarmed/${n}.png`)).image.data;
  const b=decode(path.join(ROOT,dir,`${n}.png`)).image.data;
  if(!byteEqual(a,b))problems.push(`${direction} unchanged F${n} differs from baseline`);
 }
 const comp=decode(path.join(ROOT,dir,'02.png')).image, native=decode(path.join(ROOT,dir,'native/02.png')).image;
 const crop=Buffer.alloc(128*128*4);
 for(let y=0;y<128;y++)comp.data.copy(crop,y*128*4,((y+64)*256+64)*4,((y+64)*256+192)*4);
 if(!byteEqual(crop,native.data))problems.push(`${direction} F02 native is not body-only composite crop`);
}
const clipPath=path.join(ROOT,d,'clip.json');
const clip=JSON.parse(fs.readFileSync(clipPath,'utf8'));
if(clip.totalDurationMs!==730||clip.frameCount!==8||clip.nativeCanvas.join('x')!=='128x128')problems.push('clip metadata duration/frame/native contract');
for(const [p,h] of [[clip.master,clip.masterSha256],[clip.bodyMaster,clip.bodyMasterSha256],[clip.nativeMaster,clip.nativeMasterSha256],[clip.strip,clip.stripSha256]]){
 const f=path.join(ROOT,p);if(!fs.existsSync(f))problems.push(`missing metadata source ${p}`);else if(hash(fs.readFileSync(f))!==h)problems.push(`metadata source hash mismatch ${p}`);
}
for(let i=0;i<clip.frames.length;i++){
 const f=clip.frames[i];
 for(const [key,hkey] of [['png','sha256'],['nativePng','nativeSha256']])
   if(hash(fs.readFileSync(path.join(ROOT,f[key])))!==f[hkey])problems.push(`metadata hash mismatch ${key} frame ${i}`);
 for(const layer of Object.values(f.layers))if(hash(fs.readFileSync(path.join(ROOT,layer.png)))!==layer.sha256)problems.push(`metadata layer hash mismatch frame ${i}`);
}
function gifDelays(file){const b=fs.readFileSync(file),v=[];for(let i=0;i<b.length-7;i++)if(b[i]===0x21&&b[i+1]===0xf9&&b[i+2]===4)v.push(b.readUInt16LE(i+4)*10);return v;}
const gifChecks=[];
for(const [name,want] of [['1x',durations],['075x',[120,110,120,110,130,110,130,150]],['05x',durations.map(ms=>ms*2)]]){
 const file=path.join(ROOT,'experiments/main-orc-rear-recovery-v2',`back_r-sword-representative-${name}.gif`);
 const got=gifDelays(file);
 if(!byteEqual(Buffer.from(got),Buffer.from(want)))problems.push(`${name} GIF frame delays ${got} expected ${want}`);
 gifChecks.push({file:path.relative(ROOT,file).replaceAll('\\','/'),frameDelaysMs:got,expectedMs:want,sha256:hash(fs.readFileSync(file))});
}
const result={status:problems.length?'FAIL':'PASS',frames:bounds,gifChecks,problems,
 checks:['exact four-layer recomposition','native128 equals body-only crop','body bounds/ground row measured','front F02 retains unchanged frames 00/01/03/04 and exports body-only native128','representative clip paths/frame hashes match metadata','Aseprite review GIF delays checked']};
const out=path.join(ROOT,'experiments/main-orc-rear-recovery-v2/composed-cycle-verification.json');
fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2)); if(problems.length)process.exitCode=1;
