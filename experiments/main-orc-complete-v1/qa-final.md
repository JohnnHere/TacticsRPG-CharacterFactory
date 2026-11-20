# Independent QA Report — `main-orc-complete-v1`

- **Date:** 2026-10-25 · **QA reviewer:** independent agent (did not author the candidate)
- **Scope:** Mandatory independent QA of the complete 4-direction × 7-action animation library and Unity-ready staging package for `orc-v1` (Orc V1 · Verde Warcraft), per `experiments/main-orc-complete-v1/qa-brief.md`.
- **Build under review (after L1 fix):** `dist/editor/orc-v1-complete-v1/72bad312d0d5c2fcee21` (Aseprite 1.3.18.6-x64, batch `--noinapp`, cloudCalls: none; created 2026-10-26T01:41:57Z). Supersedes initial build `04f145ce9e6b72bf77e3`.
- **Re-review:** 2026-10-25 — L1 fix verified **RESOLVED**; all mandated checks re-run and passing.

## VERDICT: **APPROVED** (technical QA)

No blockers, no high or medium severity findings. The single LOW finding (L1) from the initial review was **fixed and verified RESOLVED in re-review** — no LOW findings remain, only accepted-by-design notes. This approval covers **technical completeness, consistency, integrity and governance only**. It does **not** grant artistic approval (`PENDING_CREATOR` remains, Gate 2 belongs to the creator) and does **not** authorize Unity integration (`runtimeImplemented: false`).

## 1. Mandated commands — executed and passing

| Command | Result |
| --- | --- |
| `node --test test/main-orc-complete.test.mjs` | 1 test / 1 pass / 0 fail (initial 98 ms; re-review 253 ms) |
| `node src/cli.mjs validate --id orc-v1 --stage full` | Initial: PASS 749 · FAIL 0 · **WARNING 8** · NOT_RUN 1 · REQUIRES_HUMAN_REVIEW 1 → **After L1 fix (re-review): PASS 749 · FAIL 0 · WARNING 5 · NOT_RUN 1 · REQUIRES_HUMAN_REVIEW 1** |

The test is genuine and non-trivial: it re-reads the coverage matrix, all 28 clip manifests, frame-level `weaponVisible` flags, protected-file hashes, governance pointers, and the Unity handoff contract. It would fail on any drift.

## 2. Independent verification (recomputed from disk, not trusting manifests)

| # | Claim (qa-brief / coverage / contract) | Independent check | Result |
| --- | --- | --- | --- |
| 1 | 28/28 cells `COMPLETE_VERIFIED` (4 dirs × 7 actions) | Recounted cells + full combo matrix | ✅ 28/28, no missing/extra combos |
| 2 | Aseprite masters verified via `exportAseprite` (75 jobs / 599 frames) | Re-review build `72bad312d0d5c2fcee21`: 75 job folders on disk; `build.json` summary jobs=75, frames=599, comparedFrames=599; coverage matrix `editorBuild.path` updated to the new build | ✅ |
| 3 | Native validation 749 PASS / 0 FAIL | Re-ran `validate --stage full` before and after the L1 fix; after fix, checks = 749 PASS + 5 WARNING + 1 REQUIRES_HUMAN_REVIEW + 1 NOT_RUN — the 3 exceptional attack-frame `duplicate` entries were eliminated (756 vs 759 entries) | ✅ |
| 4 | `master256`/`master128` sha256 in coverage matrix | Recomputed SHA-256 of every declared master on disk | ✅ all match (20 cells with 128 masters; 8 attack cells composite-only by design) |
| 5 | Clip manifests consistent (timings, frames, policy, approval) | Re-read all 28 `clip.json`: `durationsMs` sums == `totalDurationMs` == coverage values; frame counts match; `attack-only-v1` + `PENDING_CREATOR` everywhere | ✅ |
| 6 | Idle = `idle-balanced-v1` (400/450/500/450/400 = 2200 ms, loop) | All 4 directions match exactly; `config/idle-art-standard-v1.json` (MANDATORY_CREATOR_STANDARD) confirms same timings/2px head excursion reference | ✅ |
| 7 | Sword 13f/730ms visibleInterval [2,10]; Axe 12f/1005ms [2,8] | Frame-level visibility maps recomputed from clips: Sword `0011111111100`, Axe `001111111000` in every direction; entry/recovery frames hidden | ✅ |
| 8 | Contact events Sword f8@360ms, Axe f6@410ms, Unarmed f2@190ms | Recomputed cumulative start times from `durationsMs`: 360/410/190 ms exact | ✅ |
| 9 | 149 native 128×128 PNGs | Walked `characters/orc-v1/sprites/` | ✅ 149 |
| 10 | 4 static directional bases (both canvases) + 2 independent weapon assets + unarmed supplement | All present on disk and in dist | ✅ |
| 11 | dist package integrity | Re-hashed **894/894** files against `dist/orc-v1/complete-v1/hashes.json`; structure: `Directions` ×4, `Weapons` ×2, `Animations`, `Actions`, `Composite256`, `unity-handoff-contract.json`, `factory-manifest.json`, `animation-coverage-matrix.json` | ✅ |
| 12 | Canonical art preserved (protection snapshot) | Recomputed **525/525** protected hashes (concepts, studies, rescue-v3/polish-v1/entry-v1, orc-pixellab-05, both weapon packs) | ✅ byte-identical |
| 13 | Pointers untouched: `equipment-current.json` = `main-orc-onehanded-v3`; entry candidate = `main-orc-onehanded-entry-v1` | Re-read both | ✅ intact |
| 14 | `unityRepositoryModified: false` | `git -C ../TacticsRPG status --porcelain` → empty tree | ✅ zero modifications |
| 15 | Zero destructive Git operations | `git status --porcelain` in factory: only `M`/`??` entries, **no `D`** | ✅ |
| 16 | Contract geometry | Pivot math verified: 128px `groundY 126` → normalized (0.5, 0.015625) from bottom; 256px `groundY 190` → (0.5, 0.2578125); `bodyOffset [64,64]` + 126 = 190 (zero-shift registration); world sizes 1.28² vs 2.56² @PPU 100 consistent; grips Sword [48,66] / Axe [36,55] identical across brief, coverage, contract, build tool and Lua | ✅ |
| 17 | front_r reuse of canonical entry-v1 | Lua authoring script explicitly byte-preserves front_r composite PNGs from `onehanded-entry-v1`; protection hashes confirm sources untouched | ✅ |
| 18 | Review studios | `Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html`, `…/Estudos Comparativos/Orc principal - Biblioteca completa/index.html`, library index — all exist | ✅ |


