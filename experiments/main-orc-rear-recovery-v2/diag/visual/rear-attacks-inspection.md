# Rear Attacks Visual Inspection — TacticsRPG CharacterFactory

**Scope:** 8 contact-sheet strips (256x256 per frame, leftmost = frame 00), 4 attacks x 2 layers (composite = full render with weapon; body = body-only, weapon hidden).
- backR-Sword (composite + body)
- backL-Sword (composite + body)
- backR-Axe (composite + body)
- backL-Axe (composite + body)

**Method:** read-only visual inspection of rendered strips at native resolution. No editing, no PixelLab, no Unity. Where resolution prevents certainty, that is stated explicitly.

---

## STEP 0 — Vision self-test

File: `tmp/vision-test.png` (16x16 quadrant pattern).

| Quadrant | Color |
|---|---|
| Top-left | Red |
| Top-right | Green |
| Bottom-left | Blue |
| Bottom-right | Yellow |
| Exact center (1 pixel) | Black |

Self-test: **PASSED**. Vision is functional; no guessing required below.

---

## 1. backR-Sword — right-facing back swing, sword

Composite = `backR-Sword-composite.png`; body = `backR-Sword-body.png`.

### Frame-by-frame

| Frame | Body posture (torso/shoulders/arms) | Weapon (visible? grasp? floating?) | Bright edge artifacts | Notes |
|---|---|---|---|---|
| 00 | Idle: arms at sides, torso upright facing back. Clean, no anomalies. | Weapon not visible (held/down at side, out of frame or sheathed). | None seen. | Rest pose. |
| 01 | Right arm bent and raised behind head (wind-up). Left arm stays at side. | Visible: sword held up behind right shoulder, blade pointing up. Hand appears to contact handle but glove-to-handle wrap is **not clearly resolved** at this resolution; may read as pasted/floating at the grip. | None clearly on body silhouette; highest-risk area is the weapon grip junction (unresolved). | Anticipation begins. |
| 02 | Right arm extended straight upward, elbow near vertical above head (peak of wind-up). Left arm at side. | Visible: sword vertical behind head, highest point. Grappling still ambiguous (same caveat as 01). | None clearly on body. | Peak anticipation. |
| 03 | Essentially identical to 02: right arm straight up overhead. | Visible: sword vertical overhead. | None clearly on body. | Holds peak; no angle reversal here. |
| 04 | Right arm swings forward and down, extended toward the right side of screen (strike). Left arm at side. | Visible: sword extended forward/down to the right. The extended weapon arm **looks pasted/floating** — the hand-to-blade connection and handle grasp are not clearly rendered; abrupt angle change from vertical (03) to horizontal-down (04). | Possible pale border along the outer (right) edge of the extended right forearm — **unresolved at this resolution** (could be intended metal highlight vs stray bright pixel). | Strike; first clear coherence risk. |
| 05 | Right arm further extended down-right (follow-through). | Visible: sword angled down-right, away from body. Same floating/pasted grip ambiguity. | Same possible pale border on extended forearm edge (unresolved). | Follow-through. |
| 06 | Right arm returning down by side; sword angling down toward hip. | Visible: sword down by side/hip, mostly hidden behind body. | None clearly on body. | Recovery beginning. |
| 07 | Back to idle: arms at sides, torso upright. | Weapon not visible. | None. | Recovery complete. |

### Overall coherence
Reads as a largely coherent swing: idle -> anticipation (01-03) -> strike (04-05) -> recovery (06-07). No limb disappearance or duplication detected; left arm stable throughout; no old-geometry remnant.

**Weakest frames:** 04 and 05 — the weapon looks pasted/floating rather than grasped, the angle reverses abruptly from vertical (03) to horizontal-down (04), and there is a suspected (unresolved) pale border on the extended forearm edge.

---

## 2. backL-Sword — left-facing back swing, sword

Composite = `backL-Sword-composite.png`; body = `backL-Sword-body.png`.

### Frame-by-frame

