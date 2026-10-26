# TASK — TACTICSRPG CHARACTER FACTORY
# Main Orc: Natural Weapon Entry & Attack Transition Polish

## TASK CLASSIFICATION

Targeted artistic refinement of the current MAIN ORC's one-handed sword and axe attack animations.

**Primary focus:** natural transition from unarmed Idle to the first armed attack pose.

**Secondary focus:** arm anatomy, weapon trajectory, body mechanics and recovery continuity.

**Target repository:** TacticsRPG Character Factory.

**Scope:** current sword and axe attack candidates, beginning with the views demonstrated in the latest preview.

---

# 1. OBJECTIVE

Refine the MAIN ORC's current one-handed sword and axe animations so that the beginning of each attack looks anatomically coherent, visually continuous and physically convincing.

The recent animation improvements must be preserved.

The creator considers the current result substantially better than earlier versions, but the transition into the armed attack remains unnatural.

In particular, the weapon appears to enter the animation without convincing preparation by the character's shoulder, elbow, wrist and gripping hand.

The objective is NOT to rebuild the attacks.

**Improve the transition into the weapon strike while preserving the existing successful poses, independent weapon assets and established visual identity.**

Also correct directly related animation issues when doing so improves the overall movement without expanding the task unnecessarily.

---

# 2. CURRENT PROJECT AUTHORITY

The Orc currently under development in Character Factory is the authoritative MAIN ORC.

The historical Orc V4 is obsolete.

Do not restore or use historical V4 assets as the current production source.

Inspect the actual repository to identify:

- Current MAIN ORC master files.
- Current sword and axe assets.
- Current attack animations.
- Current animation profiles.
- Current hand/grip metadata.
- Current frame durations.
- Current production preview.
- Current Aseprite and PixelLab workflows.

Preserve the MAIN ORC's identity, armor, face, palette, proportions, pixel-art style and recognizable silhouette.

Corrections to defective body poses are authorized.

Unrelated character redesigns are not.

---

# 3. CANONICAL WEAPON VISIBILITY POLICY

The creator has deliberately simplified equipped-weapon presentation.

For this task:

- Idle: no weapon.
- Walk: no weapon.
- Normal resting state: no weapon.
- Attack: equipped weapon visible during the appropriate attack sequence.
- After Attack: weapon hidden.
- Hit/Defeat: no persistent weapon overlay unless separately authorized.

Weapons remain independent assets.

Do not reintroduce armed Idle or Walk animations.

Do not introduce a new sheathing, drawing or holstering system.

## Critical interpretation

The creator describes the unnatural beginning of the attack as "drawing the weapon."

However, the current visual contract does not include a visible sheath, holster or persistent carried weapon.

Therefore, do not interpret this request as authorization to create an actual unsheathing mechanic.

Instead, solve the problem as an **attack-entry animation transition**.

The character must naturally establish an armed attack pose.

The equipped weapon should appear at a coherent moment, already aligned with the character's gripping hand.

Its visual introduction must not resemble an arbitrary floating object, sudden disjointed arm pose or unexplained mid-swing teleportation.

Do not invent additional lore or magical materialization effects to justify the presentation.

Keep the existing streamlined combat-animation philosophy.

---

# 4. MANDATORY ARTISTIC AND TECHNICAL INSPECTION

Before changing anything, inspect the active Character Factory source and documentation.

Relevant known documents may include:

- `AGENTS.md`
- `handoff/AGENT_CONTEXT.md`
- `docs/VISUAL_IDENTITY.md`
- `docs/WORKFLOW.md`
- `docs/ASEPRITE.md`
- `docs/EQUIPMENT_AND_ACTIONS.md`
- `docs/RECIPES.md`
- `docs/ROADMAP.md`

Also inspect the actual active:

- Aseprite masters.
- PixelLab integration contracts.
- Sword attack body frames.
- Axe attack body frames.
- Weapon sources.
- Weapon pivots.
- Grip/attachment points.
- Occlusion layers.
- Per-frame timing.
- Preview generation code.
- Export manifests.
- Relevant automated validations.

Paths are historical guidance, not proof of the current repository structure.

Locate the current authoritative equivalents where necessary.

Inspect Git status.

Preserve unrelated uncommitted work.

Do not modify the sibling Unity repository.

---

# 5. VIDEO-BASED OBSERVATIONS

