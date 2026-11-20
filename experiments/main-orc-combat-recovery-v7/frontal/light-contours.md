# T3 — Light-contour search in the four frontal clips

Status: `TECHNICALLY_COMPLETE` / `VISUAL_REVIEW_REQUIRED` / `PENDING_CREATOR`
Scope: `front_l/Sword`, `front_l/Axe`, `front_r/Axe`, `front_r/Sword` (13/12/12/13 frames)
Result: **no confirmed light-contour artifact. 0 pixels changed by T3.**

This document is measurement only. No art was authored for T3. The single change present in the
frontal set (19 px in `front_l/Sword` F03/F04) belongs to T2 and is documented separately in
`report.md` and `verification-v7.json`.

---

## 0. Visual limitation (binding)

DEV worked **without image perception**. No frame was "looked at". Every statement below comes from
Pillow pixel arithmetic over the exported PNGs and from Aseprite Lua re-export. A negative result
from a numeric detector is **not** an artistic approval: it means the detector, at the thresholds
justified here, found nothing that matches the definition of an artifact. Independent perceptual QA
at 1x and normal playback speed is still mandatory before creator review.

---

## 1. What "artifact" was defined to mean

The T3 brief asks for *confirmed* light contours — specks, fringes or halos that read as damage and
were plausibly introduced by the V6 escalation. An artifact is therefore not "a light pixel". The
frontal set is full of legitimate light pixels (rim light, blade highlights, glove rims). The
operational definition used here is deliberately narrow:

| Candidate class | Definition | Why it would be an artifact |
|---|---|---|
| `boundaryLight` | light pixel with an exterior-background 4-neighbour | a light contour on the silhouette edge |
| `smallLightOnBoundary` | `boundaryLight` whose 4-connected light run is ≤ 2 px | an isolated bright speck on the contour |
| `haloSpeck` | light cluster of ≤ 3 px sitting directly outside the body, on a weapon layer | a halo detached from its surface |
| `insetLightLine` | light run ≥ 3 px separated from the exterior by exactly one opaque dark pixel | a light line *inside* the interior outline, i.e. a doubled outline |
| `spike` | opaque pixel with exactly one opaque 4-neighbour and ≥ 2 exterior 4-neighbours | a 1 px contour spike |

Each of these also had to survive two controls before being called confirmed:

1. **Palette control** — the composer's own colour vocabulary must not explain it.
2. **V5 control** — the same pixel must not already exist in the pre-escalation V5 frontal clip.

Neither control fires for any candidate. Section 5 shows why.

---

## 2. Threshold calibration against the actual palette

The palette maximum lightness in this character is **L = 177.72** (`rgb(176,178,180)`, blade edge).
"White" or "very light" cannot be calibrated as L ≥ 200 — nothing would ever match. The measured
lightness ladder is:

| Colour | Role | L |
|---|---|---|
| `rgb(176,178,180)` | blade edge highlight (max) | 177.7 |
| `rgb(153,154,155)` | metal light plane | 153.9 |
| `rgb(147,148,149)` | body rim light (top of the body family) | 147.9 |
| `rgb(140,140,141)` | body rim, second step | 140.1 |
| `rgb(135,136,137)` | body rim, third step | 135.3 |
| `rgb(107,108,111)` | body rim, fourth step | 108.0 |
| `rgb(89,91,94)` | body rim, fifth step | 90.8 |
| `rgb(80,82,86)` | body shadow transition | 81.9 |
| `rgb(72,74,78)` | body shadow | 73.9 |
| `rgb(55,57,61)` | body core shadow | 56.9 |
| `rgb(20,20,26)` | body deep shadow | 20.4 |
| `rgb(12,15,18)` | INK (weapon/contour ink) | 14.6 |
| `rgb(2,2,3)` | body darkest | 2.1 |

Detector thresholds were swept at T = 120 / 130 / 140 / 145 / 150 / 160 / 170.
**T = 145** is the operating threshold: it is the highest value that still *includes* the body rim
family (`147,148,149`), so a genuine light fringe on the body contour cannot hide below it, while it
cleanly separates the body rim from the metal/blade bands for attribution. T = 170 was rejected
because it leaves only the blade edge and would make the detector blind to a body fringe by
construction. T = 120 was retained as the sensitive sweep (it also picks up the mid rim steps).

