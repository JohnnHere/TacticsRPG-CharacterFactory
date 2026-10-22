import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { PNG } from 'pngjs';
import { ROOT, inside, id, json, readJSON, write, hash, slash, now, files, loadCharacter, approval, digest, assertSlot, escapeHTML } from './core.mjs';
import { decode, measure, savePNG } from './images.mjs';

export const ASSET_KINDS = ['character','enemy','environment','prop','effect','ui','weapon'];
const localConfig = path.join(ROOT,'config/aseprite.local.json');
const scriptPath = path.join(ROOT,'tools/aseprite/bridge.lua');
const stamp = file => hash(fs.readFileSync(file));
const relative = file => slash(path.relative(ROOT,file));
function positive(n, name, max=4096) { if(!Number.isInteger(n)||n<1||n>max) throw Error(`${name}: inteiro 1..${max}.`); return n; }

// Explicit setting wins; discovery only reads installation metadata, never starts Steam.
export function findAseprite(explicit, env=process.env) {
  if(explicit || env.ASEPRITE_PATH || fs.existsSync(localConfig)) {
    const selected=explicit || env.ASEPRITE_PATH || readJSON(localConfig).executable;
    if(typeof selected!=='string'||!selected.trim()) throw Error('ASEPRITE_PATH/config sem executavel.');
    const resolved=path.resolve(selected), exe=fs.existsSync(resolved)&&fs.statSync(resolved).isDirectory()?path.join(resolved,process.platform==='win32'?'Aseprite.exe':'aseprite'):resolved;
    if(!fs.existsSync(exe)||!fs.statSync(exe).isFile()) throw Error(`Aseprite ausente: ${exe}`);
    return fs.realpathSync(exe);
  }
  const candidates=[];
  if(process.platform==='win32') {
    for(const root of [env['ProgramFiles(x86)'],env.ProgramFiles].filter(Boolean)) candidates.push(path.join(root,'Aseprite/Aseprite.exe'),path.join(root,'Steam/steamapps/common/Aseprite/Aseprite.exe'));
    const reg=spawnSync('reg.exe',['query','HKCU\\Software\\Valve\\Steam','/v','SteamPath'],{encoding:'utf8',windowsHide:true,timeout:5000});
    const steam=reg.stdout?.match(/SteamPath\s+REG_SZ\s+(.+)/i)?.[1]?.trim();
    if(steam) {
      candidates.push(path.join(steam,'steamapps/common/Aseprite/Aseprite.exe'));
      const vdf=path.join(steam,'steamapps/libraryfolders.vdf');
      if(fs.existsSync(vdf)) for(const m of fs.readFileSync(vdf,'utf8').matchAll(/"path"\s+"([^"]+)"/g)) candidates.push(path.join(m[1].replaceAll('\\\\','\\'),'steamapps/common/Aseprite/Aseprite.exe'));
    }
  } else candidates.push('/Applications/Aseprite.app/Contents/MacOS/aseprite',path.join(os.homedir(),'.steam/steam/steamapps/common/Aseprite/aseprite'),'/usr/bin/aseprite');
  for(const dir of (env.PATH??'').split(path.delimiter)) candidates.push(path.join(dir,process.platform==='win32'?'Aseprite.exe':'aseprite'));
  const found=candidates.find(p=>fs.existsSync(p)&&fs.statSync(p).isFile());
  if(!found) throw Error('Aseprite nao encontrado. Use editor-config --input CAMINHO ou ASEPRITE_PATH.');
  return fs.realpathSync(found);
}

export function executeAseprite(executable,args,timeout=120000) {
  const result=spawnSync(executable,['--batch','--noinapp',...args],{cwd:ROOT,windowsHide:true,encoding:'utf8',timeout,maxBuffer:8*1024*1024});
  if(result.error || result.status!==0) throw Error(`Aseprite falhou: ${result.error?.message??result.stderr??result.stdout} (exit ${result.status})`);
  if(/Error:|Error creating directory/i.test(result.stderr??'')) throw Error(`Aseprite: ${result.stderr.trim()}`);
  return {stdout:result.stdout,stderr:result.stderr};
}
export function checkAseprite(explicit) {
  try {
    const executable=findAseprite(explicit), version=executeAseprite(executable,['--version']).stdout.trim();
    if(!/Aseprite\s+1\.(?:[3-9]|\d{2,})\./.test(version)) throw Error('Requer Aseprite >=1.3 e <2; confira a versao.');
    return {status:'AVAILABLE',executable,version,mode:'batch',windowsHide:true,steamClient:'--noinapp',cloudCalls:'none'};
  } catch(error) { return {status:'UNAVAILABLE',error:error.message,optional:true}; }
}
export function configureAseprite(input) {
  const checked=checkAseprite(input); if(checked.status!=='AVAILABLE') throw Error(checked.error);
  json(localConfig,{schemaVersion:1,executable:checked.executable}); return checked;
}
function editor() { const checked=checkAseprite(); if(checked.status!=='AVAILABLE') throw Error(checked.error); return checked; }

