# Defect Evidence — rear-recovery-v2 (numeric, read-only)

**Scope:** 12 `ACTIVE_CANDIDATE` clips from `candidate28manifest.json` + 3 protected baseline aliases (front_l/Sword/Attack, front_r/Walk, front_l/Walk). 123 frames, 180 layer PNGs. No files outside `experiments/main-orc-rear-recovery-v2/diag/` were modified.

**Decoder:** `decode()` from `src/images.mjs` (pngjs-backed). The 15 clip composites are 256x256; all 644 PNGs scanned under `rear-recovery-v2` are colorType 6. Composite metadata hashes cross-checked: 0 mismatches; layer hashes: 0 mismatches.

**Metrics:** per-frame alpha silhouette (`opaque`, `partialAlpha`, bbox, halves, horizontal eighths `bands8`), visible consecutive-frame changes, exact RGBA duplicate pairs, luma >=200 edge clusters, bbox jumps >8 px, and `rightGrip`/`rotationDeg`/`weaponVisible` metadata steps. `bands8` are spatial slices (256-wide: 32 px); `lumaCounts`/`edgeLumaCounts` are luma-threshold counts, not spatial bands. These are **suspects for review**, not artistic verdicts. Coordinate lists are capped at 50 per frame.

**Audit correction:** a scan of 644 PNGs under `rear-recovery-v2` found only alpha 0/255 (no partial alpha) and 151,630 fully transparent pixels with nonzero RGB. Visible deltas now exclude RGB-only differences between transparent pixels and report them as `transparentRgbOnly`. This changes back_l/Walk frame 00->01 from 22.88% RGBA to **7.08% visible**, and removes the apparent loop outlier; `summary.lastVsFirst` records 10,172 transparent-RGB-only pixels at the loop. Exact RGBA duplicates still compare all four channels.

**Claims checked:** Walk left-arm flicker; backR Unarmed fist loss; backL Unarmed inconsistency/duplicates; front Unarmed opposite-arm fade; front Defeat kneeling; frontL Sword armpit; front Walk cloth shading; rear Sword/Axe floating weapon and bright edge. Back Defeat is the praised reference and is not in the 15 targets.

**Reading the numbers:** a count, delta or cluster is a review flag. It does not establish anatomy, intent, or visual quality, and a zero does not by itself prove absence of a perceived defect.

## Clip summary

`bright` = worst body-surface 200-luma edge count (edge max in parentheses); layered Sword/Axe composite peaks are under Finding 8.

| clip | frames | exact dups | max visible body delta | bright >=200 | bbox jumps body/comp |
|---|---:|---:|---|---:|---:|
| front_r/Unarmed | 5 | 0 | 0->1 9.22% | 0 (142) | 2/0 |
| front_r/Defeat | 5 | 0 | 0->1 10.46% | 0 (184) | 3/0 |
| front_l/Unarmed | 5 | 0 | 0->1 9.16% | 0 (148) | 2/0 |
| front_l/Defeat | 5 | 0 | 0->1 10.46% | 0 (168) | 3/0 |
| back_r/Walk | 8 | 0 | 3->4 7.36% | 0 (81) | 0/0 |
| back_r/Unarmed | 5 | 0 | 2->3 8.58% | 0 (158) | 3/0 |
| back_r/Sword | 8 | 0 | 4->5 7.31% | 0 (158) | 2/7 |
| back_r/Axe | 8 | 0 | 0->1 8.92% | 0 (123) | 3/7 |
| back_l/Walk | 8 | 0 | 6->7 7.35% | 0 (68) | 0/0 |
| back_l/Unarmed | 5 | 0 | 1->2 9.84% | 0 (173) | 2/0 |
| back_l/Sword | 8 | 0 | 0->1 4.45% | 0 (138) | 3/6 |
| back_l/Axe | 8 | 0 | 0->1 7.14% | 0 (154) | 4/5 |
| front_l/Sword (baseline) | 13 | 2 | 2->3 9.16% | 0 (160) | 3/9 |
| front_r/Walk (baseline) | 16 | 0 | 11->12 9.05% | 1 px/frame x5 | 3/0 |
| front_l/Walk (baseline) | 16 | 0 | 11->12 9.01% | 1 px/frame x5 | 3/0 |

