# Localized ART polish — main-orc-combat-rescue-v5

**Character:** orc-v1 / Verde Warcraft (MAIN ORC). Obsolete Orc V4 forbidden and not used.
**Date:** 2026-10-29
**Scope:** four Walk directions (reararm / frontcloth shading) + front_r/front_l Defeat (prone terminal + reported handsmear).
**Write-only dirs:** `characters/orc-v1/source/combat-rescue-v5/localized/` and `experiments/main-orc-combat-rescue-v5/localized/`.
**Not touched:** Sword/Axe/Unarmed/grip (main combat producer owns). Idle/Hit/rearDefeat fully protected. No Unity, no commits, no shared docs/globalmatrix changes.
**Internal status:** `LOCALIZED_CORRECTION_APPLIED` — correction applied and numerically verified; final motion/Defeat verification belongs to independent QA (not blocked on creator approval to conclude internal production).
**Artistic approval:** `PENDING_CREATOR` (not claimed).

## Tooling confirmation (Root gate 1 — DONE)
- Aseprite `F:\SteamLibrary\steamapps\common\Aseprite\Aseprite.exe` 1.3.18.6-x64 confirmed AVAILABLE via `editor-check` (batch, `--noinapp`, hidden window, `ASEPRITE_USER_FOLDER=tmp/aseprite-batch-profile`).
- Python Pillow available at `tmp/pixel-venv/Scripts/python.exe`; used ONLY for read/validate/preview, never production raster.
- All artistic raster edits/master save/export done inside Aseprite `--batch --noinapp` (Lua `putPixel` on a forked native master). No image-gen, no external drawing.
- NOTE: I did NOT run Root's `experiments/main-orc-combat-rescue-v5/validate.mjs` — the target matrix does not exist yet in this scope, and I must not alter Root's files.

## Investigation method (read pixels, not dimensions/binary-alpha)
Compared full normal 1× sequences across 16f (front Walk) and 8f (rear Walk), then located temporal inconsistency via half-cycle same-pose region comparisons with semantic material inspection:
- Rear Walk arm: compared F(i) vs F(i+4) (8-frame loop → arm at identical screen coordinates; arm bounding boxes near-identical across all 8 frames).
- Front Walk cloth: compared F(i) vs F(i+8) (16-frame loop) in between-legs zone.
- Defeat: inspected F02/F03 (hands) and F04 (terminal) for partial alpha, bright pixels, smear.
LIMITATION (honest): evidence is static frame captures (nearest-neighbor), not continuous 1× motion. Comparing F(i) vs F(i+4) plus opaque-pixel intersection and similar bboxes supports, but does not by itself prove, identical pose/material. Binary alpha and absence of bright pixels do NOT exclude a smeared/deformed hand. Final motion and Defeat verification is QA's role.

## Findings — honest hypothesis vs confirmed

### 1. back_l Walk — reararm shading — LOCALIZED CORRECTION APPLIED (pending QA motion verification)
**Hypothesis:** creator-reported rear-arm shading flicker is a real per-frame material inconsistency at identical arm coordinates.
**Observation (confirmed numerically):** Same-geometry opaque pixels at identical arm coordinates differ between half-cycle frames:
- right arm F00/F04: 1,554 differing pixels; F04 composite `(137,84)` bright outlier `(184,186,185)` vs F00 dark `(6,6,8)`.
- right arm F01/F05: 1,493; F02/F06: 1,540; F03/F07: 1,612 differing pixels. Left arm 1,444–1,456 per pair.
- Arm bounding boxes near-identical across all 8 frames (right arm x[128,146], y-top 70–73; left arm x[108,126]).
**Honest limit:** this establishes a material inconsistency at repeated pose coordinates; it does not by itself prove the perceived flicker in motion, nor that F0–F3 is the "correct" reference vs F4–F7. The choice of F0–F3 as reference is a production decision, not a proven ground truth.
**Correction applied:** Aseprite batch Lua `putPixel` on forked native master `walk-back_l-fixed.aseprite`: copied reference-half (F0–F3) arm material color to target half (F4–F7) at **overlapping-opaque identical coordinates only** (both source & target opaque → geometry-only differences such as a 1–2 px arm top-edge shift were NOT touched). 2,741 pixels total (right arm 1,364; left arm 1,377).
**Numerical verification (actual checks):**
- Alpha changed count: **0** (no alpha writes, no transparent-pixel writes, no erasing opaque original).
- Color-only changes, alpha preserved: **2,741 / 2,741**.
- F0–F3 fixed composites pixel-identical to originals (unmodified art preserved).
- F04/F05/F06/F07 differ from originals by exactly 667 / 690 / 713 / 671 pixels = fix counts (nothing else changed).
- Post-fix half-cycle right/left arm same-geometry diffs: **0** (loop shade-periodic at repeated pose coordinates).
- Gait/timing/silhouette untouched: durations all 160 ms (total 1280 ms), canvas/bodyOffset/groundY unchanged.
**Disposition:** `CORRECTION_APPLIED` — material normalization applied and numerically verified; whether it resolves perceived flicker in continuous 1× motion is for QA, not declared fixed by me.

### 2. back_r Walk — KEEP (no defect demonstrated)
Right-arm highlight `(156,158,158)` moves across frames `(136,87) → (137,86) → … → (135,87)` = highlight travels with the arm swing (genuine motion). Half-cycle diffs (643–707) are `(2,2,3)↔(7,7,10)` shadow/transition shading as the arm rotates — no stuck bright outlier. No defect demonstrated; kept unchanged.

