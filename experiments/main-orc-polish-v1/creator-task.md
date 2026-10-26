# TASK — TACTICSRPG CHARACTER FACTORY
# One-Handed Combat Animation Polish
## Body Mechanics, Timing, Impact, Grip and Animation Continuity

### TASK TYPE
Targeted artistic refinement and animation quality improvement.

### TARGET
Current MAIN ORC — one-handed sword and axe attack animations.

### PRIORITY
High — Artistic quality and gameplay readability.

---

# 1. ROLE AND OBJECTIVE

Act as a Senior Pixel Art Animation Director, Technical Artist, Character Animation Specialist and Artistic QA Engineer.

Work within the existing TacticsRPG Character Factory repository.

The creator has reviewed the latest sword and axe animation corrections.

**The previous corrective task produced a substantial improvement.**

The current results are significantly better than the original rejected animations.

Specifically:

- One-handed weapon proportions are considerably more appropriate.
- Hand-to-weapon attachment is more convincing.
- Sword and axe attacks have distinct poses.
- Weapon visibility is limited to attack sequences.
- The MAIN ORC's visual identity has been preserved.
- The implementation is now a viable foundation for further refinement.

However, the animation still lacks the desired level of polish.

The remaining problems primarily concern:

1. Insufficient body participation in weapon swings.
2. Weak weight transfer and torso mechanics.
3. Abrupt transitions between selected poses.
4. Inconsistent timing and motion spacing.
5. Insufficient visual emphasis at the moment of impact.
6. Recovery poses that could communicate more physical effort.
7. Remaining grip, occlusion and wrist-alignment imperfections.
8. Abrupt weapon appearance/disappearance at action boundaries.

### PRIMARY OBJECTIVE

**Polish the CURRENT animations into convincing, cohesive and expressive one-handed melee attacks without discarding the improvements already achieved.**

This is an incremental improvement task.

Do NOT rebuild the character.

Do NOT recreate the animation pipeline.

Do NOT replace the current weapon system.

Do NOT introduce new gameplay systems.

The objective is better animation, not more architecture.

---

# 2. CRITICAL PROJECT CONTINUITY

The Orc currently being developed in Character Factory is the authoritative MAIN ORC.

The historical Orc V4 is obsolete and must not be treated as a current production source.

Do not restore historical Orc assets or use old V4 manifests as authoritative references.

Inspect the current repository to determine:

- Current MAIN ORC masters.
- Current sword and axe masters.
- Current attack animations.
- Current approved poses.
- Current attachment metadata.
- Current production manifests.
- Current preview/export mechanisms.
- Current approval status.

The latest creator instructions take precedence over historical documentation.

### Preserve what already works

The most recent corrective work significantly improved:

- Weapon scaling.
- Weapon silhouettes.
- Grip positioning.
- Character-to-weapon alignment.
- Separate weapon presentation.
- Animation structure.

These improvements should be preserved.

Do not replace working poses merely because a new animation could theoretically be generated.

**Improve successful work through targeted refinements.**

---

# 3. MANDATORY INSPECTION

Before making changes, inspect the repository's current authoritative documentation and implementation.

Relevant known documents may include:

- `AGENTS.md`
- `handoff/AGENT_CONTEXT.md`
- `docs/VISUAL_IDENTITY.md`
- `docs/WORKFLOW.md`
- `docs/ASEPRITE.md`
- `docs/EQUIPMENT_AND_ACTIONS.md`
- `docs/RECIPES.md`
- `docs/ROADMAP.md`

Also inspect:

- Current PixelLab integration documentation.
- Current MAIN ORC character manifests.
- Current weapon sources.
- Attack animation frame sequences.
- Frame duration metadata.
- Grip and attachment data.
- Occlusion/layering rules.
- Existing preview generation scripts.
- Existing validation and QA tooling.

These paths are examples based on project history. Locate authoritative replacements if files have moved.

Inspect Git status and preserve unrelated changes.

If the latest playtest recording is available in the working context, inspect its actual animation frames.