`0` in the bright column means no **edge** pixel reached luma 200. It is not evidence that no bright contour exists: `maxLuma` can be just below the threshold (back_l/Walk: 199, interior) and the 170 pass finds sub-200 highlights (Findings 6 and 8).

## Finding 1 — Rear Walk: "left arm flickers or disappears"

- **No numeric outlier survives the alpha-aware recount.** back_l visible adjacent deltas: 7.08, 7.25, 4.82, 6.86, 6.31, 6.85, 7.35%; loop 7.44% (median 6.86%; first step 1.03x; loop 1.08x). back_r: 6.50-7.36%; loop 6.79%.
- **Correction:** the earlier 22.88% first step / 22.96% loop counted RGB changes inside fully transparent pixels (10,352 and 10,172 pixels). Those changes are invisible; the tool now reports them as `transparentRgbOnly` and excludes them from visible deltas. Do not cite 22.88/22.96 as motion.
- **Shared rest frame:** frame 00 of back_l Walk is exact-RGBA identical (pixelSha `641afc628b9d`; composite file SHA-256 prefix `0fb8c85ac00f`) to frame 00 of back_l Unarmed/Sword/Axe; back_r Walk frame 00 matches back_r Unarmed/Axe (pixelSha `0980202da33a`; file prefix `245ce5ce71ce`). This is a fact about files, not proof of a copy/paste defect.
- **Slice count:** the x64-95 spatial band (band 2) never reaches zero: back_r 69-114, back_l 91-175. This is a positional count, not an arm measurement; occlusion behind the torso can preserve silhouette area.
- Both clips: 0 exact RGBA duplicates, 0 bbox jumps.
- **Numeric verdict:** no numeric discontinuity in either Walk clip. The claimed flicker remains a visual-review suspect; these metrics neither confirm nor refute a shading/occlusion flicker.

## Finding 2 — backR Unarmed: "striking fist briefly disappears"

- At 1->2 the right half drops 2936 -> 2424 (**-17.4%**) and band 4 (x128-159) drops 2651 -> 2127 (**-19.8%**); both recover at 2->3 (2797, 2603).
- At the strike band 5 (x160-191) grows 180 -> 285 -> 297, and body bbox x1 goes 173 -> 186 -> 170. The outer right extent grows at the strike frame.
- 0 exact RGBA duplicates; visible body deltas 7.57%, 8.29%, 8.58%, 7.64%; 3 body bbox jumps.
- **Numeric verdict:** no frame has an empty right half or a zero band 5. The one-frame thinning is real; the claim that a fist disappears is not supported by silhouette counts. The metrics do not identify a fist or anatomy.

## Finding 3 — backL Unarmed: "severe inconsistent movement / duplicated frames"

- **No exact RGBA duplicates:** 0 identical pairs. F03 and F04 differ from F00 by 8.71% and 8.73% of visible pixels. Near-duplicates were not tested.
- **One-sided contraction is present:** left half 2845 (f02) -> 1818 (f03, **-36.1%**), band 2 (x64-95) 347 -> 0; bbox width 94 -> 64 -> 72.
- **Bbox whips:** 0->1 (dx -15, dw +22) and 2->3 (dx +29, dw -30). Visible body deltas 9.59%, 9.84%, 8.60%, 7.30%: no global spike, but a 36% loss inside one half at 2->3.
- **Numeric verdict:** a large one-sided contraction and two bbox jumps are numeric. The x64-95 collapse is positional; it does not prove a missing recovery pose, an arm, or occlusion. Visual review remains authoritative.

## Finding 4 — Front Unarmed: "opposite arm fades at F03-04"

