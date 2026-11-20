# V5 Combat Rescue Report (`main-orc-combat-rescue-v5`)

- **Character**: `orc-v1` (Verde Warcraft)
- **Scope**: 12 Combat Clips (`front_r/Unarmed`, `front_l/Unarmed`, `back_r/Unarmed`, `back_l/Unarmed`, `front_r/Sword`, `front_l/Sword`, `front_r/Axe`, `front_l/Axe`, `back_r/Sword`, `back_l/Sword`, `back_r/Axe`, `back_l/Axe`)
- **Technical Status**: `TECHNICALLY_COMPLETE` (`12/12` clips, `102/102` frames, `588/588` SHA-256 hashes verified)
- **Artistic Status**: `VISUAL_REVIEW_REQUIRED`
- **Creator Approval**: `PENDING_CREATOR`

---

## 1. Confirmed V4 / V2 Root Causes & How V5 Solves Each Defect

### A. Rear Weapon Body Choreography & Technique Separation (`back_r/Sword`, `back_l/Sword`, `back_r/Axe`, `back_l/Axe`)
- **Confirmed V4 Failure**:
  - In V4, rear `Sword` and `Axe` shared near-identical body frames or relied on component cut-outs/shears, lacking genuine whole-body weight transfer and distinct weapon-family mechanics.
  - Furthermore, raw generation artifacts caused off-hand drift/jitter and occasional border clipping or residual weapon/strap pixels on the empty-handed body layer.
- **V5 Solution**:
  - Generated **4 dedicated whole-body empty-handed rear skeleton sequences** via PixelLab `animate_with_skeleton_v3` using the canonical `back_r.png` (`north-east`) and `back_l.png` (`north-west`) base references:
    1. `back_r/Sword` (`06c2d829-7b45-4d6f-b64e-ce7db44ffac1`, 7f, 3 gen): **Horizontal/diagonal shoulder-height slash**. The right arm chambers at shoulder height (`F01..F02`, `gy=110 -> 91`), sweeps wide across the horizontal/diagonal plane (`F03..F05`, `gx=184..181`), and settles at `F06` before returning to guard at `F07`.
    2. `back_r/Axe` (`d6d12081-e933-4a9c-98eb-358654566039`, 7f, 3 gen): **Heavy high-overhead cleave**. The right arm hoists steep and high above the crown (`F01..F02`, `gy=73`), then drives vertically downward (`F03..F05`, `gy=90 -> 119 -> 136`) with heavy torso lean.
    3. `back_l/Sword` (`10f597b6-5677-4bc4-8364-bc9b88511ff2`, 7f, 3 gen): **Left-handed horizontal/diagonal slash** (`north-west`), maintaining dorsal armor asymmetry without mirroring.
    4. `back_l/Axe` (`b1e88042-81c9-4e11-a217-292be7eb2021`, 7f, 3 gen): **Left-handed high-overhead cleave** (`north-west`), lifting to `gy=78 -> 73` before cleaving down to `gy=129 -> 137`.
  - **Quantitative Sword vs. Axe Body Separation (`layers-off`)**:
    - `back_r/Sword` vs `back_r/Axe`: `[0, 3960, 4196, 3960, 4672, 4128, 3316, 0]` differing body bytes across `F00..F07`.
    - `back_l/Sword` vs `back_l/Axe`: `[0, 3692, 4132, 3440, 4724, 4392, 3812, 0]` differing body bytes across `F00..F07`.
  - **Aseprite `layers-off` Cleanup & Off-Hand Anchor (`clean_rear_weapon_bodies.lua`)**:
    - Anchored the non-attacking off-hand column (`x <= 48` on `back_r`, `x >= 79` on `back_l`) directly from the `F00` guard pose across `F01..F07`, achieving **`0` off-hand pixel shift** across the entire clip.
    - Verified `layers-off` (`cleaned_rear_bodies_4x8.png`) across all 32 rear weapon body frames: zero phantom blades, shafts, pommels, neck bands, or shoulder hooks, and zero border clipping (`xmin >= 2`, `xmax <= 125`, `ymin >= 2`, `groundY = 126`).