Otherwise, inspect the equivalent current production previews and source animations.

Do not invent observations from an unavailable recording.

---

# 4. REQUIRED ARTISTIC AUDIT

Before refining the artwork, evaluate the current sword and axe animations frame by frame.

Classify each existing pose as:

- **KEEP:** artistically correct; should remain unchanged.
- **MINOR_POLISH:** good foundation requiring small corrections.
- **REWORK_POSE:** fundamentally weak pose requiring targeted redraw.
- **TIMING_ONLY:** good artwork with incorrect playback timing.
- **TRANSITION_FIX:** pose relationship or transition is the primary problem.

For every major correction, identify:

1. What is visually wrong.
2. Why the motion feels unnatural.
3. Which existing pose can be preserved.
4. Whether the correction belongs to body art, weapon art, attachment metadata or playback timing.
5. The smallest change likely to improve the animation.

Avoid unnecessary edits to successful frames.

### Important

Do not treat every motion problem as an attachment-coordinate problem.

A weapon can be perfectly attached and still produce a terrible-looking attack.

Evaluate the actual movement.

---

# 5. PRIORITY ONE — BODY MECHANICS AND WEIGHT TRANSFER

This is the highest-priority artistic improvement.

The current attacks rely too heavily on the weapon arm while the rest of the body remains relatively static.

The Orc should appear to produce force through coordinated body movement.

## Required improvements

Evaluate and refine:

- Stance.
- Foot support.
- Hip orientation.
- Torso rotation.
- Shoulder movement.
- Elbow trajectory.
- Wrist orientation.
- Balance.
- Weight transfer.
- Recovery posture.

The swing should communicate a coherent kinetic chain:

**Stance → Hips/Torso → Shoulder → Arm → Hand → Weapon**

This does not require physically realistic simulation.

It requires convincing visual cues.

### Pixel-art considerations

Subtle changes may be sufficient.

A few carefully placed pixels can communicate:

- Torso twisting.
- Weight shifting toward the leading leg.
- Shoulder extension.
- Body leaning into the strike.
- Recovery from momentum.

Do not exaggerate body deformation.

Do not change the Orc's overall anatomy, size or characteristic silhouette.

Do not produce uncontrolled perspective changes.

The character must remain compact, sturdy and visually consistent with the current approved art direction.

### Hard constraint

The Orc must not appear to be a stationary body with a rotating weapon attached to its arm.

---

# 6. PRIORITY TWO — TIMING AND SPACING

The current attacks have recognizable poses but do not always feel like continuous movements.

Some pose changes appear abrupt.

The objective is to improve perceived movement through correct timing and spacing.

## Review the existing timing

Inspect:

- Animation frame count.
- Individual frame durations.
- Distance between successive poses.
- Weapon trajectory between frames.
- Body displacement.
- Acceleration.
- Deceleration.
- Transition into recovery.

Do not automatically add frames.

First determine whether the existing poses can produce convincing motion through improved timing.

### Sword timing

The sword should generally convey:

- Clear but compact anticipation.
- Rapid acceleration.
- A readable strike.
- Controlled follow-through.
- Smooth recovery.

The swing should feel fast without becoming visually incomprehensible.

### Axe timing

The axe should convey:

- More deliberate anticipation.
- Perceptible mass toward the axe head.
- Fast committed acceleration.
- A forceful strike.
- Slightly heavier follow-through and recovery.

The axe should feel different from the sword.

### Spacing requirements

Do not distribute motion evenly if doing so makes it mechanical.

The attack should have recognizable rhythm.

Where appropriate:

- Smaller positional changes during anticipation.
- Larger changes during acceleration.
- A strong impact pose.
- Controlled deceleration.
- Natural recovery.

If additional in-between frames are necessary, add only those that materially improve the result.

Do not increase frame count simply to satisfy a perceived technical target.

Preserve actual frame-duration metadata and export consistency.

---

# 7. PRIORITY THREE — IMPACT AND ATTACK READABILITY

