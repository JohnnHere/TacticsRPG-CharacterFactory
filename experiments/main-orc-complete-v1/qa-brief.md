# Mandatory Independent QA Brief — `main-orc-complete-v1`

## 1. Original Request & Acceptance Criteria
Full production completion of the CURRENT MAIN ORC (`characters/orc-v1` / "Orc V1 · Verde Warcraft", derived from `orc-pixellab-05` with `green-skin-v3`) required animation library and Unity-ready staging package in `TacticsRPG-CharacterFactory`:
- **4 directions (`front_r`, `front_l`, `back_r`, `back_l`) × 7 actions (`Idle`, `Walk`, `Unarmed` / `Attack`, `Sword Attack`, `Axe Attack`, `Hit`, `Defeat`) = 28 cells + 4 directional static bases (`Directions/orc_v1_dir_<dir>.png`).**
- **Identity & Historical V4 Rule:** Current Main Orc is `characters/orc-v1` (`orc-pixellab-05` + `green-skin-v3`). Historical `orc-01` / Orc V4 remains discarded (`historicalV4Discarded: true`).
- **Weapon Visibility (`attack-only-v1`):** Weapons (`recruit-sword` `96x96` grip `[48,66]`, `militia-axe` `96x96` grip `[36,55]`) are separate assets visible ONLY inside declared `visibleInterval` (`Sword`: `[2, 10]` of `0..12`; `Axe`: `[2, 8]` of `0..11`). Hidden in `Idle`, `Walk`, `Unarmed`, `Hit`, `Defeat`, and on entry/recovery frames (`0, 1` and `11, 12` for Sword; `0, 1` and `9, 10, 11` for Axe).
- **4-Layer Occlusion Order:** `["weaponBack", "body", "weaponFront", "handFront"]`.
- **Canonical Timings & Standards:**
  - `Idle`: `idle-balanced-v1`, 5 frames `[400, 450, 500, 450, 400]` ms = `2200` ms (`loop: true`).
  - `Walk`: `locomotion.walk-v1`, 16 frames `80` ms each = `1280` ms (`loop: true`).
  - `Unarmed` (`Attack` slot): `basic.unarmed`, 5 frames `[80, 110, 50, 90, 120]` ms = `450` ms (`oneShot: true`, impact frame 2 @ 190 ms).
  - `Sword Attack`: `basic.sword-slash`, 13 frames / `730` ms (`oneShot: true`, `visibleInterval: [2, 10]`, impact frame 8 @ 360 ms). Reuses `main-orc-onehanded-entry-v1` in `front_r`.
  - `Axe Attack`: `basic.axe-chop`, 12 frames / `1005` ms (`oneShot: true`, `visibleInterval: [2, 8]`, impact frame 6 @ 410 ms). Reuses `main-orc-onehanded-entry-v1` in `front_r`.
  - `Hit`: `reaction.hit`, 5 frames `[45, 95, 115, 95, 100]` ms = `450` ms (`oneShot: true`).
  - `Defeat`: `reaction.defeat`, 5 frames `[70, 95, 115, 130, 290]` ms = `700` ms (`terminal: true`, `terminalFrame: 4`).
- **Aseprite Masters & Staging Package:**
  - Editable `.aseprite` masters in `characters/orc-v1/source/aseprite/complete-v1/{native,composite}/`, verified via `exportAseprite` (`75 jobs / 599 frames PASS`, `experiments/main-orc-complete-v1/build.json`).
  - Native `128x128` PNGs in `characters/orc-v1/sprites/` (`groundY: 126`, `749 PASS, 0 FAIL` in `characters/orc-v1/reports/validation.json`) and unarmed action supplement in `characters/orc-v1/source/actions/basic-unarmed/v1/`.
  - Composite `256x256` clips, layers, strips, `clip.json`, and `profile.json` in `characters/orc-v1/source/complete-v1/<dir>/` (`bodyOffset: [64, 64]`, `groundY: 190`).
  - Machine-readable coverage matrix: `reports/orc-v1-animation-coverage-v1.json` (`28/28` cells `COMPLETE_VERIFIED`).
  - Unity-ready staging package: `dist/orc-v1/complete-v1/` with `Assets/Resources/Characters/orc-v1/unity-handoff-contract.json`.
  - Interactive review studio pages: `Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html` and `Biblioteca de Arte/Estudos Comparativos/Orc principal - Biblioteca completa/index.html` + `Biblioteca de Arte/index.html`.
- **Governance & Safety:**
  - `artisticApproval: "PENDING_CREATOR"`, `runtimeImplemented: false`.
  - Active selection pointer `characters/orc-v1/source/equipment-current.json` (`main-orc-onehanded-v3`) and entry candidate pointer `characters/orc-v1/source/equipment-entry-candidate.json` (`main-orc-onehanded-entry-v1`) preserved untouched.
  - Zero modifications to `../TacticsRPG` and zero destructive Git operations.

## 2. Files Created / Modified
- `tools/aseprite/author-main-orc-complete.lua` (Aseprite Lua authoring script for 4 directions × 7 actions)
- `tools/build-main-orc-complete.mjs` (Manifests, `exportAseprite` verification, `validate()`, coverage matrix, and `dist/orc-v1/complete-v1/` packager)
- `tools/build-main-orc-complete-review.py` (Interactive 4-direction × 7-action review studio generator)
- `tools/audit-main-orc-complete-animation.mjs` & `experiments/main-orc-complete-animation-v1/` (Stage A baseline audit & protected snapshot)
- `characters/orc-v1/character.json` (Added `Attack: 5, Hit: 5, Defeat: 5`, `groundY: 126`, and `completeAnimationCandidate` pointer)
- `characters/orc-v1/source/equipment-complete-candidate.json` (Candidate pointer for `main-orc-complete-v1`)
- `characters/orc-v1/source/aseprite/complete-v1/` & `characters/orc-v1/source/complete-v1/` & `characters/orc-v1/sprites/` & `characters/orc-v1/source/actions/`
- `reports/orc-v1-animation-coverage-v1.json`
- `dist/orc-v1/complete-v1/`
- `test/main-orc-complete.test.mjs`
- `AGENTS.md`, `handoff/AGENT_CONTEXT.md`, `docs/ROADMAP.md`, `docs/MAIN_ORC_COMBAT_POLISH.md`
- `Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html`, `Biblioteca de Arte/Estudos Comparativos/Orc principal - Biblioteca completa/index.html`, `Biblioteca de Arte/index.html`

