// Small per-category pose tables, no skeletal runtime or item-specific body generation.
import fs from 'node:fs';import path from 'node:path';import {ROOT} from '../src/core.mjs';
const E='experiments/main-orc-weapon-rescue-v3',B='characters/orc-v1/source/onehanded-rescue-v3',M='characters/orc-v1/source/aseprite/onehanded-rescue-v3';
const read=p=>JSON.parse(fs.readFileSync(path.join(ROOT,p),'utf8'));const weapons=read(E+'/weapon-revisions.json');const rest='characters/orc-v1/source/studies/Idle/00.png';
const f=(input,phase,durationMs,grip,angle,hand,cleanup=[],footShift=null,behind=false)=>({input,phase,durationMs,grip,angle,visible:!!grip,hand,cleanup,footShift,behind});
const source=i=>`${E}/sword-posed/raw/${String(i).padStart(2,'0')}.png`;
const profiles={Sword:{id:'basic.sword-slash',weapon:weapons.sword,frames:[
 f(rest,'rest',80,null,0,[]),
 f(source(0),'load',100,[29,66],270,[[[24,63],[28,62],[29,66],[26,69],[23,67]],[[28,65],[34,65],[34,68],[30,70],[26,68]]],[[[14,63],[24,63],[24,72],[14,72]],[[35,58],[41,58],[41,72],[35,72]]]),
 f(source(1),'high-guard',130,[34,25],345,[[[29,22],[33,21],[35,25],[34,29],[30,28]],[[34,23],[38,23],[39,26],[35,27]]],[],null,true),
 f(source(3),'drive',65,[93,48],20,[[[90,44],[94,44],[96,47],[95,51],[91,52],[89,49]],[[94,47],[98,47],[98,50],[95,52]]],[[[86,0],[97,0],[97,39],[101,40],[101,45],[82,45],[82,40],[86,39]],[[92,56],[99,56],[99,64],[92,64]]],5),
 f(`${E}/sword-strike/raw/00.png`,'crossing',55,[94,70],55,[[[88,67],[92,65],[95,67],[96,71],[93,74],[89,73]],[[94,68],[98,69],[98,73],[95,75]]],[[[99,55],[127,15],[128,15],[128,39],[106,68]]],4),
 f(source(5),'strike-follow-through',95,[95,78],100,[[[90,74],[94,73],[97,76],[96,80],[92,82],[89,79]],[[95,76],[99,77],[99,81],[96,83]]],[[[101,66],[128,66],[128,80],[101,80]]],3),
 f(`${E}/sword-recovery/raw/00.png`,'recovery',130,[46,83],105,[[[41,80],[44,78],[48,79],[48,84],[45,87],[41,86]],[[45,81],[48,81],[48,85],[45,87]]],[[[31,79],[41,79],[41,88],[31,88]]],1),
 f(rest,'return-unarmed',120,null,0,[])
]}};
// The inpaint protected the original fist, but left a narrow old guard at its edge.
// Clone the already-restored adjacent hip material into that 5x13 area, inside Aseprite.
profiles.Sword.frames[6].cloneSelf={source:[54,75,5,13],target:[49,75]};
const axePlan=path.join(ROOT,E,'axe-profile-authored.json');if(fs.existsSync(axePlan))profiles.Axe=read(E+'/axe-profile-authored.json');
const base=Object.fromEntries(['Idle','Walk'].map(state=>{const c=read(`characters/orc-v1/source/studies/${state}/clip.json`);return[state,{state,loop:true,frames:c.frames.map(a=>({input:a.png,durationMs:a.durationMs})),master:c.master}]}));
const plan={revision:'main-orc-onehanded-v3',character:'orc-v1',direction:'front_r',canvas:[256,256],bodyOffset:[64,64],groundY:190,ppu:100,output:B,masters:M,reference:rest,profiles,base,layerOrder:['weaponBack','body','weaponFront','handFront'],visibilityPolicy:'attack-only-v1'};
fs.writeFileSync(path.join(ROOT,E,'composition-plan.json'),JSON.stringify(plan,null,2));console.log({profiles:Object.keys(profiles),weaponSourceIndependent:true});
