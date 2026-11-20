#!/usr/bin/env python3
"""Stage A diagnosis: build labeled contact sheets from the REAL exported frames.

Read-only over dist/editor build; writes only under
experiments/main-orc-rear-recovery-v2/diagnosis/.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
BUILD = ROOT / "dist/editor/orc-v1-complete-v1/b178422e1f7fc19f068c"
OUT = ROOT / "experiments/main-orc-rear-recovery-v2/diagnosis"

# job id -> display label
JOBS = [
    ("comp-walk-back_r", "Rear Walk back_r"),
    ("comp-walk-back_l", "Rear Walk back_l"),
    ("comp-walk-front_r", "REF front Walk front_r"),
    ("comp-unarmed-back_r", "Rear Unarmed back_r"),
    ("comp-unarmed-back_l", "Rear Unarmed back_l"),
    ("comp-unarmed-front_r", "Front Unarmed front_r"),
    ("comp-unarmed-front_l", "Front Unarmed front_l"),
    ("comp-sword-attack-back_r", "Rear Sword back_r"),
    ("comp-sword-attack-back_l", "Rear Sword back_l"),
    ("comp-axe-attack-back_r", "Rear Axe back_r"),
    ("comp-axe-attack-back_l", "Rear Axe back_l"),
    ("comp-defeat-front_r", "Front Defeat front_r"),
    ("comp-defeat-front_l", "Front Defeat front_l"),
    ("comp-defeat-back_r", "Rear Defeat back_r"),
    ("comp-defeat-back_l", "Rear Defeat back_l"),
    ("comp-hit-front_r", "Front Hit front_r"),
    ("comp-hit-back_r", "Rear Hit back_r"),
]


def load_meta(job: str) -> dict:
    p = BUILD / "jobs" / job / "sheet.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    index = []
    for job, label in JOBS:
        jdir = BUILD / "jobs" / job / "frames"
        if not jdir.exists():
            print(f"MISSING {job}", file=sys.stderr)
            continue
        frames = sorted(jdir.glob("*.png"))
        if not frames:
            print(f"NOFRAMES {job}", file=sys.stderr)
            continue
        meta = load_meta(job)
        cell = 256
        pad = 6
        label_h = 16
        width = len(frames) * (cell + pad) + pad
        height = cell + pad * 2 + label_h
        sheet = Image.new("RGBA", (width, height), (24, 26, 30, 255))
        draw = ImageDraw.Draw(sheet)
        for i, f in enumerate(frames):
            im = Image.open(f).convert("RGBA")
            if im.size != (cell, cell):
                im = im.resize((cell, cell), Image.NEAREST)
            x = pad + i * (cell + pad)
            # checker so transparency is visible
            draw.rectangle([x, pad, x + cell - 1, pad + cell - 1], fill=(48, 50, 56, 255))
            sheet.alpha_composite(im, (x, pad))
            draw.text((x + 3, pad + 3), f"{i}", fill=(255, 230, 120, 255))
        draw.text((pad, height - label_h + 2), f"{label}  [{job}]  frames={len(frames)}",
                  fill=(235, 235, 240, 255))
        name = f"{job}.png"
        sheet.save(OUT / name)
        index.append({"job": job, "label": label, "frames": len(frames),
                      "sheet": name, "meta": {k: meta.get(k) for k in
                                              ("durations", "frameCount", "totalDurationMs")
                                              if k in meta}})
        print(f"OK {job} frames={len(frames)}")
    (OUT / "index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
