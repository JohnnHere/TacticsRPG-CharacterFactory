# Independent Artistic-Recovery QA Report — `main-orc-complete-v1`

- **Date:** 2026-10-26 · **QA reviewer:** independent mandatory QA agent `cline-glm-api/glm-5.3` (did not author the recovery pass)
- **Scope:** "MAIN ORC — ARTISTIC QUALITY RECOVERY & PRODUCTION GATE IMPROVEMENT" for `orc-v1` (Orc V1 · Verde Warcraft): true reconstruction of rear views (`back_r`/`back_l`), re-choreographed `Hit` and `Defeat`, surgical removal of the frontal attack head-crown halo, Before/After review surfaces, and the artistic quality gate contract (`factory.artistic-quality-gates.v1`).
- **Build under review:** `dist/editor/orc-v1-complete-v1/b178422e1f7fc19f068c` (recovery). Supersedes `2595e12a39cc29670933`.
- **Predecessor report (not modified by this QA):** `experiments/main-orc-complete-v1/qa-final.md` — technical QA on build `72bad312d0d5c2fcee21`, verdict APPROVED (technical scope only).
- **Method:** all pixel measurements recomputed from disk with a Node measurement script (`tmp/qa-artistic-measure.mjs`; PNGs inspected only via Node — never opened as text), plus `node --test test/main-orc-complete.test.mjs`, the full test suite, `node src/cli.mjs validate --id orc-v1 --stage full`, SHA-256 recount of the protected map, `git -C ../TacticsRPG status`, and a line-level cross-check of `config/artistic-quality-gates-v1.json` ↔ `docs/ARTISTIC_QUALITY_GATES.md` ↔ `AGENTS.md`/`handoff/AGENT_CONTEXT.md`/`docs/MAIN_ORC_COMBAT_POLISH.md`/`docs/ROADMAP.md`.

---

## VERDICT (per `factory.artistic-quality-gates.v1` taxonomy — no labels outside it)

| Field | Value |
|---|---|
| `technicalStatus` | **`TECHNICALLY_COMPLETE`** |
| `artisticStatus` | **`VISUAL_REVIEW_REQUIRED`** |
| `artisticApproval` | **`PENDING_CREATOR`** |

All automated artistic-defect gates **PASS** on build `b178422e1f7fc19f068c`. Passing them does not grant artistic approval: automation cannot approve art (`automationCannotApproveArt: true`), and the package now awaits explicit creator visual inspection in the interactive studios. No Unity integration is authorized by this QA.

---

## 1. Technical Gate — `TECHNICALLY_COMPLETE` (independently re-verified this session)

| Item | Recorded claim | Independent re-verification | Result |
|---|---|---|---|
| Native validation | 749 PASS / 0 FAIL | Live run `node src/cli.mjs validate --id orc-v1 --stage full` → `{"PASS":749,"FAIL":0,"WARNING":9,"NOT_RUN":1,"REQUIRES_HUMAN_REVIEW":1}` | ✅ |
| Test suite | 17/17 tests PASS | Live run `node --test "test/*.test.mjs"` → 17 tests / 17 pass / 0 fail (incl. both `main-orc-complete` tests) | ✅ |
| Aseprite jobs / frames | 75 jobs / 599 frames | `reports/orc-v1-animation-coverage-v1.json` summary (`editorJobsVerified: 75`, `editorFramesVerified: 599`) + test assertion | ✅ |
| Protected canonical art | 525/525 files preserved | `experiments/main-orc-complete-v1/protected-art.json` has exactly 525 entries; `test/main-orc-complete.test.mjs` recomputes every SHA-256 and passes | ✅ |
| `../TacticsRPG` untouched | no Unity writes | `git -C ../TacticsRPG status --porcelain` → empty (clean tree) | ✅ |
| Coverage matrix | 28/28 cells `COMPLETE_VERIFIED` | Coverage JSON + test assertion (4 directions × 7 actions, `missingCells: 0`) | ✅ |
| Governance pointers | active v3 + entry candidate untouched | Test asserts `equipment-current.json` = `main-orc-onehanded-v3`, `equipment-entry-candidate.json` = `main-orc-onehanded-entry-v1`, `unityRepositoryModified: false`, frame-level `attack-only-v1` visibility maps (Sword `0011111111100`, Axe `001111111000` in every direction) | ✅ |