export function inspectAseprite(file) {
  const b=fs.readFileSync(file);
  if(b.length<128||b.readUInt16LE(4)!==0xa5e0||b.readUInt32LE(0)!==b.length) throw Error(`ASE invalido: ${file}`);
  const count=b.readUInt16LE(6), durations=[]; let off=128;
  for(let i=0;i<count;i++) {
    if(off+16>b.length||b.readUInt16LE(off+4)!==0xf1fa) throw Error('Frame ASE truncado.');
    const len=b.readUInt32LE(off); if(len<16||off+len>b.length) throw Error('Tamanho de frame ASE invalido.');
    durations.push(b.readUInt16LE(off+8)||b.readUInt16LE(16)); off+=len;
  }
  return {width:b.readUInt16LE(8),height:b.readUInt16LE(10),frames:count,durationsMs:durations};
}

function readManifest(input) {
  const manifest=typeof input==='string'?readJSON(inside(ROOT,input)):structuredClone(input);
  if(manifest.schemaVersion!==1||!ASSET_KINDS.includes(manifest.kind)||!Array.isArray(manifest.jobs)||!manifest.jobs.length) throw Error('Manifesto editor invalido: schemaVersion=1, kind e jobs obrigatorios.');
  id(manifest.id); const seen=new Set();
  for(const job of manifest.jobs) {
    id(job.id); if(seen.has(job.id)) throw Error('Job duplicado.'); seen.add(job.id);
    if(!/\.(aseprite|ase)$/i.test(job.source)) throw Error('Fonte deve ser .aseprite/.ase.');
    const source=inside(ROOT,job.source); if(!fs.statSync(source).isFile()) throw Error('Fonte nao e arquivo.');
    if(job.sourceSha256 && stamp(source)!==job.sourceSha256) throw Error(`Fonte alterada: ${job.source}`);
    const p=job.profile; if(!p) throw Error('Profile obrigatorio por job.');
    positive(p.width,'width'); positive(p.height,'height');
    if(p.width*p.height>16777216) throw Error('Canvas acima de 16M pixels.');
    if(p.frames!==undefined) positive(p.frames,'frames',10000);
    if(p.durationMs!==undefined) positive(p.durationMs,'durationMs',65535);
    if(p.durationsMs!==undefined&&(!Array.isArray(p.durationsMs)||p.durationsMs.some(v=>!Number.isInteger(v)||v<1||v>65535)))throw Error('durationsMs: lista de duracoes inteiras 1..65535.');
    if(p.alpha!==undefined&&!['binary','any'].includes(p.alpha)) throw Error('alpha: binary|any');
    for(const key of ['requireContent','requireTransparency'])if(p[key]!==undefined&&typeof p[key]!=='boolean')throw Error(`${key}: booleano obrigatorio.`);
    if(job.tileset!==undefined&&typeof job.tileset!=='boolean')throw Error('tileset: booleano obrigatorio.');
    if(p.groundY!==undefined&&p.groundY!==null&&(!Number.isInteger(p.groundY)||p.groundY<0||p.groundY>=p.height)) throw Error('groundY invalido.');
    for(const key of ['layers','excludeLayers']) if(job[key]!==undefined&&(!Array.isArray(job[key])||job[key].some(v=>typeof v!=='string'||!v))) throw Error(`${key}: lista de nomes.`);
    if(job.tag!==undefined&&(typeof job.tag!=='string'||!job.tag)) throw Error('Tag invalida.');
    for(const key of ['targets','compare']) if(job[key]!==undefined&&(!Array.isArray(job[key])||job[key].some(v=>typeof v!=='string'||!v))) throw Error(`${key}: lista de caminhos.`);
    if(job.tileset && (job.targets||job.compare||p.groundY!=null)) throw Error('Tileset nao aceita slots de personagem/compare/chao.');
  }
  return manifest;
}

