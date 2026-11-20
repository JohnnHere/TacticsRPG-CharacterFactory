#!/usr/bin/env python3
"""Stage A: per-frame motion metrics from real exported frames."""
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
BUILD = ROOT / "dist/editor/orc-v1-complete-v1/b178422e1f7fc19f068c"
OUT = ROOT / "experiments/main-orc-rear-recovery-v2/diagnosis"

JOBS = [
    "comp-walk-back_r", "comp-walk-back_l", "comp-walk-front_r",
    "comp-unarmed-back_r", "comp-unarmed-back_l", "comp-unarmed-front_r",
    "comp-sword-attack-back_r", "comp-sword-attack-back_l",
    "comp-axe-attack-back_r", "comp-axe-attack-back_l",
    "comp-defeat-front_r", "comp-defeat-back_r",
    "comp-hit-front_r", "comp-hit-back_r",
    "comp-idle-back_r", "comp-idle-front_r",
]


def load(p):
    im = Image.open(p).convert("RGBA")
    return im


def metrics(im):
    a = im.getchannel("A").point(lambda v: 255 if v > 8 else 0)
    bb = a.getbbox()
    px = a.load()
    w, h = a.size
    n = 0
    sx = sy = 0
    rows = {}
    for y in range(h):
        for x in range(w):
            if px[x, y]:
                n += 1; sx += x; sy += y
                rows[y] = rows.get(y, 0) + 1
    if n == 0:
        return None
    top = min(rows)
    # "skin/head top": topmost row in the top 30% band of the sprite
    return {
        "bbox": list(bb), "opaque": n,
        "top": top, "bottom": bb[3],
        "height": bb[3] - bb[1],
        "cx": round(sx / n, 2), "cy": round(sy / n, 2),
    }


def changed_pct(a, b):
    pa, pb = a.getchannel("A").load(), b.getchannel("A").load()
    w, h = a.size
    diff = 0
    tot = 0
    for y in range(h):
        for x in range(w):
            va, vb = pa[x, y], pb[x, y]
            if va > 8 or vb > 8:
                tot += 1
                if abs(va - vb) > 8:
                    diff += 1
    return round(100.0 * diff / max(tot, 1), 2)


def main():
    out = {}
    for job in JOBS:
        jdir = BUILD / "jobs" / job / "frames"
        frames = sorted(jdir.glob("*.png"))
        if not frames:
            continue
        imgs = [load(f) for f in frames]
        ms = [metrics(im) for im in imgs]
        # duplicate detection by exact bytes
        hashes = [f.name for f in frames]
        import hashlib
        sig = [hashlib.sha256(f.read_bytes()).hexdigest()[:12] for f in frames]
        dup = {}
        for i, s in enumerate(sig):
            dup.setdefault(s, []).append(i)
        dups = [v for v in dup.values() if len(v) > 1]
        # pairwise diff vs frame 0 and consecutive
        vs0 = [changed_pct(im, imgs[0]) for im in imgs]
        consec = [changed_pct(imgs[i], imgs[i + 1]) for i in range(len(imgs) - 1)]
        # centroid x range (horizontal sway) and top range (vertical bob)
        tops = [m["top"] for m in ms]
        cxs = [m["cx"] for m in ms]
        heights = [m["height"] for m in ms]
        op = [m["opaque"] for m in ms]
        out[job] = {
            "frames": len(frames),
            "durations": json.loads((BUILD / "jobs" / job / "sheet.json").read_text(encoding="utf-8")).get("durations")
            if (BUILD / "jobs" / job / "sheet.json").exists() else None,
            "top_range": [min(tops), max(tops)],
            "bob_px": max(tops) - min(tops),
            "cx_range": [min(cxs), max(cxs)],
            "sway_px": round(max(cxs) - min(cxs), 2),
            "height_range": [min(heights), max(heights)],
            "opaque_range": [min(op), max(op)],
            "dup_frames": dups,
            "changed_vs_f0_pct": vs0,
            "consecutive_diff_pct": consec,
            "per_frame": ms,
        }
    (OUT / "metrics.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    for job, d in out.items():
        print(f"{job}: bob={d['bob_px']}px sway={d['sway_px']}px h={d['height_range']} "
              f"dup={d['dup_frames']} consec={d['consecutive_diff_pct']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
