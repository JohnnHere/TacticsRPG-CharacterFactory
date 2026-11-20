> Atualização de integração — 27/10/2026: o checkpoint pós-QA de9 ativos/3 em reparo descrito abaixo é histórico. Os três reparos locais foram integrados como candidatos: matriz atual12 ativos/16 aliases, sem aprovação do criador. A versão corrigida precisa do parecer do MESMO QA Copilot no novo freeze. Consulte o [relatório corrente](root-integration-report.md) e seu qa-result.json para o veredito da versão exata; não interpretar a rejeição6fa4653e nem o checkpoint interno como aprovação desta versão.

# QA Revision 1 Knowledge & Contracts Report — main-orc-rear-recovery-v2

**Date:** 2026-10-27  
**Role:** CONTRACT/KNOWLEDGE DEV (Documentation, quality contracts, candidate recipes, validator tests)  
**Contract ID:** `factory.artistic-quality-gates.v1`  
**Candidate Manifest:** [`characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json`](../../characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json)  
**Independent QA Reviewer:** GPT Sol6.1 via GitHub Copilot (`modelId: gpt-6.1-sol`)  
**Reviewed Freeze:** `6fa4653eabe660992acc422aa32159b48e4971122df0e995b99a19261df4a843` (3,794 files)  
**QA Verdict:** `REVISIONS_REQUIRED` ([`qa-argon-final.md`](qa-argon-final.md) / [`qa-result.json`](qa-result.json))  
**Package Artistic Status:** `ARTISTIC_REVISION_REQUIRED`  
**Creator Approval:** `PENDING_CREATOR` (Sole authority of the human creator)  
**Runtime Claim:** `runtimeImplemented: false` (Zero modifications to `../TacticsRPG`)

---

## 1. Executive Summary & QA Findings

Independent integrated visual QA conducted by **GPT Sol6.1 via GitHub Copilot** on freeze `6fa4653e` issued **`REVISIONS_REQUIRED`**, identifying four specific defects (QA-01..QA-04) across three rear weapon cells:

| Defect ID | Severity | Affected Cell & Frames | Confirmed Defect | Status & Corrective Action |
|---|---|---|---|---|
| **QA-01** | HIGH | `back_l/Sword`<br>F01–F07 (strip in F05) | The supposedly unarmed `body` layer contains a second light blade/shaft cluster beside the non-striking right hip (F01–F07) and a pale strip across the upper shoulder/neck (F05). Pixels survive with weapon layers off. F07 is not visually unarmed. | Rejection on freeze `6fa4653e` recorded as historical/frozen QA verdict. Historical Art Luna (`8eb61d74`) went idle at 04:50:23Z without canonical art mutation; partial attempt rejected by Root (256 donor offset error + 64px displacement). Active repair in progress under sole Art Producer `b8ca8bb5-e80c-4c39-ade9-09b167774d78` (`GPT-6.1 Sol Codex xhigh` via Paseo) without paid calls. Package status: `ARTISTIC_REVISION_REQUIRED` (NO PASS). |
| **QA-02** | HIGH | `back_r/Axe`<br>F01–F03 | Weapon contamination in `body` itself: a second curved axe-head shape beside raised forearm in F01 and brown shaft pixels above raised hand in F02–F03, duplicating weapon silhouettes when the independent axe overlay is added. | Same historical rejection. Active repair in progress under sole Art Producer `b8ca8bb5-e80c-4c39-ade9-09b167774d78` removing contamination locally in Aseprite. Status: `ARTISTIC_REVISION_REQUIRED` (NO PASS). |
| **QA-03** | HIGH | `back_r/Axe`<br>F04–F05 | Broken kinematic chain in downward attack commit: F04 has a truncated body arm, and F05 has a doubled lower-arm silhouette, severing the continuous shoulder-elbow-wrist connection. | Same historical rejection. Active repair in progress under sole Art Producer `b8ca8bb5-e80c-4c39-ade9-09b167774d78` restoring continuous limb chain. Status: `ARTISTIC_REVISION_REQUIRED` (NO PASS). |
| **QA-04** | MEDIUM | `back_l/Axe`<br>F02–F03 | Extraneous thin hook/strand protruding from the image-right shoulder in native body cels F02–F03. The raised-fist donor repair itself is valid, but the shoulder contour requires cleanup. | Same historical rejection. Active cleanup in progress under sole Art Producer `b8ca8bb5-e80c-4c39-ade9-09b167774d78` in Aseprite. Status: `ARTISTIC_REVISION_REQUIRED` (NO PASS). |