### B. Natural Handle-Enclosing Grip Across All 8 Weapon Clips (`front_r`, `front_l`, `back_r`, `back_l` × `Sword`, `Axe`)
- **Confirmed V4 Failure**:
  - In V4, `handFront` overlays were tiny `12–40 px` semi-random specks or flat patches that left the weapon handle floating over the wrist/forearm or hid the crossguard/pommel.
- **V5 Solution (`author_weapons_8clips.lua`)**:
  - Preserved **100% of the approved frontal body choreography and frame durations** on `front_r/Sword`, `front_l/Sword`, `front_r/Axe`, and `front_l/Axe` (exact RGBA pixel match on `layers/body` and `native`).
  - Authored an articulated **`95–128 px` armored gauntlet `handFront` layer** for every weapon-visible frame across all 8 weapon clips:
    - **4 articulated steel finger straps** (`IRON_LITE`, `IRON_MID`, `IRON_DARK` separated by `INK` inter-finger crevices) curling around the outer edge of the handle shaft (`hu > 0`).
    - **Upper thumb lock** (`hv` near `vTop`) clinching the upper handle below the crossguard / axe eye without covering the guard or pommel.
    - **Stitched leather wrist cuff bridge** (`LEATH_MID`, `LEATH_DARK`, `INK` border on `hu < 0`) automatically oriented toward the character's forearm vector so the grip visually connects into the posed gauntlet forearm in every frame.
  - Verified at `3x` zoom in `experiments/main-orc-combat-rescue-v5/combat/sheets/weapon_grips_8clips_3x_zoom.png`.

### C. Unarmed 4 Views (`front_r/Unarmed`, `front_l/Unarmed`, `back_r/Unarmed`, `back_l/Unarmed`)
- **Confirmed V4 / V2 Failures**:
  - **Frontal (`front_r/Unarmed`, `front_l/Unarmed`)**: In `F03` (`90ms` follow-through/recoil), the baseline replaced the entire body with an incompatible pose where the punching fist disappeared behind the torso and the non-punching guard arm teleported by `17px`.
  - **Rear (`back_r/Unarmed`, `back_l/Unarmed`)**: Previously reused weapon-swing donor poses or suffered arm truncation.
- **V5 Solution (`author_unarmed_4views.lua`)**:
  - **Frontal (`front_r/Unarmed`, `front_l/Unarmed`)**: Preserved `F00, F01, F02, F04` with exact RGBA pixels (`0` pixel diffs). Rebuilt `F03` inside Aseprite Lua from the `F02` impact torso/legs/guard-arm base while retracting the punching forearm and intact `72px` armored gauntlet fist by `(-4px, +2px)` on `front_r` (`(+4px, +2px)` on `front_l`) and bridging the shoulder-to-elbow plate seamlessly. The punching fist now remains 100% visible through recoil and the guard arm has `0px` teleportation between `F02` and `F03`.
  - **Rear (`back_r/Unarmed`, `back_l/Unarmed`)**: Generated 2 dedicated whole-body rear brawler punch skeleton sequences (`9fdb5943` and `eea7ce3b`, 5f, 3 gen each), anchored the off-hand from `F00`, and exported clean 5-frame (`450ms`) clips.
  - Verified in `experiments/main-orc-combat-rescue-v5/combat/sheets/unarmed_4views_v5_sheet.png`.

---

## 2. PixelLab Generation Accounting & Receipts

| Metric | Value | Evidence |
|---|---|---|
| Initial Balance | `1403.70` generations (`$0.00` USD) | `experiments/main-orc-combat-rescue-v5/combat/receipts/balance-initial.json` |
| Final Balance | `1385.70` generations (`$0.00` USD) | `experiments/main-orc-combat-rescue-v5/combat/receipts/balance-final.json` |
| Total Account Delta | **`18.00` generations** | Exact match to 6 `animate_with_skeleton_v3` jobs × 3 generations |

