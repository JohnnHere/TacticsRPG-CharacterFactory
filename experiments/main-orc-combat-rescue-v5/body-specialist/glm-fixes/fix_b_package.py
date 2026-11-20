# -*- coding: utf-8 -*-
"""Empacotamento FIX B: paridade BYTE dos frames intocados do ciclo Axe.
Copia de repair1 -> glm-fixes (ambas as raízes) os frames != 02 (nativo e composto).
O frame reparado 02 (nativo+composto, saído do Aseprite) é espelhado CH -> EX.
"""
import shutil
from pathlib import Path

ROOT = Path.cwd()
SRC = ROOT / "characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/repair1/back_l-Axe-full"
CH = ROOT / "characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/back_l-Axe-full"
EX = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes/back_l-Axe-full"

for sub in ("native", "body256"):
    (CH / sub).mkdir(parents=True, exist_ok=True)
    (EX / sub).mkdir(parents=True, exist_ok=True)
    for i in range(12):
        fn = "%02d.png" % i
        if i == 2:
            continue  # frame reparado: já correto em CH (Aseprite)
        shutil.copyfile(SRC / sub / fn, CH / sub / fn)
        shutil.copyfile(SRC / sub / fn, EX / sub / fn)
        print("copied untouched", sub, fn)

for sub in ("native", "body256"):
    shutil.copyfile(CH / sub / "02.png", EX / sub / "02.png")
    print("mirrored repaired", sub, "02.png")
print("FIX B packaging done.")
