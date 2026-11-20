"""Locate the V6 escalated axilla repair (diff against the non-escalated V6 body) and the V5 baseline."""
import json
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
V6 = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6")
V5 = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-rescue-v5")
ESC = os.path.join(V6, "frontal-escalated", "front_l-Sword-full")
PLAIN = os.path.join(V6, "frontal", "front_l-Sword-full")


def load(p):
    with Image.open(p) as im:
        return im.convert("RGBA")


def diff(a, b):
    pa, pb = list(a.getdata()), list(b.getdata())
    w = a.size[0]
    out = []
    for i, (ca, cb) in enumerate(zip(pa, pb)):
        if ca != cb:
            out.append((i % w, i // w, ca, cb))
    return out


for i in range(13):
    a = load(os.path.join(ESC, "layers", "body", "%02d.png" % i))
    b = load(os.path.join(PLAIN, "layers", "body", "%02d.png" % i))
    d = diff(a, b)
    if d:
        xs = [t[0] for t in d]
        ys = [t[1] for t in d]
        print("F%02d escalated-vs-plain body: %d px  bbox=(%d,%d)-(%d,%d)" % (i, len(d), min(xs), min(ys), max(xs), max(ys)))
        for x, y, ca, cb in d[:200]:
            print("    (%3d,%3d) plain=%s -> escalated=%s" % (x, y, cb, ca))
    else:
        print("F%02d escalated-vs-plain body: identical" % i)
