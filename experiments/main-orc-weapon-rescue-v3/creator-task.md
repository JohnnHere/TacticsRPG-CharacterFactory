# TASK — TACTICSRPG CHARACTER FACTORY
# Main Orc — One-Handed Weapon Animation Rescue
## Natural Grip, Correct Proportions, Convincing Attacks and Attack-Only Weapon Visibility

---

# 1. ROLE AND PRIMARY OBJECTIVE

Act as a Senior Pixel Art Animation Director, Technical Artist, Character Animation Engineer and Production Pipeline Specialist.

Work in the **TacticsRPG Character Factory** repository.

Your task is to correct the currently unacceptable quality of the MAIN ORC's one-handed sword and axe animations.

The creator has reviewed the existing local animation preview and identified major artistic failures:

- Weapons are held unnaturally.
- Hands do not convincingly grip the handles.
- Arm movements are poorly coordinated with weapon movement.
- Attacks look artificial and mechanically animated.
- The one-handed axe is excessively large.
- Weapon proportions are inconsistent with their intended category.
- Weapons move unnaturally during Idle and Walk.
- The overall result does not meet the project's artistic standards.

The current implementation requires a substantial artistic correction, not merely a minor coordinate adjustment.

**Primary objective: make the MAIN ORC perform visually convincing one-handed sword and axe attacks while keeping the weapons independently replaceable.**

Prioritize animation quality, anatomical credibility, visual consistency and maintainability.

Do not introduce unnecessary complexity.

---

# 2. CRITICAL PROJECT CONTINUITY CORRECTION

## THE CURRENT ORC IS THE AUTHORITATIVE CHARACTER

The creator has explicitly clarified:

**THE PREVIOUS ORC V4 NO LONGER EXISTS AS THE CURRENT PRODUCTION VERSION.**

The Orc currently being developed in this repository is the **MAIN ORC**.

It is the active character whose sword and axe animations must be corrected.

Therefore:

- Do not assume Orc V4 remains the approved character.
- Do not use historical Orc V4 artwork as the mandatory artistic reference.
- Do not restore older Orc V4 sources.
- Do not select assets merely because historical documentation identifies them as V4.
- Do not compare the current Orc against obsolete versions as though the older version had greater authority.
- Do not overwrite current artwork using historical masters.
- Do not attempt to reproduce an obsolete character design.
- Do not rely on old asset counts, manifests or production reports without checking their present validity.

If historical documents contradict the current production state, identify the discrepancy and follow the creator's latest decision.

The MAIN ORC currently present in the Character Factory is the authoritative visual character.

Determine its actual source files, animation structure, production status and current references through repository inspection.

### Important distinction

Preserving the MAIN ORC's identity does NOT mean preserving defective animation frames.

You are explicitly authorized to improve:

- Body poses.
- Arm positions.
- Wrist orientations.
- Hand shapes.
- Weapon handling.
- Attack timing.
- Animation silhouettes.
- Necessary animation transitions.
- Weapon scale and attachment points.

As long as these corrections preserve the character's recognizable visual identity.

**Do not treat poor animations as untouchable approved artwork.**

---

# 3. NEW CANONICAL EQUIPMENT PRESENTATION POLICY

The creator has decided to simplify the game's weapon presentation.

## WEAPONS APPEAR ONLY WHEN USED

For the current one-handed melee weapon implementation:

| Character state | Weapon visibility |
|---|---|
| Idle | Hidden |
| Walk | Hidden |
| Normal resting state | Hidden |
| Free inspection | Hidden |
| Attack | Visible during the appropriate attack sequence |
| After Attack | Hidden |
| Hit | Hidden by default |
| Defeat | Hidden by default |

This decision replaces previous requirements for permanently visible weapons during Idle or Walk.

Update the current documentation accordingly.

### Important behavior

The character should not appear to carry a sword or axe while walking or standing still.

When attacking:

1. The equipped weapon becomes visible at the appropriate beginning of the attack sequence.
2. The Orc convincingly grips and uses the weapon.
3. The weapon follows the hand and attack movement.
4. The attack concludes naturally.
5. The weapon becomes hidden when the action finishes.

