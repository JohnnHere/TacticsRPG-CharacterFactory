import os
import json
import hashlib

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

cand_dir = 'characters/orc-v1/source/rear-recovery-v2/back_r/Walk'
nat_master = 'characters/orc-v1/source/aseprite/rear-recovery-v2/native/walk-back_r.aseprite'
comp_master = 'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/walk-unarmed.aseprite'
strip_file = os.path.join(cand_dir, 'native-strip.png')

clip_meta = {
    "schemaVersion": 1,
    "revision": "main-orc-rear-recovery-v2",
    "id": "locomotion.walk-v2",
    "character": "orc-v1",
    "state": "Walk",
    "legacySlotState": "Walk",
    "direction": "back_r",
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
    "master": comp_master.replace('\\', '/'),
    "masterSha256": sha256_file(comp_master),
    "nativeMaster": nat_master.replace('\\', '/'),
    "nativeMasterSha256": sha256_file(nat_master),
    "strip": strip_file.replace('\\', '/'),
    "stripSha256": sha256_file(strip_file),
    "visibilityPolicy": "attack-only-v1",
    "weaponVisible": False,
    "weaponOverlay": False,
    "contactEvent": None,
    "frames": [
        {
            "index": i,
            "png": f"characters/orc-v1/source/rear-recovery-v2/back_r/Walk/{i:02d}.png",
            "sha256": sha256_file(os.path.join(cand_dir, f"{i:02d}.png")),
            "durationMs": 160,
            "phase": f"stride-step-{i:02d}",
            "groundY": 190,
            "nativeGroundY": 126
        }
        for i in range(8)
    ]
}

out_clip = os.path.join(cand_dir, 'clip.json')
with open(out_clip, 'w', encoding='utf-8') as f:
    json.dump(clip_meta, f, indent=2)

print(f"Saved clip.json with hashes to {out_clip}")