The creator's latest approximately 48-second recording shows a local Character Factory preview of the current sword and axe attack candidates.

The following observations are visual evidence, not confirmed code-level root causes.

## Sword — approximately 11.85–12.17 seconds

The weapon is initially shown low and almost horizontally toward the left side of the character.

Shortly afterward, the weapon is elevated beside the Orc's head.

The transition does not sufficiently communicate the intervening motion of the arm and upper body.

It can look like the Orc suddenly assumes a weapon-ready posture instead of reaching that posture naturally.

Investigate:

- First armed frame.
- Previous unarmed pose.
- Shoulder position.
- Elbow path.
- Wrist angle.
- Hand-to-handle registration.
- Weapon pivot.
- Transition timing.
- Missing or poorly selected connecting poses.

## Sword — approximately 12.25–12.49 seconds

The strike becomes more readable, but the arm/body composition can still feel somewhat rigid as the weapon passes across the front of the torso.

Review:

- Shoulder rotation.
- Elbow position.
- Forearm anatomy.
- Armor occlusion.
- Blade trajectory.
- Torso contribution.

## Sword — approximately 12.57–12.81 seconds

Review the recovery into Idle.

The body should not abruptly abandon the striking posture simply because the weapon becomes hidden.

## Axe — approximately 32.12–32.60 seconds

The initial armed pose has the axe projected forward.

The movement still risks reading as an isolated arm gesture rather than a physically motivated attack preparation.

Review:

- Shoulder and elbow articulation.
- Forearm angle.
- Wrist orientation.
- Body balance.
- Axe head trajectory.
- Grip continuity.
- Transition from unarmed posture.

## Axe — approximately 32.68–33.16 seconds

Review follow-through and recovery.

The weight of the axe head should remain perceptible as the character returns to Idle.

### Evidence limitations

Do not assume these timestamps prove any particular implementation defect.

Inspect actual production frames and metadata to establish the causes.

The recording is a local preview and does not prove Unity runtime integration or correctness in every directional view.

---

# 6. PRIMARY CORRECTION — NATURAL ATTACK ENTRY

This is the most important requirement.

The animation must establish a coherent transition:

**Unarmed Idle → Body preparation → Valid armed attack pose → Strike**

The transition must not appear as:

**Unarmed Idle → Sudden disconnected weapon/arm pose → Strike**

## 6.1 Anatomical continuity

Ensure that the first attack poses are compatible with the preceding Idle pose.

The following must move consistently:

- Shoulder.
- Upper arm.
- Elbow.
- Forearm.
- Wrist.
- Hand.
- Upper torso.

The shoulder must not appear detached from the arm's movement.

The elbow must follow a plausible path.

The forearm must remain anatomically connected.

The wrist must support the actual orientation of the weapon handle.

The hand must visually grip the weapon, not merely touch its sprite.

## 6.2 Anticipation

Introduce a convincing preparatory gesture.

Possible artistic solutions include:

- A compact shift in stance.
- A subtle shoulder rotation.
- A slight torso lean.
- A readable arm preparation.
- A brief redistribution of weight.
- A carefully selected intermediate pose.

These are options, not mandatory additions.

Choose the smallest combination that produces a convincing result.

Do not add a lengthy animation just to make the weapon's introduction appear technically justified.

Combat responsiveness matters.

## 6.3 First visible weapon frame

The first frame containing the weapon must:

- Show a valid one-handed grip.
- Align the hand and handle convincingly.
- Maintain correct wrist anatomy.
- Be compatible with the preceding body pose.
- Preserve character proportions.
- Avoid sudden position or scale discontinuities.
- Establish the intended attack direction.

The weapon should not appear visibly disconnected from the hand.

If the first armed pose is incompatible with the preceding unarmed posture, refine the entry body pose rather than merely relocating the weapon.

## 6.4 Transition timing

Use appropriate timing and spacing.

Avoid:

- A long static hold followed by a sudden large movement.
- A weapon appearing before the hand is ready.
- A drastic jump in elbow or shoulder position.
- An unnatural pause between preparation and strike.
- Excessively slow anticipation that makes combat feel sluggish.

Review the motion at actual intended gameplay speed.

A transition that appears acceptable at 0.5× speed may still look abrupt at normal speed.

---

# 7. SWORD-SPECIFIC REFINEMENT

The one-handed sword attack should feel:

