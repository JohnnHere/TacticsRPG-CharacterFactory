import fs from 'node:fs';
import path from 'node:path';
const E='experiments/main-orc-backl-v5base';
const swordBody='characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full';
const base='characters/orc-v1/source/combat-rescue-v5/combat/back_l';
const sdur=[30,65,35,50,45,35,30,35,35,100,55,80,45,90],adur=[40,65,35,80,155,35,115,110,130,50,90,100];
const sp='rest,body-preparation,establish-grip,anticipation,coil-behind,apex-hold,apex-descent,slash-release,contact,follow-through,recoil,settle-grip,release-grip,return-to-guard'.split(',');
const ap='rest,body-preparation,establish-grip,anticipation,overhead-coil,cleave-drive,heavy-impact,follow-through,recoil,settle-grip,release-grip,return-to-guard'.split(',');
const smap=[0,2,3,3,3,3,5,6,7,8,9,10,10,11];
const sbind={2:[163,108,10],3:[157,92,350],5:[169,106,285],6:[162,111,265],7:[150,148,245],8:[152,148,240],9:[157,150,230],10:[157,143,220]};
const amap=[0,0,1,1,2,3,4,5,6,7,7,7];
const v8=JSON.parse(fs.readFileSync('characters/orc-v1/source/combat-recovery-v8/candidate28manifest.json'));
const configs=[];
for(const [name,cat,map,durs,phases,window,contact] of [['sword','Sword',smap,sdur,sp,[2,11],8],['axe','Axe',amap,adur,ap,[2,8],6]]){
 const old=JSON.parse(fs.readFileSync(`${base}/${cat}/clip.json`));
 const cell=v8.cells.find(c=>c.cellId===`back_l/${cat}`);
 const frames=map.map((src,i)=>{
  const armed=i>=window[0]&&i<=window[1]; const dx=(name==='sword'&&i===3)?1:(name==='sword'&&i===4)?-1:(name==='sword'&&i===5)?-2:(name==='axe'&&i===3)?1:0;
  const binding=name==='sword'&&armed?sbind[src]:null;
  return {index:i,sourceIndex:src,phase:phases[i],durationMs:durs[i],weaponVisible:armed,dx,dy:0,
   operation:dx?`adaptação local: translação inteira X=${dx} px; mão sem alteração interna`:'reuso direto',
   decisionStatus:(name==='sword'&&[3,4,5].includes(i))||(name==='axe'&&i===3)?'NEEDS_DECISION':'VISUAL_REVIEW_REQUIRED',
   reason:phases[i]+(dx?'; distingue antecipação/hold sem inventar anatomia':''),
   sourceBody:name==='sword'?`${swordBody}/body256/${String(src).padStart(2,'0')}.png`:old.frames[src].layers.body.png,
   sourceLayers:name==='axe'?old.frames[src].layers:null,
   grip:binding?binding.slice(0,2).map((v,j)=>v+(j===0?dx:0)):(old.frames[src]?.rightGrip??[0,0]).map((v,j)=>v+(j===0?dx:0)),
   angleDeg:binding?binding[2]:(old.frames[src]?.rotationDeg??0),
   handBox:binding?[binding[0]-8,binding[1]-6,binding[0]+8,binding[1]+7]:null};
 });
 configs.push({name,category:cat,bodySource:name==='sword'?swordBody:`${base}/Axe`,weaponDefinition:`characters/orc-v1/source/combat-rescue-v5/combat/weapons/${cat}/weapon.json`,beforeClip:cell.clipJson,frames,durationsMs:durs,phases,visibleInterval:window,contactEvent:{frame:contact,timeMs:durs.slice(0,contact).reduce((a,b)=>a+b,0),phase:phases[contact],appliesDamage:false}});
}
fs.writeFileSync(`${E}/author-config.json`,JSON.stringify(configs,null,2));


