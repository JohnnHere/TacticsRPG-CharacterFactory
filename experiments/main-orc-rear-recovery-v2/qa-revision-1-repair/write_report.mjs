import fs from 'node:fs';
import crypto from 'node:crypto';
const E='experiments/main-orc-rear-recovery-v2',O=`${E}/qa-revision-1-repair`;
const read=p=>JSON.parse(fs.readFileSync(p));
const write=(p,x)=>fs.writeFileSync(p,JSON.stringify(x,null,2)+'\n');
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const mpath='characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json',m=read(mpath);
const summaries={
 'back_l/Sword':'QA-01 repaired locally in Aseprite: same-view non-striking gauntlet restored F01..07, F04 pale far-shoulder triangle and F05 attacking-shoulder blade removed; original bent elbow chain retained. Root accepted body checkpoint only for composition. Fresh source proof and local1/.75/.5 playback passed; new independent review remains pending, PENDING_CREATOR.',
 'back_r/Axe':'QA-02/QA-03 repaired locally in Aseprite: duplicate body equipment removed F01..03; F04/F05 old distal arm erased before a single connected own same-view donor limb was placed. Compact independent axe aligned to actual reconstructed glove in F01/F04/F05. Local source/playback checks passed; new independent review pending, PENDING_CREATOR.',
 'back_l/Axe':'QA-04 repaired locally in Aseprite: far-shoulder tip/strand restored in F02/F03. Exact origin remains unproven. Raised-fist donor pixels and earlier27 transparent cleanup coordinates preserved. Local source/playback checks passed; new independent review pending, PENDING_CREATOR.'
};
for(const c of m.cells)if(summaries[c.cellId]){
 c.qaRevision1.previousRejectedNotes=c.notes.split(' QA revision 1 authored locally')[0];
 c.qaRevision1.originalProvenance=c.provenance;
 c.notes=summaries[c.cellId];
 c.provenance=`QA revision1 Aseprite source repair; ${O}/provenance.json. Prior independent rejection retained in qa-argon-final.md; new independent re-review pending.`;
}
write(mpath,m);
const p=read(`${O}/provenance.json`),cp=read(`${O}/checkpoint/checkpoint.json`),proof=read(`${O}/source-proof.json`),play=read(`${O}/playback-verification.json`),pres=read(`${O}/preservation.json`),val=read(`${O}/manifest-validation.json`);
const checks={createdAtUtc:new Date().toISOString(),status:'PASS',checks:[
 {command:'node experiments/main-orc-rear-recovery-v2/qa-revision-1-repair/verify_saved_sources.mjs',exitCode:0,sets:21,freshExactFrameComparisons:168,evidence:`${O}/source-proof.json`},
 {command:'node experiments/main-orc-rear-recovery-v2/qa-revision-1-repair/playback.mjs',exitCode:0,actualRAFRuns:9,all8FramesObserved:9,loopBoundariesObserved:9,errors:0,evidence:`${O}/playback-verification.json`},
 {command:'node experiments/main-orc-rear-recovery-v2/verify_new_representatives.mjs --check',exitCode:0,clips:4,failures:0,readOnly:true},
 {command:'node experiments/main-orc-rear-recovery-v2/validate_candidate_manifest.mjs --output experiments/main-orc-rear-recovery-v2/qa-revision-1-repair/manifest-validation.json',exitCode:0,checksPassed:338,failed:0,evidence:`${O}/manifest-validation.json`},
 {command:'node --test experiments/main-orc-rear-recovery-v2/validate_candidate_manifest.test.mjs',exitCode:0,tests:14,passed:14,failed:0,newTestsAuthored:0},
 {command:'node experiments/main-orc-rear-recovery-v2/root-check-qa-regressions.mjs',exitCode:0,filesChecked:1911,changed:0,referenceFreeze:'6fa4653eabe660992acc422aa32159b48e4971122df0e995b99a19261df4a843'},
 {command:'node experiments/main-orc-rear-recovery-v2/qa-revision-1-repair/preservation.mjs',exitCode:0,backupFilesVerified:197,independentWeaponFilesUnchanged:14,axeLRaisedFistChangedPixels:0,prior27PixelsTransparent:true,evidence:`${O}/preservation.json`},
 {command:'node experiments/main-orc-rear-recovery-v2/verify_front_f02_and_protected_frames.mjs',exitCode:0,views:2,frames:10,baselineFramesPreserved:8,changedF02Frames:2,readOnly:true},
 {command:'node experiments/main-orc-rear-recovery-v2/verify_four_early_clip_source_metadata.mjs',exitCode:0,clips:4,nativeFrames:20,readOnly:true}
]};
write(`${O}/checks.json`,checks);
const rows=p.cells.map(c=>`| ${c.cell} | ${c.changedBodyPixels.filter(f=>f.changedPixels).map(f=>'F'+String(f.index).padStart(2,'0')+': '+f.changedPixels).join('; ')} | ${c.changedBodyPixels.reduce((s,f)=>s+f.changedPixels,0)} |`).join('\n');
const sources=p.cells.map(c=>`- **${c.cell}**: composite \`${c.master}\`; body \`${c.bodyMaster}\`; native \`${c.nativeMaster}\`. Updated SHA-256 values: [provenance.json](qa-revision-1-repair/provenance.json).`).join('\n');
const layers=pres.targetPackageComparisons.map(c=>({cell:c.cell,weaponChanged:c.frames.filter(f=>f.layers.weaponBack.changedRgbaPixels||f.layers.weaponFront.changedRgbaPixels).map(f=>f.index),handChanged:c.frames.filter(f=>f.layers.handFront.changedRgbaPixels).map(f=>f.index)}));
p.validation=`${O}/checks.json`;p.finalManifest={path:mpath,sha256:sha(mpath),active:12,aliases:16,inRevision:0};
p.finalLayerChanges=layers;p.report=`${E}/qa-revision-1-art-escalation-report.md`;write(`${O}/provenance.json`,p);
const report=`# Sole ART replacement — scoped QA revision 1

**TECHNICALLY_COMPLETE. VISUAL_REVIEW_REQUIRED. PENDING_CREATOR.** Three local packages repaired and returned to Root for build/new freeze and the **same Copilot08686c14 independent reviewer**. This is ART source work and local verification, not independent QA or creator approval. No pending user input or permission is needed; ART returns idle after this report.

## Checkpoint and ownership

Actual body-only checkpoint: [index.html](qa-revision-1-repair/checkpoint/index.html), [SwordL](qa-revision-1-repair/checkpoint/SwordL-wholebody.png), [AxeR](qa-revision-1-repair/checkpoint/AxeR-wholebody.png), [AxeL](qa-revision-1-repair/checkpoint/AxeL-wholebody.png). Each is derived from a saved master reopened in Aseprite. Root inspected and explicitly accepted this checkpoint **for local weapon composition only** in the session. Acceptance is recorded in [checkpoint.json](qa-revision-1-repair/checkpoint/checkpoint.json).

Only SwordL, AxeR, AxeL sources/packages, their metadata, and the three canonical manifest cells were changed. Root retains integration/build/freeze ownership; knowledge2046 retains docs/config/recipes ownership. The prior rejected Luna partial remains untouched at [E/qa-revision-1-art-report.md](E/qa-revision-1-art-report.md). Earlier unsuccessful staged masks were not used as evidence of a repair.

## Actual authored repairs

- **QA-01 / SwordL:** Removed the baked equipment at the non-striking image-right hand/hip in F01..F07. Restored a silhouette-shaped own back_l static gauntlet and lower arm, including transparency where the extra blade extended beyond the hand. F04 pale triangle behind the far pauldron was removed. F05 blade/hilt across the image-left attacking shoulder was traced and removed; the upper pauldron rim reuses its own F04 pixels at native translation (+6,-3), retaining the original bent elbow/forearm chain. Six individually inspected detached source pixels were cleared. F07 is unarmed in the BODY and in the full composite.
- **QA-02 / AxeR:** Removed the actual F01 curved head/old distal silhouette and used the accepted own back_r SwordR F01 reach/closed glove to build one connected preparation limb. Source shaft pixels above F02/F03 were removed; the last F03 stub was replaced with a small rounded knuckle cap authored inside Aseprite. All poses were inspected as whole body with weapon layers off.
- **QA-03 / AxeR:** The complete obsolete distal arm was cleared to transparency first. A static base is inappropriate here because its hanging arm reintroduces a second limb. The accepted same-view SwordR F05 upper arm/elbow/forearm and real handFront glove pixels were reused at (0,-3) for F04 and (0,+1) for F05. The saved BODY now contains the whole closed glove and one continuous chain. No separate hand layer conceals a broken connection. The independent militia axe was rerendered to the actual glove for F01/F04/F05; the original compact item and rotations were retained.
- **QA-04 / AxeL:** Restored only the far-pauldron protruding tip/strand contour in F02/F03 using own back_l static armor pixels. This includes the farther source pixels missed by earlier masks. The origin of the strand is still unproven. The existing raised-fist donor pixels, torso, legs and earlier exact27-pixel cleanup were preserved.

All actual raster changes were authored by recorded Lua **inside Aseprite1.3.18.6**, hidden isolated-profile --batch --noinapp. Python created QA layouts/crops only; it did not edit production pixels. Coordinates in [author_body.lua](qa-revision-1-repair/author_body.lua) are native128 with explicit (+64,+64) registration into composite256. [compose.lua](qa-revision-1-repair/compose.lua) saved and reopened the canonical masters before exporting. No generation calls, Unity operations, commits, new agents, or selection promotion occurred. Accounting remains **78 units /17 jobs**; no balance/token/dollar estimate was made.

## Frame and pixel evidence

Counts below are exact changed RGBA pixel positions in BODY versus the independently rejected before-state; they are not a claim of all-new art. Per-frame bounding boxes, before/after hashes and source master hashes are in checkpoint.json/provenance.json. The complete polygons, translations and individually authored pixels are in the Lua source.

| Cell | Edited body frames: changed pixel positions | Total |
|---|---|---:|
${rows}

Native F00 is unchanged in all three clips. AxeR F06/F07 and AxeL F00/F01/F04..F07 remain pixel-identical in BODY. Independent weapon layers are pixel-identical in **all SwordL/AxeL frames** and AxeR F00/F02/F03/F06/F07; only AxeR F01/F04/F05 weapon transforms changed. Finger occlusion is restricted to actual repaired body glove pixels. Exact per-layer deltas and byte identities are in [preservation.json](qa-revision-1-repair/preservation.json).

## Sources, exports and grips

${sources}

All three retain **8 frames**, **[90,80,90,80,100,80,100,110]ms =730ms**, four independently selectable layers **weaponBack/body/weaponFront/handFront**, 256 composite and128 body native masters. Weapon layers are empty outside F01..F06. Native PNGs remain exact center crops of BODY, consistent with the existing contract; the full composed256 exports contain the weapons.

AxeR actual composite glove grips are F01(175,106), F02(167,73), F03(167,78), F04(181,118), F05(181,122), F06(156,139). The changed F04/F05 grips correspond to the reused closed glove, not an opaque forearm/pauldron. SwordL/AxeL grip positions and independent weapon transforms were preserved. Source weapon hashes and donor hashes are recorded in [provenance.json](qa-revision-1-repair/provenance.json).

Full composite sheets: [SwordL](qa-revision-1-repair/final/SwordL-composite-wholebody.png), [AxeR](qa-revision-1-repair/final/AxeR-composite-wholebody.png), [AxeL](qa-revision-1-repair/final/AxeL-composite-wholebody.png). Each tile includes the entire256 canvas, including the axe head at its furthest extension. Actual glove/handle comparisons: [SwordL grips](qa-revision-1-repair/final/SwordL-grips.png), [AxeR grips](qa-revision-1-repair/final/AxeR-grips.png), [AxeL grips](qa-revision-1-repair/final/AxeL-grips.png).

## Local motion inspection

[review.html](qa-revision-1-repair/review.html) plays the actual canonical saved-source exports. Fresh headless Chromium RAF runs covered all8 frames at **1×,0.75×,0.5×**, with all9 runs crossing F07→F00. Full256, native128 BODY, and full-composite half-scale (body approximately64px) were shown. Direct inspection of the complete actual-transition filmstrips found one connected AxeR limb during commit/impact, fist-following compact weapon transforms, and unarmed endpoints. SwordL's bent elbow remains connected after the shoulder cleanup; AxeL's repaired raised fist remains visible and its shoulder strand no longer pops.

Actual ordered temporal samples: [SwordL all speeds](qa-revision-1-repair/playback/SwordL-all-speeds.png), [AxeR all speeds](qa-revision-1-repair/playback/AxeR-all-speeds.png), [AxeL all speeds](qa-revision-1-repair/playback/AxeL-all-speeds.png). Full individual screenshots and transition times are in playback/ and [playback-verification.json](qa-revision-1-repair/playback-verification.json). This was actual RAF playback inspected through complete captured temporal samples, **not a continuous video/live-GUI inspection or independent artistic verdict**. Review looping does not change oneShot runtime metadata. GIFs at1/.75/.5 were freshly exported in Aseprite; GIF delay quantization gives730/980/1460ms while RAF uses the exact speed multiplier.

## Verification and preservation

- **168/168 fresh source frame comparisons:**21 export sets from the9 saved sources (composite/body/native plus every independent layer), exact decoded RGBA and durations. Production read-only. [source-proof.json](qa-revision-1-repair/source-proof.json).
- **338 contract checks passed**, zero failures in FINAL mode;12 ACTIVE_CANDIDATE/16 UNCHANGED_ALIAS/0 revision. No validator or test code was changed. [manifest-validation.json](qa-revision-1-repair/manifest-validation.json).
- **14/14 existing contract tests passed**, including negative SHA/missing-source fixtures. No new test suite was authored. The existing suite regenerated its normal manifest-validation-report.json artifact; the scoped FINAL result above is retained independently.
- **verify_new_representatives.mjs --check passed**, including four-layer recomposition, native crop consistency, independent item hashes, frame/timing and three GIF speeds.
- **1,911 protected production/source/weapon/baseline files unchanged** against rejected freeze6fa4653e... via root-check-qa-regressions.mjs. This preserves the successful9 candidate clips and16 aliases. All25 non-target manifest cells remain unchanged.
- The byte backup in E/rejected/qa-revision-1-before/ still has **197/197 matching inventory entries**, including source records/scripts. Root's separately verified192-file rejected-freeze manifest remains preserved at rejected/qa-revision-1-before/backup-manifest.json. These are separate inventories, not conflicting file counts.
- **14 independent weapon files unchanged**. AxeL raised-fist ROIs F02/F03 have **zero changed pixels**; all27 earlier cleanup coordinates remain transparent. Front F02 preservation checker and four early-source/native metadata checker also passed.

Commands, exit codes and counts: [checks.json](qa-revision-1-repair/checks.json). No existing production/source validator was weakened. No root review builder was run or edited; the integrated library copies still require Root's rebuild.

## Handoff state

Canonical [candidate28manifest.json](../../characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json) now has12 ACTIVE_CANDIDATE and16 UNCHANGED_ALIAS. The repaired three have reviewStatus **VISUAL_REVIEW_REQUIRED**, retain original rejection evidence/IDs, and explicitly await a new freeze for the same independent Copilot reviewer. The historic qa-argon-final.md/qa-result.json verdict is untouched and applies to the rejected freeze, not to this new local repair.

**TECHNICALLY_COMPLETE / VISUAL_REVIEW_REQUIRED / PENDING_CREATOR.** Root can rebuild the review/library, freeze this revision and request the same reviewer's independent re-review. No internal check closes QA-01..04 on behalf of that reviewer, and CREATOR_APPROVED has not been granted. ART returns idle; no task blocker or unanswered permission remains.
`;
fs.writeFileSync(`${E}/qa-revision-1-art-escalation-report.md`,report);
write(`${O}/handoff.json`,{status:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',creatorApproval:'PENDING_CREATOR',artState:'RETURNING_IDLE',pendingUserInput:false,report:`${E}/qa-revision-1-art-escalation-report.md`,checkpoint:`${O}/checkpoint/index.html`,review:`${O}/review.html`,nextOwner:'Root',nextAction:'Rebuild review/library; new freeze; same independent Copilot08686c14 re-review',runtimeImplemented:false,newGenerationCalls:0});
console.log(JSON.stringify({report:`${E}/qa-revision-1-art-escalation-report.md`,status:'TECHNICALLY_COMPLETE',artisticStatus:'VISUAL_REVIEW_REQUIRED',artState:'RETURNING_IDLE'}));
