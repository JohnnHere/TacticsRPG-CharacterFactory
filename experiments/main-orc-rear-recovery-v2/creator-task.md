# TASK — TACTICSRPG CHARACTER FACTORY
# MAIN ORC — TARGETED REAR ANIMATION RECOVERY, COMBAT POLISH & PRODUCTION KNOWLEDGE

## 1. ROLE AND OBJECTIVE

Work within the TacticsRPG Character Factory repository.

This task concerns the current MAIN ORC:

- Character ID: `orc-v1`
- Character identity: Verde Warcraft
- Current artistic recovery build: `b178422e1f7fc19f068c`, subject to repository verification
- Current status: technically complete, artistic review required, creator approval pending

The latest production significantly improved the character's rear-facing base design, frontal artwork, Hit reaction, Defeat presentation and source/export integrity.

However, the creator's latest visual review identifies serious remaining animation defects.

### Primary objectives

1. Repair the defective rear-facing animations.
2. Refine the frontal unarmed attack.
3. Resolve inconsistent terminal Defeat poses.
4. Reassess Hit intensity and timing without unnecessary rework.
5. Preserve every successful part of the current production.
6. Improve the Factory's production recipes and artistic evaluation standards.
7. Document all relevant failures, corrections, successful methods and resource-efficiency lessons.
8. Deliver a complete, immediately accessible visual review package.

**This is a targeted quality-recovery task, not another full character-generation task.**

Do not modify Unity.

Do not rebuild the entire 28-clip library.

---

# 2. CURRENT CREATOR FEEDBACK

The creator reviewed the latest approximately 8-minute-36-second recording and reported:

### High-priority defects

- Rear Sword Attack is visibly bugged.
- Rear Walk is visibly bugged.
- Rear Unarmed Attack is severely bugged.
- Rear Axe Attack is visibly bugged.

These observations apply to the relevant `back_r` and `back_l` variants unless repository evidence narrows the affected set.

### Medium-priority defects

- Frontal Unarmed Attack has minor visual problems.
- Hit looks substantially improved but may be exaggerated and unnaturally fast at normal playback speed.
- Front-facing Defeat can resemble a kneeling character rather than an unconscious or defeated character.

### Successful work

- Rear static anatomy improved significantly.
- Frontal visual quality remains strong.
- The rear terminal Defeat pose looks substantially better.
- Prior successful frontal sword/axe animations should remain intact.
- Previously improved Idle and frontal Walk should remain intact.
- Current independent weapon assets and attack-only visibility are correct design decisions.

### Production-process concern

The creator observed that the previous orchestration session directly executed substantial PixelLab/Aseprite production in the main orchestration context.

The future orchestration workflow is responsible for execution delegation. This technical task must expose clear production boundaries, candidate requirements, reusable artifacts and cost/quality evidence.

Do not prescribe which agent or model performs the work.

Do not request an additional independent QA process.

---

# 3. VERIFY THE REAL CURRENT BASELINE

Before implementation, inspect:

- `AGENTS.md`
- `handoff/AGENT_CONTEXT.md`
- `docs/VISUAL_IDENTITY.md`
- `docs/WORKFLOW.md`
- `docs/ARTISTIC_QUALITY_GATES.md`
- `docs/ASEPRITE.md`
- `docs/EQUIPMENT_AND_ACTIONS.md`
- `docs/RECIPES.md`
- `docs/MAIN_ORC_COMBAT_POLISH.md`
- `docs/ROADMAP.md`

Also locate current equivalents of:

- `config/artistic-quality-gates-v1.json`
- `equipment-current.json`
- `equipment-complete-candidate.json`
- Current MAIN ORC manifests
- Current active `.aseprite` masters
- Current sword/axe assets
- Animation coverage reports
- Current visual preview pages
- Current PixelLab production records
- Current source and export validators

These paths are historical references and must be verified.

The historical Orc V4 is obsolete.

Do not restore it or use it as current production authority.

Inspect Git status before changing any files.

Preserve all unrelated uncommitted work.

### Preserve previous production evidence

The latest report describes:

- 75 Aseprite production jobs.
- 599 frames verified.
- 749 native validation passes.
- 17 automated test suites passing.
- 15 PixelLab-generated keyframes during recovery.
- A candidate still awaiting creator artistic approval.

