"""Silhouette-only ASCII (opaque '#') plus interior transparent gaps ('o'), front_l/Sword body."""
import os
import sys
from collections import deque

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6", "frontal-escalated", "front_l-Sword-full")
X0, X1, Y0, Y1 = 80, 182, 88, 178


def load(p):
    with Image.open(p) as im:
        return im.convert("RGBA")


def interior_holes(alpha, w, h):
    """Transparent pixels not reachable from the border (4-connected)."""
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
    return [alpha[i] < 128 and not bg[i] for i in range(w * h)]


for i in [int(a) for a in sys.argv[1:]] or [0]:
    im = load(os.path.join(BASE, "layers", "body", "%02d.png" % i))
    px = list(im.getdata())
    w, h = im.size
    alpha = [p[3] for p in px]
    holes = interior_holes(alpha, w, h)
    print("    body F%02d  (x %d..%d, y %d..%d)  '#'=opaque  'o'=interior transparent  '.'=exterior" % (i, X0, X1 - 1, Y0, Y1 - 1))
    print("     " + "".join(str((x // 10) % 10) for x in range(X0, X1)))
    print("     " + "".join(str(x % 10) for x in range(X0, X1)))
    for y in range(Y0, Y1):
        row = []
        for x in range(X0, X1):
            k = y * w + x
            if alpha[k] >= 128:
                row.append("#")
            elif holes[k]:
                row.append("o")
            else:
                row.append(".")
        print("  %3d %s" % (y, "".join(row)))
