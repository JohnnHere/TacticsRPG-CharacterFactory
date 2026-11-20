import json
import base64
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

ROOT = Path(".")
EXP_DIR = ROOT / "experiments/main-orc-combat-rescue-v5/combat"
REQ_DIR = EXP_DIR / "requests"
REC_DIR = EXP_DIR / "receipts"
RAW_DIR = EXP_DIR / "raw"
SHEET_DIR = EXP_DIR / "sheets"

import time

batch = [
    ("back_l_sword_v1", "10f597b6-c402-4578-8854-48d39360520c", 7, "back_l_base_128.png"),
    ("back_r_axe_v1",   "d6d12081-e75b-45ce-82d3-615b5238d8be", 7, "back_r_base_128.png"),
    ("back_l_axe_v1",   "b1e88042-3740-4c54-86a2-3222f34b48a8", 7, "back_l_base_128.png"),
    ("back_r_unarmed_v1", "9fdb5943-eeb1-4947-9ce8-b94bd6df7814", 4, "back_r_base_128.png"),
    ("back_l_unarmed_v1", "eea7ce3b-bca7-45b4-a6ec-bc17c89a0bea", 4, "back_l_base_128.png"),
]

# Poll until all 5 jobs report completed
for attempt in range(30):
    all_done = True
    for tag, jid, n_frames, base_name in batch:
        p_req = REQ_DIR / f"poll_{tag}.json"
        p_res = REC_DIR / f"poll_{tag}_res.json"
        p_req.write_text(json.dumps({"job_id": jid}), encoding="utf-8")
        subprocess.run([
            str(ROOT / "tmp/pixel-venv/Scripts/python.exe"),
            str(ROOT / "tools/pixellab-mcp.py"),
            "--call", "get_image",
            "--input", str(p_req),
            "--output", str(p_res)
        ], check=True)
        txt = p_res.read_text(encoding="utf-8")
        if "status: completed" not in txt:
            all_done = False
            print(f"[Attempt {attempt}] {tag} still processing...")
    if all_done:
        print("All 5 jobs completed!")
        break
    time.sleep(8)

for tag, jid, n_frames, base_name in batch:
    out_dir = RAW_DIR / tag
    out_dir.mkdir(parents=True, exist_ok=True)
    # Poll summary
    p_req = REQ_DIR / f"poll_{tag}.json"
    p_res = REC_DIR / f"poll_{tag}_res.json"
    p_req.write_text(json.dumps({"job_id": jid}), encoding="utf-8")
    subprocess.run([
        str(ROOT / "tmp/pixel-venv/Scripts/python.exe"),
        str(ROOT / "tools/pixellab-mcp.py"),
        "--call", "get_image",
        "--input", str(p_req),
        "--output", str(p_res)
    ], check=True)
    # Fetch each frame explicitly
    for idx in range(n_frames):
        idx_req = REQ_DIR / f"poll_{tag}_f{idx:02d}.json"
        idx_res = REC_DIR / f"poll_{tag}_f{idx:02d}_res.json"
        idx_req.write_text(json.dumps({"job_id": jid, "index": idx}), encoding="utf-8")
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
                (out_dir / f"{idx:02d}.png").write_bytes(base64.b64decode(it["data"]))
                break

    print(f"=== {tag} ({jid}) ===")
    for idx in range(n_frames):
        im = np.array(Image.open(out_dir / f"{idx:02d}.png").convert("RGBA"))
        vis = im[:, :, 3] > 0
        ys, xs = np.where(vis)
        print(f"  Frame {idx:02d}: vis={int(np.sum(vis))} bbox=[{xs.min()},{ys.min()}..{xs.max()},{ys.max()}]")

# Build combined contact sheet of all 5 new rear jobs
rows = len(batch)
sheet = Image.new("RGBA", (8 * 256 + 16, rows * 280 + 16), (24, 28, 34, 255))
draw = ImageDraw.Draw(sheet)

for r_i, (tag, jid, n_frames, base_name) in enumerate(batch):
    base_im = Image.open(RAW_DIR / base_name).convert("RGBA")
    frames = [base_im] + [Image.open(RAW_DIR / tag / f"{i:02d}.png").convert("RGBA") for i in range(n_frames)]
    y0 = 12 + r_i * 280
    for c_i, im in enumerate(frames):
        x0 = 8 + c_i * 256
        draw.rectangle([x0, y0 + 20, x0 + 255, y0 + 275], fill=(42, 46, 54, 255), outline=(90, 98, 110, 255))
        draw.line([(x0, y0 + 20 + 252), (x0 + 255, y0 + 20 + 252)], fill=(180, 80, 80, 180), width=1)
        sheet.alpha_composite(im.resize((256, 256), Image.NEAREST), (x0, y0 + 20))
        lbl = f"{tag} F00" if c_i == 0 else f"F0{c_i} (raw {c_i-1:02d})"
        draw.text((x0 + 6, y0 + 2), lbl, fill=(235, 240, 245, 255))

sheet_out = SHEET_DIR / "batch_rear_5jobs_sheet.png"
sheet.save(sheet_out)
print("Saved combined sheet:", sheet_out)