## 3. Findings (severity-ranked)

### BLOCKER — none
### HIGH — none
### MEDIUM — none

### LOW
- **L1 · Unarmed Attack frame 01 pixel-identical to frame 00 in 3 of 4 directions — ✅ RESOLVED (verified in re-review).** Fix: frame 01 now carries the distinct Axe/03 raised shoulder-coil pose in all 4 directions. Independently verified: `attack_<dir>_01.png` differs from `attack_<dir>_00.png` in every direction (byte-distinct, different sizes → distinct pixels); the 3 `duplicate` WARNING entries (`attack_back_l_01`, `attack_back_r_01`, `attack_front_r_01`) are gone; WARNINGs dropped 8 → 5, leaving only the 5 by-design static-base duplicates (I3). Package fully rebuilt as `72bad312d0d5c2fcee21` and re-verified end-to-end (894/894 dist hashes; test suite still 1/1 pass; frame-level `attack-only-v1` maps unchanged).

### INFO / accepted-by-design (no action required)
- **I1 · `REQUIRES_HUMAN_REVIEW` (art check):** identity across views, anatomy, silhouette, clusters, light, dominant hand, loop. This is the correct artistic gate and remains with the creator — expected, not a defect.
- **I2 · `NOT_RUN` (unity check):** Import/Resources.Load/PlayMode not executed. Expected: this task is staging-only; the contract enumerates 5 required runtime extensions (UnitVisuals registration, per-frame `durationsMs`, weapon-kind profile resolution, pivot mapping, attack-only-v1 visibility enforcement).
- **I3 · All 5 remaining duplicate warnings are by design:** 4 directional static bases equal Idle frame 0 (rest pose), and `orc_v1_mvp1_static_128.png` equals the front_r directional base. After the L1 fix these are the only WARNINGs left in the full validation.
- **I4 · Sword/Axe attacks have no 128×128 native master:** two-canvas architecture — native 128 carries weaponless states; combat lives in 256×256 composites with `weaponBack/body/weaponFront/handFront` layers. Consistently documented in the contract; nothing claims otherwise.
- **I5 · Contact events are `CANDIDATE_VISUAL_ONLY`, `appliesDamage: false`:** honestly declared; no gameplay wiring is claimed.
- **I6 · `dist/` is not Git-tracked** (build output policy); integrity is provided by `hashes.json`, which this QA fully re-verified (894/894).

## 4. Governance & safety — confirmed

- Active selection `main-orc-onehanded-v3` and entry candidate `main-orc-onehanded-entry-v1` preserved untouched; new pointer `equipment-complete-candidate.json` correctly marked `PENDING_CREATOR` / `runtimeImplemented: false`.
- 525/525 protected canonical art files byte-identical (SHA-256).
- Zero deletions or destructive Git operations in the factory repo; `../TacticsRPG` working tree completely clean — no Unity writes.
- `attack-only-v1` verified at frame level in all 8 attack clips across all 4 directions (maps in §2 #7); all Idle/Walk/Unarmed/Hit/Defeat clips are weapon-invisible on every frame.
- Weapon visibility also enforced after action (`hideAfterAction`) and `layerOrder` uniform everywhere.
- **Re-review (build `72bad312d0d5c2fcee21`):** all guarantees in this section re-verified unchanged — governance pointers intact, 525/525 protected files byte-identical, factory Git has no deletions, `../TacticsRPG` still completely clean.

## 5. Method & limitations

- All hashes recomputed with SHA-256; coverage matrix, clip manifests, Unity contract, Lua authoring script, build tool, review builder and test cross-checked against each other and against disk; timing and pivot math recomputed from raw `durationsMs`.
- Verification script kept at `tmp/qa-verify-main-orc-complete.mjs` (scratch, Git-ignored) — 0 FAIL findings on final run.
- **This QA does not judge artistic quality** (identity between views, anatomy, grip plausibility, silhouette readability). Those remain explicitly with the creator via the review studios (`Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html` and `…/Estudos Comparativos/Orc principal - Biblioteca completa/index.html`), per `PENDING_CREATOR`. No Unity PlayMode evidence exists or was claimed.

## 6. Bottom line

**APPROVED — FINAL (re-review confirms L1 RESOLVED).** The package on build `72bad312d0d5c2fcee21` is technically complete, internally consistent, integrity-verified and governance-compliant: 28/28 cells `COMPLETE_VERIFIED`, 75 jobs / 599 frames editor verification, 749 PASS / 0 FAIL / 5 WARNING (all by design, I3), 894/894 dist hashes, 525/525 protected files, Unity repo untouched. **No LOW findings remain.** The pending artistic review (`PENDING_CREATOR`) is the only item carried forward to the creator.