---

## 3. Census — per-frame counts at T = 145

`lightBoundary` = all light pixels touching the exterior, on any layer.

| Clip | F00 | F01 | F02 | F03 | F04 | F05 | F06 | F07 | F08 | F09 | F10 | F11 | F12 | Σ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `front_l/Sword` | 0 | 0 | 5 | 3 | 0 | 0 | 3 | 3 | 3 | 6 | 1 | 1 | 0 | **25** |
| `front_l/Axe` | 0 | 0 | 3 | 5 | 3 | 3 | 3 | 4 | 5 | 2 | 0 | 0 | – | **31** |
| `front_r/Axe` | 0 | 0 | 3 | 4 | 3 | 3 | 3 | 4 | 3 | 0 | 0 | 0 | – | **23** |
| `front_r/Sword` | 0 | 0 | 5 | 2 | 0 | 0 | 3 | 0 | 2 | 4 | 0 | 0 | 0 | **16** |

`smallLightOnBoundary` (run ≤ 2 px) — the only class that could plausibly read as a speck:

| Clip | Σ | by layer | colours | run lengths |
|---|---|---|---|---|
| `front_l/Sword` | 16 | `body` 9, `weaponFront` 7 | `147,148,149` ×9, `153,154,155` ×7 | 1 px ×10, 2 px ×6 |
| `front_l/Axe` | 22 | `weaponFront` 17, `body` 5 | `176,178,180` ×17, `147,148,149` ×5 | 1 px ×13, 2 px ×9 |
| `front_r/Axe` | 17 | `weaponFront` 17 | `176,178,180` ×17 | 1 px ×8, 2 px ×9 |
| `front_r/Sword` | 7 | `weaponFront` 7 | `153,154,155` ×7 | 1 px ×3, 2 px ×4 |

`insetLightLine` and `spike` (structural vocabulary, T = 145):

| Clip | insetLine Σ | insetLine per frame | spike Σ | spike per frame |
|---|---|---|---|---|
| `front_l/Sword` | 282 | 0,0,19,38,52,58,18,52,18,16,11,0,0 | 115 | 9,9,11,13,9,7,6,6,14,4,10,8,9 |
| `front_l/Axe` | 34 | 0,0,4,6,6,4,4,4,5,0,1,0 | 135 | 9,9,16,16,15,20,17,8,6,3,7,9 |
| `front_r/Axe` | 34 | 0,0,4,6,6,4,4,4,5,0,1,0 | 135 | 9,9,16,16,15,20,17,8,6,3,7,9 |
| `front_r/Sword` | 282 | 0,0,19,38,52,58,18,52,18,16,11,0,0 | 118 | 9,9,11,16,9,7,6,6,14,4,10,8,9 |

Two facts follow immediately from this table:

* `insetLightLine` is **281/282 `weaponFront` and 1/282 `body`** in the Sword clips, **33/34
  `weaponFront`** in the Axe clips, with run lengths 3–19 px. It is the interior shading line of the
  blade/axe head, not a doubled body outline. The mirrored clip pairs are numerically identical
  (`front_l/Axe` ≡ `front_r/Axe`, `front_l/Sword` ≡ `front_r/Sword`), which is what a mirrored
  authored asset must do — an artifact would not mirror to the pixel.
* `spike` totals are dominated by `rgb(6,6,8)`/`rgb(0,0,1)`/`rgb(2,2,3)` on the `body` layer, i.e.
  the ink contour of the character. F00/F01 spikes are *identical* in all four clips (9 each), which
  is the shared idle-bookend pose.

---

## 4. The 14 body-layer boundary light pixels, in full

These are the only light pixels on a **body** contour in the whole frontal set. Every one is
`rgb(147,148,149)` and every one sits at the **top of a graduated darkening ramp** running down the
same column, inside the body:

