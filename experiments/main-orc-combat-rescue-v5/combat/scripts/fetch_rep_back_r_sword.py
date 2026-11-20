import json
import base64
import re
import urllib.request
import subprocess
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")
EXP_DIR = ROOT / "experiments/main-orc-combat-rescue-v5/combat"
REQ_DIR = EXP_DIR / "requests"
REC_DIR = EXP_DIR / "receipts"
RAW_DIR = EXP_DIR / "raw/back_r_sword_v1"
RAW_DIR.mkdir(parents=True, exist_ok=True)

job_id = "06c2d829-7b45-4d6f-b64e-ce7db44ffac1"

# First wait_for_jobs if needed
wait_req = REQ_DIR / "wait_back_r_sword_v1.json"
wait_res = REC_DIR / "wait_back_r_sword_v1_res.json"
wait_req.write_text(json.dumps({"timeout_seconds": 120, "min_finished": 1}), encoding="utf-8")

subprocess.run([
    str(ROOT / "tmp/pixel-venv/Scripts/python.exe"),
    str(ROOT / "tools/pixellab-mcp.py"),
    "--call", "wait_for_jobs",
    "--input", str(wait_req),
    "--output", str(wait_res)
], check=True)
print("wait_for_jobs result:", wait_res.read_text(encoding="utf-8")[:400])

# Poll get_image for each frame 0..6 (or full job)
poll_req = REQ_DIR / "poll_back_r_sword_v1.json"
poll_res = REC_DIR / "poll_back_r_sword_v1_res.json"
poll_req.write_text(json.dumps({"job_id": job_id}), encoding="utf-8")

subprocess.run([
    str(ROOT / "tmp/pixel-venv/Scripts/python.exe"),
    str(ROOT / "tools/pixellab-mcp.py"),
    "--call", "get_image",
    "--input", str(poll_req),
    "--output", str(poll_res)
], check=True)

res = json.loads(poll_res.read_text(encoding="utf-8"))
content = res.get("content", [])
saved_frames = []

# Check how images are returned in content
img_idx = 0
for item in content:
    if item.get("type") == "image" and item.get("data"):
        raw_bytes = base64.b64decode(item["data"])
        out_p = RAW_DIR / f"{img_idx:02d}.png"
        out_p.write_bytes(raw_bytes)
        saved_frames.append(str(out_p))
        img_idx += 1
    elif item.get("type") == "text":
        txt = item.get("text", "")
        print("Text block:\n", txt)
        # Also check if there are download URLs for frames not inline
        urls = re.findall(r"https://[^\s)\"']+\.png[^\s)\"']*", txt)
        if urls:
            print(f"Found {len(urls)} URLs in text block")

# If fewer than 7 frames came back inline, fetch each index 0..6 explicitly
if len(saved_frames) < 7:
    print(f"Inline returned {len(saved_frames)} frames; fetching indices 0..6 explicitly...")
    saved_frames = []
    for idx in range(7):
        idx_req = REQ_DIR / f"poll_back_r_sword_v1_f{idx:02d}.json"
        idx_res = REC_DIR / f"poll_back_r_sword_v1_f{idx:02d}_res.json"
        idx_req.write_text(json.dumps({"job_id": job_id, "index": idx}), encoding="utf-8")
        subprocess.run([
            str(ROOT / "tmp/pixel-venv/Scripts/python.exe"),
            str(ROOT / "tools/pixellab-mcp.py"),
            "--call", "get_image",
            "--input", str(idx_req),
            "--output", str(idx_res)
        ], check=True)
        r_idx = json.loads(idx_res.read_text(encoding="utf-8"))
        for it in r_idx.get("content", []):
            if it.get("type") == "image" and it.get("data"):
                out_p = RAW_DIR / f"{idx:02d}.png"
                out_p.write_bytes(base64.b64decode(it["data"]))
                saved_frames.append(str(out_p))
                break

print(f"Saved {len(saved_frames)} frames to {RAW_DIR}")
for idx in range(len(saved_frames)):
    p = RAW_DIR / f"{idx:02d}.png"
    im = np.array(Image.open(p).convert("RGBA"))
    vis = im[:, :, 3] > 0
    ys, xs = np.where(vis)
    print(f"  Frame {idx:02d}: size={im.shape[1]}x{im.shape[0]} vis={int(np.sum(vis))} bbox=[{xs.min()},{ys.min()}..{xs.max()},{ys.max()}]")
