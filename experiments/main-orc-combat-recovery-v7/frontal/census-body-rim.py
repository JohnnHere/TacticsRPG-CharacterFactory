"""T3 measurement: boundary (exterior-touching) light pixels at L>=145, attributed to their
owning layer, for the four frontal clips. Measurement only; writes no art."""
import json
import os
import sys
from collections import deque

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-recovery-v7", "frontal")
OUT = os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7", "frontal", "detect")
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


def clusters(mask, w, h):
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


out = {}
for clip in ("front_l-Sword-full", "front_l-Axe-full", "front_r-Axe-full", "full-front-r-sword"):
    d = os.path.join(BASE, clip)
    with open(os.path.join(d, "clip.json"), encoding="utf-8") as f:
        meta = json.load(f)
    n = meta["frameCount"]
    per_frame = []
    for i in range(n):
        ix = "%02d.png" % i
        comp = load(os.path.join(d, ix))
        px = list(comp.getdata())
        w, h = comp.size
        alpha = [p[3] for p in px]
        ext = exterior(alpha, w, h)
        light = [alpha[k] >= 128 and lum(px[k]) >= T for k in range(w * h)]
        lab = clusters(light, w, h)
        layers = {name: list(load(os.path.join(d, "layers", name, ix)).getdata()) for name in ORDER}
        owner = [None] * (w * h)
        for name in ORDER:
            lp = layers[name]
            for k in range(w * h):
                if owner[k] is None and lp[k][3] >= 128:
                    owner[k] = name
        body_hits = []
        weapon_hits = {"px": 0, "kinds": {}, "hits": []}
        for k in range(w * h):
            if not light[k]:
                continue
            x, y = k % w, k // w
            nb = [(y + dy) * w + (x + dx) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= x + dx < w and 0 <= y + dy < h]
            if not any(ext[j] for j in nb):
                continue
            lay = owner[k]
            if lay == "body":
                body_hits.append({"x": x, "y": y, "rgb": list(px[k][:3]), "L": round(lum(px[k]), 1),
                                  "cluster": lab[k]})
            else:
                weapon_hits["px"] += 1
                weapon_hits["hits"].append({"x": x, "y": y, "layer": lay, "rgb": list(px[k][:3]),
                                            "L": round(lum(px[k]), 1), "cluster": lab[k]})
                key = lay + "|" + ",".join(str(c) for c in px[k][:3])
                weapon_hits["kinds"][key] = weapon_hits["kinds"].get(key, 0) + 1
        per_frame.append({"frame": i, "bodyBoundaryLight": len(body_hits), "bodyHits": body_hits,
                          "weaponBoundaryLight": weapon_hits["px"],
                          "weaponColours": weapon_hits["kinds"],
                          "weaponHits": weapon_hits["hits"]})
    out[clip] = {"threshold": T, "frameCount": n, "perFrame": per_frame,
                 "bodyTotal": sum(f["bodyBoundaryLight"] for f in per_frame)}

dst = os.path.join(OUT, "body-rim-census.json")
with open(dst, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
print("WROTE", dst)
for clip, v in out.items():
    print(clip, "bodyBoundaryLightTotal=", v["bodyTotal"],
          [f["bodyBoundaryLight"] for f in v["perFrame"]])
    colours = {}
    for f in v["perFrame"]:
        for hit in f["bodyHits"]:
            key = ",".join(str(c) for c in hit["rgb"])
            colours[key] = colours.get(key, 0) + 1
    print("   body colours:", colours)
    wl = {}
    for f in v["perFrame"]:
        for k, c in f["weaponColours"].items():
            wl[k] = wl.get(k, 0) + c
    print("   weapon boundary px:", sum(f["weaponBoundaryLight"] for f in v["perFrame"]),
          " colours:", dict(sorted(wl.items(), key=lambda kv: -kv[1])[:6]))