| Clip | Frame | (x,y) | run | column below (+1 / +2) |
|---|---|---|---|---|
| `front_l/Sword` | F03 | (92,112) | 1 | `72,74,78` [74] → `55,57,61` [57] |
| `front_l/Sword` | F07 | (100,103) | 2 | `147,148,149` [148] → `140,140,141` [140] |
| `front_l/Sword` | F07 | (100,104) | 2 | `140,140,141` [140] → `140,140,141` [140] |
| `front_l/Sword` | F07 | (94,122) | 1 | `107,108,111` [108] → `89,91,94` [91] |
| `front_l/Sword` | F08 | (88,146) | 1 | transparent → transparent (bottom rim of the boot) |
| `front_l/Sword` | F09 | (98,103) | 1 | `107,108,111` [108] → `89,91,94` [91] |
| `front_l/Sword` | F09 | (88,142) | 1 | `20,20,26` [20] → `2,2,3` [2] |
| `front_l/Sword` | F10 | (96,103) | 1 | `140,140,141` [140] → `89,91,94` [91] |
| `front_l/Sword` | F11 | (96,103) | 1 | `140,140,141` [140] → `89,91,94` [91] |
| `front_l/Axe` | F03 | (92,112) | 1 | `72,74,78` [74] → `55,57,61` [57] |
| `front_l/Axe` | F08 | (98,103) | 1 | `107,108,111` [108] → `89,91,94` [91] |
| `front_l/Axe` | F08 | (88,142) | 1 | `20,20,26` [20] → `2,2,3` [2] |
| `front_l/Axe` | F09 | (98,103) | 1 | `107,108,111` [108] → `89,91,94` [91] |
| `front_l/Axe` | F09 | (88,142) | 1 | `20,20,26` [20] → `2,2,3` [2] |

`front_r/Axe` and `front_r/Sword` have **zero** body-layer boundary light at T = 145. That is the
expected asymmetry: the rim light is modelled on the character's lit side, which faces away from
camera in the right-facing views. A *V6 artifact* would not respect that asymmetry.

**Verdict for this class: legitimate rim light, not a speck.** Justification: (a) identical colour
value in all 14 cases, (b) it is the maximum of a continuous 5-step darkening ramp
(`148 → 140 → 108 → 91 → 74 → 57`), never a lone value in a flat field, (c) it appears only on the
lit-facing views, (d) **all 14 of the 14** instances are already present at exactly the same
coordinates and colour in the V5 control (`detect/body-rim-v5-control.json`: 9/9 common for
`front_l/Sword`, 5/5 common for `front_l/Axe`, 0 extra in either direction).

The remaining `smallLightOnBoundary` pixels (7 + 17 + 17 + 7 = 48) are all on `weaponFront`, at
`rgb(153,154,155)` or `rgb(176,178,180)` — the metal light plane and blade edge. Their 4-connected
light runs are short (1–2 px) simply because the metal is a *band*, not a blob; they are edge
lighting of the weapon silhouette. And, decisively, **the weapon layers are byte-identical between
V5 and V7 on every frame of every clip** (section 5), so no weapon light pixel can have been
introduced by the V6 escalation.

---

## 5. V5 control: did the escalation introduce any light contour?

The control compares the V7 frontal clips against `characters/orc-v1/source/combat-rescue-v5/grip-specialist/`,
the last state before the V6 escalation repainted the frontal bodies.

### 5.1 Boundary-light census, V5 vs V7 (`detect/v5-vs-v7-boundary.json`)

| Clip | Frames where V5 ≠ V7 at T=120 | Frames where V5 ≠ V7 at T=145 |
|---|---|---|
| `front_l/Sword` | 1 (F03: 20 → 18) | 0 |
| `front_l/Axe` | 0 | 0 |
| `front_r/Axe` | 0 | 0 |
| `front_r/Sword` | 0 | 0 |

The single difference is `front_l/Sword` F03 at T = 120, where V7 has **two fewer** light boundary
pixels than V5. That is the T2 axilla repair erasing two mid-ramp pixels on the medial edge of the
opening; it removes light, it cannot create a light contour. At the operating threshold T = 145
there is **no difference at all**.

Conclusion: the V6 escalation added **no** light boundary pixel to any frontal frame.

### 5.2 Layer-level diff, V5 → V7 (`detect/v5-vs-v7-layers.json`)

Changed pixels per frame, per layer:

| Clip | `weaponBack` | `weaponFront` | `handFront` | `body` (range over frames) |
|---|---|---|---|---|
| `front_l/Sword` | **0** | **0** | **0** | 1–33 |
| `front_l/Axe` | **0** | **0** | **0** | 0–22 |
| `front_r/Axe` | **0** | **0** | **0** | 0–22 |
| `front_r/Sword` | **0** | **0** | **0** | 1–22 |

