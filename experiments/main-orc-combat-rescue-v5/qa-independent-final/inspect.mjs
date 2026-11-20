import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';
const out=path.dirname(new URL(import.meta.url).pathname.replace(/^\/(?=[A-Za-z]:)/,''));
const dir=decodeURIComponent(out);
const m=JSON.parse(fs.readFileSync('characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json'));
for(const cell of m.cells){
 const clip=JSON.parse(fs.readFileSync(cell.clipJson));
 for(const kind of ['composite',...(clip.frames[0].layers?['body']:[])]){
  const sheet=new PNG({width:1024,height:Math.ceil(clip.frames.length/4)*256});
  clip.frames.forEach((f,i)=>{
   const im=PNG.sync.read(fs.readFileSync(kind==='body'?f.layers.body.png:f.png));
   PNG.bitblt(im,sheet,0,0,im.width,im.height,(i%4)*256,Math.floor(i/4)*256);
  });
  fs.writeFileSync(path.join(dir,`${cell.direction}-${cell.action}-${kind}.png`),PNG.sync.write(sheet));
 }
}
console.log('28 composite grids and 8 whole-body layers-off grids written; diagnostic layouts only.');