Both weapons need a stronger visual moment of impact.

The player should immediately recognize when the effective strike occurs.

## Sword impact

Improve:

- Blade direction.
- Body commitment.
- Shoulder and wrist alignment.
- Strike silhouette.
- Follow-through.
- Readability at normal playback speed.

The sword should appear to cut through a coherent arc.

Avoid a random sequence of disconnected blade orientations.

## Axe impact

Improve:

- Body weight commitment.
- Axe-head trajectory.
- Downward or diagonal chopping motion, as appropriate to the current animation.
- Follow-through.
- Sense of force.

The axe should communicate more mass than the sword.

### Impact emphasis

Appropriate artistic techniques may include:

- A particularly strong key pose.
- Brief timing emphasis.
- Subtle body compression.
- Small recoil or controlled follow-through.
- Clear directional silhouettes.
- Limited smear frames, only when compatible with the established visual style.

Do not introduce exaggerated cartoon effects that conflict with the game's serious fantasy identity.

Do not add new VFX, screen shake, sound effects or gameplay damage events in this task.

Those are separate concerns.

### Important distinction

The artistic impact frame is not authorization to change actual combat hit timing.

If animation metadata defines an impact event, keep it internally consistent and document any proposed timing change.

Do not modify Unity gameplay damage application.

---

# 8. PRIORITY FOUR — GRIP, ANATOMY AND OCCLUSION CLEANUP

The grip has improved significantly.

Do not rebuild the entire attachment system.

Perform a targeted inspection of problematic frames.

Check:

- Palm-to-handle contact.
- Finger/handle overlap.
- Wrist alignment.
- Forearm continuity.
- Elbow position.
- Shoulder connection.
- Weapon depth relative to the torso.
- Front/back layering.
- Weapon silhouette consistency.

### Acceptance requirements

The weapon must not:

- Float.
- Detach from the hand.
- Slide through the grip.
- Change apparent scale unexpectedly.
- Rotate around an incorrect pivot.
- Pass unnaturally through the body.
- Change hand contact points without a corresponding pose adjustment.

Correct artistic defects through the appropriate current Aseprite source and attachment metadata.

Maintain the body and weapon as independently editable assets.

Do not permanently bake the weapon into the body sprite.

Do not introduce a new rigging framework.

---

# 9. PRIORITY FIVE — ATTACK TRANSITIONS

The canonical weapon visibility policy remains:

- Idle: weapon hidden.
- Walk: weapon hidden.
- Attack: weapon visible.
- After Attack: weapon hidden.
- Hit and Defeat: no persistent weapon overlay by default.

### Refine Idle → Attack

The character must transition naturally from its idle pose into the attack sequence.

The weapon may appear as part of the initial attack pose, but it should not seem randomly attached halfway through an already-moving arm.

The initial armed pose must establish a believable grip.

Do not create elaborate draw-weapon animations.

### Refine Attack → Idle

Recovery must return the Orc toward its proper unarmed resting pose.

Prevent:

- Body snapping.
- Sudden changes in scale.
- Incorrect arm position.
- Residual weapon overlays.
- Stale weapon attachment.
- Inconsistent feet or ground pivot.

The disappearance of the weapon should occur at a coherent action boundary.

A completely separate sheathing animation is not necessary.

### Preserve simplicity

Attack-only visibility is a deliberate product decision.

Do not reintroduce armed Idle or Walk animations.

---

# 10. PRESERVE DISTINCT SWORD AND AXE PERSONALITIES

Sword and axe attacks must be visibly different.

However, both must remain compatible with the MAIN ORC's established body identity.

### Sword characteristics

- Relatively fast.
- Controlled.
- Directional.
- Fluid.
- Distinct blade arc.
- Shorter, more precise recovery.

### Axe characteristics

- More committed.
- Slightly heavier.
- Stronger anticipation.
- More pronounced body weight transfer.
- Convincing chopping trajectory.
- Recovery reflecting weapon-head momentum.

