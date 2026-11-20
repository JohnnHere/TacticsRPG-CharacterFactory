# -*- coding: utf-8 -*-
"""GLM body-fixes — análise TEXTUAL de pixels (somente leitura; nunca escreve produção).
Lê PNGs nativos 128x128 dos ciclos repair1 e emite grades hex textuais para:
  FIX A: back_r-Sword-full 05/06/07 (resíduos flutuantes + região da malha y88..94/x45..55)
  FIX B: back_l-Axe-full 01/02/03 (trave de madeira + pino + bloco; braço direito)
Saída: experiments/.../glm-fixes/analysis/frames-analysis.txt (resumo curto no stdout).
"""
import os
from PIL import Image

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
SRC = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-rescue-v5", "body-specialist", "final-cycles", "repair1")
OUT = os.path.join(ROOT, "experiments", "main-orc-combat-rescue-v5", "body-specialist", "glm-fixes", "analysis")
os.makedirs(OUT, exist_ok=True)

def load(cycle, n):
    return Image.open(os.path.join(SRC, cycle, "native", "%02d.png" % n)).convert("RGBA")

def hx(im, x, y):
    r, g, b, a = im.getpixel((x, y))
    if a == 0:
        return ".."
    return "%02x%02x%02x" % (r, g, b)

lines = []
def w(s=""):
    lines.append(s)

def grid(im, x0, x1, y0, y1, title):
    w("== %s (x%d..%d, y%d..%d) ==" % (title, x0, x1, y0, y1))
    w("     " + "".join("%5d" % x for x in range(x0, x1 + 1)))
    for y in range(y0, y1 + 1):
        w("%3d: %s" % (y, " ".join("%s" % hx(im, x, y) for x in range(x0, x1 + 1))))
    w()

def bbox(im, tag):
    px = im.load()
    xs, ys = [], []
    for y in range(128):
        for x in range(128):
            if px[x, y][3] != 0:
                xs.append(x); ys.append(y)
    w("bbox %s: x %d..%d, y %d..%d (n=%d)" % (tag, min(xs), max(xs), min(ys), max(ys), len(xs)))

# ---------------- FIX A ----------------
w("########## FIX A: back_r-Sword-full (native 128) ##########")
A = {n: load("back_r-Sword-full", n) for n in (5, 6, 7)}
floats = [(112, 64), (110, 69), (109, 70), (108, 71), (107, 72)]
w("-- pixels flutuantes QA (F06=06.png) e mesmas coords em F05/F07 --")
for (x, y) in floats:
    row = ["(%d,%d)" % (x, y)]
    for n in (5, 6, 7):
        r, g, b, a = A[n].getpixel((x, y))
        row.append("F%02d=%02x%02x%02x/%d" % (n, r, g, b, a))
    w(" ".join(row))
w()
for n in (5, 6, 7):
    bbox(A[n], "back_r-Sword F%02d" % n)
w()
for n in (5, 6, 7):
    grid(A[n], 40, 62, 82, 100, "back_r-Sword F%02d região saiote/malha" % n)
w("-- diffs F06 vs F05 e F06 vs F07 na região y88..94 x45..55 --")
for y in range(88, 95):
    for x in range(45, 56):
        c6 = hx(A[6], x, y); c5 = hx(A[5], x, y); c7 = hx(A[7], x, y)
        if c6 != c5 or c6 != c7:
            w("(%d,%d) F05=%s F06=%s F07=%s" % (x, y, c5, c6, c7))
w()

# ---------------- FIX B ----------------
w("########## FIX B: back_l-Axe-full (native 128) ##########")
B = {n: load("back_l-Axe-full", n) for n in (1, 2, 3)}
for n in (1, 2, 3):
    bbox(B[n], "back_l-Axe F%02d" % n)
w()
w("-- alvos QA F02: pino x70 y14..18; bloco x83..92 y15..20 --")
for y in range(12, 22):
    row = ["y%-3d" % y]
    for x in (70, 83, 86, 89, 92):
        r, g, b, a = B[2].getpixel((x, y))
        row.append("x%d=%02x%02x%02x/%d" % (x, r, g, b, a))
    w(" ".join(row))
w()
for n in (1, 2, 3):
    grid(B[n], 58, 98, 6, 46, "back_l-Axe F%02d braço direito/ombro/pescoço" % n)
w("-- varredura madeira em F02 (x58..100, y5..30): marrons r>70 r>g>b g<0.78r b<0.62r --")
im = B[2]; px = im.load()
wood = []
for y in range(5, 31):
    for x in range(58, 101):
        r, g, b, a = px[x, y]
        if a and r > 70 and r > g and g > b and g < 0.78 * r and b < 0.62 * r:
            wood.append((x, y, "%02x%02x%02x" % (r, g, b)))
w("contagem=%d" % len(wood))
w(" ".join("(%d,%d,%s)" % t for t in wood))
w()

path = os.path.join(OUT, "frames-analysis.txt")
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("OK written:", path, "lines:", len(lines))