| Job Name | Job ID | Direction | Target Clip | Frames | Cost | Receipt Path |
|---|---|---|---|---|---|---|
| `back_r_sword_v1` | `06c2d829-7b45-4d6f-b64e-ce7db44ffac1` | `north-east` | `back_r/Sword` | 7 | 3 gen | `combat/receipts/job-back_r_sword_v1-final.json` |
| `back_l_sword_v1` | `10f597b6-5677-4bc4-8364-bc9b88511ff2` | `north-west` | `back_l/Sword` | 7 | 3 gen | `combat/receipts/job-back_l_sword_v1-final.json` |
| `back_r_axe_v1` | `d6d12081-e933-4a9c-98eb-358654566039` | `north-east` | `back_r/Axe` | 7 | 3 gen | `combat/receipts/job-back_r_axe_v1-final.json` |
| `back_l_axe_v1` | `b1e88042-81c9-4e11-a217-292be7eb2021` | `north-west` | `back_l/Axe` | 7 | 3 gen | `combat/receipts/job-back_l_axe_v1-final.json` |
| `back_r_unarmed_v1` | `9fdb5943-ccfd-456d-aa2e-d07a49f3591c` | `north-east` | `back_r/Unarmed` | 5 | 3 gen | `combat/receipts/job-back_r_unarmed_v1-final.json` |
| `back_l_unarmed_v1` | `eea7ce3b-0136-4f8b-8a6b-a6a871b24f68` | `north-west` | `back_l/Unarmed` | 5 | 3 gen | `combat/receipts/job-back_l_unarmed_v1-final.json` |

---

## 3. Technical & Contract Verification Summary

Executed `node experiments/main-orc-combat-rescue-v5/combat/scripts/verify_patch_contract.mjs`:
- **Result**: `COMBAT_PATCH_12_PASS` (`cellsChecked: 12`, `framesChecked: 102`, `hashesChecked: 588`)
- Every clip satisfies:
  - `canvas = [256, 256]`, `groundY = 190`, `nativeCanvas = [128, 128]`, `nativeGroundY = 126`, `bodyOffset = [64, 64]`
  - Exact `.aseprite` header dimensions and frame durations (`master`, `bodyMaster`, `nativeMaster`)
  - Exact 4-layer alpha-over composition (`weaponBack -> body -> weaponFront -> handFront == composite`)
  - Exact `native[64,64]` crop equality (`native == body[64:192, 64:192]`)
  - Zero partial alpha pixels (`partial == 0`)
  - Strict `attack-only-v1` visibility (all weapon/hand layers empty when `weaponVisible == false`)

---

## 4. Deliverables & Review Surfaces

- **Integration Patch Manifest**:
  - `characters/orc-v1/source/combat-rescue-v5/combat/patch-manifest.json`
  - `experiments/main-orc-combat-rescue-v5/combat/patch-manifest.json`
- **Interactive HTML Preview (`1x`, `0.5x`, `0.25x`, step-frame, Before/After, `Composite` / `Layers-Off` / `HandFront`)**:
  - `experiments/main-orc-combat-rescue-v5/combat/preview/index.html`
- **Static Visual Contact Sheets**:
  - `experiments/main-orc-combat-rescue-v5/combat/sheets/unarmed_4views_v5_sheet.png`
  - `experiments/main-orc-combat-rescue-v5/combat/sheets/cleaned_rear_bodies_4x8.png`
  - `experiments/main-orc-combat-rescue-v5/combat/sheets/rear_weapons_4x8_composite.png`
  - `experiments/main-orc-combat-rescue-v5/combat/sheets/weapon_grips_8clips_3x_zoom.png`
