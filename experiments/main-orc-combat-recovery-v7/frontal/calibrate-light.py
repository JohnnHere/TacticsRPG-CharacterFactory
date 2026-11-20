"""Calibration for the T3 light-contour detector: distribution of light pixels by layer,
boundary contact and cluster size, for a range of thresholds. Measurement only."""
import os
import sys
from collections import deque

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-recovery-v7", "frontal")
ORDER = ["weaponBack", "body", "weaponFront", "handFront"]
THRESHOLDS = (130, 140, 145, 150, 160, 170)


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


def sized_clusters(mask, w, h):
    seen = [False] * (w * h)
    lab = [0] * (w * h)
    for i in range(w * h):
        if not mask[i] or seen[i]:
            continue
        comp = []
        q = deque([i])
        seen[i] = True
        while q:
            k = q.popleft()
            comp.append(k)
            y, x = divmod(k, w)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        j = ny * w + nx
                        if mask[j] and not seen[j]:
                            seen[j] = True
                            q.append(j)
        for k in comp:
            lab[k] = len(comp)
    return lab


clip = sys.argv[1]
d = os.path.join(BASE, clip)
import json
with open(os.path.join(d, "clip.json"), encoding="utf-8") as f:
    meta = json.load(f)
n = meta["frameCount"]

for t in THRESHOLDS:
    per_layer = {k: {"total": 0, "boundary": 0, "smallOnBoundary": 0} for k in ORDER}
    per_frame_boundary = []
    for i in range(n):
        ix = "%02d.png" % i
        comp = load(os.path.join(d, ix))
        px = list(comp.getdata())
        w, h = comp.size
        alpha = [p[3] for p in px]
        ext = exterior(alpha, w, h)
        light = [alpha[k] >= 128 and lum(px[k]) >= t for k in range(w * h)]
        lab = sized_clusters(light, w, h)
        layers = {name: list(load(os.path.join(d, "layers", name, ix)).getdata()) for name in ORDER}
        owner = [None] * (w * h)
        for name in ORDER:
            lp = layers[name]
            for k in range(w * h):
                if owner[k] is None and lp[k][3] >= 128:
                    owner[k] = name
        bcount = 0
        for k in range(w * h):
            if not light[k]:
                continue
            x, y = k % w, k // w
            lay = owner[k]
            per_layer[lay]["total"] += 1
            nb = [(y + dy) * w + (x + dx) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= x + dx < w and 0 <= y + dy < h]
            if any(ext[j] for j in nb):
                per_layer[lay]["boundary"] += 1
                bcount += 1
                if lab[k] <= 3:
                    per_layer[lay]["smallOnBoundary"] += 1
        per_frame_boundary.append(bcount)
    print("t=%3d boundary per frame %s" % (t, per_frame_boundary))
    for k in ORDER:
        v = per_layer[k]
        if v["total"]:
            print("    %-11s total=%5d boundary=%4d smallOnBoundary=%4d" % (k, v["total"], v["boundary"], v["smallOnBoundary"]))
