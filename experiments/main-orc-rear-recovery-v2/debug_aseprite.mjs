import {spawnSync} from 'node:child_process';
import {checkAseprite} from '../../src/aseprite.mjs';
const ed=checkAseprite();
const r=spawnSync(ed.executable,['--batch','--noinapp','--script',process.argv[2]],{cwd:process.cwd(),encoding:'utf8',windowsHide:true,env:{...process.env,ASEPRITE_USER_FOLDER:process.cwd()+'/tmp/aseprite-batch-profile'}});
console.log(JSON.stringify({status:r.status,error:r.error?.message,stdout:r.stdout,stderr:r.stderr},null,2));