Honest accounting of the non-PASS validation entries (non-blocking, FAIL = 0): `WARNING: 9` — the predecessor technical QA had classified the 5 duplicate-class warnings as by-design (qa-final I3: static bases equal Idle frame 0, MVP static equals front_r base); the recovery build reports 9, and this QA did not individually re-classify the 4 additional ones → recorded as an open follow-up for the next technical pass. `NOT_RUN: 1` = Unity import/PlayMode (staging-only task, expected). `REQUIRES_HUMAN_REVIEW: 1` = the art check itself — exactly the gate this report feeds.

---

## 2. Directional View Gate (`directional-view-gate-v1`, applies to `back_r`/`back_l`) — PASS

| Measurable check | Gate | Measured (this session) | Result |
|---|---|---|---|
| `noFrontFacePixels` — head-zone near-white eye/tusk pixels (min(RGB) ≥ 200) | 0 in rear views | `front_r`: 12 · `front_l`: 12 · **`back_r`: 0 · `back_l`: 0** | ✅ |
| `mirrorDependence` — back_r vs horizontally flipped back_l | agreement < 97% (a pure mirror is insufficient) | **65.6% all-pixels / 6.2% opaque-pixels** | ✅ far below the mirror-copy threshold |
| Distinct rear bases vs each other | must differ | SHA-256 inequality `orc_v1_dir_back_r.png` ≠ `orc_v1_dir_back_l.png` (test-asserted) | ✅ |
| Distinct from superseded art | must differ | SHA-256 inequality for all 4 preserved pairs: `dir_back_r_before.png` / `dir_back_l_before.png` vs current bases; `front_r_defeat_strip_before.png` / `front_r_hit_strip_before.png` vs current strips (test-asserted) | ✅ |
| Head-zone bare skin (construction proxy) | rear heads must not carry the frontal face | front 207/207 px vs back 137/116 px — rear heads expose less skin, consistent with skull/nape/collar construction | ✅ (proxy) |
| `lightingSide` — highlight centroid above body centroid | all four views | above in all four (−10.7 to −19.2 px vertical offset) | ✅ |

`markerPresence` (occipital skull, nape/trapezius, rear gorget, dorsal plate with spine channel, scapula plates, rear belt without sternum peak, rear tassets, popliteal straps, angled heels) is a **human-inspection** check by contract: this QA verified the pixel proxies above, not the anatomical reading — that belongs to the creator in the studio (see §7).

---

## 3. Choreography Gate — `Hit` (`hit-impact-reaction-v1`) — PASS

5 frames, durations `45/95/115/95/100 ms` (450 ms, one-shot), bottom pinned to `groundY = 126` in every frame and direction (verified).

| Direction | Skin/bbox top excursion (gate ≥ 6 px) | Height range `max(h)−min(h)` (gate ≥ 5 px, contract definition) | Centroid displacement from frame 0 (gate ≥ 4 px) | Idle reference top excursion |
|---|---|---|---|---|
| `front_r` | **12 px** | **12 px** (heights 112/108/109/111/120) | **7.98 px** | 2 px |
| `front_l` | **12 px** | **12 px** | **7.98 px** | 2 px |
| `back_r` | **13 px** | **13 px** (heights 109/109/106/109/119) | **10.36 px** | 2 px |
| `back_l` | **12 px** | **13 px** (heights 109/109/106/109/118) | **10.89 px** | 2 px |

Head-top excursion is 6–6.5× the Idle breathing amplitude in every direction. The rejected "before" state measured a 3 px tremor with ~2 px centroid — the exact defect this gate forbids.

Transparency notes (both variants recorded, neither hides a failure):