These figures are reported historical results, not proof that the current working tree remains unchanged.

Verify relevant source and manifest identities.

Do not rewrite previous reports to make unsuccessful artistic work appear approved.

---

# 4. ROOT-CAUSE INVESTIGATION BEFORE REDRAWING

Determine why the problematic animations remain visually unacceptable despite improved rear base sprites.

Investigate separately:

### A. Directional body geometry

- Incorrect shoulder or hip orientation.
- Foreground/background limb confusion.
- Perspective-incompatible anatomical reuse.
- Incorrect head/torso motion.
- Misplaced hands or feet.

### B. Animation choreography

- Poses not belonging to the same physical motion.
- Abrupt frame-to-frame changes.
- Unnatural limb trajectories.
- Inadequate anticipation.
- Weak follow-through.
- Poor recovery.
- Incorrect weight transfer.

### C. Asset and compositing system

- Invalid grip points.
- Incorrect weapon orientation.
- Weapon/body occlusion mistakes.
- Incorrect pivots.
- Transform or scale drift.
- Inconsistent frame metadata.
- Unwanted reuse of incompatible source poses.

### D. Preview or export defects

- Incorrect clip selection.
- Bad frame order.
- Preview-specific transforms.
- Stale exports.
- Incorrect timing interpretation.

Do not assume that all defects originate in PixelLab, Lua or attachment metadata.

Identify the actual causes from the current source and exported animations.

Record confirmed causes separately from hypotheses.

---

# 5. PRIORITY ONE — REPAIR REAR WALK

Target:

- `back_r / Walk`
- `back_l / Walk`

These must show natural locomotion away from the camera.

### Required qualities

- Alternating and readable leg motion.
- Proper weight transfer.
- Coherent hip and shoulder behavior.
- Correct direction of feet and knees.
- Stable center of mass.
- No unnatural torso twisting.
- No disconnected arms.
- No unexpected body rotation.
- Stable ground anchoring.
- No obvious foot sliding.
- Consistent rear armor geometry.
- Clean cyclic transition.

Do not fix locomotion merely by shifting the entire sprite up and down.

Do not mirror the frontal Walk without verifying anatomy and direction.

Do not reconstruct the currently acceptable front Walk.

Inspect whether current rear frames can be corrected through targeted pose changes or require replacing incompatible frames.

Preserve the overall character style and reasonable walking rhythm.

---

# 6. PRIORITY TWO — REPAIR REAR UNARMED ATTACK

Target:

- `back_r / Unarmed`
- `back_l / Unarmed`

The rear unarmed attack is a major artistic blocker.

The action must clearly communicate an actual attack, not disconnected shoulder motion, random arm movement or a malformed silhouette.

### Requirements

- Clear attack preparation.
- Coherent torso movement.
- Correct shoulder articulation.
- Anatomically plausible elbows and wrists.
- Natural fist movement.
- Readable strike direction.
- Visible impact pose.
- Appropriate follow-through.
- Natural recovery.
- Stable ground contact.

No weapons must be visible.

Do not merely combine unrelated Sword and Axe frames because their source metadata is technically compatible.

Pose reuse is valid only when the resulting motion remains artistically convincing.

Ensure consistent action identity across the two rear views.

---

# 7. PRIORITY THREE — REPAIR REAR SWORD ATTACK

Target:

- `back_r / Sword`
- `back_l / Sword`

Preserve:

- Independent `recruit-sword` source.
- Attack-only weapon visibility.
- One-handed grip.
- Correct scale.
- Reusable sword attack profile.

### Correct the motion

The attack must exhibit:

1. Natural anticipation.
2. Correct rear-perspective torso rotation.
3. Valid hand/weapon contact.
4. Coherent elbow and shoulder trajectory.
5. Proper weapon depth and occlusion.
6. A believable sword arc.
7. Readable impact.
8. Controlled follow-through.
9. Natural return to the unarmed resting pose.

### Explicitly reject

- A sword floating behind the character.
- A weapon rotating independently of the hand.
- A grip that changes arbitrarily.
- A sword passing through the shoulder or back incorrectly.
- Abrupt weapon angle changes.
- Front-facing attack poses superficially repainted as rear-facing.
- Invalid foreground/background arm layering.

Preserve successful frontal sword choreography and existing weapon art.

Change rear-specific body poses and attachment metadata as needed.

