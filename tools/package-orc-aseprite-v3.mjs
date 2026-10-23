// Metadata and review packaging only. Does not create or edit raster pixels.
import fs from 'node:fs';import path from 'node:path';
import {ROOT,hash} from '../src/core.mjs';
const read=p=>JSON.parse(fs.readFileSync(path.join(ROOT,p),'utf8'));
const save=(p,v)=>{fs.mkdirSync(path.dirname(path.join(ROOT,p)),{recursive:true});fs.writeFileSync(path.join(ROOT,p),JSON.stringify(v,null,2)+'\n');};
const base='characters/orc-01-aseprite-v3',v2=read('characters/orc-01-refinement-v2/character.json'),spec=read(base+'/character.json');
spec.name='Orc Warrior — autoria nativa Aseprite v3';spec.role=v2.role;spec.outfit=v2.outfit;
spec.derivedFrom.purpose='same-approved-design-reauthored-in-Aseprite';
spec.authoringPolicy={master:'Aseprite',method:'Agent-authored explicit pixel drawings executed by Aseprite Lua',noImageGeneration:true,externalRasterInputs:0,approval:'PENDING_CREATOR'};
spec.reuseAssessment=[
 {component:'Individual identity and approved outfit',category:'REUSE_DIRECT',evidence:'Approved V2 concept and creator statement in conversation 2026-10-22.',adaptation:'Visual reference only; no raster imported.',artRisk:'New explicit drawings may deviate in face and proportions.',technicalRisk:'No live approved slot modified.',dependencies:['V2 approved reference'],validation:'PENDING_CREATOR',productionImpact:'New isolated study.'},
 {component:'Native pixel artwork and poses',category:'CREATE_NEW',evidence:base+'/source/aseprite/author-orc-v3.lua',adaptation:'Native 128px original drawings, material shading and action silhouettes in Aseprite.',artRisk:'Simpler shading and anatomy than V2; quality is not guaranteed by editor choice.',technicalRisk:'Check compositing, bounds, palette, exact export and cels.',dependencies:['Aseprite Lua runtime'],validation:'TECHNICAL_PASS_ART_REVIEW_PENDING',productionImpact:'Concept1 + Attack5 + Hit3 regional layered frames.'},
 {component:'Timing and review exporter',category:'REUSE_DIRECT',evidence:'V2 durations and src/aseprite.mjs.',adaptation:'Same counts and total action time for equal comparison.',artRisk:'Timing alone cannot establish better motion.',technicalRisk:'Variable timings are not proven in Unity.',dependencies:[],validation:'EDITOR_EXPORT_PASS',productionImpact:'Review only.'},
 {component:'Equipment rig / runtime',category:'REQUIRES_EXTENSION',evidence:'Regional layers do not form a complete body/clothing rig; UnitVisuals still WarriorPilot.',adaptation:'Requires independent bodies, equipment sockets, occlusion and runtime integration.',artRisk:'Hidden anatomy is not finished.',technicalRisk:'No runtime implemented.',dependencies:['Artist review','Unity extension task'],validation:'NOT_RUN',productionImpact:'No Unity writes.'}
];save(base+'/character.json',spec);
const candidate=read('reports/orc-refinement-candidates-v2.json');
const evidence='Apesar de eu ter aprovado essa V2';
save('characters/orc-01-refinement-v2/reports/creator-approval-v2.json',{decision:'approved',reviewer:'Criador',recordedAt:new Date().toISOString(),evidence,scope:'V2 previously shown concept and Attack/Hit studies. No automatic baseline apply or Unity gate.',files:[candidate.concept,...candidate.clips.flatMap(c=>c.after)].map(file=>({file,sha256:hash(fs.readFileSync(path.join(ROOT,file)))}))});
const report=read('reports/orc-aseprite-authorship-v3.json');
const out=base+'/source/aseprite/authored';
const dimension=p=>{const b=fs.readFileSync(path.join(ROOT,p));return [b.readUInt32BE(16),b.readUInt32BE(20)];};
save('reports/orc-aseprite-comparison-v3.json',{
 status:'PENDING_CREATOR',baseline:'V2 approved by creator; prior image_gen art + external reconstruction',candidate:'V3 original pixel authorship in Aseprite Lua; 0 imported art pixels',
 concept:{before:candidate.concept,after:base+'/concepts/aseprite-native-v3.png',beforeResolution:dimension(candidate.concept),afterResolution:[128,128],note:'V2 is a high-resolution concept. V3 is a native pixel concept study; not identical authoring resolution.'},
 clips:candidate.clips.map(c=>({state:c.state,direction:c.direction,before:c.after,after:c.after.map((_,i)=>`${out}/${c.state.toLowerCase()}/${c.state.toLowerCase()}_front_r_${String(i).padStart(2,'0')}.png`),beforeDurationsMs:c.afterDurationsMs,afterDurationsMs:c.afterDurationsMs})),
 sourceReport:'reports/orc-aseprite-authorship-v3.json',build:report.editorBuild,
 layers:read(out+'/authorship.json').documents[0].layers,
 approval:'PENDING_CREATOR',limitations:report.limitations
});console.log('V3 metadata, V2 approval evidence and comparison manifest packaged.');
