# Round 2 Visual Inspection — TacticsRPG CharacterFactory

**Scope:** composite contact-sheet strips (frame 00 = leftmost), read-only visual inspection at native resolution. No editing, no PixelLab, no Unity.
- A) backR-Walk-composite.png (8f), backL-Walk-composite.png (8f)
- B) frontR-Unarmed-composite.png (5f), frontL-Unarmed-composite.png (5f)
- C) backR-Unarmed-composite.png (5f)
- D) backL-Unarmed-composite.png (5f)
- E) frontR-Defeat-composite.png (5f), frontL-Defeat-composite.png (5f); backR-Defeat-composite.png (5f), backL-Defeat-composite.png (5f)
- F) frontL-Sword-Attack-composite.png (13f)
- G) frontR-Walk-composite.png (16f), frontL-Walk-composite.png (16f)

**Convention:** For back_* strips, "image-left arm" = character's LEFT arm (screen-left side), "image-right arm" = character's RIGHT arm (screen-right side). Character faces away from camera.

Where resolution prevents certainty, finding is marked NOT_CONFIRMED.

---

## A) Walk loops (backR-Walk 8f, backL-Walk 8f)

Creator claim: left arm flickers / temporarily changes or disappears between frames.

### backR-Walk-composite.png (8f) — back view, facing right

| Frame | Image-left arm (screen-left) | Image-right arm (screen-right) | Attached at shoulder? | Notes |
|---|---|---|---|---|
| 00 | Present, hangs down at side | Present, hangs down at side | Yes | Idle-like rest, both arms down |
| 01 | Present, swings back | Present, swings forward | Yes | Mid-stride, both arms visible |
| 02 | Present, forward/up | Present, back/down | Yes | Both arms visible |
| 03 | Present, **raised up near shoulder** (shape/pose change vs other frames) | Present, down | Yes | Left arm pose differs from adjacent frames |
| 04 | Present, back | Present, forward | Yes | Both arms visible |
| 05 | Present | Present | Yes | Both arms visible |
| 06 | Present | Present | Yes | Both arms visible |
| 07 | Present, down | Present, down | Yes | Return toward rest |

**Arm disappearance check:** No frame shows the left arm fully absent. Both arms are present and attached at the shoulder in all 8 frames.
**Shape change:** Frame 03 — image-left arm is raised up near the shoulder, unlike frames 00/04/07 where it hangs down. This is a pose variation, not a disappearance.
**Creator claim (left arm disappears):** NOT_CONFIRMED — left arm never fully disappears; only a pose change in frame 03.

### backL-Walk-composite.png (8f) — back view, facing left

| Frame | Image-left arm (screen-left) | Image-right arm (screen-right) | Attached at shoulder? | Notes |
|---|---|---|---|---|
| 00 | Present, hangs down at side | Present, hangs down at side | Yes | Rest |
| 01 | Present, extends forward (screen-left) | Present, swings back | Yes | Both arms visible |
| 02 | Present, **raised up near shoulder/head** (pose change) | Present, down/back | Yes | Left arm pose differs from adjacent frames |
| 03 | Present | Present | Yes | Both arms visible |
| 04 | Present | Present | Yes | Both arms visible |
| 05 | Present | Present | Yes | Both arms visible |
| 06 | Present | Present | Yes | Both arms visible |
| 07 | Present, down | Present, down | Yes | Return toward rest |

**Arm disappearance check:** No frame shows the left arm fully absent. Both arms present and attached in all 8 frames.
**Shape change:** Frame 02 — image-left arm raised up near shoulder/head; frame 01 — left arm extends forward. Pose variations within a walk, not disappearances.
**Creator claim (left arm disappears):** NOT_CONFIRMED — left arm never fully disappears.

### Section A summary
Creator's "left arm disappears/flickers" claim is NOT_CONFIRMED. Both arms remain present and attached at the shoulder in every frame of both walk loops. Minor pose variations exist (backR-Walk F03 left arm raised; backL-Walk F02 left arm raised) but these are normal walk-cycle motion, not defects.

---

## B) frontR-Unarmed 5f / frontL-Unarmed 5f

Creator claim: arm OPPOSITE the striking fist fades / partially disappears near end (frames 03-04).