- **front_r:** left half 2940 (f01) -> 1790 (f02, **-39.1%**) -> 1658 (f03, **-43.6%**) -> 2437 (f04); band 2 goes 436 -> 0. Bbox x0 74 -> 104 -> 99 -> 97 and x1 170 -> 171 -> 162 -> 168. Total opaque 5961 -> 4716 -> 4374 -> 5600.
- **front_l is mirrored:** right half 2940 -> 1790 -> 1658 -> 2437; band 5 goes 436 -> 0; bbox x1 181 -> 151 -> 156 -> 158 and x0 85 -> 88 -> 93 -> 87.
- **The contraction starts at f02, one frame earlier than the claim.** Visible body deltas: front_r 9.22%, 8.98%, 6.55%, 7.80%; front_l 9.16%, 8.89%, 6.41%, 7.77%. The half-body change is hidden by the global number.
- **Numeric verdict:** the non-striking half contracts ~39-44% for two frames and recovers; the full bbox also shifts. This is a silhouette fact. It does not identify an arm, prove an alpha fade, or prove occlusion; visual round 2 still saw the arm near the hip.

## Finding 5 — Front Defeat: "terminal pose reads as kneeling"

- **Heights:** front_r 112, 90, 86, 63, 66; front_l 112, 90, 86, 63, 67.
- **Terminal frame (f04):** front_r 120x66 at x68-187, y125-190; front_l 121x67 at x67-187, y124-190. Previous frame is 88x63 in both.
- **The change:** terminal width expands **+32 px (+36.4%)** / **+33 px (+37.5%)** in one frame with the ground edge fixed at y=190; height changes only +3/+4 px. Body delta 8.10% / 8.21%, so there is no motion spike.
- **Numeric verdict:** the final pose is a sudden wide, low silhouette swap (aspect 1.82/1.81), not a gradual collapse. The numbers cannot distinguish kneeling from prone or identify anatomy. The praised rear Defeat terminal was not in the 15 targets, so no comparison was measured.

## Finding 6 — frontL Sword: "armpit defect"

- **13 frames, 2 exact duplicate pairs:** body and composite f00 == f12 (pixelSha `f8eb47d52291`; file SHA-256 prefix `ff130f2072bf`). The clip returns exactly to its first frame.
- **At the weapon-onset step f01->f02:** body changes **19 px (0.03%)** inside bbox **x133-139, y104-112**; composite changes **712 px (1.09%)** inside bbox x133-197, y89-141. The clip's `rightGrip` metadata is (154,131), about 30 px from the patch center; this is not a contact measurement.
- **Next frame is global:** f02->f03 changes **6,003 body px (9.16%)** and 6,634 composite px (10.12%).
- **Bright edge:** 0 edge suspects >=200 on body; body edge max 160, composite 178. The 170 pass finds one 1-px composite pixel at (196,91), where the body layer is transparent, mean RGB [176,178,180] — a metallic-highlight suspect, not a defect.
- **Numeric verdict:** a compact 19-px body change is the only body change at weapon onset and lies in the y104-112 band; whether that is the armpit is not measured. The metric cannot establish anatomy, a hole, overlap, or intent; visual review remains authoritative.

## Finding 7 — Front Walk: "cloth shading jumps between the legs"

- 16 frames each, 0 exact duplicates, max visible body delta 9.05% / 9.01% (11->12), 3 body bbox width jumps (dw -15, +10, +15).
- Five one-pixel >=200 edge suspects per clip, f06-f10, at x155-156 (front_r) / x99-100 (front_l), y92-97, RGB 201-237. They are isolated highlights, not a continuous band.
- **Shading, folds and cloth panels are not measurable** by alpha, luma-cluster or bbox metrics. The tool has no cloth segmentation and cannot place the reported panel.
- **Numeric verdict:** unverified. No measurable shading jump was found, and the tool has no metric that could confirm one. The bright pixels must not be cited as proof either way.

## Finding 8 — Rear Sword/Axe: floating/pasted weapon and bright edge

