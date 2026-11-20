"""Build experiments/main-orc-combat-recovery-v7/patch-manifest.json.

Reads the exported frontal cell directories (V6 baseline vs V7 candidate), the V7 clip.json
provenance and the T1/T2/T3 deliverables, and emits one machine-readable manifest of what
changed for this checkpoint. Measurement only: it hashes and compares PNGs, it never writes art.
"""
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
EXP = os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7")
V7 = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-recovery-v7", "frontal")
V6 = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6")
CHECKPOINT = "V7_ECON_FORENSICS_AND_FRONTAL_READY"


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()


def walk(d):
    out = {}
    for root, _dirs, files in os.walk(d):
        for f in files:
            p = os.path.join(root, f)
            out[os.path.relpath(p, d).replace("\\", "/")] = sha(p)
    return out


def compare(v6dir, v7dir):
    a = walk(v6dir)
    b = walk(v7dir)
    same = sorted(k for k in b if k in a and a[k] == b[k])
    diff = sorted(k for k in b if k in a and a[k] != b[k])
    return {
        "baselineFiles": len(a),
        "candidateFiles": len(b),
        "byteIdentical": len(same),
        "changed": diff,
        "onlyInBaseline": sorted(k for k in a if k not in b),
        "onlyInCandidate": sorted(k for k in b if k not in a),
        "changedCount": len(diff),
    }


cells = [
    ("front_l/Sword", "front_l-Sword-full", os.path.join(V6, "frontal-escalated", "front_l-Sword-full")),
    ("front_l/Axe", "front_l-Axe-full", os.path.join(V6, "frontal", "front_l-Axe-full")),
    ("front_r/Axe", "front_r-Axe-full", os.path.join(V6, "frontal", "front_r-Axe-full")),
    ("front_r/Sword", "full-front-r-sword", os.path.join(V6, "frontal", "full-front-r-sword")),
]

manifest_cells = []
for cell, dirname, baseline in cells:
    v7dir = os.path.join(V7, dirname)
    cmp_ = compare(baseline, v7dir)
    with open(os.path.join(v7dir, "clip.json"), encoding="utf-8") as f:
        clip = json.load(f)
    entry = {
        "cell": cell,
        "clipDir": rel(v7dir),
        "baselineDir": rel(baseline),
        "clipId": clip["id"],
        "category": clip["category"],
        "direction": clip["direction"],
        "frameCount": clip["frameCount"],
        "totalDurationMs": clip["totalDurationMs"],
        "durationsMs": clip["durationsMs"],
        "canvas": clip["canvas"],
        "nativeCanvas": clip["nativeCanvas"],
        "bodyOffset": clip["bodyOffset"],
        "groundY": clip["groundY"],
        "nativeGroundY": clip["nativeGroundY"],
        "layerOrder": clip["layerOrder"],
        "visibilityPolicy": clip["visibilityPolicy"],
        "visibleInterval": clip["visibleInterval"],
        "state": "CHANGED" if cmp_["changedCount"] else "VERIFIED_UNCHANGED",
        "byteIdentity": {
            "baselineFiles": cmp_["baselineFiles"],
            "candidateFiles": cmp_["candidateFiles"],
            "byteIdentical": cmp_["byteIdentical"],
            "changed": cmp_["changedCount"],
            "onlyInBaseline": cmp_["onlyInBaseline"],
            "onlyInCandidate": cmp_["onlyInCandidate"],
        },
        "hashes": {
            "clipJson": sha(os.path.join(v7dir, "clip.json")),
            "masterComposite": clip["masterSha256"],
            "bodyMaster": clip["bodyMasterSha256"],
            "nativeMaster": clip["nativeMasterSha256"],
            "handMaster": clip["handMasterSha256"],
            "nativeStrip": clip["nativeStripSha256"],
            "compositeStrip": clip["compositeStripSha256"],
        },
        "technicalStatus": clip["technicalStatus"],
        "artisticStatus": clip["artisticStatus"],
        "artisticApproval": clip["artisticApproval"],
        "runtimeImplemented": clip.get("runtimeImplemented", clip.get("provenance", {}).get("runtimeImplemented", False)),
        "eligibleForIntegration": clip.get("eligibleForIntegration", False),
        "newPixelLabCalls": clip.get("provenance", {}).get("newPixelLabCalls", 0),
        "costUsd": clip.get("provenance", {}).get("costUsd", 0.0),
    }
    if cmp_["changedCount"]:
        entry["framesChanged"] = [3, 4]
        entry["pixelsChanged"] = 19
        entry["pixelsChangedPerFrame"] = {"3": 9, "4": 10}
        entry["changedFiles"] = cmp_["changed"]
        entry["defects"] = clip["v7AxillaRepair"]["defectsAddressed"]
        entry["rule"] = clip["v7AxillaRepair"]["rule"]
        entry["residualRisk"] = clip["v7AxillaRepair"]["residualRisk"]
        entry["bodyRgbaDelta"] = {"frame3": "30 -> 27", "frame4": "28 -> 24"}
    else:
        entry["note"] = ("Byte-identical copy of the V6 frontal source, kept as a measurement "
                         "carrier so the four frontal cells can be reviewed together. Its clip.json "
                         "is the unmodified V6 file, which stays valid because every PNG is identical.")
    manifest_cells.append(entry)

