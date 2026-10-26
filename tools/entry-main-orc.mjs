// Attack-ENTRY assembler for the MAIN ORC (orc-v1).
// `experiments/main-orc-entry-v1/entry-plan.json` is the only sequence/art authority. This tool resolves
// exact baseline polish-v1 layers plus orchestrator inputs exported in Aseprite, assembles an isolated
// candidate, and checks its contracts. It authors nothing, relocates nothing by heuristic, and changes
// neither the active equipment selection, Unity, nor any delivered asset.
// Modes: resolve | build | verify. Artifact measurement here is diagnostic, never artistic acceptance.
import fs from 'node:fs';
import path from 'node:path';
import {ROOT,hash,inside} from '../src/core.mjs';
import {findAseprite,executeAseprite,exportAseprite} from '../src/aseprite.mjs';
import {decode,measure} from '../src/images.mjs';

const E='experiments/main-orc-entry-v1';
const PLAN=`${E}/entry-plan.json`;
const RESOLVED=`${E}/entry-plan.resolved.json`;
const CONTRACT=`${E}/contract.json`;
const CATEGORIES=['Sword','Axe'];
const LAYER_ORDER=['weaponBack','body','weaponFront','handFront'];
// Preparation phases are reported separately from strike acceleration. The numbers below only describe
// the entry motion; they never approve or reject the artwork.
const ENTRY_PHASES=new Set(['rest','body-preparation','establish-grip','entry-elbow-lift','entry-shoulder-coil','load','preparation','anticipation','raise','guard','high-guard','cocked-shoulder']);
const DIAGNOSTIC={gripStepPx:24,angleStepDeg:90,maxFrameMs:600};
const abs=p=>path.join(ROOT,p);
const readJSON=p=>JSON.parse(fs.readFileSync(abs(p),'utf8').replace(/^\uFEFF/,''));
const writeJSON=(p,value)=>{fs.mkdirSync(path.dirname(abs(p)),{recursive:true});fs.writeFileSync(abs(p),JSON.stringify(value,null,2)+'\n')};
const sha=p=>hash(fs.readFileSync(abs(p)));
const fail=message=>{throw Error(`entry-main-orc: ${message}`)};
const pad=i=>String(i).padStart(2,'0');
const angleDelta=(a,b)=>{let d=(b-a)%360;if(d>180)d-=360;if(d<-180)d+=360;return d};
const round2=v=>Math.round(v*100)/100;

