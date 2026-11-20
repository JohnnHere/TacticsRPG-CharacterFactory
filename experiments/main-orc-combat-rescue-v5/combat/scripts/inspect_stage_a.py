import json
import hashlib
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")
OUT_DIR = ROOT / "experiments/main-orc-combat-rescue-v5/combat"
OUT_DIR.mkdir(parents=True, exist_ok=True)

manifest_path = ROOT / "characters/orc-v1/source/rear-reconstruction-v4/candidate28manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

combat_actions = {"Sword", "Axe", "Unarmed"}
entries = manifest.get("cells") or manifest.get("clips") or manifest.get("entries") or []
clips = [c for c in entries if c["action"] in combat_actions]

print(f"Found {len(clips)} combat clips in v4 manifest:")
for c in clips:
    print(f"  {c['direction']}/{c['action']} -> {c['clipJson']} ({c['status']})")

# Inspect each clip's clip.json and frame properties
summary = {}
for c in clips:
    key = f"{c['direction']}/{c['action']}"
    cj_path = ROOT / c["clipJson"]
    cj = json.loads(cj_path.read_text(encoding="utf-8"))
    summary[key] = {
        "clipJson": c["clipJson"],
        "frameCount": cj.get("frameCount"),
        "durationsMs": [f.get("durationMs") for f in cj.get("frames", [])],
        "totalMs": sum(f.get("durationMs", 0) for f in cj.get("frames", [])),
        "visibleInterval": cj.get("visibleInterval"),
        "frames": []
    }
    for f in cj.get("frames", []):
        idx = f.get("index")
        f_info = {
            "index": idx,
            "phase": f.get("phase"),
            "weaponVisible": f.get("weaponVisible"),
            "socket": f.get("socket"),
            "occlusion": f.get("occlusion"),
        }
        # Check handFront pixel count if weapon clip
        layers = f.get("layers", {})
        if "handFront" in layers and layers["handFront"]:
            hf_val = layers["handFront"]
            hf_rel = hf_val["png"] if isinstance(hf_val, dict) else hf_val
            hf_path = ROOT / hf_rel
            if hf_path.exists():
                im = np.array(Image.open(hf_path).convert("RGBA"))
                vis = np.argwhere(im[:, :, 3] > 0)
                f_info["handFrontPixels"] = int(len(vis))
                if len(vis) > 0:
                    ys, xs = vis[:, 0], vis[:, 1]
                    f_info["handFrontBbox256"] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
            f_info["rightGrip"] = f.get("rightGrip")
            f_info["rotationDeg"] = f.get("rotationDeg")
            f_info["weaponBehindBody"] = f.get("weaponBehindBody")
        summary[key]["frames"].append(f_info)

(OUT_DIR / "stage-a-baseline-inspection.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

# Check what raw PixelLab frames exist in rear-recovery-v2/raw
raw_v2 = ROOT / "experiments/main-orc-rear-recovery-v2/raw"
if raw_v2.exists():
    print("\nExisting raw files in experiments/main-orc-rear-recovery-v2/raw:")
    for p in sorted(raw_v2.rglob("*")):
        if p.is_file():
            print(" ", p.relative_to(raw_v2))

# Inspect front_r and front_l Unarmed frames 00..04 in detail (checking fist region)
for d in ["front_r", "front_l", "back_r", "back_l"]:
    u_dir = ROOT / f"characters/orc-v1/source/rear-recovery-v2/{d}/Unarmed"
    print(f"\nUnarmed {d}:")
    prev_arr = None
    for idx in range(5):
        p = u_dir / f"{idx:02d}.png"
        im = np.array(Image.open(p).convert("RGBA"))
        # crop to 128x128 native (offset 64,64)
        nat = im[64:192, 64:192]
        vis = np.argwhere(nat[:, :, 3] > 0)
        ys, xs = vis[:, 0], vis[:, 1]
        diff_cnt = 0
        diff_bbox = None
        if prev_arr is not None:
            diff_mask = np.any(nat != prev_arr, axis=2)
            diff_pts = np.argwhere(diff_mask)
            diff_cnt = len(diff_pts)
            if diff_cnt > 0:
                dys, dxs = diff_pts[:, 0], diff_pts[:, 1]
                diff_bbox = [int(dxs.min()), int(dys.min()), int(dxs.max()), int(dys.max())]
        print(f"  F{idx:02d}: vis={len(vis)} bbox=[{xs.min()},{ys.min()}..{xs.max()},{ys.max()}] diff_from_prev={diff_cnt} diff_bbox={diff_bbox}")
        prev_arr = nat