- The measurement script also prints a stricter **rest-relative dip** (frame-0 height − minimum height): 4 px (front) / 3 px (back). The contract's gated `heightCompressionDefinition` is the clip range `max(h) − min(h)` ("Max standing height … minus minimum compressed height during impact recoil (max(h) − min(h))"), which is exactly what the test asserts and what passes at 12–13 px. Both numbers are disclosed so the creator can judge recoil depth with open eyes.
- **Motion energy** (honest finding, not a failure): raw non-time-normalized changed-pixel ratio Hit/Idle measured **1.68 / 1.69** (`front_r`/`front_l`) and **1.14 / 1.17** (`back_r`/`back_l`). The contract's `minMotionEnergyVsIdle: 2.0` is defined on a **time-normalized** rate (`changedPixelPct / frameDurationMs`); since Hit frames (45–100 ms) are 4–5× shorter than Idle frames (400–500 ms), the normalized ratio computes to roughly **5.6–8.2×** — comfortably above 2.0. However, this specific check is **not machine-enforced** in the current test suite, and the QA script emits only the raw proxy. Recorded as a verification gap to harden (add the normalized assertion to the test), and as the first number to revisit **if** rear Hit reads "soft" in the studio (§7.4).

---

## 4. Choreography Gate — `Defeat` (`defeat-collapse-v1`) — PASS

5 stages `fatal-stagger → knees-buckle → drop-to-knees → collapse-impact → terminal-defeated`, durations `70/95/115/130/290 ms` (700 ms), non-looping, terminal frame 4, bottom pinned to `groundY = 126` in every frame and direction (verified).

| Direction | Stage heights (px) | Stage widths (px) | Terminal height (gate ≥ 58) | Terminal aspect W/H (gate ≥ 1.3) | Width growth (gate ≥ 10%) | Max single-stage drop (gate ≤ 0.35) |
|---|---|---|---|---|---|---|
| `front_r` | 112, 90, 86, 63, 66 | 87, 85, 83, 88, 120 | **66** | **1.82** | **37.9%** | 0.205 |
| `front_l` | 112, 90, 86, 63, 66 | 87, 85, 83, 88, 120 | **66** | **1.82** | **37.9%** | 0.205 |
| `back_r` | 111, 91, 84, 67, 66 | 90, 83, 93, 97, 119 | **66** | **1.80** | **32.2%** | 0.18 |
| `back_l` | 111, 91, 84, 67, 66 | 90, 83, 93, 97, 119 | **66** | **1.80** | **32.2%** | 0.18 |

The forbidden pattern is gone: the rejected "before" was a standing sprite globally rotated 2D and squashed (`vScale = 0.52`) into a 21 px-high / 109 px-wide strip (width 82 → 109). The recovery keeps head/pauldron/chest volume on the ground line across a progressive 5-stage collapse, with no single transition removing more than ~20% of standing height. Front/rear pairs are choreography-consistent while remaining distinct constructions (§2).

---

## 5. Frontal Attack Head Gate (`frontal-attack-head-cleanup-v1`) — PASS

Region `y = 68..83, x = 116..149` of the 256×256 composite (green skull dome above the brow line), INK outline language `#0C0F12` (`rgb(12,15,18)`).

| Clip set | Halo pixels at min(RGB) ≥ 235 / ≥ 200 / ≥ 170 / ≥ 150 / **≥ 130** | Result |
|---|---|---|
| **8 frontal attack combinations** — `front_r`/`front_l` Sword (13 f), Axe (12 f), Unarmed (5 f each) | **0 / 0 / 0 / 0 / 0** in every frame | ✅ |
| Test-enforced boundary detector (neutral-grey 4-neighbors of green skull pixels, `|R−G| ≤ 10`, `|G−B| ≤ 16`, `R ≥ 90`) across all Sword/Axe frames × both front directions | **0** | ✅ |
| Before snapshots `rejected-before/front_r_sword_07_halo_before.png`, `…axe_05…` | 0 / 0 / 0 / 0 / **8** and **16** px at ≥ 130 | eliminated ✅ |

The light-grey crown halo present in the superseded build is gone even at a permissive threshold of 130, achieved surgically — without regenerating the clips or breaking the preserved frontal choreography (§6).

---

## 6. Complete-Set Review Contract (`complete-set-review-v1`) — PASS (surface integrity)

