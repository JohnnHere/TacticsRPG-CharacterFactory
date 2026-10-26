// Read durable results from the official extension; never sends generation
// requests or reads its account/package/preferences. Packaging runs in Aseprite.
import fs from 'node:fs';import path from 'node:path';import {spawnSync} from 'node:child_process';
import {ROOT} from '../src/core.mjs';import {decode} from '../src/images.mjs';
const archiveRoot=path.join(process.env.APPDATA,'Aseprite/extensions/pixellab/generation_history');
const jobs=JSON.parse(fs.readFileSync(path.join(ROOT,'experiments/pixellab-independent-orc-v1/jobs.json'),'utf8'));
const result=[];
for(const j of jobs){
 const output=path.join(ROOT,'characters',j.id,'source/studies',j.state,'clip.json');if(fs.existsSync(output)){result.push({...j,status:'PACKAGED'});continue;}
 const folder=fs.readdirSync(archiveRoot).find(n=>n.endsWith(' - '+String(j.job).padStart(3,'0')));
 if(!folder||fs.readdirSync(path.join(archiveRoot,folder)).filter(n=>/^\d+\.png$/.test(n)).length!==9){result.push({...j,status:'WAITING_PROVIDER'});continue;}
 const input=decode(path.join(archiveRoot,folder,'0.png')).image,concept=decode('characters/'+j.id+'/concepts/concept-selected.png').image;
 if(!input.data.equals(concept.data))throw Error('Archive input mismatch: '+j.id+' '+j.state);
 const packaged=spawnSync(process.execPath,['tools/import-pixellab-animation.mjs',j.id,j.state,folder,j.history],{cwd:ROOT,windowsHide:true,encoding:'utf8'});
 if(packaged.status!==0)throw Error(packaged.stderr||packaged.stdout);result.push({...j,status:'PACKAGED',archive:folder});
}
fs.writeFileSync(path.join(ROOT,'reports/pixellab-jobs-status.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result.map(j=>({id:j.id,state:j.state,status:j.status}))));
