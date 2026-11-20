import fs from 'node:fs';
import path from 'node:path';
import { ROOT } from '../../src/core.mjs';
import { exportAseprite, checkAseprite } from '../../src/aseprite.mjs';
import { decode } from '../../src/images.mjs';
import { PNG } from 'pngjs';

const ed=checkAseprite();
if(ed.status!=='AVAILABLE') throw Error('Aseprite unavailable');
const definitions=[
  {id:'representative-sword-back-r-v2',master:'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-attack-representative-v2.aseprite',dir:'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2',count:8,durations:[90,80,90,80,100,80,100,110]},
  ...['front_r','front_l'].map(d=>({id:`unarmed-f02-${d}`,master:`characters/orc-v1/source/aseprite/rear-recovery-v2/composite/${d}/unarmed-attack.aseprite`,dir:`characters/orc-v1/source/rear-recovery-v2/${d}/Unarmed`,count:5,durations:[80,110,50,90,120]}))
];
const manifest={schemaVersion:1,id:'main-orc-rear-recovery-v2-representative-export',kind:'character',characterId:'orc-v1',jobs:definitions.map(d=>({id:d.id,source:d.master,profile:{width:256,height:256,frames:d.count,durationsMs:d.durations,alpha:'any',requireContent:true,requireTransparency:true}}))};
const result=exportAseprite(manifest);
if(result.status!=='PASS') throw Error(`Export failed: ${JSON.stringify(result)}`);
let framesChecked=0, byteDiffs=0, timingErrors=0;
for(const d of definitions){
  const job=path.join(ROOT,result.path,'jobs',d.id);
  const sheet=decode(path.join(job,'sheet.png')).image;
  const sheetMeta=JSON.parse(fs.readFileSync(path.join(job,'sheet.json'),'utf8'));
  if(sheet.width!==d.count*256||sheet.height!==256) throw Error(`${d.id}: unexpected exported sheet dimensions ${sheet.width}x${sheet.height}`);
  for(let i=0;i<d.count;i++){
    const exp=Buffer.alloc(256*256*4);
    for(let y=0;y<256;y++){
      const src=(y*sheet.width+i*256)*4, dst=y*256*4;
      sheet.data.copy(exp,dst,src,src+256*4);
    }
    const p=path.join(ROOT,d.dir,`${String(i).padStart(2,'0')}.png`);
    const want=decode(p).image.data;
    const diffs=exp.equals(want)?0:exp.reduce((n,v,j)=>n+(v!==want[j]),0);
    if(diffs) byteDiffs++;
    const got=sheetMeta.frames[i]?.duration;
    if(got!==d.durations[i]) timingErrors++;
    framesChecked++;
    console.log(`${diffs===0?'PASS':'FAIL'} ${d.id} f${String(i).padStart(2,'0')} pixels=${diffs} duration=${got}/${d.durations[i]}ms`);
  }
}
const report={status:byteDiffs===0&&timingErrors===0?'PASS':'FAIL',build:result.path,framesChecked,byteMismatchFrames:byteDiffs,timingErrors,sourceMasters:definitions.map(d=>d.master)};
fs.writeFileSync(path.join(ROOT,'experiments/main-orc-rear-recovery-v2/representative-export-verification.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
if(report.status!=='PASS') process.exitCode=1;
