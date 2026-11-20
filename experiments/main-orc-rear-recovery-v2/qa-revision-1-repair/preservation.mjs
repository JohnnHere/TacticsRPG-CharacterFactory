import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {PNG} from 'pngjs';
const E='experiments/main-orc-rear-recovery-v2',O=`${E}/qa-revision-1-repair`,B=`${E}/E/rejected/qa-revision-1-before`;
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const inv=JSON.parse(fs.readFileSync(`${B}/backup-inventory.json`));
const result={status:'PASS',backupFiles:inv.files.length,backupHashMismatches:[],targetPackageComparisons:[],failures:[]};
for(const r of inv.files)if(sha(path.resolve(B,r.backup))!==r.sha256)result.backupHashMismatches.push(r.backup);
const old=p=>{const row=inv.files.find(r=>r.source===p);if(!row)throw Error(`Missing verified old source ${p}`);return path.resolve(B,row.backup)};
const bytes=im=>im.data;
for(const [d,a]of [['back_l','Sword'],['back_r','Axe'],['back_l','Axe']]){
 const root=`characters/orc-v1/source/rear-recovery-v2/${d}/${a}/Attack-representative-v1`;
 const rows=[];
 for(let i=0;i<8;i++){
  const n=String(i).padStart(2,'0'),layers={};
  for(const l of ['weaponBack','body','weaponFront','handFront']){
   const p=`${root}/layers/${l}/${n}.png`,b=PNG.sync.read(fs.readFileSync(old(p))),v=PNG.sync.read(fs.readFileSync(p));let changed=0;
   for(let j=0;j<v.data.length;j+=4)if(!v.data.subarray(j,j+4).equals(b.data.subarray(j,j+4)))changed++;
   layers[l]={changedRgbaPixels:changed,byteIdentical:sha(p)===sha(old(p))};
  }
  rows.push({index:i,layers});
 }
 result.targetPackageComparisons.push({cell:`${d}/${a}`,frames:rows});
}
// Same 27 exact locations from the successful prior repair, shifted only by
// source-frame numbering (old raw02 -> canonical F03), remain transparent.
const coords=[[18,22],[18,23],[18,24],[19,24],[19,25],[20,25],[19,26],[20,26],[20,27],[21,27],[20,28],[21,28],[22,28],[21,29],[22,29],[21,30],[22,30],[23,30],[22,31],[23,31],[24,31],[24,32],[25,32],[25,33],[26,33],[26,34],[28,35]];
const p='characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/layers/body/03.png',im=PNG.sync.read(fs.readFileSync(p));
result.axeL27PriorCleanup=coords.map(([x,y])=>({native:[x,y],alpha:im.data[((y+64)*256+x+64)*4+3]}));
if(result.axeL27PriorCleanup.some(x=>x.alpha))result.failures.push('AxeL prior27 cleanup changed');
result.axeLRaisedFist=[];
for(const i of [2,3]){
 const p=`characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/layers/body/${String(i).padStart(2,'0')}.png`;
 const b=PNG.sync.read(fs.readFileSync(old(p))),v=PNG.sync.read(fs.readFileSync(p));let changed=0;
 for(let y=64;y<110;y++)for(let x=72;x<116;x++){const j=(y*256+x)*4;if(!b.data.subarray(j,j+4).equals(v.data.subarray(j,j+4)))changed++}
 result.axeLRaisedFist.push({frame:i,nativeROI:[8,0,51,45],changedPixels:changed});if(changed)result.failures.push(`AxeL F${i} raised-fist ROI changed`);
}
const freeze=JSON.parse(fs.readFileSync(`${E}/qa-history/6fa4653eabe660992acc422aa32159b48e4971122df0e995b99a19261df4a843/delivery-freeze.json`));
const weaponFiles=Object.entries(freeze.files).filter(([p])=>/^assets\/weapons\/(militia-axe|recruit-sword)\//.test(p));
result.independentWeapons={checkedFiles:weaponFiles.length,changed:weaponFiles.filter(([p,h])=>sha(p)!==h).map(([p])=>p)};
if(result.backupHashMismatches.length||result.independentWeapons.changed.length)result.failures.push('Backup or weapon preservation mismatch');
result.status=result.failures.length?'FAIL':'PASS';
fs.writeFileSync(`${O}/preservation.json`,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:result.status,backupFiles:result.backupFiles,independentWeapons:result.independentWeapons,prior27Preserved:!result.axeL27PriorCleanup.some(x=>x.alpha),raisedFist:result.axeLRaisedFist,failures:result.failures},null,2));if(result.failures.length)process.exitCode=1;
