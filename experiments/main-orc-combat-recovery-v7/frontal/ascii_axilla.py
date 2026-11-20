"""Axilla window analysis for front_l/Sword: V6 escalated vs V6 plain vs V5 baseline, all 13 frames."""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
V6 = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6")
ESC = os.path.join(V6, "frontal-escalated", "front_l-Sword-full")
PLAIN = os.path.join(V6, "frontal", "front_l-Sword-full")
V5 = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-rescue-v5", "grip-specialist", "front_l-Sword-full")

X0, X1, Y0, Y1 = 138, 164, 106, 134


def load(p):
    with Image.open(p) as im:
        return im.convert("RGBA")


def cls(r, g, b, a):
    if a < 128:
        return "."
    L = 0.2126 * r + 0.7152 * g + 0.0722 * b
    if L < 6:
        return " "
    if L < 14:
        return "K"  # ink
    if L < 22:
        return "1"
    if L < 32:
        return "2"
    if L < 48:
        return "3"
    if L < 70:
        return "4"
    if L < 100:
        return "5"
    if L < 130:
        return "6"
    if L < 150:
        return "7"
    return "8"


def show(path, title):
    if not os.path.exists(path):
        print("  MISSING", path)
        return
    im = load(path)
    px = list(im.getdata())
    w = im.size[0]
    print("   ", title)
    print("     " + "".join(str((x // 10) % 10) for x in range(X0, X1)))
    print("     " + "".join(str(x % 10) for x in range(X0, X1)))
    for y in range(Y0, Y1):
        row = "".join(cls(*px[y * w + x]) for x in range(X0, X1))
        print("  %3d %s" % (y, row))


frames = [int(a) for a in sys.argv[1:]] or [2, 3, 4, 5]
for i in frames:
    print("========== F%02d" % i)
    show(os.path.join(ESC, "layers", "body", "%02d.png" % i), "V6 escalated body")
    show(os.path.join(PLAIN, "layers", "body", "%02d.png" % i), "V6 plain body")
    show(os.path.join(V5, "layers", "body", "%02d.png" % i), "V5 baseline body")