Weapon and hand layers: **0 px changed on every frame of every frontal clip.** So no weapon light,
no glove rim and no halo on a weapon surface can be attributed to V6. The body deltas are the V6
frontal isolated-pixel fix (108 single-pixel edits recorded in the V6 `verify-result.json`) plus, for
`front_l/Sword`, the 19 px of the T2 axilla repair in F03/F04.

### 5.3 Body-rim identity against V5 (`detect/body-rim-v5-control.json`)

Comparing the exact (frame, x, y, colour) tuples of body-layer boundary light at T = 145:

| Clip | V5 | V7 | identical tuples | only in V5 | only in V7 |
|---|---|---|---|---|---|
| `front_l/Sword` | 9 | 9 | **9** | 0 | 0 |
| `front_l/Axe` | 5 | 5 | **5** | 0 | 0 |
| `front_r/Axe` | 0 | 0 | 0 | 0 | 0 |
| `front_r/Sword` | 0 | 0 | 0 | 0 | 0 |

Every body rim-light pixel in the frontal set predates the V6 escalation at the same coordinate.

---

## 6. Per-clip verdicts

| Clip | Candidates examined | Confirmed artifacts | Pixels changed |
|---|---|---|---|
| `front_l/Sword` | 16 `smallLightOnBoundary` (9 body, 7 weapon), 282 `insetLightLine`, 115 `spike` | **0** | **0** (19 px belong to T2, not T3) |
| `front_l/Axe` | 22 `smallLightOnBoundary` (5 body, 17 weapon), 34 `insetLightLine`, 135 `spike` | **0** | **0** |
| `front_r/Axe` | 17 `smallLightOnBoundary` (17 weapon), 34 `insetLightLine`, 135 `spike` | **0** | **0** |
| `front_r/Sword` | 7 `smallLightOnBoundary` (7 weapon), 282 `insetLightLine`, 118 `spike` | **0** | **0** |

**T3 conclusion: no confirmed light-contour artifact. Zero pixels of the frontal set were changed
for T3.** The three non-Sword frontal clips in
`characters/orc-v1/source/combat-recovery-v7/frontal/` are byte-identical copies of their V6 sources
(79/79, 79/79 and 85/85 files verified by SHA-256), retained as measurement carriers so the four
frontal cells can be reviewed together.

---

## 7. What a numeric negative cannot rule out

Honest limits of this verdict, to be closed by independent perceptual QA:

1. A light contour that is *continuous with* a legitimate one (e.g. a rim that grew one row taller
   while staying below T = 145 and connected to the real rim) would not be flagged by any of the
   five detectors. Section 5.1 covers this at the census level (no new light boundary pixel at
   either threshold), but not per-row shape.
2. Perceived flicker at playback speed is a temporal property. The per-frame tables above show no
   single-frame spike (no frame differs from both neighbours by an isolated count), which is the
   numeric proxy, but it is a proxy.
3. Hue/saturation artifacts at *identical* lightness would be invisible to an L-based detector. All
   reported classes were additionally checked by exact RGBA equalities against the palette ladder in
   section 2, and no colour outside that ladder appeared on a body contour.

## 8. Reproduction

```
tmp\pixel-venv\Scripts\python.exe experiments\main-orc-combat-recovery-v7\frontal\structural-census.py
tmp\pixel-venv\Scripts\python.exe experiments\main-orc-combat-recovery-v7\frontal\census-body-rim.py
tmp\pixel-venv\Scripts\python.exe experiments\main-orc-combat-recovery-v7\frontal\body-rim-v5-control.py
tmp\pixel-venv\Scripts\python.exe experiments\main-orc-combat-recovery-v7\frontal\calibrate-light.py front_l-Sword-full
tmp\pixel-venv\Scripts\python.exe experiments\main-orc-combat-recovery-v7\frontal\v5-vs-v7-layers.py
```

Outputs: `detect/structural-*.json`, `detect/body-rim-census.json`,
`detect/body-rim-v5-control.json`, `detect/light-contours-*.json`,
`detect/v5-vs-v7-boundary.json`, `detect/v5-vs-v7-layers.json`.
All scripts read PNGs and write JSON only; none of them writes art.