| Frame | Body posture | Weapon | Bright edge artifacts | Notes |
|---|---|---|---|---|
| 00 | Idle: arms at sides. Clean. | Not visible. | None. | Rest. |
| 01 | **Right arm already extended forward/left** (toward screen left), fully outstretched — NOT a wind-up. Left arm at side. | Visible: sword already extended horizontally to the left at strike distance. Grasp ambiguous (pasted/floating possible). | None clearly on body; grip junction unresolved. | **Structure problem:** this looks like the strike position, not anticipation. No draw-back phase visible. |
| 02 | Right arm raised straight overhead (peak). | Visible: sword vertical overhead behind head. | None clearly on body. | Goes from extended-left (01) straight to overhead (02) — non-linear path. |
| 03 | Right arm straight overhead, same as 02. | Visible: sword vertical overhead. | None clearly on body. | Holds peak. |
| 04 | Right arm extended forward/left again. | Visible: sword extended down-left. | None clearly on body; grip unresolved. | Second extension to the left — redundant with 01. |
| 05 | Right arm extended down-left, arm lowering. | Visible: sword angled down-left away from body. | None clearly on body. | Follow-through-ish. |
| 06 | Right arm down by side; sword at hip/hidden. | Visible (barely): sword at side. | None. | Recovery. |
| 07 | Idle: arms at sides. | Not visible. | None. | Rest. |

### Overall coherence
**Does NOT read as a clean anticipation -> strike -> follow-through.** Frame 01 already shows the arm/weapon fully extended forward (left), then 02-03 snap to overhead, then 04-05 extend left again. The expected anticipation (weapon drawn back behind the right shoulder, as seen cleanly in backR-Sword) is missing or mis-sequenced; the limb teleports from side (00) to full extension (01), then reverses up to overhead, then back down-left.

**Weakest frames:** 01 (wrong pose — already at strike extension instead of wind-up) and 02 (abrupt snap from extended-left to overhead with no in-between). This is the clearest structural defect across all 8 strips.

**Body integrity:** no limb disappearance, duplication, or detached-geometry remnant detected; left arm stable; right arm remains connected. The issue is sequencing/pose choice, not broken geometry.

---

## 3. backR-Axe — right-facing back swing, axe

Composite = `backR-Axe-composite.png`; body = `backR-Axe-body.png`.

### Frame-by-frame

| Frame | Body posture | Weapon | Bright edge artifacts | Notes |
|---|---|---|---|---|
| 00 | Idle: arms at sides. Clean. | Not visible. | None. | Rest. |
| 01 | Right arm bent, raised behind right shoulder/head (wind-up). Left arm at side. | Visible: axe head up behind right shoulder. Grasp ambiguous (painted-on look possible; glove wrap not resolved). | None clearly on body. | Clean anticipation. |
| 02 | Right arm straight up overhead (peak). | Visible: axe vertical overhead, blade up. | None clearly on body. | Peak. |
| 03 | Right arm straight up overhead, same as 02. | Visible: axe vertical overhead. | None clearly on body. | Holds peak; no reversal. |
| 04 | Right arm extended forward/right (strike). | Visible: axe extended forward/down to the right. Handle-to-head connection looks **pasted/floating** — no clear glove wrap on the haft; abrupt angle reversal from vertical (03) to horizontal-down (04). | Possible pale border on outer edge of extended right forearm — unresolved (highlight vs artifact). | Strike; coherence risk. |
| 05 | Right arm extended down-right (follow-through). | Visible: axe angled down-right. Same floating/pasted haft ambiguity. | Same suspected pale border on forearm edge (unresolved). | Follow-through. |
| 06 | Right arm returning to side; axe down at hip. | Visible: axe down by side. | None. | Recovery. |
| 07 | Idle: arms at sides. | Not visible. | None. | Rest. |

### Overall coherence
Reads as a coherent swing: idle -> anticipation (01-03) -> strike (04-05) -> recovery (06-07). Body geometry intact; no limb detachment/duplication; left arm stable.

**Weakest frames:** 04 and 05 — axe looks pasted/floating (haft not visibly grasped), abrupt angle reversal from vertical to horizontal-down, suspected (unresolved) pale border on extended forearm.

---

## 4. backL-Axe — left-facing back swing, axe

Composite = `backL-Axe-composite.png`; body = `backL-Axe-body.png`.

### Frame-by-frame

