#!/usr/bin/env python3
"""Stage A: layer-level composition analysis for weapon attack clips.

Measures, per frame: body-layer motion (does the torso actually move/rotate?),
hand layer presence, weapon layer presence/position, and where the weapon
sits relative to the body silhouette.
"""
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "characters/orc-v1/source/complete-v1"
OUT = ROOT / "experiments/main-orc-rear-recovery-v2/diagnosis"

TARGETS = [
    ("back_r", "Sword", "Attack"),
    ("back_l", "Sword", "Attack"),
    ("front_r", "Sword", "Attack"),
    ("back_r", "Axe", "Attack"),
    ("back_l", "Axe", "Attack"),
    ("front_r", "Axe", "Attack"),
]


def info(im):
    a = im.getchannel("A").point(lambda v: 255 if v > 8 else 0)
    bb = a.getbbox()
    if not bb:
        return {"empty": True}
    px = a.load()
    n = sx = sy = 0
    for y in range(bb[1], bb[3]):
        for x in range(bb[0], bb[2]):
            if px[x, y]:
                n += 1; sx += x; sy += y
    return {"empty": False, "bbox": list(bb), "opaque": n,
            "cx": round(sx / n, 2), "cy": round(sy / n, 2),
            "h": bb[3] - bb[1], "w": bb[2] - bb[0]}


def main():
    report = {}
    for direction, action, sub in TARGETS:
        base = SRC / direction / action / sub
        if not base.exists():
            continue
        layers_dir = base / "layers"
        if not layers_dir.exists():
            continue
        layer_names = sorted(d.name for d in layers_dir.iterdir() if d.is_dir())
        frames = sorted((base).glob("[0-9][0-9].png"))
        clip = json.loads((base / "clip.json").read_text(encoding="utf-8"))
        entry = {
            "clip": {k: clip.get(k) for k in
                     ("frameCount", "durationsMs", "totalDurationMs", "loop",
                      "oneShot", "weaponVisible", "visibleInterval", "frames")},
            "layers": layer_names,
            "per_frame": [],
        }
        for i, f in enumerate(frames):
            row = {"frame": i}
            for ln in layer_names:
                p = layers_dir / ln / f.name
                if p.exists():
                    row[ln] = info(Image.open(p).convert("RGBA"))
            row["composite"] = info(Image.open(f).convert("RGBA"))
            entry["per_frame"].append(row)
        report[f"{direction}/{action}"] = entry
    out = OUT / "layers.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    for key, e in report.items():
        print(f"== {key} layers={e['layers']}")
        print(f"   clip={e['clip']}")
        for row in e["per_frame"]:
            bits = []
            for ln in e["layers"]:
                d = row.get(ln, {})
                bits.append(f"{ln}:" + ("empty" if d.get("empty")
                                        else f"o={d['opaque']} cx={d['cx']} cy={d['cy']}"))
            c = row["composite"]
            bits.append("COMP:" + ("empty" if c.get("empty")
                                   else f"h={c['h']} cx={c['cx']} cy={c['cy']}"))
            print(f"   f{row['frame']:02d} " + " | ".join(bits))
    return 0


if __name__ == "__main__":
    sys.exit(main())
