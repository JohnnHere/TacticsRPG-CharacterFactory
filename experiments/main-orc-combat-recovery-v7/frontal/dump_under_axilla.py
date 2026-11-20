"""Edge-column diagnostic under the axilla: x146..150, y120..134 for every frame of front_l/Sword."""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
V6 = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6")
DIRS = {
    "esc": os.path.join(V6, "frontal-escalated", "front_l-Sword-full"),
    "plain": os.path.join(V6, "frontal", "front_l-Sword-full"),
}
X0, X1, Y0, Y1 = 144, 152, 118, 136


def load(p):
    with Image.open(p) as im:
        return im.convert("RGBA")


for k in ("esc", "plain"):
    print("==========", k)
    print("     " + " ".join("x%d  " % x for x in range(X0, X1)))
    for i in range(13):
        p = os.path.join(DIRS[k], "layers", "body", "%02d.png" % i)
        im = load(p)
        px = list(im.getdata())
        w = im.size[0]
        print("  F%02d" % i)
        for y in range(Y0, Y1):
            cells = []
            for x in range(X0, X1):
                r, g, b, a = px[y * w + x]
                cells.append("  ..  " if a == 0 else "%02x%02x%02x" % (r, g, b))
            print("   %3d %s" % (y, " ".join(cells)))
