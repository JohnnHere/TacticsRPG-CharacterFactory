"""Rewrite the copied V7 clip.json: real paths, real hashes, V7 provenance.

The clip.json inherited from the V6 escalated candidate still points at V6 paths and V6
hashes. This script rewrites paths to the V7 output tree, recomputes every SHA-256 from
disk, recomputes bodyRgbaDelta against the non-escalated V6 clip, and records the V7
axilla repair provenance. It performs no image work.
"""
import hashlib
import json
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
V7 = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-recovery-v7", "frontal", "front_l-Sword-full")
V6ESC = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6",
                     "frontal-escalated", "front_l-Sword-full")
V6PLAIN = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6",
                       "frontal", "front_l-Sword-full")
CLIP = os.path.join(V7, "clip.json")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


def uniq_colors(p):
    with Image.open(p) as im:
        return len(set(im.convert("RGBA").getdata()))


with open(CLIP, encoding="utf-8") as f:
    clip = json.load(f)

with open(os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7",
                       "frontal", "verification-v7.json"), encoding="utf-8") as f:
    verify = json.load(f)

old_prefix = rel(V6ESC)
new_prefix = rel(V7)

# --- scalar paths -------------------------------------------------------------
for key in ("master", "bodyMaster", "nativeMaster", "handMaster", "strip", "nativeStrip", "compositeStrip"):
    if key in clip and isinstance(clip[key], str):
        clip[key] = clip[key].replace(old_prefix, new_prefix)

# --- hashes -------------------------------------------------------------------
def path_of(key):
    return os.path.join(ROOT, clip[key].replace("/", os.sep))

clip["masterSha256"] = sha(path_of("master"))
clip["bodyMasterSha256"] = sha(path_of("bodyMaster"))
clip["nativeMasterSha256"] = sha(path_of("nativeMaster"))
clip["handMasterSha256"] = sha(path_of("handMaster"))
clip["stripSha256"] = sha(path_of("strip"))
clip["nativeStripSha256"] = sha(path_of("nativeStrip"))
clip["compositeStripSha256"] = sha(path_of("compositeStrip"))

# --- per frame ---------------------------------------------------------------
plain_counts = {}
for i in range(clip["frameCount"]):
    fr = clip["frames"][i]
    ix = "%02d" % i
    fr["png"] = rel(os.path.join(V7, ix + ".png"))
    fr["sha256"] = sha(os.path.join(V7, ix + ".png"))
    fr["nativePng"] = rel(os.path.join(V7, "native", ix + ".png"))
    fr["nativeSha256"] = sha(os.path.join(V7, "native", ix + ".png"))
    for name, entry in fr["layers"].items():
        p = os.path.join(V7, "layers", name, ix + ".png")
        entry["png"] = rel(p)
        entry["sha256"] = sha(p)
    # bodyRgbaDelta is defined against the non-escalated V6 clip (bodyRgbaDeltaReference)
    a = os.path.join(V6PLAIN, "layers", "body", ix + ".png")
    b = os.path.join(V7, "layers", "body", ix + ".png")
    with Image.open(a) as ia, Image.open(b) as ib:
        pa = list(ia.convert("RGBA").getdata())
        pb = list(ib.convert("RGBA").getdata())
    plain_counts[i] = sum(1 for x, y in zip(pa, pb) if x != y)
    fr["bodyRgbaDelta"] = plain_counts[i]

# --- revision / status / provenance ------------------------------------------
parent_clip = os.path.join(V6ESC, "clip.json")
clip["revision"] = "main-orc-v7-axilla-recovery"
clip["sourceParentClip"] = rel(parent_clip)
clip["sourceParentClipSha256"] = sha(parent_clip)
clip["technicalStatus"] = "TECHNICALLY_COMPLETE"
clip["artisticStatus"] = "VISUAL_REVIEW_REQUIRED"
clip["artisticApproval"] = "PENDING_CREATOR"
clip["eligibleForIntegration"] = False
clip["runtimeImplemented"] = False
clip["checkpoint"] = "V7_ECON_FORENSICS_AND_FRONTAL_READY"
clip["fullClipIndependentQA"] = "PENDING"

v7_script = os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7", "scripts",
                         "author-frontl-sword-v7.lua")
