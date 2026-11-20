import os, json, hashlib

durations_ms = [70, 95, 115, 130, 290]
phases = ["fatal-stagger", "knees-buckle", "drop-to-knees", "collapse-impact", "terminal-defeated"]

def get_hash(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

for d in ['front_r', 'front_l']:
    cand_dir = f'characters/orc-v1/source/rear-recovery-v2/{d}/Defeat'
    out_frames = []
    
    for idx in range(5):
        png_path = os.path.join(cand_dir, f"{idx:02d}.png").replace('\\', '/')
        sha = get_hash(png_path)
        dur = durations_ms[idx]
        phase = phases[idx]
        
        out_frames.append({
            "index": idx,
            "png": png_path,
            "sha256": sha,
            "nativePng": f"experiments/main-orc-rear-recovery-v2/raw/defeat_{d}_04_candidate.png" if idx == 4 else f"characters/orc-v1/sprites/Animations/Defeat/defeat_{d}_{idx:02d}.png",
            "durationMs": dur,
            "phase": phase,
            "weaponVisible": False
        })
    
    strip_path = os.path.join(cand_dir, "native-strip.png").replace('\\', '/')
    
    clip_json = {
        "action": "Defeat",
        "direction": d,
        "canvas": [256, 256],
        "groundY": 190,
        "nativeCanvas": [128, 128],
        "nativeGroundY": 126,
        "totalFrames": 5,
        "totalDurationMs": sum(durations_ms),
        "durationsMs": durations_ms,
        "loop": False,
        "oneShot": True,
        "terminal": True,
        "weaponVisible": False,
        "provenance": {
            "generator": "Paseo ART DEV (Aseprite Lua)",
            "source": "experiments/main-orc-rear-recovery-v2/author_defeat_candidates.lua",
            "terminalCandidate": f"experiments/main-orc-rear-recovery-v2/raw/defeat_{d}_04_candidate.png",
            "jobId": "ef720a14-9a92-46be-b586-8d1295ccebf6" if d == 'front_r' else "f1601bbd-bd2d-4661-88ac-70d348bc6a0c"
        },
        "strip": strip_path,
        "frames": out_frames
    }
    
    clip_path = os.path.join(cand_dir, "clip.json").replace('\\', '/')
    with open(clip_path, 'w', encoding='utf-8') as f:
        json.dump(clip_json, f, indent=2)
    print(f"Saved {clip_path} (totalDuration: {clip_json['totalDurationMs']}ms)")
