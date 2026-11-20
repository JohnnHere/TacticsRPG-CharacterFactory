# -*- coding: utf-8 -*-
"""Comparações antes/depois (layout Pillow; leitura + arquivo novo em glm-fixes)."""
import os
from PIL import Image, ImageDraw

ROOT = os.getcwd()
CH = "characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes"
EX = "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes"
SRC = "characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/repair1"

def zoom(img, box, z):
    c = img.crop(box)
    return c.resize((c.width * z, c.height * z), Image.NEAREST)

def diff_overlay(a, b):
    d = Image.new("RGBA", a.size, (10, 10, 14, 255))
    pa, pb, pd = a.load(), b.load(), d.load()
    for y in range(a.height):
        for x in range(a.width):
            if pa[x, y] != pb[x, y]:
                pd[x, y] = (255, 40, 40, 255)
            elif pa[x, y][3] != 0:
                r, g, bb, _ = pa[x, y]
                pd[x, y] = (r // 3, g // 3, bb // 3, 255)
    return d

def label(img, txt):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width, 10], fill=(0, 0, 0, 255))
    d.text((3, 1), txt, fill=(255, 255, 255, 255))
    return img

def make_compare(cycle, frame, out_name, box, z, note):
    before = Image.open(os.path.join(SRC, cycle, "native", "%02d.png" % frame)).convert("RGBA")
    after = Image.open(os.path.join(CH, cycle, "native", "%02d.png" % frame)).convert("RGBA")
    zb, za = zoom(before, box, z), zoom(after, box, z)
    gap = 8
    W = max(before.width * 3 + gap * 2, zb.width * 2 + gap) + 4
    H = before.height + zb.height + 46
    cv = Image.new("RGBA", (W, H), (16, 16, 20, 255))
    cv.paste(label(before.copy(), "ANTES (repair1)"), (2, 14))
    cv.paste(label(after.copy(), "DEPOIS (glm-fixes)"), (before.width + gap + 2, 14))
    cv.paste(label(diff_overlay(before, after), "DIFF (vermelho=mudou)"), (before.width * 2 + gap * 2 + 2, 14))
    cv.paste(label(zb, "ZOOM ANTES"), (2, before.height + 26))
    cv.paste(label(za, "ZOOM DEPOIS"), (zb.width + gap + 2, before.height + 26))
    ImageDraw.Draw(cv).text((4, 2), "%s F%02d — %s" % (cycle, frame, note), fill=(230, 230, 230, 255))
    for root in (EX, CH):
        cv.save(os.path.join(root, out_name))
    print("saved", out_name, cv.size)

make_compare("back_r-Sword-full", 6, "glm-back_r-Sword-f06-before-after.png",
             (36, 76, 68, 106), 4, "malha y88..94/x45..55 + flutuantes (112,64)..(107,72)")
make_compare("back_l-Axe-full", 2, "glm-back_l-Axe-f02-before-after.png",
             (62, 4, 104, 38), 6, "mascara inpaint x68..100/y8..33 (braco/punho/trave)")
print("PREVIEWS OK")
