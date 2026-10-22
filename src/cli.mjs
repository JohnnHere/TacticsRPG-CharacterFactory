#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { fileURLToPath } from 'node:url';
import { ROOT, now, readJSON, json, write, hash, inside, slash, charDir, loadCharacter, id, catalogEntry, assertSlot, expectedSlots, digest, approval, pngFiles } from './core.mjs';
import { syncReferences, verifyReferences } from './references.mjs';
import { createCharacter, prepare, preview } from './workflow.mjs';
import { decode, validate, composite, savePNG } from './images.mjs';
import { saveRecipe, reviewRecipe } from './recipes.mjs';
import { checkAseprite, configureAseprite, createEditorTemplate, forkEditorSources, exportAseprite, applyCharacterBuild } from './aseprite.mjs';

const help=`Character Factory 0.1 — sprites 2D / Node >=20
  doctor
  editor-config --input "CAMINHO/Aseprite.exe"
  editor-check
  editor-template --manifest config/aseprite-template.example.json
  editor-fork --manifest CAMINHO/editor.json --name revisao-v2 [--job JOB] [--id PERSONAGEM]
  editor-export --manifest CAMINHO/editor.json
  editor-apply --id orc-01 --build dist/editor/ID/BUILD [--force]
  sync --source ../TacticsRPG [--accept-update]
  catalog --kind races|jobs
  new --id orc-01 --race Orc --job Warrior
  outfit --from orc-01 --id orc-01-archer --job Archer
  refresh-base --id orc-01-archer
  recipe-save --kind races|jobs --from orc-01-archer [--force]
  recipe-review --kind jobs --name archer --decision approved|changes_requested --reviewer NOME --evidence TEXTO
  prepare --id orc-01 [--purpose concept|outfit|base|directions|animation] [--state Idle]
  import --id orc-01 --input imagem.png --kind concept --name candidato-a [--provider ferramenta] [--model versao]
  import --id orc-01 --input sprite.png --kind sprite --slot Directions/orc_01_dir_front_r.png
  compose --id orc-01 --manifest characters/orc-01/source/layers.json [--force]
  preview --id hero-reference
  validate --id hero-reference [--stage base|directions|full]
  review --id orc-01 --gate concept|base|consistency|in-game --decision approved|changes_requested --reviewer NOME --evidence TEXTO
  export --id orc-01
  demo
Comandos nao geram arte sem ferramenta/autor externo. prepare cria pacote pronto para uma LLM com geracao de imagens.
Exit 0: comando concluido; 1: falha tecnica/validacao; 2: uso invalido ou gate pendente.
`;

function lineage(spec) {
  if (!spec.derivedFrom) return;
  const parent=loadCharacter(spec.derivedFrom.character);
  if(parent.spec.identityId!==spec.identityId || parent.spec.race.id!==spec.race.id) throw Error('Identidade racial/individual divergente da base.');
  const ref=spec.references.find(x=>x.character===parent.spec.id);
  if(!approval(parent.spec,parent.dir,'concept')) throw Error('Conceito do individuo base ainda sem aprovacao valida.');
  if(ref?.sourceDigest!==digest(parent.spec,parent.dir,'concept')) throw Error('Base alterada. Execute refresh-base e revise novamente esta roupa.');
}
function requireConcept(spec,dir) {
  if(spec.status==='reference_only') throw Error('Piloto de referencia nao e producao aprovada. Crie outro ID para trabalho novo.');
  if(!approval(spec,dir,'concept')) throw Error('Gate 1: conceito sem aprovacao explicita valida.');
  lineage(spec);
}
function appendAsset(dir,record) {
  const p=path.join(dir,'assets.json'), assets=readJSON(p);
  assets.push({at:now(),...record}); json(p,assets);
}
function required(o,...keys) {for(const key of keys) if(!o[key]) throw Error(`Parametro obrigatorio: --${key}`);}

