// Read-only production check: fresh exports from all nine repaired saved masters,
// including each of the four independently selectable composite layers.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {PNG} from 'pngjs';
import {checkAseprite,executeAseprite,inspectAseprite} from '../../../src/aseprite.mjs';
const O='experiments/main-orc-rear-recovery-v2/qa-revision-1-repair';
const ed=checkAseprite();if(ed.status!=='AVAILABLE')throw Error('Aseprite unavailable');
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const read=p=>PNG.sync.read(fs.readFileSync(p));
const result={status:'PASS',editor:ed.version,productionReadOnly:true,sets:[],failures:[]};
const specs=[['SwordL','back_l','Sword'],['AxeR','back_r','Axe'],['AxeL','back_l','Axe']];
for(const [key,d,a]of specs){
 const c=JSON.parse(fs.readFileSync(`characters/orc-v1/source/rear-recovery-v2/${d}/${a}/Attack-representative-v1/clip.json`));
 const sets=[['composite',c.master,256,null,f=>f.png],['body',c.bodyMaster,256,null,f=>f.layers.body.png],['native',c.nativeMaster,128,null,f=>f.nativePng],...c.layerOrder.map(l=>[l,c.master,256,l,f=>f.layers[l].png])];
 for(const [kind,master,size,layer,target]of sets){
  const out=`${O}/source-proof/${key}/${kind}`;fs.mkdirSync(out,{recursive:true});
  const digest=sha(master),info=inspectAseprite(path.resolve(master));
  const args=[...(layer?['--layer',layer]:[]),path.resolve(master),'--sheet-type','horizontal','--format','json-array','--sheet',path.resolve(out,'sheet.png'),'--data',path.resolve(out,'sheet.json')];
  executeAseprite(ed.executable,args);
  const im=read(`${out}/sheet.png`),meta=JSON.parse(fs.readFileSync(`${out}/sheet.json`));
  const frames=[];
  if(info.width!==size||info.height!==size||meta.frames.length!==8)result.failures.push(`${key}/${kind} source geometry/frame count`);
  for(let i=0;i<8;i++){
   const r=meta.frames[i].frame,want=read(target(c.frames[i]));let differences=0;
   for(let y=0;y<size;y++)for(let x=0;x<size;x++)for(let j=0;j<4;j++)if(im.data[((r.y+y)*im.width+r.x+x)*4+j]!==want.data[(y*size+x)*4+j])differences++;
   const duration=meta.frames[i].duration;
   if(differences||duration!==c.frames[i].durationMs)result.failures.push(`${key}/${kind}/F${i} diff=${differences} duration=${duration}`);
   frames.push({index:i,differingRgbaBytes:differences,durationMs:duration,target:target(c.frames[i])});
  }
  if(sha(master)!==digest)result.failures.push(`${key}/${kind} source mutated during read-only export`);
  result.sets.push({cell:`${d}/${a}`,kind,master,masterSha256:digest,frames});
 }
 console.log(`Fresh saved-source exports checked ${key}: composite/body/native +4 layers, 56 frame comparisons`);
}
result.status=result.failures.length?'FAIL':'PASS';result.freshFrameComparisons=result.sets.reduce((n,s)=>n+s.frames.length,0);
fs.writeFileSync(`${O}/source-proof.json`,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:result.status,freshFrameComparisons:result.freshFrameComparisons,failures:result.failures}));
if(result.failures.length)process.exitCode=1;