### frontR-Unarmed-composite.png (5f) — front view facing right, strikes with RIGHT fist

| Frame | Striking arm (right) | Opposite arm (left) | Opposite arm present? | Notes |
|---|---|---|---|---|
| 00 | Down at side | Down at side | Yes | Rest |
| 01 | Punches forward (screen-right) | Pulled back to hip | Yes | Both arms visible |
| 02 | Fully extended forward (strike peak) | At hip | Yes | Both arms visible |
| 03 | Returning (bent) | At hip | Yes | Left arm visible at hip, not faded |
| 04 | Back at side | Down at side | Yes | Rest, both arms visible |

**Opposite arm in F03-04:** Left arm remains visible at hip (F03) and at side (F04). No fade or partial disappearance observed.
**Creator claim:** NOT_CONFIRMED — opposite arm does not fade/disappear in frames 03-04.

### frontL-Unarmed-composite.png (5f) — front view facing left, strikes with LEFT fist

| Frame | Striking arm (left) | Opposite arm (right) | Opposite arm present? | Notes |
|---|---|---|---|---|
| 00 | Down at side | Down at side | Yes | Rest |
| 01 | Punches forward (screen-left) | Pulled back to hip | Yes | Both arms visible |
| 02 | Fully extended forward (strike peak) | At hip | Yes | Both arms visible |
| 03 | Returning (bent) | At hip | Yes | Right arm visible at hip, not faded |
| 04 | Back at side | Down at side | Yes | Rest, both arms visible |

**Opposite arm in F03-04:** Right arm remains visible at hip (F03) and at side (F04). No fade or partial disappearance observed.
**Creator claim:** NOT_CONFIRMED — opposite arm does not fade/disappear in frames 03-04.

### Section B summary
Creator's "opposite arm fades/partially disappears near end (F03-04)" claim is NOT_CONFIRMED for both frontR-Unarmed and frontL-Unarmed. The non-striking arm remains clearly visible at the hip/side in all frames, including 03 and 04.

---

## C) backR-Unarmed-composite.png (5f)

Creator claim: striking fist briefly disappears.

backR-Unarmed = back view facing right; striking arm = image-right arm (screen-right side).

| Frame | Striking arm (right) | Striking fist visible? | Notes |
|---|---|---|---|
| 00 | Down at side | Yes (hand at side) | Rest |
| 01 | Raised up near shoulder | Yes (fist near shoulder level) | Wind-up |
| 02 | Extended forward/out to screen-right (strike) | Yes (fist at end of extended arm, small but visible) | Strike peak |
| 03 | Returning down toward hip | Yes (fist near hip) | Recovery |
| 04 | Down at side | Yes | Rest |

**Fist disappearance check:** The striking fist is visible in every frame (00-04). At F02 (strike peak) the fist is small because the arm is fully extended, but it is present at the end of the arm — not absent.
**Creator claim:** NOT_CONFIRMED — striking fist does not disappear in any frame of backR-Unarmed.

---

## D) backL-Unarmed-composite.png (5f)

Creator claim: severe inconsistent movement, possibly duplicated or incompatible frames.

backL-Unarmed = back view facing left; striking arm = image-left arm (screen-left side).

| Frame | Pose description | Notes |
|---|---|---|
| 00 | Back view, both arms down at sides (idle) | Rest pose |
| 01 | Left arm raised up near shoulder/head level; right arm at side | Wind-up |
| 02 | Left arm extended out to screen-left (strike); right arm at side | Strike peak |
| 03 | Both arms down at sides — near-identical to F00 | Abrupt return to idle |
| 04 | Both arms down at sides — near-identical to F00 and F03 | Hold at rest |

**Identical / near-identical frames:** F00, F03, and F04 are near-identical idle poses (both arms down at sides). F03 and F04 duplicate the F00 rest pose.
**Abrupt pose jump:** F02 (arm fully extended striking) → F03 (arm instantly back at side, idle). No return-to-hip or follow-through intermediate; the strike snaps straight back to rest.
**Perspective change:** None — all 5 frames are back view; no frame looks like a different camera angle.
**Arm length change:** None detected — arm proportions consistent across frames.

