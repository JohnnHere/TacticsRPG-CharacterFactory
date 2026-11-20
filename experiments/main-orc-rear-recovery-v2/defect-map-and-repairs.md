# Defect map & repair design — creator review 2026-10-27

> **Historical hypotheses, not an accepted repair plan.** R1 and R2 are
> unintegrated experiments; their frame removal, timing and grip changes require
> visual review. The R2 back_r/Axe draft uses outdated F04/F05 grip coordinates
> rather than the repaired freeze's `[181,118]` and `[181,122]`. The original
> Walk delta included invisible RGB differences; see
> [the corrected diagnostic](diag/DEFECT-EVIDENCE.md). The frontal crown-only
> halo check is a coverage limitation, but the cause of the reported rear
> contours has not been established. Do not treat the proposals below as fixes
> or their numerical and visual claims as an artistic verdict.

Base: freeze `0ad263a6…` (verified 4061/4061 against working tree). Creator matrix + VL round 1
(`diag/visual/rear-attacks-inspection.md`) + numeric checks. No PixelLab budget (78/78 consumed);
all repairs are local Aseprite authoring + procedural recomposition.

## Evidence → root cause → repair (by area)

### 1. back_l Sword + back_l Axe — "severe motion inconsistency" (CRITICAL)
- VL: F01 is a full forward extension (no wind-up); F02 snaps to overhead; F04 extends again (double reversal).
- Numeric: F01 body ≠ F04 body (68%/22% diff) — misplaced distinct pose, not a duplicate.
- Angles: Sword 270→350→20→240; Axe 270→315→350→315.
- **Repair R1: drop F01.** New 7-frame arc: idle → cocked-overhead → load/hold → release → impact → follow → recovery.
  Retimed to ~700 ms. Recompose via `author_back_l_sword_and_back_r_axe_representatives.lua` param table
  (bodies: base + cleaned-native minus frame 00; grips/angles preserved from kept frames).

### 2. back_r Sword v2 + back_r Axe — abrupt reversal + grip (CRITICAL→HIGH)
- VL: coherent overall; F03(overhead)→F04(extended) snaps with no easing; weapon reads pasted at F04-F05.
- Angles Sword: 325→20→345→60 (hold wobble 20↔345 = 35° jitter during overhead hold).
- **Repair R2:** normalize overhead-hold angles (F02/F03 same angle ±5°), keep strike snap but tune hold/strike
  durations (hold +20 ms, strike −20 ms) so the snap reads as impact speed. No pose redraw.

### 3. Grip "not visibly grasped" — all 4 rear attacks (HIGH)
- handFront is procedurally copied from body glove pixels (±5 px window at grip). At extended frames the
  body glove cluster is thin → no wrap reads; weaponFront covers the hand.
- **Repair R3: glove authoring in body frames.** At extended/cocked frames, author a full fist cluster
  (≈11×11: knuckles, thumb hint, palette from existing glove) at the measured hand anchor in the 128×128
  body frames; handFront extraction then captures a wrapping fist. Iterate: compose → VL zoom-crop verdict.
- Contract kept: `weaponBack → body → weaponFront → handFront`, attack-only visibility, weapons independent.

### 4. Bright/pale edges — back_r Sword/Axe F04-F05 (CRITICAL report; VL low-confidence)
- VL could not confirm at strip resolution (may be intended metal highlight on forearm).
- **Repair R4 (conditional):** awaiting DEV-diag bright-edge cluster report on body layers. Remove only clusters
  verified NOT to match approved armor-highlight palette/position; compare with front_r approved highlights.

### 5. Unarmed front — opposite arm disappears near end (HIGH) — awaiting VL round 2 + diag
### 6. Unarmed back_r — striking fist disappears (HIGH) — diag already shows band drop −20% at F02
### 7. Unarmed back_l — severe inconsistency/duplicates (CRITICAL) — awaiting VL round 2 + diag
### 8. Walk rear — arm flicker (HIGH) — awaiting VL round 2 + diag
### 9. Defeat front — terminal reads kneeling (HIGH) — awaiting VL round 2; good reference = back Defeat terminals
### 10. front_l Sword armpit (MEDIUM) — awaiting VL round 2 (13-frame strip)
### 11. Walk front cloth shading (MINOR) — awaiting VL round 2

## Verified recurrence gap (section 17 of task)
- Halo/bright-pixel gate exists but was scoped to **frontal head band only** (`config/artistic-quality-gates-v1.json`
  + docs). Rear views were never covered → bright edges returned unchecked.
- Fix: extend bright-edge diagnostic to all views/whole-silhouette (as diagnostic warning, not hard fail),
  wire into diag tooling; document in ARTISTIC_QUALITY_GATES lesson update.

## Repair ordering
R1 (drop F01 backL) → R2 (hold normalization + timing) → R3 (glove authoring, VL loop) → R4 (conditional
bright-edge removal) → unarmed/walk/defeat batches after evidence lands. Every batch: fork → edit → recompose →
re-export → verify (existing verifiers + diag rerun) → VL check → update manifest cell status only after pass.