---

# 8. PRIORITY FOUR — REPAIR REAR AXE ATTACK

Target:

- `back_r / Axe`
- `back_l / Axe`

Preserve the current compact one-handed axe proportions.

The axe must have a distinct attack identity rather than a slower sword animation.

### Requirements

- Convincing anticipation.
- Proper shoulder and torso commitment.
- Plausible hand-to-handle attachment.
- Consistent weapon size.
- Correct rear-perspective occlusion.
- A clear chopping trajectory.
- Perceptible head-heavy momentum.
- Readable impact.
- Natural follow-through.
- Coherent recovery.

Do not compensate for weak animation by enlarging the axe.

Do not introduce two-handed motion.

Do not permanently bake weapon artwork into the body sprite.

---

# 9. PRIORITY FIVE — TARGETED FRONTAL UNARMED CORRECTION

Inspect:

- `front_r / Unarmed`
- `front_l / Unarmed`

The creator reports a minor visual defect.

Identify the exact problematic poses or transitions before modifying the artwork.

Check:

- Shoulder and elbow coherence.
- Fist movement.
- Hit pose readability.
- Hand anatomy.
- Body balance.
- Return to Idle.

Fix only confirmed issues.

Preserve successful front-facing Idle, Walk, Sword and Axe animations.

Do not reconstruct complete frontal animation sets to fix a small Unarmed defect.

---

# 10. HIT — CALIBRATION, NOT AUTOMATIC RECONSTRUCTION

The current Hit animation has improved significantly.

The creator considers it potentially exaggerated and too fast at normal speed.

### Important design warning

The current artistic gates reportedly require numerical movement thresholds such as:

- Minimum head excursion.
- Minimum center-of-mass displacement.
- Minimum motion relative to Idle.

These metrics were introduced to prevent overly subtle Hit reactions.

However, they may encourage exaggerated movement.

**Movement amplitude is a diagnostic measurement, not a universal artistic quality score.**

A smaller, well-animated reaction may be better than an exaggerated reaction that passes numeric thresholds.

### Required assessment

Compare the current Hit at:

- 1× playback.
- 0.75× playback, if supported.
- 0.5× playback.
- Expected approximate tactical display scale.

Assess:

- Impact readability.
- Apparent armor weight.
- Shoulder/head recoil.
- Body balance.
- Recovery.
- Perceived duration.
- Frame spacing.

Do not change timing simply because the animation is fast.

Do not change amplitude simply because it is large.

Make a targeted correction only if the actual motion looks unnatural.

### Future Unity consideration

Some Hit timing judgments depend on:

- Combat feedback.
- Damage-number presentation.
- SFX.
- Attack synchronization.
- Turn pacing.

Do not modify Unity in this task.

If a timing decision cannot be reliably established from the standalone Factory preview, document it as a future in-game calibration item.

### Update the gates

Replace simplistic hard minimums with context-sensitive ranges, diagnostic warnings or action-specific evaluation criteria where appropriate.

Do not weaken technical integrity checks.

---

# 11. DEFEAT — STANDARDIZE TERMINAL OUTCOME

The creator prefers the improved rear-facing Defeat terminal posture, where the Orc is clearly down on the ground.

The front-facing Defeat may instead appear to end with the Orc kneeling.

That makes the terminal state semantically inconsistent.

### Canonical interpretation

For the MAIN ORC's current Defeat animation, the terminal pose must communicate that the character is fully incapacitated.

A final upright kneeling posture is insufficient if it reads as a character still able to continue fighting.

### Requirements

- Inspect all four Defeat animations.
- Preserve successful falling choreography.
- Preserve the improved rear terminal pose where valid.
- Refine front-facing terminal poses to clearly communicate collapse or unconsciousness.
- Preserve anatomy and body volume.
- Maintain perspective-correct ground contact.
- Avoid flattening the character using global transforms.
- Preserve terminal-frame semantics.
- Avoid accidental return to Idle.

The four directions do not need pixel-identical poses.

They must communicate the same gameplay outcome.

### Important

Do not transform Defeat into a resurrection, death-confirmation or ragdoll system.

Do not modify gameplay rules.

---

# 12. PRESERVE THE CURRENT SUCCESSES

Do not repeat earlier mistakes by rebuilding everything.

Preserve existing high-quality content:

