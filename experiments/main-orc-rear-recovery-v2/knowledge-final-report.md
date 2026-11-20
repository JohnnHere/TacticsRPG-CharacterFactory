> Atualização de integração — 27/10/2026: o checkpoint pós-QA de9 ativos/3 em reparo descrito abaixo é histórico. Os três reparos locais foram integrados como candidatos: matriz atual12 ativos/16 aliases, sem aprovação do criador. A versão corrigida precisa do parecer do MESMO QA Copilot no novo freeze. Consulte o [relatório corrente](root-integration-report.md) e seu qa-result.json para o veredito da versão exata; não interpretar a rejeição6fa4653e nem o checkpoint interno como aprovação desta versão.

# Knowledge & Contracts Final Report — main-orc-rear-recovery-v2

> [!IMPORTANT]
> **Dated Correction Notice (2026-10-27):**
> Independent QA review by **GPT Sol6.1 via GitHub Copilot** (`gpt-6.1-sol`) on freeze `6fa4653e` ([`qa-argon-final.md`](qa-argon-final.md) / [`qa-result.json`](qa-result.json)) issued **`REVISIONS_REQUIRED`**, reclassifying package artistic status to **`ARTISTIC_REVISION_REQUIRED`** (`PENDING_CREATOR`).
> **Correction of Prior Claims:**
> 1. **Matrix & Review Readiness:** Prior claims of 12 fully review-ready candidates are superseded. The canonical matrix has 12 scoped target cells (currently 9 `ACTIVE_CANDIDATE` and 3 `ARTISTIC_REVISION_REQUIRED`) and 16 `UNCHANGED_ALIAS`.
> 2. **Semantic Cleanliness vs Structural Layer Integrity:** Prior assertions that four-layer alpha-over equality and body-crop equality proved absence of weapon contamination in `body` were false. Layer equality proves only mathematical export packaging, NOT semantic absence of AI-generated weapon pixels baked into the `body` layer.
> 3. **Confirmed Defects (QA-01..QA-04):** `back_l/Sword` body contains a secondary blade/shaft at the hip (F01–F07) and pale shoulder strip (F05); `back_r/Axe` body contains an axe-head in F01 and shaft in F02–F03 duplicating the weapon overlay, plus broken kinematic connection in F04–F05 (truncated body arm and double forearm); `back_l/Axe` body has a protruding shoulder hook in F02–F03.
> 4. **Active Local Repair:** Luna (`8eb61d74`) went idle at 04:50:23Z without canonical art mutation (partial attempt rejected by Root). Sole active Art Producer is now `b8ca8bb5-e80c-4c39-ade9-09b167774d78` (`GPT-6.1 Sol Codex xhigh` via Paseo), repairing `back_l/Sword`, `back_r/Axe`, and `back_l/Axe` locally in Aseprite with zero additional paid calls. Re-review will be performed under a new freeze by the same reviewer (Copilot session `08686`). Status: `ARTISTIC_REVISION_REQUIRED` (NO PASS).
> 5. **Accounting Invariant:** 17 jobs and 78 generations charged (14 rejected, 24 incompatible in cache, 28 accepted non-weapon, 12 weapon-body units). 792/793 production files byte-identical. QA is NOT PASSED.

**Date:** 2026-10-26 (Updated with dated QA corrections: 2026-10-27)  
**Role:** CONTRACT/KNOWLEDGE DEV (Sole owner of docs, config, recipes, and tests)  
**Contract ID:** `factory.artistic-quality-gates.v1`  
**Candidate Manifest:** [`characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json`](../../characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json)  
**Status:** ARTISTIC_REVISION_REQUIRED (Independent QA: REVISIONS_REQUIRED; Creator Sign-off: PENDING_CREATOR)  
**Independent QA Outputs:** Copilot QA results recorded in [`qa-argon-final.md`](qa-argon-final.md) and [`qa-result.json`](qa-result.json) (freeze `6fa4653e`)  
**Runtime Claim:** `runtimeImplemented: false` (Zero modifications to `../TacticsRPG`)

---

## 1. Executive Summary & Ownership Boundaries

- **Role Ownership:** CONTRACT/KNOWLEDGE DEV exclusively owns configuration, quality gate schemas, workflow documentation, candidate recipes, and test suites. Sole Art Producer is **`b8ca8bb5-e80c-4c39-ade9-09b167774d78`** (`GPT-6.1 Sol Codex xhigh` via Paseo), succeeding Luna (`8eb61d74`) who went idle at 04:50:23Z. Preview Owner is **GLM (`8591`)**. There is zero code or role overlap.
- **Runtimes & Tooling:** Verified Node v24.20.0, Python 3.12.14 (`C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`), Git 2.55.0, and Aseprite 1.3.18.6-x64 (`--batch --noinapp`). Factory doctor returned 0 reference errors and `cloudCalls: "none"`.
- **Preservation Invariant:** Baseline library (`complete-v1`, build `b178422e1f7fc19f068c`) and protected production files (**793 files tracked = 792 byte-identical + 1 authorized gate config changed; 73 baseline masters preserved**; historical unsupported count of 525 superseded). Review tools consume isolated candidate entries without overwriting the baseline library.

