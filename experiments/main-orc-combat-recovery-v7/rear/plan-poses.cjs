const fs = require('fs');
const root='experiments/main-orc-combat-recovery-v7/rear/';
const old=JSON.parse(fs.readFileSync('experiments/main-orc-artistic-reconstruction-v6/rear/sword-reference2-request.json','utf8'));
const base=old.first_frame_keypoints;
const specs={
 sword:[[.66,.32,.69,.45,.70,.59,0],[.67,.31,.71,.39,.72,.48,0],[.68,.30,.73,.32,.72,.33,.01],[.68,.29,.72,.25,.67,.18,.02],[.67,.28,.70,.21,.61,.12,.02],[.66,.28,.69,.20,.60,.11,.02],[.64,.30,.64,.24,.55,.20,-.01],[.62,.32,.59,.34,.50,.39,-.02],[.61,.33,.57,.40,.48,.52,-.02],[.63,.33,.60,.43,.52,.57,-.01],[.65,.32,.66,.45,.65,.58,0],[.66,.32,.69,.45,.70,.59,0]],
 axe:[[.66,.32,.69,.45,.70,.59,0],[.67,.31,.71,.39,.72,.48,0],[.68,.30,.73,.31,.72,.31,.01],[.68,.29,.72,.25,.67,.17,.02],[.67,.28,.71,.20,.61,.10,.02],[.64,.30,.65,.24,.55,.21,-.01],[.61,.33,.59,.39,.49,.51,-.02],[.61,.34,.57,.42,.48,.56,-.02],[.62,.33,.59,.42,.51,.56,-.01],[.64,.32,.63,.43,.60,.55,0],[.65,.32,.67,.45,.66,.58,0],[.66,.32,.69,.45,.70,.59,0]]};
for(const [name, poses] of Object.entries(specs)){
 const keypoints=poses.map(([sx,sy,ex,ey,wx,wy,shift])=>base.map(j=>{let k={...j}; if(['NOSE','NECK','RIGHT EYE','LEFT EYE','RIGHT EAR','LEFT EAR','LEFT SHOULDER','LEFT ELBOW','LEFT ARM'].includes(k.label)) k.x+=shift; if(k.label==='RIGHT SHOULDER'){k.x=sx;k.y=sy;k.depth=150} if(k.label==='RIGHT ELBOW'){k.x=ex;k.y=ey;k.depth=180} if(k.label==='RIGHT ARM'){k.x=wx;k.y=wy;k.depth=185} return k;}));
 let req={description:'Adult muscular green orc seen from behind in three quarter view, bald green occipital skull, dark steel spiked shoulder plates and articulated bracers, chain mail sleeves, broad dark back plate, red cloth tassets, dark greaves and grounded boots. Both hands empty, right hand a visible closed leather glove. Same individual, entire body, refined pixel clusters and dark outlines.',action:name==='sword'?'raise right fist above head, rotate shoulder and trunk, drive fist diagonally down across the front, recover':'load right fist above shoulder, rotate trunk, drive fist downward, settle and recover',direction:'north-west',first_frame_base64:old.first_frame_base64,first_frame_keypoints:base,keypoints,view:'low top-down',no_background:true,seed:name==='sword'?71031:71032};
 fs.writeFileSync(root+name+'-request.json',JSON.stringify(req,null,2));
}
