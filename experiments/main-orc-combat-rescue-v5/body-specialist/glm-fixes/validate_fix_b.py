# -*- coding: utf-8 -*-
"""Validação TEXTUAL do edit1 PixelLab vs F02 original (somente leitura).
Testes:
 1) Diff completo: contagem, bbox, e diff FORA da máscara (x68..100 / y8..33).
 2) Trave horizontal: runs horizontais >=8 px da família marrom nas linhas y15..21
    dentro de x66..96 (a trave original cobria x73..90 em y19..20).
 3) Pino x70..72 y16..18 e bloco x82..92 y15..20: pixels mudaram vs original?
 4) Conectividade do braço: componente opaco dentro de x64..102/y6..36 deve conectar
    a zona do ombro (linha y>=20) à zona do punho (linha y<=16) — cadeia contínua.
 5) Punho: cluster marrom (luva) em y6..20/x62..100 com >=10 px.
 6) Fundo: cantos transparentes; linhas y40..127 idênticas ao original.
 7) Paleta: cores novas na máscara inexistentes no original inteiro (lista).
"""
import json
import os
from PIL import Image

ROOT = os.getcwd()
G = os.path.join(ROOT, "experiments", "main-orc-combat-rescue-v5", "body-specialist", "glm-fixes")
ORIG = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-rescue-v5", "body-specialist", "final-cycles", "repair1", "back_l-Axe-full", "native", "02.png")
EDIT = os.path.join(G, "pixellab-f02-edit1.png")

o = Image.open(ORIG).convert("RGBA")
e = Image.open(EDIT).convert("RGBA")
rep = {}

def brown(r, g, b):
    return 0x1a <= r <= 0x90 and r > g and g > b and (r - b) >= 8 and (g - b) >= 3

# 1) diff
diff, outside = [], []
for y in range(128):
    for x in range(128):
        if o.getpixel((x, y)) != e.getpixel((x, y)):
            diff.append((x, y))
            if not (68 <= x <= 100 and 8 <= y <= 33):
                outside.append((x, y))
rep["changed"] = len(diff)
rep["changedOutsideMask"] = len(outside)
rep["outsideSample"] = outside[:40]
if diff:
    xs = [c[0] for c in diff]; ys = [c[1] for c in diff]
    rep["diffBBox"] = [min(xs), max(xs), min(ys), max(ys)]
print("diff:", rep["changed"], "| fora da mascara:", rep["changedOutsideMask"], "| bbox:", rep.get("diffBBox"))
print("fora (amostra):", rep["outsideSample"])

# 2) runs marrons horizontais (trave)
runs = []
for y in range(12, 24):
    run = 0
    for x in range(64, 100):
        r, g, b, a = e.getpixel((x, y))
        if a and brown(r, g, b):
            run += 1
        else:
            if run >= 8:
                runs.append((y, x - run, run))
            run = 0
    if run >= 8:
        runs.append((y, 100 - run, run))
rep["beamRuns"] = runs
print("runs de trave (>=8px marrom contínuo):", runs)

# 3) pino e bloco
peg_same = sum(1 for y in range(14, 19) for x in range(70, 73) if o.getpixel((x, y)) == e.getpixel((x, y)))
blk_same = sum(1 for y in range(15, 21) for x in range(83, 93) if o.getpixel((x, y)) == e.getpixel((x, y)))
rep["pegUnchangedPx"] = peg_same
rep["blockUnchangedPx"] = blk_same
print("pino inalterado px (de 15):", peg_same, "| bloco inalterado px (de 60):", blk_same)

# 4) conectividade ombro->punho dentro da janela
W = range(62, 104)
H = range(4, 38)
opaque = {(x, y) for y in H for x in W if e.getpixel((x, y))[3] != 0}
seen = set()
comps = []
for p in opaque:
    if p in seen:
        continue
    stack, comp = [p], set()
    seen.add(p)
    while stack:
        cx, cy = stack.pop()
        comp.add((cx, cy))
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                q = (cx + dx, cy + dy)
                if q in opaque and q not in seen:
                    seen.add(q)
                    stack.append(q)
    comps.append(comp)
comps.sort(key=len, reverse=True)
main = comps[0] if comps else set()
ys_main = [c[1] for c in main]; xs_main = [c[0] for c in main]
rep["mainComponent"] = {"px": len(main), "xRange": [min(xs_main), max(xs_main)], "yRange": [min(ys_main), max(ys_main)]}
touches_shoulder = any(y >= 20 for _, y in main)
touches_fistzone = any(y <= 16 for _, y in main)
rep["armConnectedShoulderToFistZone"] = bool(touches_shoulder and touches_fistzone)
print("componente principal:", rep["mainComponent"], "| ombro<->zonaPunho conectados:", rep["armConnectedShoulderToFistZone"])

# 5) cluster marrom (punho/luva) na zona alta
fist = [(x, y) for y in range(6, 21) for x in range(62, 102)
        if e.getpixel((x, y))[3] and brown(*e.getpixel((x, y))[:3])]
rep["fistBrownPx"] = len(fist)
if fist:
    fx = [c[0] for c in fist]; fy = [c[1] for c in fist]
    rep["fistBBox"] = [min(fx), max(fx), min(fy), max(fy)]
print("px marrons zona punho (y6..20):", rep["fistBrownPx"], "| bbox:", rep.get("fistBBox"))

# 6) fundo/base
corners = [e.getpixel(c)[3] for c in ((0, 0), (127, 0), (0, 127), (127, 127))]
bottom_same = all(o.getpixel((x, y)) == e.getpixel((x, y)) for y in range(40, 128) for x in range(128))
rep["cornersAlpha"] = corners
rep["belowY40Identical"] = bottom_same
print("cantos alpha:", corners, "| y>=40 idêntico:", bottom_same)

# 7) cores novas na máscara
orig_colors = {o.getpixel((x, y)) for y in range(128) for x in range(128)}
new_colors = {e.getpixel((x, y)) for y in range(8, 34) for x in range(68, 101)} - orig_colors
rep["newColorsInMask"] = ["#%02x%02x%02x/%d" % c for c in sorted(new_colors)]
print("cores novas na máscara:", rep["newColorsInMask"])

ok = (rep["changed"] > 0 and not runs and peg_same < 15 and blk_same < 60
      and rep["armConnectedShoulderToFistZone"] and rep["fistBrownPx"] >= 10
      and all(a == 0 for a in corners) and bottom_same)
rep["verdict"] = "ACCEPT_FOR_COMPOSITE" if ok else "NEEDS_REVIEW"
with open(os.path.join(G, "validate-fix-b.json"), "w", encoding="utf-8") as f:
    json.dump(rep, f, indent=2)
print("VERDICT FIX B edit1:", rep["verdict"])
