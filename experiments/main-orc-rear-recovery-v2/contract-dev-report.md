# Contract/Knowledge DEV report — main-orc-rear-recovery-v2

**Date:** 2026-10-26  
**Role:** CONTRACT/KNOWLEDGE DEV (Sole owner of docs, config, recipes, and tests)  
**Contract ID:** `factory.artistic-quality-gates.v1`  
**Candidate Manifest:** `characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json`  
**Status:** Candidate Final Pending Independent QA & Creator Sign-off (`PENDING_CREATOR`)  
**Data Sync State:** Final exact art master counts and manifest await Root final production report  
**Future QA Pointer:** `experiments/main-orc-rear-recovery-v2/qa-argon-final.md`  
**Full Report:** See [knowledge-final-report.md](knowledge-final-report.md).

## 1. Scope Completed & Role Boundaries
- Scoped knowledge contracts, quality gates, workflow/recipe docs, and automated tests 100% complete and synchronized.
- Zero role overlap: Art Producer is **Luna (`8eb61d74`)** (superseding historical `64f9`). Preview Owner is **GLM (`8591`)**. DEV owns config, docs, recipes, tests, and reports.
- Preservation invariant: Baseline library (`complete-v1`, build `b178422e1f7fc19f068c`) and protected production files (**793 files tracked = 792 byte-identical + 1 authorized gate config changed; 73 baseline masters preserved**; historical unsupported count of 525 superseded).

## 2. Accurate Accounting & Wave 2 Facts
- **Jobs & Generations:** 16 jobs total (13 historical [66 gen] + 1 early deviation job `31e61c4b` [3 gen] + 2 authorized jobs [6 gen: SwordL job `8f0f4e44-0936-4502-8c5e-15b4d57e2449` and AxeR job `8b6ad151-8708-4431-a606-06b250388fc4`]).
- **Generation Categorization (75 gen):** 14 rejected + 24 unused/incompatible cached whole-body pose geometry (flattening/grip was a later Lua composition defect) + 28 accepted non-weapon contributions + 3 early deviation + 6 authorized. (1418.70 balance was verified prior to debit of the 6 authorized gen; no unverified current balance guess). 0 future paid jobs authorized.
- **Root Checks:**
  - Representative SwordR (8f, 730ms, 4 layers, native 128 body master) passed: `PASS_FOR_INTERNAL_EXPANSION`.
  - Front Unarmed F02 donor restoration internally accepted for both views.
  - In-flight: SwordL (job `8f0f4e44`) and representative AxeR (job `8b6ad151`) underway by Luna (`8eb61d74`) under bounded authorization (no ready claim).
  - Hit reviewed by Root in headless Chromium (4 directions, 1x/0.75x/0.5x, native 128 and approx 64); recoil legible, stance planted; recommend retaining pixels and 450ms; Unity calibration deferred.
- **Matrix & Manifest:** 12 affected cells + 16 unchanged aliases in `candidate28manifest.json`. Exact final art master counts and manifest await Root final production report.
- **QA:** Independent Argon QA is NOT STARTED (`NOT_STARTED`).

## 3. Contracts & Documentation Synced
- **Contextual Hit Gate:** Converted amplitude thresholds into diagnostic warnings (`diagnosticWarnings`, `severity: warning`, `notHardFailures: true`). Formulated `heavyOrc` profile. Hard integrity checks retained (`bottomPinnedToGroundY: true`, file validity, hashes). Legacy rule 4 superseded.
- **Volumetric Defeat Gate:** Ground line mass retention (`aspect >= 1.3`, `height >= 58px`) framed as local diagnostic baseline for `orc-v1` on 128 canvas, not a rigid universal gate. Legacy rule 5 superseded.
- **12 Semantic Lessons with 9 Fields:** Formalized all 12 required lessons plus 2 operational lessons, distinguishing verified evidence from hypotheses, documenting the 16 jobs, and distinguishing the 24 unused pose keys from the later Lua flattening defect.
- **Candidate Recipe:** `recipes/races/orc.candidate.json` created with status `candidate` and zero automated approval.
- **Docs Synchronized:** `docs/ARTISTIC_QUALITY_GATES.md`, `docs/WORKFLOW.md`, `docs/RECIPES.md`, `docs/MAIN_ORC_COMBAT_POLISH.md`, `docs/ROADMAP.md`, `handoff/AGENT_CONTEXT.md`, and `AGENTS.md`.

## 4. Test Verification
- `test/main-orc-complete.test.mjs` verifies semantic lesson IDs, 9 non-empty evidence fields per lesson, `legacyRecords` with superseding notes for rules 4/5, Hit warning-vs-technical-failure distinction, and groundY pinning. All 12 primary tests pass.

## 5. Governance
- Technical: `TECHNICALLY_COMPLETE`
- Artistic: `VISUAL_REVIEW_REQUIRED` (with rear weapons in revision/in-flight)
- Approval: `PENDING_CREATOR` (creator-only)
- Data Sync: Final exact counts and manifest await Root final production report
- Runtime: `runtimeImplemented: false` (no Unity integration)
