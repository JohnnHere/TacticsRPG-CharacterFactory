# Independent QA of the integrated Orc V1 recovery

You are the independent final reviewer, not a DEV. The creator explicitly requested Paseo orchestration and independent integrated QA. Do not spawn additional QA agents. Do not edit production sources, docs, metadata, preview or selection. No paid PixelLab calls, no Unity, no Git commit/reset. Write only your reports, diagnostic screenshots and temporary export checks.

Repository: current working directory. E means `experiments/main-orc-rear-recovery-v2`, not a literal E subdirectory. Read `E/delivery-freeze.json`, `E/root-integration-report.md`, `E/production-final-report.md`, `E/creator-task.md` and the relevant final code/docs. The frozen manifest identifies the exact delivery version. Start and end with `node E/root-freeze.mjs --check` and record its freezeId in your result. Here and below expand E to the actual experiment path in commands.

First report your actual capabilities: terminal, inspection of PNG/GIF images, real browser playback and Aseprite hidden export. Do not claim artistic review using hashes alone. If an essential capability is unavailable, report it; never invent a visual PASS.

## Current scope

Character is `orc-v1` / Verde Warcraft, baseline `dist/editor/orc-v1-complete-v1/b178422e1f7fc19f068c`. Canonical candidate: `characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json`.

There are12 affected candidate cells and16 unchanged baseline aliases,28 total. Affected: both rear views Walk/Unarmed/Sword/Axe; both front views Unarmed F02 only and Defeat terminal only. Expected total210 composite frames,78 frames in affected clips (not78 newly redrawn frames). No creator approval. Original equipment-current pointer remains preserved; do not promote this candidate.

Main review: `Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/index.html`. All before/after strips must show actual composite frames at equal scale, including weapons. Source-native body strips must not silently replace armed comparisons. Main player must use actual declared candidate paths, not fallback to another action.

## Visual review is mandatory

Inspect actual source-derived images AND real playback, at1× and slower0.75×/0.5×, with practical display scale as well as native detail. Record actual evidence per action/direction, not just a generic checklist.

- Rear Walk: alternating support/swing feet, stable body, correct rear perspective, connected limbs, plausible ground contact and loop. Reject pure vertical bob or front-facing legs pasted into rear bodies.
- Rear Unarmed: readable preparation, fist extension, impact and recovery; connected shoulder/elbow/wrist, no weapon. Reject unrelated old weapon poses assembled into an incoherent punch.
- Rear Sword: one-handed grip following the actual fist, coherent rear arm/torso/weapon arc, proper occlusion, no floating blade or neck crossing, natural recovery. Preserve approved front clips.
- Rear Axe: compact one-handed proportions, distinct overhead chop and head-heavy follow-through, not just retimed sword. Verify AxeL's locally reused same-view forearm is connected and unclipped. Inspect the whole body with weapon layers off for residual generated axes/shafts/old arms, not only grip crops.
- Front Unarmed: only confirmed F02 fist defect corrected; the other four frames preserve exact decoded RGBA and timing. Candidate PNG encoding differs; original baseline files remain byte-preserved. No donor from a tasset, shoulder plate or empty background masquerading as a fist.
- Front Defeat: terminal fully incapacitated rather than active kneeling; stages0..3 preserved. Rear Defeat remains exact baseline. Terminal playback holds, does not restart unexpectedly.
- Hit: actual four-direction playback at1/.75/.5, native and approximate game scale; retained450ms is justified in root-hit-playback-assessment.md. Unity camera, combat cadence and hit-stop calibration remain deferred; no false runtime claims or universal excursion minimum.

Root internal visual passes permit integration only. They do not substitute your review. Archived rejected drafts are historical; inspect canonical current paths rather than treating an archived failure as the current result.

## Technical/source review

Independently validate actual saved Aseprite masters against exports, not only metadata hashes. Re-export changed composite/native masters to YOUR temporary directory, never over canonical outputs. Verify frame count/order/timings, exact decoded RGBA, body-only native crop and source layer composition. Four rear weapons require real `weaponBack/body/weaponFront/handFront` layers; independent weapon PNGs must match preserved sources. Weapon pixels only in attack frames01..06; no weapon baked into native body. All active clips must expose real composite/native editable masters and hashes. Source/export validity is not artistic approval.

Check baseline preservation,16 exact aliases, four preserved frames in each frontUnarmed, four preserved stages in each frontDefeat, existing libraries, current source selection, and absence of Unity integration. Source provenance and costs must be truthful:78 generation units/17 jobs, original66 cap,3 early-execution deviation, later explicit6+3 authorizations.14 initial rejected units and24 incompatible cached keys are not successful final assets. No fabricated token/USD totals or current account balance.

Review changed quality gates, recipes, workflow, handoff and roadmap. Required12 semantic lessons each need9 nonempty evidence fields. Failures and verified successes should become actionable scoped guidelines, not universal anatomy formulas. Technical file/source checks remain hard; numeric Hit amplitude is contextual diagnostic only. Creator approval remains `PENDING_CREATOR`.

## Relevant executable checks

- `node E/validate_candidate_manifest.mjs` (FINAL strict mode)
- `node --test E/validate_candidate_manifest.test.mjs` (includes isolated negative fixtures)
- `node E/verify_new_representatives.mjs --check` (read-only four weapon proofs)
- `node E/verify_front_f02_and_protected_frames.mjs`
- `node E/verify_four_early_clip_source_metadata.mjs` (if delivered; inspect its mode before executing)
- Python `test/test_rear_recovery_review.py`, Node `test/test_review_js_runtime.mjs`, Node `test/browser-check-rear-recovery-review.mjs`
- Node tests `test/main-orc-complete.test.mjs`, `test/action-contract.test.mjs`, `test/factory.test.mjs`, `test/preview-entry.test.mjs`

Do not rebuild the canonical review after freeze: it has build timestamps. Tests may write their diagnostic outputs, not frozen production. Do not run author_* scripts that rewrite metadata as if they were read-only validators. You may create QA-only export Lua/scripts under E/qa-argon or tmp and use hidden Aseprite with isolated profile.

Python is `C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`. Playwright module is `C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright`. Chromium is `C:/Users/João Orlando/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe`. Launch your own headless browser with file access, bounded waits and finally-close; do not use or terminate the creator's browser or Root's helper. Aseprite path is in local config; use repository helpers, `--batch --noinapp`, hidden Windows process, isolated batch profile.

## Decision and outputs

Write `E/qa-argon-final.md` and `E/qa-result.json`, plus optional diagnostics under E/qa-argon. Include actual model/provider if exposed, frozenID, scope, actual tests, image/playback/source evidence, limitations, findings with exact path/frame/line and severity. Separate confirmed defects from hypotheses. REVISIONS_REQUIRED if blocker/high artistic or technical findings remain; no conditional PASS. A PASS means ready for creator review, never creator-approved. Return idle when your bounded review is finished; do not monitor indefinitely.

If corrections are needed, Root will reintegrate and send the new freeze to THIS same reviewer. Review exact corrected files plus relevant regressions, record the new frozenID, and only then issue a final verdict. Do not preapprove future fixes.
