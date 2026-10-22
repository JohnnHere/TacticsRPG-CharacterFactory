import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { ROOT, inside, write, json, readJSON, hash, loadCharacter, approval } from '../src/core.mjs';
import { createCharacter } from '../src/workflow.mjs';
import { run } from '../src/cli.mjs';
import { decode, savePNG } from '../src/images.mjs';
import { PNG } from 'pngjs';
import { checkAseprite, findAseprite, executeAseprite, inspectAseprite, exportAseprite, verifyEditorBuild, createEditorTemplate, forkEditorSources, applyCharacterBuild } from '../src/aseprite.mjs';

test('editor discovery rejects explicit invalid path; malformed manifests cannot escape workspace',()=>{
  assert.throws(()=>findAseprite(path.join(ROOT,'tmp/definitely-missing.exe')),/ausente/);
  assert.throws(()=>exportAseprite({schemaVersion:1,id:'bad-asset',kind:'prop',jobs:[{id:'bad-source',source:'../TacticsRPG/other.aseprite',profile:{width:16,height:16}}]}),/fora do pacote/);
});

const available=checkAseprite();
test('real Aseprite bridge: frames, layers, tags, tilemap, source preservation, immutable builds, templates and gated apply',{skip:available.status!=='AVAILABLE'?'Aseprite optional: set ASEPRITE_PATH':false},()=>{
  const name='test-editor-'+crypto.randomBytes(5).toString('hex');
  const temp=inside(ROOT,'tmp/'+name);fs.mkdirSync(temp,{recursive:true});
  const outputs=[];let character;
  const manifest=(suffix,job)=>({schemaVersion:1,id:name+'-'+suffix,kind:'prop',jobs:[{id:'test-clip',source:`tmp/${name}/animation.aseprite`,profile:{width:16,height:16,frames:3,alpha:'binary',requireContent:false},...job}]});
  const build=m=>{const r=exportAseprite(m);outputs.push(path.join(ROOT,r.path));return r;};
  try {
    executeAseprite(available.executable,['--script-param',`output=${temp}`,'--script',path.join(ROOT,'test/fixtures/aseprite.lua')]);
    const original=hash(fs.readFileSync(path.join(temp,'animation.aseprite')));
    assert.deepEqual(inspectAseprite(path.join(temp,'animation.aseprite')).durationsMs,[80,120,160]);
    const normal=build(manifest('normal',{}));assert.equal(normal.summary.frames,3);
    assert.deepEqual(normal.jobs[0].frames.map(f=>f.durationMs),[80,120,160]);
    assert.equal(normal.jobs[0].frames[2].contentHeight,0,'empty frame retained');
    const first=decode(path.join(ROOT,normal.path,normal.jobs[0].frames[0].file)).image;
    assert.deepEqual([...first.data.subarray((12*16+2)*4,(12*16+2)*4+4)],[30,50,220,255]);
    const doc=readJSON(path.join(ROOT,normal.path,normal.jobs[0].metadata));assert.equal(doc.tags[0].name,'first-two');assert.equal(doc.slices[0].name,'socket');
    const selected=build(manifest('selected',{tag:'first-two',layers:['Body'],profile:{width:16,height:16,frames:2,durationsMs:[80,120],alpha:'binary'}}));
    assert.equal(selected.jobs[0].frames[0].rgbaSha256,selected.jobs[0].frames[1].rgbaSha256,'duplicate frame retained');
    assert.equal(hash(fs.readFileSync(path.join(temp,'animation.aseprite'))),original);
    const fork=forkEditorSources(manifest('fork',{}),name+'-fork');outputs.push(path.dirname(path.join(ROOT,fork.manifest)));
    assert.equal(hash(fs.readFileSync(path.join(ROOT,fork.sources[0]))),original);
    assert.equal(readJSON(path.join(ROOT,fork.manifest)).jobs[0].sourceSha256,undefined);
    assert.throws(()=>forkEditorSources(manifest('fork',{}),name+'-fork'),/ja existe/);
    assert.equal(exportAseprite(manifest('normal',{})).reused,true);
    assert.throws(()=>build(manifest('bad-layer',{layers:['Missing']})),/layer nao existe/);
    assert.throws(()=>build(manifest('bad-exclusion',{excludeLayers:['Missing']})),/layer nao existe/);
    assert.throws(()=>build(manifest('bad-timing',{profile:{width:16,height:16,frames:3,durationMs:90,requireContent:false}})),/duracao alterada/);
    assert.throws(()=>build(manifest('bad-source',{sourceSha256:'0'.repeat(64)})),/Fonte alterada/);

    const tile=build({schemaVersion:1,id:name+'-tiles',kind:'environment',jobs:[{id:'terrain',source:`tmp/${name}/tilemap.aseprite`,tileset:true,profile:{width:24,height:24,requireContent:false}}]});
    const layout=readJSON(path.join(ROOT,tile.path,tile.jobs[0].metadata)).tilemaps[0];
    assert.equal(layout.tileWidth,8);assert.equal(layout.tileHeight,8);assert.equal(layout.x,8);assert.equal(layout.y,8);
    assert.equal(layout.cells.length,2);assert.equal(layout.cells[1].flags,0x80000000);assert.ok(layout.cells.every(c=>c.tile>0));
    const library=tile.jobs[0].tilesets.find(ts=>ts.id===layout.tilesetId);
    assert.equal(library.tiles.length,3);assert.deepEqual(library.tiles.map(t=>t.index),[0,1,2]);
    assert.equal(tile.jobs[0].tilesets.length,2);assert.notEqual(tile.jobs[0].tilesets[0].id,tile.jobs[0].tilesets[1].id);
    for(const t of library.tiles)assert.equal(decode(path.join(ROOT,tile.path,t.file)).colorType,6);

    const templateFile=`tmp/${name}/template.json`;
    json(path.join(ROOT,templateFile),{schemaVersion:1,id:name,kind:'effect',profile:{width:16,height:16,frames:3,durationMs:100},layers:['Base','Glow']});
    const template=createEditorTemplate(templateFile);outputs.push(path.dirname(path.join(ROOT,template.request)));
    assert.equal(inspectAseprite(path.join(ROOT,template.source)).frames,3);
    assert.throws(()=>createEditorTemplate(templateFile),/ja existe/);
    assert.throws(()=>exportAseprite(template.manifest),/frame vazio/);

    // Only synthetic test data receives synthetic test approvals.
    createCharacter(name,'Humano','Warrior');character=loadCharacter(name);
    const png=new PNG({width:128,height:128});png.data.set([220,50,30,255],(126*128+64)*4);
    savePNG(path.join(temp,'body.png'),png);executeAseprite(available.executable,[path.join(temp,'body.png'),'--save-as',path.join(temp,'body.aseprite')]);
    const slot=name.replaceAll('-','_')+'_mvp1_static_128.png';
    const applied=build({schemaVersion:1,id:name+'-apply',kind:'character',characterId:name,jobs:[{id:'body',source:`tmp/${name}/body.aseprite`,profile:{width:128,height:128,groundY:126,frames:1},targets:[slot]}]});
    assert.throws(()=>applyCharacterBuild(name,applied.path),/Gate 1/);
    run(['import','--id',name,'--input',path.join(temp,'body.png'),'--kind','concept','--name','synthetic-fixture']);
    run(['review','--id',name,'--gate','concept','--decision','approved','--reviewer','SYNTHETIC TEST','--evidence','Synthetic pipeline fixture, not artwork']);
    assert.equal(applyCharacterBuild(name,applied.path).status,'APPLIED_REVIEW_REQUIRED');
    assert.equal(applyCharacterBuild(name,applied.path).status,'UNCHANGED');
    const target=path.join(character.dir,'sprites',slot);
    write(target,PNG.sync.write(png,{deflateLevel:1,colorType:6}));const alternativeEncoding=hash(fs.readFileSync(target));
    assert.equal(applyCharacterBuild(name,applied.path).status,'UNCHANGED');
    assert.equal(hash(fs.readFileSync(target)),alternativeEncoding,'identical pixels preserve existing PNG bytes and approvals');
    png.data[(126*128+64)*4]=50;savePNG(target,png);
    assert.throws(()=>applyCharacterBuild(name,applied.path),/Destino existente/);
    const beforeReplacement=hash(fs.readFileSync(target)),replacement=applyCharacterBuild(name,applied.path,true);
    assert.equal(replacement.status,'APPLIED_REVIEW_REQUIRED');
    assert.equal(hash(fs.readFileSync(path.join(ROOT,replacement.backup,slot))),beforeReplacement);
    const animation=build({schemaVersion:1,id:name+'-animation-gate',kind:'character',characterId:name,jobs:[{id:'body',source:`tmp/${name}/body.aseprite`,profile:{width:128,height:128,frames:1},targets:['Animations/Idle/idle_front_r_00.png']}]});
    assert.throws(()=>applyCharacterBuild(name,animation.path),/Gate base/);
    assert.equal(approval(character.spec,character.dir,'consistency'),null);
    assert.equal(verifyEditorBuild(normal.path).report.status,'PASS');
    fs.appendFileSync(path.join(ROOT,normal.path,'preview.html'),'tamper');
    assert.throws(()=>verifyEditorBuild(normal.path),/alterado/);
  } finally {
    for(const out of outputs) {inside(ROOT,path.relative(ROOT,out));fs.rmSync(out,{recursive:true,force:true});}
    if(character)fs.rmSync(character.dir,{recursive:true,force:true});
    fs.rmSync(temp,{recursive:true,force:true});
  }
});
