import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { ROOT, DIRECTIONS, now, json, write, readJSON, hash, slash, charDir, loadCharacter, catalogEntry, expectedSlots, approval, digest, inside, escapeHTML, pngFiles } from './core.mjs';
import { decode, contactSheet, validate } from './images.mjs';
import { activeRecipe } from './recipes.mjs';

export function createCharacter(name, raceName, jobName, from) {
  const dir=charDir(name);
  if(fs.existsSync(dir)) throw Error('ID ja existe. Use outro ID; arquivos existentes sao preservados.');
  const race=catalogEntry('races',raceName), job=catalogEntry('jobs',jobName), style=readJSON(path.join(ROOT,'config/style.json'));
  const parent=from?loadCharacter(from):null;
  const jobRecipe=activeRecipe('jobs',job.id),raceRecipe=parent?.spec.styleRecipes?.find(r=>r.kind==='races')??activeRecipe('races',race.id);
  if(parent && parent.spec.race.id!==race.id) throw Error('Variante de roupa preserva raca. Crie outro personagem para outra raca.');
  const spec={schemaVersion:1,id:name,identityId:parent?.spec.identityId??crypto.randomUUID(),name:name,
    status:'candidate',createdAt:now(),styleId:style.id,race:{id:race.id,name:race.name,bodyProfile:race.bodyProfile},
    job:{id:job.id,name:job.name},role:'TBD',culture:'TBD',faction:'TBD',form:'base',
    appearance:parent?structuredClone(parent.spec.appearance):{face:'TBD',ageImpression:'TBD',body:'TBD',palette:[],dominantHand:'TBD',asymmetries:[],lighting:'Observar a ancora; direcao numerica nao canonizada.'},
    outfit:jobRecipe?.outfit?structuredClone(jobRecipe.outfit):{id:job.id+'-candidate',description:'TBD — definir silhueta e materiais de classe; personagem base sem arma, asset de arma separado; sem receita visual aprovada.',silhouette:'TBD',palette:[],materials:[],equipmentMode:'weapon-independent-base',weapon:'TBD — asset separado, sem desenho no corpo base'},
    styleRecipes:[raceRecipe,jobRecipe].filter(Boolean),
    profile:structuredClone(parent?.spec.profile??style.baselineProfile),
    references:[{path:style.anchor,role:'global-style-anchor'},...(parent?[{character:from,role:'same-individual-body-and-face',sourceDigest:digest(parent.spec,parent.dir,'concept')}]:[])],
    derivedFrom:parent?{character:from,purpose:'outfit-variant',mustPreserve:['identityId','race','appearance'],conceptApprovalAtCreation:!!approval(parent.spec,parent.dir,'concept')}:null,
    reuseAssessment:[
      {component:'rendering/reference contract',category:'REUSE_DIRECT',evidence:'Docs/ART_DIRECTION.md + ancora',adaptation:'Aplicar ao novo corpo; revisar em escala de jogo.'},
      {component:'race anatomy/face',category:parent?'REUSE_ADAPTED':'CREATE_NEW',evidence:parent?from:'RACES.md fornece perfil, sem modelo racial aprovado.',adaptation:'TBD',artRisk:'TBD',technicalRisk:'Validar canvas/escala',dependencies:[],validation:'NOT_RUN',productionImpact:'TBD'},
      {component:'job outfit',category:'CREATE_NEW',evidence:job.source,adaptation:'TBD',artRisk:'Identidade de classe deve permanecer entre racas.',technicalRisk:'Camadas por vista/quadro',dependencies:[],validation:'NOT_RUN',productionImpact:'TBD'},
      {component:'Unity registration',category:'REQUIRES_EXTENSION',evidence:'UnitVisuals fixa WarriorPilot.',adaptation:'Registro multi-personagem externo a esta fabrica.',validation:'NOT_RUN'}
    ]};
  json(path.join(dir,'character.json'),spec);
  for(const p of ['concepts','source/layers','sprites','handoff','reports']) fs.mkdirSync(path.join(dir,p),{recursive:true});
  json(path.join(dir,'assets.json'),[]); json(path.join(dir,'reviews.json'),[]);
  json(path.join(dir,'source/layers.example.json'),{schemaVersion:1,frames:[{slot:`${name.replaceAll('-','_')}_mvp1_static_128.png`,layers:['body_front_r.png','outfit_front_r.png']}],note:'Camadas do personagem base sem arma. Assets de arma sao independentes e requerem render por equipamento/acao; o compose atual nao implementa essa invocacao.'});
  prepare(name,'concept');
  return spec;
}