- Controlled.
- Decisive.
- Fluid.
- Anatomically coherent.
- Faster and more precise than the axe attack.

## Required review

Examine the progression from the initial armed pose to the raised-sword position.

Determine whether the current sequence contains an excessively abrupt change of weapon direction or arm position.

Correct the transition with the minimum necessary pose and timing adjustments.

Ensure:

- The elbow leads naturally into the strike.
- The shoulder supports the overhead or diagonal preparation.
- The wrist does not abruptly reverse orientation.
- The sword maintains a coherent arc.
- The torso participates without excessive deformation.
- The hand remains properly attached.
- The strike retains a readable impact pose.

### Torso crossing and occlusion

When the sword and arm move across the chest:

- Review armor layering.
- Avoid implausible intersections.
- Preserve readable silhouette.
- Keep shoulder and forearm anatomy coherent.
- Avoid hiding the gripping hand in a way that makes the weapon appear to float.

Do not convert the attack into a completely different technique unless the current animation cannot be corrected satisfactorily.

Preserve existing successful key poses.

---

# 8. AXE-SPECIFIC REFINEMENT

The one-handed axe attack should feel:

- Heavier than the sword.
- More committed.
- Deliberate during anticipation.
- Forceful during acceleration.
- Stable and balanced during recovery.

## Required review

The current initial axe pose is too reliant on the projected weapon arm.

Improve the body mechanics supporting the attack.

Consider:

- A more natural initial elbow angle.
- Better shoulder alignment.
- Subtle torso participation.
- Correct wrist orientation.
- Improved connection between stance and strike.
- More convincing axe-head momentum.

### Weight distribution

A one-handed axe has a different balance from a sword.

Its attack should communicate mass concentrated toward the head.

This can be represented through:

- Appropriate anticipation.
- Accelerating motion.
- Strong key poses.
- Clear follow-through.
- Controlled recovery.

Do not exaggerate the axe's physical dimensions.

Do not turn the movement into a two-handed attack.

Do not reuse the sword's exact animation and merely change playback speed.

---

# 9. SECONDARY REFINEMENT — BODY MECHANICS

Review whether the current animations rely excessively on shoulder and arm movement while the lower body remains static.

Do not automatically create foot movement.

For short tactical attacks, a planted stance can be appropriate.

However, the upper-body motion must be supported by believable balance.

Evaluate:

- Foot support.
- Knee flexion.
- Hip alignment.
- Torso rotation.
- Shoulder movement.
- Center of mass.
- Recovery balance.

Use restrained pixel-level adjustments.

Avoid:

- Unnecessary foot sliding.
- Ground pivot displacement.
- Exaggerated body deformation.
- Unstable character proportions.
- Unintended perspective changes.

The Orc should remain heavy, compact and visually consistent.

---

# 10. SECONDARY REFINEMENT — RECOVERY CONTINUITY

Review the transition:

**Strike → Follow-through → Recovery → Unarmed Idle**

The weapon should disappear at a coherent action boundary.

However, hiding the weapon must not force the body to snap instantly into Idle.

Ensure that:

- The attack finishes its physical movement.
- The arm returns plausibly.
- The torso regains balance.
- Hand position remains coherent.
- Weapon visibility ends at the intended moment.
- The final attack pose connects naturally with Idle.

Do not add weapon-sheathing animations.

Do not reintroduce persistent weapon visibility.

Do not unnecessarily increase attack duration.

The result should remain responsive for a tactical RPG.

---

# 11. PRESERVE SUCCESSFUL WORK

The previous refinements substantially improved the animations.

Treat the current production state as the baseline for this task.

Before changing frames, classify important existing poses:

- KEEP
- MINOR_POLISH
- REWORK_POSE
- TIMING_ONLY
- TRANSITION_FIX

Preserve successful poses when possible.

Do not regenerate the entire animation simply to fix the first frames.

Do not redesign:

- Orc face.
- Armor.
- Body proportions.
- Character palette.
- Sword identity.
- Axe identity.
- Overall pixel-art style.

Improve only the parts necessary to achieve convincing animation continuity.

---

# 12. WEAPON INDEPENDENCE AND REUSABILITY

Maintain the existing separation between:

- Character body animation.
- Weapon source asset.
- Weapon attachment metadata.
- Animation timing.
- Runtime-ready derivatives.

