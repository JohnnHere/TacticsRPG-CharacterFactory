# -*- coding: utf-8 -*-
"""Dados dos ciclos glm-fixes (hashes aceitos pelo QA; contabilidade PixelLab real)."""
import hashlib

CH = "characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes"
EX = "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes"
SRC = "characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/repair1"

PL_AXE = {"jobs": [{"tool": "inpaint_image_pro_flash",
    "jobId": "540302e4-2690-4282-8de5-c609f15b1142", "segment": "F02-right-arm-reauthor",
    "cost": 6.0, "seed": 20261029, "mask": {"x": 68, "y": 8, "w": 33, "h": 26}}],
    "repairGenerationsCharged": 6.0,
    "note": "Inpaint condicionado apenas ao F02; composto no Aseprite via Lua (delta 510 px na mascara)"}
PL_ZERO = {"jobs": [], "repairGenerationsCharged": 0.0,
    "note": "Reparo cirurgico 100% local no Aseprite via Lua (doadores F05/F07); 0 chamadas PixelLab"}

CYCLES = {
 "back_r-Sword-full": dict(
  id="basic.sword-slash.body-specialist.glm-fixes",
  revision="body-specialist-glm-fixes-back-r-sword-v1",
  category="Sword", direction="back_r", total=730, repairedFrame=6,
  repairedDefect="REAR-01-RESIDUAL-A + REAR-01-RESIDUAL-B",
  repStatus="BODY_BACK_R_SWORD_GLM_FIXES_READY",
  scope="GLM body-fixes: F06 flutuantes zerados + malha reconstruida com doadores F05/F07 (prescrito pelo QA); demais frames byte-herdados de repair1",
  durations=[40, 60, 60, 70, 70, 40, 40, 90, 70, 70, 60, 60],
  keys={3: ("01-hoist", "a573c039202f52315eb681da5fe375199b34fa101a1f9404b8c9263920589ff2"),
        4: ("02-apex", "9607fb5c7f36b1dcd7649eba505d5eca925f2abb670d636f8a235c42c6cbb40d"),
        7: ("03-impact", "ac51e08bdd1cc40de255f5233d08f79916c8112b2b9c68b00eee8c509f204107")},
  pixellab=PL_ZERO),
 "back_l-Axe-full": dict(
  id="basic.axe-chop.body-specialist.glm-fixes",
  revision="body-specialist-glm-fixes-back-l-axe-v1",
  category="Axe", direction="back_l", total=1100, repairedFrame=2,
  repairedDefect="REAR-02-PERSISTENT",
  repStatus="BODY_BACK_L_AXE_GLM_FIXES_READY",
  scope="GLM body-fixes: F02 braco direito reautoral via inpaint PixelLab condicionado (mascara x68..100/y8..33) composto no Aseprite; demais frames byte-herdados de repair1",
  durations=[70, 80, 90, 100, 110, 50, 60, 110, 100, 100, 100, 130],
  keys={3: ("01-hoist", "d240b9ac537499625f7a86fcbfcf8cf2287b26947dc164092a76f313196c79ce"),
        4: ("02-apex", "7adfd9f45be25ce862d261f4bf6e47881e52043969605acf9cd4f918c9e00d56"),
        7: ("03-impact", "7a0c943c51f555f683ba78913150190e9b375a0091714644125b6fef7ea8c1a0")},
  pixellab=PL_AXE),
}

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

# Hashes esperados das chaves carregados do clip.json de repair1 (fonte da verdade
# auditada pelo QA) — elimina erro de digitação de hash manual.
import json as _json
import os as _os
for _name, _c in CYCLES.items():
    with open(_os.path.join(SRC, _name, "clip.json"), encoding="utf-8") as _f:
        _clip = _json.load(_f)
    _byidx = {f["index"]: f for f in _clip["frames"]}
    _c["keys"] = {i: (kn, _byidx[i]["nativePng"]["sha256"]) for i, (kn, _) in _c["keys"].items()}

