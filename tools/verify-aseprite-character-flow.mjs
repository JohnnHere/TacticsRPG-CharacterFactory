// Exercise the public CLI on a real approved clip without changing production pixels.
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
import {ROOT,inside,readJSON,json,hash,pngFiles,slash,now} from '../src/core.mjs';
const name='idle-front-r-editor-v1', character='orc-01';
const folder=`characters/${character}/source/aseprite/${name}`,manifest=folder+'/editor.json';
const stamp=file=>hash(fs.readFileSync(inside(ROOT,file)));
const protectedFiles=[`characters/${character}/reviews.json`,`characters/${character}/assets.json`,...pngFiles(inside(ROOT,`characters/${character}/sprites`)).map(p=>slash(path.relative(ROOT,p)))];
const before=protectedFiles.map(file=>({file,sha256:stamp(file)}));
function cli(args){const p=spawnSync(process.execPath,[path.join(ROOT,'src/cli.mjs'),...args],{cwd:ROOT,windowsHide:true,encoding:'utf8',timeout:120000});if(p.error||p.status!==0)throw Error(p.error?.message??p.stderr??p.stdout);return JSON.parse(p.stdout);}
if(!fs.existsSync(inside(ROOT,manifest)))cli(['editor-fork','--manifest','reports/aseprite-production-manifest-v1.json','--id',character,'--job','orc-01-00','--name',name]);
const exported=cli(['editor-export','--manifest',manifest]);
const applied=cli(['editor-apply','--id',character,'--build',exported.path]);
assert.equal(applied.status,'UNCHANGED','Unedited fork must preserve production files without --force');
for(const p of before)assert.equal(stamp(p.file),p.sha256,p.file);
const working=readJSON(inside(ROOT,manifest)).jobs[0].source;
const report={status:'PASS',createdAt:now(),commands:['editor-fork','editor-export','editor-apply'],workingSource:working,workingManifest:manifest,build:exported.path,preview:exported.preview,frames:exported.summary.frames,applyResult:applied,protectedFiles:before,creatorReviewsChanged:false,reuseAssessment:[{component:'approved editable clip',category:'REUSE_DIRECT',evidence:'lineage.json and matching RGBA export',adaptation:'Independent saved working copy; no artistic changes',risk:'Future edits require existing gates/review',validation:'UNEDITED_APPLY_UNCHANGED'},{component:'Aseprite CLI bridge',category:'CREATE_NEW',evidence:'src/aseprite.mjs + tools/aseprite/bridge.lua',validation:'REAL_EDITOR_EXPORT_AND_APPLY_PASS'},{component:'Unity terrain/equipment rendering',category:'REQUIRES_EXTENSION',evidence:'docs/ARCHITECTURE.md and docs/EQUIPMENT_AND_ACTIONS.md',validation:'NOT_RUN'}],unityIntegration:'NOT_RUN'};
json(inside(ROOT,'reports/aseprite-character-flow-v1.json'),report);console.log(JSON.stringify({status:report.status,workingSource:working,build:exported.path,frames:report.frames,applyResult:applied},null,2));