The implementation must continue supporting weapon replacement without requiring a complete new body animation for every compatible sword or axe.

Acceptable corrections include:

- Per-frame grip positions.
- Weapon pivot alignment.
- Specific attachment orientations.
- Localized body pose changes.
- Layer/occlusion corrections.
- Weapon-family-specific attack timing.

Do not create a universal equipment architecture.

Do not introduce skeletal rigging unless a genuine existing dependency requires it.

Do not modify weapon dimensions merely to conceal attachment mistakes.

Preserve the established one-handed sword and axe categories.

---

# 13. ASEPRITE + PIXELLAB

Use the Character Factory's currently authorized Aseprite and PixelLab workflow.

## Aseprite

Primary tool for:

- Editing current source masters.
- Correcting attack poses.
- Refining anatomy.
- Improving transitions.
- Adjusting frame timing.
- Updating grip/occlusion.
- Maintaining layers.
- Producing review candidates.

## PixelLab

May assist with:

- Local pose corrections.
- Anatomical refinements.
- Candidate intermediate poses.
- Controlled inpainting.

Use PixelLab only where it provides meaningful artistic value.

Do not:

- Perform mass regeneration.
- Replace the MAIN ORC design.
- Overwrite active masters with unreviewed candidates.
- Lose provenance.
- Spend unapproved external credits.
- Introduce inconsistent pixel-art rendering.

Prefer targeted improvements to the current source artwork.

---

# 14. FOCUSED IMPLEMENTATION CHECKPOINTS

## Checkpoint A — Current-state audit

Inspect the real active animations.

Identify the specific entry poses and frame transitions responsible for the perceived unnatural weapon introduction.

Determine whether each problem comes from:

- Body artwork.
- Grip placement.
- Weapon orientation.
- Frame timing.
- Occlusion.
- Preview playback.

Do not assume all defects share one cause.

## Checkpoint B — Sword entry correction

Correct the transition from unarmed Idle into the sword attack.

Preserve the strongest existing strike and recovery poses.

Produce a revised candidate.

## Checkpoint C — Axe entry correction

Correct the transition from unarmed Idle into the axe attack.

Preserve appropriate one-handed proportions and existing successful motion.

Produce a revised candidate.

## Checkpoint D — Secondary corrections

Address directly related problems in:

- Torso participation.
- Arm crossing.
- Impact readability.
- Follow-through.
- Recovery.

Keep the changes proportional.

## Checkpoint E — Validation evidence

Prepare reviewable output showing exactly what changed.

Do not propagate automatically to every direction, character or equipment variant.

---

# 15. PREVIEW AND COMPARISON REQUIREMENTS

Use the existing Character Factory review system.

Do not build a new preview framework.

Provide real animation playback for:

1. Current sword attack.
2. Refined sword attack.
3. Current axe attack.
4. Refined axe attack.
5. Idle → Sword Attack → Idle.
6. Idle → Axe Attack → Idle.

The preview must support or preserve existing useful controls, such as:

- Play/Pause.
- Frame stepping.
- Normal speed.
- Slow motion.
- Native pixel-art zoom.
- Side-by-side comparison.

Where possible, make the following especially easy to inspect:

- Last unarmed frame.
- First frame with weapon.
- Initial grip.
- First anticipation pose.
- Transition to strike.
- Impact frame.
- Final armed frame.
- Return to Idle.

Use actual exported frames and authentic timing metadata.

Do not use smoothing or preview-only interpolation to conceal defects.

### Useful additional evidence

If straightforward within the current preview system, include:

- Grip-point visualization.
- Hand and weapon pivot markers.
- Frame duration labels.
- Highlighting of changed frames.

These are diagnostic aids, not requirements for a new UI system.

---

# 16. ACCEPTANCE CRITERIA

The task is technically complete when:

- Current authoritative MAIN ORC sources are used.
- Sword entry transition has been refined.
- Axe entry transition has been refined.
- Existing successful attack poses are preserved where possible.
- Weapons remain independent assets.
- Idle and Walk remain weaponless.
- Weapon visibility is limited to the intended attack interval.
- Frame ordering and durations are valid.
- Exports and previews are reproducible.
- No unrelated assets or systems are modified.

## Artistic acceptance criteria

The candidate should demonstrate:

