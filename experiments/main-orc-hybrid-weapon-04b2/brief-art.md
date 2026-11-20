# Experiment 04 — Hybrid Weapon Architecture | Pilot B2 (`back_r / Sword`)

## 1. Purpose
Prove that **Architecture C (Hybrid Weapon Architecture)** reuses the recovered rear-right sword attack animation (`characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword/clip.json`) with two independent one-handed sword variants (`Sword A` = Recruit Sword, `Sword B` = Faceted Light Steel Sword) **without modifying a single pixel of the Orc's body or gripping hand (`body` and `handFront`)**.

## 2. Authoritative Inputs
- **Source Animation Clip**: `characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword/clip.json` (`14` frames, `730 ms`, weapon visible `F02..F11`, contact `F08` at `325 ms`).
- **Source Aseprite Master**: `characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword/source/composite.aseprite` (`256×256`, 4 layers: `weaponBack -> body -> weaponFront -> handFront`).
- **Weapon Variant A**: `experiments/main-orc-hybrid-weapon-04b2/variants/sword-a/` (`96×96`, grip `[48, 66]`, byte-identical to Pilot A/B1).
- **Weapon Variant B**: `experiments/main-orc-hybrid-weapon-04b2/variants/sword-b/` (`96×96`, grip `[48, 66]`, byte-identical to Pilot A/B1).

## 3. Rear-Right (`back_r`) Depth, Occlusion & Blade Mapping Rules
1. **Layer Ordering**: `weaponBack -> body -> weaponFront -> handFront`.
2. **Depth Split**:
   - `weaponBack` holds the rear hilt/pommel behind the right hip/torso (`F02..F05`, `F07..F11`) and the leather grip in `F06` (`53..116 px` occluded behind `body`).
   - `weaponFront` holds 100% of the blade (`v <= 54`, plus 2 rotation-rounded seam pixels at `v == 55` in `F07`) and crossguard in front of the body (`172 px` in `F02`, `51 px` in `F06` passing in front of `body`).
   - `handFront` (`46..119 px`) overlays the gripping gauntlet fingers over the handle (`38..83 px` overlap with weapon layers).
3. **Proportional Interior Bevel Mapping (`author.lua`)**:
   - Because Sword B's ricasso (`v = 45..54`, `u = 45..51`, 7 px wide) and mid-blade (`v = 13..44`, `u = 44..52`, 9 px wide) are narrower than Sword A's blade (`u = 42..53`, 12 px wide), outer 1 px dark outline pixels (`max(R,G,B) <= 32`) map to Sword B's `1 px` dark outline `(12,15,18)`, while interior blade metal pixels (`max(R,G,B) > 32`) map proportionally across Sword B's interior faceted steel bevel (`(214,226,238)`, `(178,192,206)`, `(146,162,178)`, `(94,108,124)`). This preserves 100% of the rotated blade silhouette (`silhouetteDeltaAB = 0`) with a clean `1 px` outline and zero thick black rim.