- Frontal Idle.
- Frontal Walk.
- Frontal Sword.
- Frontal Axe.
- Current MAIN ORC visual identity.
- Improved static rear foundations, except where a specific defect is proven.
- Independent weapon assets.
- Correct attack-only visibility.
- Valid source/export contracts.

Use targeted source revisions and recoverable candidates.

Do not overwrite active artistic masters without appropriate source preservation.

---

# 13. UPDATE THE ARTISTIC QUALITY GATES

The Factory's new artistic gate documentation is valuable, but needs refinement based on this latest feedback.

### Improve evaluation of:

- Rear locomotion.
- Back-facing melee choreography.
- Hand-to-weapon coherence.
- Directional anatomy.
- Body mechanics.
- Unarmed attacks.
- Hit intensity.
- Timing and spacing.
- Terminal Defeat semantics.
- Consistency across the complete animation library.

### Hard technical invariants versus artistic evaluation

Keep hard automated checks for:

- File validity.
- Missing frames.
- Invalid references.
- Corrupt sources.
- Asset provenance.
- Export reproducibility.
- Layer visibility.
- Manifest integrity.

Treat subjective artistic measurements as:

- Diagnostics.
- Suspicion triggers.
- Review prompts.
- Context-dependent thresholds.

Do not force every character race, anatomy or animation style to meet identical motion-amplitude numbers.

### Gate progression

Before large-scale animation propagation:

1. Validate directional bases.
2. Validate representative key poses.
3. Validate one complete action cycle.
4. Verify anatomical and perspective continuity.
5. Expand compatible directions/actions.
6. Compare complete real playback.
7. Retain explicit creator approval status.

A technically complete asset library may remain artistically rejected.

Do not automatically promote candidates.

---

# 14. PRODUCTION EFFICIENCY — LEARN WHAT WORKS

This task must improve future production efficiency.

The objective is to reduce:

- Unnecessary agent tokens.
- Unnecessary PixelLab Pro calls.
- Repeated generation of defective poses.
- Repeated source audits.
- Duplicate animation production.
- Rework caused by propagating an incorrect foundation.
- Documentation inconsistency.
- Redundant preview construction.

### Required production methodology

**A. Reuse-first**

Inspect current sources, approved recipes, usable poses and previously validated references before producing new material.

Use the established reuse categories where applicable:

- REUSE_DIRECT
- REUSE_ADAPTED
- REQUIRES_EXTENSION
- CREATE_NEW

**B. Key-pose-first**

Validate a small representative pose set before generating complete directional sequences.

Do not create hundreds of new frames from an unresolved anatomical base.

**C. Targeted PixelLab use**

Use PixelLab for specifically identified artistic problems where existing assets and Aseprite editing cannot solve them efficiently.

Avoid full-character regeneration when only an arm, grip or perspective needs correction.

**D. Local-first refinement**

Prefer current-source Aseprite corrections, approved recipes, existing references and deterministic local operations when they can produce equal or better quality.

Do not use procedural methods that repeat already documented artistic failures.

**E. Cache and provenance**

Reuse valid generated candidates and source references.

Maintain provenance and input/output relationships.

Do not repeat identical paid generation calls unnecessarily.

**F. No mass propagation before validation**

A defective key pose must not be propagated into dozens of additional frames.

**G. Measure the full cost of approved output**

Optimize for a final usable asset, not simply the cost of producing a draft.

---

# 15. DOCUMENT WHAT FAILED AND WHAT SUCCEEDED

This is a major deliverable.

Update current authoritative Character Factory documentation, especially the relevant:

- Artistic quality gates.
- Character animation workflow.
- Production recipes.
- MAIN ORC animation documentation.
- Roadmap.
- Agent handoff/continuity instructions.

Use actual current paths.

### Record each important production lesson

For every recurring problem, document:

1. **Symptom** — what looked wrong.
2. **Root cause** — what was verified.
3. **Failed approach** — what produced inadequate results.
4. **Successful correction** — what improved the artwork.
5. **Reuse opportunity** — what can safely be reused.
6. **Prevention rule** — what future production must check.
7. **Validation evidence** — how to determine success.
8. **Cost/effort implications** — when measurable.
9. **Scope of applicability** — which characters or actions the lesson covers.

### Required lessons to include

