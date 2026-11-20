"""Numeric state of the front_l/Sword axilla opening per frame (V6 escalated, V6 plain, V5 baseline)."""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
V6 = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6")
DIRS = {
    "esc": os.path.join(V6, "frontal-escalated", "front_l-Sword-full"),
    "plain": os.path.join(V6, "frontal", "front_l-Sword-full"),
    "v5": os.path.join(ROOT, "characters", "orc-v1", "source", "combat-rescue-v5", "grip-specialist", "front_l-Sword-full"),
}
XW = (140, 168)
YW = (106, 140)


def load(p):
    with Image.open(p) as im:
        return im.convert("RGBA")


def gaps(px, w):
    """Interior transparent runs inside the window, per row (only runs bounded by opaque on both sides)."""
    out = []
    for y in range(YW[0], YW[1] + 1):
        runs = []
        x = XW[0]
        while x <= XW[1]:
            if px[y * w + x][3] < 128:
                s = x
                while x <= XW[1] and px[y * w + x][3] < 128:
                    x += 1
                e = x - 1
                left_opaque = s - 1 >= 0 and px[y * w + (s - 1)][3] >= 128
                right_opaque = e + 1 < w and px[y * w + (e + 1)][3] >= 128
                if left_opaque and right_opaque:
                    runs.append((s, e, e - s + 1))
            else:
                x += 1
        out.append((y, runs))
    return out


which = sys.argv[1:] or ["esc"]
for i in range(13):
    print("========== F%02d" % i)
    for k in which:
        p = os.path.join(DIRS[k], "layers", "body", "%02d.png" % i)
        if not os.path.exists(p):
            print("  %s MISSING" % k)
            continue
        im = load(p)
        px = list(im.getdata())
        w = im.size[0]
        rows = [(y, r) for y, r in gaps(px, w) if r]
        if not rows:
            print("  %-5s no interior gap in window" % k)
            continue
        total = sum(sum(g[2] for g in r) for _, r in rows)
        print("  %-5s gapRows=%d totalGapPx=%3d  %s" % (k, len(rows), total, " ".join("y%d:%s" % (y, "+".join("%d-%d(%d)" % g for g in r)) for y, r in rows)))
