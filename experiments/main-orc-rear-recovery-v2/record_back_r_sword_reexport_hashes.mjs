import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {ROOT} from '../../src/core.mjs';

const clipPath='characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json';
const absolute=path.join(ROOT,clipPath);const clip=JSON.parse(fs.readFileSync(absolute,'utf8'));
const changed=[];
for(const frame of clip.frames){
 const layer=frame.layers.body;const actual=crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT,layer.png))).digest('hex');
 if(layer.sha256!==actual){changed.push({frame:frame.index,oldSha256:layer.sha256,newSha256:actual});layer.sha256=actual;}
}
if(changed.length){fs.writeFileSync(absolute,JSON.stringify(clip,null,2)+'\n');}
console.log(JSON.stringify({clipPath,updatedLayerHashCount:changed.length,changed},null,2));
