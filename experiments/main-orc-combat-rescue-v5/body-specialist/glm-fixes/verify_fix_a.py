# -*- coding: utf-8 -*-
"""Verificação TEXTUAL do FIX A (somente leitura; não edita produção).
Confere:
 1) Diff glm-fixes/back_r-Sword-full/native/06.png vs repair1 06.png confinado a
    {(112,64),(110,69),(109,70),(108,71),(107,72)} + região y88..94/x45..55.
 2) Os 5 flutuantes agora alpha 0.
 3) Ausência de família vinho na região QA.
 4) Outros 11 frames byte-idênticos (SHA-256) aos de repair1.
 5) Ground: última linha opaca y=126 em todos os frames novos.
 6) Composto 256: ground y=190 e pixel-for-pixel = nativo deslocado (64,64).
"""
import hashlib
import json
import os
from PIL import Image

ROOT = os.getcwd()
SRC = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-rescue-v5", "body-specialist", "final-cycles", "repair1", "back_r-Sword-full")
NEW = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-rescue-v5", "body-specialist", "glm-fixes", "back_r-Sword-full")
OUT = os.path.join(ROOT, "experiments", "main-orc-combat-rescue-v5", "body-specialist", "glm-fixes")
report = {}

REDS = {"592d2b", "482025", "34181e", "30171c", "27181d", "271218", "211117", "1e0e14", "240e17"}
FLOATS = [(112, 64), (110, 69), (109, 70), (108, 71), (107, 72)]

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def px(im, x, y):
    r, g, b, a = im.getpixel((x, y))
    return ("%02x%02x%02x" % (r, g, b), a)

old = Image.open(os.path.join(SRC, "native", "06.png")).convert("RGBA")
new = Image.open(os.path.join(NEW, "native", "06.png")).convert("RGBA")

# 1) diff confinado
region = set((x, y) for y in range(88, 95) for x in range(45, 56))
allowed = region | set(FLOATS)
diff = []
for y in range(128):
    for x in range(128):
        if old.getpixel((x, y)) != new.getpixel((x, y)):
            diff.append((x, y))
outside = [c for c in diff if c not in allowed]
report["changedPixels"] = len(diff)
report["changesOutsideAllowed"] = outside
print("diff total:", len(diff), "| fora do permitido:", outside)

# 2) floats alpha 0
report["floats"] = {str(c): new.getpixel(c)[3] for c in FLOATS}
print("floats alpha:", report["floats"])

# 3) sem vinho na região
red_left = [(x, y) for (x, y) in region if px(new, x, y)[0] in REDS and px(new, x, y)[1] != 0]
report["redsRemainingInRegion"] = red_left
print("vinho restante na região:", red_left)

# 4) 11 frames byte-idênticos
byte_ok, hashes = [], {}
for i in range(12):
    if i == 6:
        continue
    fn = "%02d.png" % i
    a, b = sha(os.path.join(SRC, "native", fn)), sha(os.path.join(NEW, "native", fn))
    byte_ok.append(a == b)
    hashes[fn] = b
report["otherFramesByteIdentical"] = all(byte_ok)
print("11 frames byte-idênticos:", all(byte_ok))
report["native06Sha256"] = sha(os.path.join(NEW, "native", "06.png"))

# 5) ground y126 (última linha opaca) em todos
grounds = []
for i in range(12):
    im = Image.open(os.path.join(NEW, "native", "%02d.png" % i)).convert("RGBA")
    last = max(y for y in range(128) if any(im.getpixel((x, y))[3] != 0 for x in range(128)))
    grounds.append(last)
report["nativeGrounds"] = grounds
print("grounds nativos:", grounds)

# 6) composto = nativo em (64,64); ground composto 190
comp_ok, comp_grounds = True, []
for i in range(12):
    im = Image.open(os.path.join(NEW, "native", "%02d.png" % i)).convert("RGBA")
    cm = Image.open(os.path.join(NEW, "body256", "%02d.png" % i)).convert("RGBA")
    last = max(y for y in range(256) if any(cm.getpixel((x, y))[3] != 0 for x in range(256)))
    comp_grounds.append(last)
    for y in range(128):
        for x in range(128):
            if im.getpixel((x, y)) != cm.getpixel((x + 64, y + 64)):
                comp_ok = False
report["compositeMatchesNative"] = comp_ok
report["compositeGrounds"] = comp_grounds
print("composto ok:", comp_ok, "| grounds composto:", comp_grounds)

report["verdict"] = "PASS" if (not outside and not red_left and all(byte_ok) and comp_ok
                               and all(g == 126 for g in grounds) and all(g == 190 for g in comp_grounds)
                               and all(v == 0 for v in report["floats"].values())) else "FAIL"
with open(os.path.join(OUT, "verify-fix-a.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)
print("VERDICT FIX A:", report["verdict"])