- **Composite bbox jumps:** Sword 7/6, Axe 7/5; body only 2-4. Largest repositions: back_r Sword 3->4 (dw +62, dh -35); back_l Sword 0->1 (dx -56), 1->2 (dy -60); back_l Axe 0->1 (dx -37), 1->2 (dy -41).
- **Rotation-metadata reversals:** back_r Sword -35, +55, -35, +75, +40, +35, **-135**; back_l Sword -90, +80, +30, **-140**, -25, -15, **+160**; back_r Axe -45, +35, +10, +70, +35, +30, **-135**; back_l Axe -90, +45, +35, -35, -45, -35, **+125** degrees.
- **Composite deltas exceed body deltas** on all four weapon clips (max: 9.14 vs 7.31, 5.88 vs 4.45, 9.76 vs 8.92, 7.89 vs 7.14%). This is consistent with non-body layers contributing; the tool does not isolate the weapon.
- At back_l Axe f02->f03 the body changes 0.67% (34 px) while rotation metadata steps +35 deg; back_r Axe changes 1.52% at the same step. Largest grip-metadata steps: +175/+106 and -170/-127 (back_r), +92/+108 and -99/-145 (back_l). These are authored metadata, not observed hand contact.
- **Bright edge:** no edge pixel reaches luma 200 on rear weapon frames. Body edge maxima 123-158; composite edge max 178. This does **not** prove the absence of the outline reported by the creator: 1-px 178-luma highlights are present, and sub-200 contour, anti-aliasing or shading is outside the threshold. The 170 pass finds 4-7 isolated 1-px clusters on Axe frames f01-f06 (0 at f00/f07; Sword 0-1), all mean RGB [176,178,180]; the body layer is transparent at every one of those pixels. These are consistent with metallic weapon-edge highlights, but the tool does not identify the layer.
- **Numeric verdict:** one-frame weapon repositions and repeated direction reversals are confirmed. The bright-outline claim is unresolved, not refuted. Hand-to-hilt contact and "floating" cannot be judged from these metrics.

## Finding 9 — Back Defeat: praised reference

Not among the 15 requested targets, so no rows or comparison exist here. Its positive status is from visual review only.

## Baseline controls

- **front_l/Sword/Attack** has 2 exact duplicate pairs (f00==f12) and the 19-px step above; it is a protected alias.
- **front Walk aliases** each have 3 bbox width jumps and five 1-px 200+ edge highlights.
- Small numeric flags are therefore normal in protected baseline art; none of them is an artistic verdict.

## Limitations

1. No numeric metric proves artistic quality, intent, or perceived speed. Creator/visual review remains authoritative.
2. Silhouette counts cannot identify which limb moved, or separate occlusion from deletion. `bands8` are positional 32-px slices at 256 width, not anatomy; luma counts are threshold counts, not spatial bands.
3. Bright-edge results depend on the absolute 200-luma threshold; the 170 pass is sensitivity only. Zero at 200 does not prove no contour. Sub-200 highlights, anti-aliasing, shading and alpha blends are not measured. The 15 clips are binary alpha; synthetic tests cover partial-alpha semantics.
4. Exact RGBA duplicate pairs only. Near-duplicates/visual duplicates were not tested. Fully transparent RGB differences are invisible and excluded from visible deltas; exact RGBA equality can still be affected by them.
5. Grip correctness, wrong-side placement and hand contact were not validated; `rightGrip` and `rotationDeg` are authored metadata.
6. No playback, Unity, or timing review was performed. Hit timing was not measured (no Hit clip). Rear Defeat, native 128px derivatives and in-engine scaling were not measured.
7. Shading, cloth folds, panel segmentation and sub-pixel alpha blends are outside what these metrics can see.

## Reproduce

```bash
node experiments/main-orc-rear-recovery-v2/diag/diag.mjs --all
node experiments/main-orc-rear-recovery-v2/diag/diag.mjs --clip characters/orc-v1/source/rear-recovery-v2/back_l/Walk/clip.json
node --test experiments/main-orc-rear-recovery-v2/diag/diag.test.mjs
```

Output: `experiments/main-orc-rear-recovery-v2/diag/diagnostics-all.json` (compact, 311,531 bytes, 15 clips). Two consecutive `--all` runs were byte-identical (SHA-256 `527D30293D884124C0044396351228794B6C4B609BB05FB42555554A40FF72F8`); runtime 885 ms cold / 984 ms warm. Test suite: 15 tests pass (~2-3 s), covering PNG load/alpha, bright edges, components, delta alpha/colors, duplicates, loops, body fallback, BOM, relative assets, errors and determinism.