function resolvePlan(){
  if(!fs.existsSync(abs(PLAN)))fail(`plano ausente: ${PLAN}. O scaffold NÃO cria plano padrão, não reposiciona a mão e não inventa arte.
Forneça {revision,baseline,output,masters,sequences:{Sword:[...],Axe:[...]},impactIndex:{Sword:n,Axe:n}}.
Cada entrada: {fromCategory,index,durationMs,phase?,visible?,grip?,angle?,bodyInput?,handInput?}.
bodyInput/handInput são PNGs FULL 256x256 exportados no Aseprite em ${E}/inputs/.`);
  const plan=readJSON(PLAN),c=readJSON(CONTRACT);
  if(typeof plan.revision!=='string'||!plan.revision)fail('revision obrigatório');
  for(const key of ['baseline','output','masters'])if(plan[key]!==c[key])fail(`${key}='${plan[key]}' diverge do contrato '${c[key]}'`);
  if(!plan.sequences||typeof plan.sequences!=='object')fail('sequences obrigatório');
  if(!plan.impactIndex||typeof plan.impactIndex!=='object')fail('impactIndex obrigatório');
  const inputs=[];
  const input=(value,label)=>{
    if(value===undefined||value===null)return null;
    if(typeof value!=='string'||!value)fail(`${label} deve ser caminho de arquivo`);
    if(!value.startsWith(`${E}/inputs/`))fail(`${label} deve estar em ${E}/inputs/ (recebido ${value})`);
    if(!value.endsWith('.png'))fail(`${label} deve ser .png exportado no Aseprite (recebido ${value})`);
    // Prefix alone is not confinement: 'inputs/../../x' still starts with it.
    inside(ROOT,value);
    if(!fs.existsSync(abs(value)))fail(`${label} inexistente: ${value}`);
    const d=decode(abs(value));
    if(d.image.width!==c.canvas[0]||d.image.height!==c.canvas[1])fail(`${label} deve ter ${c.canvas[0]}x${c.canvas[1]} (recebido ${d.image.width}x${d.image.height})`);
    if(d.colorType!==6)fail(`${label} precisa PNG RGBA (colorType=${d.colorType})`);
    const record=inputs.find(r=>r.path===value)??{field:label,path:value,sha256:d.sha256};
    if(!inputs.includes(record))inputs.push(record);
    return record;
  };
  const sequences={};
  for(const category of CATEGORIES){
    const list=plan.sequences[category];
    if(!Array.isArray(list)||list.length<2)fail(`sequences.${category} deve ser lista com ao menos 2 entradas`);
    const baseClip=readJSON(`${c.baseline}/${category}/Attack/clip.json`);
    sequences[category]=list.map((entry,i)=>{
      const at=`sequences.${category}[${i}]`;
      if(!CATEGORIES.includes(entry.fromCategory))fail(`${at}.fromCategory deve ser Sword ou Axe`);
      const source=readJSON(`${c.baseline}/${entry.fromCategory}/Attack/clip.json`).frames[entry.index];
      if(!Number.isInteger(entry.index)||!source)fail(`${at}.index inválido para a base ${entry.fromCategory}`);
      if(!Number.isInteger(entry.durationMs)||entry.durationMs<1||entry.durationMs>DIAGNOSTIC.maxFrameMs)fail(`${at}.durationMs deve ser inteiro 1..${DIAGNOSTIC.maxFrameMs}`);
      const visible=entry.visible??source.weaponVisible;
      if(typeof visible!=='boolean')fail(`${at}.visible precisa ser booleano na base ou no plano`);
      const plannedGrip=entry.grip??source.rightGrip,grip=visible?plannedGrip:null;
      if(visible&&(!Array.isArray(grip)||grip.length!==2||grip.some(v=>!Number.isInteger(v))))fail(`${at} visível sem grip inteiro utilizável`);
      const angle=visible?(entry.angle??source.rotationDeg):null;
      if(visible&&typeof angle!=='number')fail(`${at} visível sem angle utilizável`);
      return {fromCategory:entry.fromCategory,index:entry.index,durationMs:entry.durationMs,visible,phase:entry.phase??source.phase??'entry',grip,angle,plannedGrip,weaponBehindBody:visible?!!source.weaponBehindBody:false,bodySource:source.layers.body.png,handSource:source.layers.handFront.png,bodyInput:input(entry.bodyInput,`${at}.bodyInput`),handInput:input(entry.handInput,`${at}.handInput`)};
    });
    const seq=sequences[category];
    if(seq[0].visible)fail(`sequences.${category}[0] deve ser sem arma: o Idle costura com o repouso`);
    if(seq[seq.length-1].visible)fail(`sequences.${category}[${seq.length-1}] deve ser sem arma: o retorno ao Idle precisa do corpo neutro`);
    const armed=seq.flatMap((q,i)=>q.visible?[i]:[]);
    if(armed.length<2)fail(`sequences.${category} precisa de ao menos 2 quadros armados`);
    if(!armed.every((v,i)=>i===0||v===armed[i-1]+1))fail(`sequences.${category} tem intervalo de arma não contíguo (${armed.join(',')}): visibleInterval exige bloco único`);
    const impact=plan.impactIndex[category];
    if(!Number.isInteger(impact)||impact<0||impact>=seq.length)fail(`impactIndex.${category} inválido`);
    if(!seq[impact].visible)fail(`impactIndex.${category} aponta para quadro sem arma`);
  }
  return {plan,contract:c,sequences,inputs};
}