export function run(argv=process.argv.slice(2)) {
  const [command='help',...rest]=argv;
  const names=['id','race','job','from','source','kind','purpose','state','input','name','provider','model','slot','stage','manifest','gate','decision','reviewer','evidence','build'];
  const {values:o}=parseArgs({args:rest,options:{...Object.fromEntries(names.map(n=>[n,{type:'string'}])),force:{type:'boolean'},'accept-update':{type:'boolean'},help:{type:'boolean'}},strict:true});
  if(command==='help'||o.help) return console.log(help);
  if(command==='editor-config') {required(o,'input');console.log(JSON.stringify(configureAseprite(o.input),null,2));return;}
  if(command==='editor-check') {const result=checkAseprite();console.log(JSON.stringify(result,null,2));return result.status==='AVAILABLE'?0:1;}
  if(command==='sync') {required(o,'source'); return console.log(JSON.stringify(syncReferences(o.source,o['accept-update']),null,2));}
  const errors=verifyReferences();
  if(command==='doctor') {
    console.log(JSON.stringify({node:process.version,root:ROOT,referenceErrors:errors,cloudCalls:'none',generation:'Pacotes para ferramentas de imagem da conversa; nenhum endpoint/API cobrado configurado.',editor:checkAseprite(),editorPolicy:'Aseprite/LibreSprite opcionais. editor-check exige Aseprite; comandos existentes continuam locais.'},null,2));
    return errors.length?1:0;
  }
  if(errors.length) throw Error('Referencias ausentes/alteradas. Execute doctor e sync antes de prosseguir.');
  if(command==='editor-template') {required(o,'manifest');console.log(JSON.stringify(createEditorTemplate(o.manifest),null,2));return;}
  if(command==='editor-fork') {required(o,'manifest','name');console.log(JSON.stringify(forkEditorSources(o.manifest,o.name,{jobId:o.job,characterId:o.id}),null,2));return;}
  if(command==='editor-export') {required(o,'manifest');const result=exportAseprite(o.manifest,{onProgress:p=>{if(p.completed%10===0||p.completed===p.total)console.error(`Aseprite ${p.completed}/${p.total}: ${p.id}`);}});console.log(JSON.stringify({status:result.status,path:result.path,preview:result.path+'/preview.html',reused:result.reused,summary:result.summary},null,2));return;}
  if(command==='editor-apply') {required(o,'id','build');console.log(JSON.stringify(applyCharacterBuild(o.id,o.build,o.force),null,2));return;}
  if(command==='catalog') {if(!['races','jobs'].includes(o.kind)) throw Error('--kind races|jobs'); console.log(JSON.stringify(readJSON(path.join(ROOT,'catalogs',o.kind+'.json')),null,2));return;}
  if(command==='new') {required(o,'id','race','job');createCharacter(o.id,o.race,o.job);console.log(`Criado: characters/${o.id}/handoff/prompt.md`);return;}
  if(command==='outfit') {required(o,'id','from','job');const parent=loadCharacter(o.from);createCharacter(o.id,parent.spec.race.id,o.job,o.from);console.log(`Roupa candidata criada: ${o.id}; identidade preservada de ${o.from}.`);return;}
  if(command==='recipe-save') {required(o,'kind','from');const {dir,spec}=loadCharacter(o.from);console.log(JSON.stringify(saveRecipe(spec,dir,o.kind,o.force),null,2));return;}
  if(command==='recipe-review') {required(o,'kind','name','decision','reviewer','evidence');console.log(JSON.stringify(reviewRecipe(o.kind,o.name,o.decision,o.reviewer,o.evidence,loadCharacter),null,2));return;}
  if(command==='demo') {
    if(!fs.existsSync(charDir('hero-reference'))) {
      const spec=createCharacter('hero-reference','Humano','Warrior');
      spec.status='reference_only';spec.name='Human Warrior Pilot / Hero do sandbox';
      spec.appearance={face:'Humano masculino adulto/jovem-adulto, cabelo castanho, expressao seria.',body:'Proporcoes compactas do piloto; nao obrigatorias para outras racas.',palette:['prata','azul-marinho','couro marrom','ouro contido'],dominantHand:'Revisao entre vistas pendente no historico',asymmetries:['capa e espada'],lighting:'Consultar ancora.'};
      spec.outfit.equipmentMode='embedded-pilot-exception';spec.outfit.description='Armadura do piloto. Opcional como referencia, nao uniforme global.';
      const dir=charDir(spec.id);json(path.join(dir,'character.json'),spec);
      const source=path.join(ROOT,'references/tacticsrpg/Assets/Resources/Characters/WarriorPilot');
      for(const p of pngFiles(source)) {
        let rel=slash(path.relative(source,p)).replaceAll('warrior_pilot','hero_reference');
        const dest=inside(path.join(dir,'sprites'),rel);write(dest,fs.readFileSync(p));
        appendAsset(dir,{kind:'source-reference',file:`sprites/${rel}`,sha256:hash(fs.readFileSync(p)),provider:'TacticsRPG-existing-pilot',source:slash(path.relative(ROOT,p)),note:'Copia de evidencia. Sem aprovacao adicional.'});
      }
      prepare(spec.id,'concept');
    }
    for(const [name,race,job] of [['orc-01','Orc','Warrior'],['undead-01','Undead','Archer']]) if(!fs.existsSync(charDir(name))) createCharacter(name,race,job);
    if(!fs.existsSync(charDir('orc-01-archer'))) createCharacter('orc-01-archer','Orc','Archer','orc-01');
    console.log(JSON.stringify(preview('hero-reference'),null,2));
    console.log('Orc/Undead sao fichas candidatas sem arte inventada. Hero foi copiado como referencia.');return;
  }
  required(o,'id');const {dir,spec}=loadCharacter(o.id);
  if(command==='refresh-base') {
    if(!spec.derivedFrom) throw Error('Ficha nao e variante de roupa.');
    const parent=loadCharacter(spec.derivedFrom.character);
    if(parent.spec.identityId!==spec.identityId || parent.spec.race.id!==spec.race.id) throw Error('Base de outra identidade.');
    spec.appearance=structuredClone(parent.spec.appearance);
    spec.references.find(r=>r.character===parent.spec.id).sourceDigest=digest(parent.spec,parent.dir,'concept');
    json(path.join(dir,'character.json'),spec);prepare(o.id,'outfit');console.log('Base atualizada; gates anteriores ficam desatualizados por hash.');return;
  }
  if(command==='prepare') {if(!['concept','outfit'].includes(o.purpose??'concept')) requireConcept(spec,dir);console.log(JSON.stringify(prepare(o.id,o.purpose??'concept',o.state??'Idle'),null,2));return;}
  if(command==='import') {
    required(o,'input','kind');const input=path.resolve(o.input);const image=decode(input);
    let rel;
    if(o.kind==='concept') {required(o,'name');rel=`concepts/${id(o.name)}.png`;}
    else if(o.kind==='sprite') {required(o,'slot');requireConcept(spec,dir);rel=`sprites/${assertSlot(spec,o.slot)}`;
      if(o.slot.startsWith('Animations/')&&!approval(spec,dir,'base')) throw Error('Revisao humana da base/vistas pendente: review --gate base.');
      if(image.image.width!==spec.profile.width || image.image.height!==spec.profile.height || image.colorType!==6 || image.image.depth!==8) throw Error('Sprite deve ser RGBA8 nativo no canvas da ficha. Nao reduzimos conceito.');
    } else throw Error('--kind concept|sprite');
    const target=inside(dir,rel);if(fs.existsSync(target)&&!o.force) throw Error('Arquivo existente; outro nome ou --force. Revisoes serao invalidadas.');
    write(target,fs.readFileSync(input));appendAsset(dir,{kind:o.kind,file:rel,sha256:image.sha256,provider:o.provider??'manual-unspecified',model:o.model??'unknown',sourceFile:path.basename(input),preparedPromptSha256:fs.existsSync(path.join(dir,'handoff/prompt.md'))?hash(fs.readFileSync(path.join(dir,'handoff/prompt.md'))):null,promptUsage:'NOT_VERIFIED: hash do pacote preparado; nao comprova o prompt realmente enviado ao gerador.'});
    console.log(`Importado sem reescala: ${rel}`);return;
  }
  if(command==='compose') {
    required(o,'manifest');requireConcept(spec,dir);
    const manifest=readJSON(path.resolve(o.manifest));if(manifest.schemaVersion!==1 || !Array.isArray(manifest.frames)||!manifest.frames.length) throw Error('Manifesto de camadas invalido.');
    const staged=[],slots=new Set();
    for(const frame of manifest.frames) {
      assertSlot(spec,frame.slot);if(slots.has(frame.slot)) throw Error('Slot duplicado.');slots.add(frame.slot);
      if(frame.slot.startsWith('Animations/')&&!approval(spec,dir,'base')) throw Error('Revisao humana da base/vistas pendente.');
      if(!Array.isArray(frame.layers)||!frame.layers.length) throw Error('Frame sem camadas.');
      const layers=frame.layers.map(p=>{const file=inside(path.join(dir,'source/layers'),p),decoded=decode(file);if(decoded.colorType!==6||decoded.image.depth!==8) throw Error('Camada deve ser RGBA8.');return {file,...decoded};});
      const target=inside(path.join(dir,'sprites'),frame.slot);if(fs.existsSync(target)&&!o.force) throw Error('Destino existe; use --force.');
      staged.push({target,image:composite(layers.map(l=>l.image),spec.profile.width,spec.profile.height),slot:frame.slot,layers:layers.map(l=>({file:slash(path.relative(dir,l.file)),sha256:l.sha256}))});
    }
    for(const frame of staged) {savePNG(frame.target,frame.image);appendAsset(dir,{kind:'composed-native-2d',file:`sprites/${frame.slot}`,sha256:hash(fs.readFileSync(frame.target)),layers:frame.layers});}
    console.log(`${staged.length} frames compostos. Nenhuma peca nova foi desenhada pelo comando.`);return;
  }
  if(command==='preview') {console.log(JSON.stringify(preview(o.id),null,2));return;}
  if(command==='validate') {
    const report=validate(spec,dir,o.stage??'full');json(path.join(dir,'reports/validation.json'),report);console.log(JSON.stringify(report.summary,null,2));return report.summary.FAIL?1:0;
  }
  if(command==='review') {
    required(o,'gate','decision','reviewer','evidence');
    if(!['concept','base','consistency','in-game'].includes(o.gate)||!['approved','changes_requested'].includes(o.decision)) throw Error('Gate/decisao invalida.');
    if(spec.status==='reference_only') throw Error('Aprovacao de referencia historica nao pode virar aprovacao de producao.');
    if(o.decision==='approved') {
      if(o.gate==='concept'&&!pngFiles(path.join(dir,'concepts')).length) throw Error('Sem conceito PNG para revisar.');
      if(o.gate!=='concept') {
        requireConcept(spec,dir);const r=validate(spec,dir,o.gate==='base'?'directions':'full');if(r.summary.FAIL) throw Error('Revisao exige inventario da etapa sem falhas tecnicas.');
        if(o.gate==='consistency'&&!approval(spec,dir,'base')) throw Error('Revisao da base/vistas pendente.');
        if(o.gate==='in-game'&&(!approval(spec,dir,'consistency')||!approval(spec,dir,'base'))) throw Error('Gate 2 ou revisao da base pendente.');
      }
    }
    const reviews=readJSON(path.join(dir,'reviews.json'));reviews.push({at:now(),gate:o.gate,decision:o.decision,reviewer:o.reviewer,evidence:o.evidence,digest:digest(spec,dir,o.gate),attestation:'Registro informado pelo operador; nao e autenticacao nem aprovacao por testes.'});json(path.join(dir,'reviews.json'),reviews);console.log('Revisao humana registrada para estes arquivos e esta ficha.');return;
  }
  if(command==='export') {
    requireConcept(spec,dir);
    if(!approval(spec,dir,'base')) throw Error('Revisao humana da base/vistas ausente, rejeitada ou desatualizada.');
    if(spec.profile.width!==128 || spec.profile.height!==128 || spec.profile.ppu!==100 || spec.profile.counts.Walk!==6 || ['Idle','Walk','Attack','Hit','Defeat'].some(s=>!Object.hasOwn(spec.profile.counts,s)) || Object.keys(spec.profile.counts).some(s=>!['Idle','Walk','Attack','Hit','Defeat'].includes(s))) throw Error('Perfil exige extensao Unity nao implementada. Exportador atual entrega apenas baseline 128x128/PPU100/Walk6 e os cinco estados conhecidos.');
    const report=validate(spec,dir,'full');json(path.join(dir,'reports/validation.json'),report);if(report.summary.FAIL) throw Error('Validacao falhou; consulte reports/validation.json.');
    if(!approval(spec,dir,'consistency')) throw Error('Gate 2: consistencia ainda sem aprovacao explicita valida.');
    const build=hash(JSON.stringify({content:digest(spec,dir,'consistency'),reviews:readJSON(path.join(dir,'reviews.json'))})).slice(0,16), dest=inside(path.join(ROOT,'dist'),`${spec.id}/${build}`);
    if(fs.existsSync(dest)) {console.log(`Build ja existente, preservado: ${dest}`);return;}
    const output=path.join(dest,'Assets/Resources/Characters',spec.id);
    for(const slot of expectedSlots(spec)) write(path.join(output,slot),fs.readFileSync(path.join(dir,'sprites',slot)));
    json(path.join(output,'factory-manifest.json'),{schemaVersion:1,id:spec.id,build,ppu:spec.profile.ppu,profile:spec.profile,sourceDigest:digest(spec,dir,'consistency'),gate1:approval(spec,dir,'concept'),gate2:approval(spec,dir,'consistency'),gate3:approval(spec,dir,'in-game')??'PENDING_PLAYMODE',runtimeRegistration:'REQUIRES_EXTENSION: UnitVisuals esta fixa em WarriorPilot',files:report.measurements.map(m=>({path:m.file,sha256:m.sha256}))});
    write(path.join(dest,'Assets/Editor/CharacterFactoryImporter.cs'),fs.readFileSync(path.join(ROOT,'unity/CharacterFactoryImporter.cs')));
    write(path.join(dest,'INTEGRATION.md'),fs.readFileSync(path.join(ROOT,'docs/UNITY.md')));
    json(path.join(dest,'validation.json'),report);console.log(`Exportado para revisao: ${dest}\nRegistro no Unity e Gate 3 permanecem pendentes.`);return;
  }
  throw Error(`Comando desconhecido: ${command}`);
}

if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  try {process.exitCode=run()??0;} catch(error) {console.error('ERRO:',error.message);process.exitCode=2;}
}
