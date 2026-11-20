# Round 3 Zoomed Verdicts — TacticsRPG CharacterFactory

**Scope:** zoomed crops under `tmp/rear-inspect/crops/` (8× zoom, checkerboard background; B-* are 2× full-width bands; E is 2×). Read-only visual inspection at native/crop resolution. No editing, no PixelLab, no Unity. Where resolution prevents certainty, finding is marked NOT_CONFIRMED / uncertain.

Crop mapping (native coords): each E-crop strip panel = 160 native px wide shown at 2×. A/C/D are tight 8× crops of the named region.

---

## A) frontL-Sword-Attack armpit — F00 / F01 / F02

Crops: `A-frontL-Sword-F00-armpit.png`, `A-frontL-Sword-F01-armpit.png`, `A-frontL-Sword-F02-armpit.png` (8×).

**What is visible:** All three crops show essentially the same tight region: top-left = dark grey shoulder pauldron with spikes; center = grey arm/torso meeting; bottom-left = red-brown tunic/fabric; bottom-right = checkerboard (transparent). A dark reddish-brown sleeve/shoulder mass sits on the right side of each crop. The three frames look identical to one another at this rendering.

**The 19-px patch (x133-139, y104-112):** I cannot resolve whether pixels were added, removed, or color-shifted in that band — F00, F01, and F02 armpits render identically to my eye. There is no visible hole/gap/stray pixel cluster and no detached bright speck at the armpit band in any of the three crops. The grey-to-dark transition where the arm meets the shoulder reads as **intentional armpit shading** (the natural fold/occlusion between raised arm and torso), not a defect.

**Verdict on creator's armpit defect claim:** NOT_CONFIRMED as visible here. The armpit at F01 looks fine; no gap/hole/stray is apparent in any of the three crops. If a defect exists it is either (a) below the resolution of these 8× crops, or (b) located elsewhere (not at this armpit band in F00–F02). I did not find the defect at this location.

---

## B) frontR / frontL Unarmed F02 / F03 — opposite (non-striking) arm

Crops: `B-frontR-Unarmed-F02-mirror.png`, `B-frontR-Unarmed-F03-mirror.png`, `B-frontL-Unarmed-F02-mirror.png`, `B-frontL-Unarmed-F03-mirror.png` (2× full-width bands).

### frontR-Unarmed (faces right, strikes with RIGHT fist)
- **F02:** RIGHT arm extended forward (screen-right) at strike peak with brown fist. LEFT arm (opposite/non-striking): present as a dark mass tucked at the left hip/waist, partially behind the red tunic and torso — **partially occluded**, legitimate tucking. Not missing.
- **F03:** RIGHT arm returning/bent toward body. LEFT arm: present at left hip, dark mass against torso/tunic — **partially occluded**, legitimate. Not missing.

### frontL-Unarmed (faces left, strikes with LEFT fist)
- **F02:** LEFT arm extended forward (screen-left) at strike peak. RIGHT arm (opposite): present as dark mass at right hip/waist, partially behind torso/tunic — **partially occluded**, legitimate.
- **F03:** LEFT arm returning. RIGHT arm: present at right hip — **partially occluded**, legitimate.

**Mass loss location (numeric: 39–44% opaque pixels lost at F02/F03 vs neighbors):** The loss is concentrated in the non-striking arm being pulled back **behind the torso/tunic at the hip** (tucked), reducing its exposed silhouette. This is consistent with legitimate tucking/occlusion during a punch (guard returns to hip), **not** an arm actually disappearing. At 2× band resolution the opposite arm remains visibly drawn as a dark hip mass in all four crops.

**Verdict:** Creator's "opposite arm fades/partially disappears near end (F03-04)" is NOT_CONFIRMED for F02/F03 here — the non-striking arm is present but tucked/occluded at the hip in every frame. The numeric mass loss is explained by occlusion, not a missing arm.

---

## C) backR Sword/Axe F04/F05 — bright edge artifacts on extended forearm + weapon

Crops: `C-backR-Sword-F04-forearm.png`, `C-backR-Sword-F05-forearm.png`, `C-backR-Axe-F04-forearm.png`, `C-backR-Axe-F05-forearm.png` (8×).

