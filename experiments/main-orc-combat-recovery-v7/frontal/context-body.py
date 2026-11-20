"""Exact 7x7 RGBA context around a pixel in the body (and composite) of a clip."""
import json
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-recovery-v7", "frontal")


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def load(p):
    with Image.open(p) as im:
        return im.convert("RGBA")


clip, frame = sys.argv[1], int(sys.argv[2])
coords = [tuple(int(v) for v in a.split(",")) for a in sys.argv[3:]]
d = os.path.join(BASE, clip)
ix = "%02d.png" % frame
body = load(os.path.join(d, "layers", "body", ix))
comp = load(os.path.join(d, ix))
for (cx, cy) in coords:
    print("== %s F%02d (%d,%d) body=%s L=%.1f" % (clip, frame, cx, cy, body.getpixel((cx, cy))[:3], lum(body.getpixel((cx, cy)))))
    for y in range(cy - 3, cy + 4):
        row = []
        for x in range(cx - 3, cx + 4):
            p = body.getpixel((x, y))
            if p[3] == 0:
                row.append("  ..  ")
            else:
                row.append("%02x%02x%02x" % p[:3])
        print("   y=%3d %s" % (y, " ".join(row)))
