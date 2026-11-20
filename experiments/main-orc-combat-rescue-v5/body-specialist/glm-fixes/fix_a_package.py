# -*- coding: utf-8 -*-
"""Empacotamento FIX A: garante paridade BYTE dos frames intocados.
Copia de repair1 -> glm-fixes (ambas as raízes) os 11 frames nativos + 11 compostos
intocados (file-copy = byte-idêntico, preservando as chaves F03/F04/F07 com hashes
aceitos pelo QA). O frame reparado 06 (nativo+composto, já corrigido pelo Aseprite)
é copiado da raiz characters para a raiz experiments (espelho).
Mestres .aseprite e tiras já foram salvos pelo fix-a-back-r-sword-f06.lua.
"""
import shutil
from pathlib import Path

ROOT = Path.cwd()
SRC = ROOT / "characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/repair1/back_r-Sword-full"
CH = ROOT / "characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/back_r-Sword-full"
EX = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes/back_r-Sword-full"

for sub in ("native", "body256"):
    (CH / sub).mkdir(parents=True, exist_ok=True)
    (EX / sub).mkdir(parents=True, exist_ok=True)
    for i in range(12):
        fn = "%02d.png" % i
        if sub == "native" and i == 6:
            continue  # frame reparado: já correto em CH (Aseprite)
        src_file = SRC / sub / fn
        shutil.copyfile(src_file, CH / sub / fn)
        shutil.copyfile(src_file, EX / sub / fn)
        print("copied untouched", sub, fn)

# frame reparado 06: espelha CH -> EX (byte do Aseprite)
for sub in ("native", "body256"):
    shutil.copyfile(CH / sub / "06.png", EX / sub / "06.png")
    print("mirrored repaired", sub, "06.png")
print("FIX A packaging done.")
