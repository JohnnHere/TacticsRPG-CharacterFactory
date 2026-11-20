import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const root=process.cwd();
const dirs=['front_r','front_l','back_r','back_l'];
const speedRows={
 front_r:{1:[4.7,62.7,171.7,297.1,407.1],0.75:[0.4,78.5,204.6,361.9,502.7],0.5:[0.4,107.8,310.9,557.5,759.5]},
 front_l:{1:[0.9,61.4,166.7,290.3,399.8],0.75:[0.7,79.1,218.8,370.9,515.5],0.5:[0.5,148.9,311,542,744.2]},
 back_r:{1:[1,60.1,170,293.6,402.1],0.75:[0.7,78.8,210.4,371.7,510.7],0.5:[0.4,109,312.2,545.3,740.3]},
 back_l:{1:[0.6,62.9,169.7,296.7,405.2],0.75:[0.6,78.3,219.7,370.8,512.1],0.5:[0.5,110.6,316,546.5,747.5]}
};
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(path.join(root,p))).digest('hex');
const clips=dirs.map(direction=>{
 const p=`characters/orc-v1/source/complete-v1/${direction}/Hit/clip.json`;
 const clip=JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
 return {direction,clipJson:p,clipJsonSha256:sha(p),frameCount:clip.frameCount,durationsMs:clip.durationsMs,totalDurationMs:clip.totalDurationMs,master:clip.master,masterSha256:clip.masterSha256,nativePngs:clip.frames.map(f=>({path:f.nativePng,sha256:sha(f.nativePng)}))};
});
const result={schemaVersion:1,createdAtUtc:'2026-10-26T18:45:40Z',status:'TECHNICALLY_COMPLETE',scope:'Unchanged production complete-v1 Hit aliases; no art edits performed',viewer:{path:'experiments/main-orc-rear-recovery-v2/hit-playback-review.html',browserId:'55ccb687-96e4-414f-99a7-d8ffe9afa172',source:'actual nativePng paths from each clip.json',displayScales:{'1x':'128px native pixels','0.75x':'64px tactical display','0.5x':'64px tactical display','zoom':'512px QA-only; not used for gameplay readability claim'}},nominal:{frameDurationsMs:[45,95,115,95,100],totalMs:450,expectedElapsedMsBySpeed:{'1x':450,'0.75x':600,'0.5x':900}},browserObservedFrameStartsMs:speedRows,qualitative:{at1x128px:'All four directions retain readable recoil, bracing, and return-to-guard sequence at native sprite scale. Front views show upper-body/head recoil into a braced crouch, followed by rise and reset. Rear views show shoulder/torso recoil with raised arms, then settle and reset.',at075x64px:'The same phase order remains clear at tactical scale; impact-to-brace is easier to parse than frame details.',at05x64px:'Slow playback separates the 95ms recoil, 115ms brace, and recovery phases; it is diagnostic and not a gameplay-speed claim.',zoom512px:'Inspection-only view; it reveals pixel clusters but is not used as evidence of in-game readability.',limits:'Browser setTimeout sampling was 0–~65ms late versus the first nominal transition and accumulated modest overhead. Reported clip timing remains the production metadata; browser measurements confirm order and practical playback, not engine-clock calibration.',decision:'Preserve current protected Hit sources. No verified visual defect justified editing them. Actual Unity feel and damage-window calibration remain deferred.'},clips};
fs.writeFileSync(path.join(root,'experiments/main-orc-rear-recovery-v2/hit-playback-assessment.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:result.status,clips:clips.length,frames:clips.reduce((n,c)=>n+c.frameCount,0),totals:clips.map(c=>[c.direction,c.totalDurationMs,c.durationsMs])}));
