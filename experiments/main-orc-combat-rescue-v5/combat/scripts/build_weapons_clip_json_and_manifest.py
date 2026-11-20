import os
import json
import hashlib
from PIL import Image
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
V4_ROOT = "characters/orc-v1/source/rear-reconstruction-v4"
V5_ROOT = "characters/orc-v1/source/combat-rescue-v5/combat"
EXP_ROOT = "experiments/main-orc-combat-rescue-v5/combat"

def sha256_file(rel_path):
    abs_path = os.path.join(ROOT, rel_path.replace("/", os.sep))
    h = hashlib.sha256()
    with open(abs_path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def read_json(rel_path):
    abs_path = os.path.join(ROOT, rel_path.replace("/", os.sep))
    with open(abs_path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(rel_path, data):
    abs_path = os.path.join(ROOT, rel_path.replace("/", os.sep))
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

# 1. Write weapons/Sword/weapon.json and weapons/Axe/weapon.json
for cat, item_id in [("Sword", "recruit-sword"), ("Axe", "militia-axe")]:
    parent_w_rel = f"{V4_ROOT}/weapons/{cat}/weapon.json"
    w_data = read_json(parent_w_rel)
    sprite_rel = f"{V5_ROOT}/weapons/{cat}/{item_id}.png"
    master_rel = f"{V5_ROOT}/weapons/{cat}/{item_id}.aseprite"
    w_data["revision"] = "main-orc-combat-rescue-v5"
    w_data["sprite"] = sprite_rel
    w_data["master"] = master_rel
    w_data["spriteSha256"] = sha256_file(sprite_rel)
    w_data["masterSha256"] = sha256_file(master_rel)
    w_data["sourceSha256"] = sha256_file(master_rel)
    w_data["bindings"] = "Associated with the 8 V5 weapon clips with natural handle-enclosing grip and whole-body rear choreography; weapon geometry unchanged."
    w_data["parentWeaponDefinition"] = parent_w_rel
    write_json(f"{V5_ROOT}/weapons/{cat}/weapon.json", w_data)
    print(f"Wrote {V5_ROOT}/weapons/{cat}/weapon.json")

# 1b. Write clip.json for all 4 Unarmed clips (with canvas=[256,256], groundY=190, provenance)
UNARMED_SPECS = {
    "front_r": {"jobId": None, "paidUnits": 0, "phases": ["guard-prep", "shoulder-coil", "heavy-gauntlet-impact", "recoil-follow-through", "return-to-guard"]},
    "front_l": {"jobId": None, "paidUnits": 0, "phases": ["guard-prep", "shoulder-coil", "heavy-gauntlet-impact", "recoil-follow-through", "return-to-guard"]},
    "back_r":  {"jobId": "9fdb5943-ccfd-456d-aa2e-d07a49f3591c", "paidUnits": 3, "phases": ["guard-prep", "chamber-coil", "brawler-punch-impact", "recoil-retract", "return-to-guard"]},
    "back_l":  {"jobId": "eea7ce3b-0136-4f8b-8a6b-a6a871b24f68", "paidUnits": 3, "phases": ["guard-prep", "chamber-coil", "brawler-punch-impact", "recoil-retract", "return-to-guard"]},
}

for d, u_spec in UNARMED_SPECS.items():
    clip_dir = f"{V5_ROOT}/{d}/Unarmed"
    parent_clip_rel = f"characters/orc-v1/source/rear-recovery-v2/{d}/Unarmed/clip.json"
    parent_clip = read_json(parent_clip_rel)
    master_rel = f"{V5_ROOT}/aseprite/{d}/unarmed.aseprite"
    native_master_rel = f"{V5_ROOT}/aseprite/{d}/unarmed-native.aseprite"
    strip_rel = f"{clip_dir}/native-strip.png"
    durations_ms = [80, 110, 50, 90, 120]

    frames_out = []
    for idx in range(5):
        f_png = f"{clip_dir}/{idx:02d}.png"
        f_nat = f"{clip_dir}/native/{idx:02d}.png"
        frames_out.append({
            "index": idx,
            "png": f_png,
            "sha256": sha256_file(f_png),
            "nativePng": f_nat,
            "nativeSha256": sha256_file(f_nat),
            "durationMs": durations_ms[idx],
            "phase": u_spec["phases"][idx],
            "weaponVisible": False
        })

    is_rear = d.startswith("back_")
    u_clip_json = {
        "schemaVersion": 1,
        "revision": "main-orc-combat-rescue-v5",
        "id": "basic.unarmed",
        "character": "orc-v1",
        "state": "Unarmed",
        "legacySlotState": "Attack",
        "direction": d,
        "loop": False,
        "oneShot": True,
        "terminal": False,
        "canvas": [256, 256],
        "bodyOffset": [64, 64],
        "groundY": 190,
        "nativeCanvas": [128, 128],
        "nativeGroundY": 126,
        "ppu": 100,
        "frameCount": 5,
        "durationsMs": durations_ms,
        "totalDurationMs": 450,
        "master": master_rel,
        "masterSha256": sha256_file(master_rel),
        "nativeMaster": native_master_rel,
        "nativeMasterSha256": sha256_file(native_master_rel),
        "strip": strip_rel,
        "stripSha256": sha256_file(strip_rel),
        "nativeStrip": strip_rel,
        "nativeStripSha256": sha256_file(strip_rel),
        "visibilityPolicy": "attack-only-v1",
        "weaponVisible": False,
        "weaponOverlay": False,
        "contactEvent": {
            "frame": 2,
            "timeMs": 190,
            "status": "CANDIDATE_VISUAL_ONLY",
            "appliesDamage": False
        },
        "technicalStatus": "TECHNICALLY_COMPLETE",
        "artisticStatus": "VISUAL_REVIEW_REQUIRED",
        "artisticApproval": "PENDING_CREATOR",
        "provenance": {
            "parentClip": parent_clip_rel,
            "parentMaster": parent_clip["master"],
            "parentMasterSha256": sha256_file(parent_clip["master"]),
            "authoringScript": f"{EXP_ROOT}/scripts/author_unarmed_4views.lua",
            "bodyCleanupScript": None,
            "pixelLabJobId": u_spec["jobId"],
            "paidGenerationUnits": u_spec["paidUnits"],
            "bodyArtChanged": True,
            "bodyArtScope": (
                f"New PixelLab animate_with_skeleton_v3 whole-body rear brawler punch choreography ({u_spec['jobId']}), cleaned and off-hand anchored in Aseprite"
                if is_rear else
                "Preserved F00/F01/F02/F04 exact RGBA pixels; rebuilt F03 recoil from F02 torso/legs/guard-arm base with retracted (-4px/+2px) punching forearm and intact 72px gauntlet fist"
            ),
            "handArtChanged": False,
            "choreographyChanged": is_rear,
            "timingChanged": False
        },
        "frames": frames_out
    }
    write_json(f"{clip_dir}/clip.json", u_clip_json)
    print(f"Wrote {clip_dir}/clip.json (5 frames)")

# Specs from author_weapons_8clips.lua
WEAPON_SPECS = {
    ("front_r", "Sword"): {
        "id": "basic.sword-slash",
        "durationsMs": [30, 65, 35, 50, 45, 65, 35, 35, 100, 55, 80, 45, 90],
        "visibleInterval": [2, 10],
        "contactFrame": 6,
        "contactTimeMs": 290,
        "frames": [
            {"vis": False, "phase": "rest"},
            {"vis": False, "phase": "body-preparation"},
            {"vis": True, "gx": 101, "gy": 131, "rot": 315, "behind": False, "phase": "establish-grip"},
            {"vis": True, "gx": 88,  "gy": 118, "rot": 330, "behind": False, "phase": "anticipation"},
            {"vis": True, "gx": 98,  "gy": 100, "rot": 340, "behind": True,  "phase": "coil-behind"},
            {"vis": True, "gx": 98,  "gy": 89,  "rot": 345, "behind": True,  "phase": "apex-hold"},
            {"vis": True, "gx": 157, "gy": 112, "rot": 20,  "behind": False, "phase": "slash-release"},
            {"vis": True, "gx": 158, "gy": 134, "rot": 55,  "behind": False, "phase": "contact"},
            {"vis": True, "gx": 159, "gy": 142, "rot": 100, "behind": False, "phase": "follow-through"},
            {"vis": True, "gx": 129, "gy": 148, "rot": 102, "behind": False, "phase": "recoil"},
            {"vis": True, "gx": 110, "gy": 147, "rot": 105, "behind": False, "phase": "settle-grip"},
            {"vis": False, "phase": "release-grip"},
            {"vis": False, "phase": "return-to-guard"},
        ]
    },
    ("front_l", "Sword"): {
        "id": "basic.sword-slash",
        "durationsMs": [30, 65, 35, 50, 45, 65, 35, 35, 100, 55, 80, 45, 90],
        "visibleInterval": [2, 10],
        "contactFrame": 6,
        "contactTimeMs": 290,
        "frames": [
            {"vis": False, "phase": "rest"},
            {"vis": False, "phase": "body-preparation"},
            {"vis": True, "gx": 154, "gy": 131, "rot": 45,  "behind": False, "phase": "establish-grip"},
            {"vis": True, "gx": 167, "gy": 118, "rot": 30,  "behind": False, "phase": "anticipation"},
            {"vis": True, "gx": 157, "gy": 100, "rot": 20,  "behind": True,  "phase": "coil-behind"},
            {"vis": True, "gx": 157, "gy": 89,  "rot": 15,  "behind": True,  "phase": "apex-hold"},
            {"vis": True, "gx": 98,  "gy": 112, "rot": 340, "behind": False, "phase": "slash-release"},
            {"vis": True, "gx": 97,  "gy": 134, "rot": 305, "behind": False, "phase": "contact"},
            {"vis": True, "gx": 96,  "gy": 142, "rot": 260, "behind": False, "phase": "follow-through"},
            {"vis": True, "gx": 126, "gy": 148, "rot": 258, "behind": False, "phase": "recoil"},
            {"vis": True, "gx": 145, "gy": 147, "rot": 255, "behind": False, "phase": "settle-grip"},
            {"vis": False, "phase": "release-grip"},
            {"vis": False, "phase": "return-to-guard"},
        ]
    },
    ("front_r", "Axe"): {
        "id": "basic.axe-chop",
        "durationsMs": [40, 65, 35, 80, 155, 35, 115, 110, 130, 50, 90, 100],
        "visibleInterval": [2, 8],
        "contactFrame": 5,
        "contactTimeMs": 375,
        "frames": [
            {"vis": False, "phase": "rest"},
            {"vis": False, "phase": "body-preparation"},
            {"vis": True, "gx": 101, "gy": 131, "rot": 300, "behind": False, "phase": "establish-grip"},
            {"vis": True, "gx": 88,  "gy": 118, "rot": 325, "behind": False, "phase": "anticipation"},
            {"vis": True, "gx": 98,  "gy": 100, "rot": 350, "behind": True,  "phase": "overhead-coil"},
            {"vis": True, "gx": 146, "gy": 119, "rot": 35,  "behind": False, "phase": "cleave-drive"},
            {"vis": True, "gx": 148, "gy": 143, "rot": 85,  "behind": False, "phase": "heavy-impact"},
            {"vis": True, "gx": 138, "gy": 148, "rot": 90,  "behind": False, "phase": "weight-settle"},
            {"vis": True, "gx": 129, "gy": 148, "rot": 80,  "behind": False, "phase": "wrench-recovery"},
            {"vis": False, "phase": "release-grip"},
            {"vis": False, "phase": "shoulder-reset"},
            {"vis": False, "phase": "return-to-guard"},
        ]
    },
    ("front_l", "Axe"): {
        "id": "basic.axe-chop",
        "durationsMs": [40, 65, 35, 80, 155, 35, 115, 110, 130, 50, 90, 100],
        "visibleInterval": [2, 8],
        "contactFrame": 5,
        "contactTimeMs": 375,
        "frames": [
            {"vis": False, "phase": "rest"},
            {"vis": False, "phase": "body-preparation"},
            {"vis": True, "gx": 154, "gy": 131, "rot": 60,  "behind": False, "phase": "establish-grip"},
            {"vis": True, "gx": 167, "gy": 118, "rot": 35,  "behind": False, "phase": "anticipation"},
            {"vis": True, "gx": 157, "gy": 100, "rot": 10,  "behind": True,  "phase": "overhead-coil"},
            {"vis": True, "gx": 109, "gy": 119, "rot": 325, "behind": False, "phase": "cleave-drive"},
            {"vis": True, "gx": 107, "gy": 143, "rot": 275, "behind": False, "phase": "heavy-impact"},
            {"vis": True, "gx": 117, "gy": 148, "rot": 270, "behind": False, "phase": "weight-settle"},
            {"vis": True, "gx": 126, "gy": 148, "rot": 280, "behind": False, "phase": "wrench-recovery"},
            {"vis": False, "phase": "release-grip"},
            {"vis": False, "phase": "shoulder-reset"},
            {"vis": False, "phase": "return-to-guard"},
        ]
    },
    ("back_r", "Sword"): {
        "id": "basic.sword-slash",
        "durationsMs": [90, 80, 90, 80, 100, 80, 100, 110],
        "visibleInterval": [1, 6],
        "contactFrame": 4,
        "contactTimeMs": 340,
        "jobId": "06c2d829-7b45-4d6f-b64e-ce7db44ffac1",
        "frames": [
            {"vis": False, "phase": "guard-start"},
            {"vis": True, "gx": 172, "gy": 110, "rot": 335, "behind": False, "phase": "chamber-grip"},
            {"vis": True, "gx": 180, "gy": 91,  "rot": 355, "behind": True,  "phase": "lateral-windup"},
            {"vis": True, "gx": 184, "gy": 87,  "rot": 25,  "behind": True,  "phase": "slash-release"},
            {"vis": True, "gx": 185, "gy": 99,  "rot": 70,  "behind": False, "phase": "slash-contact"},
            {"vis": True, "gx": 181, "gy": 113, "rot": 105, "behind": False, "phase": "follow-through"},
            {"vis": True, "gx": 172, "gy": 124, "rot": 130, "behind": False, "phase": "recoil-settle"},
            {"vis": False, "phase": "guard-recovery"},
        ]
    },
    ("back_r", "Axe"): {
        "id": "basic.axe-chop",
        "durationsMs": [90, 80, 90, 80, 100, 80, 100, 110],
        "visibleInterval": [1, 6],
        "contactFrame": 4,
        "contactTimeMs": 340,
        "jobId": "d6d12081-e933-4a9c-98eb-358654566039",
        "frames": [
            {"vis": False, "phase": "guard-start"},
            {"vis": True, "gx": 160, "gy": 73,  "rot": 325, "behind": True,  "phase": "overhead-hoist"},
            {"vis": True, "gx": 157, "gy": 73,  "rot": 345, "behind": True,  "phase": "overhead-apex"},
            {"vis": True, "gx": 180, "gy": 90,  "rot": 25,  "behind": False, "phase": "cleave-drop"},
            {"vis": True, "gx": 184, "gy": 119, "rot": 75,  "behind": False, "phase": "heavy-impact"},
            {"vis": True, "gx": 173, "gy": 136, "rot": 110, "behind": False, "phase": "weight-sink"},
            {"vis": True, "gx": 164, "gy": 133, "rot": 130, "behind": False, "phase": "wrench-back"},
            {"vis": False, "phase": "guard-recovery"},
        ]
    },
    ("back_l", "Sword"): {
        "id": "basic.sword-slash",
        "durationsMs": [90, 80, 90, 80, 100, 80, 100, 110],
        "visibleInterval": [1, 6],
        "contactFrame": 4,
        "contactTimeMs": 340,
        "jobId": "10f597b6-5677-4bc4-8364-bc9b88511ff2",
        "frames": [
            {"vis": False, "phase": "guard-start"},
            {"vis": True, "gx": 80,  "gy": 86,  "rot": 25,  "behind": False, "phase": "chamber-grip"},
            {"vis": True, "gx": 76,  "gy": 76,  "rot": 5,   "behind": True,  "phase": "lateral-windup"},
            {"vis": True, "gx": 71,  "gy": 87,  "rot": 335, "behind": True,  "phase": "slash-release"},
            {"vis": True, "gx": 70,  "gy": 109, "rot": 290, "behind": False, "phase": "slash-contact"},
            {"vis": True, "gx": 71,  "gy": 130, "rot": 255, "behind": False, "phase": "follow-through"},
            {"vis": True, "gx": 86,  "gy": 136, "rot": 230, "behind": False, "phase": "recoil-settle"},
            {"vis": False, "phase": "guard-recovery"},
        ]
    },
    ("back_l", "Axe"): {
        "id": "basic.axe-chop",
        "durationsMs": [90, 80, 90, 80, 100, 80, 100, 110],
        "visibleInterval": [1, 6],
        "contactFrame": 4,
        "contactTimeMs": 340,
        "jobId": "b1e88042-81c9-4e11-a217-292be7eb2021",
        "frames": [
            {"vis": False, "phase": "guard-start"},
            {"vis": True, "gx": 92,  "gy": 78,  "rot": 35,  "behind": True,  "phase": "overhead-hoist"},
            {"vis": True, "gx": 98,  "gy": 73,  "rot": 15,  "behind": True,  "phase": "overhead-apex"},
            {"vis": True, "gx": 72,  "gy": 88,  "rot": 335, "behind": False, "phase": "cleave-drop"},
            {"vis": True, "gx": 72,  "gy": 129, "rot": 285, "behind": False, "phase": "heavy-impact"},
            {"vis": True, "gx": 82,  "gy": 137, "rot": 250, "behind": False, "phase": "weight-sink"},
            {"vis": True, "gx": 91,  "gy": 136, "rot": 230, "behind": False, "phase": "wrench-back"},
            {"vis": False, "phase": "guard-recovery"},
        ]
    }
}

# 2. Write clip.json for all 8 weapon clips
for (d, cat), spec in WEAPON_SPECS.items():
    clip_dir = f"{V5_ROOT}/{d}/{cat}"
    parent_clip_rel = f"{V4_ROOT}/{d}/{cat}/clip.json"
    parent_clip = read_json(parent_clip_rel)

    is_sword = (cat == "Sword")
    item_id = "recruit-sword" if is_sword else "militia-axe"
    item_name = "Espada do Recruta" if is_sword else "Machado de Milícia"
    item_grip = [48, 66] if is_sword else [36, 55]
    w_sprite = f"{V5_ROOT}/weapons/{cat}/{item_id}.png"
    w_master = f"{V5_ROOT}/weapons/{cat}/{item_id}.aseprite"
    w_def    = f"{V5_ROOT}/weapons/{cat}/weapon.json"

    master_rel = f"{clip_dir}/source/composite.aseprite"
    body_master_rel = f"{clip_dir}/source/body.aseprite"
    hand_master_rel = f"{clip_dir}/source/hand.aseprite"
    native_master_rel = f"{clip_dir}/source/native.aseprite"
    strip_rel = f"{clip_dir}/native-strip.png"
    comp_strip_rel = f"{clip_dir}/composite-strip.png"

    frames_out = []
    for idx, f_spec in enumerate(spec["frames"]):
        f_png = f"{clip_dir}/{idx:02d}.png"
        f_nat = f"{clip_dir}/native/{idx:02d}.png"
        l_wb  = f"{clip_dir}/layers/weaponBack/{idx:02d}.png"
        l_b   = f"{clip_dir}/layers/body/{idx:02d}.png"
        l_wf  = f"{clip_dir}/layers/weaponFront/{idx:02d}.png"
        l_hf  = f"{clip_dir}/layers/handFront/{idx:02d}.png"

        f_obj = {
            "index": idx,
            "png": f_png,
            "sha256": sha256_file(f_png),
            "durationMs": spec["durationsMs"][idx],
            "phase": f_spec["phase"],
            "weaponVisible": f_spec["vis"],
            "rightGrip": [f_spec.get("gx", 0), f_spec.get("gy", 0)],
            "rotationDeg": f_spec.get("rot", 0),
            "scale": 1,
            "weaponBehindBody": f_spec.get("behind", False),
            "handSource": "Articulated 4-finger armored gauntlet + thumb lock + leather wrist cuff wrapping handle shaft in Aseprite Lua",
            "layers": {
                "weaponBack": {
                    "png": l_wb,
                    "sha256": sha256_file(l_wb)
                },
                "body": {
                    "png": l_b,
                    "sha256": sha256_file(l_b)
                },
                "weaponFront": {
                    "png": l_wf,
                    "sha256": sha256_file(l_wf)
                },
                "handFront": {
                    "png": l_hf,
                    "sha256": sha256_file(l_hf)
                }
            },
            "nativePng": f_nat,
            "nativeSha256": sha256_file(f_nat)
        }
        frames_out.append(f_obj)

    is_rear = d.startswith("back_")
    clip_json = {
        "schemaVersion": 1,
        "revision": "main-orc-combat-rescue-v5",
        "id": spec["id"],
        "character": "orc-v1",
        "category": cat,
        "state": "Attack",
        "direction": d,
        "loop": False,
        "oneShot": True,
        "terminal": False,
        "canvas": [256, 256],
        "bodyOffset": [64, 64],
        "groundY": 190,
        "nativeCanvas": [128, 128],
        "nativeGroundY": 126,
        "ppu": 100,
        "frameCount": len(spec["durationsMs"]),
        "durationsMs": spec["durationsMs"],
        "totalDurationMs": sum(spec["durationsMs"]),
        "master": master_rel,
        "masterSha256": sha256_file(master_rel),
        "bodyMaster": body_master_rel,
        "bodyMasterSha256": sha256_file(body_master_rel),
        "handMaster": hand_master_rel,
        "handMasterSha256": sha256_file(hand_master_rel),
        "nativeMaster": native_master_rel,
        "nativeMasterSha256": sha256_file(native_master_rel),
        "strip": strip_rel,
        "stripSha256": sha256_file(strip_rel),
        "nativeStrip": strip_rel,
        "nativeStripSha256": sha256_file(strip_rel),
        "compositeStrip": comp_strip_rel,
        "compositeStripSha256": sha256_file(comp_strip_rel),
        "layerOrder": ["weaponBack", "body", "weaponFront", "handFront"],
        "visibleInterval": spec["visibleInterval"],
        "weaponVisible": True,
        "weaponOverlay": True,
        "weapon": {
            "id": item_id,
            "name": item_name,
            "grip": item_grip,
            "canvas": [96, 96],
            "sprite": w_sprite,
            "master": w_master,
            "spriteSha256": sha256_file(w_sprite),
            "masterSha256": sha256_file(w_master),
            "source": w_master,
            "sourceSha256": sha256_file(w_master),
            "definition": w_def,
            "scale": 1
        },
        "contactEvent": {
            "frame": spec["contactFrame"],
            "timeMs": spec["contactTimeMs"],
            "status": "CANDIDATE_VISUAL_ONLY",
            "appliesDamage": False
        },
        "technicalStatus": "TECHNICALLY_COMPLETE",
        "artisticStatus": "VISUAL_REVIEW_REQUIRED",
        "artisticApproval": "PENDING_CREATOR",
        "provenance": {
            "parentClip": parent_clip_rel,
            "parentMaster": parent_clip["master"],
            "parentMasterSha256": sha256_file(parent_clip["master"]),
            "authoringScript": f"{EXP_ROOT}/scripts/author_weapons_8clips.lua",
            "bodyCleanupScript": f"{EXP_ROOT}/scripts/clean_rear_weapon_bodies.lua" if is_rear else None,
            "pixelLabJobId": spec.get("jobId"),
            "paidGenerationUnits": 3 if is_rear else 0,
            "bodyArtChanged": is_rear,
            "bodyArtScope": (
                f"New PixelLab animate_with_skeleton_v3 whole-body empty-handed rear {cat.lower()} choreography ({spec.get('jobId')}), cleaned and off-hand anchored in Aseprite"
                if is_rear else
                "Frontal body choreography 100% preserved (exact RGBA pixel match to parent native/body frames)"
            ),
            "handArtChanged": True,
            "handArtScope": "Articulated 4-finger armored gauntlet + thumb lock + leather wrist cuff wrapping handle shaft (95-128 px per visible frame)",
            "choreographyChanged": is_rear,
            "timingChanged": False
        },
        "frames": frames_out
    }
    write_json(f"{clip_dir}/clip.json", clip_json)
    print(f"Wrote {clip_dir}/clip.json ({len(frames_out)} frames)")

# 3. Build patch-manifest.json for all 12 changed combat clips
parent_manifest = read_json(f"{V4_ROOT}/candidate28manifest.json")
parent_cells_by_id = {f"{c['direction']}/{c['action']}": c for c in parent_manifest["cells"]}

COMBAT_12 = [
    ("front_r", "Unarmed"),
    ("front_r", "Sword"),
    ("front_r", "Axe"),
    ("front_l", "Unarmed"),
    ("front_l", "Sword"),
    ("front_l", "Axe"),
    ("back_r", "Unarmed"),
    ("back_r", "Sword"),
    ("back_r", "Axe"),
    ("back_l", "Unarmed"),
    ("back_l", "Sword"),
    ("back_l", "Axe"),
]

patch_entries = []
for d, act in COMBAT_12:
    cell_id = f"{d}/{act}"
    p_cell = parent_cells_by_id[cell_id]
    clip_rel = f"{V5_ROOT}/{d}/{act}/clip.json"
    clip_data = read_json(clip_rel)
    p_clip_rel = p_cell["clipJson"]
    p_clip_data = read_json(p_clip_rel)

    # Classify each frame relative to parent
    frame_classifications = []
    for idx, f_obj in enumerate(clip_data["frames"]):
        if act == "Unarmed" and d.startswith("front_"):
            f_class = "REPAIRED_LOCAL_ASEPRITE" if idx == 3 else "PRESERVED_EXACT_RGBA"
            f_note = (
                "Rebuilt F03 recoil from F02 torso/legs/guard-arm base with retracted (-4px/+2px) punching forearm and intact visible fist gauntlet"
                if idx == 3 else
                "Preserved exact RGBA pixels from approved frontal Unarmed baseline"
            )
        elif act == "Unarmed" and d.startswith("back_"):
            f_class = "PRESERVED_GUARD_BOOKEND" if idx in (0, 4) else "NEW_PIXELLAB_SKELETON_AND_ASEPRITE_CLEANUP"
            f_note = (
                "Clean rear guard bookend anchored to canonical rear base"
                if idx in (0, 4) else
                f"New whole-body rear brawler punch frame from PixelLab job {clip_data['provenance']['pixelLabJobId']} + Aseprite off-hand/border cleanup"
            )
        elif act in ("Sword", "Axe") and d.startswith("front_"):
            if f_obj["weaponVisible"]:
                f_class = "PRESERVED_BODY_NEW_NATURAL_GRIP"
                f_note = f"Preserved exact frontal body choreography; authored articulated {cat} gauntlet handFront wrapping handle at grip {f_obj['rightGrip']}"
            else:
                f_class = "PRESERVED_EXACT_BOOKEND"
                f_note = "Preserved exact empty-handed frontal bookend frame (weapon hidden)"
        else:
            # Rear Sword / Axe
            if f_obj["weaponVisible"]:
                f_class = "NEW_REAR_BODY_CHOREOGRAPHY_AND_NATURAL_GRIP"
                f_note = f"New whole-body empty-handed rear {act} pose ({clip_data['provenance']['pixelLabJobId']}) + Aseprite off-hand/border cleanup + articulated gauntlet handFront at grip {f_obj['rightGrip']}"
            else:
                f_class = "CLEAN_REAR_BOOKEND_WEAPON_HIDDEN"
                f_note = "Clean empty-handed rear guard bookend frame (weapon hidden outside Attack window)"

        frame_classifications.append({
            "index": idx,
            "phase": f_obj.get("phase"),
            "durationMs": f_obj["durationMs"],
            "weaponVisible": f_obj.get("weaponVisible", False),
            "classification": f_class,
            "sha256": f_obj["sha256"],
            "nativeSha256": f_obj["nativeSha256"],
            "notes": f_note
        })

    if act == "Unarmed" and d.startswith("front_"):
        notes = f"Fixed {d}/Unarmed F03 late fist disappearance in Aseprite Lua using F02 torso/legs/guard-arm base with a retracted (-4px/+2px) punching forearm and intact 72px gauntlet fist; F00, F01, F02, F04 preserve exact RGBA pixels."
    elif act == "Unarmed" and d.startswith("back_"):
        notes = f"Replaced re-weaponed/truncated rear Unarmed with dedicated whole-body rear brawler punch choreography (PixelLab animate_with_skeleton_v3 job {clip_data['provenance']['pixelLabJobId']}) + Aseprite off-hand anchor and border cleanup."
    elif act in ("Sword", "Axe") and d.startswith("front_"):
        notes = f"Preserved 100% of approved {d}/{act} frontal body choreography and timing; replaced 12-40px speck handFront with 95-126px articulated 4-finger armored gauntlet + thumb lock + leather wrist cuff enclosing the {act.lower()} handle."
    else:
        tech_desc = (
            "horizontal/diagonal shoulder-height slash arc"
            if act == "Sword" else
            "steep high-overhead hoist (gy=73) and vertical-diagonal cleave drive"
        )
        notes = f"New whole-body empty-handed rear {act} choreography (PixelLab animate_with_skeleton_v3 job {clip_data['provenance']['pixelLabJobId']}) featuring distinct {tech_desc}, 0-shift anchored off-hand, zero body weapon contamination in layers-off, and 101-128px articulated gauntlet handFront grip."

    entry = {
        "direction": d,
        "action": act,
        "cellId": cell_id,
        "status": "ACTIVE_CANDIDATE",
        "isAffected": True,
        "clipJson": clip_rel,
        "clipSha256": sha256_file(clip_rel),
        "reviewStatus": "VISUAL_REVIEW_REQUIRED",
        "artisticStatus": "VISUAL_REVIEW_REQUIRED",
        "artisticApproval": "PENDING_CREATOR",
        "provenance": clip_data["provenance"]["authoringScript"],
        "notes": notes,
        "master": clip_data["master"],
        "masterSha256": clip_data["masterSha256"],
        "bodyMaster": clip_data.get("bodyMaster"),
        "bodyMasterSha256": clip_data.get("bodyMasterSha256"),
        "handMaster": clip_data.get("handMaster"),
        "handMasterSha256": clip_data.get("handMasterSha256"),
        "nativeMaster": clip_data["nativeMaster"],
        "nativeMasterSha256": clip_data["nativeMasterSha256"],
        "strip": clip_data["strip"],
        "stripSha256": clip_data["stripSha256"],
        "nativeStripSha256": clip_data["nativeStripSha256"],
        "durationsMs": clip_data["durationsMs"],
        "totalDurationMs": clip_data["totalDurationMs"],
        "frameCount": clip_data["frameCount"],
        "parentCell": {
            "manifest": f"{V4_ROOT}/candidate28manifest.json",
            "cellId": cell_id,
            "clipJson": p_clip_rel,
            "clipSha256": sha256_file(p_clip_rel)
        },
        "lineage": {
            "parentRevision": "main-orc-rear-reconstruction-v4",
            "parentClipJson": p_clip_rel,
            "parentMaster": p_clip_data.get("master"),
            "parentMasterSha256": sha256_file(p_clip_data["master"]) if p_clip_data.get("master") else None,
            "pixelLabJobId": clip_data["provenance"].get("pixelLabJobId"),
            "paidGenerationUnits": clip_data["provenance"].get("paidGenerationUnits", 0),
            "authoringScript": clip_data["provenance"]["authoringScript"],
            "bodyCleanupScript": clip_data["provenance"].get("bodyCleanupScript")
        },
        "frameClassifications": frame_classifications
    }
    patch_entries.append(entry)

patch_manifest = {
    "schemaVersion": 1,
    "patchId": "orc-v1.combat-rescue-v5.combat-patch-12",
    "characterId": "orc-v1",
    "characterName": "Verde Warcraft",
    "revision": "main-orc-combat-rescue-v5",
    "parentManifest": f"{V4_ROOT}/candidate28manifest.json",
    "parentManifestSha256": sha256_file(f"{V4_ROOT}/candidate28manifest.json"),
    "scope": "12 combat clips: 4 rear weapon clips (back_r/Sword, back_l/Sword, back_r/Axe, back_l/Axe), 4 Unarmed clips (front_r/Unarmed, front_l/Unarmed, back_r/Unarmed, back_l/Unarmed), and natural handle-enclosing grip across all 8 weapon clips (including front_r/Sword, front_l/Sword, front_r/Axe, front_l/Axe with preserved frontal body choreography).",
    "technicalStatus": "TECHNICALLY_COMPLETE",
    "artisticStatus": "VISUAL_REVIEW_REQUIRED",
    "artisticApproval": "PENDING_CREATOR",
    "affectedClipsCount": 12,
    "affectedFramesCount": sum(e["frameCount"] for e in patch_entries),
    "paidPixelLabJobsCount": 6,
    "paidPixelLabGenerationsTotal": 18,
    "weapons": {
        "Sword": f"{V5_ROOT}/weapons/Sword/weapon.json",
        "Axe": f"{V5_ROOT}/weapons/Axe/weapon.json"
    },
    "cells": patch_entries
}

write_json(f"{V5_ROOT}/patch-manifest.json", patch_manifest)
write_json(f"{EXP_ROOT}/patch-manifest.json", patch_manifest)
print(f"Wrote patch-manifest.json to {V5_ROOT} and {EXP_ROOT} ({len(patch_entries)} cells, {patch_manifest['affectedFramesCount']} frames)")