- **Matrix:** 4 directions × 7 actions = **28/28 cells** `COMPLETE_VERIFIED`, every clip manifest present on disk (test-asserted), all reachable from a single page in both studios.
- **Studios verified present and structurally complete** (test-asserted): `Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html` and `Biblioteca de Arte/Estudos Comparativos/Orc principal - Biblioteca completa/index.html` — Before/After section ("Comparação Visual Antes (v1 Rejeitada) vs Depois (Recuperação Artística)"), `VISUAL_REVIEW_REQUIRED` badges, and `AntesDepois/` assets (e.g. `dir_back_r_before.png`).
- **Before/After integrity:** all preserved `rejected-before/` snapshots SHA-differ from the current output (4/4 pairs test-asserted) → the captures predate the rewrite; the contract's invalid-comparison rule (a byte-identical "before") does not trigger.
- **Preserved-by-design frontal art:** `front_r` Idle and Walk remain byte-identical; frontal Sword/Axe choreography preserved with only the crown-outline cleanup (52 of 75 jobs changed; the 23 unchanged jobs are exactly the protected frontal cells, per `docs/MAIN_ORC_COMBAT_POLISH.md` evidence table).
- Honest note: whether the studio *reading* experience (one-click 28-cell matrix, step-by-frame, transitions, zoom) is pleasant and sufficient is a creator-experience judgment; structural presence is what was verified here.

---

## 7. Honest visual/artistic notes for the creator's inspection

These are observations and measurement disclosures — **not** approval, and **not** defects by themselves. Per reviewer duties, any true defect must be named with action + direction + frame range.

1. **Rear `Idle` is a symmetric 3-pose breathing loop** across 5 frames `[0, 1, 2, 1, 0]` (measured: 3/5 distinct frames in `back_r` and `back_l`, vs 5/5 distinct in `front_r`/`front_l`). Timing still follows the mandatory `idle-balanced-v1` standard exactly (400/450/500/450/400 ms = 2200 ms, ~2 px head amplitude, test-asserted in all 4 directions), so the standard is honored — but a ping-pong symmetric loop can read slightly more mechanical (pendulum) than the frontal 5-pose set. The creator should confirm in the studio that the rear breathing feels as alive as the frontal one.
2. **`back_r`/`back_l` lighting and 3/4 perspective are ready for creator visual review.** Automated proxies pass (views are constructions, not mirrors; highlights above body center). One number to eyeball: the highlight-centroid horizontal offset sits **left** of body center in `front_r` (−2.2 px), `front_l` (−0.6 px) and `back_l` (−5.5 px), but **right** of center in `back_r` (+3.8 px). The 3/4 perspective shift may fully justify it; the contract's "consistent horizontal side" wording is not numerically enforced, so this QA flags it for the creator's eye rather than failing it.
3. **Doc/measure discrepancy found (minor; the gate passes either way):** `docs/MAIN_ORC_COMBAT_POLISH.md` (honesty note 2) states ~95% mirror agreement between the rear views and highlight variance "−3.3 px to +1.0 px"; this QA measures **65.6% all-pixel / 6.2% opaque** mirror agreement and highlight offsets **−5.5 px to +3.8 px** on the current build. The QA numbers indicate the rear views are *more* distinct than the doc claims, and both figures sit far below the 97% mirror-copy threshold — but the doc figures should be corrected in a future pass to match what the current build actually measures.
4. **`Hit` rear motion-energy proxy is modest** (raw 1.14–1.17× Idle in rear views vs 1.68–1.69× frontal; §3): displacement gates all pass decisively, but if the rear Hit reaction reads "soft" next to the frontal one in the studio, the time-normalized energy check is the first number to revisit and the missing machine assertion is the first test to add.
5. **`Hit` recovery-settle (frame 4) rises above rest height** (120 px vs 112 px standing; head top 8 px above rest) after the recoil dip. Verify in the studio that this final frame reads as *settling back*, not a stretch/grow.
6. **1–2 red pixels detected in the rear head zones** (`back_r`: 1, `back_l`: 2; frontal: 0). Almost certainly armor/strap/crown accents rather than face features (near-whites are zero), but worth a glance at 100% zoom.
7. **What this QA could NOT judge** (recorded explicitly, per lesson 10): whether the reconstructed occipital skull, nape, dorsal plate with spine channel, scapula plates, rear belt and tassets *read* correctly to a human eye; silhouette readability of the collapse stages in motion; weapon-sync feel during attacks; overall identity/light coherence across the four directions at game speed. These require creator inspection — that is precisely what `VISUAL_REVIEW_REQUIRED` / `PENDING_CREATOR` mean.