- A rear-facing character needs real rear anatomy.
- Correct rear static artwork does not guarantee good rear animation.
- Weapon-anchor alignment does not prove natural combat choreography.
- Reusing incompatible attack poses creates unnatural animations.
- Numeric Hit thresholds can encourage overacting.
- Defeat must communicate a consistent terminal outcome across directions.
- Technical completion is not artistic approval.
- Validated poses should be reused instead of regenerated.
- Small failed artistic foundations can create extensive downstream rework.
- A complete review interface is mandatory for meaningful creator approval.
- Successful methods must be documented as carefully as failed methods.
- Quality should be evaluated at actual playback speed and practical game scale.

Do not merely append generic lessons to a report.

Convert verified lessons into usable production guidelines, recipe constraints and review checklists.

Do not impose rigid visual formulas on every future race.

---

# 16. COST AND RESOURCE EVIDENCE

Track actual measurable work where the available tooling supports it.

Useful metrics include:

- PixelLab operations performed.
- PixelLab credits consumed, if exposed.
- Number of candidates generated.
- Candidates reused.
- Candidates rejected.
- Aseprite batch jobs.
- Frames modified versus preserved.
- Number of iterations required.
- Successful reuse assessments.
- Production duration, if reliably measurable.
- Agent/model token usage when externally reported.

### Important

Do not invent token counts or credit usage.

If metrics are not exposed, state that explicitly.

Do not treat every Aseprite script run as a paid PixelLab call.

Do not assume a free coding model makes PixelLab generation free.

Use the measurements to recommend more efficient future production recipes.

The execution/orchestration layer owns model assignment, delegation, monitoring and QA.

This technical task only specifies the production evidence needed.

---

# 17. COMPLETE VISUAL REVIEW

Preserve the current interactive visualizer.

The final delivery must have a clear, clickable project-local entry point.

It must support:

- All four directions.
- All seven actions.
- Sword and Axe separately.
- Unarmed Attack.
- Hit.
- Defeat.
- Normal-speed playback.
- Slow motion.
- Frame stepping.
- Looping where appropriate.
- Correct terminal Defeat display.

Provide before/after evidence specifically for:

- Rear Walk.
- Rear Unarmed.
- Rear Sword.
- Rear Axe.
- Front Unarmed.
- Front Defeat.
- Hit, if modified.

Use actual source-derived exports.

Do not hide missing or broken clips with unrelated fallback animations.

Do not build a new preview system unnecessarily.

Verify the review entry point actually resolves and the affected clips can be selected.

---

# 18. IMPLEMENTATION STAGES

The following are technical production stages, not subagent assignments.

### Stage A — Baseline and diagnosis

Identify current authoritative source assets.

Inspect rejected clips.

Record confirmed causes.

Preserve successful sources.

### Stage B — Correct rear locomotion

Refine rear Walk for both views.

Validate complete cycles before expanding further.

### Stage C — Correct rear Unarmed

Repair body mechanics, key poses and perspective.

### Stage D — Correct rear weapon attacks

Repair rear Sword and Axe using their distinct action profiles.

Preserve weapon independence.

### Stage E — Localized front correction

Refine only defective frontal Unarmed frames.

### Stage F — Defeat consistency

Improve frontal terminal poses while preserving good rear Defeat.

### Stage G — Hit assessment

Compare current Hit timing/intensity and apply only justified corrections.

### Stage H — Production contracts

Update artistic quality gates, reusable recipes and documented lessons.

### Stage I — Exports and evidence

Generate reproducible candidate assets, tests, metadata and review pages.

Do not automatically promote the result to creator-approved status.

---

# 19. ACCEPTANCE CRITERIA

## Rear Walk

- Both rear views show plausible walking.
- Feet alternate coherently.
- No obvious sliding or artificial body twisting.
- Torso and limb movement remain anatomically connected.
- Directional identity remains intact.

## Rear Unarmed

- Both views show an identifiable attack.
- Body mechanics are coherent.
- Fists remain anatomically connected.
- Impact is readable.
- Recovery returns naturally to Idle.
- No weapon appears.

## Rear Sword

- Both views show a natural one-handed sword strike.
- Hand/weapon contact is stable.
- Sword trajectory is coherent.
- Arm occlusion is correct.
- No floating or disconnected weapon.
- Existing front sword remains intact.

## Rear Axe