The weapon must not randomly teleport between positions while visible.

However, do not implement unnecessary drawing, sheathing, inventory or equip/unequip animations.

The disappearance of the weapon outside the attack is intentional.

### Keep the system simple

Do not introduce:

- Persistent weapon-holding states.
- Armed walking cycles.
- Armed idle cycles.
- Sheathing systems.
- Drawing animations.
- Advanced inventory presentation.
- Unnecessary skeletal frameworks.
- Separate body animations for every individual sword or axe.

The goal is an effective, reusable tactical RPG attack animation system.

---

# 4. MANDATORY REPOSITORY AUDIT

Before modifying any artwork or implementation, inspect the current Character Factory repository.

Read the available authoritative documents, including relevant files such as:

- `AGENTS.md`
- `handoff/AGENT_CONTEXT.md`
- `docs/VISUAL_IDENTITY.md`
- `docs/WORKFLOW.md`
- `docs/ASEPRITE.md`
- `docs/EQUIPMENT_AND_ACTIONS.md`
- `docs/RECIPES.md`
- `docs/ROADMAP.md`
- Current character production documentation
- Current weapon production documentation
- Current Aseprite integration documentation
- Current PixelLab integration documentation
- Current asset manifests
- Current animation and attachment configuration
- Current preview implementation

These are known historical paths, not guaranteed current paths.

Locate the actual authoritative files if they have been moved or renamed.

### Required investigation

Determine:

1. Which Orc source is currently authoritative.
2. Where its editable `.aseprite` masters are located.
3. Which sword and axe assets are currently selected.
4. Which animation source files and exports are active.
5. How body poses are generated or edited.
6. How weapons are attached to the hands.
7. Whether attachment points differ per animation frame.
8. How weapon rotation and scale are currently calculated.
9. How weapon occlusion is handled.
10. How Idle, Walk and Attack sequences are presented.
11. How the local preview loads and displays animation data.
12. Which production gates currently apply.
13. Which historical documentation has become obsolete.

Inspect Git status before making changes.

Preserve unrelated uncommitted work.

### Source-of-truth precedence

1. Creator's latest explicit decisions.
2. Current authoritative production files.
3. Current approved artistic references.
4. Current production documentation.
5. Historical reports and obsolete handoffs.

If the repository contains contradictory historical instructions, document the conflict.

Do not silently restore a deprecated pipeline.

---

# 5. ROOT-CAUSE ANALYSIS

Investigate the current animation problems before implementing the correction.

Do not assume they can be solved simply by moving a weapon attachment point.

Potential causes include:

- Incorrect hand-to-handle alignment.
- Incorrect grip location.
- Improper wrist orientation.
- Poor forearm and elbow poses.
- Lack of shoulder participation.
- Insufficient torso rotation.
- Incorrect weapon dimensions.
- Inconsistent weapon scale between frames.
- Incorrect weapon pivot.
- Overreliance on rigid sprite transformations.
- Poor timing and spacing.
- Missing anticipation.
- Missing follow-through.
- Incorrect foreground/background layering.
- Misaligned per-frame metadata.
- Invalid assumptions about perspective.
- Reusing one attachment configuration across incompatible animations.
- Preview rendering artifacts.

Inspect the current composite animation frame by frame.

Distinguish problems with:

**A. Original weapon artwork**

Incorrect proportions, scale or design.

**B. Orc body animation**

Bad anatomy, weak poses or unnatural movement.

**C. Weapon-to-body composition**

Poor attachment, rotation or occlusion.

**D. Animation playback**

Incorrect timing, frame order or transitions.

**E. Preview rendering**

Problems introduced by the local preview rather than the actual source assets.

Your implementation must address confirmed causes.

Do not apply blind corrective offsets.

---

# 6. ONE-HANDED WEAPON PROPORTIONS

Correct the existing starter sword and starter axe.

Preserve their intended identity and material design where possible.

## Sword

The sword must:

- Read clearly as a one-handed sword.
- Have believable blade-to-hilt proportions.
- Have a grip compatible with the Orc's hand.
- Remain recognizable at tactical camera scale.
- Maintain consistent dimensions throughout animation.
- Avoid exaggerated proportions inappropriate for basic equipment.