---

## 2. Accurate Accounting & Wave 2 Art Facts

- **Generation Ledger & Budget Accounting (17 jobs, 78 generations total):**
  - **13 historical jobs = 66 generations** (initial session cap).
  - **1 early execution deviation job (`31e61c4b`, 3 generations, skeleton SwordR):** executed before explicit Root authorization, preserved as historical deviation and authorized for local import/refinement only.
  - **3 explicitly authorized jobs = 9 generations:** authorized by Root under hard caps:
    - `back_l` Sword: **job `8f0f4e44-0936-4502-8c5e-15b4d57e2449`** (3 generations charged).
    - `back_r` Axe: **job `8b6ad151-8708-4431-a606-06b250388fc4`** (3 generations charged).
    - `back_l` Axe: **job `5296ac98-b253-4133-8468-155f7e90c68e`** (3 generations charged under `root-axe-pass-final-direction-authorization.txt`).
  - **Precise Categorization of the 78 Generations:**
    - **14 rejected:** 12 in Draft-01 inpaint (`af1e7ba8`, `ed109b13`) + 2 in weak punch draft (`2ace783c`).
    - **24 unused/incompatible in cache:** exploratory isolated whole-body pose geometry; the flattening and inverted layering in historical Lua scripts was a later composition defect.
    - **28 accepted non-weapon cycle/terminal contributions:** walk, unarmed, defeat (NOT Hit).
    - **12 weapon-body-cycle units:** corresponding to the 4 body cycles for armed actions (`Sword`/`Axe` across both rear views), with subsequent local refinement in Aseprite.
    - *(Nota contábil: nenhuma das 38 gerações rejeitadas/incompatíveis é rotulada como sucesso).*
  - **Account Balance:** 1418.70 generations remaining was verified at 2026-10-26T18:25:58Z at the 69-generation checkpoint prior to debiting the later authorized jobs; current balance after 78 is not estimated without a new receipt (no token or dollar totals invented). Zero future paid jobs authorized.
- **Canonical Matrix & Local Coverage:**
  - 28 canonical matrix clips in `candidate28manifest.json`: exactly **12 `ACTIVE_CANDIDATE`** and **16 `UNCHANGED_ALIAS`** (0 in revision).
  - **28 referenced active masters:** all 12 candidate clips declare real, existing composite 256 masters and native 128 masters with verified digests.
  - **Local coverage:** 210 composite frames across 28 clips: 78 frames in 12 candidate clips (not 78 all-new pixels), and 132 frames across the 16 protected baseline aliases.
- **Rear Weapon Source & Export Proof:**
  - All 4 weapon representatives (`back_r` Sword, `back_l` Sword, `back_r` Axe, `back_l` Axe) feature 4 independent layers (`weaponBack`, `body`, `weaponFront`, `handFront`), 8 frames, 730 ms (`[90,80,90,80,100,80,100,110] ms`), native 128 body-only masters, and own composite masters.
  - Read-only verifier confirms four-layer alpha-over equals exported composite, body-only master equals body layer, and native 128 equals exact center crop without weapon contamination.
- **Aseprite Surgical Repair of AxeL:**
  - Addressed AI generation limitation where skeleton-v3 cropped the raised hand at the top canvas boundary and introduced accidental weapon contamination.
  - Raised fist is completely visible within the canvas boundary.
  - Mandatory inspection with weapon layers off (`layers-off`) expunged AI-generated shoulder axe and brown shaft pixels.
  - Verification of donor cluster before reuse ensured a genuine raised gauntlet (from same-view `back_l/Sword`), rejecting empty backgrounds or forearm crops.
  - Exact removal of 27 pixels of old-arm residue and brown shaft remnants via exact coordinate masks in Aseprite.
- **Front Unarmed F02 & Front Defeat Preservation:**
  - `front_r` and `front_l` Unarmed: only F02 repaired (restoring hanging closed gauntlet from same-view F00); frames00/01/03/04 preserve exact decoded RGBA pixels and timing. Candidate PNG encoding differs; the original baseline files themselves remain byte-preserved.
  - `front_r` and `front_l` Defeat: stages 00..03 preserved; only terminal stage 04 replaced with volumetric ground collapse.
- **Hit Assessment by Root:**
  - Reviewed by Root in headless Chromium across 4 directions at 1x, 0.75x, and 0.5x in native 128 and approximate 64 display; retains 450 ms and current pixels for creator review; Unity gameplay calibration deferred.
