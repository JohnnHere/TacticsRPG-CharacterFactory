# Implementation-ready art-coordinate handoff — main-orc-rear-recovery-v2 (2026-10-26)

Author: GLM ART executor turn (assessment + handoff only, per Root role narrowing).
No source art authored this session; no paid calls made. All QA helper files preserved under
`experiments/main-orc-rear-recovery-v2/qa-zoom/` (helper: `qa_zoom.py`, QA-only, not production).
Must-preserve: `root-cost-audit-correction.md` — ledger records 1–2 keep Root's corrected UUIDs
(`af1e7ba8-655e-45fd-9798-2ba4b8cda7e9`, `ed109b13-7b60-4200-8a43-ed8a9fb8f561`) and corrected
input/output paths (`raw/walk-draft01-k[12]-{request,creation}.json`, receipts `raw/root-cost-confirmation-k[12].json`).

## 1. Verified tool capabilities (actually exercised this session)

- Aseprite AVAILABLE: `checkAseprite()` → `F:\SteamLibrary\steamapps\common\Aseprite\Aseprite.exe`.
  Official hidden runner works: `node experiments/main-orc-rear-recovery-v2/run_aseprite_script.mjs <script.lua>`
  (wraps `src/aseprite.mjs` `executeAseprite`, `--batch --noinapp`, `ASEPRITE_USER_FOLDER=tmp/aseprite-batch-profile`).
- Agent image viewing works (read_files on PNG). Practical limit: long strips get downscaled — always add
  32px grid + numeric labels (pattern in `qa_zoom.py`, `sword-bodies-grid-half*.png`).
- venv Python: `tmp/pixel-venv/Scripts/python.exe`, PIL 13.0.0 — QA/analysis only.
- Node repo tooling (`exportAseprite`, `hash`, `decode`, pngjs) verified by the previous PASS build
  `dist/editor/main-orc-rear-recovery-v2-export/663e379bdd42e17b8cba`.
- Environment gotcha: PowerShell wraps python stderr as NativeCommandError (traceback lost). Use `cmd /c`.
- Blocker resolved by Root: weapon rotation — use the proven transform, do NOT use app.command.Rotate.

## 2. Transform function pointer (reuse ONLY this math)

`tools/aseprite/author-main-orc-complete.lua` lines 896–925 — `renderWeaponLayers(itemImg, itemGrip,
targetGrip, angleDeg, behindBody, flipBit, isRearForwardStrike)`: nearest-neighbor inverse rotation about
itemGrip→targetGrip via `math.cos/sin` + `getPixel/drawPixel`, alpha>=128, per-pixel back/front split.
- DO NOT copy its rear depth policy (`isRearForwardStrike → toBack=true`) — that blanket rule was part of
  the floating-weapon defect. Use explicit per-frame depth (§5).
- Independent weapon assets (unchanged, hashes in complete-v1 clip.json):
  - recruit-sword `assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png`, 96×96, itemGrip `[48,66]`
  - militia-axe `assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png`, 96×96, itemGrip `[36,55]`
- Angle convention NOT yet calibrated: verify the sword sprite's native orientation first by rendering one
  known pose (e.g. angle 0 at a rest grip) and viewing it; then derive the per-frame angle table. Old
  metadata rotationDeg values (e.g. back_r f2=315, axe f2=60) were authored for the OLD placements —
  treat as hints only, re-derive after calibration.

## 3. Body cycle decision (verified by viewing, not assumption)

- OLD cycle bodies ARE the cached empty-hand swing: rest → reach/establish → cock up-high → sweep
  down/out → rest. Internally consistent art. The creator-visible bug is the weapon floating detached
  on the WRONG side (old composite f07: large sword left of body, no hand contact; weaponBack f05–f09
  visiblePct 36–81% = blade hidden behind torso while hand is elsewhere).
- The 4 ProFlash keys (24 gen; `raw/clean_sword_slash_r|l.png`, `test_axe_r|l_clean.png`) are
  effectively EMPTY-HAND single poses but with DIFFERENT proportions (bulkier torso, larger head,
  different cape rendering). Mixing them into the old body sequence = proportion pop (lesson 5/8).
  DECISION: do not use as body layers; representative cycle = old bodies + weapon re-anchored per frame.
  Documented as "reuse where compatible → NOT compatible as mixed layers".
- Shared bodies: `qa-zoom/hand-analysis.json` `bodyEquality_sword_vs_axe_0-11` =
  [T,T,T,T,T,F,F,F,T,F,F] — axe has its OWN body art at f5–f8 and f10–f11 (heavier chop poses).
  For axe expansion, read `back_r/Axe/Attack/layers/body/NN.png` separately; do not reuse sword grips there.

## 4. Rejected auto-detector — why it found feet (do not redo blind)

Erosion-based arm-extremity detector (`qa_zoom.py` `hand_extremity`): MinFilter(5)×3 on the alpha mask
strips thin appendages; farthest-from-centroid survivor = hand. Result: feet won (tips y≈185–190,
x alternating 93/155) because feet are the largest extremity of the standing silhouette and the mask
was NOT region-limited. Fix (described, NOT implemented): restrict mask to the arm band (y≈70..170,
x≈105..190 for back_r) BEFORE erosion, then take the band-limited extremity. Kept as optional precise
step; the manual-grid + verify-adjust loop below is the primary path.

## 5. Manual grips (APPROXIMATE — needs verify-adjust, then lock)

