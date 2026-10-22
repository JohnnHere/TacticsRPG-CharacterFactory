import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { ROOT, files, hash, json, now, slash, slug, write, escapeHTML } from './core.mjs';

const documents = [
  'AGENTS.md', 'Docs/AGENTS.md', 'Docs/ART_DIRECTION.md', 'Docs/GAMEPLAY.md', 'Docs/ROADMAP.md',
  'Docs/GameDesign/DOCUMENT_INDEX.md', 'Docs/GameDesign/DESIGN_DECISIONS.md',
  'Docs/GameDesign/RACES.md', 'Docs/GameDesign/RACIAL_ABILITIES.md',
  'Docs/GameDesign/JOB_CATALOG.md', 'Docs/GameDesign/JOB_SYSTEM.md',
  'Docs/GameDesign/JOB_ACCESS_RULES.md', 'Docs/GameDesign/FACTIONS_AND_RECRUITMENT.md',
  'Docs/Art/CHARACTER_PIPELINE.md', 'Docs/Art/Characters/CHARACTER_TEMPLATE.md',
  'Docs/Art/Characters/HUMAN_WARRIOR_PILOT.md', 'Docs/Art/Characters/HUMAN_WARRIOR_DIRECTIONS.md',
  'Docs/Art/Characters/HUMAN_WARRIOR_ANIMATIONS.md', 'Docs/Art/References/character_style_anchor_v1.png',
  'Assets/Scripts/Presentation/UnitVisuals.cs', 'Assets/Scripts/Presentation/UnitView.cs',
  'Assets/Tests/EditMode/DirectionMappingTests.cs', 'Assets/Tests/EditMode/IdleFrameTests.cs', 'Assets/Tests/EditMode/WalkFrameTests.cs'
];
export function syncReferences(source, accept = false) {
  source = path.resolve(source);
  const skill = '.agents/skills/character-art-design', pilot = 'Assets/Resources/Characters/WarriorPilot';
  const selected = [...documents, ...files(path.join(source, skill)).map(p => slash(path.relative(source,p))), ...files(path.join(source,pilot)).map(p => slash(path.relative(source,p)))];
  const entries = selected.map(p => {
    const b = fs.readFileSync(path.join(source,p));
    return { originalPath:p, path:`tacticsrpg/${p}`, sha256:hash(b), bytes:b.length,
      role:p.includes('character_style_anchor') ? 'global-style-anchor-declared-approved-in-source' : p.includes('WarriorPilot') ? 'pilot-reference-only' : p.endsWith('.cs') ? 'runtime-evidence-snapshot' : 'source-document' };
  });
  const manifestPath=path.join(ROOT,'references/manifest.json');
  if(fs.existsSync(manifestPath) && !accept) throw Error('Snapshot ja existe. Revise alteracoes e use sync --accept-update para atualizar; isso invalida revisoes antigas.');
  for (const e of entries) {
    const target=path.join(ROOT,'references',e.path);
    fs.mkdirSync(path.dirname(target),{recursive:true}); fs.copyFileSync(path.join(source,e.originalPath),target);
  }
  // Catalog IDs are factory-local identifiers, never asserted to be runtime JobId/RaceId.
  const races=fs.readFileSync(path.join(source,'Docs/GameDesign/RACES.md'),'utf8').split(/\r?\n/).filter(l=>l.startsWith('| ') && l.split('|').length===9 && !l.includes('Raça |')).map(l=>{
    const c=l.split('|').slice(1,-1).map(s=>s.trim());
    return {id:slug(c[0]),name:c[0],fantasy:c[1],cultureProposal:c[4],bodyProfile:c[6],source:'references/tacticsrpg/Docs/GameDesign/RACES.md',status:'source-design-not-runtime'};
  });
  const jobs=fs.readFileSync(path.join(source,'Docs/GameDesign/JOB_CATALOG.md'),'utf8').split(/\r?\n/).filter(l=>/^\| (Básica|Intermediária|Avançada|Secreta|Única) \|/.test(l)).map(l=>{
    const c=l.split('|').slice(1,-1).map(s=>s.trim());
    return {id:slug(c[1]),name:c[1],category:c[0],role:c[2],affinities:c[5],source:'references/tacticsrpg/Docs/GameDesign/JOB_CATALOG.md',status:'source-design-not-runtime',approvedVisualRecipe:null};
  });
  if(races.length!==28 || jobs.length!==63 || new Set(jobs.map(j=>j.id)).size!==63) throw Error(`Catalogo divergente: ${races.length} racas, ${jobs.length} Jobs. Revisao necessaria.`);
  json(path.join(ROOT,'catalogs/races.json'),races); json(path.join(ROOT,'catalogs/jobs.json'),jobs);
  let revision='unknown', dirty=null;
  try {revision=execFileSync('git',['-C',source,'rev-parse','HEAD'],{encoding:'utf8',stdio:['ignore','pipe','ignore']}).trim();dirty=!!execFileSync('git',['-C',source,'status','--porcelain'],{encoding:'utf8'}).trim();}catch{}
  const manifest={schemaVersion:1,capturedAt:now(),sourceRoot:slash(path.relative(ROOT,source)),revision,sourceWasDirty:dirty,
    note:'Snapshot exato dos arquivos locais, inclusive modificacoes nao commitadas. Git HEAD sozinho nao identifica este conteudo. Hero e evidencia de piloto; nenhuma nova aprovacao artistica.', files:entries};
  json(manifestPath,manifest);
  write(path.join(ROOT,'references/index.html'),`<!doctype html><html lang="pt-br"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Referencias TacticsRPG</title><style>body{font:16px system-ui;background:#20222a;color:#eee;margin:24px;max-width:1000px}a{color:#87ceff}img{max-width:100%;width:480px;image-rendering:pixelated}li{margin:8px 0}code{overflow-wrap:anywhere}</style><h1>Referencias da Character Factory</h1><p>Snapshot ${manifest.capturedAt}. Origem tinha alteracoes locais: ${dirty}. 28 racas / 63 Jobs. Manifesto registra hashes.</p><h2>Ancora aprovada: linguagem visual</h2><img src="tacticsrpg/Docs/Art/References/character_style_anchor_v1.png"><h2>Hero: piloto de referencia</h2><p>Identidade, roupa, anatomia e cores nao sao regra universal. Prototipo com pendencias de revisao artistica.</p><img style="width:384px" src="tacticsrpg/Assets/Resources/Characters/WarriorPilot/warrior_pilot_mvp1_static_128.png"><h2>Documentos e evidencia</h2><ul>${entries.filter(e=>e.originalPath.endsWith('.md')||e.originalPath.endsWith('.cs')).map(e=>`<li><a href="${escapeHTML(e.path)}">${escapeHTML(e.originalPath)}</a> — ${escapeHTML(e.role)}</li>`).join('')}</ul></html>`);
  return {files:entries.length,races:races.length,jobs:jobs.length,sourceWasDirty:dirty};
}
export function verifyReferences() {
  const p=path.join(ROOT,'references/manifest.json');
  if(!fs.existsSync(p)) return [{path:'manifest.json',error:'Execute sync primeiro.'}];
  const manifest=JSON.parse(fs.readFileSync(p,'utf8'));
  return manifest.files.flatMap(e=>{
    const p=path.join(ROOT,'references',e.path);
    return fs.existsSync(p)&&hash(fs.readFileSync(p))===e.sha256 ? [] : [{path:e.path,error:'Snapshot ausente ou alterado; sincronize conscientemente.'}];
  });
}
