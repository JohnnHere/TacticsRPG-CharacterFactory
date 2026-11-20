// Run the unchanged repository exporter inside a local factory mirror.
// Its fixed dist/editor and tmp destinations are thus confined to this experiment.
import fs from 'node:fs';import path from 'node:path';import {pathToFileURL} from 'node:url';
const E='experiments/main-orc-hybrid-weapon-04',P=E+'/pipeline';
for(const file of ['src/core.mjs','src/images.mjs','src/aseprite.mjs','tools/aseprite/bridge.lua']){fs.mkdirSync(path.dirname(P+'/'+file),{recursive:true});fs.copyFileSync(file,P+'/'+file)}
fs.writeFileSync(P+'/package.json','{"type":"module"}');
process.env.ASEPRITE_PATH='F:/SteamLibrary/steamapps/common/Aseprite/Aseprite.exe';
const jobs=[];const times=[30,65,35,50,45,35,30,35,35,100,55,80,45,90];
for(const v of ['a','b']){fs.mkdirSync(P+'/sources',{recursive:true});fs.copyFileSync(`${E}/full/${v}/composite.aseprite`,`${P}/sources/${v}.aseprite`);jobs.push({id:'sword-'+v,source:`sources/${v}.aseprite`,profile:{width:256,height:256,frames:14,durationsMs:times,alpha:'binary',requireTransparency:true},targets:Array.from({length:14},(_,i)=>`${v}/${i}.png`)})}
fs.writeFileSync(P+'/manifest.json',JSON.stringify({schemaVersion:1,id:'hybrid-weapon-04',kind:'weapon',jobs}));
const {exportAseprite}=await import(pathToFileURL(path.resolve(P,'src/aseprite.mjs')));
const result=exportAseprite('manifest.json');fs.writeFileSync(E+'/pipeline-result.json',JSON.stringify(result,null,2));console.log(JSON.stringify({status:result.status,path:P+'/'+result.path}));

