# -*- coding: utf-8 -*-
"""Verificação TEXTUAL final do FIX B (somente leitura).
 1) Diff glm-fixes/native/02.png vs repair1 02.png confinado à máscara x68..100/y8..33.
 2) Outros 11 frames byte-idênticos (SHA-256) aos de repair1 (nativo e composto).
 3) Ausência de trave horizontal marrom >=8px em y12..23 dentro de x64..99.
 4) Conectividade ombro->zona punho na janela x62..103/y4..37.
 5) Cluster de punho (marrons) em y6..20.
 6) Ground nativo 126 / composto 190 em todos; composto = nativo deslocado (64,64).
"""
import hashlib
import json
import os
from PIL import Image

ROOT = os.getcwd()
SRC = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-rescue-v5", "body-specialist", "final-cycles", "repair1", "back_l-Axe-full")
NEW = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-rescue-v5", "body-specialist", "glm-fixes", "back_l-Axe-full")
OUT = os.path.join(ROOT, "experiments", "main-orc-combat-rescue-v5", "body-specialist", "glm-fixes")
report = {}

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def brown(r, g, b):
    return 0x1a <= r <= 0x90 and r > g and g > b and (r - b) >= 8 and (g - b) >= 3

old = Image.open(os.path.join(SRC, "native", "02.png")).convert("RGBA")
new = Image.open(os.path.join(NEW, "native", "02.png")).convert("RGBA")

allowed = set((x, y) for y in range(8, 34) for x in range(68, 101))
diff = [(x, y) for y in range(128) for x in range(128) if old.getpixel((x, y)) != new.getpixel((x, y))]
outside = [c for c in diff if c not in allowed]
report["changedPixels"] = len(diff)
report["changesOutsideMask"] = outside
print("diff:", len(diff), "| fora da máscara:", outside)

runs = []
for y in range(12, 24):
    run = 0
    for x in range(64, 100):
        r, g, b, a = new.getpixel((x, y))
        if a and brown(r, g, b):
            run += 1
        else:
            if run >= 8:
                runs.append((y, x - run, run))
            run = 0
    if run >= 8:
        runs.append((y, 100 - run, run))
report["beamRuns"] = runs
print("runs de trave:", runs)

opaque = {(x, y) for y in range(4, 38) for x in range(62, 104) if new.getpixel((x, y))[3] != 0}
seen, best = set(), set()
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
    if len(comp) > len(best):
        best = comp
ys = [c[1] for c in best]; xs = [c[0] for c in best]
report["mainComponent"] = {"px": len(best), "x": [min(xs), max(xs)], "y": [min(ys), max(ys)]}
report["armConnected"] = bool(any(y >= 20 for _, y in best) and any(y <= 16 for _, y in best))
print("componente principal:", report["mainComponent"], "| conectado:", report["armConnected"])

fist = [(x, y) for y in range(6, 21) for x in range(62, 102)
        if new.getpixel((x, y))[3] and brown(*new.getpixel((x, y))[:3])]
report["fistBrownPx"] = len(fist)
print("px marrons zona punho:", len(fist))

byte_ok = []
hashes = {}
for sub in ("native", "body256"):
    for i in range(12):
        if i == 2:
            continue
        fn = "%02d.png" % i
        a, b = sha(os.path.join(SRC, sub, fn)), sha(os.path.join(NEW, sub, fn))
        byte_ok.append(a == b)
        if sub == "native":
            hashes[fn] = b
report["otherFramesByteIdentical"] = all(byte_ok)
report["native02Sha256"] = sha(os.path.join(NEW, "native", "02.png"))
print("demais frames byte-idênticos:", all(byte_ok))

grounds, cgrounds, comp_ok = [], [], True
for i in range(12):
    im = Image.open(os.path.join(NEW, "native", "%02d.png" % i)).convert("RGBA")
    cm = Image.open(os.path.join(NEW, "body256", "%02d.png" % i)).convert("RGBA")
    grounds.append(max(y for y in range(128) if any(im.getpixel((x, y))[3] for x in range(128))))
    cgrounds.append(max(y for y in range(256) if any(cm.getpixel((x, y))[3] for x in range(256))))
    if any(im.getpixel((x, y)) != cm.getpixel((x + 64, y + 64)) for y in range(128) for x in range(128)):
        comp_ok = False
report["nativeGrounds"] = grounds
report["compositeGrounds"] = cgrounds
report["compositeMatchesNative"] = comp_ok
print("grounds:", set(grounds), set(cgrounds), "| composto exato:", comp_ok)

report["verdict"] = "PASS" if (not outside and not runs and report["armConnected"]
                               and report["fistBrownPx"] >= 10 and all(byte_ok)
                               and all(g == 126 for g in grounds) and all(g == 190 for g in cgrounds)
                               and comp_ok) else "FAIL"
with open(os.path.join(OUT, "verify-fix-b.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)
print("VERDICT FIX B:", report["verdict"])