## Axe

The current axe is visibly too large.

Correct this.

The axe must:

- Read unmistakably as a one-handed axe.
- Have a compact and believable shaft.
- Have a proportionate axe head.
- Remain compatible with one-handed handling.
- Preserve the recognizable identity of the existing design.
- Avoid visually resembling a two-handed weapon.
- Maintain consistent scale throughout the attack.

### Proportion validation

Evaluate both weapons relative to:

- Orc height.
- Torso width.
- Arm length.
- Hand size.
- Shoulder-to-hand reach.
- Grip position.
- Attack trajectory.
- Overall combat silhouette.

Do not use arbitrary global scaling as the only correction.

If the weapon source itself requires modification, correct the current editable source through the authorized Character Factory workflow.

Create a safe source revision or backup before destructive changes.

Do not modify unrelated weapons.

Do not impose arbitrary pixel dimensions without checking the current character proportions.

---

# 7. NATURAL ONE-HANDED GRIP

The hand must convincingly hold the weapon.

This is a mandatory artistic requirement.

For each relevant attack frame:

1. Identify the hand's grip/contact point.
2. Identify the weapon handle's grip point.
3. Align these points consistently.
4. Adjust the hand pose to visually grasp the handle.
5. Maintain plausible wrist orientation.
6. Maintain a natural forearm connection.
7. Ensure the elbow and shoulder support the pose.
8. Correct foreground/background occlusion.
9. Avoid the weapon cutting unnaturally through the hand.
10. Prevent the weapon from floating or drifting.

### No fake attachment

Matching anchor coordinates is insufficient.

The hand must visually appear to wrap around the grip.

If the fingers need to overlap the handle, represent the overlap convincingly through the approved art/layering workflow.

Maintain weapon/body source separation.

Do not permanently bake the sword or axe into the character artwork.

### Per-frame composition

A static attachment transform is not necessarily sufficient for a dynamic attack.

Use per-frame attachment metadata or appropriately scoped pose-specific rules when necessary.

However, do not create an unnecessarily complex inverse-kinematics or skeletal-rigging system.

Prefer controlled artistic poses with reliable attachment metadata.

---

# 8. REBUILD CONVINCING ATTACK ANIMATIONS

The current attack animations are artistically rejected.

You are authorized to correct or replace their defective poses while preserving the MAIN ORC's identity.

## 8.1 Fundamental principle

**The body must drive the strike. The weapon must follow the hand and body mechanics.**

Do not create animation by rotating a weapon independently around a nearly static character.

## 8.2 Animation phases

Design a convincing attack using the following motion principles.

### Anticipation

- Establish stance and balance.
- Prepare the shoulder and torso.
- Position the arm for a credible attack.
- Introduce the weapon in a believable action pose.
- Preserve a convincing one-handed grip.

### Acceleration

- Coordinate torso, shoulder, elbow and wrist.
- Move the weapon along a readable trajectory.
- Use appropriate timing and spacing.
- Maintain the weapon's apparent size and contact with the hand.

### Strike

- Present a clear attack pose.
- Communicate direction and force.
- Preserve anatomical credibility.
- Maintain a believable grip.
- Avoid disproportionate exaggeration.

### Follow-through

- Allow the motion to continue naturally.
- Respect the weapon's weight.
- Avoid mechanical stopping or abrupt changes of direction.

### Recovery

- Return toward the current character's appropriate resting pose.
- Preserve consistent body proportions.
- Hide the weapon after the action is completed.
- Avoid snapping or animation-state artifacts.

These phases do not dictate an exact frame count.

Choose the number of frames and their durations according to animation quality and the actual production constraints.

Avoid excessive frames when a small number of strong key poses would achieve a better result.

---

# 9. DIFFERENT ATTACK PROFILES FOR SWORD AND AXE

Do not force a sword and axe to share identical attack motion.

These weapons have different physical characteristics.

## Sword attack

Create a controlled and believable one-handed sword strike.

Characteristics:

- Clear attack direction.
- Convincing sword arc.
- Appropriate wrist orientation.
- Fast but readable motion.
- Coordinated shoulder and torso.
- Natural follow-through.
- Consistent blade silhouette.

Avoid arbitrary sword spinning.

## Axe attack

Create a heavier one-handed chopping motion.

Characteristics:

- Slightly more deliberate anticipation.
- Convincing weight toward the axe head.
- Coordinated body mechanics.
- Clear impact pose.
- Controlled follow-through.
- Consistent handle grip.
- No exaggerated or weightless rotation.

Avoid turning the attack into a two-handed swing.

## Reuse policy

A sword animation may be reused with other compatible one-handed swords.

An axe animation may be reused with other compatible one-handed axes.

Different weapon categories may require different animation profiles.

Do not sacrifice artistic quality to enforce one universal animation for all equipment.

---

# 10. PRESERVE EQUIPMENT REUSABILITY

The creator's equipment strategy remains:

**Weapon assets are independent from character body sprites.**

This allows weapon changes without redrawing every body animation.

Your solution should support:

- Swapping compatible one-handed sword assets.
- Swapping compatible one-handed axe assets.
- Retaining the corresponding body attack animation.
- Applying weapon-specific grip registration when needed.
- Maintaining correct scale.
- Maintaining correct occlusion.
- Maintaining correct attack timing.

Do not create a full general-purpose weapon framework for every future Job.

Implement the smallest reusable structure that supports the current MAIN ORC and the two starter weapon categories.

A reusable animation profile must still look convincing when an actual weapon is attached.

A technically generic solution with poor animation quality is unacceptable.

---

# 11. ASEPRITE + PIXELLAB PRODUCTION

The Character Factory uses an integrated PixelLab + Aseprite artistic pipeline.

Follow its current documented configuration and permissions.

## Aseprite

Use Aseprite for:

- Editing the current MAIN ORC source.
- Correcting attack poses.
- Refining hand and arm anatomy.
- Pixel-level adjustments.
- Animation timing.
- Layer and occlusion corrections.
- Maintaining editable masters.
- Producing approved export candidates.
- Reviewing frame consistency.

The current `.aseprite` files remain authoritative editable sources under the active pipeline.

## PixelLab

PixelLab may assist with:

- Developing candidate attack poses.
- Correcting limited anatomical regions.
- Producing pose variations.
- Inpainting or guided refinement.
- Exploring improvements consistent with the existing MAIN ORC.

Use only currently available and authorized PixelLab operations.

Do not assume every model or endpoint is available.

Avoid unnecessary paid generation calls.

Do not overwrite the current MAIN ORC design with a new generic generated character.

### Art quality rule

Use whichever authorized combination of PixelLab and Aseprite produces the strongest result.

Do not force automation where careful frame-by-frame artistic correction would be more effective.

Do not treat geometric scripts or procedural transforms as substitutes for good animation design.

Generated candidates still require artistic validation.

Record provenance accurately.

---

# 12. PROTECT THE CURRENT ORC'S IDENTITY

The current MAIN ORC is the visual authority.

Preserve:

- Face and expression style.
- Skin tone.
- Body identity.
- General anatomy.
- Clothing and armor design.
- Color palette.
- Rendering style.
- Pixel cluster quality.
- Tactical camera perspective.
- Overall recognizable silhouette.

However, correcting a visibly defective attack may require substantial changes to:

- Arms.
- Hands.
- Upper body pose.
- Shoulder positioning.
- Torso orientation.
- Weapon interaction.

These improvements are authorized.

Do not reject necessary pose corrections simply to preserve historically exported frames.

### Artistic preservation rule

Preserve the character's identity, NOT defective animation behavior.

Work directly from current production sources and maintain recoverable versions of modified assets.

Do not resurrect older Orc generations.

---

# 13. CONTROLLED IMPLEMENTATION STRATEGY

Avoid generating a large number of mediocre assets.

Implement this correction through a focused vertical slice.

## Checkpoint A — Current-source audit

Identify:

- Current MAIN ORC.
- Current sword.
- Current axe.
- Current attack body animations.
- Current attachment system.
- Current preview system.
- Current production masters.

