import os, json, hashlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
CLIP_REL = "characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword"
V5_ROOT = "characters/orc-v1/source/combat-rescue-v5/combat"
V4_ROOT = "characters/orc-v1/source/rear-reconstruction-v4"
EXP_REL = "experiments/main-orc-combat-rescue-v5/combat/qa5-repair1"

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

durations_ms = [30, 65, 35, 50, 45, 65, 35, 35, 100, 55, 80, 45, 90]
anatomy = {
    0:  {"vis": False, "sh": [104,102], "el": [92,118],  "wr": [94,133],  "pa": [96,138],  "ang": 0,   "phase": "rest"},
    1:  {"vis": False, "sh": [104,103], "el": [95,115],  "wr": [98,122],  "pa": [101,125], "ang": 0,   "phase": "body-preparation"},
    2:  {"vis": True,  "sh": [104,103], "el": [93,117],  "wr": [96,126],  "pa": [100,130], "ang": 332, "phase": "establish-grip"},
    3:  {"vis": True,  "sh": [105,100], "el": [87,108],  "wr": [83,116],  "pa": [81,119],  "ang": 336, "phase": "anticipation"},
    4:  {"vis": True,  "sh": [105,97],  "el": [85,103],  "wr": [79,109],  "pa": [76,111],  "ang": 330, "phase": "coil-behind"},
    5:  {"vis": True,  "sh": [107,98],  "el": [89,104],  "wr": [84,109],  "pa": [80,111],  "ang": 346, "phase": "apex-hold"},
    6:  {"vis": True,  "sh": [112,102], "el": [126,109], "wr": [136,111], "pa": [142,115], "ang": 78,  "phase": "slash-release"},
    7:  {"vis": True,  "sh": [114,103], "el": [132,117], "wr": [145,124], "pa": [152,129], "ang": 108, "phase": "contact"},
    8:  {"vis": True,  "sh": [110,104], "el": [126,129], "wr": [141,139], "pa": [148,143], "ang": 128, "phase": "follow-through"},
    9:  {"vis": True,  "sh": [106,105], "el": [109,129], "wr": [118,144], "pa": [122,149], "ang": 115, "phase": "recoil"},
    10: {"vis": True,  "sh": [104,104], "el": [97,122],  "wr": [104,136], "pa": [109,141], "ang": 95,  "phase": "settle-grip"},
    11: {"vis": False, "sh": [104,103], "el": [95,120],  "wr": [99,136],  "pa": [102,140], "ang": 0,   "phase": "release-grip"},
    12: {"vis": False, "sh": [104,102], "el": [92,118],  "wr": [94,133],  "pa": [96,138],  "ang": 0,   "phase": "return-to-guard"},
}

write_json(f"{EXP_REL}/diagnostics/front_r_sword_anatomy.json", {
    str(k): {
        "shoulder": v["sh"],
        "elbow": v["el"],
        "wrist": v["wr"],
        "palm": v["pa"],
        "weaponVisible": v["vis"],
        "rotationDeg": v["ang"],
        "phase": v["phase"]
    } for k, v in anatomy.items()
})

w_sprite = f"{V5_ROOT}/weapons/Sword/recruit-sword.png"
w_master = f"{V5_ROOT}/weapons/Sword/recruit-sword.aseprite"
w_def    = f"{V5_ROOT}/weapons/Sword/weapon.json"

master_rel        = f"{CLIP_REL}/source/composite.aseprite"
body_master_rel   = f"{CLIP_REL}/source/body.aseprite"
hand_master_rel   = f"{CLIP_REL}/source/hand.aseprite"
native_master_rel = f"{CLIP_REL}/source/native.aseprite"
strip_rel         = f"{CLIP_REL}/native-strip.png"
comp_strip_rel    = f"{CLIP_REL}/composite-strip.png"