### Validated Retained Work (No Blocking Defects Confirmed)
The QA review confirmed that the following assets are sound and must be retained:
- **`back_r/Walk` & `back_l/Walk`:** Alternating boot lift, crossing/plant phases, and stable armored trunk reading as true walking loops rather than vertical bobs.
- **`back_r/Unarmed` & `back_l/Unarmed`:** Directionally coherent punches communicated in depth with connected limbs.
- **`front_r/Unarmed` & `front_l/Unarmed`:** Localized F02 repairs restoring closed gauntlets validated; candidate frames 00/01/03/04 have decoded RGBA pixels and timings identical to `complete-v1` (candidate PNG encoding differs), while original baseline files remain byte-preserved.
- **`front_r/Defeat` & `front_l/Defeat`:** Multi-stage volumetric ground collapse retaining head/pauldron/chest mass on ground line; terminal frame held properly at all playback speeds.
- **`Hit` (all 4 directions):** Headless Chromium playback at 1×, 0.75×, and 0.5× confirmed readable torso/shoulder recoil with planted feet; 450 ms timing and current pixels retained for creator review.
- **`back_r/Sword`:** Overhead preparation and forward cut verified without floating blade or severed limbs.

---

## 2. Semantic Cleanliness vs. Structural Layer Integrity

A key takeaway formalized in this review is the **strict distinction between structural pipeline checks and semantic visual cleanliness**:

> [!CAUTION]
> **False Claims of Clean Body Disproved:**
> Automated checks (`body` == `master` == `native crop` and `alpha-over` == `composite`) verify **only mathematical packaging and export consistency**. They **cannot detect** when generative diffusion models bake secondary weapons, blades, or shafts directly into the flesh or armor pixels of the `body` layer.

### Mandatory Verification Protocol:
1. **Semantic Layers-Off Visual Inspection (`weapon-contamination-and-layers-off-inspection`):**
   Every equipable body cycle must be inspected visually with **all weapon layers turned off** across every frame to guarantee that the body is truly unarmed (no phantom blades, duplicate heads, or brown shaft remnants).
2. **Kinematic Chain Continuity:**
   The anatomical chain from shoulder to elbow to wrist must remain continuous and physically plausible across keyframes (anticipation, strike commit, impact, recovery) before applying front-hand occlusion cels (`handFront`) or equipment overlays.

---

## 3. Canonical Matrix Partition & Accounting Truth

### Canonical Matrix State (`candidate28manifest.json`)
The canonical matrix comprises exactly 28 cells (4 directions × 7 actions):
- **12 Scoped Target Cells:**
  - **9 `ACTIVE_CANDIDATE`:** `front_r/Unarmed`, `front_r/Defeat`, `front_l/Unarmed`, `front_l/Defeat`, `back_r/Walk`, `back_r/Unarmed`, `back_r/Sword`, `back_l/Walk`, `back_l/Unarmed`.
  - **3 `ARTISTIC_REVISION_REQUIRED`:** `back_l/Sword` (QA-01), `back_r/Axe` (QA-02, QA-03), `back_l/Axe` (QA-04).