with open(os.path.join(EXP, "input-preservation.json"), encoding="utf-8") as f:
    preserved = json.load(f)


def verify_preservation():
    ok = 0
    changed, missing = [], []
    for relpath, expected in preserved["files"].items():
        p = os.path.join(ROOT, relpath.replace("/", os.sep))
        if not os.path.exists(p):
            missing.append(relpath)
        elif sha(p) == expected:
            ok += 1
        else:
            changed.append(relpath)
    return {"checked": len(preserved["files"]), "identical": ok,
            "changed": changed, "missing": missing}


pres = verify_preservation()

verification = json.load(open(os.path.join(EXP, "frontal", "verification-v7.json"), encoding="utf-8"))
rim = json.load(open(os.path.join(EXP, "frontal", "detect", "body-rim-v5-control.json"), encoding="utf-8"))

doc_paths = {
    "taskText": "experiments/main-orc-combat-recovery-v7/econ-dev-prompt.txt",
    "forensicsReport": "experiments/main-orc-combat-recovery-v7/forensics/white-flash.md",
    "forensicsData": "experiments/main-orc-combat-recovery-v7/forensics/white-flash.json",
    "lightContoursReport": "experiments/main-orc-combat-recovery-v7/frontal/light-contours.md",
    "lightContoursData": "experiments/main-orc-combat-recovery-v7/frontal/detect/body-rim-census.json",
    "lightContoursV5Control": "experiments/main-orc-combat-recovery-v7/frontal/detect/body-rim-v5-control.json",
    "boundaryCensusV5VsV7": "experiments/main-orc-combat-recovery-v7/frontal/detect/v5-vs-v7-boundary.json",
    "layerDiffV5VsV7": "experiments/main-orc-combat-recovery-v7/frontal/detect/v5-vs-v7-layers.json",
    "editPlan": "experiments/main-orc-combat-recovery-v7/frontal/edit-plan-v7.json",
    "editTable": "experiments/main-orc-combat-recovery-v7/frontal/edit-table-v7.json",
    "verification": "experiments/main-orc-combat-recovery-v7/frontal/verification-v7.json",
    "reviewSurface": "experiments/main-orc-combat-recovery-v7/frontal/review.html",
    "authorScript": "experiments/main-orc-combat-recovery-v7/scripts/author-frontl-sword-v7.lua",
    "report": "experiments/main-orc-combat-recovery-v7/report.md",
    "thisManifest": "experiments/main-orc-combat-recovery-v7/patch-manifest.json",
}
del doc_paths["thisManifest"]

