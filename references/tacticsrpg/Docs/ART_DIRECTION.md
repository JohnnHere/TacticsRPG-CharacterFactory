# ART DIRECTION — TacticsRPG

## 1. Purpose

This document defines the official character art direction for the project.

Its role is to:
- establish a consistent visual identity for the project
- define the approved reference style for all future characters
- guide the creation of classes, races, named units, enemies, and important NPCs
- ensure visual coherence across the full roster

---

## 2. Official Style Anchor

Official visual reference:

![Character Style Anchor](Art/References/character_style_anchor_v1.png)

Reference file:
`Docs/Art/References/character_style_anchor_v1.png`

This image is the current approved visual anchor for the project’s character style.

It defines the baseline for:
- character proportions
- sprite readability
- armor rendering
- cloth rendering
- face maturity
- silhouette clarity
- detail density
- shading quality
- overall visual tone

Important:
This anchor defines the STYLE, not the exact character template.
Future characters do not need to share the same hair, armor, weapon, colors, or role.
They must preserve the same visual language.

---

## 3. Core Visual Inspirations

The project’s visual identity should be guided by the following inspirations:

### 3.1 Final Fantasy Tactics and classic tactical RPGs
Used as inspiration for:
- compact tactical character proportions
- battlefield readability
- class-based identity
- iconic silhouette clarity
- strong unit recognizability

### 3.2 World of Warcraft
Used as inspiration for:
- fantasy armor language
- visual boldness
- faction-readable shapes
- class identity through equipment and silhouette
- strong fantasy archetypes

Important:
Use World of Warcraft as inspiration for visual richness and fantasy clarity,
not for cartoon exaggeration or oversized proportions.

### 3.3 Tolkien-inspired fantasy
Used as inspiration for:
- grounded medieval-fantasy atmosphere
- noble heroic tone
- believable races and cultural flavor
- mythic but serious mood
- elegant, immersive fantasy worldbuilding

Important:
Use Tolkien as inspiration for tone, world flavor, and fantasy sensibility,
not as a requirement to mimic any specific copyrighted design.

---

## 4. Style Summary

Target style:
- tactical RPG character art
- refined pixel-art presentation
- compact readable proportions
- mature and grounded fantasy tone
- elegant armor and costume rendering
- visually rich but controlled detail
- game-ready character readability

The art should feel like a blend of:
- classic tactical RPG readability
- strong fantasy identity
- polished HD-2D-inspired sprite presentation

---

## 5. Character Rendering Rules

### 5.1 Proportions
- compact tactical proportions
- not chibi
- not super-deformed
- not realistic full-human proportions
- slightly heroic but readable at small scale

### 5.2 Face Design
- faces should look expressive and readable
- avoid excessively childish or baby-faced characters unless intentional
- default style should lean slightly mature or young-adult
- facial features should remain simple and readable in sprite scale

### 5.3 Silhouette
- each class must remain identifiable by the character's body, clothing, armor, and stance
- weapons are separate assets; when an action invokes an equipped weapon, its silhouette reinforces the role without being baked into the character sprite
- readability at gameplay scale is mandatory

### 5.4 Pixel Rendering
- handcrafted-looking pixel art
- clean clusters
- controlled detail density
- readable shading
- avoid muddy or noisy rendering
- avoid overly painterly softness
- avoid excessive blur

### 5.5 Materials
Armor:
- polished steel / silver base
- controlled highlights
- readable forms

Cloth:
- rich but controlled folds
- readable cape and tunic shapes
- strong color blocking

Leather:
- warm brown range
- straps, belts, boots should help define equipment hierarchy

Gold accents:
- restrained and elegant
- ornamental, not excessive

### 5.6 Weapon-independent character art
- New character concepts and character-base sprites show the character without a weapon in hand, carried, or sheathed.
- Weapon designs are authored as independent assets. They appear only when the unit has that weapon equipped and the current action invokes it.
- Character identity and Job readability must hold in weaponless states such as Idle and Walk.
- The Human Warrior Pilot's embedded sword is a historical prototype exception, not a template for new assets.
- This is an approved visual direction; dynamic weapon rendering, hand anchors, occlusion, and action synchronization still require implementation.

---

## 6. Tone and Mood

The project should feel:
- heroic
- noble
- serious
- medieval-fantasy
- grounded but imaginative
- visually rich without losing tactical clarity

Avoid:
- overly comedic stylization
- excessively childish art direction
- exaggerated cartoon stretch
- visual overload
- overdesigned noise

---

## 7. Character Diversity Rules

As the project grows into many classes, races, and named units,
future character creation must become more detailed and specific.

Each new character brief should define:
- class
- race
- role in gameplay
- faction / kingdom / origin
- age impression
- body type
- personality tone
- primary colors
- secondary colors
- armor / clothing type
- weapon type as a separate equipment asset, plus the actions that invoke it
- notable accessories
- silhouette goals
- special fantasy motifs if any

The more important the character, the more detailed the brief must be.

---

## 8. Style Boundaries

Do not drift into:
- generic mobile-game fantasy
- overly realistic painterly art
- soft illustration that loses sprite clarity
- oversized anime heads
- childlike proportions by default
- excessively noisy pixel rendering
- overly giant weapons unless intentionally class-specific
- direct imitation of copyrighted characters

---

## 9. Approval Criteria

A character should only be approved if it:
- matches the approved style anchor
- is readable as a tactical RPG unit
- has a strong and clear silhouette
- visually communicates class and role
- feels coherent with the project’s fantasy world
- respects the mature heroic tone
- preserves the project’s rendering language

---

## 10. Production Workflow

Recommended creation workflow:

1. Define character brief
2. Define class and race identity
3. Define silhouette goals
4. Generate candidate visuals
5. Compare against style anchor
6. Approve or refine
7. Save approved art reference
8. Add character to visual roster documentation

For the full technical process (directional views, animation frame contract, Unity import
standards, Presentation integration, testing and approval gates), follow
**`Docs/Art/CHARACTER_PIPELINE.md` v1.0** (spec template:
`Docs/Art/Characters/CHARACTER_TEMPLATE.md`). Principles that carry over from this document:
compact readable proportions, silhouette-first design, and **weapon-independent character
art as the production rule** — permanent weapons drawn into sprites (as in the Human Warrior
Pilot) are a historical prototype exception, not a production standard.

---

## 11. AI / Agent Usage Rule

Any AI agent or tool used for character creation must:
- read this document first
- inspect `Docs/Art/References/character_style_anchor_v1.png`
- preserve the approved visual language
- ask for clarification if it cannot interpret the image reference

If image interpretation is unavailable, the agent must rely on the written style rules in this document.

---

## 12. Versioning

Current approved anchor:
- `character_style_anchor_v1.png`

Future revisions may add:
- additional approved anchors for other archetypes
- race-specific style anchors
- enemy-specific anchors
- monster anchors
- environment anchors
