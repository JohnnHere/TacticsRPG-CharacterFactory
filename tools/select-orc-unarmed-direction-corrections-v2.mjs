import fs from 'node:fs';import path from 'node:path';import {ROOT,readJSON,json,hash} from '../src/core.mjs';
const read=f=>readJSON(path.join(ROOT,f)),stamp=f=>hash(fs.readFileSync(path.join(ROOT,f))),file='characters/orc-unarmed-directions-batch-v1.json',bs=read(file);
for(const b of bs){
 const needs=b.direction==='back_l'||b.id==='orc-01-rogue'&&b.direction==='front_l';if(!needs)continue;
 const folder=b.folder.replace('action-clips-v1','action-clips-v2'),gfile=folder+'/generation.json';if(!fs.existsSync(path.join(ROOT,gfile)))throw Error('Actual corrected source missing');
 const g=read(gfile);for(const r of g.references)r.sha256=stamp(r.file);g.sourceSha256=stamp(folder+'/'+g.source);g.promptSha256=stamp(folder+'/'+g.promptFile);g.baseApprovalDigest=b.baseApprovalDigest;json(path.join(ROOT,gfile),g);
 const old=read(b.folder+'/generation.json');old.status=b.direction==='back_l'?'NOT_SELECTED_NEAR_LEFT_JAB_INSTEAD_OF_RIGHT_PUNCH':'NOT_SELECTED_ROGUE_HOOD_LOWERED';json(path.join(ROOT,b.folder,'generation.json'),old);
 const oldManifest=`characters/${b.id}/actions/basic-unarmed/${b.supplementVersion}/${b.direction}/clip-manifest.json`;if(fs.existsSync(path.join(ROOT,oldManifest))){const m=read(oldManifest);if(m.artisticReview?.startsWith('APPROVED_'))throw Error('Approved action cannot be replaced');m.status='NOT_SELECTED_CORRECTED_SOURCE_AVAILABLE';json(path.join(ROOT,oldManifest),m);}
 b.folder=folder;b.supplementVersion='v2';b.prompt=fs.readFileSync(path.join(ROOT,folder,g.promptFile),'utf8').trimEnd();b.references=g.references;json(path.join(ROOT,folder,'handoff.json'),{...b,contract:'config/equipment-actions-v1.json',purpose:'Corrected anatomical right punch or raised hood'});
}
json(path.join(ROOT,file),bs);console.log('Six corrected occluded right punches and Rogue raised hood selected; original attempts preserved.');
