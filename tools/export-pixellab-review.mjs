// Export review-only masters through the existing local Aseprite bridge.
import fs from 'node:fs';
import {hash} from '../src/core.mjs';
import {exportAseprite} from '../src/aseprite.mjs';
const selected=JSON.parse(fs.readFileSync('experiments/pixellab-independent-orc-v1/selected-candidates.json','utf8'));
const jobs=[];
for(const c of selected){
 const base='characters/'+c.id;
 jobs.push({id:c.id+'-concept',source:base+'/source/aseprite/concept-selected.aseprite',compare:[base+'/concepts/concept-selected.png'],profile:{width:128,height:128,frames:1,alpha:'any',requireTransparency:true}});
 for(const state of ['Idle','Walk']){
  const clip=JSON.parse(fs.readFileSync(base+'/source/studies/'+state+'/clip.json','utf8'));
  jobs.push({id:c.id+'-'+state.toLowerCase(),source:clip.master,sourceSha256:clip.masterSha256,compare:clip.frames.map(f=>f.png),profile:{width:128,height:128,frames:8,durationMs:100,alpha:'any',requireTransparency:true}});
 }
}
for(const j of jobs)j.sourceSha256=hash(fs.readFileSync(j.source));
const manifest={schemaVersion:1,id:'pixellab-orcs-independent-v1',kind:'enemy',purpose:'Candidate review only; no character slots or Unity integration',jobs};
fs.writeFileSync('experiments/pixellab-independent-orc-v1/editor.json',JSON.stringify(manifest,null,2)+'\n');
const result=exportAseprite(manifest);
fs.writeFileSync('reports/pixellab-master-roundtrip.json',JSON.stringify({status:result.status,path:result.path,summary:result.summary,artisticApproval:'PENDING_CREATOR',UnityIntegration:'NOT_RUN'},null,2)+'\n');
console.log(JSON.stringify({status:result.status,path:result.path,summary:result.summary}));