const luaPlan=({plan,contract:c,sequences})=>({revision:plan.revision,baseline:c.baseline,output:c.output,masters:c.masters,layerOrder:LAYER_ORDER,canvas:c.canvas,bodyOffset:c.bodyOffset,groundY:c.groundY,ppu:c.ppu,impactIndex:plan.impactIndex,planSha256:sha(PLAN),sequences:Object.fromEntries(CATEGORIES.map(category=>[category,sequences[category].map(q=>({fromCategory:q.fromCategory,index:q.index,durationMs:q.durationMs,visible:q.visible,phase:q.phase,grip:q.grip,angle:q.angle,plannedGrip:q.plannedGrip,weaponBehindBody:q.weaponBehindBody,bodySource:q.bodySource,handSource:q.handSource,bodyInput:q.bodyInput?.path??null,handInput:q.handInput?.path??null}))]))});

function resolve(){
  const resolved=resolvePlan();
  writeJSON(RESOLVED,luaPlan(resolved));
  const summary={plan:PLAN,resolved:RESOLVED,planSha256:sha(PLAN),inputs:resolved.inputs,sequences:Object.fromEntries(CATEGORIES.map(k=>[k,{frames:resolved.sequences[k].length,totalMs:resolved.sequences[k].reduce((s,q)=>s+q.durationMs,0),impact:resolved.plan.impactIndex[k],bodyInputs:resolved.sequences[k].filter(q=>q.bodyInput).length}]))};
  console.log(JSON.stringify({status:'RESOLVED',...summary},null,2));
  return resolved;
}