function makePreview(root,report) {
  const jobs=report.jobs.map(j=>({id:j.id,tileset:j.tileset,frames:j.frames.map(f=>({file:f.file,durationMs:f.durationMs})),source:j.source.original,kind:report.kind}));
  const payload=JSON.stringify(jobs).replaceAll('<','\\u003c');
  write(path.join(root,'preview.html'),`<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>${escapeHTML(report.id)} — Aseprite</title>
<style>body{background:#20252d;color:#eee;font:16px system-ui;margin:24px}select,button{font:inherit;margin:6px}canvas{image-rendering:pixelated;max-width:95vw;background:repeating-conic-gradient(#404650 0 25%,#303640 0 50%) 0/16px 16px}p{max-width:850px}</style>
<h1>${escapeHTML(report.id)}</h1><p>Preview de autoria. Validacao tecnica nao concede aprovacao artistica.</p><select id="clip"></select><button id="play">Pausar</button><label>Quadro <input id="frame" type="range" min="0" value="0"></label><label>Zoom <select id="zoom"><option>1</option><option selected>2</option><option>3</option><option>4</option></select></label><p id="info"></p><canvas id="view"></canvas>
<script>
const jobs=${payload};
const clip=document.querySelector('#clip'),slider=document.querySelector('#frame'),zoom=document.querySelector('#zoom'),view=document.querySelector('#view'),ctx=view.getContext('2d'),play=document.querySelector('#play');
let selected=0,index=0,playing=false,next=0,images=[],loadToken=0;
for(const [i,j] of jobs.entries()){const o=document.createElement('option');o.value=i;o.textContent=j.id+' · '+(j.tileset?'tileset · ':'')+j.source.split('/').pop();clip.append(o)}
function setPlaying(value){playing=value;play.textContent=value?'Pausar':'Continuar';next=performance.now()+(jobs[selected].frames[index]?.durationMs??100)}
async function load(){
  const token=++loadToken;setPlaying(false);selected=Number(clip.value);index=0;images=[];view.dataset.job='';
  try{
    const loaded=await Promise.all(jobs[selected].frames.map(f=>new Promise((ok,no)=>{const i=new Image();i.onload=()=>ok(i);i.onerror=()=>no(Error('Imagem ausente: '+f.file));i.src=f.file})));
    if(token!==loadToken)return;images=loaded;slider.max=images.length-1;draw();setPlaying(!jobs[selected].tileset);
  }catch(error){if(token===loadToken)document.querySelector('#info').textContent=error.message}
}
function draw(){
  if(!images[index])return;const im=images[index];view.width=im.width;view.height=im.height;view.style.width=im.width*Number(zoom.value)+'px';view.style.height=im.height*Number(zoom.value)+'px';ctx.drawImage(im,0,0);view.dataset.job=jobs[selected].id;slider.value=index;
  document.querySelector('#info').textContent=jobs[selected].id+' — '+(index+1)+'/'+images.length+' — '+jobs[selected].frames[index].durationMs+'ms';view.title=jobs[selected].source;
}
function tick(t){if(playing&&images.length&&t>=next){index=(index+1)%images.length;draw();next=t+jobs[selected].frames[index].durationMs}requestAnimationFrame(tick)}
clip.onchange=load;slider.oninput=()=>{setPlaying(false);index=Number(slider.value);draw()};zoom.onchange=draw;play.onclick=()=>setPlaying(!playing);load();requestAnimationFrame(tick);
</script></html>`);
}

function inventory(root) { return files(root).filter(p=>path.basename(p)!=='hashes.json').map(p=>({file:slash(path.relative(root,p)),sha256:stamp(p)})); }
export function verifyEditorBuild(buildPath) {
  const dir=inside(path.join(ROOT,'dist/editor'),path.relative(path.join(ROOT,'dist/editor'),path.resolve(ROOT,buildPath)));
  const expected=readJSON(path.join(dir,'hashes.json')), actual=inventory(dir);
  if(JSON.stringify(expected)!==JSON.stringify(actual)) throw Error('Build do editor alterado/incompleto.');
  const report=readJSON(path.join(dir,'build.json')); if(report.status!=='PASS') throw Error('Build nao aprovado tecnicamente.');
  return {dir,report};
}