- **16 `UNCHANGED_ALIAS`:** Exact baseline canonical clips preserved from `complete-v1` (`b178422e1f7fc19f068c`).
- **Total Local Composite Frames:** 210 frames (78 in candidate/target cells, 132 in protected baseline aliases).
- **Active Masters Declared & Verified:** 28 unique masters with verified SHA-256 digests.

### Budget Accounting Invariant (17 Jobs, 78 Generations)
- **13 Historical Jobs:** 66 generations (initial session cap).
- **1 Early Execution Deviation (`job 31e61c4b`):** 3 generations, preserved as deviation and authorized for local refinement.
- **3 Explicitly Authorized Jobs (9 generations):**
  - `back_l/Sword` (`8f0f4e44`, 3 generations).
  - `back_r/Axe` (`8b6ad151`, 3 generations).
  - `back_l/Axe` (`5296ac98`, 3 generations under `root-axe-pass-final-direction-authorization.txt`).
- **Breakdown of 78 Generations:**
  - 14 rejected (12 Draft-01 inpaint + 2 weak punch).
  - 24 incompatible isolated whole-body geometry in cache (later Lua composition flattening defect).
  - 28 accepted non-weapon cycle/terminal contributions (Walk, Unarmed, Defeat; NOT Hit).
  - 12 weapon-body-cycle units (`Sword`/`Axe` across both rear views).
- **Financial Balance:** 1418.70 generations remaining verified at 69-generation checkpoint; current balance after 78 is not guessed without a new receipt. Zero future paid jobs authorized.
- **Preservation Tracked:** 793 files tracked = 792 byte-identical + 1 authorized gate config changed; 73 baseline masters preserved.

---

## 4. Contract, Config, Recipe, and Test Files Altered by DEV

As sole owner of contracts, documentation, recipes, and test suites, DEV executed the following modifications:

1. **[`config/artistic-quality-gates-v1.json`](../../config/artistic-quality-gates-v1.json):**
   - Updated Lesson 15 (`weapon-contamination-and-layers-off-inspection`) to establish the semantic layers-off rule and continuous kinematic chain requirement.
   - Updated `currentAssessment`:
     - `setStatus`: `"ARTISTIC_REVISION_REQUIRED"`
     - `independentQAStatus`: `"REVISIONS_REQUIRED"`
     - `independentQAVerdict`: `"REVISIONS_REQUIRED by GPT Sol6.1 Copilot on freeze 6fa4653e (findings QA-01..QA-04)"`
     - `perActionStatus`: set `"Sword Attack"` and `"Axe Attack"` to `"ARTISTIC_REVISION_REQUIRED"`.
     - `activeCandidatesCount`: 9, `inRevisionCount`: 3, `unchangedAliasesCount`: 16.
     - Documented QA-01..QA-04, layers-off semantic distinction, and Luna's active local repair in `criticalFindings`.
2. **[`recipes/races/orc.candidate.json`](../../recipes/races/orc.candidate.json):**
   - Updated Rule 17 to require semantic whole-body visual inspection with layers off and continuous shoulder-elbow-wrist kinematic chain validation.
3. **[`docs/RECIPES.md`](../../docs/RECIPES.md):**
   - Updated Section 5 checklist to incorporate semantic layers-off inspection, kinematic chain continuity, and donor cluster verification.
4. **[`AGENTS.md`](../../AGENTS.md) & [`handoff/AGENT_CONTEXT.md`](../../handoff/AGENT_CONTEXT.md):**
   - Documented the Copilot QA verdict `REVISIONS_REQUIRED` on freeze `6fa4653e` as historical/frozen.
   - Recorded findings QA-01..04, Luna's idle/rejection, active local repair by sole Art Producer `b8ca8bb5-e80c-4c39-ade9-09b167774d78` (`GPT-6.1 Sol Codex xhigh` via Paseo) in Aseprite without paid calls, and package status `ARTISTIC_REVISION_REQUIRED` (NO PASS).
   - Clarified matrix status: 12 target cells (9 active / 3 in revision) + 16 unchanged aliases.
