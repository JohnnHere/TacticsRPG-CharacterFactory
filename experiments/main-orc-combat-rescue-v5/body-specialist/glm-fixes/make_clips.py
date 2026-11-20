# -*- coding: utf-8 -*-
"""Gera clip.json (x4) + representative.json (x4) + hashes-summary.json com hashes reais."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contracts_data import CH, EX, SRC, CYCLES, sha

hs = {}
for name, c in CYCLES.items():
    chd, exd = os.path.join(CH, name), os.path.join(EX, name)
    h = {"frames": {}, "keys": {}}
    for idx, (kn, kh) in c["keys"].items():
        got = sha(os.path.join(chd, "native", "%02d.png" % idx))
        assert got == kh, "KEY MISMATCH %s F%02d" % (name, idx)
        h["keys"]["F%02d" % idx] = got
    for kind in ("native", "body256"):
        for i in range(12):
            h["frames"]["%s/%02d" % (kind, i)] = sha(os.path.join(chd, kind, "%02d.png" % i))
    h["nativeMaster"] = sha(os.path.join(chd, "native128.aseprite"))
    h["bodyMaster"] = sha(os.path.join(chd, "body256.aseprite"))
    h["strip"] = sha(os.path.join(chd, "native-strip.png"))
    h["compositeStrip"] = sha(os.path.join(chd, "body256-strip.png"))
    hs[name] = h

    def clip_for(prefix, c=c, h=h, name=name):
        frames = []
        for i in range(12):
            f = {"index": i, "durationMs": c["durations"][i],
                 "nativePng": {"path": "%s/%s/native/%02d.png" % (prefix, name, i),
                               "sha256": h["frames"]["native/%02d" % i]},
                 "compositePng": {"path": "%s/%s/body256/%02d.png" % (prefix, name, i),
                                  "sha256": h["frames"]["body256/%02d" % i]},
                 "weaponVisible": False, "isAcceptedKey": i in c["keys"]}
            if i in c["keys"]:
                kn, kh = c["keys"][i]
                f.update(keyName=kn, keySourceSha256=kh, pixelExact=True, byteExact=True)
            if i == c["repairedFrame"]:
                f.update(repairedDefect=c["repairedDefect"], repairedBy="glm-fixes")
            frames.append(f)
        return {"schemaVersion": 1, "id": c["id"], "revision": c["revision"],
                "character": "orc-v1", "identity": "Verde Warcraft",
                "category": c["category"], "state": "Attack", "direction": c["direction"],
                "scope": c["scope"], "loop": False, "oneShot": True, "terminal": False,
                "canvas": [256, 256], "nativeCanvas": [128, 128], "bodyOffset": [64, 64],
                "groundY": 190, "nativeGroundY": 126, "frameCount": 12,
                "durationsMs": c["durations"], "totalDurationMs": c["total"],
                "master": "%s/%s/body256.aseprite" % (prefix, name),
                "masterSha256": h["bodyMaster"],
                "bodyMaster": "%s/%s/body256.aseprite" % (prefix, name),
                "bodyMasterSha256": h["bodyMaster"],
                "nativeMaster": "%s/%s/native128.aseprite" % (prefix, name),
                "nativeMasterSha256": h["nativeMaster"],
                "strip": "%s/%s/native-strip.png" % (prefix, name),
                "stripSha256": h["strip"],
                "compositeStrip": "%s/%s/body256-strip.png" % (prefix, name),
                "compositeStripSha256": h["compositeStrip"],
                "technicalStatus": "TECHNICALLY_COMPLETE",
                "artisticStatus": "VISUAL_REVIEW_REQUIRED",
                "creatorStatus": "PENDING_CREATOR", "propagationAllowed": False,
                "frames": frames}

    p_ch, p_ex = os.path.join(chd, "clip.json"), os.path.join(exd, "clip.json")
    for p, clip in ((p_ch, clip_for(CH)), (p_ex, clip_for(EX))):
        with open(p, "w", encoding="utf-8") as f:
            json.dump(clip, f, indent=2)
    rep = {"schemaVersion": 1, "status": c["repStatus"],
           "technicalStatus": "TECHNICALLY_COMPLETE",
           "artisticStatus": "VISUAL_REVIEW_REQUIRED",
           "globalArtisticStatusUnchanged": "ARTISTIC_REVISION_REQUIRED",
           "creatorStatus": "PENDING_CREATOR", "character": "orc-v1",
           "identity": "Verde Warcraft", "direction": c["direction"],
           "category": c["category"], "scope": c["scope"],
           "repairedDefect": c["repairedDefect"], "repairedFrame": c["repairedFrame"],
           "clip": {"path": CH + "/%s/clip.json" % name, "sha256": sha(p_ch)},
           "master": {"path": CH + "/%s/body256.aseprite" % name,
                      "sha256": h["bodyMaster"]},
           "nativeMaster": {"path": CH + "/%s/native128.aseprite" % name,
                            "sha256": h["nativeMaster"]},
           "frameCount": 12, "totalDurationMs": c["total"],
           "acceptedKeyReuse": [{"frameIndex": i, "keyName": kn,
                "source": {"path": "%s/%s/native/%02d.png" % (SRC, name, i), "sha256": kh},
                "export": {"path": "%s/%s/native/%02d.png" % (CH, name, i),
                           "sha256": h["keys"]["F%02d" % i]},
                "pixelExact": True, "byteExact": True}
                for i, (kn, kh) in sorted(c["keys"].items())],
           "generationAccounting": c["pixellab"]}
    for root in (chd, exd):
        with open(os.path.join(root, "representative.json"), "w", encoding="utf-8") as f:
            json.dump(rep, f, indent=2)
    print("cycle ok:", name, "clipSha:", sha(p_ch)[:16], "expSha:", sha(p_ex)[:16])

with open(os.path.join(EX, "hashes-summary.json"), "w", encoding="utf-8") as f:
    json.dump(hs, f, indent=2)
print("CLIPS OK")