// Every run uses copied input in a private directory; the open GUI document is never touched.
export function exportAseprite(input,{onProgress=()=>{}}={}) {
  const manifest=readManifest(input), tool=editor();
  const sources=manifest.jobs.map(j=>({file:j.source,sha256:stamp(inside(ROOT,j.source))}));
  const provenance={manifest,sources,version:tool.version,bridge:stamp(scriptPath),exporter:stamp(new URL(import.meta.url))};
  const build=hash(JSON.stringify(provenance)).slice(0,20);
  const dest=inside(path.join(ROOT,'dist/editor'),`${manifest.id}/${build}`);
  if(fs.existsSync(dest)) {const checked=verifyEditorBuild(relative(dest));return {...checked.report,path:relative(dest),reused:true};}
  const workBase=path.join(ROOT,'tmp/aseprite');fs.mkdirSync(workBase,{recursive:true});
  const stage=fs.mkdtempSync(path.join(workBase,manifest.id+'-'));
  const report={schemaVersion:1,id:manifest.id,kind:manifest.kind,characterId:manifest.characterId??null,build,createdAt:now(),tool,provenance,manifest,status:'BUILDING',jobs:[],runtimeIntegration:'NOT_RUN',artisticApproval:'REQUIRES_CREATOR_REVIEW'};
  try {
    for(let ji=0;ji<manifest.jobs.length;ji++) {
      const job=manifest.jobs[ji], source=inside(ROOT,job.source), dir=path.join(stage,'jobs',job.id);fs.mkdirSync(dir,{recursive:true});
      const snapshot=path.join(dir,'source.aseprite');write(snapshot,fs.readFileSync(source));
      if(stamp(snapshot)!==sources[ji].sha256)throw Error(`${job.id}: fonte mudou durante a copia.`);
      const native=inspectAseprite(snapshot); if(native.width!==job.profile.width||native.height!==job.profile.height) throw Error(`${job.id}: canvas da fonte divergente.`);
      const sheet=path.join(dir,'sheet.png'), data=path.join(dir,'sheet.json'), document=path.join(dir,'document.json');
      const args=[];for(const layer of job.layers??[])args.push('--layer',layer);for(const layer of job.excludeLayers??[])args.push('--ignore-layer',layer);
      if(job.tag)args.push('--tag',job.tag);if(job.tileset)args.push('--export-tileset');
      args.push('--list-layer-hierarchy','--list-tags','--list-slices',snapshot,'--sheet-type','horizontal','--format','json-array','--sheet',sheet,'--data',data,'--script-param',`metadata=${document}`,'--script',scriptPath);
      if(job.tileset)args.splice(args.length-2,0,'--script-param',`tilesDirectory=${path.join(dir,'tilesets')}`);
      executeAseprite(tool.executable,args);
      if(!fs.existsSync(data)||!fs.existsSync(document)||!fs.existsSync(sheet)) throw Error(`${job.id}: Aseprite nao produziu saidas completas.`);
      const meta=readJSON(data), doc=readJSON(document), frames=meta.frames;
      if(!Array.isArray(frames)||!frames.length) throw Error(`${job.id}: nenhum frame exportado.`);
      if(job.profile.frames!==undefined&&frames.length!==job.profile.frames) throw Error(`${job.id}: contagem divergente.`);
      if(job.profile.durationsMs&&job.profile.durationsMs.length!==frames.length)throw Error(`${job.id}: contagem de duracoes divergente.`);
      if(!job.tag&&!job.tileset&&frames.length!==native.frames) throw Error(`${job.id}: frames vazios/duplicados foram perdidos.`);
      if(job.targets&&job.targets.length!==frames.length||job.compare&&job.compare.length!==frames.length) throw Error(`${job.id}: targets/compare diferentes do numero de frames.`);
      if(job.tag&&!doc.tags.some(t=>t.name===job.tag)) throw Error(`${job.id}: tag nao existe.`);
      for(const layer of [...job.layers??[],...job.excludeLayers??[]])if(!doc.layers.some(l=>l.path===layer||l.name===layer))throw Error(`${job.id}: layer nao existe: ${layer}`);
      if(job.tileset&&!doc.tilemaps.length) throw Error(`${job.id}: fonte sem tilemap.`);
      const tileLibraries=[];
      if(job.tileset)for(const ts of doc.tilesets) {
        const tiles=[];
        for(const tile of ts.tiles) {
          const tileFile=inside(dir,tile.file),d=decode(tileFile);
          if(d.image.width!==ts.tileWidth||d.image.height!==ts.tileHeight)throw Error(`${job.id}: dimensao de tile divergente.`);
          if(job.profile.alpha==='binary'&&measure(d.image).partial)throw Error(`${job.id}: alfa parcial em tile.`);
          savePNG(tileFile,d.image);
          tiles.push({...tile,file:`jobs/${job.id}/${tile.file}`,sha256:stamp(tileFile),rgbaSha256:hash(d.image.data)});
        }
        tileLibraries.push({...ts,tiles});
      }
      const raster=decode(sheet).image, out=[];
      for(let i=0;i<frames.length;i++) {
        const f=frames[i], r=f.frame,p=job.profile;
        if(!r||['x','y','w','h'].some(k=>!Number.isInteger(r[k]))||r.w<1||r.h<1)throw Error(`${job.id}: retangulo de frame invalido.`);
        const expectedWidth=job.tileset?r.w:p.width, expectedHeight=job.tileset?r.h:p.height;
        if(f.trimmed||f.rotated||!r||r.w!==expectedWidth||r.h!==expectedHeight||r.x<0||r.y<0||r.x+r.w>raster.width||r.y+r.h>raster.height) throw Error(`${job.id}: frame recortado/rotacionado/canvas invalido.`);
        const image=new PNG({width:r.w,height:r.h});PNG.bitblt(raster,image,r.x,r.y,r.w,r.h,0,0);
        const m=measure(image);if(p.alpha==='binary'&&m.partial)throw Error(`${job.id}: alfa parcial.`);
        if((p.requireContent??!job.tileset)&&!m.contentHeight)throw Error(`${job.id}: frame vazio.`);
        if(p.requireTransparency&&m.transparent===0)throw Error(`${job.id}: transparencia ausente.`);
        if(p.groundY!=null&&m.bottom!==p.groundY)throw Error(`${job.id}: groundY ${m.bottom}, esperado ${p.groundY}.`);
        const durationMs=f.duration;
        if(!Number.isInteger(durationMs)||durationMs<1)throw Error(`${job.id}: duracao invalida.`);
        const expectedDuration=Array.isArray(p.durationsMs)?p.durationsMs[i]:p.durationMs;
        if(expectedDuration!==undefined&&durationMs!==expectedDuration)throw Error(`${job.id}: duracao alterada no frame ${i}.`);
        if(!job.tag&&!job.tileset&&durationMs!==native.durationsMs[i])throw Error(`${job.id}: timing diferente da fonte.`);
        let compare=null;
        if(job.compare) {const target=inside(ROOT,job.compare[i]),d=decode(target);if(d.image.width!==image.width||d.image.height!==image.height||!d.image.data.equals(image.data))throw Error(`${job.id}: RGBA diferente de ${job.compare[i]}`);compare={file:job.compare[i],sha256:d.sha256,rgbaIdentical:true};}
        const file=`jobs/${job.id}/frames/${String(i).padStart(3,'0')}.png`;savePNG(path.join(stage,file),image);
        out.push({file,sha256:stamp(path.join(stage,file)),rgbaSha256:hash(image.data),durationMs,...m,compare,target:job.targets?.[i]??null});
      }
      if(stamp(source)!==sources[ji].sha256)throw Error(`${job.id}: fonte mudou durante a exportacao. Salve e repita.`);
      report.jobs.push({id:job.id,tileset:!!job.tileset,tilesets:tileLibraries,source:{original:job.source,file:`jobs/${job.id}/source.aseprite`,sha256:sources[ji].sha256},frames:out,metadata:`jobs/${job.id}/document.json`,sheetMetadata:`jobs/${job.id}/sheet.json`});
      onProgress({completed:ji+1,total:manifest.jobs.length,id:job.id});
    }
    report.status='PASS';report.summary={jobs:report.jobs.length,frames:report.jobs.reduce((n,j)=>n+j.frames.length,0),comparedFrames:report.jobs.reduce((n,j)=>n+j.frames.filter(f=>f.compare).length,0)};
    json(path.join(stage,'build.json'),report);json(path.join(stage,'manifest.json'),manifest);makePreview(stage,report);json(path.join(stage,'hashes.json'),inventory(stage));
    fs.mkdirSync(path.dirname(dest),{recursive:true});fs.renameSync(stage,dest);
    return {...report,path:relative(dest),reused:false};
  } catch(error) { json(path.join(stage,'failure.json'),{status:'FAIL',message:error.message,createdAt:now(),report});throw Error(`${error.message} Evidencia: ${relative(stage)}/failure.json`); }
}

