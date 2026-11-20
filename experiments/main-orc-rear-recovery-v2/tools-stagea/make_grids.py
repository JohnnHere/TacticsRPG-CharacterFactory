#!/usr/bin/env python3
"""Stage A: cropped/zoomed grid sheets from real exported frames.

Crops to the union bbox of opaque pixels (margin), scales with NEAREST so
pixel clusters stay readable, lays frames out in a grid.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
BUILD = ROOT / "dist/editor/orc-v1-complete-v1/b178422e1f7fc19f068c"
OUT = ROOT / "experiments/main-orc-rear-recovery-v2/diagnosis"

JOBS = [
    ("comp-walk-back_r", "Rear Walk back_r", 4),
    ("comp-walk-back_l", "Rear Walk back_l", 4),
    ("comp-walk-front_r", "REF front Walk front_r", 4),
    ("comp-unarmed-back_r", "Rear Unarmed back_r", 5),
    ("comp-unarmed-back_l", "Rear Unarmed back_l", 5),
    ("comp-unarmed-front_r", "Front Unarmed front_r", 5),
    ("comp-sword-attack-back_r", "Rear Sword back_r", 5),
    ("comp-sword-attack-back_l", "Rear Sword back_l", 5),
    ("comp-axe-attack-back_r", "Rear Axe back_r", 4),
    ("comp-axe-attack-back_l", "Rear Axe back_l", 4),
    ("comp-defeat-front_r", "Front Defeat front_r", 5),
    ("comp-defeat-front_l", "Front Defeat front_l", 5),
    ("comp-defeat-back_r", "Rear Defeat back_r", 5),
    ("comp-hit-front_r", "Front Hit front_r", 5),
    ("comp-hit-back_r", "Rear Hit back_r", 5),
]

ZOOM = 2
MARGIN = 10
BG = (30, 32, 36, 255)


def union_bbox(frames):
    x0, y0, x1, y1 = 10**9, 10**9, -1, -1
    for f in frames:
        im = Image.open(f).convert("RGBA")
        bb = im.getbbox()
        if not bb:
            continue
        x0 = min(x0, bb[0]); y0 = min(y0, bb[1])
        x1 = max(x1, bb[2]); y1 = max(y1, bb[3])
    if x1 < 0:
        return None
    return (x0, y0, x1, y1)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    report = []
    for job, label, cols in JOBS:
        jdir = BUILD / "jobs" / job / "frames"
        frames = sorted(jdir.glob("*.png"))
        if not frames:
            print(f"MISSING {job}", file=sys.stderr); continue
        bb = union_bbox(frames)
        bb = (max(0, bb[0] - MARGIN), max(0, bb[1] - MARGIN),
              min(256, bb[2] + MARGIN), min(256, bb[3] + MARGIN))
        cw, ch = (bb[2] - bb[0]) * ZOOM, (bb[3] - bb[1]) * ZOOM
        rows = (len(frames) + cols - 1) // cols
        pad, lab = 8, 14
        W = cols * (cw + pad) + pad
        H = rows * (ch + pad + lab) + pad + lab
        sheet = Image.new("RGBA", (W, H), BG)
        d = ImageDraw.Draw(sheet)
        for i, f in enumerate(frames):
            im = Image.open(f).convert("RGBA").crop(bb)
            im = im.resize((cw, ch), Image.NEAREST)
            r, c = divmod(i, cols)
            x = pad + c * (cw + pad)
            y = pad + lab + r * (ch + pad + lab)
            d.rectangle([x - 1, y - 1, x + cw, y + ch], fill=(48, 50, 56, 255))
            sheet.alpha_composite(im, (x, y))
            d.text((x, y - lab + 2), f"f{i}", fill=(255, 226, 110, 255))
        d.text((pad, 2), f"{label} [{job}] bbox={bb} zoom={ZOOM}x",
               fill=(235, 235, 240, 255))
        name = f"grid-{job}.png"
        sheet.save(OUT / name)
        report.append({"job": job, "bbox": list(bb), "sheet": name, "frames": len(frames)})
        print(f"OK {job} bbox={bb} -> {name} {W}x{H}")
    (OUT / "grids-index.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