- Both views show a credible one-handed chop.
- Axe proportions remain appropriate.
- Momentum differs from the sword.
- Grip and body movement are synchronized.
- Existing front axe remains intact.

## Front Unarmed

- Confirmed minor pose defects are corrected.
- Existing good motion is preserved.
- Character identity and proportions remain consistent.

## Hit

- No exaggerated or excessively abrupt movement remains, if confirmed.
- Impact is readable at intended playback speed.
- Stable grid anchoring and anatomy are preserved.
- Any deferred Unity-specific timing decision is documented.

## Defeat

- All four views communicate full incapacitation.
- Frontal terminal poses no longer look like an active kneeling stance.
- Rear successful terminal poses remain intact.
- Character body volume and ground contact remain believable.
- Terminal playback behavior remains correct.

## Pipeline

- Technical validation remains intact.
- Artistic gates distinguish hard failures from diagnostic warnings.
- Failed and successful approaches are documented.
- Reuse guidance is actionable.
- Credit/token evidence is reported only when available.
- No mass regeneration of unaffected frames occurs.
- No unrelated asset production occurs.

## Review

- One primary project-local review link works.
- All relevant animations are selectable.
- Real before/after visual evidence is accessible.
- Creator artistic approval remains pending.

---

# 20. TECHNICAL VALIDATION AND SAFETY

Use existing Factory validators and tests.

Verify:

- Active Orc source selection.
- Valid Aseprite masters.
- Correct frame ordering.
- Valid duration metadata.
- Valid weapon profiles.
- Correct visibility rules.
- Proper pivots.
- Stable export hashes.
- Reproducible exports.
- No obsolete Orc V4 selection.
- No missing required clips.
- No unintended changes to successful frontal art.
- Correct preview routes.
- Appropriate provenance records.

Do not require arbitrary test counts.

Technical tests cannot independently prove visual naturalness.

### Workspace safety

- Inspect Git status.
- Preserve unrelated uncommitted work.
- Use recoverable source revisions.
- Preserve production history.
- Avoid destructive resets or cleanup.
- Do not modify Unity.
- Do not introduce new gameplay mechanics.
- Do not create new Jobs or weapon families.
- Do not create Git commits.
- Do not modify current unrelated approved art.
- Do not consume unapproved PixelLab credits.

The existing orchestration prompt handles agent execution and independent QA.

Do not request additional QA agents.

---

# 21. FINAL DELIVERABLES

Provide:

### A. Diagnosis

Confirmed causes of the remaining animation defects.

### B. Artistic changes

- Corrected rear Walk.
- Corrected rear Unarmed.
- Corrected rear Sword.
- Corrected rear Axe.
- Refined front Unarmed.
- Corrected front Defeat terminal presentation.
- Hit corrections if warranted.

### C. Production evidence

- Modified source paths.
- Preserved source paths.
- Export manifest.
- Relevant asset hashes.
- Frame/timing changes.
- Reuse decisions.
- PixelLab provenance.

### D. Production learning

- Updated artistic gate contract.
- Updated animation recipes.
- Verified failure patterns.
- Successful correction strategies.
- Resource-efficiency lessons.
- Recommendations for future races.

### E. Review package

- Main clickable visualizer entry point.
- Before/after comparisons.
- Actual selectable action coverage.

### F. Technical report

- Actual tests performed.
- Validation results.
- Known limitations.
- Creator approval status.
- Git diff summary.
- Unity integration still pending.

Do not claim artistic approval before creator review.

---

# FINAL DIRECTIVE

**Fix the remaining defective animations without restarting successful production.**

The static rear anatomy has improved, but rear motion must now receive the same artistic attention as frontal motion.

Prioritize:

1. Rear Walk.
2. Rear Unarmed.
3. Rear Sword.
4. Rear Axe.
5. Front Unarmed.
6. Terminal Defeat consistency.
7. Context-sensitive Hit calibration.

Preserve the current MAIN ORC and all successful assets.

Do not rebuild all 28 clips.

Document both successful and failed approaches so future races and characters benefit from this work.

Optimize for a high-quality final result with less unnecessary generation, fewer agent tokens and less PixelLab Pro credit consumption.

Do not modify Unity.

Do not automatically promote the new candidate to creator-approved status.

**The goal is a convincing character animation library and a smarter Character Factory production process.**