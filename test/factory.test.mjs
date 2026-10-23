import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { PNG } from 'pngjs';
import { ROOT, inside, id, expectedSlots, digest, approval, write, json, readJSON, charDir, loadCharacter } from '../src/core.mjs';
import { composite, measure, savePNG, decode, validate } from '../src/images.mjs';
import { verifyReferences } from '../src/references.mjs';
import { saveRecipe, reviewRecipe, activeRecipe } from '../src/recipes.mjs';

function bitmap(color=[200,100,50,255]) {
  const img=new PNG({width:128,height:128});
  for(let y=27;y<=126;y++) for(let x=50;x<78;x++) color.forEach((c,k)=>img.data[(y*128+x)*4+k]=c);
  return img;
}
function cli(...args) {
  return spawnSync(process.execPath,[path.join(ROOT,'src/cli.mjs'),...args],{cwd:ROOT,encoding:'utf8',timeout:30000});
}
function ok(result) {assert.equal(result.status,0,result.stderr||result.stdout);}

test('confinamento rejeita traversal, IDs perigosos e junction/symlink externo',()=>{
  assert.throws(()=>id('../Hero'));
  assert.throws(()=>inside(ROOT,'../TacticsRPG/Assets'));
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'factory-path-')),other=fs.mkdtempSync(path.join(os.tmpdir(),'factory-outside-'));
  try {
    fs.symlinkSync(other,path.join(root,'outside'),process.platform==='win32'?'junction':'dir');
    assert.throws(()=>inside(root,'outside/new.png'),/simbolico/);
  } finally {fs.rmSync(root,{recursive:true,force:true});fs.rmSync(other,{recursive:true,force:true});}
});

test('source-over preserva pixel grid, respeita ordem/alfa e rejeita canvas diferente',()=>{
  const a=new PNG({width:1,height:1}),b=new PNG({width:1,height:1});a.data.set([255,0,0,255]);b.data.set([0,0,255,128]);
  const out=composite([a,b],1,1);assert.deepEqual([...out.data],[127,0,128,255]);
  assert.deepEqual([...composite([b,a],1,1).data],[255,0,0,255]);
  assert.throws(()=>composite([a],128,128),/canvas/);
});

test('medicao considera alfa, fundo transparente e linha do chao',()=>{
  const m=measure(bitmap());assert.equal(m.bottom,126);assert.equal(m.top,27);assert.equal(m.contentHeight,100);assert.equal(m.partial,0);assert.equal(m.colorCount,1);assert.ok(m.transparent>0);
});

test('PNG corrompido e limites de dimensao sao rejeitados antes de uso',()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'factory-png-'));
  try {const p=path.join(dir,'fake.png');write(p,'not png');assert.throws(()=>decode(p),/Assinatura/);}
  finally {fs.rmSync(dir,{recursive:true,force:true});}
});

test('catalogos e referencias congeladas preservam baseline 28/63',()=>{
  assert.deepEqual(verifyReferences(),[]);
  assert.equal(readJSON(path.join(ROOT,'catalogs/races.json')).length,28);
  const jobs=readJSON(path.join(ROOT,'catalogs/jobs.json'));assert.equal(jobs.length,63);assert.equal(new Set(jobs.map(j=>j.id)).size,63);
  ok(cli('doctor'));ok(cli('help'));
});

