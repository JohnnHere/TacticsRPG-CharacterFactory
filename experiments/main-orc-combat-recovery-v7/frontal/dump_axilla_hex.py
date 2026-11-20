"""Exact RGBA dump of the front_l/Sword axilla zone (compact hex, '......' = transparent)."""
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
X0, X1, Y0, Y1 = 143, 164, 110, 130


def load(p):
    with Image.open(p) as im:
        return im.convert("RGBA")


for i in [int(a) for a in sys.argv[1:]] or [3]:
    print("========== F%02d" % i)
    for k in ("esc", "plain", "v5"):
        p = os.path.join(DIRS[k], "layers", "body", "%02d.png" % i)
        if not os.path.exists(p):
            print("  %s MISSING" % k)
            continue
        im = load(p)
        px = list(im.getdata())
        w = im.size[0]
        print("  --", k)
        print("      " + " ".join("%02d" % x for x in range(X0, X1)))
        for y in range(Y0, Y1):
            cells = []
            for x in range(X0, X1):
                r, g, b, a = px[y * w + x]
                cells.append("......" if a == 0 else "%02x%02x%02x" % (r, g, b))
            print("  %3d %s" % (y, " ".join(cells)))
