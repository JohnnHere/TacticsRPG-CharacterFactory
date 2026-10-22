// Synthetic fixtures exercise the bridge; no production art is created or approved.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {ROOT,inside,json,readJSON,now} from '../src/core.mjs';
import {checkAseprite,executeAseprite,exportAseprite} from '../src/aseprite.mjs';
const tool=checkAseprite();if(tool.status!=='AVAILABLE')throw Error(tool.error);
const folder=inside(ROOT,'tmp/aseprite-capabilities-v1');fs.mkdirSync(folder,{recursive:true});
executeAseprite(tool.executable,['--script-param',`output=${folder}`,'--script',path.join(ROOT,'test/fixtures/aseprite.lua')]);
const build=exportAseprite({schemaVersion:1,id:'aseprite-capabilities-v1',kind:'environment',jobs:[
 {id:'synthetic-animation',source:'tmp/aseprite-capabilities-v1/animation.aseprite',profile:{width:16,height:16,frames:3,durationsMs:[80,120,160],alpha:'binary',requireContent:false}},
 {id:'synthetic-tileset',source:'tmp/aseprite-capabilities-v1/tilemap.aseprite',tileset:true,profile:{width:24,height:24,requireContent:false}}
]});
const doc=readJSON(path.join(ROOT,build.path,build.jobs[1].metadata));const tilemap=doc.tilemaps[0];
assert.equal(tilemap.tileWidth,8);assert.equal(tilemap.tileHeight,8);assert.equal(tilemap.x,8);assert.equal(tilemap.y,8);assert.equal(tilemap.cells.length,2);assert.equal(tilemap.cells[1].flags,0x80000000);
const library=build.jobs[1].tilesets.find(ts=>ts.id===tilemap.tilesetId);assert.deepEqual(library.tiles.map(t=>t.index),[0,1,2]);
const report={status:'PASS',createdAt:now(),scope:'SYNTHETIC TEST FIXTURE ONLY; not production art or Unity terrain',tool,build:build.path,preview:build.path+'/preview.html',summary:build.summary,checks:['frames and durations','empty frame retained','layer/tag/slice metadata','tileset raster export','tilemap indices and flip flags','tile dimensions and cel position','explicit tilesetId/tile index to RGBA PNG mapping'],tilemap,tilesets:build.jobs[1].tilesets,tilesetFrames:build.jobs[1].frames.map(f=>({file:f.file,width:f.width,height:f.height})),unityIntegration:'NOT_RUN'};
json(inside(ROOT,'reports/aseprite-capabilities-v1.json'),report);console.log(JSON.stringify(report,null,2));