**Creator claim:** PARTIALLY CONFIRMED — there are near-identical/duplicated idle frames (F00 ≈ F03 ≈ F04) and an abrupt pose jump from strike (F02) directly to idle (F03) with no in-between. I did NOT observe incompatible frames, different perspectives, or arm-length changes. "Severe inconsistent movement" is overstated; the issue is a missing recovery intermediate plus duplicated idle holds.

---

## E) Defeat strips (terminal pose analysis)

### frontR-Defeat-composite.png (5f) — front view facing right

| Frame | Pose |
|---|---|
| 00 | Standing upright |
| 01 | Crouching, bending forward, hands near knees |
| 02 | Kneeling on both knees, torso forward, hands toward ground |
| 03 | Torso lower, head down, near ground |
| 04 (terminal, 290ms hold) | Character on ground: head very low/down, torso angled forward, appears to be on knees/hands with body collapsed forward |

**Terminal pose (F04):** Head is down low near the ground. The body appears to be on knees with torso collapsed forward — not lying fully flat/prone. At this resolution this reads as **kneeling with head down / collapsed-forward** rather than fully unconscious-and-incapacitated (which would be fully prone, body horizontal, masses spread on ground). The knees/legs still support some weight; the character is not fully flat on the ground.

### frontL-Defeat-composite.png (5f) — front view facing left

| Frame | Pose |
|---|---|
| 00 | Standing upright |
| 01 | Crouching, bending forward |
| 02 | Kneeling on both knees, torso forward |
| 03 | Torso lower, head down |
| 04 (terminal) | Character on ground: head down low, torso angled forward, on knees/hands, body collapsed forward |

**Terminal pose (F04):** Same as frontR — kneeling/collapsed-forward with head down. Not fully prone. Reads as **kneeling/defeated-but-upright-on-knees** rather than fully unconscious.

### backR-Defeat-composite.png (5f) — back view facing right — CREATOR SAYS: GOOD reference

| Frame | Pose |
|---|---|
| 00 | Standing upright, arms up slightly (startled) |
| 01 | Bending forward, collapsing |
| 02 | On knees, torso forward, head down |
| 03 | Lower, torso near ground, head down |
| 04 (terminal) | **Fully on ground — lying face-down/side, body horizontal, head down, masses (chest, hips, thighs) all on the ground** |

**Terminal pose (F04):** Character is fully prone/collapsed on the ground. Head down, body horizontal, torso/chest/hips/thighs all in contact with the ground. This reads as **fully incapacitated / unconscious / knocked out** — masses on ground, no support from knees. This is the positive reference.

### backL-Defeat-composite.png (5f) — back view facing left — CREATOR SAYS: GOOD reference

| Frame | Pose |
|---|---|
| 00 | Standing upright, arms up slightly |
| 01 | Bending forward, collapsing |
| 02 | On knees, torso forward, head down |
| 03 | Lower, near ground |
| 04 (terminal) | **Fully on ground — lying face-down/side, body horizontal, head down, masses on ground** |

**Terminal pose (F04):** Same as backR — fully prone, body horizontal, head down, masses on ground. Fully incapacitated reading.

### Section E summary
- frontR-Defeat / frontL-Defeat terminal F04: head down, body **on knees / collapsed-forward**, not fully flat. Reads as **kneeling**, NOT fully incapacitated/unconscious. **Creator claim CONFIRMED.**
- backR-Defeat / backL-Defeat terminal F04 (positive reference): body **fully prone horizontal**, head down, all masses on ground. Reads as fully unconscious/incapacitated. Confirmed as good reference.

The contrast is clear: front defeat ends kneeling-on-ground (head down but still supported by knees), back defeat ends fully prone (no knee support, body flat on ground).

---

## F) frontL-Sword-Attack-composite.png (13f)

Creator claim: small frame defect near attacking arm's ARMPIT.

frontL-Sword-Attack = front view facing left. Sword held in image-right hand (screen-right side at rest), swung across to strike toward screen-left.

