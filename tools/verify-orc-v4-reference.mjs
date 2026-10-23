import fs from 'node:fs';import {ROOT,inside,readJSON,hash,json,now} from '../src/core.mjs';
import {executeAseprite,findAseprite} from '../src/aseprite.mjs';
const prepared=readJSON(inside(ROOT,'reports/orc-production-v4-prepared.json'));
const before=new Map(prepared.jobs.map(j=>[j.source,hash(fs.readFileSync(inside(ROOT,j.source)))]));
const result=executeAseprite(findAseprite(),['--script-param',`root=${ROOT}`,'--script',inside(ROOT,'tools/aseprite/verify-orc-v4-reference.lua')],300000);
for(const [file,sha]of before)if(hash(fs.readFileSync(inside(ROOT,file)))!==sha)throw Error('Verification modified master');
if(!result.stdout.includes('PASS: 856 original cels exact'))throw Error('Reference count mismatch');
json(inside(ROOT,'reports/orc-production-v4-saved-reference-check.json'),{status:'PASS',createdAt:now(),savedMasters:before.size,referenceCels:856,mastersUnchanged:true,result:result.stdout.trim()});console.log(result.stdout.trim());