function build(){
  const resolved=resolve(),{plan,contract:c,sequences}=resolved;
  const baselineManifest=readJSON(`${c.baseline}/manifest.json`);
  const lua=mode=>executeAseprite(findAseprite(),['--script-param','root='+ROOT,'--script-param','mode='+mode,'--script-param','plan='+abs(RESOLVED),'--script',abs('tools/aseprite/entry-main-orc.lua')]);
  lua('assemble');
  for(const category of CATEGORIES){
    const out=`${c.output}/${category}/Attack`,stem=`${c.masters}/${category.toLowerCase()}`,seq=sequences[category];
    const frames=seq.map((q,i)=>{const ref=name=>{const png=`${out}/layers/${name}/${pad(i)}.png`;return{png,sha256:sha(png)}};return{body:ref('body'),handFront:ref('handFront'),durationMs:q.durationMs,phase:q.phase,grip:q.grip,angle:q.angle,scale:1,weaponVisible:q.visible,weaponBehindBody:q.weaponBehindBody}});
    const baselineProfile=readJSON(`${c.baseline}/${category}/Attack/profile.json`);
    const profile={id:baselineProfile.id,character:'orc-v1',category,direction:baselineProfile.direction,canvas:c.canvas,bodyOffset:c.bodyOffset,groundY:c.groundY,ppu:c.ppu,bodyMaster:`${stem}-body.aseprite`,handMaster:`${stem}-hand-front.aseprite`,frames,itemContract:baselineProfile.itemContract,artisticApproval:'PENDING_CREATOR',revision:plan.revision,baselineRevision:baselineManifest.revision};
    writeJSON(`${out}/profile.json`,profile);
    const clipBase=readJSON(`${c.baseline}/${category}/Attack/clip.json`);
    writeJSON(`${E}/${category}-composition.json`,{category,item:{id:clipBase.weapon.id,sprite:clipBase.weapon.sprite,grip:clipBase.weapon.grip,category},profile:`${out}/profile.json`,bodyProfile:profile,output:out,scope:'ISOLATED_ENTRY_CANDIDATE from entry-plan.json; no active selection, runtime or gameplay change'});
    executeAseprite(findAseprite(),['--script-param','root='+ROOT,'--script-param','plan='+abs(`${E}/${category}-composition.json`),'--script',abs('tools/aseprite/compose-compatible-main-orc-item.lua')]);
  }
  lua('finish');
  const clips=[],jobs=[];
  for(const category of CATEGORIES){
    const seq=sequences[category],out=`${c.output}/${category}/Attack`,stem=`${c.masters}/${category.toLowerCase()}`,profile=readJSON(`${out}/profile.json`),clipBase=readJSON(`${c.baseline}/${category}/Attack/clip.json`),impact=plan.impactIndex[category];
    const frames=profile.frames.map((f,i)=>{
      const q=seq[i];
      return {png:`${out}/${pad(i)}.png`,sha256:sha(`${out}/${pad(i)}.png`),durationMs:f.durationMs,phase:f.phase,weaponVisible:f.weaponVisible,rightGrip:f.grip,rotationDeg:f.angle,scale:1,weaponBehindBody:f.weaponBehindBody,
        sourceMapping:{from:q.fromCategory,index:q.index,ms:q.durationMs,visible:q.visible,plannedGrip:q.plannedGrip,grip:q.grip,angle:q.angle,phase:q.phase,bodyInput:q.bodyInput?.path??null,handInput:q.handInput?.path??null,bodySource:q.bodySource,handSource:q.handSource},
        layers:Object.fromEntries(LAYER_ORDER.map(name=>{const png=`${out}/layers/${name}/${pad(i)}.png`;return[name,{png,sha256:sha(png)}]}))};
    });
    const armed=frames.flatMap((f,i)=>f.weaponVisible?[i]:[]);
    const clip={...clipBase,revision:plan.revision,frameCount:frames.length,master:`${stem}-attack.aseprite`,masterSha256:sha(`${stem}-attack.aseprite`),bodyMaster:`${stem}-body.aseprite`,bodyMasterSha256:sha(`${stem}-body.aseprite`),handMaster:`${stem}-hand-front.aseprite`,handMasterSha256:sha(`${stem}-hand-front.aseprite`),frames,layerOrder:LAYER_ORDER,visibilityPolicy:'attack-only-v1',visibleInterval:[armed[0],armed[armed.length-1]],hideAfterAction:true,contactEvent:{frame:impact,timeMs:frames.slice(0,impact).reduce((s,f)=>s+f.durationMs,0),status:'CANDIDATE_VISUAL_ONLY',appliesDamage:false},artisticApproval:'PENDING_CREATOR',runtimeImplemented:false,baselineRevision:baselineManifest.revision,entryPlan:PLAN,entryPlanSha256:sha(PLAN)};
    writeJSON(`${out}/clip.json`,clip);
    clips.push({state:'Attack',category,clip:`${out}/clip.json`,binding:`${out}/profile.json`,master:clip.master,baseline:clipBase.master});
    for(const [suffix,source,compare,content] of [['attack',clip.master,frames.map(f=>f.png),true],['body',clip.bodyMaster,frames.map(f=>f.layers.body.png),true],['hand-front',clip.handMaster,frames.map(f=>f.layers.handFront.png),false]])
      jobs.push({id:`${category.toLowerCase()}-${suffix}`,source,sourceSha256:sha(source),profile:{width:c.canvas[0],height:c.canvas[1],frames:frames.length,durationsMs:frames.map(f=>f.durationMs),alpha:'binary',requireTransparency:true,requireContent:content},compare});
    jobs.push({id:`${category.toLowerCase()}-item`,source:clipBase.weapon.master,sourceSha256:sha(clipBase.weapon.master),profile:{width:clipBase.weapon.canvas[0],height:clipBase.weapon.canvas[1],frames:1,alpha:'binary',requireTransparency:true},compare:[clipBase.weapon.sprite]});
  }
  for(const state of ['Idle','Walk']){
    const source=`${c.baseline}/${state}/clip.json`,clip=readJSON(source);
    writeJSON(`${c.output}/${state}/clip.json`,clip);
    clips.push({state,clip:source,master:clip.master,alias:true,copy:`${c.output}/${state}/clip.json`});
    jobs.push({id:`${state.toLowerCase()}-unarmed`,source:clip.master,sourceSha256:sha(clip.master),profile:{width:c.canvas[0],height:c.canvas[1],frames:clip.frameCount,durationsMs:clip.frames.map(f=>f.durationMs),alpha:'binary',requireTransparency:true},compare:clip.frames.map(f=>f.png)});
  }
  writeJSON(`${c.output}/manifest.json`,{revision:plan.revision,baselineRevision:baselineManifest.revision,character:'orc-v1',direction:'front_r',canvas:c.canvas,bodyOffset:c.bodyOffset,groundY:c.groundY,ppu:c.ppu,experiment:E,output:c.output,masters:c.masters,baseline:c.baseline,layerOrder:LAYER_ORDER,visibilityPolicy:'attack-only-v1',clips,entryPlan:PLAN,entryPlanSha256:sha(PLAN),inputs:resolved.inputs,artisticApproval:'PENDING_CREATOR',runtimeImplemented:false,selection:'REVIEW_ONLY; equipment-current unchanged'});
  const editor={schemaVersion:1,id:plan.revision,kind:'character',characterId:'orc-v1',jobs};
  writeJSON(`${c.masters}/editor.json`,editor);
  const report=exportAseprite(editor);
  writeJSON(`${E}/build.json`,{status:report.status,path:report.path,reused:report.reused??false,summary:report.summary,planSha256:sha(PLAN),createdAt:new Date().toISOString()});
  console.log(JSON.stringify({status:'ISOLATED_ENTRY_CANDIDATE',revision:plan.revision,output:c.output,masters:c.masters,build:report.path,buildStatus:report.status,summary:report.summary,cloudCalls:0,selectionChanged:false},null,2));
}