1. Anatomically coherent transition from Idle to attack.
2. Shoulder and elbow positions consistent with the arm movement.
3. Plausible wrist orientation.
4. Convincing grip before and during the strike.
5. No visibly floating or disconnected weapon.
6. No unexplained large jumps in weapon position or orientation.
7. Readable anticipation without excessive delay.
8. Coherent sword trajectory.
9. Coherent axe trajectory and sense of weight.
10. Appropriate torso and body participation.
11. Clear strike and follow-through.
12. Natural return toward unarmed Idle.
13. Stable character proportions.
14. Preservation of the MAIN ORC's visual identity.
15. No regression in the improvements achieved by previous refinement tasks.

### Important

Artistic credibility cannot be proven by checking attachment coordinates alone.

A valid export is not proof that an animation looks natural.

The final artistic approval belongs to the creator.

Do not claim creator approval automatically.

---

# 17. TECHNICAL VALIDATION

Use existing testing and validation infrastructure.

Verify relevant contracts:

- Current asset selection.
- Correct sword profile.
- Correct axe profile.
- Frame index validity.
- Timing metadata.
- Hand/weapon registration.
- Pivot consistency.
- No unintended scale drift.
- Stable ground anchoring.
- Independent weapon references.
- Attack-only visibility.
- Correct return to Idle.
- Valid exports.
- Valid preview rendering.
- Preserved source provenance.

Add focused automated tests only where they protect meaningful technical behavior.

Do not create arbitrary test counts.

Distinguish technical validation from artistic acceptance.

The creator's separate orchestration prompt handles independent QA.

**Do not request, assign or organize additional QA agents.**

---

# 18. DOCUMENTATION

Update the relevant current Character Factory documentation.

Record:

- The observed attack-entry problem.
- Confirmed technical/artistic causes.
- Corrected transition behavior.
- Any adjusted frame timing.
- Relevant anatomy and attachment conventions.
- Sword-specific considerations.
- Axe-specific considerations.
- Recovery behavior.
- Preserved equipment-reuse rules.
- Current candidate approval status.
- Known limitations.

Update the current roadmap where appropriate.

Do not create redundant documentation.

Do not restore historical Orc V4 references as current authority.

---

# 19. SAFETY AND SCOPE BOUNDARIES

This task is authorized only within the Character Factory.

Do not modify the Unity project.

Do not:

- Redesign the MAIN ORC.
- Rebuild the weapon framework.
- Implement inventory systems.
- Add weapon-drawing or sheathing mechanics.
- Create persistent armed Idle/Walk.
- Add new weapon designs.
- Create new Jobs or races.
- Modify combat damage or gameplay rules.
- Change unrelated sprites.
- Regenerate all animation directions.
- Propagate changes across every outfit.
- Perform uncontrolled PixelLab generations.
- Overwrite unrelated creator work.
- Use destructive Git operations.
- Create commits without authorization.

Inspect Git status first.

Preserve uncommitted work.

Maintain recoverable artistic sources.

Use the existing approved noninteractive Aseprite workflow where applicable.

Do not interfere with an open editing session containing unsaved work.

---

# 20. FINAL TECHNICAL DELIVERABLES

Provide:

1. Current MAIN ORC source identification.
2. Confirmed causes of the unnatural weapon-entry movement.
3. Sword frames/poses refined.
4. Axe frames/poses refined.
5. Timing changes, if any.
6. Grip and attachment corrections, if any.
7. Body-mechanics improvements.
8. Recovery improvements.
9. Before/after preview paths.
10. Edited `.aseprite` source paths.
11. Exported candidate paths.
12. Technical tests and results.
13. Remaining artistic limitations.
14. Updated documentation.
15. Git diff summary.
16. Clear indication that creator artistic approval is still pending.

Do not request a new independent QA process.

The separate orchestration workflow handles QA and execution management.

---

# FINAL DIRECTIVE

**Refine the existing animation; do not rebuild it.**

The primary goal is to make the beginning of the sword and axe attacks feel natural.

The MAIN ORC should not abruptly jump from unarmed Idle into an anatomically disconnected weapon pose.

His shoulder, elbow, forearm, wrist, hand and weapon must form a coherent movement.

The sword should feel controlled and fluid.

The axe should feel heavier and more committed.

The weapon remains a separate asset and appears only during the attack.

Preserve the improvements already achieved, the character's visual identity and the factory's reusable production pipeline.

Deliver focused corrections and clear before/after evidence for creator approval.