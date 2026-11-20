"""Control comparison for T3: light pixels on the external silhouette, V5 baseline vs V6/V7.

If the V6 pass had introduced a light fringe ("halo") around the silhouette, the boundary-light
census of V6/V7 would grow against the V5 baseline that predates all V6 art edits. This script
measures that census frame by frame for the four frontal clips, at two thresholds.
"""
import json
import os
import sys
from collections import deque

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
V5BASE = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-rescue-v5", "grip-specialist")
V7BASE = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-recovery-v7", "frontal")
PAIRS = [
    ("front_l-Sword-full", "front_l-Sword-full"),
    ("front_l-Axe-full", "front_l-Axe-full"),
    ("front_r-Axe-full", "front_r-Axe-full"),
    ("full-front-r-sword", "full-front-r-sword"),
]


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def load(p):
    with Image.open(p) as im:
        return im.convert("RGBA")


def exterior(alpha, w, h):
    bg = [False] * (w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            i = y * w + x
            if alpha[i] < 128 and not bg[i]:
                bg[i] = True
                q.append(i)
    for y in range(h):
        for x in (0, w - 1):
            i = y * w + x
            if alpha[i] < 128 and not bg[i]:
                bg[i] = True
                q.append(i)
    while q:
        i = q.popleft()
        y, x = divmod(i, w)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h:
                j = ny * w + nx
                if alpha[j] < 128 and not bg[j]:
                    bg[j] = True
                    q.append(j)
    return bg


def census(path, t):
    im = load(path)
    px = list(im.getdata())
    w, h = im.size
    alpha = [p[3] for p in px]
    ext = exterior(alpha, w, h)
    n = 0
    for k in range(w * h):
        if alpha[k] < 128 or lum(px[k]) < t:
            continue
        x, y = k % w, k // w
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and ext[ny * w + nx]:
                n += 1
                break
    return n


out = []
for v7name, v5name in PAIRS:
    d7 = os.path.join(V7BASE, v7name)
    d5 = os.path.join(V5BASE, v5name)
    with open(os.path.join(d7, "clip.json"), encoding="utf-8") as f:
        meta = json.load(f)
    rows = []
    for i in range(meta["frameCount"]):
        ix = "%02d.png" % i
        rows.append({
            "frame": i,
            "v5_t120": census(os.path.join(d5, ix), 120),
            "v7_t120": census(os.path.join(d7, ix), 120),
            "v5_t145": census(os.path.join(d5, ix), 145),
            "v7_t145": census(os.path.join(d7, ix), 145),
        })
    out.append({"clip": v7name, "v5": os.path.relpath(d5, ROOT).replace("\\", "/"),
                "v7": os.path.relpath(d7, ROOT).replace("\\", "/"), "rows": rows})
    print("== %s" % v7name)
    for t in (120, 145):
        a = [r["v5_t%d" % t] for r in rows]
        b = [r["v7_t%d" % t] for r in rows]
        print("   t=%3d v5=%s" % (t, a))
        print("         v7=%s" % (b,))

p = os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7", "frontal", "detect", "v5-vs-v7-boundary.json")
with open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, indent=2)
    f.write("\n")
print("wrote", p)