| Frame | Body posture | Weapon | Bright edge artifacts | Notes |
|---|---|---|---|---|
| 00 | Idle: arms at sides. Clean. | Not visible. | None. | Rest. |
| 01 | **Right arm already extended forward/left**, fully outstretched — not a wind-up. Left arm at side. | Visible: axe already extended horizontally to the left. Haft grasp ambiguous / pasted look. | None clearly on body. | **Structure problem:** strike position used where anticipation should be (mirrors backL-Sword). |
| 02 | Right arm raised straight overhead (peak). | Visible: axe vertical overhead. | None clearly on body. | Snap from extended-left (01) to overhead (02) — non-linear. |
| 03 | Right arm straight overhead, same as 02. | Visible: axe vertical overhead. | None clearly on body. | Holds peak. |
| 04 | Right arm extended forward/left again. | Visible: axe extended down-left. | None clearly on body. | Redundant second extension to the left. |
| 05 | Right arm extended down-left, lowering. | Visible: axe angled down-left away from body. | None clearly on body. | Follow-through-ish. |
| 06 | Right arm down by side; axe at hip/hidden. | Visible (barely): axe at side. | None. | Recovery. |
| 07 | Idle: arms at sides. | Not visible. | None. | Rest. |

### Overall coherence
Same defect as backL-Sword: **no clean anticipation -> strike flow.** Frame 01 already at full forward extension, then 02-03 snap to overhead, then 04-05 extend left again. The draw-back/wind-up behind the shoulder (present in the backR equivalents) is missing.

**Weakest frames:** 01 (already at strike extension instead of wind-up) and 02 (abrupt snap extended-left -> overhead).

**Body integrity:** no limb disappearance, duplication, or detached-geometry remnant detected; left arm stable; right arm stays connected. Defect is sequencing/pose, not broken geometry.

---

## Cross-cutting findings

### Bright edge artifacts (c)
No definitive pale/white/bright unwanted borders on the body silhouette were confirmed at this resolution in any of the 8 strips. The only candidates are:
- A possible pale border along the outer edge of the extended right forearm in backR-Sword (frames 04-05) and backR-Axe (frames 04-05) — **unresolved**: could be intended metal highlight rather than stray bright pixel.
- Weapon grip/haft junctions in all extended frames (04-05 of every attack) — **unresolved** whether stray bright pixels exist at the hand-weapon seam.

Recommendation: pixel-level diff of composite vs body for frames 04-05 of each attack to confirm or rule out bright borders. Do not treat the above as confirmed artifacts.

### Weapon grasp (b)
In every attack, when the weapon is extended (frames 04-05, and 01-02 of backL attacks), the hand-to-handle connection is **not clearly resolved**: the glove does not visibly wrap the handle/haft, so the weapon can read as pasted/floating rather than grasped. This is consistent across all 4 attacks.

### Abrupt angle reversals (b)
- backR-Sword: vertical overhead (03) -> horizontal-down extended (04): abrupt.
- backR-Axe: vertical overhead (03) -> horizontal-down extended (04): abrupt.
- backL-Sword / backL-Axe: extended-left (01) -> overhead (02) -> extended-left (04): non-linear, two reversals.

### Body posture (a)
No limb disappearance, hand shape change, detachment, duplication, or old-geometry remnant detected in any frame of any attack. The left arm remains at the side in all frames; the right arm stays connected to the shoulder throughout.

### Overall (d)
- **Coherent swings:** backR-Sword, backR-Axe (both follow anticipation -> peak -> strike -> follow-through -> recovery cleanly).
- **Non-coherent swings:** backL-Sword, backL-Axes (frame 01 already at strike extension; no proper anticipation; non-linear path).

### Biggest visual problems (ranked)
1. **backL-Sword and backL-Axe frame 01**: already at full forward strike extension instead of a wind-up/draw-back; breaks anticipation->strike narrative. (Clear, high confidence.)
2. **backL-Sword and backL-Axe frame 02**: abrupt snap from extended-left (01) to overhead (02) with no in-between. (Clear, high confidence.)
3. **Weapon not visibly grasped** in extended frames (04-05 of all attacks; 01-02 of backL attacks): looks pasted/floating; handle wrap unresolved. (Medium confidence at this resolution.)
4. **Suspected pale border on extended right forearm** (frames 04-05 of backR attacks): unconfirmed at this resolution; needs pixel-level composite-vs-body diff. (Low confidence; unresolved.)

### Files inspected
- tmp/rear-inspect/backR-Sword-composite.png, backR-Sword-body.png
- tmp/rear-inspect/backL-Sword-composite.png, backL-Sword-body.png
- tmp/rear-inspect/backR-Axe-composite.png, backR-Axe-body.png
- tmp/rear-inspect/backL-Axe-composite.png, backL-Axe-body.png
- tmp/vision-test.png (self-test; passed)
