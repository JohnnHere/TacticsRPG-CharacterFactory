// Preserve the previous review before refining unapproved PixelLab candidates.
import fs from 'node:fs';
import path from 'node:path';
import {ROOT, hash} from '../src/core.mjs';

const relative='experiments/pixellab-orc-refinement-v2';
const root=path.join(ROOT,relative);
const snapshot=path.join(root,'before');
if (fs.existsSync(path.join(root,'before-manifest.json'))) throw Error('Immutable snapshot already exists.');
fs.mkdirSync(snapshot,{recursive:true});
const entries=[];
function copyTree(source,destination){
  fs.mkdirSync(destination,{recursive:true});
  for(const item of fs.readdirSync(source,{withFileTypes:true})){
    const from=path.join(source,item.name),to=path.join(destination,item.name);
    if(item.isDirectory()) copyTree(from,to);
    else if(item.isFile()){
      fs.copyFileSync(from,to);
      entries.push({original:path.relative(ROOT,from).replaceAll('\\','/'),snapshot:path.relative(ROOT,to).replaceAll('\\','/'),sha256:hash(fs.readFileSync(from))});
    }
  }
}
for(const id of ['04','05','06','07'])copyTree(path.join(ROOT,`characters/orc-pixellab-${id}`),path.join(snapshot,`orc-pixellab-${id}`));
copyTree(path.join(ROOT,'reports/orc-pixellab-v4-comparison'),path.join(snapshot,'comparison'));
fs.writeFileSync(path.join(root,'before-manifest.json'),JSON.stringify({createdAt:new Date().toISOString(),entries},null,2)+'\n');

const idle='Idle. A calm alert standing guard, breathing slowly and shallowly. Only a tiny expansion of the chest and a subtle settling of the shoulders; the head stays almost still. Both feet remain firmly planted in the exact same ground positions. Arms hang relaxed. Keep the same facing, face, anatomy, armor and palette. No stepping, turning, crouching, head gestures, rocking or exaggerated body bob. A restrained seamless breathing loop, full body, empty hands, transparent background, fixed camera.';
const walk='Walking in place through one complete clear two-step walk cycle. The legs drive the action: left leg reaches forward and plants while the right leg extends behind; right heel lifts, knee bends and the right boot swings visibly off the ground past the support leg; then reverse the legs for the second step. Alternate contact, down, passing and up poses. Each boot must visibly travel forward and backward and lift several pixels during its swing, rather than remain anchored. Moderate natural stride, opposite arm swing and slight weight transfer. Preserve the character design, armor, face, palette and three-quarter facing while freely articulating hips, knees and ankles. Fixed camera, centered full body, both boots visible, empty hands, no weapons, transparent background. Seamless cycle returning to its initial contact pose.';
const concept='Original highly detailed medieval dark-fantasy tactical RPG pixel art. A towering adult male orc shock infantry veteran, inspired by the intimidating organized Uruk-hai archetype of Tolkien and the strong silhouette clarity of Warcraft. Tall long-legged powerful anatomy, broad angular shoulders, deep chest, narrow waist, thick neck, roughly seven-head proportions; imposing and battle-hardened, not squat or rounded. Ash-grey skin, severe scarred angular face, pronounced brow, uneven blunt tusks, short coarse black hair. Elaborate functional blackened iron armor: overlapping angular breastplate panels with a raised central ridge, layered articulated pauldrons, riveted neck guard, segmented vambraces, small chainmail at joints, lamellar hip tassets, reinforced knee plates and armored boots. Distinct steel bevels, fasteners, leather straps, worn edge highlights, restrained dents and scratches; carefully shaded large metal planes remain readable. Dark gunmetal, cold steel edges, oxblood cloth and aged brown leather. Brutal disciplined infantry presence, chin slightly lowered and gaze challenging. Both hands empty and relaxed beside the body. Entire figure from head to both complete boots, front three-quarter standing view, centered in a 128x128 transparent canvas with clear margin on every side. Crisp deliberate pixel clusters, rich material detail and controlled contrast. No held, carried or sheathed weapon, shield, scenery, text, franchise insignia or named character.';
const jobs=[['04','Walk'],['04','Idle'],['07','Walk'],['07','Idle'],['06','Idle'],['05','Idle'],['05','Walk']].map(([id,state])=>({id:`orc-pixellab-${id}`,state,prompt:state==='Idle'?idle:walk,status:'PREPARED_NOT_SUBMITTED',input: id==='05'?'PENDING_REVISED_CONCEPT':`characters/orc-pixellab-${id}/concepts/concept-selected.png`}));
const brief={createdAt:new Date().toISOString(),status:'PREPARED_WAITING_UPDATED_EXTENSION_PERMISSIONS',provider:'PixelLab official Aseprite extension',scope:'Refine Walk and Idle 04/07, restrained Idle 06, redesign 05 armor/presence and match its Idle/Walk to the new concept.',concept05:{prompt:concept,status:'PREPARED_NOT_SUBMITTED',inputImages:[],styleImages:[]},jobs,artisticApproval:'PENDING_CREATOR',unityIntegration:'NOT_RUN',actualAccountDebit:'NOT_EXPOSED'};
fs.writeFileSync(path.join(root,'brief.json'),JSON.stringify(brief,null,2)+'\n');
console.log(JSON.stringify({snapshot:relative+'/before',files:entries.length,plannedAnimationJobs:jobs.length,conceptRevisions:1}));