All four crops show: extended right arm (dark grey forearm armor) → brown glove → weapon (sword or axe) extending to screen-right, checkerboard background. Weapon edges carry light grey/white pixels along the blade/axe-head cutting edge.

**Per-crop verdict:**

| Crop | (1) Pale outline around FOREARM armor | (2) Bright pixels along weapon blade edge | (3) Halo where weapon meets glove | Overall |
|---|---|---|---|---|
| C-backR-Sword-F04 | NOTHING — dark grey forearm meets brown glove, no pale border | INTENTIONAL HIGHLIGHT — white/grey along steel blade edge (normal metal rendering) | NOTHING — glove-to-hilt connection is clean, no pale halo | INTENTIONAL HIGHLIGHT |
| C-backR-Sword-F05 | NOTHING | INTENTIONAL HIGHLIGHT — steel blade edge | NOTHING — clean glove-to-hilt join | INTENTIONAL HIGHLIGHT |
| C-backR-Axe-F04 | NOTHING | INTENTIONAL HIGHLIGHT — grey/white on axe-head blade edge | NOTHING — clean glove-to-haft join | INTENTIONAL HIGHLIGHT |
| C-backR-Axe-F05 | NOTHING | INTENTIONAL HIGHLIGHT — blade edge | NOTHING — clean glove-to-haft join | INTENTIONAL HIGHLIGHT |

**Distinctions:** The forearm armor itself carries no pale/white outline (dark grey, clean silhouette). The bright pixels along weapon blade edges (RGB ~[176,178,180] per numeric, max body 123-158, nothing >=200) read as **intentional steel highlights** on metal — standard pixel-art metal rendering — not pale artifact borders. There is no halo/ghosting where weapon meets glove; the join is tight.

**Verdict on creator's bright-edge-artifact claim:** NOT_CONFIRMED as an artifact. No pale border on forearm armor, no weapon-glove halo. Weapon-edge brightness is intentional metal highlight. Nothing >=200 luminance on body; isolated weapon-edge pixels are in normal highlight range.

---

## D) backL-Unarmed F02 / F03 — left side (striking arm) disappearance

Crops: `D-backL-Unarmed-F02-left.png`, `D-backL-Unarmed-F03-left.png` (8×, left side band).

- **F02-left:** Shows the character's left side. At the **top-left corner** there is a reddish-brown/dark arm shape extending upward and outward — this is the striking LEFT arm extended (strike pose). Below it: grey torso, red tunic belt, legs at bottom.
- **F03-left:** Shows the same left-side band, but the extended arm shape at top-left is **gone**. The top area is now grey torso/shoulder/spikes with no extended arm mass. The red tunic/belt and legs remain similar.

**What disappears between F02 and F03:** The **striking LEFT arm** (extended outward/up at F02) vanishes by F03. It retracts/disappears instantly rather than returning through a visible recovery-to-hip intermediate. Numeric corroborates: left half loses 36% of pixels and band rows ~96–112 goes 347→0 — an entire vertical band of arm mass is removed.

**Not the whole left side:** The torso, tunic, belt, and legs persist; only the extended striking-arm mass is lost.

**Where recovery mass should be restored:** The left arm should return to the hip/side through intermediate frames (as in front Unarmed, where the non-striking arm tucks to hip). Between F02 (extended strike) and F03 (back at side/idle) there is no visible recovery mass — the arm snaps straight back. Recovery arm mass should be restored in an inserted intermediate frame(s) between F02 and F03 showing the arm bending back to the hip.

**Verdict:** Creator's "striking fist briefly disappears" (Round 2) is extended here: the whole striking LEFT arm disappears between F02 and F03 with no recovery intermediate — CONFIRMED visible in these crops.

---

## E) backL-Walk F00 / F01 / F02 / F07 — first-step / loop jump

Crop: `E-backL-Walk-F00F01F02F07.png` (2×, four 160-native-px-wide panels side by side). back view facing away.

