"""T3 detector: light contours on the four frontal clips (V7 copies).

Detectors (all numeric, no perception):
  H  halo-speck      light pixel (L>=120) touching the exterior background whose connected light
                     cluster (8-connectivity, L>=120) has <= 3 pixels
  I  isolated-light  light pixel with zero light 8-neighbours and no contact with the exterior
  B  boundary-light  every light pixel on the exterior boundary (flicker census, no judgement)
  D  inner-light-line light pixels forming a 1 px wide line that sits 1 px inside the silhouette
                     (a candidate double contour): light pixel whose inward neighbour is dark and
                     whose outward neighbour is opaque and whose own outward neighbour is exterior

For every hit the owning layer (first opaque layer in draw order) is resolved so a repair can be
aimed at the right cel. Writes build/light-contours-*.json.
"""
import json
import os
import sys
from collections import deque

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-recovery-v7", "frontal")
OUTDIR = os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7", "frontal", "detect")
LIGHT = 120.0
ORDER = ["weaponBack", "body", "weaponFront", "handFront"]


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


def clusters(light, w, h, minv):
    seen = [False] * (w * h)
    out = []
    for i in range(w * h):
        if not light[i] or seen[i]:
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
                        if light[j] and not seen[j]:
                            seen[j] = True
                            q.append(j)
        if len(comp) >= minv:
            out.append(comp)
    return out


def analyse(clip):
    d = os.path.join(BASE, clip)
    with open(os.path.join(d, "clip.json"), encoding="utf-8") as f:
        meta = json.load(f)
    n = meta["frameCount"]
    res = {"clip": clip, "direction": meta["direction"], "category": meta["category"],
           "frames": n, "lightThreshold": LIGHT, "perFrame": [], "hits": []}
    for i in range(n):
        ix = "%02d.png" % i
        comp = load(os.path.join(d, ix))
        px = list(comp.getdata())
        w, h = comp.size
        alpha = [p[3] for p in px]
        ext = exterior(alpha, w, h)
        light = [alpha[k] >= 128 and lum(px[k]) >= LIGHT for k in range(w * h)]
        layers = {}
        for name in ORDER:
            layers[name] = list(load(os.path.join(d, "layers", name, ix)).getdata())
        owner = [None] * (w * h)
        for name in ORDER:
            lp = layers[name]
            for k in range(w * h):
                if owner[k] is None and lp[k][3] >= 128:
                    owner[k] = name
        counts = {"H": 0, "I": 0, "B": 0, "D": 0}
        for k in range(w * h):
            if not light[k]:
                continue
            x, y = k % w, k // w
            nb = [(y + dy) * w + (x + dx) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= x + dx < w and 0 <= y + dy < h]
            touches_ext = any(ext[j] for j in nb)
            if touches_ext:
                counts["B"] += 1
            lighb = sum(1 for j in nb if light[j])
            if touches_ext and lighb <= 1 and len(px) > 0:
                counts["H"] += 1
            if lighb == 0 and not touches_ext:
                counts["I"] += 1
        res["perFrame"].append({"frame": i, "boundaryLight": counts["B"],
                                "haloSpeck": counts["H"], "isolatedLight": counts["I"]})
        # detailed hits for H and I
        for k in range(w * h):
            if not light[k]:
                continue
            x, y = k % w, k // w
            nb = [(y + dy) * w + (x + dx) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= x + dx < w and 0 <= y + dy < h]
            lighb = sum(1 for j in nb if light[j])
            touches_ext = any(ext[j] for j in nb)
            if lighb == 0:
                res["hits"].append({"frame": i, "x": x, "y": y, "kind": "isolated-light",
                                    "rgba": list(px[k][:3]), "L": round(lum(px[k]), 1),
                                    "layer": owner[k], "atBoundary": touches_ext})
            elif lighb == 1 and touches_ext:
                res["hits"].append({"frame": i, "x": x, "y": y, "kind": "halo-speck?",
                                    "rgba": list(px[k][:3]), "L": round(lum(px[k]), 1),
                                    "layer": owner[k], "atBoundary": True})
    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "light-contours-%s.json" % clip), "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=2)
        f.write("\n")
    print("%-22s frames=%2d boundaryLight=%s" % (clip, n, [p["boundaryLight"] for p in res["perFrame"]]))
    print("%-22s hits=%d %s" % ("", len(res["hits"]),
                                sorted({(h["kind"], h["layer"]) for h in res["hits"]})))
    return res


if __name__ == "__main__":
    for clip in sys.argv[1:] or ["front_l-Sword-full", "front_l-Axe-full", "front_r-Axe-full", "full-front-r-sword"]:
        analyse(clip)