### 3. front_r Walk & front_l Walk — KEEP (no defect demonstrated)
Cloth bright highlight `(231,230,227)` changes coordinates between half-cycle frames as legs move (e.g. front_r F00 `(126,101),(131,103)` vs F08 `(128,103),(131,106)`). The cloth hangs between moving legs, so half-cycle apart the cloth is in a different shape/position — genuine cloth motion, not flicker. Gait/timing/cloth silhouette intact. Kept unchanged.

### 4. front_r Defeat & front_l Defeat — KEEP (inspection recorded; smear not excluded by alpha alone)
**Hypothesis:** reported hand smear/blur in F02/F03; terminal may be kneeling not prone.
**Observation:** F02/F03/F04 partial-alpha = 0 and bright (>600 sum) = 0 in all three frames → no partial-alpha or bright-pixel smear source found in the raster.
**Honest limit:** per Root, binary alpha and absence of bright pixels do NOT exclude a smeared/deformed hand. I recorded this observation; I do NOT claim the smear is definitively absent. Static terminal F04 reads prone per the independent QA report ("front Defeat F04 already reads prone in staticframe"), but continuous-motion Defeat verification is QA's role.
**No edit made:** no global rotation/flattening/regional compression; no hand repaint. Kept unchanged pending QA.
**Disposition:** `KEPT — observation recorded, smear not excluded by alpha alone; QA to verify motion/Defeat.`

### 5. back_r Defeat & back_l Defeat — KEEP (protected)
Protected rear Defeat, preserved intact (not in localized edit scope).

## Protected animations
Idle (all directions), Hit (all directions), rear Defeat (back_r/back_l), front_r/front_l Sword/Axe choreography: preserved, not in localized edit scope. Sword/Axe/Unarmed/grip owned by main combat producer — not touched.

## Metadata compatibility with parent (verified)
Fixed `back_l/Walk` clip matches parent contract exactly:
- canvas [256,256], bodyOffset [64,64], groundY 190
- nativeCanvas [128,128], nativeGroundY 126
- frameCount 8, durationsMs [160]×8, totalDurationMs 1280
- visibilityPolicy attack-only-v1, weaponVisible false, weaponOverlay false, loop true, oneShot false, terminal false
- nativeMaster sha `3e4fcf16001b205e841f18208fb7b89bfbbc253c0149ba71eb96634fa7e35352` matches `walk-back_l-fixed.aseprite` on disk
- strip sha `bc71022f86f121aeea4233ea2210039612611af5cbca354ec1c5329b84343232`
- No weapons introduced (images have independent weapons hidden).

## Master contract (fixed per validate.mjs finding)
The `.aseprite` master is split into two sources, per the parent contract:
- `clip.master` / `masterSha256` → `walk-back_l-fixed-256.aseprite` (**256×256 composite master**, bodyOffset `64,64`, 8 frames × 160ms, pixels identical to the 8 composite PNGs). sha `1d6069e94a9897f02c65c9afe76a9069792d2b94760182d88a56602a90d45f18`.
- `clip.nativeMaster` / `nativeMasterSha256` → `walk-back_l-fixed.aseprite` (**128×128 native master**, source of truth for the localized fix). sha `3e4fcf16001b205e841f18208fb7b89bfbbc253c0149ba71eb96634fa7e35352`.

**Lesson (honest):** Aseprite Lua `Frame.duration` is in **seconds**, not ms. Setting `frame.duration = 160` saturated the 16-bit field to 65535ms (65.535s); corrected to `frame.duration = 0.160` (160ms). All 8 frames now export at `duration=0.16` (160ms).

## Files produced (write-only scope only)
- `characters/orc-v1/source/combat-rescue-v5/localized/patch-manifest.json`
- `characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed-256.aseprite` (256 composite master, saved via Aseprite batch)
- `characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed.aseprite` (128 native master, forked + fixed)
- `characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/clip.json`
- `characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/00.png–07.png` (composite 256×256)
- `characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/native/00.png–07.png` (native 128×128)
- `characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/native-strip.png`
- `experiments/main-orc-combat-rescue-v5/localized/backl_walk_arm_fixlist.json` (2,741 traced fix pixels)
- `experiments/main-orc-combat-rescue-v5/localized/before_after_inventory.json` (before/after; alpha preserved)
- `experiments/main-orc-combat-rescue-v5/localized/apply_backl_fix.lua` (Aseprite batch fix script)
- `experiments/main-orc-combat-rescue-v5/localized/create_master256.lua` (256 master creation script)
- `experiments/main-orc-combat-rescue-v5/localized/fix_duration_seconds.lua` (duration 0.160s correction script)
- `experiments/main-orc-combat-rescue-v5/localized/checkpoint.json` (milestones)
- `experiments/main-orc-combat-rescue-v5/localized/preview_rightArm_before_after.png`, `preview_leftArm_before_after.png`

## Preview (for creator)
Before/after arm sheets in `experiments/main-orc-combat-rescue-v5/localized/preview_*_before_after.png` (NEAREST zoom, no smoothing).

## Honest limits recap
- Numeric diff to zero ≠ proven artistic fix; QA must verify motion.
- Binary alpha / no-bright-pixels ≠ hand smear absent; QA must verify Defeat motion.
- F0–F3 chosen as reference is a production decision, not proven ground truth.
- I do not claim artistic approval; `PENDING_CREATOR`.

## Next steps (Root)
- Root handles integration and mandatory independent QA (motion + Defeat).
- Await QA findings before any promotion; no artistic approval claimed here.