**Pose descriptions:**
- **F00 (panel 1):** Neutral/rest. Both arms down at sides, legs balanced under hips, weight even, head centered.
- **F01 (panel 2):** Mid-stride / contact pose. One leg forward (stride), arms swinging. Body appears in a stride attitude.
- **F02 (panel 3):** Continuing stride — leg positions progress smoothly from F01.
- **F07 (panel 4):** Returning toward rest — legs rebalancing, arms down, approaching neutral.

**Pose jump at F00→F01:** Large discontinuity. F00 (neutral, balanced) → F01 (full stride) jumps ~22.9% vs other inter-step jumps of 4.8–7.4%. F01 connects smoothly *forward* to F02 (normal ~5–7%), but jumps *backward* from F00. The legs pop into a wide stride and the torso/hips shift relative to F00.

**Pose jump at F07→F00 (loop):** Also ~23%. F07 (rebalancing toward neutral) → F00 (neutral) jumps back; F00 does not land cleanly after F07, and F00 does not launch cleanly into F01. F00 is the discontinuity anchor on both sides.

**Which body parts move wrongly:** The **legs/feet** pop (foot placement changes drastically between F00 and F01), and the **hips/torso** appear horizontally offset relative to F00/F02. It is not an arm swap — arms stay down in all four. It is not obviously a different perspective — all four are back view, same camera.

**Is F01 a plausible contact pose that is mis-registered (shifted)?** Yes — F01 looks like a legitimate mid-stride/contact pose and it connects smoothly to F02 onward. The anomaly is at the F00 boundary: F01 appears **horizontally shifted (mis-registered)** relative to F00 (and F07→F00 loop). A small horizontal dx shift of F01 (or of F00) would likely make F00→F01 continuous.

**Estimated shift:** Each panel = 160 native px. Normal step ≈ 4.8–7.4% ≈ 8–12 native px. Excess of F00→F01 over normal ≈ 22.9% − ~6% ≈ ~17% ≈ ~27 native px total frame-difference; of that, the pure *mis-registration* (shift) component is plausibly on the order of **~8–14 native px of horizontal dx** (roughly half-to-full normal stride) to realign F01's foot/hip placement with F00/F02. Vertical dy appears minimal (head heights align across F00–F02–F07). This shift estimate is **uncertain** — sub-pixel alignment cannot be measured from the 2× render, and part of the 23% may be legitimate rest→stride motion rather than pure shift.

**Verdict:** Creator's big first-step/loop jump is CONFIRMED visible (22.9% vs 4.8–7.4%; loop 23%). F01 is a plausible contact pose but appears horizontally mis-registered relative to F00/F02; a small dx shift (~8–14 native px, estimate uncertain) would likely smooth it. dy minimal.

---

## Final verdicts (one line per section)

A) frontL-Sword armpit F00–F02: **NOT_CONFIRMED** — 19-px armpit band (x133-139,y104-112) cannot be resolved as added/removed/hole; F00/F01/F02 armpits look identical and read as intentional shading, no visible defect; creator's armpit defect not found at this location.
B) frontR/frontL-Unarmed opposite arm F02/F03: **NOT_CONFIRMED as disappearing** — non-striking arm present but tucked/occluded at hip in all four crops; 39–44% mass loss explained by legitimate occlusion, not a missing arm.
C) backR Sword/Axe forearm/weapon edges F04/F05: **NOTHING / INTENTIONAL HIGHLIGHT** — no pale forearm border, no weapon-glove halo; weapon-edge brightness (max ~[176,178,180], nothing >=200 on body) reads as intentional steel highlight, not artifact.
D) backL-Unarmed striking arm F02→F03: **CONFIRMED** — extended striking LEFT arm at top-left of F02-left is entirely gone in F03-left (band rows 96–112 347→0); whole striking arm vanishes with no recovery intermediate; recovery mass should be restored between F02 and F03.
E) backL-Walk F00→F01 and F07→F00: **CONFIRMED jump** — 22.9% vs 4.8–7.4% normals; loop 23%; legs/hips pop, F01 is a plausible contact pose but appears horizontally mis-registered vs F00/F02; estimated dx shift ~8–14 native px (uncertain), dy minimal.