export function createEditorTemplate(input) {
  const spec=readJSON(inside(ROOT,input));id(spec.id);
  if(spec.schemaVersion!==1||!ASSET_KINDS.includes(spec.kind))throw Error('Template: schemaVersion=1 e kind obrigatorios.');
  const p=spec.profile;positive(p?.width,'width');positive(p?.height,'height');positive(p?.frames,'frames',1000);positive(p?.durationMs,'durationMs',65535);
  if(!Array.isArray(spec.layers)||!spec.layers.length||spec.layers.some(l=>typeof l!=='string'||!l))throw Error('Layers obrigatorias.');
  let base;
  if(spec.characterId) {const c=loadCharacter(spec.characterId);if(!['character','enemy'].includes(spec.kind)||c.spec.profile.width!==p.width||c.spec.profile.height!==p.height)throw Error('Template diferente do perfil do personagem.');base=path.join(c.dir,'source/aseprite',spec.id);}
  else base=inside(path.join(ROOT,'assets',spec.kind),spec.id);
  base=inside(ROOT,path.relative(ROOT,base));
  if(fs.existsSync(base))throw Error('Template ja existe; escolha novo id para preservar fontes.');
  const tool=editor();fs.mkdirSync(base,{recursive:true});
  const source=path.join(base,'source',spec.id+'.aseprite'),request=path.join(base,'template.json');fs.mkdirSync(path.dirname(source),{recursive:true});json(request,spec);
  executeAseprite(tool.executable,['--script-param',`template=${request}`,'--script-param',`output=${source}`,'--script',scriptPath]);
  const actual=inspectAseprite(source);if(actual.frames!==p.frames||actual.width!==p.width||actual.height!==p.height)throw Error('Template nao foi criado corretamente.');
  json(path.join(base,'editor.json'),{schemaVersion:1,id:spec.id,kind:spec.kind,characterId:spec.characterId??null,jobs:[{id:spec.id,source:relative(source),profile:{...p,requireContent:true},...(spec.targets?{targets:spec.targets}:{})}]});
  return {status:'EMPTY_AUTHORING_TEMPLATE',source:relative(source),manifest:relative(path.join(base,'editor.json')),request:relative(request),artProduced:false};
}

