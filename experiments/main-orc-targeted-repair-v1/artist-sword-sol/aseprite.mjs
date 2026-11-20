// Private hidden batch wrapper. Does not touch Unarmed's wrapper/profile.
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {findAseprite} from '../../../src/aseprite.mjs';
const E='experiments/main-orc-targeted-repair-v1/artist-sword-sol';
const profile=path.resolve(E,'batch-profile');fs.mkdirSync(profile,{recursive:true});
const exe=findAseprite(),args=['--batch','--noinapp',...process.argv.slice(2)];
const r=spawnSync(exe,args,{cwd:process.cwd(),env:{...process.env,ASEPRITE_USER_FOLDER:profile},windowsHide:true,encoding:'utf8',timeout:120000,maxBuffer:8*1024*1024});
const log={executable:exe,args,mode:'hidden --batch --noinapp',isolatedProfile:profile,exitCode:r.status,stdout:r.stdout,stderr:r.stderr,error:r.error?.message};
fs.writeFileSync(path.resolve(E,'last-aseprite-run.json'),JSON.stringify(log,null,2)+'\n');
if(r.stdout)process.stdout.write(r.stdout);if(r.stderr)process.stderr.write(r.stderr);if(r.error)throw r.error;if(r.status!==0||/Error:|Error creating directory/i.test(r.stderr??''))throw Error('Aseprite batch failed');