`experiments/main-orc-rear-recovery-v2/rear-sword-back_r-manual-grips.json` (composite 256 coords,
±8 px, visual read off the 32px-grid strips). Arc: rest f0–2 (150,133) → rise f3 (152,105) → cock
f4–6 (148–150, 90–94) → f7 (150,96) → swing-out f8 (152,118) → f9 (151,124) → low f10 (149,130) → rest.
Choreography mapping (horizontal slash vs old diagonal; sword only, back_r):
- f2–3 establish grip: blade diagonal up-forward at hand, weaponFront.
- f4–7 windup: blade horizontal pulled back-left ACROSS BEHIND torso → weaponBack (honest back placement:
  the blade crosses the dorsal plate — not a blanket rule).
- f8 SLASH: blade horizontal extending RIGHT from fist (flipBit=true after calibration) → weaponFront.
- f9 follow-through: same orientation, hand lower → weaponFront.
- f10 recovery: blade diagonal down-right → weaponFront.
- f11–12 + f0–1: no weapon (visibleInterval [2,10] preserved).
- handFront on ALL weapon-visible frames: re-stack the body's OWN fist pixels (copy body-layer pixels
  inside the fist bbox around rightGrip into the handFront layer at identical coordinates) so the
  authored gauntlet occludes the hilt. No redraw.
- Distinctness rule: sword = horizontal orientation through swing; axe (expansion) = vertical overhead
  cock + vertical chop using axe's own f5–f8/f10–f11 bodies. No axe enlargement.

## 6. Front Unarmed F02 surgical fix (confirmed defect; coords as known)

- front_r: truncation at flat cut x≈157..162, cut gray [101,102,105], arm band y≈105..121 (verified in
  `qa-zoom/front-unarmed-02-cut-8x.png`, `front-unarmed-02-arm-4x.png`). Donor fist: frame 03's own
  extended-arm gauntlet fist, approx bbox (156..172, 124..146) in 03 (`front-unarmed-03-arm-4x.png`) —
  VERIFY exact bbox visually before copying. Target: fist center ≈ (166,113), overlapping the cut edge
  by ~2px; forearm connect = extend 02's own armor band columns (sample x≈152..157) outward 3–5px; then
  remove any exposed flat-cut column pixels. All in Aseprite Lua; donor/target are same-character art.
- front_l: mirror-geometry (punch toward viewer-left, cut edge x≈95..100, band y≈105..121, verified in
  `front_l-unarmed-02-arm-4x.png`). Donor = front_l 03 fist — bbox NOT yet visually verified
  (`front_l-unarmed-03-arm-4x.png` exists but was not inspected). Verify before authoring.
- After fix: front_r/front_l Unarmed become ACTIVE_CANDIDATE (aliases 18→16). Keep frames 00/01/03/04
  byte-identical, durations [80,110,50,90,120] unchanged. Masters to fork into
  `characters/orc-v1/source/aseprite/rear-recovery-v2/composite/front_r|front_l/unarmed-attack.aseprite`.

## 7. Remaining implementation tasks (next authorized agent; no scope re-audit needed)

1. back_r Sword representative (FIRST, root review before expansion): new Lua via official runner;
   body layers = old bodies byte-identical; weapon layers per §5 choreography via transform pointer;
   handFront per §5; write masters `composite/back_r/sword-attack.aseprite` (4 layers, 13 frames,
   durations [30,65,35,50,45,65,35,35,100,55,80,45,90]), `sword-body.aseprite`, `sword-hand-front.aseprite`,
   native `native/sword-back_r.aseprite` (128×128, offset −64,−64, nativeGroundY 126); export candidate
   `characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack/` (NN.png, layers/…, native-strip.png,
   clip.json with new per-frame rightGrip/rotationDeg/weaponVisible + regenerated layer hashes, weapon
   block hashes unchanged; keep contactEvent f8/360ms CANDIDATE_VISUAL_ONLY; attack-only-v1).
2. Grip proof (hard check, not metadata): body layer opaque at rightGrip; weapon bbox extends ≥6px past
   body silhouette on slash frames; handFront opaque at rightGrip; emit marked proof strip for viewer.
3. Re-export verification: extend `verify_export_aseprite.mjs` + `verify_export_pixels.mjs` job lists
   (add sword-back_r; later weapons + front unarmed). Keep existing 6 jobs passing.
4. Root review checkpoint → then expand: back_r Axe (own bodies f5–f8/f10–f11, vertical chop, itemGrip
   [36,55], visibleInterval [2,8], durations [40,65,35,80,155,35,115,110,130,50,90,100]), then back_l
   Sword/Axe (read back_l bodies fresh; NW authored views, never flip front art).
5. Front F02 fix per §6 (+ verify jobs + manifest status flips).
6. HIT playback QA: 1x/.75x/.5x GIFs at native 128 for 4 directions from UNCHANGED clip frames
   (external Python GIF assembly of unchanged art = QA-only, allowed); record observed motion honestly,
   defer runtime feel calibration; no compulsory redraw.
7. Update `candidate28manifest.json` statuses/paths, `production-final-report.md` (notify PreviewGLM8591
   via file only), `cost-provenance-ledger.json` stays 66 consumed (no new paid calls; preserve Root's
   corrected records 1–2).

## 8. Status vocabulary (binding)

Rear weapon cells remain `ARTISTIC_REVISION_REQUIRED` until representative lands + root review;
front Unarmed remain alias-defective until F02 lands. Nothing here is creator-approved
(`PENDING_CREATOR` throughout). No Unity writes. No commits. Keep failed-attempt archives intact
(`rejected/flat-weapon-masters/`, `rejected/draft-01-crossfade/`, `rejected/weak-punch/`).


