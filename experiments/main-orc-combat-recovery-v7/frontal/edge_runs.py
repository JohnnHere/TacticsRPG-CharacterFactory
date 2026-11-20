"""Exact opaque runs + hole runs across the axilla for F02..F05, escalated vs plain, x138..x170."""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
V6 = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6")
DIRS = {
    "esc": os.path.join(V6, "frontal-escalated", "front_l-Sword-full"),
    "plain": os.path.join(V6, "frontal", "front_l-Sword-full"),
}
X0, X1 = 138, 171
Y0, Y1 = 110, 130


def load(p):
    with Image.open(p) as im:
        return im.convert("RGBA")


def runs(seq):
    out, start = [], None
    for i, v in enumerate(seq):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(seq) - 1))
    return out


for k in ("plain", "esc"):
    print("### " + k)
    for i in (2, 3, 4, 5):
        im = load(os.path.join(DIRS[k], "layers", "body", "%02d.png" % i))
        px = list(im.getdata())
        w = im.size[0]
        print("  F%02d" % i)
        for y in range(Y0, Y1):
            op = [px[y * w + x][3] >= 128 for x in range(X0, X1)]
            rr = runs(op)
            parts = []
            for a, b in rr:
                ax, bx = X0 + a, X0 + b
                ca = px[y * w + ax][:3]
                cb = px[y * w + bx][:3]
                parts.append("[%d-%d] L=%d,%d,%d R=%d,%d,%d" % (ax, bx, ca[0], ca[1], ca[2], cb[0], cb[1], cb[2]))
            holes = [(X0 + a, X0 + b, b - a + 1) for a, b in runs([not v for v in op])]
            print("    y=%3d holes=%s runs=%s" % (y, holes, " ".join(parts)))
