"""T3 structural census: (1) small light clusters touching the exterior in ANY layer,
(2) light lines inset 1 px from the silhouette, (3) 1 px contour spikes.

Everything is measured on the composite plus the per-layer cels, and reported per frame so that
flicker (a feature present in one frame and absent in its neighbours) can be judged numerically.
"""
import json
import os
import sys
from collections import deque

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-recovery-v7", "frontal")
ORDER = ["weaponBack", "body", "weaponFront", "handFront"]
T = 145.0


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


def nbrs(k, w, h):
    x, y = k % w, k // w
    return [((y + dy) * w + (x + dx), x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
            if 0 <= x + dx < w and 0 <= y + dy < h]


def cluster_sizes(mask, w, h):
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
            for j, _x, _y in nbrs(k, w, h):
                if mask[j] and not seen[j]:
                    seen[j] = True
                    q.append(j)
        for k in comp:
            lab[k] = len(comp)
    return lab


def analyse(clip):
    d = os.path.join(BASE, clip)
    with open(os.path.join(d, "clip.json"), encoding="utf-8") as f:
        meta = json.load(f)
    out = {"clip": clip, "frames": [], "smallLightOnBoundary": [], "insetLightLine": [], "spike": []}
    for i in range(meta["frameCount"]):
        ix = "%02d.png" % i
        comp = load(os.path.join(d, ix))
        px = list(comp.getdata())
        w, h = comp.size
        alpha = [p[3] for p in px]
        ext = exterior(alpha, w, h)
        light = [alpha[k] >= 128 and lum(px[k]) >= T for k in range(w * h)]
        # 4-connectivity clusters: a 4-connected run is the meaningful "line" unit
        lab4 = cluster_sizes(light, w, h)
        owner = [None] * (w * h)
        for name in ORDER:
            lp = list(load(os.path.join(d, "layers", name, ix)).getdata())
            for k in range(w * h):
                if owner[k] is None and lp[k][3] >= 128:
                    owner[k] = name
        small, inset, spike = [], [], []
        for k in range(w * h):
            x, y = k % w, k // w
            nb = nbrs(k, w, h)
            touches = any(ext[j] for j, _a, _b in nb)
            if light[k] and touches and lab4[k] <= 2:
                small.append({"x": x, "y": y, "layer": owner[k], "rgba": list(px[k][:3]),
                              "L": round(lum(px[k]), 1), "run": lab4[k]})
            if light[k] and not touches and lab4[k] >= 3:
                # is there an opaque dark pixel between it and the background?
                for j, jx, jy in nb:
                    if ext[j]:
                        continue
                    inner = [(k2, x2, y2) for k2, x2, y2 in nbrs(j, w, h) if (x2, y2) != (jx, jy)]
                    if any(ext[k2] for k2, _x2, _y2 in inner) and not light[j] and alpha[j] >= 128:
                        inset.append({"x": x, "y": y, "layer": owner[k], "run": lab4[k]})
                        break
            if alpha[k] >= 128:
                dark_op = [j for j, _a, _b in nb if alpha[j] >= 128]
                extn = [j for j, _a, _b in nb if ext[j]]
                if len(dark_op) == 1 and len(extn) >= 2:
                    spike.append({"x": x, "y": y, "layer": owner[k], "rgba": list(px[k][:3])})
        out["frames"].append({"frame": i, "lightBoundary": sum(1 for k in range(w * h) if light[k] and any(
            ext[j] for j, _a, _b in nbrs(k, w, h))), "smallLight": len(small), "insetLine": len(inset),
            "spike": len(spike)})
        for s in small:
            s["frame"] = i
            out["smallLightOnBoundary"].append(s)
        for s in inset:
            s["frame"] = i
            out["insetLightLine"].append(s)
        for s in spike:
            s["frame"] = i
            out["spike"].append(s)
    print("== %s" % clip)
    print("   frame     :", [f["frame"] for f in out["frames"]])
    print("   lightBnd  :", [f["lightBoundary"] for f in out["frames"]])
    print("   smallLight:", [f["smallLight"] for f in out["frames"]])
    print("   insetLine :", [f["insetLine"] for f in out["frames"]])
    print("   spike     :", [f["spike"] for f in out["frames"]])
    os.makedirs(os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7", "frontal", "detect"), exist_ok=True)
    with open(os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7", "frontal", "detect",
                           "structural-%s.json" % clip), "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2)
        f.write("\n")
    return out


if __name__ == "__main__":
    for c in sys.argv[1:] or ["front_l-Sword-full", "front_l-Axe-full", "front_r-Axe-full", "full-front-r-sword"]:
        analyse(c)
