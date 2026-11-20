import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {PNG} from 'pngjs';
const E='experiments/main-orc-hybrid-weapon-04';
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const json=(p,v)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,JSON.stringify(v,null,2)+'\n')};
const clip=JSON.parse(fs.readFileSync('characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_l-sword/clip.json'));
const walk=p=>fs.readdirSync(p,{withFileTypes:true}).flatMap(d=>d.isDirectory()?walk(path.join(p,d.name)):[path.join(p,d.name)]);
const stage=process.argv[2]??'representative';
if(stage==='representative')json(E+'/protected-before.json',Object.fromEntries(['characters','assets','reports'].flatMap(walk).map(p=>[p,hash(p)])));
if(stage==='representative'||stage==='full'){
 const r=spawnSync('F:/SteamLibrary/steamapps/common/Aseprite/Aseprite.exe',['--batch','--noinapp','--script-param',`stage=${stage}`,'--script',E+'/author.lua'],{windowsHide:true,encoding:'utf8',timeout:120000,env:{...process.env,ASEPRITE_USER_FOLDER:path.resolve(E,'batch-profile')}});
 fs.writeFileSync(E+`/${stage}-aseprite.log`,r.stdout+'\n'+r.stderr);if(r.status!==0)throw Error(JSON.stringify(r));console.log(r.stdout);
}
if(stage==='verify'){
 const png=p=>PNG.sync.read(fs.readFileSync(p));const rows=[];
 for(const f of clip.frames)for(const n of ['body','handFront']){
  const fn=`F${String(f.index).padStart(2,'0')}.png`;const src=f.layers[n].png;
  const a=`${E}/full/a/layers/${n}/${fn}`,b=`${E}/full/b/layers/${n}/${fn}`;
  rows.push({frame:f.index,layer:n,sourceSha256:hash(src),aSha256:hash(a),bSha256:hash(b),byteIdenticalAB:hash(a)===hash(b),byteIdenticalSource:hash(src)===hash(a),rgbaIdentical:png(src).data.equals(png(a).data)&&png(a).data.equals(png(b).data)});
 }
 const before=JSON.parse(fs.readFileSync(E+'/protected-before.json'));const changed=Object.keys(before).filter(p=>!fs.existsSync(p)||hash(p)!==before[p]);const added=['characters','assets','reports'].flatMap(walk).filter(p=>!(p in before));
 json(E+'/pixel-diff.json',{status:rows.every(r=>r.byteIdenticalSource&&r.byteIdenticalAB)&&!changed.length&&!added.length?'PASS':'FAIL',comparisons:rows,protectedFiles:Object.keys(before).length,protectedChanged:changed,protectedAdded:added});
 for(const v of ['a','b'])json(`${E}/variants/sword-${v}/provenance.json`,{source:clip.weapon,authoring:v==='a'?'Byte-preserved copy of existing saved master; freshly exported in Aseprite':'Programmatic Lua blade authorship in Aseprite; inherited hilt y>=55 byte-preserved; hidden original layers retained',script:E+'/author.lua',scriptSha256:hash(E+'/author.lua'),masterSha256:hash(`${E}/variants/sword-${v}/sword.aseprite`),pngSha256:hash(`${E}/variants/sword-${v}/sword.png`),canvas:[96,96],grip:[48,66],newPixelLabCalls:0});
 json(E+'/grip-profile.json',{schemaVersion:1,family:'Sword/basic.sword-slash',animationSource:'characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_l-sword/clip.json',sourceSha256:hash('characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_l-sword/clip.json'),hand:'anatomical right hand; original body glove + original handFront per frame',canvas:[96,96],contact:[48,66],pivot:[48,66],scale:1,layerOrder:clip.layerOrder,occlusion:{weaponBack:'Original per-frame mask, leather grip v60..70 behind body',weaponFront:'Original guard/pommel and blade; B replaces blade v<=54 only',handFront:'Original traced glove, unchanged, overlays front weapon; no new overlay'},visibleInterval:clip.visibleInterval,contactEvent:clip.contactEvent,durationsMs:clip.durationsMs,totalDurationMs:730,frames:clip.frames.map(f=>({index:f.index,visible:f.weaponVisible,grip:f.grip,rotationDeg:f.rotationDeg,unwrappedAngleDeg:f.unwrappedAngleDeg,specialTransform:f.index===6?'F05 inverse nearest lookup then -16 degrees around target (128,101), source (157,89); see author.lua':null}))});
 const a=png(E+'/variants/sword-a/sword.png'),b=png(E+'/variants/sword-b/sword.png');let silhouette=0,hilt=0;for(let y=0;y<96;y++)for(let x=0;x<96;x++){let i=(y*96+x)*4;if(!!a.data[i+3]!==!!b.data[i+3])silhouette++;if(y>=55&&!a.data.subarray(i,i+4).equals(b.data.subarray(i,i+4)))hilt++;}
 json(E+'/weapon-diff.json',{silhouetteChangedPixels:silhouette,hiltChangedPixels:hilt,lengthA:48,lengthB:48,lengthChangePercent:0});console.log({comparisons:rows.length,allByteIdentical:rows.every(r=>r.byteIdenticalSource&&r.byteIdenticalAB),silhouette,hilt,protectedChanged:changed.length});
}