| Frame | Pose | Attacking-side armpit (right side, under raised sword arm) | Notes |
|---|---|---|---|
| 00 | Idle, sword at side | Normal, arm down | Rest |
| 01 | Sword starting to lift | Normal | Wind-up start |
| 02 | Sword rising | Normal |  |
| 03 | Sword high, arm raising | Under raised arm — visible, no obvious hole | Armpit region present |
| 04 | Sword vertical overhead (peak) | Under raised arm — visible | Peak |
| 05 | Sword coming down | Normal |  |
| 06 | Sword extended forward screen-left (strike) | Arm across body, armpit closed | Strike |
| 07 | Sword extended | Normal |  |
| 08 | Sword returning | Normal |  |
| 09 | Sword returning | Normal |  |
| 10 | Sword back at side | Normal |  |
| 11 | Idle | Normal |  |
| 12 | Idle | Normal |  |

**Armpit defect check:** In frames where the attacking (right) arm is raised (F03-F05), the armpit region under the raised arm is visible and shows no obvious missing pixels, hole, or overlap error at this resolution. The arm meets the torso cleanly.
**Creator claim:** NOT_CONFIRMED — no armpit defect (missing pixels/hole/overlap) visible in any frame of frontL-Sword-Attack at this resolution. The armpit area in frames F03-F05 appears intact.

Note: at 256x256 per frame with a small character, sub-pixel armpit defects may exist but are not resolvable here.

---

## G) frontR-Walk 16f / frontL-Walk 16f

Creator claim: minor inconsistent shading in clothing hanging BETWEEN the legs; folds/shading jump without leg motion reason.

The cloth region between the legs (front skirt/tunic panel) was compared across frames in both strips.

### frontR-Walk-composite.png (16f)
The cloth between the legs moves with the leg stride in a walk pattern. At this resolution, the shading/folds of the between-legs cloth shift consistently with leg motion across the 16 frames. No frame shows a fold/shading jump that is unexplained by leg position. Specific frames with shading jumps NOT identified.

### frontL-Walk-composite.png (16f)
Same observation — between-legs cloth shading tracks leg motion through the 16-frame walk loop. No unexplained shading/fold jump identified at this resolution.

**Creator claim:** NOT_CONFIRMED — no inconsistent shading/fold jump in the between-legs cloth was detectable in either front walk strip at this resolution. The 16-frame resolution and small character size make subtle shading inconsistencies in that region unresolvable here.

---

## Cross-cutting summary of confirmed / refuted creator findings

| # | Creator finding | Strip(s) | Verdict | Evidence |
|---|---|---|---|---|
| 1 | Left arm flickers/disappears | backR-Walk, backL-Walk | NOT_CONFIRMED | Both arms present & attached in all frames; only pose changes (backR F03, backL F02 left arm raised) |
| 2 | Opposite arm fades/disappears F03-04 | frontR-Unarmed, frontL-Unarmed | NOT_CONFIRMED | Opposite arm visible at hip/side in F03-04 of both |
| 3 | Striking fist disappears | backR-Unarmed | NOT_CONFIRMED | Fist visible in all frames 00-04 |
| 4 | Severe inconsistent movement / duplicated frames | backL-Unarmed | PARTIALLY CONFIRMED | F00≈F03≈F04 near-identical idle; abrupt jump F02(strike)→F03(idle) with no intermediate. No perspective/arm-length defects seen. |
| 5 | Front Defeat terminal = kneeling not incapacitated | frontR-Defeat, frontL-Defeat | CONFIRMED | Terminal F04: head down, on knees/collapsed-forward, not fully prone |
| 6 | Back Defeat terminal = good reference (masses on ground, head down) | backR-Defeat, backL-Defeat | CONFIRMED | Terminal F04: fully prone horizontal, head down, all masses on ground |
| 7 | Armpit defect on attacking arm | frontL-Sword-Attack | NOT_CONFIRMED | Armpit region intact in frames F03-F05 where arm raised |
| 8 | Between-legs cloth shading jumps | frontR-Walk, frontL-Walk | NOT_CONFIRMED | Cloth shading tracks leg motion; no unexplained jump detectable |

**Biggest confirmed visual problem:** backL-Unarmed has duplicated idle holds (F00≈F03≈F04) and an abrupt snap from strike (F02) straight to idle (F03) with no recovery intermediate. Secondary: front Defeat terminal pose reads as kneeling rather than fully incapacitated, unlike the back Defeat positive reference.

**Files inspected:** all 14 composite strips listed above under tmp/rear-inspect/. No body-layer comparison performed for Round 2 (composite-only inspection per instructions).