export function forkEditorSources(input,name,{jobId,characterId}={}) {
  id(name);const original=readManifest(input);
  let jobs=jobId?original.jobs.filter(j=>j.id===jobId):original.jobs;
  if(!jobs.length)throw Error('Job solicitado nao encontrado.');
  characterId??=original.characterId;
  let base;
  if(characterId) {
    const c=loadCharacter(characterId),prefix=`characters/${characterId}/source/`;
    if(!['character','enemy'].includes(original.kind))throw Error('Tipo incompativel com personagem.');
    if(!original.characterId)jobs=jobs.filter(j=>slash(j.source).startsWith(prefix));
    if(!jobs.length||original.characterId&&original.characterId!==characterId)throw Error('Nenhuma fonte deste personagem.');
    base=path.join(c.dir,'source/aseprite',name);
  } else base=inside(path.join(ROOT,'assets',original.kind),name);
  base=inside(ROOT,path.relative(ROOT,base));
  if(fs.existsSync(base))throw Error('Copia de trabalho ja existe; escolha novo --name.');
  const pending=jobs.map(job=>{
    const {sourceSha256,compare,...copy}=job;
    const source=inside(ROOT,job.source),target=path.join(base,'source',job.id+'.aseprite');
    return {source,target,job:{...copy,source:relative(target)},original:{source:job.source,sha256:stamp(source)}};
  });
  for(const p of pending)write(p.target,fs.readFileSync(p.source));
  const manifest={schemaVersion:1,id:name,kind:original.kind,characterId:characterId??null,jobs:pending.map(p=>p.job)};
  const file=path.join(base,'editor.json');json(file,manifest);json(path.join(base,'lineage.json'),{createdAt:now(),sources:pending.map(p=>p.original),artisticApproval:'WORKING_COPY_NOT_REVIEWED'});
  return {status:'WORKING_COPY',manifest:relative(file),sources:pending.map(p=>relative(p.target)),characterApplySupported:!!characterId&&pending.every(p=>p.job.targets?.length)};
}

