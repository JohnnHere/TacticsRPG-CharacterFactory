"""What changed from the V5 baseline to the V7 copies, per layer and per frame.

Confirms (a) which frontal frames were touched at all by V5 -> V6 -> V7, and (b) whether the weapon
layers were ever repainted, which would be the only way a frontal pass could introduce a weapon halo.
"""
import json
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
V5BASE = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-rescue-v5", "grip-specialist")
V7BASE = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-recovery-v7", "frontal")
CLIPS = ["front_l-Sword-full", "front_l-Axe-full", "front_r-Axe-full", "full-front-r-sword"]
LAYERS = ["body", "weaponBack", "weaponFront", "handFront"]


def load(p):
    with Image.open(p) as im:
        return im.convert("RGBA")


def diff(a, b):
    pa, pb = list(a.getdata()), list(b.getdata())
    w = a.size[0]
    return [(i % w, i // w) for i in range(len(pa)) if pa[i] != pb[i]]


result = {}
for clip in CLIPS:
    d5, d7 = os.path.join(V5BASE, clip), os.path.join(V7BASE, clip)
    with open(os.path.join(d7, "clip.json"), encoding="utf-8") as f:
        meta = json.load(f)
    rows = []
    for i in range(meta["frameCount"]):
        ix = "%02d.png" % i
        row = {"frame": i}
        for name in LAYERS:
            p5 = os.path.join(d5, "layers", name, ix)
            p7 = os.path.join(d7, "layers", name, ix)
            if not (os.path.exists(p5) and os.path.exists(p7)):
                row[name] = None
                continue
            d = diff(load(p5), load(p7))
            row[name] = len(d)
            if d and name != "body":
                xs = [t[0] for t in d]
                ys = [t[1] for t in d]
                row[name + "Bbox"] = [min(xs), min(ys), max(xs), max(ys)]
        cd = diff(load(os.path.join(d5, ix)), load(os.path.join(d7, ix)))
        row["composite"] = len(cd)
        rows.append(row)
    result[clip] = rows
    print("== %s" % clip)
    for r in rows:
        print("   F%02d composite=%4d body=%4d weaponBack=%s weaponFront=%s handFront=%s" % (
            r["frame"], r["composite"], r["body"] if r["body"] is not None else -1,
            r["weaponBack"], r["weaponFront"], r["handFront"]))

p = os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7", "frontal", "detect", "v5-vs-v7-layers.json")
with open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, indent=2)
    f.write("\n")
print("wrote", p)
