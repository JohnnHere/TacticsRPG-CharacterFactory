// Orchestration only. Every new art pixel is drawn/saved by the Lua inside Aseprite.
import fs from 'node:fs';
import path from 'node:path';
import {ROOT,hash} from '../src/core.mjs';
import {findAseprite,executeAseprite,exportAseprite,inspectAseprite} from '../src/aseprite.mjs';
const id='orc-01-aseprite-v3',base=`characters/${id}`,source=`${base}/source/aseprite`;
const read=p=>JSON.parse(fs.readFileSync(path.join(ROOT,p),'utf8'));
const write=(p,v)=>{fs.mkdirSync(path.dirname(path.join(ROOT,p)),{recursive:true});fs.writeFileSync(path.join(ROOT,p),JSON.stringify(v,null,2)+'\n');};
const stamp=p=>hash(fs.readFileSync(path.join(ROOT,p)));
const script=`${source}/author-orc-v3.lua`,out=`${source}/authored`;
const text=fs.readFileSync(path.join(ROOT,script),'utf8');
// Reject raster-loading APIs in this specific all-new authorship exercise.
if(/fromFile\s*=|app\.open\s*\(|loadfile\s*\(|dofile\s*\(/.test(text))throw Error('Raster/input load in author script.');
const executable=findAseprite(),started=performance.now();
const run=dest=>executeAseprite(executable,['--script-param','output='+path.join(ROOT,dest),'--script',path.join(ROOT,script)]);
run(out);const elapsedMs=Math.round(performance.now()-started);
executeAseprite(executable,['--script-param','source='+path.join(ROOT,out),'--script-param','output='+path.join(ROOT,source,'components'),'--script',path.join(ROOT,'tools/aseprite/export-orc-v3-components.lua')]);
// Independent rerun into ignored scratch; compare final RGBA/source bytes.
const rerun=`tmp/orc-aseprite-v3-repro/${stamp(script).slice(0,16)}`;run(rerun);
const authored=read(`${out}/authorship.json`),jobs=[],checks=[];
for(const doc of authored.documents){
 const header=inspectAseprite(path.join(ROOT,out,doc.id+'.aseprite'));
 const files=doc.frames.map(f=>`${out}/${doc.id}/${f.file}`);
 for(const file of files){const other=file.replace(out,rerun);if(stamp(file)!==stamp(other))throw Error('Non-deterministic PNG '+file);}
 if(stamp(`${out}/${doc.id}.aseprite`)!==stamp(`${rerun}/${doc.id}.aseprite`))throw Error('Non-deterministic source '+doc.id);
 checks.push({id:doc.id,...header,sourceSha256:stamp(`${out}/${doc.id}.aseprite`),frames:files.map(file=>({file,sha256:stamp(file)})),deterministicPngAndSource:true});
 jobs.push({id:doc.id+'-front-r',source:`${out}/${doc.id}.aseprite`,sourceSha256:stamp(`${out}/${doc.id}.aseprite`),profile:{width:128,height:128,frames:files.length,durationsMs:doc.frames.map(f=>f.durationMs),groundY:126,alpha:'binary',requireContent:true,requireTransparency:true},compare:files});
}
const manifest={schemaVersion:1,id:'orc-aseprite-authorship-v3',kind:'character',characterId:id,jobs};
write(`${source}/editor.json`,manifest);
const build=exportAseprite(manifest);
build.preview=build.path+'/preview.html';
const v2=read('reports/orc-refinement-candidates-v2.json');
const previous=read('reports/orc-assets-audit-v2.json');
const changed=previous.protectedFiles.filter(f=>stamp(f.file)!==f.sha256);if(changed.length)throw Error('Approved original art changed: '+changed.map(x=>x.file));
const referenceFiles=[v2.concept,...v2.clips.flatMap(c=>c.after),'references/tacticsrpg/Docs/Art/References/character_style_anchor_v1.png','references/tacticsrpg/Assets/Resources/Characters/WarriorPilot/warrior_pilot_mvp1_static_128.png'];
const report={schemaVersion:1,status:'TECHNICAL_PASS_ART_REVIEW_PENDING',createdAt:new Date().toISOString(),author:'Codex agent',pixelEngine:'Aseprite Steam Lua',method:'Original explicit pixel drawings, material planes and individually authored action silhouettes. Scripted authorship, not mouse drawing.',externalArtGenerationCalls:0,externalImageInputsToAuthor:0,postExportRasterEditing:0,sourceScript:{file:script,sha256:stamp(script)},referencePolicy:'Images observed as visual references only; no image bytes sampled or imported into authored art.',references:referenceFiles.map(file=>({file,sha256:stamp(file)})),authoringElapsedMs:elapsedMs,checks,protectedOriginalFilesUnchanged:previous.protectedFiles.length,editorBuild:{path:build.path,preview:build.preview,summary:build.summary},approval:'PENDING_CREATOR',limitations:['This demonstrates agent-authored Lua pixel craft in Aseprite, not the maximum artistic quality of the editor or a built-in image generator.','Nine regional layers, not a complete reusable equipment rig. Removing armor does not expose a finished nude body.','Concept is native 128x128; V2 concept is high resolution. Compare native combat at equal resolution.','Only front_r concept/Attack/Hit study; not a new complete production character.','No runtime Unity or weapons/events/bindings implemented.']};
write(`${source}/provenance.json`,report);write('reports/orc-aseprite-authorship-v3.json',report);
console.log(JSON.stringify({status:report.status,elapsedMs,build:report.editorBuild,protectedFiles:report.protectedOriginalFilesUnchanged},null,2));