export function prepare(name,purpose='concept',state='Idle') {
  if(!['concept','base','directions','animation','outfit'].includes(purpose)) throw Error('purpose: concept, base, directions, animation ou outfit.');
  const {dir,spec}=loadCharacter(name), style=readJSON(path.join(ROOT,'config/style.json'));
  if(!Object.hasOwn(spec.profile.counts,state)) throw Error('Estado fora do perfil.');
  if(purpose!=='concept' && purpose!=='outfit' && !approval(spec,dir,'concept')) throw Error('Gate 1 pendente: registre a aprovacao explicita do conceito antes de solicitar sprites.');
  if(purpose==='animation') {
    const missing=expectedSlots(spec,'directions').filter(s=>!fs.existsSync(path.join(dir,'sprites',s)));
    if(missing.length) throw Error('Validar base/vistas antes das animacoes.');
    if(validate(spec,dir,'directions').summary.FAIL || !approval(spec,dir,'base')) throw Error('Base/vistas exigem validacao e revisao humana valida (review --gate base) antes das animacoes.');
  }
  const job=catalogEntry('jobs',spec.job.id),race=catalogEntry('races',spec.race.id);
  const parent=spec.derivedFrom?loadCharacter(spec.derivedFrom.character):null;
  const refs=[{path:style.anchor,role:style.anchorRole},{path:'references/tacticsrpg/Assets/Resources/Characters/WarriorPilot/warrior_pilot_mvp1_static_128.png',role:style.pilotRole},
    ...(spec.styleRecipes??[]).flatMap(r=>r.images),
    ...pngFiles(path.join(dir,'concepts')).map(p=>({path:slash(path.relative(ROOT,p)),role:'Conceito deste personagem; conferir reviews.json para aprovacao.'})),
    ...(parent?pngFiles(path.join(parent.dir,'concepts')).map(p=>({path:slash(path.relative(ROOT,p)),role:'Preservar identidade do individuo base; conferir aprovacao antes de usar como verdade.'})):[])];
  const instruction=spec.status==='reference_only' ? 'Consultar este piloto como referencia historica de leitura/implementacao. Descrever e revisar o material existente. Para criar arte nova, abrir outro ID de personagem.' : purpose==='concept'||purpose==='outfit' ? 'Criar candidato de conceito 2D para aprovacao; nao produzir lote de sprites/animacoes finais nesta etapa.' : purpose==='base' ? `Produzir UMA base estatica front_r em pixel art nativa ${spec.profile.width}x${spec.profile.height}, RGBA transparente.` : purpose==='directions' ? `Produzir as quatro vistas ${DIRECTIONS.join(', ')} individualmente, com anatomia e mao dominante coerentes.` : `Trabalhar ${state}, ${spec.profile.counts[state]} quadros/vista; iniciar por front_r e revisar antes das demais vistas. Nao criar o pacote todo automaticamente.`;
  const sourceFiles=['Docs/ART_DIRECTION.md','Docs/GameDesign/DESIGN_DECISIONS.md','Docs/GameDesign/RACES.md','Docs/GameDesign/JOB_CATALOG.md','Docs/GameDesign/JOB_ACCESS_RULES.md','Docs/Art/CHARACTER_PIPELINE.md','Docs/Art/Characters/CHARACTER_TEMPLATE.md','.agents/skills/character-art-design/SKILL.md','.agents/skills/character-art-design/references/design-and-reuse.md','.agents/skills/character-art-design/references/production.md'];
  const instructions=`# Pedido de criacao — ${spec.id}\n\nEtapa: ${purpose}. ${instruction}\n\nLeia AGENTS.md e os documentos apontados em handoff.json. Abra e observe as imagens antes de gerar.\n\n## Identidade e fontes\n\nRaca: ${race.name}; perfil documentado: ${race.bodyProfile}; fantasia: ${race.fantasy}.\nJob: ${job.name}; papel: ${job.role}. Afinidades sao contexto, sem bloqueio racial.\nFicha completa: character.json anexado. Campos TBD sao lacunas/propostas, nunca fatos aprovados.\n\n${style.principles.map(x=>'- '+x).join('\n')}\n\n${spec.derivedFrom?`Variante do MESMO individuo ${spec.derivedFrom.character}. Preservar rosto, anatomia, tracos e assimetrias; ${spec.derivedFrom.purpose==='outfit-variant'?'mudar roupa/equipamento do Job':'preservar tambem a roupa aprovada nesta reautoria/refinamento'}. Base aprovada agora: ${!!(parent&&approval(parent.spec,parent.dir,'concept'))}. Se pendente, produzir somente proposta e declarar a pendencia.\n`:''}\nHero e referencia opcional de leitura e implementacao. Seu cabelo, armadura, arma e cores nao sao um uniforme do jogo.\n\n## Autoria obrigatoria no Aseprite\n\nDecisao expressa do criador em 2026-10-22: TODA a producao de arte deve acontecer no Aseprite, incluindo conceitos, sprites, poses, animacoes e acabamento. A fonte .aseprite salva e o arquivo mestre; PNGs/folhas sao derivados. Autoria por scripts Lua executados no Aseprite e permitida, com codigo, procedencia e referencias registrados; declarar que e autoria programatica do agente, nao desenho manual nem geracao inteligente do editor.\nNao usar image_gen ou outra geracao externa para produzir arte nova sem nova instrucao explicita do criador. Nao desenhar/reconstruir/recolorir pixels fora do Aseprite. Ferramentas externas podem organizar metadados, comparar hashes/pixels e montar previews sem alterar a arte. Legados aprovados preservam sua procedencia original.\nUsar processos batch ocultos enquanto o criador usa a maquina; nao disputar a GUI. Sem Aseprite disponivel, registrar NOT_RUN e o bloqueio real; nao substituir a ferramenta. Preservar gates e copiar referencias sem promover historicos rejeitados.\n\n## Entrega\n\nSalvar candidatos PNG sem substituir refs aprovadas, registrar prompt/modelo quando conhecidos, mostrar preview e solicitar avaliacao artistica do lote. Nao autoaprovar. Conceito em resolucao alta permanece em concepts/. Sprite nativo precisa de producao propria e entra em sprites/ somente via importacao validada.\n\n## Ficha resolvida\n\n\`\`\`json\n${JSON.stringify(spec,null,2)}\n\`\`\`\n`;
  write(path.join(dir,'handoff/prompt.md'),instructions);
  const allDocs=sourceFiles.map(p=>({path:`references/tacticsrpg/${p}`,sha256:hash(fs.readFileSync(path.join(ROOT,'references/tacticsrpg',p)))}));
  json(path.join(dir,'handoff/handoff.json'),{schemaVersion:1,createdAt:now(),character:slash(path.relative(ROOT,path.join(dir,'character.json'))),purpose,state,referenceRoot:'Caminhos relativos a raiz deste repositorio',images:refs,documents:allDocs,specSha256:hash(JSON.stringify(spec))});
  write(path.join(dir,'handoff/context.md'),`# Instrucoes da fabrica\n\n${fs.readFileSync(path.join(ROOT,'AGENTS.md'),'utf8')}\n\n# Contrato visual derivado\n\n${JSON.stringify(style,null,2)}\n\n---\n\n`+allDocs.map(d=>`# ${d.path}\n\n${fs.readFileSync(path.join(ROOT,d.path),'utf8')}`).join('\n\n---\n\n'));
  write(path.join(dir,'brief.md'),`# ${name}\n\n${race.name} / ${job.name}. Status: ${spec.status}.\n\nConceitos e sprites-base mostram corpo e roupa sem armas empunhadas, carregadas ou embainhadas. Armas sao assets independentes e so aparecem quando equipadas e invocadas por uma acao. A espada embutida do Human Warrior Pilot e excecao historica. O runtime atual ainda nao suporta overlays dinamicos de arma.\n\nEdite character.json para definir individuo, cultura, faccao, forma, paleta, mao dominante, silhueta/roupa e Reuse Assessment. Regenere com prepare.\n\nNao ha producao de arte automatica ao criar esta ficha. Pacote para o agente: handoff/prompt.md + handoff/handoff.json + imagens indicadas + handoff/context.md.\n`);
  return {package:slash(path.relative(ROOT,path.join(dir,'handoff'))),purpose,images:refs.length};
}

