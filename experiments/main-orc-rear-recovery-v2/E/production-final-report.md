# Production final report — `main-orc-rear-recovery-v2`

**Generated:** 2026-10-26T23:21:53Z  
**Canonical matrix:** `characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json`  
**Generation ledger:** `experiments/main-orc-rear-recovery-v2/cost-provenance-ledger.json`  
**Candidate state:** `TECHNICALLY_COMPLETE` for current local package; `VISUAL_REVIEW_REQUIRED`; `PENDING_CREATOR`.  
**Independent Argon QA:** `NOT_STARTED`.  
**Runtime:** `runtimeImplemented: false`.

## Matrix result

The canonical 28-cell matrix has 12 affected candidate cells and 16 protected aliases. Counts are recomputed from the cell statuses:

| `cells.status` | Count |
|---|---:|
| `ACTIVE_CANDIDATE` | 12 |
| `ARTISTIC_REVISION_REQUIRED` | 0 |
| `IN_PRODUCTION` | 0 |
| `UNCHANGED_ALIAS` | 16 |

Root review decisions remain in `reviewStatus`, never in the production status field. The internally reviewed rear weapon candidates are:

| Cell | Canonical source | Internal review state |
|---|---|---|
| `back_r/Sword` | `characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json` | `PASS_FOR_INTERNAL_EXPANSION` |
| `back_l/Sword` | `characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/clip.json` | `PASS_FOR_INTERNAL_EXPANSION` |
| `back_r/Axe` | `characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/clip.json` | `PASS_FOR_INTERNAL_EXPANSION` |
| `back_l/Axe` | `characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/clip.json` | `PASS_FOR_INTERNAL_INTEGRATION` |

The two front Unarmed cells have localized F02 candidates and `PASS_FOR_INTERNAL_INTEGRATION`; front Defeat and the rear Walk/Unarmed candidates remain among the other six active candidates. Exact preserved aliases remain linked to `complete-v1` at baseline build `b178422e1f7fc19f068c`. No candidate has creator approval. Final integrated Argon QA remains outstanding.

## Rear weapon source and export proof

All four weapon representatives use independent `weaponBack`, `body`, `weaponFront`, and `handFront` layers. Their 256×256 composite masters, separate body-only masters, and native 128×128 body masters are saved under `characters/orc-v1/source/aseprite/rear-recovery-v2/`. Final PNGs were re-exported from saved Aseprite masters. The read-only verifier confirms, for each 8-frame clip:

- Four-layer alpha-over composition equals the exported composite pixels.
- Body-only master equals the composite's body layer.
- Native 128×128 frames equal the centered crop of the 256×256 body layer; weapon pixels do not enter native/body exports.
- Weapon pixels are limited to attack frames 01–06, and hand-front pixels exist at the grip frames.
- Clip frame hashes, master timings, independent weapon source hash, and generated-source provenance match metadata.
- GIF frame delays match the source at 1×, 0.75×, and 0.5×.

Each representative is 8 frames at `[90,80,90,80,100,80,100,110] ms` (730 ms). The resulting playback durations are 730 ms, 980 ms, and 1460 ms respectively. The existing root-owned actual 1× browser playback evidence remains the visual checkpoint evidence: SwordR `diagnosis/root-representative-playback.json`; SwordL/AxeR `diagnosis/root-clean-armed-playback-0..8.png` and JSON; AxeL `diagnosis/root-axeL-final-playback.json` and screenshots 0–9. Root's AxeL checkpoint specifically recorded the coherent overhead preparation, downward chop, lowered follow-through, recovery, visible closed fist, and preserved NW body view. It is an internal review only.

