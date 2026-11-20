"""Census of one exact light colour in the body layer: how many pixels, in what cluster sizes,
and at which coordinates. Used to prove whether rgb(147,148,149) is a stray family or part of a
larger light plate."""
import os
import sys
from collections import Counter, deque

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-recovery-v7", "frontal")
TARGET = tuple(int(v) for v in (sys.argv[1] if len(sys.argv) > 1 else "147,148,149").split(","))
CLIP = sys.argv[2] if len(sys.argv) > 2 else "front_l-Sword-full"


def load(p):
    with Image.open(p) as im:
        return im.convert("RGBA")


def clusters(mask, w, h):
    seen = [False] * (w * h)
    out = []
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
        out.append(comp)
    return out


d = os.path.join(BASE, CLIP)
import json
with open(os.path.join(d, "clip.json"), encoding="utf-8") as f:
    meta = json.load(f)
print("clip", CLIP, "target", TARGET)
for i in range(meta["frameCount"]):
    ix = "%02d.png" % i
    for name in ("body", "weaponFront", "weaponBack", "handFront"):
        px = list(load(os.path.join(d, "layers", name, ix)).getdata())
        w = 256
        mask = [p[3] >= 128 and p[:3] == TARGET for p in px]
        tot = sum(mask)
        if not tot:
            continue
        cs = sorted((len(c) for c in clusters(mask, w, 256)), reverse=True)
        coords = [(k % w, k // w) for k in range(w * 256) if mask[k]]
        print("  F%02d %-11s n=%4d clusters=%s coords(<=6)=%s" % (i, name, tot, cs[:8], coords[:6]))