Avoid simply slowing down the exact same animation to represent a heavier weapon.

Differences should be evident in the poses and movement mechanics themselves.

---

# 11. EQUIPMENT REUSABILITY

Weapons remain separate assets.

The creator must be able to replace one compatible one-handed sword with another without redrawing the character's entire attack sequence.

The same applies to compatible one-handed axes.

Preserve the current reusable attack profiles wherever possible.

Improve existing attachment conventions rather than replacing them.

### Acceptable refinements

- Per-frame grip adjustments.
- Weapon-specific pivot registration.
- Limited scale normalization based on actual asset dimensions.
- Weapon-category-specific attack profiles.
- Per-frame orientation corrections.
- Improved occlusion metadata.

### Avoid

- One body animation per individual weapon.
- Universal animation frameworks for every planned weapon category.
- New inventory systems.
- New equipment gameplay.
- Complex skeletal animation.
- Unnecessary runtime dependencies.
- Rebuilding the current export architecture.

Do not compromise visual quality to make every possible weapon share one generic swing.

---

# 12. ASEPRITE + PIXELLAB WORKFLOW

The Character Factory currently integrates Aseprite and PixelLab.

Use the current approved workflow.

## Aseprite

Use Aseprite as the main environment for:

- Editing animation masters.
- Correcting individual pixels.
- Improving body poses.
- Refining grip.
- Adjusting frame timing.
- Preserving layers.
- Maintaining editable `.aseprite` sources.
- Exporting production candidates.

## PixelLab

PixelLab may assist with:

- Pose exploration.
- Controlled anatomical refinements.
- Limited inpainting.
- Generating candidate in-between poses.
- Refining difficult transitions.

Do not use PixelLab merely because it is available.

Prefer targeted edits to existing strong source artwork.

Generated content must preserve:

- Orc facial identity.
- Armor and clothing.
- Current palette.
- Pixel cluster quality.
- Perspective.
- Proportions.
- Character silhouette.

Generated candidates must pass the same artistic review requirements as any other artwork.

Use only configured and authorized external operations and credit budgets.

Do not overwrite authoritative masters with unreviewed generated material.

Maintain accurate provenance.

---

# 13. INCREMENTAL IMPLEMENTATION PLAN

Do not attempt another large-scale reconstruction.

Use these internal checkpoints.

## CHECKPOINT A — Artistic diagnosis

Inspect the current animations and classify existing frames.

Produce a concise improvement plan for both weapons.

Identify the most important problems in:

- Body mechanics.
- Timing.
- Impact.
- Grip.
- Transitions.

## CHECKPOINT B — Sword refinement

Refine the current sword animation.

Start with the canonical active front-facing diagonal view (`front_r`, if still applicable).

Prioritize body mechanics and timing.

Keep successful poses intact.

Export an isolated review candidate.

## CHECKPOINT C — Axe refinement

Refine the current axe animation.

Preserve its corrected one-handed proportions.

Increase the perception of weight and physical effort.

Export an isolated review candidate.

## CHECKPOINT D — Transition cleanup

Validate:

- Idle → Sword Attack → Idle.
- Idle → Axe Attack → Idle.
- Weapon appearance and disappearance.
- Body restoration.
- Ground alignment.
- Grip continuity.

## CHECKPOINT E — Comparative QA

Review current and refined animations side by side.

Compare:

- Movement clarity.
- Body participation.
- Weapon weight.
- Impact.
- Fluidity.
- Grip.
- Consistency.

Identify any regression relative to the current improved animations.

## CHECKPOINT F — Review delivery

Produce inspectable preview assets for creator evaluation.

Do not automatically propagate the refined animation to additional directions, characters or weapon families.

Wait for artistic approval before broad propagation.

---

# 14. PREVIEW AND REVIEW REQUIREMENTS

Use or extend the existing local preview system.

Do not build an entirely new preview application unless the current one cannot support essential review.

Provide:

1. Current sword animation.
2. Refined sword animation.
3. Current axe animation.
4. Refined axe animation.
5. Side-by-side playback.
6. Normal-speed playback.
7. Slow-motion playback.
8. Frame-by-frame inspection.
9. Key-pose comparison.
10. Looping Idle → Attack → Idle.

Where possible, include:

- Frame duration labels.
- Frame index.
- Grip close-up.
- Highlighted impact frame.
- Native pixel-art zoom.

Use real exported frames and actual timing metadata.

Do not artificially improve visual quality using preview-only interpolation, motion smoothing or unrelated transformations.

The preview must accurately represent the candidate production assets.

---

# 15. ARTISTIC QUALITY GATES

A candidate does not pass artistic QA merely because it exports correctly.

## Sword

Evaluate:

- Natural grip.
- Body participation.
- Clear anticipation.
- Convincing blade trajectory.
- Readable impact.
- Smooth follow-through.
- Controlled recovery.
- Character identity preservation.

## Axe

Evaluate:

- Correct one-handed proportions.
- Convincing weight.
- Body commitment.
- Natural grip.
- Strong chopping trajectory.
- Distinct impact.
- Controlled recovery.
- Character identity preservation.

## Shared quality failures

Reject or flag candidate frames if they demonstrate:

- Floating weapons.
- Broken anatomy.
- Arbitrary blade orientation.
- Mechanical rotating-sprite motion.
- Sudden character scale changes.
- Unnatural torso twisting.
- Disconnected motion.
- Excessive deformation.
- Weak or unreadable impact.
- Abrupt transition artifacts.
- Significant loss of previously achieved quality.

### Important

Artistic quality is not fully measurable through automated tests.

A QA agent may provide qualitative findings and recommendations, but must not claim definitive creator approval.

The creator remains the final artistic authority.

---

# 16. TECHNICAL REGRESSION VALIDATION

Verify that the refinement does not break existing functionality.

Relevant checks include:

- Current MAIN ORC asset resolution.
- Current sword asset resolution.
- Current axe asset resolution.
- Correct frame references.
- Correct frame duration metadata.
- Correct weapon category assignment.
- Stable grip registration.
- Consistent canvas dimensions.
- Correct ground pivot.
- No unintended frame displacement.
- Weapon hidden outside Attack.
- Weapon visible during Attack.
- Correct animation completion.
- No stale weapon overlays.
- Valid `.aseprite` sources.
- Reproducible exports.
- Valid preview loading.
- No duplicate or unexpected production assets.
- Preservation of unrelated character sources.
- No accidental selection of obsolete Orc versions.

Add focused tests where a meaningful technical contract is missing.

Do not generate dozens of redundant tests.

A technical PASS does not imply artistic approval.

---

# 17. DOCUMENTATION

Update the relevant current Character Factory documentation.

Record:

- What was artistically deficient.
- Which poses were preserved.
- Which poses were refined.
- Body mechanics improvements.
- Timing changes.
- Impact-frame decisions.
- Grip and occlusion refinements.
- Attack transition behavior.
- Weapon reuse considerations.
- QA results.
- Remaining artistic limitations.

Update the relevant roadmap section.

Do not rewrite unrelated documentation.

Do not modify Unity documentation.

The current MAIN ORC must remain the production authority.

Historical Orc V4 material must not be restored.

---

# 18. SCOPE RESTRICTIONS

DO NOT:

- Redesign the MAIN ORC.
- Revert to the obsolete Orc V4.
- Rebuild the Character Factory.
- Reimplement equipment architecture.
- Modify Unity.
- Create new Jobs.
- Add new weapons.
- Add new combat mechanics.
- Reintroduce armed Idle/Walk.
- Add sheathing or drawing systems.
- Redesign the current sword and axe unnecessarily.
- Propagate to all outfits or directions.
- Produce a new character generation pipeline.
- Replace approved unrelated animations.
- Perform large uncontrolled PixelLab generation batches.
- Create Git commits without authorization.

### Modification principle

