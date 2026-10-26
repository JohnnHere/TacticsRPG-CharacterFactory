// Store allowlisted provenance only; never copy account/settings records.
import fs from 'node:fs';import path from 'node:path';import {ROOT} from '../src/core.mjs';
const [id,state,model,history,archive]=process.argv.slice(2);
if(!/^orc-pixellab-0[4-7]$/.test(id)||!['Idle','Walk','Concept'].includes(state)||!/^generate_[a-z_]+$/.test(model)||!/^\d{14}\.json$/.test(history)||!archive||path.basename(archive)!==archive)throw Error('Invalid request metadata');
const file=path.join(ROOT,'experiments/pixellab-orc-refinement-v2/brief.json');const brief=JSON.parse(fs.readFileSync(file,'utf8'));
const h=JSON.parse(fs.readFileSync(path.join(process.env.APPDATA,'Aseprite/extensions/pixellab/request_history',model,history),'utf8'));
const job=state==='Concept'?brief.concept05:brief.jobs.find(j=>j.id===id&&j.state===state);if(!job)throw Error('Job missing');
if(job.requestHistory&&job.requestHistory!==history){job.attempts??=[];job.attempts.push({requestHistory:job.requestHistory,model:job.model,archive:job.archive,submittedPrompt:job.submittedPrompt,seed:job.seed,status:job.status});}
job.submittedPrompt=h.description??h.action;job.requestHistory=history;job.model=model;job.archive=archive;job.seed=h.seed;job.requestedFrameCount=h.frame_count??null;job.status='SUBMITTED_WAITING_OUTPUT';job.submittedAt=new Date().toISOString();
job.requestSettings={cameraView:h.view??null,direction:h.direction??null,frameCount:h.frame_count??null};
brief.status='GENERATING_REFINEMENTS';brief.remainingScope=['After these refinements, create two additional Orc concepts with different visual patterns, using project inspirations.'];
fs.writeFileSync(file,JSON.stringify(brief,null,2)+'\n');console.log(JSON.stringify({id,state,model,history,archive,promptMatchesPlan:job.prompt===job.submittedPrompt}));