- **Review Studio / Preview:**
  - Built from all 28 actual clips with 12 before/after sections, using exact 256px composite tiles in review-only strips (preventing scale distortion and weapon omission).
  - Root resolved compatibility fixes after GLM foreground error; Chromium 20/20 checks passed (28 painted/selectable, strips decoded, frame step, speeds, terminal hold, 0 failed requests).
- **Independent QA Status:**
  - Independent Argon QA is **NOT STARTED** (`NOT_STARTED`), with pointers reserved for future `qa-argon-final.md` and `qa-result.json`.
  - Overall status is **`PENDING_CREATOR`**.

---

## 3. Contracts & Quality Gates Synced

1. **Contextual Hit Gate (`choreographyGate.hit`):**
   - Converted amplitude thresholds into diagnostic warnings (`diagnosticWarnings`, `severity: "warning"`, `notHardFailures: true`).
   - Retained hard checks: `bottomPinnedToGroundY: true`, file validity, frame counts, and hashes.
   - Formulated `contextualProfiles.heavyOrc`: requires readable impact at 1x speed and clear recovery to rest in torso/shoulders; `headSnapOptional: true`. Universal 1-2px bans superseded.
   - **Legacy Rule 4 Superseded.**
2. **Defeat Volumetric Ground Gate (`choreographyGate.defeat`):**
   - Ground line mass retention (`height >= 58px`, `aspect >= 1.3`) is framed as a local diagnostic baseline for `orc-v1` on 128 canvas, not a rigid universal gate for all future anatomies.
   - Directional volumetric retention supersedes any rigid single-pose kneeling formula.
   - **Legacy Rule 5 Superseded.**
3. **12 Semantic Lessons with 9 Fields Each (+ Operational Lessons 13-17):**
   - Formalized all 12 required semantic lessons from Section 15 of `creator-task.md` plus operational lessons 13 (`external-crossfade-raster-interpolation-failure`), 14 (`continuous-temporal-anchored-generation`), 15 (`weapon-contamination-and-layers-off-inspection`), 16 (`donor-cluster-verification-before-reuse`), and 17 (`surgical-same-view-donor-repair`), each with all 9 non-empty evidence fields.
   - Rigorously distinguishes **verified evidence** from **hypotheses/pending verification**.
4. **Candidate Recipe Updated:**
   - Scoped candidate recipe [`recipes/races/orc.candidate.json`](../../recipes/races/orc.candidate.json) updated with directional rear anatomy, weapon independence, contextual heavyOrc Hit, volumetric Defeat, layers-off inspection, donor cluster validation, and surgical same-view repair constraints. Status is strictly `candidate` with zero automated approval.

---

## 4. Test Verification & Suite Results

- **Candidate Manifest Validator (`experiments/main-orc-rear-recovery-v2/validate_candidate_manifest.mjs`):**
  - Added required checks for real editable composite 256 master and native 128 master for **every** `ACTIVE_CANDIDATE`.
  - Verified actual SHA-256 digests against declared `masterSha256` and `nativeMasterSha256`.
  - Full execution in default FINAL mode: **332 passed, 0 failed, complete: true**.
- **Validator Dynamic Test Suite (`experiments/main-orc-rear-recovery-v2/validate_candidate_manifest.test.mjs`):**
  - **14 tests passed, 0 failed** in 4.49s.
  - Dynamically verifies manifest header counts against cell statuses.
  - Covers isolated negative fixtures: corrupted frame SHA-256, missing frame PNG, corrupted 4-layer SHA-256, missing composite master, corrupted masterSha256, missing nativeMaster.
  - Covers simulated 12/0 delivery fixture and verified schemas for all 4 rear weapon representatives.
  - All temporary fixtures created in isolated directories and cleaned up in `finally` blocks.
- **Baseline Protection Check (`verify_baseline_protection.py` via Python 3.12.14):**
  - Confirmed 792 of 793 files byte-identical; exactly 1 authorized configuration file modified (`config/artistic-quality-gates-v1.json`). 73 baseline masters intact.
- **Main Orc Complete Suite (`test/main-orc-complete.test.mjs`):**
  - **2 passed, 0 failed** (coverage matrix and artistic quality gates contracts).

---

## 5. Delivery Status & Governance

- **Technical Status:** `TECHNICALLY_COMPLETE`
- **Artistic Status:** `VISUAL_REVIEW_REQUIRED`
- **Artistic Approval:** `PENDING_CREATOR` (Creator-only authority)
- **QA Status:** `NOT_STARTED` (Awaiting Root execution of independent Argon QA)
- **Engine Status:** `runtimeImplemented: false` (Zero modifications to `../TacticsRPG`)
