import os
import json
import hashlib

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

# 1. back_l Walk clip.json
walkL_candDir = 'characters/orc-v1/source/rear-recovery-v2/back_l/Walk'
walkL_natMaster = 'characters/orc-v1/source/aseprite/rear-recovery-v2/native/walk-back_l.aseprite'
walkL_compMaster = 'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/walk-unarmed.aseprite'
walkL_strip = os.path.join(walkL_candDir, 'native-strip.png')

clip_walk_l = {
    "schemaVersion": 1,
    "revision": "main-orc-rear-recovery-v2",
    "id": "locomotion.walk-v2",
    "character": "orc-v1",
    "state": "Walk",
    "legacySlotState": "Walk",
    "direction": "back_l",
    "loop": True,
    "oneShot": False,
    "terminal": False,
    "canvas": [256, 256],
    "bodyOffset": [64, 64],
    "groundY": 190,
    "nativeCanvas": [128, 128],
    "nativeGroundY": 126,
    "ppu": 100,
    "frameCount": 8,
    "durationsMs": [160] * 8,
    "totalDurationMs": 1280,
    "master": walkL_compMaster.replace('\\', '/'),
    "masterSha256": sha256_file(walkL_compMaster),
    "nativeMaster": walkL_natMaster.replace('\\', '/'),
    "nativeMasterSha256": sha256_file(walkL_natMaster),
    "strip": walkL_strip.replace('\\', '/'),
    "stripSha256": sha256_file(walkL_strip),
    "visibilityPolicy": "attack-only-v1",
    "weaponVisible": False,
    "weaponOverlay": False,
    "contactEvent": None,
    "frames": [
        {
            "index": i,
            "png": f"characters/orc-v1/source/rear-recovery-v2/back_l/Walk/{i:02d}.png",
            "sha256": sha256_file(os.path.join(walkL_candDir, f"{i:02d}.png")),
            "durationMs": 160,
            "phase": f"stride-step-{i:02d}",
            "groundY": 190,
            "nativeGroundY": 126
        }
        for i in range(8)
    ]
}

with open(os.path.join(walkL_candDir, 'clip.json'), 'w', encoding='utf-8') as f:
    json.dump(clip_walk_l, f, indent=2)
print("Saved back_l Walk clip.json")

# 2. back_r Unarmed clip.json
unarmR_candDir = 'characters/orc-v1/source/rear-recovery-v2/back_r/Unarmed'
unarmR_natMaster = 'characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-back_r.aseprite'
unarmR_compMaster = 'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/unarmed-attack.aseprite'
unarmR_strip = os.path.join(unarmR_candDir, 'native-strip.png')

unarmR_durationsMs = [40, 60, 60, 50, 50, 80, 60, 80, 100] # 580 ms total
phases = [
    "rest-guard", "anticipation-onset", "torso-coil-load", "lunge-drive",
    "punch-strike-thrust", "impact-peak-extension", "follow-through-recoil",
    "recovery-return", "terminal-neutral-rest"
]

clip_unarmed_r = {
    "schemaVersion": 1,
    "revision": "main-orc-rear-recovery-v2",
    "id": "combat.unarmed-strike-v2",
    "character": "orc-v1",
    "state": "Unarmed",
    "legacySlotState": "Unarmed",
    "direction": "back_r",
    "loop": False,
    "oneShot": True,
    "terminal": False,
    "canvas": [256, 256],
    "bodyOffset": [64, 64],
    "groundY": 190,
    "nativeCanvas": [128, 128],
    "nativeGroundY": 126,
    "ppu": 100,
    "frameCount": 9,
    "durationsMs": unarmR_durationsMs,
    "totalDurationMs": sum(unarmR_durationsMs),
    "master": unarmR_compMaster.replace('\\', '/'),
    "masterSha256": sha256_file(unarmR_compMaster),
    "nativeMaster": unarmR_natMaster.replace('\\', '/'),
    "nativeMasterSha256": sha256_file(unarmR_natMaster),
    "strip": unarmR_strip.replace('\\', '/'),
    "stripSha256": sha256_file(unarmR_strip),
    "visibilityPolicy": "attack-only-v1",
    "weaponVisible": False,
    "weaponOverlay": False,
    "contactEvent": {
        "frame": 5,
        "timeMs": 260,
        "status": "CANDIDATE_VISUAL_ONLY",
        "appliesDamage": False,
        "description": "Heavy gauntlet unarmed punch impact extension at frame 5 (260ms)"
    },
    "frames": [
        {
            "index": i,
            "png": f"characters/orc-v1/source/rear-recovery-v2/back_r/Unarmed/{i:02d}.png",
            "sha256": sha256_file(os.path.join(unarmR_candDir, f"{i:02d}.png")),
            "durationMs": unarmR_durationsMs[i],
            "phase": phases[i],
            "groundY": 190,
            "nativeGroundY": 126
        }
        for i in range(9)
    ]
}

with open(os.path.join(unarmR_candDir, 'clip.json'), 'w', encoding='utf-8') as f:
    json.dump(clip_unarmed_r, f, indent=2)
print("Saved back_r Unarmed clip.json")
