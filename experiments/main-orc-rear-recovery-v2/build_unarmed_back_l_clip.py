import os, json, hashlib

cand_dir = 'characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed'
frames_data = [
    { "index": 0, "phase": "guard-prep", "durationMs": 80 },
    { "index": 1, "phase": "shoulder-coil", "durationMs": 110 },
    { "index": 2, "phase": "heavy-gauntlet-impact", "durationMs": 60 },
    { "index": 3, "phase": "follow-through", "durationMs": 90 },
    { "index": 4, "phase": "recovery-settle", "durationMs": 110 }
]

def get_hash(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

out_frames = []
durations_ms = []

for fd in frames_data:
    idx = fd["index"]
    png_path = os.path.join(cand_dir, f"{idx:02d}.png").replace('\\', '/')
    sha = get_hash(png_path)
    dur = fd["durationMs"]
    durations_ms.append(dur)
    
    out_frames.append({
        "index": idx,
        "png": png_path,
        "sha256": sha,
        "nativePng": f"experiments/main-orc-rear-recovery-v2/cand_unarmed_back_l_{idx:02d}.png",
        "nativeSha256": get_hash(f"experiments/main-orc-rear-recovery-v2/cand_unarmed_back_l_{idx:02d}.png"),
        "durationMs": dur,
        "phase": fd["phase"],
        "weaponVisible": False
    })

strip_path = os.path.join(cand_dir, "native-strip.png").replace('\\', '/')

clip_json = {
    "action": "Unarmed",
    "direction": "back_l",
    "canvas": [256, 256],
    "groundY": 190,
    "nativeCanvas": [128, 128],
    "nativeGroundY": 126,
    "totalFrames": len(out_frames),
    "totalDurationMs": sum(durations_ms),
    "durationsMs": durations_ms,
    "loop": False,
    "weaponVisible": False,
    "provenance": {
        "generator": "Paseo ART DEV (Aseprite Lua)",
        "source": "experiments/main-orc-rear-recovery-v2/author_unarmed_back_l.lua",
        "impactKey": "experiments/main-orc-rear-recovery-v2/raw/punch_impact_key_back_l.png",
        "jobId": "72c2a726-a756-4511-963d-c6bfbb185985"
    },
    "strip": strip_path,
    "frames": out_frames
}

clip_path = os.path.join(cand_dir, "clip.json").replace('\\', '/')
with open(clip_path, 'w', encoding='utf-8') as f:
    json.dump(clip_json, f, indent=2)

print(f"Saved {clip_path} (totalDuration: {clip_json['totalDurationMs']}ms)")