test('fluxo CLI protege gates, registra roupas, exporta baseline e invalida revisao apos mudanca',()=>{
  // Artifacts are synthetic test fixtures, removed below. Reviews do not concern real artwork.
  const name='test-'+crypto.randomBytes(5).toString('hex'),variant=name+'-archer',dir=charDir(name),vdir=charDir(variant);
  const temp=fs.mkdtempSync(path.join(os.tmpdir(),'factory-flow-'));
  const dist=inside(path.join(ROOT,'dist'),name);
  const recipeDir=inside(path.join(ROOT,'recipes/jobs'),name);
  try {
    ok(cli('new','--id',name,'--race','Humano','--job','Warrior'));
    const handoffPrompt=fs.readFileSync(path.join(dir,'handoff/prompt.md'),'utf8');
    assert.match(handoffPrompt,/TODA a producao de arte deve acontecer no Aseprite/);
    assert.match(handoffPrompt,/Nao usar image_gen/);
    assert.doesNotMatch(handoffPrompt,/Se image_gen estiver disponivel, usar/);
    assert.equal(cli('new','--id',name,'--race','Orc','--job','Warrior').status,2);
    assert.equal(cli('export','--id',name).status,2);
    const input=path.join(temp,'fixture.png');savePNG(input,bitmap());
    assert.equal(cli('import','--id',name,'--kind','sprite','--input',input,'--slot',`${name.replaceAll('-','_')}_mvp1_static_128.png`).status,2);
    ok(cli('import','--id',name,'--kind','concept','--input',input,'--name','synthetic-fixture','--provider','test-fixture'));
    ok(cli('review','--id',name,'--gate','concept','--decision','approved','--reviewer','SYNTHETIC TEST','--evidence','Teste automatizado de gates; nao e arte.'));
    ok(cli('outfit','--from',name,'--id',variant,'--job','Archer'));
    let spec=readJSON(path.join(dir,'character.json')),vspec=readJSON(path.join(vdir,'character.json'));
    assert.equal(spec.identityId,vspec.identityId);assert.equal(vspec.job.id,'archer');assert.deepEqual(spec.appearance,vspec.appearance);
    assert.equal(expectedSlots(spec).length,97);
    for(const slot of expectedSlots(spec,'directions')) ok(cli('import','--id',name,'--kind','sprite','--input',input,'--slot',slot));
    assert.equal(cli('prepare','--id',name,'--purpose','animation').status,2);
    ok(cli('review','--id',name,'--gate','base','--decision','approved','--reviewer','SYNTHETIC TEST','--evidence','Teste dos estaticos sinteticos.'));
    const baseHash=digest(spec,dir,'base');
    ok(cli('prepare','--id',name,'--purpose','animation'));
    for(const slot of expectedSlots(spec).filter(p=>p.startsWith('Animations/'))) savePNG(inside(path.join(dir,'sprites'),slot),bitmap());
    assert.equal(digest(spec,dir,'base'),baseHash,'adicionar animacao nao invalida base');
    assert.equal(validate(spec,dir,'full').summary.FAIL,0);
    assert.equal(cli('export','--id',name).status,2);
    ok(cli('review','--id',name,'--gate','consistency','--decision','approved','--reviewer','SYNTHETIC TEST','--evidence','Teste de inventario sintetico completo.'));
    ok(cli('export','--id',name));
    const builds=fs.readdirSync(dist);assert.equal(builds.length,1);
    const packageRoot=path.join(dist,builds[0]);
    assert.ok(fs.existsSync(path.join(packageRoot,'Assets/Editor/CharacterFactoryImporter.cs')));
    const manifest=readJSON(path.join(packageRoot,'Assets/Resources/Characters',name,'factory-manifest.json'));
    assert.equal(manifest.files.length,97);assert.equal(manifest.gate3,'PENDING_PLAYMODE');
    ok(cli('review','--id',name,'--gate','base','--decision','changes_requested','--reviewer','SYNTHETIC TEST','--evidence','Teste: rejeitar base bloqueia export mesmo com Gate2 anterior.'));
    assert.equal(cli('export','--id',name).status,2);
    ok(cli('review','--id',name,'--gate','base','--decision','approved','--reviewer','SYNTHETIC TEST','--evidence','Teste: reavaliacao dos estaticos.'));
    ok(cli('review','--id',name,'--gate','consistency','--decision','changes_requested','--reviewer','SYNTHETIC TEST','--evidence','Teste: ultima rejeicao vence aprovacao.'));
    assert.equal(approval(spec,dir,'consistency'),null);assert.equal(cli('export','--id',name).status,2);
    ok(cli('review','--id',name,'--gate','consistency','--decision','approved','--reviewer','SYNTHETIC TEST','--evidence','Teste: reavaliacao sintetica.'));
    assert.ok(approval(spec,dir,'consistency'));
    const anim=inside(path.join(dir,'sprites'),'Animations/Idle/idle_front_r_00.png');savePNG(anim,bitmap([12,34,56,255]));
    assert.equal(approval(spec,dir,'consistency'),null);
    assert.ok(approval(spec,dir,'base'));
    // Geometric defects must fail even if they look plausible in a contact sheet.
    const broken=bitmap();broken.data[(126*128+50)*4+3]=0;for(let x=51;x<78;x++) broken.data[(126*128+x)*4+3]=0;savePNG(anim,broken);
    assert.ok(validate(spec,dir,'full').checks.some(c=>c.file.endsWith('idle_front_r_00.png')&&c.check==='ground'&&c.status==='FAIL'));
    // A native source body can be composited and all layers have provenance hashes.
    savePNG(path.join(dir,'source/layers/body.png'),bitmap());
    const lm=path.join(temp,'layers.json');json(lm,{schemaVersion:1,frames:[{slot:expectedSlots(spec,'base')[0],layers:['body.png']}]});
    ok(cli('compose','--id',name,'--manifest',lm,'--force'));
    assert.equal(readJSON(path.join(dir,'assets.json')).at(-1).kind,'composed-native-2d');
    // Recipe versions archive actual PNG bytes, decoupled from later character edits.
    const recipeSpec={...spec,job:{id:name,name:'SYNTHETIC RECIPE'}};
    json(path.join(dir,'character.json'),recipeSpec);
    ok(cli('review','--id',name,'--gate','concept','--decision','approved','--reviewer','SYNTHETIC TEST','--evidence','Teste de receita, nenhuma aprovacao de arte real.'));
    const saved=saveRecipe(recipeSpec,dir,'jobs');
    assert.throws(()=>reviewRecipe('jobs',name,'approved','SYNTHETIC TEST','Fixture',loadCharacter),/rules/);
    const candidate=readJSON(saved.candidate);candidate.rules=['TEST ONLY: silhouette rules for automated fixture.'];json(saved.candidate,candidate);
    reviewRecipe('jobs',name,'approved','SYNTHETIC TEST','Fixture rules',loadCharacter);
    const active=activeRecipe('jobs',name);assert.equal(active.version,1);assert.equal(active.rules.length,1);
    const archive=inside(ROOT,active.images[0].path),archivedBytes=fs.readFileSync(archive);
    savePNG(path.join(dir,'concepts/synthetic-fixture.png'),bitmap([1,2,3,255]));
    assert.deepEqual(fs.readFileSync(archive),archivedBytes);
    assert.equal(activeRecipe('jobs',name).version,1);
    write(archive,'broken');assert.throws(()=>activeRecipe('jobs',name),/alterada/);
    assert.equal(cli('review','--id','hero-reference','--gate','concept','--decision','approved','--reviewer','TEST','--evidence','must be blocked').status,2);
  } finally {
    // Names were generated above and resolved through the package confinement function.
    for(const p of [dir,vdir,dist,recipeDir,recipeDir+'.candidate.json']) fs.rmSync(p,{recursive:true,force:true});
    fs.rmSync(temp,{recursive:true,force:true});
  }
});
