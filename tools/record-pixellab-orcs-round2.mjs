// Preserve safe PixelLab provenance and explicit provider-capacity outcomes.
import fs from 'node:fs';
import path from 'node:path';
import {ROOT,loadCharacter,json,hash,slash,now} from '../src/core.mjs';

const pluginRoot=path.join(process.env.APPDATA,'Aseprite','extensions','pixellab');
const paths={
 firstImage:path.join(pluginRoot,'generation_history','2026-10-23_10-01-12 - Create Image S-XL (New, Pixen) - 010','0.png'),
 firstRequest:path.join(pluginRoot,'request_history','pixen','20261023100112.json'),
 selectedRequest:path.join(pluginRoot,'request_history','pixen','20261023100436.json'),
 blockedPixenRequest:path.join(pluginRoot,'request_history','pixen','20261023100549.json'),
 blockedFluxRequest:path.join(pluginRoot,'request_history','generate_pixelart_flux','20261023100701.json')
};
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const safeRequest=(requestFile)=>{
 const source=read(requestFile),keys=['description','model_name','seed','view','direction','detail','outline','init_image','init_image_strength','output_method','no_background','image_size','shading','isometric','oblique_projection'];
 return Object.fromEntries(keys.filter(k=>Object.hasOwn(source,k)).map(k=>[k,source[k]]));
};
const rel=p=>slash(path.relative(ROOT,p));
const completedInput=read(paths.selectedRequest);
const previousInput=read(paths.firstRequest);
const blockedPixenInput=read(paths.blockedPixenRequest),blockedFluxInput=read(paths.blockedFluxRequest);

// Keep the first, cropped model output as a distinct failed-framing attempt.
const c04=loadCharacter('orc-pixellab-04'),attemptDir=path.join(c04.dir,'source','pixellab-results','Concept');
const cropTarget=path.join(attemptDir,'attempt-001-cropped.png');
if(!fs.existsSync(cropTarget))fs.copyFileSync(paths.firstImage,cropTarget);
json(path.join(attemptDir,'attempt-001-request.json'),previousInput);
json(path.join(attemptDir,'selected-request.json'),completedInput);
const record04=read(path.join(c04.dir,'source','generation-record.json'));
record04.prompt=completedInput.description;record04.tool='Create Image S-XL (New, Pixen)';record04.model='pixen';record04.seed=String(completedInput.seed);record04.status='CONCEPT_GENERATED_PENDING_CREATOR_REVIEW';
record04.attempts=[
 {tool:'Create image (Pro)',model:'Pro',outcome:'BLOCKED_FREE_TIER',message:'High load for free tier; temporary limit.',output:null},
 {tool:'Create image (Pro Flash)',model:'Pro Flash',outcome:'BLOCKED_FREE_TIER',message:'High load for free tier; temporary limit.',output:null},
 {tool:'Create Image S-XL (New, Pixen)',model:'pixen',seed:String(previousInput.seed),outcome:'GENERATED_WRONG_FRAMING',output:'source/pixellab-results/Concept/attempt-001-cropped.png',message:'Cropped around the thighs; preserved for comparison and provenance.'},
 {tool:'Create Image S-XL (New, Pixen)',model:'pixen',seed:String(completedInput.seed),outcome:'GENERATED',output:'source/pixellab-results/Concept/0.png',selectedConcept:'concepts/concept-selected.png'}
];
record04.credits='PixelLab UI advertised 1 generation per S-XL image. Two S-XL files were generated; actual account debit NOT_EXPOSED.';
record04.requestSettings=safeRequest(paths.selectedRequest);
record04.attempts[2].requestSettings=safeRequest(paths.firstRequest);
record04.attempts[3].requestSettings=safeRequest(paths.selectedRequest);
record04.outputs[0].alternateAttempts=[{file:'source/pixellab-results/Concept/attempt-001-cropped.png',sha256:hash(fs.readFileSync(cropTarget)),status:'WRONG_FRAMING_NOT_SELECTED',request:'source/pixellab-results/Concept/attempt-001-request.json'}];
json(path.join(c04.dir,'source','generation-record.json'),record04);
const b04=read(path.join(c04.dir,'source','brief.json'));b04.prompt=completedInput.description;b04.inputImages=[];b04.status='CONCEPT_GENERATED_PENDING_CREATOR_REVIEW';json(path.join(c04.dir,'source','brief.json'),b04);
const h04Path=path.join(c04.dir,'handoff','handoff.json');const h04=fs.existsSync(h04Path)?read(h04Path):{schemaVersion:1,purpose:'independent-concept-and-animation-study',requestedAnimations:['Idle','Walk'],approval:'PENDING_CREATOR'};h04.prompt=completedInput.description;h04.images=[];h04.generationStatus='CONCEPT_GENERATED_PENDING_CREATOR_REVIEW';json(h04Path,h04);
fs.writeFileSync(path.join(c04.dir,'handoff','prompt.md'),`# Veterano Ágil\n\n## Estado\n\nConceito PixelLab gerado e embalado em um mestre Aseprite; Idle/Walk ainda não gerados.\n\n## Prompt PixelLab utilizado\n\n${completedInput.description}\n\nGeração de texto no Aseprite, sem init image, imagem de estilo, paleta alvo ou condicionamento por pixels legados.\n`);
const c04assets=read(path.join(c04.dir,'assets.json'));
if(!c04assets.some(a=>a.file==='source/pixellab-results/Concept/attempt-001-cropped.png'))c04assets.push({at:now(),kind:'pixellab-generation-attempt',file:'source/pixellab-results/Concept/attempt-001-cropped.png',sha256:hash(fs.readFileSync(cropTarget)),provider:'PixelLab',model:'pixen',sourceFile:'Aseprite PixelLab generation history',promptUsage:'Exact request preserved next to this attempt; no input image.'});
json(path.join(c04.dir,'assets.json'),c04assets);

