// Read only: package metadata detection, never reads credentials or plugin settings.
import fs from 'node:fs';
import path from 'node:path';
import {ROOT} from '../src/core.mjs';
import {checkAseprite} from '../src/aseprite.mjs';
const configRoot=process.env.APPDATA?path.join(process.env.APPDATA,'Aseprite'):null;
const extensionRoot=configRoot?path.join(configRoot,'extensions'):null;
const packages=[];
if(extensionRoot&&fs.existsSync(extensionRoot))for(const dir of fs.readdirSync(extensionRoot,{withFileTypes:true})){
 if(!dir.isDirectory())continue;
 const file=path.join(extensionRoot,dir.name,'package.json');if(!fs.existsSync(file))continue;
 try{const p=JSON.parse(fs.readFileSync(file,'utf8'));if(/pixel\s*lab/i.test([p.name,p.displayName,p.description,dir.name].join(' ')))packages.push({directory:dir.name,name:p.name??null,displayName:p.displayName??null,version:p.version??null,scriptContributions:p.contributes?.scripts?.length??0});}catch{if(/pixellab/i.test(dir.name))packages.push({directory:dir.name,status:'PACKAGE_METADATA_UNREADABLE'});}
}
const result={status:packages.length?'FILES_DETECTED_OPERATIONAL_CHECK_REQUIRED':'NOT_INSTALLED_WAITING_ACCOUNT_DOWNLOAD',date:'2026-10-23',editor:checkAseprite(),extensionPackages:packages,authentication:'NOT_VERIFIED_BY_FILES_ONLY',generation:'NOT_VERIFIED_BY_FILES_ONLY',credentialsRead:false,cloudCalls:'none',batchProfile:'tmp/aseprite-batch-profile (separate from GUI)',officialSource:'https://www.pixellab.ai/docs/installation',experiment:'experiments/pixellab-independent-orc-v1/experiment.json'};
const report=path.join(ROOT,'reports/pixellab-integration-status.json');fs.mkdirSync(path.dirname(report),{recursive:true});fs.writeFileSync(report,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
