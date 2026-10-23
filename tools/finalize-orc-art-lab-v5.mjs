// Read-only integrity and delivery checks; no artistic transformation.
import fs from 'node:fs';
import path from 'node:path';
import {ROOT,hash} from '../src/core.mjs';
import {verifyEditorBuild} from '../src/aseprite.mjs';
const read=p=>JSON.parse(fs.readFileSync(path.join(ROOT,p),'utf8'));
const report=read('reports/orc-art-lab-v5.json');
for(const f of report.protectedFiles)if(hash(fs.readFileSync(path.join(ROOT,f.file)))!==f.sha256)throw Error('Protected file changed: '+f.file);
verifyEditorBuild(report.build.path);
if(read('characters/orc-01-art-lab-v5/reviews.json').length)throw Error('Unexpected creator review');
const sources=read('reports/orc-art-lab-v5-source-check.json'),preview=read('reports/orc-art-lab-v5-preview-check.json');
if(sources.status!=='PASS'||preview.status!=='PASS')throw Error('Delivery checks incomplete');
const local='docs/ORC_ART_LAB.md',main='../TacticsRPG/Docs/Art/ORC_ART_LAB.md';
if(!fs.readFileSync(path.join(ROOT,local)).equals(fs.readFileSync(path.join(ROOT,main))))throw Error('Direction documents diverged');
const htmlPath='reports/orc-art-lab-v5/review.html',html=fs.readFileSync(path.join(ROOT,htmlPath),'utf8');let links=0;
for(const m of html.matchAll(/(?:href|src)="([^"]+)"/g)){
 if(/^(?:https?:|#|data:)/.test(m[1]))continue;
 if(!fs.existsSync(path.resolve(ROOT,path.dirname(htmlPath),m[1])))throw Error('Missing review link: '+m[1]);links++;
}
const result={status:'DELIVERED_FOR_CREATOR_SELECTION',date:'2026-10-23',concepts:5,masters:5,conceptDimensions:[1254,1254],savedMasterAndPngChecks:sources.status,preview:preview.status,reviewLinksChecked:links,protectedFilesUnchanged:report.protectedProductionFiles,productionRevision:read('reports/orc-production-current.json').revision,creatorReviews:0,selection:null,documentationMirrored:true,sourceAuthorship:'Aseprite Lua over inherited approved V4 anatomy/pose; original V2 image_gen ancestry preserved.',next:'Creator selects one direction or combination, then refine concept in Aseprite.',review:htmlPath,overview:'reports/orc-art-lab-v5/five-options.png'};
fs.writeFileSync(path.join(ROOT,'reports/orc-art-lab-v5-final.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