**Only change what is necessary to meaningfully improve the current attack animations.**

Avoid speculative architectural work.

---

# 19. WORKSPACE SAFETY

Before editing:

1. Inspect Git status.
2. Identify unrelated uncommitted work.
3. Preserve the current improved animation sources.
4. Create recoverable candidates.
5. Work within the current approved production workflow.
6. Validate exports before replacing generated derivatives.
7. Review the complete final diff.

Do not use destructive repository resets or cleanup.

Do not interfere with an open Aseprite session containing unsaved creator work.

Prefer documented noninteractive production operations when appropriate.

Do not treat approval of this task as permission to overwrite unrelated current assets.

---

# 20. INDEPENDENT ARTISTIC QA

After producing refined candidates, perform an independent review using a suitable separate agent if available.

The QA reviewer should inspect actual frame sequences and playback output.

Review:

- Hand anatomy.
- Weapon grip.
- Body mechanics.
- Timing and spacing.
- Impact readability.
- Silhouette consistency.
- Transition continuity.
- Perspective stability.
- Preservation of MAIN ORC identity.
- Regression against the current improved animations.

Do not ask QA to approve the implementation solely from code inspection.

If the reviewer lacks access to visual evidence, explicitly state the limitation.

QA findings must distinguish:

- Confirmed visual problems.
- Suspected issues.
- Subjective improvement opportunities.
- Technical defects.

Prioritize significant defects over minor cosmetic preferences.

---

# 21. FINAL REPORT

Deliver a clear report containing:

## A. Before/after assessment

For each weapon:

- Problems identified.
- Corrections performed.
- Poses preserved.
- Poses modified.
- Timing changes.
- Remaining limitations.

## B. Technical changes

- Files modified.
- Master/source revisions.
- Animation metadata changes.
- Attachment changes.
- Export paths.

## C. Artistic QA

- Improvements in body mechanics.
- Improvements in timing.
- Improvements in impact.
- Improvements in grip.
- Transition quality.
- Any remaining artistic concerns.

## D. Validation

- Technical tests executed.
- Results.
- Preview validation.
- Unverified conditions.
- External PixelLab operations and costs, if any.

## E. Review materials

Provide precise local paths for:

- Sword comparison.
- Axe comparison.
- Frame-by-frame inspection.
- Combined Idle → Attack → Idle preview.

## F. Safety and continuity

- Git diff summary.
- Confirmation that the current MAIN ORC remains authoritative.
- Confirmation that Unity was not modified.
- Confirmation that unrelated assets were preserved.
- Confirmation that weapon visibility remains attack-only.

## G. Acceptance status

Explicitly distinguish:

- Implemented.
- Technically validated.
- Visually reviewed.
- Pending creator approval.

Do not mark artistic approval as complete without creator acceptance.

---

# 22. EXECUTION AUTHORIZATION

Implement this focused animation refinement now.

Authorized:

- Improve the MAIN ORC's current one-handed sword attack.
- Improve the MAIN ORC's current one-handed axe attack.
- Refine body poses.
- Improve torso participation and weight transfer.
- Refine timing and spacing.
- Improve impact frames.
- Correct residual grip and occlusion defects.
- Improve Idle/Attack transitions.
- Preserve separate weapon assets.
- Update relevant production documentation.
- Produce reviewable previews.
- Run targeted tests and QA.

Not authorized:

- Full artistic redesign.
- Historical Orc restoration.
- Unity changes.
- New equipment architecture.
- Mass propagation of animations.
- Automatic artistic approval.
- Unrelated character or asset modifications.

### FINAL DIRECTIVE

**Do not start over. Refine what is already working.**

The MAIN ORC should communicate genuine physical effort when swinging a sword or axe.

The sword must feel controlled and fluid.

The axe must feel heavier and more committed.

The body, hand and weapon must act as one connected movement.

Preserve visual identity, equipment reusability and the improvements achieved in the previous correction.

**Deliver fewer but better changes, supported by clear before/after visual evidence.**