export function applyCharacterBuild(characterId,buildPath,force=false) {
  const {dir:buildDir,report}=verifyEditorBuild(buildPath),{dir,spec}=loadCharacter(characterId);
  if(report.characterId!==characterId||!['character','enemy'].includes(report.kind))throw Error('Build nao pertence a este personagem.');
  if(spec.status==='reference_only'||!approval(spec,dir,'concept'))throw Error('Gate 1 valido obrigatorio.');
  if(spec.derivedFrom) {const parent=loadCharacter(spec.derivedFrom.character),ref=spec.references.find(r=>r.character===parent.spec.id);if(!approval(parent.spec,parent.dir,'concept')||ref?.sourceDigest!==digest(parent.spec,parent.dir,'concept')||parent.spec.identityId!==spec.identityId||parent.spec.race.id!==spec.race.id)throw Error('Base de roupa alterada; refresh-base e revisao obrigatorios.');}
  const plan=[],seen=new Set();
  for(const job of report.jobs)for(const f of job.frames) {
    if(!f.target)throw Error('Todos os frames precisam de targets explicitos para aplicar.');
    assertSlot(spec,f.target);if(seen.has(f.target))throw Error('Slot duplicado.');seen.add(f.target);
    if(f.target.startsWith('Animations/')&&!approval(spec,dir,'base'))throw Error('Gate base valido obrigatorio para animacoes.');
    const source=inside(buildDir,f.file),d=decode(source);if(d.colorType!==6||d.image.depth!==8||d.image.width!==spec.profile.width||d.image.height!==spec.profile.height)throw Error('Perfil do frame diferente do personagem.');
    const m=measure(d.image);if(!m.contentHeight||!m.transparent||spec.profile.groundY!==null&&m.bottom!==spec.profile.groundY)throw Error('Conteudo/transparencia/chao incompativel.');
    const target=inside(path.join(dir,'sprites'),f.target),exists=fs.existsSync(target);
    let same=exists&&stamp(target)===f.sha256;
    if(exists&&!same) {try {const previous=decode(target).image;same=previous.width===d.image.width&&previous.height===d.image.height&&previous.data.equals(d.image.data);}catch{same=false;}}
    if(exists&&!same&&!force)throw Error(`Destino existente: ${f.target}; use --force apos revisar o preview.`);
    plan.push({target,source,frame:f,job,old:exists?fs.readFileSync(target):null,same});
  }
  const changed=plan.filter(p=>!p.same);if(!changed.length)return {status:'UNCHANGED',frames:plan.length};
  const history=inside(dir,'source/aseprite-history');fs.mkdirSync(history,{recursive:true});
  const backup=fs.mkdtempSync(path.join(history,report.build+'-'));
  for(const p of changed)if(p.old)write(path.join(backup,p.frame.target),p.old);
  const assetFile=path.join(dir,'assets.json'),previous=fs.readFileSync(assetFile),assets=readJSON(assetFile);
  try {
    for(const p of changed) {write(p.target,fs.readFileSync(p.source));assets.push({at:now(),kind:'sprite',file:`sprites/${p.frame.target}`,sha256:p.frame.sha256,provider:'Aseprite-local',model:report.tool.version,sourceFile:p.job.source.original,sourceSha256:p.job.source.sha256,editorBuild:relative(buildDir),durationMs:p.frame.durationMs,backup:p.old?relative(path.join(backup,p.frame.target)):null});}
    json(assetFile,assets);
  } catch(error) {for(const p of changed)if(p.old)write(p.target,p.old);else if(fs.existsSync(p.target))fs.unlinkSync(p.target);write(assetFile,previous);throw error;}
  json(path.join(backup,'applied.json'),{createdAt:now(),build:relative(buildDir),frames:changed.map(p=>p.frame.target),artisticApproval:'REQUIRES_CREATOR_REVIEW'});
  return {status:'APPLIED_REVIEW_REQUIRED',frames:changed.length,backup:relative(backup),next:`node src/cli.mjs preview --id ${characterId}`};
}
