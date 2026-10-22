import fs from 'node:fs';
import path from 'node:path';
import { ROOT, id, inside, now, json, readJSON, write, hash, digest, approval, pngFiles, slash } from './core.mjs';

function recipeRoot(kind,key) {
  if(!['races','jobs'].includes(kind)) throw Error('--kind races|jobs');
  return inside(path.join(ROOT,'recipes',kind),id(key));
}
export function activeRecipe(kind,key) {
  const active=path.join(recipeRoot(kind,key),'active.json');if(!fs.existsSync(active)) return null;
  const pointer=readJSON(active),file=inside(ROOT,pointer.path);
  if(hash(fs.readFileSync(file))!==pointer.sha256) throw Error('Receita aprovada alterada; preservar versao e criar outra.');
  const recipe=readJSON(file);
  for(const image of recipe.images) if(hash(fs.readFileSync(inside(ROOT,image.path)))!==image.sha256) throw Error('Imagem da receita aprovada foi alterada.');
  return {...recipe,path:pointer.path,sha256:pointer.sha256};
}
export function saveRecipe(spec,dir,kind,force=false) {
  const key=kind==='jobs'?spec.job.id:spec.race.id,root=recipeRoot(kind,key),target=root+'.candidate.json';
  if(fs.existsSync(target)&&!force) throw Error('Receita candidata existente. Edite-a ou use --force conscientemente.');
  const recipe={schemaVersion:1,kind,key,status:'candidate',createdAt:now(),sourceCharacter:spec.id,
    sourceConceptDigest:digest(spec,dir,'concept'),rules:[],
    guidance:kind==='jobs'?'Defina regras de silhueta, roupa, materiais e variacao de Job que valham entre racas. Nao incluir pele/rosto do individuo.':'Defina anatomia racial e variacao permitida. Nao transformar um rosto/Job/faccao em regra racial.',
    ...(kind==='jobs'?{outfit:structuredClone(spec.outfit)}:{bodyProfile:spec.race.bodyProfile}),
    images:pngFiles(path.join(dir,'concepts')).map(p=>({path:slash(path.relative(ROOT,p)),sha256:hash(fs.readFileSync(p))}))};
  json(target,recipe);return {candidate:target,note:'Edite rules e revise antes de recipe-review.'};
}
export function reviewRecipe(kind,key,decision,reviewer,evidence,load) {
  const root=recipeRoot(kind,key),candidate=root+'.candidate.json',recipe=readJSON(candidate);
  if(recipe.kind!==kind||recipe.key!==key) throw Error('Identidade da receita divergente.');
  if(decision==='changes_requested') {recipe.status=decision;recipe.review={at:now(),reviewer,evidence};json(candidate,recipe);return {candidate,status:decision};}
  if(decision!=='approved') throw Error('--decision approved|changes_requested');
  const source=load(recipe.sourceCharacter);
  if(!approval(source.spec,source.dir,'concept')||digest(source.spec,source.dir,'concept')!==recipe.sourceConceptDigest) throw Error('Conceito de origem precisa de aprovacao valida; regenere a receita candidata se a base mudou.');
  if(!Array.isArray(recipe.rules)||!recipe.rules.length||recipe.rules.some(r=>typeof r!=='string'||!r.trim()||/\bTBD\b/i.test(r))) throw Error('Preencha rules com regras visuais revisadas; TBD nao e receita aprovada.');
  if(!recipe.images.length) throw Error('Receita sem referencia visual.');
  let version=1;while(fs.existsSync(path.join(root,`v${version}`))) version++;
  const dest=path.join(root,`v${version}`);
  recipe.images=recipe.images.map((img,i)=>{
    const file=inside(ROOT,img.path),data=fs.readFileSync(file);if(hash(data)!==img.sha256) throw Error('Imagem candidata alterada.');
    const target=path.join(dest,`reference-${String(i+1).padStart(2,'0')}.png`);write(target,data);return {path:slash(path.relative(ROOT,target)),sha256:hash(data),role:kind==='jobs'?'Linguagem de Job; anatomia e individuo continuam na ficha.':'Anatomia racial; Job/individuo continuam na ficha.'};
  });
  recipe.status='approved';recipe.version=version;recipe.review={at:now(),reviewer,evidence};
  const file=path.join(dest,'recipe.json');json(file,recipe);
  json(path.join(root,'active.json'),{path:slash(path.relative(ROOT,file)),sha256:hash(fs.readFileSync(file))});
  return {version,path:file,status:'approved',note:'Versao arquivada com copias dos PNGs; novas fichas usam esta versao.'};
}