Confirm the source of truth.

## Checkpoint B — Weapon correction

Correct sword/axe dimensions and grip metadata.

Prioritize the oversized one-handed axe.

## Checkpoint C — Sword attack correction

Create one convincing sword attack in the current Orc's primary `front_r` perspective, or the actual canonical equivalent identified in the repository.

Verify:

- Grip.
- Arm anatomy.
- Torso motion.
- Attack trajectory.
- Timing.
- Follow-through.
- Recovery.

## Checkpoint D — Axe attack correction

Create one convincing one-handed axe attack.

Verify:

- Correct weapon proportions.
- Convincing weight.
- Consistent grip.
- Proper hand, elbow and shoulder coordination.
- Natural motion.
- Recovery.

## Checkpoint E — Attack-only visibility

Update the appropriate preview/production behavior:

- No weapon in Idle.
- No weapon in Walk.
- Weapon visible during Attack.
- Weapon hidden after Attack.

Remove or clearly supersede obsolete armed Idle/Walk behavior.

## Checkpoint F — Reusability validation

Verify that another compatible weapon can use the relevant sword or axe profile without requiring a completely new body animation.

Do not create additional production weapons merely for this test.

## Checkpoint G — Artistic QA

Inspect animations at both native pixel scale and practical tactical display scale.

Review normal-speed and slow-motion playback.

Prepare direct comparison evidence.

Do not propagate to other views, Jobs or races before creator approval.

---

# 14. PREVIEW REQUIREMENTS

Generate or update a reviewable local preview using the current MAIN ORC.

Show:

1. Current Orc Idle without weapon.
2. Current Orc Walk without weapon.
3. Corrected sword Attack.
4. Corrected axe Attack.
5. Return to unarmed Idle.
6. Before/after sword comparison.
7. Before/after axe comparison.
8. Individual important animation frames.
9. Weapon grip close-ups.

Provide useful controls when compatible with the existing preview system:

- Play/Pause.
- Frame stepping.
- Loop.
- Playback speed.
- Native pixel-art zoom.
- Transparent/contrasting backgrounds when helpful.

Do not use smooth interpolation that hides pixel defects.

Use actual exported frames and timing.

Do not fake better animation through preview-only transforms.

The preview must demonstrate the real proposed production output.

---

# 15. ARTISTIC ACCEPTANCE CRITERIA

The corrected animations must not exhibit:

- Floating weapons.
- Disconnected hands.
- Inconsistent grip positions.
- Impossible wrist bends.
- Broken elbow or shoulder anatomy.
- Excessively large one-handed axe proportions.
- Weapon scale changes between frames.
- Rigid weapon spinning without body participation.
- Unrealistic attack direction.
- Sudden visual snapping.
- Unnatural clipping.
- Incorrect occlusion.
- Poorly coordinated torso movement.
- Missing anticipation or recovery.
- Weightless axe motion.
- A sword swing that resembles arbitrary object rotation.
- Inconsistent character identity.
- Visible weapons during Idle or Walk.

### Subjective artistic validation

Automated checks cannot prove that an attack looks natural.

Do not award automatic artistic approval based on:

- Correct dimensions.
- Successful exports.
- Valid JSON.
- Matching attachment coordinates.
- Passing tests.
- Correct frame count.

These validate technical properties, not visual quality.

Prepare clear evidence for creator review.

The creator is the final artistic authority.

---

# 16. TECHNICAL VALIDATION

Implement focused checks for:

- Correct active MAIN ORC source selection.
- No accidental selection of historical Orc versions.
- Correct weapon category.
- Correct weapon scale metadata.
- Valid independent weapon references.
- Correct grip registration.
- Correct frame ordering.
- Correct animation durations.
- Valid body/weapon composition data.
- Weapon hidden in Idle.
- Weapon hidden in Walk.
- Weapon visible in Attack.
- Weapon hidden after Attack.
- No unexpected canvas/pivot drift.
- No missing animation frames.
- Valid current exports.
- Preservation of recoverable masters.
- Correct provenance.
- Reproducible preview output.