frames_out = []
for idx in range(13):
    a = anatomy[idx]
    f_png = f"{CLIP_REL}/{idx:02d}.png"
    f_nat = f"{CLIP_REL}/native/{idx:02d}.png"
    l_wb  = f"{CLIP_REL}/layers/weaponBack/{idx:02d}.png"
    l_b   = f"{CLIP_REL}/layers/body/{idx:02d}.png"
    l_wf  = f"{CLIP_REL}/layers/weaponFront/{idx:02d}.png"
    l_hf  = f"{CLIP_REL}/layers/handFront/{idx:02d}.png"

    frames_out.append({
        "index": idx,
        "png": f_png,
        "sha256": sha256_file(f_png),
        "durationMs": durations_ms[idx],
        "phase": a["phase"],
        "weaponVisible": a["vis"],
        "rightGrip": a["pa"] if a["vis"] else [0, 0],
        "anatomy": {
            "shoulder": a["sh"],
            "elbow": a["el"],
            "wrist": a["wr"],
            "palm": a["pa"]
        },
        "rotationDeg": a["ang"],
        "scale": 1,
        "weaponBehindBody": False,
        "handSource": "Real body forearm/wrist gauntlet cuff bridge + 4 articulated fingers and thumb lock enclosing handle shaft in Aseprite Lua",
        "layers": {
            "weaponBack": {"png": l_wb, "sha256": sha256_file(l_wb)},
            "body":       {"png": l_b,  "sha256": sha256_file(l_b)},
            "weaponFront":{"png": l_wf, "sha256": sha256_file(l_wf)},
            "handFront":  {"png": l_hf, "sha256": sha256_file(l_hf)},
        },
        "nativePng": f_nat,
        "nativeSha256": sha256_file(f_nat)
    })

clip_json = {
    "schemaVersion": 1,
    "revision": "main-orc-combat-rescue-v5-qa5-repair1",
    "id": "basic.sword-slash",
    "character": "orc-v1",
    "category": "Sword",
    "state": "Attack",
    "direction": "front_r",
    "loop": False,
    "oneShot": True,
    "terminal": False,
    "canvas": [256, 256],
    "bodyOffset": [64, 64],
    "groundY": 190,
    "nativeCanvas": [128, 128],
    "nativeGroundY": 126,
    "ppu": 100,
    "frameCount": 13,
    "durationsMs": durations_ms,
    "totalDurationMs": 730,
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
    "visibleInterval": [2, 10],
    "weaponVisible": True,
    "weaponOverlay": True,
    "weapon": {
        "id": "recruit-sword",
        "name": "Espada do Recruta",
        "grip": [48, 66],
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
        "frame": 6,
        "timeMs": 290,
        "status": "CANDIDATE_VISUAL_ONLY",
        "appliesDamage": False
    },
    "technicalStatus": "TECHNICALLY_COMPLETE",
    "artisticStatus": "VISUAL_REVIEW_REQUIRED",
    "artisticApproval": "PENDING_CREATOR",
    "provenance": {
        "parentClip": f"{V4_ROOT}/front_r/Sword/clip.json",
        "parentMaster": f"{V4_ROOT}/front_r/Sword/source/composite.aseprite",
        "parentMasterSha256": sha256_file(f"{V4_ROOT}/front_r/Sword/source/composite.aseprite"),
        "authoringScript": f"{EXP_REL}/scripts/author_front_r_sword_qa5.lua",
        "bodyCleanupScript": None,
        "pixelLabJobId": None,
        "paidGenerationUnits": 0,
        "bodyArtChanged": False,
        "bodyArtScope": "Frontal body choreography 100% preserved (exact RGBA pixel match to parent native/body frames)",
        "handArtChanged": True,
        "handArtScope": "Anatomical grip centered on real distal leather fist with forearm wrist-cuff bridge and 4 articulated fingers + thumb lock enclosing wooden handle shaft",
        "choreographyChanged": False,
        "timingChanged": False
    },
    "frames": frames_out
}

write_json(f"{CLIP_REL}/clip.json", clip_json)
print("Wrote", f"{CLIP_REL}/clip.json")
