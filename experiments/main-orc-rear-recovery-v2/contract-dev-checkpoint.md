# Contract/Knowledge DEV checkpoint — main-orc-rear-recovery-v2

## Changes
- `config/artistic-quality-gates-v1.json`: Hit universal hard minimums converted from hard `measurableChecks` to context-sensitive `diagnosticWarnings` (severity warning, artisticInterpretation true, notHardFailures true). Hard integrity checks retained (`bottomPinnedToGroundY`, file validity, frame/duration metadata, export hashes/provenance). Historical measurements preserved as diagnostic values.
- `config/artistic-quality-gates-v1.json` (targeted fix): added `contextualProfiles.heavyOrc` under `choreographyGate.hit`. Heavy-orc impact must communicate readable impact + justified body mechanics; head snap is optional/contextual, not a universal per-race requirement. Required readable: impact at 1x playback, clear recovery to rest. Required body mechanics: justified torso/shoulder recoil consistent with armor weight, ground contact preserved.
- `docs/ARTISTIC_QUALITY_GATES.md`: mirrored the Hit diagnostic wording and the heavyOrc contextual profile.
- Added production lessons 11 and 12 (rear motion needs rear construction; numeric Hit thresholds can encourage overacting), each with symptom/verifiedCause/failedApproach/successfulCorrection/reuse/prevention/validation/cost/applicability.
- Added production lessons 13 and 14 (external cross-fade failure; continuous temporal anchored generation), with structured evidence fields and status markers (FAILED_METHOD_ARCHIVED / CANDIDATE_AWAITING_ROOT_INSPECTION).
- `test/main-orc-complete.test.mjs`: replaced brittle lesson-count-12 assertion with semantic required-lesson-IDs + field-coverage check; replaced hard Hit numeric minima (>=6px/>=5px/>=4px) with diagnostic finite-number checks plus an explicit warning-vs-technical-failure distinction block.

## Schema/behavior changes for art producer/root
- Hit amplitude/timing thresholds are diagnostic warnings, not technical failures. Only `bottomPinnedToGroundY` and integrity checks remain hard.
- New `contextualProfiles.heavyOrc` under `choreographyGate.hit`; `headSnap` optional for heavy orc.
- New `diagnosticWarnings` object under `choreographyGate.hit`.
- Lesson count now 14; lesson objects 11-14 use structured evidence fields; lessons 13-14 carry status markers.
- Field names preserved where possible; no deletion of integrity gates. Existing consumers reading `measurableChecks` still find `bottomPinnedToGroundY`, `heightCompressionDefinition`, `motionEnergyDefinition`.

## Compatibility
- Backward compatible: `requiredComponents` and `forbidden` retained; `contextualProfiles` is additive.
- No art produced, no paid calls, no candidate/master/renderer/preview edits, no agents, no QA by DEV.
- Creator approval still PENDING_CREATOR. Known artistic defects remain ARTISTIC_REVISION_REQUIRED until producer fixes them.

## Pending
- Producer artifacts (stage-a.md, production-lessons.json) already consumed where available; root-cause/success claims for remaining rear cells (back_l Walk, rear Unarmed, rear Sword/Axe, front Defeat terminal) still need actual producer evidence before finalization.
- root-weapons-midproduction-snapshot.json independently records weapon hashes starting now; not a pre-session baseline, not touched by DEV.
