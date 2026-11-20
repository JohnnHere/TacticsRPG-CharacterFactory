import os
import json

directions = ["front_r", "front_l", "back_r", "back_l"]
actions = ["Idle", "Walk", "Unarmed", "Sword", "Axe", "Hit", "Defeat"]

ACTIVE_CANDIDATES = {
    "back_r/Walk": {
        "clipJson": "characters/orc-v1/source/rear-recovery-v2/back_r/Walk/clip.json",
        "reviewStatus": "ROOT_PASSED_FOR_INTERNAL_EXPANSION",
        "notes": "Method-02 temporal 8-frame cycle (160ms/frame, 1280ms total) with alternating support/swing phase and ground registration"
    },
    "back_l/Walk": {
        "clipJson": "characters/orc-v1/source/rear-recovery-v2/back_l/Walk/clip.json",
        "reviewStatus": "ROOT_PASSED_FOR_INTERNAL_EXPANSION",
        "notes": "Method-02 NW base temporal 8-frame cycle with own back_l base and NW perspective"
    },
    "back_r/Unarmed": {
        "clipJson": "characters/orc-v1/source/rear-recovery-v2/back_r/Unarmed/clip.json",
        "reviewStatus": "ACTIVE_CANDIDATE",
        "notes": "5-frame heavy gauntlet strike reaching x=122; cranium, nape outline and collar aligned to character identity (450ms)"
    },
    "back_l/Unarmed": {
        "clipJson": "characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed/clip.json",
        "reviewStatus": "ACTIVE_CANDIDATE",
        "notes": "5-frame NW heavy gauntlet strike reaching x=6; cranium and collar aligned to authentic NW base (450ms)"
    },
    "front_r/Defeat": {
        "clipJson": "characters/orc-v1/source/rear-recovery-v2/front_r/Defeat/clip.json",
        "reviewStatus": "ACTIVE_CANDIDATE",
        "notes": "5-frame defeat sequence; terminal stage 04 replaced with complete incapacitated ground collapse (700ms)"
    },
    "front_l/Defeat": {
        "clipJson": "characters/orc-v1/source/rear-recovery-v2/front_l/Defeat/clip.json",
        "reviewStatus": "ACTIVE_CANDIDATE",
        "notes": "5-frame NW defeat sequence; terminal stage 04 replaced with complete incapacitated ground collapse (700ms)"
    }
}

REVISION_REQUIRED = {
    "back_r/Sword": {
        "clipJson": "characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack/clip.json",
        "rejectedEvidence": "experiments/main-orc-rear-recovery-v2/rejected/flat-weapon-masters/back_r/sword/Attack/clip.json",
        "reviewStatus": "ARTISTIC_REVISION_REQUIRED",
        "notes": "Delivered candidate was flattened into 1 layer instead of 4 independent layers (weaponBack, body, weaponFront, handFront); old blade placement misaligned with new anatomical key. Under artistic revision."
    },
    "back_l/Sword": {
        "clipJson": "characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack/clip.json",
        "rejectedEvidence": "experiments/main-orc-rear-recovery-v2/rejected/flat-weapon-masters/back_l/sword/Attack/clip.json",
        "reviewStatus": "ARTISTIC_REVISION_REQUIRED",
        "notes": "Delivered candidate was flattened into 1 layer instead of 4 independent layers; old blade placement misaligned with new anatomical key. Under artistic revision."
    },
    "back_r/Axe": {
        "clipJson": "characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack/clip.json",
        "rejectedEvidence": "experiments/main-orc-rear-recovery-v2/rejected/flat-weapon-masters/back_r/axe/Attack/clip.json",
        "reviewStatus": "ARTISTIC_REVISION_REQUIRED",
        "notes": "Delivered candidate was flattened into 1 layer instead of 4 independent layers; old blade placement misaligned with new anatomical key. Under artistic revision."
    },
    "back_l/Axe": {
        "clipJson": "characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack/clip.json",
        "rejectedEvidence": "experiments/main-orc-rear-recovery-v2/rejected/flat-weapon-masters/back_l/axe/Attack/clip.json",
        "reviewStatus": "ARTISTIC_REVISION_REQUIRED",
        "notes": "Delivered candidate was flattened into 1 layer instead of 4 independent layers; old blade placement misaligned with new anatomical key. Under artistic revision."
    }
}

cells = []

for d in directions:
    for a in actions:
        cell_id = f"{d}/{a}"
        cell = {
            "direction": d,
            "action": a,
            "cellId": cell_id,
        }
        
        if cell_id in ACTIVE_CANDIDATES:
            info = ACTIVE_CANDIDATES[cell_id]
            cell["status"] = "ACTIVE_CANDIDATE"
            cell["isAffected"] = True
            cell["clipJson"] = info["clipJson"]
            cell["reviewStatus"] = info["reviewStatus"]
            cell["provenance"] = "main-orc-rear-recovery-v2"
            cell["notes"] = info["notes"]
        elif cell_id in REVISION_REQUIRED:
            info = REVISION_REQUIRED[cell_id]
            cell["status"] = "ARTISTIC_REVISION_REQUIRED"
            cell["isAffected"] = True
            cell["clipJson"] = info["clipJson"]
            cell["rejectedEvidence"] = info["rejectedEvidence"]
            cell["reviewStatus"] = info["reviewStatus"]
            cell["provenance"] = "main-orc-rear-recovery-v2 (revision required)"
            cell["notes"] = info["notes"]
        else:
            base_clip = f"characters/orc-v1/source/complete-v1/{d}/{a}/clip.json"
            if not os.path.exists(base_clip):
                base_clip = f"characters/orc-v1/source/complete-v1/{d}/{a}/Attack/clip.json"
                
            cell["status"] = "UNCHANGED_ALIAS"
            cell["isAffected"] = False
            cell["clipJson"] = base_clip
            cell["reviewStatus"] = "PROTECTED_BASELINE_CANONICAL"
            cell["provenance"] = "main-orc-complete-v1 (baseline b178422e1f7fc19f068c)"
            cell["notes"] = "Exact protected clip preserved byte-for-byte"
            
        cells.append(cell)

manifest = {
    "schemaVersion": 1,
    "manifestId": "orc-v1.rear-recovery-v2.candidate28",
    "characterId": "orc-v1",
    "characterName": "Verde Warcraft",
    "revision": "main-orc-rear-recovery-v2",
    "baselineBuild": "dist/editor/orc-v1-complete-v1/b178422e1f7fc19f068c",
    "totalClips": 28,
    "activeCandidatesCount": sum(1 for c in cells if c["status"] == "ACTIVE_CANDIDATE"),
    "inRevisionCount": sum(1 for c in cells if c["status"] in ["IN_REVISION", "ARTISTIC_REVISION_REQUIRED"]),
    "inProductionCount": sum(1 for c in cells if c["status"] == "IN_PRODUCTION"),
    "unchangedAliasesCount": sum(1 for c in cells if c["status"] == "UNCHANGED_ALIAS"),
    "cells": cells
}

out_p1 = 'characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json'
out_p2 = 'experiments/main-orc-rear-recovery-v2/candidate28manifest.json'

os.makedirs(os.path.dirname(out_p1), exist_ok=True)
with open(out_p1, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)
with open(out_p2, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)

print(f"Candidate 28 manifest updated truthfully: {manifest['activeCandidatesCount']} active, {manifest['inRevisionCount']} revision required, {manifest['unchangedAliasesCount']} unchanged.")