5. **[`docs/ARTISTIC_QUALITY_GATES.md`](../../docs/ARTISTIC_QUALITY_GATES.md):**
   - Updated header banner and Lesson 15 with the semantic layers-off rule and current post-QA status.
6. **[`docs/ROADMAP.md`](../../docs/ROADMAP.md):**
   - Synchronized header and Wave 2 section with QA verdict `REVISIONS_REQUIRED` and active local Aseprite repairs under new Art Producer.
7. **[`docs/WORKFLOW.md`](../../docs/WORKFLOW.md):**
   - Updated operational rules 10 and 11 with the 9/3/16 matrix breakdown, semantic layers-off inspection, and kinematic chain continuity.
8. **[`experiments/main-orc-rear-recovery-v2/validate_candidate_manifest.mjs`](validate_candidate_manifest.mjs):**
   - Enhanced revision cell validator to recognize both `'ARTISTIC_REVISION_REQUIRED'` and `'REVISIONS_REQUIRED'` as valid `reviewStatus` values.
9. **[`experiments/main-orc-rear-recovery-v2/knowledge-final-report.md`](knowledge-final-report.md):**
   - Added dated correction notice (2026-10-27) rectifying prior overclaims regarding 12 ready candidates, structural layer cleanliness, and frontUnarmed pixel vs encoding preservation.

---

## 5. Test Suite Verification Results

All automated test suites pass cleanly under Node v24.20.0 and Python 3.12.14:

| Test Suite | Command | Result | Duration | Notes |
|---|---|---|---|---|
| **Complete Orc Suite** | `node --test test/main-orc-complete.test.mjs` | **2 passed, 0 failed** | ~1.67s | Coverage matrix, quality gates contract, 12 semantic lessons with 9 fields, and baseline art protection verified. |
| **Candidate Manifest Validator Suite** | `node --test experiments/main-orc-rear-recovery-v2/validate_candidate_manifest.test.mjs` | **14 passed, 0 failed** | ~4.15s | Verifies dynamic headers against live manifest, 12/0 delivery fixture, armed/unarmed policies, and isolated negative fixtures (corrupted master SHA, missing master, corrupted frame, missing frame, corrupted layer SHA). |
| **Candidate Manifest Validator CLI** | `node experiments/main-orc-rear-recovery-v2/validate_candidate_manifest.mjs --allow-incomplete` | **274 passed, 0 failed** | ~0.45s | Full contract check in partial mode; reports 9 active candidates, 3 revision cells, and 16 aliases. |
| **Baseline Art Protection** | `python experiments/main-orc-rear-recovery-v2/verify_baseline_protection.py` | **792/793 identical, 1 allowed** | ~0.80s | Exact byte preservation confirmed; only authorized `config/artistic-quality-gates-v1.json` modified. |

---

## 6. Handoff & Governance

- **Art Producer Scope:** Luna (`8eb61d74`) went idle at 04:50:23Z without canonical art mutation; partial attempt was rejected by Root (256 donor offset error + 64px displacement). Active repair is currently in progress under sole Art Producer **`b8ca8bb5-e80c-4c39-ade9-09b167774d78`** (`GPT-6.1 Sol Codex xhigh` via Paseo) for `back_l/Sword` (QA-01), `back_r/Axe` (QA-02, QA-03), and `back_l/Axe` (QA-04) locally in Aseprite with zero additional paid generation calls.
- **QA Re-review:** Once repairs and re-exports are frozen by Root under a new freeze ID, the package will be resubmitted to the same independent QA reviewer: **GPT Sol6.1 via GitHub Copilot** (session `08686`, model `gpt-6.1-sol`).
- **Creator Approval:** Remains **`PENDING_CREATOR`**. Status is strictly **`ARTISTIC_REVISION_REQUIRED`** (NO PASS).
- **Engine Status:** `runtimeImplemented: false`. Zero writes to `../TacticsRPG`. Root will synchronize repository state after ART finishes.