plan = os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7", "frontal", "edit-plan-v7.json")
verify_json = os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7", "frontal",
                           "verification-v7.json")

prev = clip.get("provenance", {})
clip["provenance"] = {
    "authoring": ("Inherited V6 escalated poses. Body-layer only: the V6 escalation painted a flat "
                  "rgb(12,15,18) ink plate on the new medial edge of the axilla opening in F03/F04; V7 "
                  "restores the native pre-escalation tone of each repainted pixel (or the adjacent "
                  "column's native tone where a run of 3+ identical colours would remain) and removes a "
                  "detached pixel, a 1 px comb-tooth island and a 1 px retrograde step. Saved, reopened and "
                  "re-exported in Aseprite."),
    "script": rel(v7_script),
    "scriptSha256": sha(v7_script),
    "plan": rel(plan),
    "planSha256": sha(plan),
    "verification": rel(verify_json),
    "anatomy": prev.get("anatomy"),
    "bodyRgbaChanged": True,
    "timingChanged": False,
    "weaponsChanged": False,
    "newPixelLabCalls": 0,
    "costUsd": 0.0,
    "runtimeImplemented": False,
    "editor": "Aseprite 1.3.18.6 --batch --noinapp, isolated profile tmp/aseprite-v7-econ-profile",
    "visualLimitation": ("DEV worked without image perception. All decisions come from Pillow pixel "
                         "measurements and Aseprite Lua authoring; no artifact was 'seen'."),
}

clip["v7AxillaRepair"] = {
    "scope": "body layer, front_l/Sword, frames 3 and 4 only",
    "edits": {"3": 9, "4": 10, "total": 19},
    "defectsAddressed": [
        "D1 flat ink plate: x=147 y117..122 held one single colour rgb(12,15,18) in both frames "
        "(plus (148,116) in both and (149,115) in F04); every untouched contour pixel in the same frames "
        "varies between 0,0,1 / 2,2,3 / 6,6,8 / 20,20,26 / 27,28,34",
        "D2 retrograde step at y=123: left boundary width sequence was 147,147,...,147 (y117..y122), "
        "148 (y123), 147 (y124) in both frames - the opening narrowed by 1 px then widened again",
        "D3 detached pixel (149,122) rgb(95,96,99) with zero opaque 8-neighbours in F03",
        "D4 comb tooth (152,115) rgb(77,79,82) in F04: a 1 px island between the 2 px pinhole "
        "(150..151) created by V6 and the main opening (153..162); only its top edge touched the body",
    ],
    "notChanged": [
        "opening extent on the right side and below y=125",
        "pose, silhouette above y=115, timing 730 ms / 13 frames",
        "weaponBack / weaponFront / handFront pixels on all 13 frames",
        "every pixel of frames 0,1,2,5,6,7,8,9,10,11,12",
    ],
    "rule": ("Restore the native colour each repainted pixel held in the non-escalated V6 clip; where "
             "that would leave 3+ consecutive identical colours on the new medial edge, take the value the "
             "adjacent column (x+1) held on the same row. No colour is invented and no pixel is filled."),
    "verificationResult": {
        "byteIdenticalFilesOutsidePatch": verify["checks"]["byteIdenticalFiles"],
        "onlyDeclaredPixelsChanged": verify["checks"]["onlyDeclaredPixelsChanged"],
        "weaponAndHandLayersIdentical": verify["checks"]["weaponAndHandLayersIdentical"],
        "monotoneLeftBoundary": verify["checks"]["monotoneLeftBoundary"],
        "danglingPixels": verify["checks"]["danglingPixels"],
    },
    "residualRisk": ("The medial edge of the opening still runs at x=147 for nine consecutive rows "
                     "(y117..y125). Vertical runs of that length also exist in the untouched frames "
                     "(F05 x=146 y123..129), so this was treated as the V6 author's opening choice and not "
                     "re-cut. Only the colour plate, the notch and the detached pixels were repaired."),
    "visualReviewRequired": True,
}

clip["bodyRgbaDeltaReference"] = rel(os.path.join(V6PLAIN, "clip.json"))

with open(CLIP, "w", encoding="utf-8", newline="\n") as f:
    json.dump(clip, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("clip.json rewritten")
print("plain deltas:", {k: v for k, v in plain_counts.items() if v})
print("clipSha256:", sha(CLIP))