// Candidate 05 was submitted to a separate recommended PixelLab model, but the shared free-tier limit blocked it.
const c05=loadCharacter('orc-pixellab-05');
const blockedDir=path.join(c05.dir,'source','pixellab-results');fs.mkdirSync(blockedDir,{recursive:true});
json(path.join(blockedDir,'attempt-001-blocked-request.json'),blockedPixenInput);
json(path.join(blockedDir,'attempt-002-blocked-request.json'),blockedFluxInput);
const r05=read(path.join(c05.dir,'source','generation-record.json'));
r05.provider='PixelLab';r05.interface='official-Aseprite-extension';r05.pluginVersion='0.4.130';r05.tool='Create Image S-XL (New, Pixen) and Create medium-extra large image (PixFlux V3)';r05.model='pixen + generate_pixelart_flux';r05.seed='NOT_APPLICABLE_BLOCKED_REQUESTS';r05.prompt=blockedPixenInput.description;r05.inputImages=[];r05.styleImages=[];r05.referenceImages=[];r05.status='BLOCKED_FREE_TIER';r05.outputMethod='New frame';r05.requestSettingsAttempts=[safeRequest(paths.blockedPixenRequest),safeRequest(paths.blockedFluxRequest)];r05.outputs=[];r05.animations=[];r05.credits='Each UI tool advertised 1 generation per image; both requests were blocked before an output appeared; actual account debit NOT_EXPOSED';r05.attempts=[{tool:'Create Image S-XL (New, Pixen)',model:'pixen',request:'source/pixellab-results/attempt-001-blocked-request.json',outcome:'BLOCKED_FREE_TIER',output:null},{tool:'Create medium-extra large image (PixFlux V3)',model:'generate_pixelart_flux',request:'source/pixellab-results/attempt-002-blocked-request.json',outcome:'BLOCKED_FREE_TIER',output:null}];r05.failure={message:'High load for free tier; provider temporarily limited free-tier requests.',requests:['source/pixellab-results/attempt-001-blocked-request.json','source/pixellab-results/attempt-002-blocked-request.json'],output:null,actualDebit:'NOT_EXPOSED'};
json(path.join(c05.dir,'source','generation-record.json'),r05);
const b05=read(path.join(c05.dir,'source','brief.json'));b05.prompt=blockedFluxInput.description;b05.inputImages=[];b05.status='BLOCKED_FREE_TIER';json(path.join(c05.dir,'source','brief.json'),b05);
const h05Path=path.join(c05.dir,'handoff','handoff.json');const h05=fs.existsSync(h05Path)?read(h05Path):{schemaVersion:1,purpose:'independent-concept-and-animation-study',requestedAnimations:['Idle','Walk'],approval:'PENDING_CREATOR'};h05.prompt=blockedFluxInput.description;h05.images=[];h05.generationStatus='BLOCKED_FREE_TIER';json(h05Path,h05);
fs.writeFileSync(path.join(c05.dir,'handoff','prompt.md'),`# Infante de Ferro\n\n## Estado\n\nDuas solicitações PixelLab foram bloqueadas antes de gerar qualquer imagem pela limitação temporária do plano gratuito. Reenvio pendente.\n\n## Prompt PixelLab enviado (S-XL)\n\n${blockedPixenInput.description}\n\n## Prompt PixelLab enviado (PixFlux V3)\n\n${blockedFluxInput.description}\n\nAmbas sem init image e sem imagens de estilo. As solicitações foram feitas no Aseprite com a extensão oficial PixelLab.\n`);

