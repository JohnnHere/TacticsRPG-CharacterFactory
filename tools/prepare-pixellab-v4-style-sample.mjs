// Create a 128x128, Aseprite-resized working copy of V4 for PixelLab style input.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {ROOT,slash,json} from '../src/core.mjs';
import {decode,measure} from '../src/images.mjs';
import {findAseprite,executeAseprite} from '../src/aseprite.mjs';

const sourceRel='characters/orc-01-aseprite-v4/source/aseprite/retouched/concept/concept_front_r_00.png';
const source=path.join(ROOT,sourceRel);
const outputDir=path.join(ROOT,'characters/orc-pixellab-07/source/pixellab-results/Style');
const image=path.join(outputDir,'v4-style-128.png');
const master=path.join(outputDir,'v4-style-128.aseprite');
const record=path.join(outputDir,'reference-record.json');
for(const p of [image,master,record])if(fs.existsSync(p))throw new Error(`Preserving existing style sample: ${slash(path.relative(ROOT,p))}`);
fs.mkdirSync(outputDir,{recursive:true});
const sourceDecoded=decode(source),scale=128/sourceDecoded.image.width;
if(sourceDecoded.image.width!==sourceDecoded.image.height)throw new Error('V4 style reference must be square.');
executeAseprite(findAseprite(),[source,'--scale',String(scale),'--save-as',image]);
const resized=decode(image),m=measure(resized.image);
if(resized.image.width!==128||resized.image.height!==128)throw new Error(`Aseprite produced unexpected style sample dimensions ${m.width}x${m.height}`);
executeAseprite(findAseprite(),[image,'--save-as',master]);
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
json(record,{purpose:'PixelLab style-conditioning sample only; not a character asset or production sprite',source:sourceRel,sourceSha256:sha(source),derivedImage:'v4-style-128.png',derivedImageSha256:sha(image),asepriteMaster:'v4-style-128.aseprite',asepriteMasterSha256:sha(master),method:'Aseprite CLI --scale nearest-neighbor; 1254x1254 -> 128x128',canvas:{width:128,height:128},measurements:m,pixelCopyIntoGeneratedCandidate:false});
console.log(JSON.stringify({image:slash(path.relative(ROOT,image)),master:slash(path.relative(ROOT,master)),record:slash(path.relative(ROOT,record)),scale,measurements:m},null,2));