export function preview(name) {
  const {dir,spec}=loadCharacter(name);
  const style=readJSON(path.join(ROOT,'config/style.json'));
  const spriteRoot=path.join(dir,'sprites'),known=expectedSlots(spec).map(s=>path.join(spriteRoot,s)).filter(p=>fs.existsSync(p));
  const knownSet=new Set(known);
  const images=[path.join(ROOT,style.anchor), ...pngFiles(path.join(dir,'concepts')), ...known, ...pngFiles(spriteRoot).filter(p=>!knownSet.has(p))];
  const rel=p=>slash(path.relative(dir,p));
  const cards=images.map(p=>`<figure><img src="${escapeHTML(rel(p))}" loading="lazy"><figcaption>${escapeHTML(rel(p))}</figcaption></figure>`).join('\n');
  const html=`<!doctype html><html lang="pt-br"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>${escapeHTML(name)} — revisao visual</title><style>body{font:16px system-ui;background:#20222a;color:#eee;margin:24px}main{display:flex;flex-wrap:wrap;gap:16px}figure{margin:0;width:288px;padding:12px;border:1px solid #737985;border-radius:8px}img{width:256px;height:256px;object-fit:contain;image-rendering:pixelated;background:repeating-conic-gradient(#666 0 25%,#444 0 50%) 0/16px 16px}figcaption{overflow-wrap:anywhere;font-size:13px}button{font:inherit;padding:8px}body.light{background:#eee;color:#111}a{color:#87ceff}</style><h1>${escapeHTML(name)}</h1><p>${escapeHTML(spec.race.name)} / ${escapeHTML(spec.job.name)} — referencia de estilo primeiro; conceitos e sprites depois. Aprovacao artistica pendente ate registro explicito. Zoom do browser permite revisar pixels.</p><button onclick="document.body.classList.toggle('light')">Fundo claro/escuro</button><main>${cards}</main></html>`;
  write(path.join(dir,'preview.html'),html);
  // Contact sheet includes first 4 references/sprites only; full inventory is in HTML.
  contactSheet(images.slice(0,16),path.join(dir,'contact-sheet.png'));
  return {html:path.join(dir,'preview.html'),contactSheet:path.join(dir,'contact-sheet.png'),images:images.length};
}
