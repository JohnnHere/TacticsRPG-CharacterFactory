import fs from 'node:fs';
const id=process.argv[2];
if(!['back_l-sword','back_r-axe'].includes(id))throw Error('unauthorized target');
const req=JSON.parse(fs.readFileSync(`experiments/main-orc-rear-recovery-v2/inputs/${id}-request.json`,'utf8'));
const b64=fs.readFileSync(`experiments/main-orc-rear-recovery-v2/inputs/${id}-native128.png`).toString('base64');
process.stdout.write(JSON.stringify({request:req,first_frame_url:`data:image/png;base64,${b64}`}));