out = {
    "schemaVersion": 1,
    "revision": "main-orc-v7-axilla-recovery",
    "checkpoint": CHECKPOINT,
    "character": "orc-v1",
    "scope": ("Four frontal combat cells only: forensics on the two rear Sword clips (T1, read-only), "
              "axilla repair of front_l/Sword F03/F04 (T2), light-contour search on all four frontal "
              "clips (T3). No rear asset, no V5 or V6 source, no Unity file was written."),
    "status": {
        "technicalStatus": "TECHNICALLY_COMPLETE",
        "artisticStatus": "VISUAL_REVIEW_REQUIRED",
        "artisticApproval": "PENDING_CREATOR",
        "runtimeImplemented": False,
        "eligibleForIntegration": False,
        "fullClipIndependentQA": "PENDING",
    },
    "budget": {"newPixelLabCalls": 0, "costUsd": 0.0, "paidServicesUsed": []},
    "authority": {
        "v6CandidateManifest": {
            "path": "characters/orc-v1/source/artistic-reconstruction-v6/candidate28manifest.json",
            "sha256": "5d68b52d3e2b2a0931d689afb5a9dd438c178835d05efb02a5fb2bcf0c64b7ca",
            "standing": ("ARTISTICALLY REJECTED by the creator. Nothing in this checkpoint promotes, "
                         "re-registers or re-uses that manifest's status; the V7 cell is an independent "
                         "candidate pending creator review."),
        },
        "baselineForT2": {
            "path": "characters/orc-v1/source/artistic-reconstruction-v6/frontal-escalated/front_l-Sword-full",
            "clipJsonSha256": "f6b3c694ceec2f6bdc1786a3aa24527021adfafc8b7af72324751879580606fd",
            "note": "Read-only baseline. Still byte-identical after this checkpoint (see preservation).",
        },
        "preEscalationReference": {
            "path": "characters/orc-v1/source/artistic-reconstruction-v6/frontal/front_l-Sword-full",
            "note": "Non-escalated frontal clip; source of the native pixel values used by the T2 repair.",
        },
        "v5Control": {
            "path": "characters/orc-v1/source/combat-rescue-v5/grip-specialist",
            "note": "Read-only control for the T3 detectors.",
        },
    },
    "preservation": {
        "inputManifest": "experiments/main-orc-combat-recovery-v7/input-preservation.json",
        "capturedAt": preserved["capturedAt"],
        "inputScope": preserved["scope"],
        "checked": pres["checked"],
        "identical": pres["identical"],
        "changed": pres["changed"],
        "missing": pres["missing"],
        "verdict": ("All tracked pre-existing Orc V1 inputs, weapons and identity authority files are "
                    "byte-identical to the snapshot taken at the start of this task.")
        if not pres["changed"] and not pres["missing"] else "PRESERVATION FAILURE",
    },
    "tasks": {
        "T1": {
            "title": "Numeric forensics of the rear Sword white flash",
            "mode": "READ_ONLY",
            "artChanged": False,
            "verdict": ("The flash is authored content in the saved master. A fresh Aseprite export of "
                        "the master equals the committed layers, the committed frames and the alpha-over "
                        "recompose with 0 differing pixels. Cause: layers/body/00.png and body/11.png are "
                        "byte-identical to complete-v1/back_l/Idle/00.png, so the preserved idle bookends "
                        "carry a light-metal highlight the generated attack bodies lack."),
            "reports": ["experiments/main-orc-combat-recovery-v7/forensics/white-flash.md",
                        "experiments/main-orc-combat-recovery-v7/forensics/white-flash.json"],
            "measured": {
                "back_l/Sword": {"leftHalfLightPxF00": 61, "F01": 13, "F10": 21, "F11": 61,
                                 "contiguousMass": {"bbox": [97, 117, 108, 137],
                                                    "rgb(153,154,155)": 36, "rgb(171,173,173)": 25},
                                 "isolated": {"bbox": [103, 117, 108, 119], "px": 9}},
                "back_r/Sword": {"leftHalfLightPxF00": 46, "F01": 2, "mirrorOf": "back_l/Sword"},
                "isolatedClusterInF01ToF10": 0,
            },
            "notClaimed": ("No claim about how the highlight reads at playback speed. T1 identifies the "
                           "source of the pixels; it does not judge them."),
        },
        "T2": {
            "title": "front_l/Sword axilla repair",
            "mode": "AUTHORED_IN_ASEPRITE",
            "cell": "front_l/Sword",
            "framesChanged": [3, 4],
            "pixelsChanged": 19,
            "pixelsChangedPerFrame": {"3": 9, "4": 10},
            "layerTouched": "body (and the derived composite/native masters)",
            "rule": ("Restore the native colour each repainted pixel held in the non-escalated V6 clip; "
                     "where that would leave 3+ consecutive identical colours on the new medial edge, "
                     "take the value the adjacent column (x+1) held on the same row. No colour invented, "
                     "no pixel filled, no pose or timing change."),
            "defectsFixed": [
                "D1 flat rgb(12,15,18) ink plate on x=147 y117..122 in F03 and F04 (+(148,116) both, +(149,115) F04)",
                "D2 retrograde step at y=123 (left boundary 147 -> 148 -> 147)",
                "D3 orphan rgb(95,96,99) at (149,122) in F03 with zero opaque neighbours",
                "D4 comb-tooth island rgb(77,79,82) at (152,115) in F04 between the 2 px pinhole and the main opening",
            ],
            "ruledOut": [
                "The light column x=147 y127..133 is identical in the non-escalated clip: a pre-existing rim, not a V6 artifact.",
                "The 5 px apex at F03 y116 is consistent with its neighbours (F04 y114 is also 5 px).",
            ],
            "measurements": {
                "bodyRgbaDeltaFrame3": {"before": 30, "after": 27},
                "bodyRgbaDeltaFrame4": {"before": 28, "after": 24},
                "byteIdenticalFilesOutsidePatch": verification["checks"]["byteIdenticalFiles"],
                "onlyDeclaredPixelsChanged": verification["checks"]["onlyDeclaredPixelsChanged"],
                "undeclaredPixels": verification["checks"]["undeclaredPixels"],
                "weaponAndHandLayersIdentical": verification["checks"]["weaponAndHandLayersIdentical"],
                "weaponExportsByteIdentical": "39/39 (weaponBack + weaponFront + handFront over 13 frames)",
                "monotoneLeftBoundary": verification["checks"]["monotoneLeftBoundary"],
                "danglingPixels": verification["checks"]["danglingPixels"],
                "leftBoundaryF03": [148, 147, 147, 147, 147, 147, 147, 147, 147, 146],
                "leftBoundaryF04": [154, 149, 148, 147, 147, 147, 147, 147, 147, 147, 147, 146],
                "timingChanged": False,
                "poseChanged": False,
            },
            "authoring": {
                "editor": "Aseprite 1.3.18.6 --batch --noinapp",
                "profile": "tmp/aseprite-v7-econ-profile (isolated)",
                "script": "experiments/main-orc-combat-recovery-v7/scripts/author-frontl-sword-v7.lua",
                "scriptOutput": "APPLIED 57 EDITS (19 declared pixels x 3 masters)",
                "authoredProgrammatically": True,
                "visualLimitation": ("DEV worked without image perception; the repair is derived from "
                                     "measured native pixel values, not from sight."),
            },
        },
        "T3": {
            "title": "Light-contour search in the four frontal clips",
            "mode": "MEASUREMENT_ONLY",
            "artChanged": False,
            "pixelsChanged": 0,
            "verdict": "NO CONFIRMED ARTIFACT",
            "operatingThreshold": 145.0,
            "thresholdRationale": ("L >= 145 is the highest value that still includes the body rim family "
                                   "rgb(147,148,149) (L=147.9) while separating the metal bands (153.9, 177.7). "
                                   "The palette maximum is only L=177.72, so an 'L >= 200 white' rule would "
                                   "match nothing."),
            "clips": {
                "front_l/Sword": {"bodyBoundaryLight": 9, "weaponBoundaryLight": 16,
                                  "smallLightOnBoundary": 16, "insetLightLine": 282, "spike": 115},
                "front_l/Axe": {"bodyBoundaryLight": 5, "weaponBoundaryLight": 23,
                                "smallLightOnBoundary": 22, "insetLightLine": 34, "spike": 135},
                "front_r/Axe": {"bodyBoundaryLight": 0, "weaponBoundaryLight": 23,
                                "smallLightOnBoundary": 17, "insetLightLine": 34, "spike": 135},
                "front_r/Sword": {"bodyBoundaryLight": 0, "weaponBoundaryLight": 16,
                                  "smallLightOnBoundary": 7, "insetLightLine": 282, "spike": 118},
            },
            "controlEvidence": {
                "boundaryCensusV5VsV7": ("Identical at T=145 on every frame of all four clips; the only "
                                         "difference anywhere is front_l/Sword F03 at T=120, where V7 has "
                                         "2 FEWER light boundary pixels (the T2 erasure)."),
                "weaponLayersV5VsV7": "0 px changed on every frame of every frontal clip",
                "bodyRimTuplesV5VsV7": {k: {"v5": v["v5"], "v7": v["v7"], "common": v["common"],
                                            "onlyV5": len(v["onlyV5"]), "onlyV7": len(v["onlyV7"])}
                                        for k, v in rim["clips"].items()},
            },
            "whyEachClassIsLegitimate": {
                "bodyBoundaryLight": ("All 14 body instances are rgb(147,148,149) sitting at the top of a "
                                      "continuous 5-step ramp (148 -> 140 -> 108 -> 91 -> 74 -> 57), appear "
                                      "only on the lit-facing left views, and all 14 predate V6 at the same "
                                      "coordinate."),
                "weaponBoundaryLight": "Weapon layers are byte-identical V5 vs V7; edge lighting of a metal band, run 1-2 px.",
                "insetLightLine": "281/282 and 33/34 are weaponFront blade/axe-head shading lines, run 3-19 px.",
                "spike": "Body ink contour rgb(6,6,8)/rgb(0,0,1)/rgb(2,2,3); F00/F01 counts identical in all four clips.",
            },
            "report": "experiments/main-orc-combat-recovery-v7/frontal/light-contours.md",
            "notRuledOut": [
                "A light contour that is continuous with a legitimate rim and stayed below T=145.",
                "Perceived flicker at playback speed (per-frame tables show no isolated single-frame spike, but that is a proxy).",
                "Hue/saturation artifacts at identical lightness (all reported classes were additionally matched by exact RGBA against the palette ladder).",
            ],
        },
    },
    "cells": manifest_cells,
    "deliverables": {},
    "guarantees": {
        "v5SourcesTouched": False,
        "v6SourcesTouched": False,
        "rearCellsTouched": False,
        "unityFilesTouched": False,
        "commitsCreated": 0,
        "runtimeImplemented": False,
        "qaPerformedHere": False,
        "integrationPerformedHere": False,
    },
    "stop": {
        "checkpoint": CHECKPOINT,
        "nextOwner": ("Orchestrator: independent QA of the front_l/Sword cell at 1x and normal playback "
                      "speed, then creator review. Nothing here is approved."),
    },
}

for key, relpath in doc_paths.items():
    p = os.path.join(ROOT, relpath.replace("/", os.sep))
    out["deliverables"][key] = {"path": relpath, "sha256": sha(p), "exists": True}

dst = os.path.join(EXP, "patch-manifest.json")
with open(dst, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("WROTE", dst)
for c in manifest_cells:
    print("  %-14s %-18s identical=%d/%d changed=%d" % (
        c["cell"], c["state"], c["byteIdentity"]["byteIdentical"],
        c["byteIdentity"]["baselineFiles"], c["byteIdentity"]["changed"]))
print("  preservation %d/%d identical, changed=%d missing=%d" % (
    pres["identical"], pres["checked"], len(pres["changed"]), len(pres["missing"])))