---

## 8. Contract/doc consistency — verified

- `config/artistic-quality-gates-v1.json` `currentAssessment`: build `b178422e1f7fc19f068c`, superseded `2595e12a39cc29670933`, `technicalStatus: TECHNICALLY_COMPLETE`, all 7 per-action statuses `VISUAL_REVIEW_REQUIRED`, `creatorApproval: PENDING_CREATOR` — consistent with `reports/orc-v1-animation-coverage-v1.json`, `characters/orc-v1/source/equipment-complete-candidate.json` and the studios (all test-asserted).
- The recovery build hash `b178422e1f7fc19f068c` appears 10× across `AGENTS.md`, `handoff/AGENT_CONTEXT.md`, `docs/MAIN_ORC_COMBAT_POLISH.md`, `docs/ROADMAP.md`, `docs/ARTISTIC_QUALITY_GATES.md` and `config/artistic-quality-gates-v1.json`. The 5 remaining references to old hashes (`2595e12a39cc29670933`, `72bad312d0d5c2fcee21`) were inspected line-by-line: all are explicitly labeled historical / superseded / before-capture citations — no stale "current" pointers.
- `docs/ARTISTIC_QUALITY_GATES.md` §6 measured table (excursion 12–13 px, compression 12–13 px, centroid 5.74–7.55 px) matches this QA's measurements for excursion and compression; the doc's centroid figures (5.74–7.55 px, torso-band variant) and this QA's full-body variant (7.98–10.89 px) are different measurement bands over the same clips — both above the 4.0 px floor. Both are recorded here for transparency.
- Status taxonomy, blocking rule, gate ordering (`TECHNICAL_GATE → ARTISTIC_DEFECT_GATES → VISUAL_REVIEW → CREATOR_APPROVED`) and the 10 production lessons are consistent between config, doc and `AGENTS.md`.

---

## 9. Bottom line

The artistic-recovery package on build `b178422e1f7fc19f068c` is **`TECHNICALLY_COMPLETE`** (749 PASS / 0 FAIL, 17/17 tests, 75 jobs / 599 frames, 525/525 protected files byte-identical, `../TacticsRPG` untouched) and passes **every automated artistic-defect gate**: rear views are constructed and distinct (0 face whites, 6.2% opaque mirror agreement, SHA-distinct from the superseded art and from each other), `Hit` communicates measured impact (12–13 px top excursion, 12–13 px height range, 7.98–10.89 px centroid, ground-pinned), `Defeat` is a ground-pinned 5-stage volumetric collapse (terminal 66 px, aspect 1.80–1.82, width growth 32–38%, no single-stage drop above 0.205), and the frontal crown halo is eliminated (0 px down to threshold 130; before: 8–16 px) without breaking the preserved frontal choreography.

The package is presented as **`artisticStatus: VISUAL_REVIEW_REQUIRED`** with **`artisticApproval: PENDING_CREATOR`**. Next step: the creator's visual review of all 28 cells (plus the 4 static bases) in the interactive studios, using the Before/After surfaces. Any revision finding should be filed as `ARTISTIC_REVISION_REQUIRED` naming action, direction and frame range; `CREATOR_APPROVED` can be granted only by the creator. This QA grants neither.

*Housekeeping: the temporary scripts `tmp/qa-artistic-measure.mjs` and `tmp/qa-verify-main-orc-complete.mjs` were deleted after this report was written (no leftover temp scripts in `git status`); `experiments/main-orc-complete-v1/qa-final.md` was read but not modified — its historical reference to `tmp/qa-verify-main-orc-complete.mjs` (§5) now describes a deleted scratch file and is kept as-is because that report is an immutable record.*