// Candidate 06 is fully prepared but deliberately not resubmitted after two distinct models returned the same block.
const c06=loadCharacter('orc-pixellab-06');
const old06=read(path.join(c06.dir,'source','brief.json'));
const prompt06=`Full-length pixel art character in a 128x128 transparent square: show the entire orc from head to both complete boots, centered as a compact figure with generous transparent space above and below. Pull the camera back; never crop, zoom in, or let any body part touch the frame. A wiry, underfed adult male orc foot soldier from grim Tolkien-inspired battlefield fantasy: narrow hunched shoulders, long arms, sinewy limbs, bony face, crooked nose, uneven small tusks, long pointed ears, sallow grey-green skin and sparse dark hair. Patched worn leather, scraps of dull iron on only one shoulder and one knee, coarse dark cloth and mismatched bindings. Dusty charcoal, swamp-olive and rust-brown palette, deliberately asymmetrical and rough. A low-ranking survivor with a memorable face and silhouette, not a brute and not a polished champion. Original high-detail medieval fantasy tactical RPG pixel art, expressive face, crisp deliberate pixel clusters and rich worn material detail, front three-quarter standing view. Both hands empty. No weapon held, carried or sheathed, no shield, no text, no scenery, isolated transparent background. Full silhouette visible with clear margin on every side. Original individual; do not reproduce any named character, film design, or franchise emblem.`;
old06.prompt=prompt06;old06.inputImages=[];old06.status='PREPARED_WAITING_FOR_PROVIDER_CAPACITY';json(path.join(c06.dir,'source','brief.json'),old06);
const r06=read(path.join(c06.dir,'source','generation-record.json'));r06.prompt=prompt06;r06.status='PREPARED_WAITING_FOR_PROVIDER_CAPACITY';r06.tool='Create Image S-XL (New, Pixen) or recommended PixelLab model';r06.model='NOT_RUN';r06.seed='NOT_RUN';r06.outputs=[];r06.animations=[];r06.credits='No request submitted after the same free-tier capacity block on two recommended PixelLab models; actual debit NOT_EXPOSED';json(path.join(c06.dir,'source','generation-record.json'),r06);
const h06Path=path.join(c06.dir,'handoff','handoff.json');const h06=fs.existsSync(h06Path)?read(h06Path):{schemaVersion:1,purpose:'independent-concept-and-animation-study',requestedAnimations:['Idle','Walk'],approval:'PENDING_CREATOR'};h06.prompt=prompt06;h06.images=[];h06.generationStatus='PREPARED_WAITING_FOR_PROVIDER_CAPACITY';json(h06Path,h06);
fs.writeFileSync(path.join(c06.dir,'handoff','prompt.md'),`# Soldado da Vala\n\n## Estado\n\nPrompt pronto para uma nova solicitação no PixelLab quando a cota gratuita aceitar geração. Nenhuma imagem de entrada ou referência visual legada.\n\n## Prompt PixelLab preparado\n\n${prompt06}\n`);

const experiment=path.join(ROOT,'experiments','pixellab-independent-orc-round2-v1');
json(path.join(experiment,'selected-candidates.json'),[{id:'orc-pixellab-04',title:'Veterano Ágil',status:'CONCEPT_ONLY_PENDING_IDLE_WALK'},{id:'orc-pixellab-05',title:'Infante de Ferro',status:'BLOCKED_FREE_TIER'},{id:'orc-pixellab-06',title:'Soldado da Vala',status:'PREPARED_WAITING_FOR_PROVIDER_CAPACITY'}]);
const brief=read(path.join(experiment,'brief.json'));brief.status='PARTIALLY_BLOCKED_FREE_TIER';brief.generatedConcepts=1;brief.generatedAlternativeAttempts=1;brief.blockedConcepts=1;brief.preparedNotSubmittedConcepts=1;brief.animationRequestsPlanned=6;brief.animationRequestsCompleted=0;brief.actualCreditDebit='NOT_EXPOSED';brief.artisticApproval='PENDING_CREATOR';json(path.join(experiment,'brief.json'),brief);
json(path.join(experiment,'provider-status.json'),{date:'2026-10-23',status:'PARTIALLY_BLOCKED_FREE_TIER',provider:'PixelLab official Aseprite extension',observedMessage:'High load for free tier; temporarily limiting free-tier requests.',successful:{candidate:'orc-pixellab-04',model:'pixen',concept:'characters/orc-pixellab-04/concepts/concept-selected.png',idle:'NOT_GENERATED',walk:'NOT_GENERATED'},blocked:[{candidate:'orc-pixellab-04',tools:['Create image (Pro)','Create image (Pro Flash)'],outcome:'BLOCKED_FREE_TIER'},{candidate:'orc-pixellab-05',tools:['Create Image S-XL (New, Pixen)','Create medium-extra large image (PixFlux V3)'],requests:[rel(paths.blockedPixenRequest),rel(paths.blockedFluxRequest)],outcome:'BLOCKED_BEFORE_OUTPUT'}],waiting:[{candidate:'orc-pixellab-06',prompt:'characters/orc-pixellab-06/source/brief.json',status:'PREPARED_NOT_SUBMITTED'}],cost:{uiAdvertisedGenerationsPerSxlImage:1,uiAdvertisedGenerationsPerPixFluxImage:1,actualAccountDebit:'NOT_EXPOSED'},inputImages:[],legacyPixelConditioning:0,unityIntegration:'NOT_RUN'});
console.log(JSON.stringify({status:brief.status,concepts:brief.generatedConcepts,blocked:brief.blockedConcepts,waiting:brief.preparedNotSubmittedConcepts},null,2));