If applicable, test attachment consistency across the active attack frames.

Do not add dozens of meaningless assertions.

Use existing testing conventions.

Report what was actually validated.

---

# 17. DOCUMENTATION UPDATES

Update only relevant current Character Factory documentation.

Record:

1. MAIN ORC is the current authoritative production character.
2. Historical Orc V4 is not an active production source.
3. Sword and axe attack corrections.
4. One-handed weapon proportion guidelines.
5. Natural grip requirements.
6. Body-driven attack animation rules.
7. Attack-only weapon visibility.
8. No armed Idle or Walk states.
9. Independent weapon asset conventions.
10. Sword/axe animation profile reuse.
11. Current source master relationships.
12. Required artistic approval gates.
13. Remaining technical limitations.
14. Future propagation strategy.

Update the current roadmap appropriately.

Do not preserve contradictory outdated instructions without marking them superseded.

Do not rewrite unrelated design documentation.

---

# 18. REPOSITORY SAFETY

Before editing:

- Inspect the current working tree.
- Identify active source files.
- Preserve unrelated changes.
- Preserve current Orc design assets.
- Use recoverable source revisions.
- Avoid destructive cleanup.
- Keep Unity `.meta` and runtime integrations untouched.

Do not:

- Restore historical Orc V4 artwork.
- Modify the sibling Unity repository.
- Introduce new Jobs.
- Redesign the Orc.
- Generate all weapon types.
- Modify unrelated outfits.
- Replace entire animation libraries.
- Create equipment gameplay mechanics.
- Add unapproved weapon systems.
- Perform uncontrolled PixelLab generations.
- Create Git commits without authorization.

If Aseprite is already open with unsaved creator work, do not interfere with that session.

Prefer safe, documented, noninteractive automation when possible.

---

# 19. FINAL REPORT

Deliver:

### A. Current production verification

- Current MAIN ORC source identified.
- Active weapon sources identified.
- Historical source conflicts, if any.

### B. Root-cause findings

- Problems in sword animation.
- Problems in axe animation.
- Problems in body movement.
- Problems in attachment/occlusion.
- Problems in weapon proportions.

### C. Corrections

- Body animation adjustments.
- Hand and arm pose adjustments.
- Weapon scale corrections.
- Grip attachment changes.
- Attack timing changes.
- Weapon visibility changes.

### D. Reusability

Explain how compatible one-handed swords and axes can reuse attack animations without requiring a complete redraw.

### E. Production evidence

- Editable source paths.
- Exports.
- Preview paths.
- Before/after comparisons.
- PixelLab usage, if any.
- Artistic provenance.

### F. Validation

- Technical tests performed.
- Results.
- Independent artistic review, if performed.
- Remaining defects.
- Creator approval still required.

### G. Documentation and Git

- Files modified.
- Current documentation updated.
- Git diff summary.
- Known limitations.
- Recommended next production step.

Do not declare the new attacks artistically approved until the creator reviews them.

---

# 20. EXECUTION AUTHORIZATION

Implement the correction in the Character Factory now.

The creator authorizes:

- Correcting the current MAIN ORC's sword attack.
- Correcting the current MAIN ORC's axe attack.
- Improving hand and arm anatomy.
- Improving torso-driven attack movement.
- Correcting oversized weapon proportions.
- Updating weapon attachment metadata.
- Updating attack-only visibility behavior.
- Creating safe revisions of current production sources.
- Updating relevant documentation.
- Producing side-by-side review previews.
- Running technical validation.

The creator does NOT authorize:

- Returning to historical Orc V4 artwork.
- Replacing the current Orc's identity.
- Modifying Unity.
- Propagating the solution across every outfit or direction.
- Implementing a large new equipment framework.
- Automatically approving final artwork.

### FINAL PRINCIPLE

**The MAIN ORC must look like a living character genuinely swinging a one-handed weapon — not a static sprite with an object rotating around its wrist.**

Correct the actual animation and artistic composition, not merely the metadata.

Preserve creative identity, equipment independence and future reuse.

Prioritize one excellent sword attack and one excellent axe attack over dozens of technically valid but visually unacceptable animations.