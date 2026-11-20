import os, json, hashlib

weapons_def = [
    { "dir": "back_r", "weapon": "Sword", "num": 13, "weaponId": "recruit-sword" },
    { "dir": "back_r", "weapon": "Axe", "num": 12, "weaponId": "militia-axe" },
    { "dir": "back_l", "weapon": "Sword", "num": 13, "weaponId": "recruit-sword" },
    { "dir": "back_l", "weapon": "Axe", "num": 12, "weaponId": "militia-axe" }
]

def get_hash(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

for wd in weapons_def:
    base_clip_path = f"characters/orc-v1/source/complete-v1/{wd['dir']}/{wd['weapon']}/Attack/clip.json"
    with open(base_clip_path) as f:
        base_clip = json.load(f)
    
    cand_dir = f"characters/orc-v1/source/rear-recovery-v2/{wd['dir']}/{wd['weapon']}/Attack"
    out_frames = []
    
    for idx in range(wd["num"]):
        png_p = os.path.join(cand_dir, f"{idx:02d}.png").replace('\\', '/')
        sha = get_hash(png_p)
        orig_fr = base_clip["frames"][idx]
        
        fr_data = dict(orig_fr)
        fr_data["png"] = png_p
        fr_data["sha256"] = sha
        fr_data["nativePng"] = f"experiments/main-orc-rear-recovery-v2/cand_{wd['weapon'].lower()}_{wd['dir']}_{idx:02d}.png"
        out_frames.append(fr_data)
        
    strip_p = os.path.join(cand_dir, "native-strip.png").replace('\\', '/')
    
    cand_clip = dict(base_clip)
    cand_clip["revision"] = "main-orc-rear-recovery-v2"
    cand_clip["frames"] = out_frames
    cand_clip["strip"] = strip_p
    cand_clip["stripSha256"] = get_hash(strip_p)
    cand_clip["master"] = f"characters/orc-v1/source/aseprite/rear-recovery-v2/composite/{wd['dir']}/{wd['weapon'].lower()}-attack.aseprite"
    cand_clip["masterSha256"] = get_hash(cand_clip["master"])
    
    out_clip_p = os.path.join(cand_dir, "clip.json").replace('\\', '/')
    with open(out_clip_p, 'w', encoding='utf-8') as f:
        json.dump(cand_clip, f, indent=2)
    print(f"Saved {out_clip_p} ({cand_clip['frameCount']} frames)")
