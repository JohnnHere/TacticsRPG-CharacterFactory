"""Dump body-layer light pixels that touch the exterior silhouette (T3 halo candidates)."""
import json
import os
import sys
from collections import deque

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-recovery-v7", "frontal")
ORDER = ["weaponBack", "body", "weaponFront", "handFront"]
T = float(os.environ.get("T3_T", "145"))


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


def sized(mask, w, h):
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
with open(os.path.join(d, "clip.json"), encoding="utf-8") as f:
    meta = json.load(f)
n = meta["frameCount"]
print("== %s (T>=%g)" % (clip, T))
for i in range(n):
    ix = "%02d.png" % i
    comp = load(os.path.join(d, ix))
    px = list(comp.getdata())
    w, h = comp.size
    alpha = [p[3] for p in px]
    ext = exterior(alpha, w, h)
    body = list(load(os.path.join(d, "layers", "body", ix)).getdata())
    light = [alpha[k] >= 128 and lum(px[k]) >= T for k in range(w * h)]
    lab = sized(light, w, h)
    hits = []
    for k in range(w * h):
        x, y = k % w, k // w
        if body[k][3] < 128 or lum(body[k]) < T:
            continue
        nb = [(y + dy) * w + (x + dx) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
              if 0 <= x + dx < w and 0 <= y + dy < h]
        if not any(ext[j] for j in nb):
            continue
        # 3x3 pattern of the composite: '.' exterior, 'o' interior empty, 'l' light, '#' opaque dark
        pat = []
        for dy in (-1, 0, 1):
            row = ""
            for dx in (-1, 0, 1):
                xx, yy = x + dx, y + dy
                if not (0 <= xx < w and 0 <= yy < h):
                    row += " "
                    continue
                j = yy * w + xx
                if alpha[j] < 128:
                    row += "." if ext[j] else "o"
                elif lum(px[j]) >= T:
                    row += "l"
                else:
                    row += "#"
            pat.append(row)
        hits.append({"x": x, "y": y, "rgba": list(body[k][:3]), "L": round(lum(body[k]), 1),
                     "cluster": lab[k], "pat": pat})
    if hits:
        print("  F%02d  %d hit(s)" % (i, len(hits)))
        for hh in hits:
            print("     (%3d,%3d) body=%s L=%5.1f cluster=%d" % (hh["x"], hh["y"], tuple(hh["rgba"]), hh["L"], hh["cluster"]))
            for row in hh["pat"]:
                print("         " + row)