function verify(){
  const {plan,contract:c,sequences}=resolvePlan();
  const checks=[];
  const add=(file,check,status,detail)=>checks.push({file,check,status,detail});
  const check=(file,name,valid,detail)=>add(file,name,valid?'PASS':'FAIL',detail);
  const manifestPath=`${c.output}/manifest.json`;
  if(!fs.existsSync(abs(manifestPath)))fail(`saída ausente: ${manifestPath}. Rode 'build'.`);
  const manifest=readJSON(manifestPath),baselineManifest=readJSON(`${c.baseline}/manifest.json`);
  check('manifest','revision',manifest.revision===plan.revision,manifest.revision);
  check('manifest','baseline',manifest.baseline===c.baseline&&manifest.baselineRevision===baselineManifest.revision,`${manifest.baseline} · ${manifest.baselineRevision}`);
  check('manifest','selection',/REVIEW_ONLY/.test(manifest.selection??''),String(manifest.selection));
  check('manifest','approval',manifest.artisticApproval==='PENDING_CREATOR',manifest.artisticApproval);
  check('manifest','runtime',manifest.runtimeImplemented===false,String(manifest.runtimeImplemented));
  check('manifest','plan',manifest.entryPlanSha256===sha(PLAN),'montagem usa o plano atual');
  check('manifest','inputs',JSON.stringify(manifest.inputs)===JSON.stringify(CATEGORIES.flatMap(k=>sequences[k]).flatMap(s=>[...(s.bodyInput?[s.bodyInput]:[]),...(s.handInput?[s.handInput]:[])]).filter((r,i,a)=>a.findIndex(x=>x.path===r.path)===i)),'hashes dos inputs do plano');
  const equipment=readJSON('characters/orc-v1/source/equipment-current.json');
  check('characters/orc-v1/source/equipment-current.json','selection-unchanged',equipment.revision==='main-orc-onehanded-v3'&&equipment.manifest.includes('onehanded-rescue-v3'),`${equipment.revision} · ${equipment.manifest}`);
  for(const category of CATEGORIES){
    const seq=sequences[category],out=`${c.output}/${category}/Attack`,clipPath=`${out}/clip.json`,profilePath=`${out}/profile.json`;
    check(category,'contract-files',fs.existsSync(abs(clipPath))&&fs.existsSync(abs(profilePath)),`${clipPath} · ${profilePath}`);
    if(!fs.existsSync(abs(clipPath))||!fs.existsSync(abs(profilePath)))continue;
    const clip=readJSON(clipPath),profile=readJSON(profilePath),baseClip=readJSON(`${c.baseline}/${category}/Attack/clip.json`);
    check(category,'frame-count',clip.frameCount===seq.length&&profile.frames.length===seq.length,`${clip.frameCount}/${profile.frames.length} vs plano ${seq.length}`);
    check(category,'masters',sha(clip.master)===clip.masterSha256&&sha(clip.bodyMaster)===clip.bodyMasterSha256&&sha(clip.handMaster)===clip.handMasterSha256,'composite, corpo e dedos');
    check(category,'canvas',JSON.stringify(clip.canvas)===JSON.stringify(c.canvas)&&JSON.stringify(clip.bodyOffset)===JSON.stringify(c.bodyOffset)&&clip.groundY===c.groundY&&clip.ppu===c.ppu,`${clip.canvas} offset ${clip.bodyOffset} chão ${clip.groundY} ppu ${clip.ppu}`);
    check(category,'visibility-policy',clip.visibilityPolicy==='attack-only-v1'&&clip.hideAfterAction===true,clip.visibilityPolicy);
    check(category,'weapon-identity',JSON.stringify(clip.weapon)===JSON.stringify(baseClip.weapon)&&sha(clip.weapon.sprite)===clip.weapon.spriteSha256&&sha(clip.weapon.master)===clip.weapon.masterSha256,`${clip.weapon.id} preservada`);
    const armed=clip.frames.flatMap((f,i)=>f.weaponVisible?[i]:[]);
    check(category,'visible-interval',JSON.stringify(clip.visibleInterval)===JSON.stringify([armed[0],armed[armed.length-1]]),JSON.stringify(clip.visibleInterval));
    check(category,'unarmed-boundaries',!clip.frames[0].weaponVisible&&clip.frames[0].rightGrip===null&&!clip.frames[clip.frames.length-1].weaponVisible,'primeiro e último quadro sem arma');
    check(category,'rest-continuity',sha(clip.frames[0].layers.body.png)===sha(baseClip.frames[0].layers.body.png)&&sha(clip.frames[clip.frames.length-1].layers.body.png)===sha(baseClip.frames[0].layers.body.png),'corpo neutro idêntico ao Idle atual nas duas pontas');
    check(category,'impact',clip.contactEvent.frame===plan.impactIndex[category]&&clip.contactEvent.timeMs===clip.frames.slice(0,clip.contactEvent.frame).reduce((s,f)=>s+f.durationMs,0)&&clip.contactEvent.appliesDamage===false,`quadro ${clip.contactEvent.frame} · ${clip.contactEvent.timeMs} ms · evento visual`);
    const steps=[];
    for(let i=1;i<seq.length;i++){
      const a=seq[i-1],b=seq[i];if(!ENTRY_PHASES.has(a.phase)&&!ENTRY_PHASES.has(b.phase))continue;
      steps.push({from:i-1,to:i,phases:[a.phase,b.phase],gripStepPx:a.plannedGrip&&b.plannedGrip?round2(Math.hypot(b.plannedGrip[0]-a.plannedGrip[0],b.plannedGrip[1]-a.plannedGrip[1])):null,angleStepDeg:a.angle!==null&&b.angle!==null?round2(Math.abs(angleDelta(a.angle,b.angle))):null});
    }
    clip.frames.forEach((f,i)=>{
      const q=seq[i],tag=`${category}[${i}]`;
      check(tag,'metadata',f.durationMs===q.durationMs&&f.phase===q.phase&&f.weaponVisible===q.visible&&f.rotationDeg===q.angle&&JSON.stringify(f.rightGrip)===JSON.stringify(q.grip)&&f.weaponBehindBody===q.weaponBehindBody&&f.scale===1,`${f.durationMs}ms ${f.phase} vis=${f.weaponVisible} grip=${JSON.stringify(f.rightGrip)} ang=${f.rotationDeg} atrás=${f.weaponBehindBody}`);
      check(tag,'layers',LAYER_ORDER.every(n=>fs.existsSync(abs(f.layers[n].png))&&sha(f.layers[n].png)===f.layers[n].sha256)&&sha(f.png)===f.sha256,'4 camadas + composto com hash');
      check(tag,'body-source',sha(f.layers.body.png)===(q.bodyInput?q.bodyInput.sha256:sha(q.bodySource)),q.bodyInput?`input ${q.bodyInput.path}`:`baseline ${q.bodySource}`);
      check(tag,'hand-source',!q.visible?measure(decode(abs(f.layers.handFront.png)).image).transparent===c.canvas[0]*c.canvas[1]:(q.handInput?sha(f.layers.handFront.png)===q.handInput.sha256:sha(f.layers.handFront.png)===sha(q.handSource)),!q.visible?'camada vazia (sem arma)':(q.handInput?`input ${q.handInput.path}`:`baseline ${q.handSource}`));
      const px=measure(decode(abs(f.png)).image);
      check(tag,'frame-contract',px.bottom===c.groundY&&px.partial===0&&(q.visible?px.contentHeight>0:px.transparent>0),`chão ${px.bottom} · alfa parcial ${px.partial}`);
      if(q.visible){
        const hand=decode(abs(f.layers.handFront.png)).image,[gx,gy]=q.grip;let covered=0;
        for(let y=Math.max(0,gy-6);y<=Math.min(c.canvas[1]-1,gy+6);y++)for(let x=Math.max(0,gx-6);x<=Math.min(c.canvas[0]-1,gx+6);x++)if(Math.hypot(x-gx,y-gy)<=6&&hand.data[(y*c.canvas[0]+x)*4+3]>0)covered++;
        add(tag,'grip-fingers',covered>0?'PASS':'FAIL',`${covered} px de luva no raio 6 do grip`);
      }
    });
    const entryMs=clip.frames.slice(0,clip.contactEvent.frame).reduce((s,f)=>s+f.durationMs,0),totalMs=clip.frames.reduce((s,f)=>s+f.durationMs,0);
    add(category,'entry-steps','INFO',JSON.stringify(steps));
    add(category,'timing','INFO',`entrada ${entryMs} ms · impacto ${clip.contactEvent.timeMs} ms · total ${totalMs} ms`);
    add(category,'art','REQUIRES_HUMAN_REVIEW','anatomia, trajetória, pegada e continuidade dependem do criador; números acima são descritivos');
  }
  for(const state of ['Idle','Walk']){
    const source=`${c.baseline}/${state}/clip.json`;
    check(state,'alias',fs.existsSync(abs(`${c.output}/${state}/clip.json`))&&sha(`${c.output}/${state}/clip.json`)===sha(source),`${state} idêntico ao baseline`);
    check(state,'weaponless',readJSON(source).frames.every(f=>!f.weaponVisible),'sem arma');
  }
  const buildInfo=fs.existsSync(abs(`${E}/build.json`))?readJSON(`${E}/build.json`):null;
  check('export','aseprite-build',buildInfo?.status==='PASS',buildInfo?`${buildInfo.path} · ${JSON.stringify(buildInfo.summary)}`:'build.json ausente; rode build');
  add('.','unity','NOT_RUN','fora do escopo; nenhuma escrita no projeto Unity');
  add('.','preservation','NOT_RUN','mapa completo de arte anterior validado pelo orquestrador; aqui: hashes de baseline/armas efetivamente reutilizados');
  add('.','artistic-approval','PENDING_CREATOR','validação técnica não é aprovação artística');
  const summary=Object.fromEntries(['PASS','FAIL','WARNING','INFO','NOT_RUN','REQUIRES_HUMAN_REVIEW'].map(s=>[s,checks.filter(x=>x.status===s).length]));
  writeJSON(`${E}/entry-check.json`,{schemaVersion:1,revision:plan.revision,createdAt:new Date().toISOString(),planSha256:sha(PLAN),diagnostic:DIAGNOSTIC,summary,checks});
  console.log(JSON.stringify({status:summary.FAIL?'FAIL':'PASS',summary,report:`${E}/entry-check.json`},null,2));
  if(summary.FAIL)process.exitCode=1;
}

const mode=process.argv[2]??'build';
if(mode==='resolve')resolve();
else if(mode==='build')build();
else if(mode==='verify')verify();
else fail(`modo inválido '${mode}'; use resolve, build ou verify`);
