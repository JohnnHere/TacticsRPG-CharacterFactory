// Sanitize the official extension's local generation history; never copy its
// package/settings/authentication fields or any legacy artwork into a study.
import fs from 'node:fs';import path from 'node:path';
import {ROOT,hash} from '../src/core.mjs';import {decode,measure} from '../src/images.mjs';
const history=path.join(process.env.APPDATA,'Aseprite/extensions/pixellab/request_history/generate_image_new/20261023010535.json');
const h=JSON.parse(fs.readFileSync(history,'utf8'));
if(h.reference_images_display?.length||h.style_image_display)throw Error('Unexpected image conditioning');
const source='characters/orc-pixellab-01/source/aseprite/concept-raw.aseprite';
const candidates=[{id:'orc-pixellab-01',title:'Veterano da Vanguarda',frame:1},{id:'orc-pixellab-02',title:'Quebra-Linhas',frame:2},{id:'orc-pixellab-03',title:'Campeão de Bronze',frame:4}];
const sha=p=>hash(fs.readFileSync(path.join(ROOT,p)));const save=(p,v)=>fs.writeFileSync(path.join(ROOT,p),JSON.stringify(v,null,2)+'\n');
for(const c of candidates){
 const base='characters/'+c.id;const spec=JSON.parse(fs.readFileSync(path.join(ROOT,base,'character.json'),'utf8'));
 spec.name=c.title;spec.outfit.description='Proposta independente PixelLab selecionada do frame '+c.frame+' do lote original. '+h.description;spec.appearance.hair='Consultar somente este resultado PixelLab novo; proposta independente.';
 save(base+'/character.json',spec);
 const png=base+'/concepts/concept-selected.png',master=base+'/source/aseprite/concept-selected.aseprite';
 const record={provider:'PixelLab',interface:'official-Aseprite-extension',pluginVersion:'0.4.130',tool:'Create image (Pro)',model:'Pro (UI); generate_image_new (official history)',prompt:h.description,seed:h.seed,inputImages:[],styleImages:[],styleReferenceCount:0,targetPalette:h.palette_choice,maxColors:h.palette_max_colors,smartColors:h.palette_smart,noBackground:h.no_background,outputMethod:h.output_method,canvas:{width:128,height:128},status:'CONCEPT_GENERATED_ANIMATION_STUDIES_PENDING',batch:{source,sha256:sha(source),generatedOutputs:4,selectedFrameZeroBased:c.frame,selectionReason:'Three visually distinct usable outputs from the same new batch; fourth retained for provenance, not discarded.'},outputs:[{png,sha256:sha(png),master,masterSha256:sha(master),metrics:measure(decode(png).image)}],elapsedMs:'NOT_EXPOSED',credits:'UI announces 10–25 generations per batch; actual debit NOT_EXPOSED',artisticApproval:'PENDING_CREATOR',animations:[]};
 save(base+'/source/generation-record.json',record);save(base+'/assets.json',[{at:new Date().toISOString(),kind:'concept',file:'concepts/concept-selected.png',sha256:sha(png),provider:'PixelLab-official-Aseprite-extension',model:record.model,sourceFile:master,sourceSha256:sha(master),prompt:h.description,seed:h.seed,upstreamBatch:source,upstreamFrame:c.frame}]);
 const handoff={schemaVersion:1,purpose:'independent-candidate-animation-study',images:[{path:png,role:'Only permitted image input: this newly generated candidate itself'}],forbiddenInputs:['V4','V4 concept','Hero','global anchor','V5','legacy palette','legacy recipe','legacy pose'],documents:['docs/PIXELLAB_ASEPRITE.md'],prompt:h.description,selection:null,artisticApproval:'PENDING_CREATOR'};
 save(base+'/handoff/handoff.json',handoff);fs.writeFileSync(path.join(ROOT,base,'handoff/prompt.md'),'# '+c.title+'\n\nConceito novo efetivamente gerado por PixelLab, sem imagens/referências. Prompt real:\n\n'+h.description+'\n\nPara Idle/Walk usar somente concepts/concept-selected.png deste pacote. Nenhuma arte legada. São estudos autorizados antes da escolha; não registrar gate como aprovado.\n');
}
save('experiments/pixellab-independent-orc-v1/selected-candidates.json',candidates);
const exp=JSON.parse(fs.readFileSync(path.join(ROOT,'experiments/pixellab-independent-orc-v1/experiment.json'),'utf8'));exp.status='THREE_CONCEPTS_GENERATED_ANIMATIONS_PENDING';exp.generatedOutputs=candidates.map(c=>'characters/'+c.id+'/concepts/concept-selected.png');exp.model='Pro / generate_image_new';exp.seed=h.seed;exp.cost='Actual debit NOT_EXPOSED; one batch of four concepts';save('experiments/pixellab-independent-orc-v1/experiment.json',exp);
console.log(JSON.stringify({status:exp.status,generatedInOneBatch:4,selected:3,styleReferences:0,seed:h.seed}));