AxeL provenance is tied to final job `5296ac98-b253-4133-8468-155f7e90c68e`, asset `42cb4114-2fe0-5310-a3e7-79b640105256`, and raw frames `experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l_axe/00.png` through `06.png`. The local repair and source hashes are recorded in `experiments/main-orc-rear-recovery-v2/axeL-local-repair-provenance.json`. Same-view SwordL arm/hand pixels were adapted locally in Aseprite only for AxeL frames 01–02; the AxeL torso, legs, armor, NW perspective, and lighting were preserved. Generated opposite-side axe pixels, detached shaft, and a confirmed 27-pixel old-arm component were removed with localized masks. Raw generated files were preserved unchanged. Root reviewed the resulting body-only sequence, full composite, grip closeups, and 1× playback.

## Front F02 and Hit evidence

The two front Unarmed candidates retain the baseline 450 ms cadence `[80,110,50,90,120] ms`. In each view, F00, F01, F03, and F04 remain pixel-identical to `complete-v1`; only F02 differs. Their 128×128 native exports match the exact center crop of the 256×256 composite frames. Read-only source evidence is reproducible with:

```powershell
node experiments/main-orc-rear-recovery-v2/verify_front_f02_and_protected_frames.mjs
```

Root's bounded real-`requestAnimationFrame` Hit assessment is preserved in `experiments/main-orc-rear-recovery-v2/root-hit-playback-assessment.md` and `diagnosis/root-hit-playback.json`. It inspected all four directions at 1×, 0.75×, and 0.5× using native 128px and approximate 64px displays, and recommends retaining the existing pixels and 450 ms timing for creator review. This does not validate runtime timing or actual Unity camera scale.

## Generation accounting and authorization history

The ledger sums actual charged receipts to **78 generations across 17 jobs**. The authorization history is kept explicit:

1. Original session cap: **66** generations.
2. Job `31e61c4b-39ea-4932-9024-07dc9639f4f7` charged **3** before explicit Root approval; it was executed while the proposal was still `BOUNDED_ROOT_PROPOSAL`. This is an authorization deviation, taking actual usage to 69. It is not represented as pre-approved.
3. Root later authorized two jobs, 3 generations each (SwordL and AxeR), then one final job, 3 generations (AxeL), reaching **78** actual.
4. Current additional generation authorization: **0**. No further paid call was made for this work.

The ledger retains the original 66 cap and the deviation record. `summary.totalConsumedGenerations` and `actualTotalConsumedGenerations` are 78; `actualJobCount` is 17; all 17 job charges sum to 78. The stored 1418.70 account-balance observation belongs to the earlier 69-generation checkpoint, not the final 78-generation balance.

## Verification run for this final state

| Check | Result |
|---|---|
| `node experiments/main-orc-rear-recovery-v2/verify_new_representatives.mjs --check` | PASS, read-only; all four rear weapon clips, saved masters, exact composition/native crop, metadata hashes, and three GIF scales |
| `node experiments/main-orc-rear-recovery-v2/verify_front_f02_and_protected_frames.mjs` | PASS, read-only; 10 front frames, eight unchanged frames, two localized F02 frames, both 450 ms timings, masters, hashes, and native crops |
| Direct canonical matrix recount and path existence check | PASS; 12 affected clip JSON paths exist, 12 active, 16 aliases, 28 total |
| Generation ledger receipt recount | PASS; 17 jobs, charges sum to 78; 66 cap and 3 early-execution deviation retained |
| `verify_baseline_protection.py` using the supplied Python runtime | Ran; reports one mismatch against its saved snapshot: `config/artistic-quality-gates-v1.json` (792 of 793 snapshot hashes match). The snapshot was left unchanged. |
| Root independent preservation evidence | `root-final-preservation.json` reports `PASS`, checks 793 baseline files and 73 masters, and confirms all eight front Defeat stages 00–03 (both views) preserved. It records the same config file in `changedBaselineEntries`; this is disclosed here, not treated as an art-source change. |

Knowledge DEV2046's `E/validate_candidate_manifest.mjs` and its test remain outside this author's edits. No Unity files, production equipment pointer, baseline character art, or weapon art were edited for this report. The existing protection snapshot and config file were not edited here. No creator approval or independent QA result is claimed.
