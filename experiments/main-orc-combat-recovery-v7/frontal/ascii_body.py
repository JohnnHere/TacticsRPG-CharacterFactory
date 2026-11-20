"""ASCII silhouette dump for front_l/Sword body frames (locating the axilla numerically)."""
import json
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6", "frontal-escalated", "front_l-Sword-full")


def lum(r, g, b):
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def load(p):
    with Image.open(p) as im:
        return im.convert("RGBA")


X0, X1 = 78, 186
Y0, Y1 = 78, 196


def dump(px, w, title):
    print("   ", title)
    print("    " + "".join(str((x // 10) % 10) for x in range(X0, X1)))
    print("    " + "".join(str(x % 10) for x in range(X0, X1)))
    for y in range(Y0, Y1):
        row = []
        for x in range(X0, X1):
            r, g, b, a = px[y * w + x]
            if a < 128:
                row.append(".")
            else:
                L = lum(r, g, b)
                row.append("#" if L >= 150 else ("+" if L >= 100 else ("-" if L >= 55 else " ")))
        print("  %3d %s" % (y, "".join(row)))


idxs = [int(a) for a in sys.argv[1:]] or [0, 3, 4]
for i in idxs:
    im = load(os.path.join(BASE, "layers", "body", "%02d.png" % i))
    dump(list(im.getdata()), im.size[0], "body F%02d" % i)
