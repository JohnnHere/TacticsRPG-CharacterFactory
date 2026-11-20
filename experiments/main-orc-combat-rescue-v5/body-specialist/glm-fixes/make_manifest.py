# -*- coding: utf-8 -*-
"""Gera patch-manifest.json a partir de hashes-summary.json + contracts_data."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contracts_data import CH, EX, CYCLES, sha

with open(os.path.join(EX, "hashes-summary.json"), encoding="utf-8") as f:
    hs = json.load(f)

cells = []
for name, c in CYCLES.items():
    h = hs[name]
    cells.append({
        "direction": c["direction"], "action": c["category"] + " Attack",
        "category": c["category"], "state": "Attack", "cycleName": name,
        "repairedDefect": c["repairedDefect"], "repairedFrame": c["repairedFrame"],
        "clipJson": CH + "/%s/clip.json" % name,
        "clipSha256": sha(os.path.join(CH, name, "clip.json")),
        "experimentClipJson": EX + "/%s/clip.json" % name,
        "experimentClipSha256": sha(os.path.join(EX, name, "clip.json")),
        "masterAseprite": CH + "/%s/body256.aseprite" % name,
        "masterSha256": h["bodyMaster"],
        "nativeMasterAseprite": CH + "/%s/native128.aseprite" % name,
        "nativeMasterSha256": h["nativeMaster"],
        "frameCount": 12, "totalDurationMs": c["total"],
        "acceptedKeyPreservation": [
            {"index": i, "name": kn, "sha256": kh, "byteExact": True, "pixelExact": True}
            for i, (kn, kh) in sorted(c["keys"].items())]})

patch = {
    "schemaVersion": 1, "status": "GLM_BODY_FIXES_READY",
    "technicalStatus": "TECHNICALLY_COMPLETE",
    "artisticStatus": "VISUAL_REVIEW_REQUIRED",
    "creatorStatus": "PENDING_CREATOR",
    "globalArtisticStatusUnchanged": "ARTISTIC_REVISION_REQUIRED",
    "character": "orc-v1", "identity": "Verde Warcraft", "cellsCount": 2,
    "producer": "GLM 5.3 body-specialist (dev de correção; sem autoaprovação)",
    "repairedDefects": ["REAR-01-RESIDUAL-A", "REAR-01-RESIDUAL-B", "REAR-02-PERSISTENT"],
    "cells": cells,
    "generationAccounting": {
        "balanceBefore": 1342.70, "chargedTotal": 6.0, "balanceAfter": 1336.70,
        "jobs": [{"tool": "inpaint_image_pro_flash",
                  "jobId": "540302e4-2690-4282-8de5-c609f15b1142",
                  "cycle": "back_l-Axe-full", "frame": 2, "seed": 20261029,
                  "charged": 6.0}],
        "costLlm": "Custo LLM não informado"}}

with open(os.path.join(EX, "patch-manifest.json"), "w", encoding="utf-8") as f:
    json.dump(patch, f, indent=2)
print("MANIFEST OK")
for c in cells:
    print(c["cycleName"], c["clipSha256"][:16], c["experimentClipSha256"][:16])
