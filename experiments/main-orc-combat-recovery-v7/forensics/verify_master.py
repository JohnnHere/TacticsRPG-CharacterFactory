"""
V7 ECON DEV / T1: compare a fresh Aseprite export of the saved master against the
committed layer/frame PNGs of the same clip (pixel-level, decoded RGBA).

Answers the question "is the defect in the saved master, in the exported PNG, or only
in the composite?" by separating the three surfaces.
"""
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6")
LAYERS = ["weaponBack", "body", "weaponFront", "handFront"]


def load(p):
    with Image.open(p) as im:
        return im.convert("RGBA")


def diff(path_a, path_b):
    a, b = load(path_a), load(path_b)
    if a.size != b.size:
        return {"sizeMismatch": [list(a.size), list(b.size)], "pixels": None}
    pa, pb = list(a.getdata()), list(b.getdata())
    n = 0
    maxerr = 0
    bbox = [9999, 9999, -1, -1]
    w = a.size[0]
    for i, (ca, cb) in enumerate(zip(pa, pb)):
        if ca != cb:
            n += 1
            maxerr = max(maxerr, max(abs(ca[k] - cb[k]) for k in range(4)))
            x, y = i % w, i // w
            bbox = [min(bbox[0], x), min(bbox[1], y), max(bbox[2], x), max(bbox[3], y)]
    return {
        "sizeMismatch": None,
        "pixels": n,
        "maxChannelError": maxerr,
        "bbox": None if n == 0 else bbox,
    }


def compare_clip(clip_dir, dump_dir):
    cj = json.load(open(os.path.join(clip_dir, "clip.json"), encoding="utf-8"))
    n = cj["frameCount"]
    out = {"clip": os.path.relpath(clip_dir, ROOT).replace("\\", "/"), "frames": [], "summary": {}}
    tot_bad = 0
    for i in range(n):
        row = {"frame": i, "layers": {}, "flatVsCommittedFrame": None}
        for lay in LAYERS:
            a = os.path.join(dump_dir, "layers", lay, "%02d.png" % i)
            b = os.path.join(clip_dir, "layers", lay, "%02d.png" % i)
            if not os.path.exists(a) or not os.path.exists(b):
                row["layers"][lay] = {"missing": True}
                continue
            d = diff(a, b)
            row["layers"][lay] = d
            if d["pixels"]:
                tot_bad += d["pixels"]
        flat = os.path.join(dump_dir, "flat", "%02d.png" % i)
        committed = os.path.join(clip_dir, "frames", "%02d.png" % i)
        if os.path.exists(flat) and os.path.exists(committed):
            row["flatVsCommittedFrame"] = diff(flat, committed)
            if row["flatVsCommittedFrame"]["pixels"]:
                tot_bad += row["flatVsCommittedFrame"]["pixels"]
        out["frames"].append(row)
    out["summary"]["layerMismatchPixelsTotal"] = tot_bad
    out["summary"]["masterMatchesExportedLayers"] = tot_bad == 0
    return out


def main():
    pairs = [
        ("back_l-sword", "back_l-sword"),
        ("back_r-sword", "back_r-sword"),
    ]
    results = []
    for folder, dump in pairs:
        clip_dir = os.path.join(V6, "rear", folder)
        dump_dir = os.path.join(HERE, "master-dump", dump)
        r = compare_clip(clip_dir, dump_dir)
        results.append(r)
        print("====", r["clip"], "mismatchPixelsTotal=", r["summary"]["layerMismatchPixelsTotal"])
        for row in r["frames"]:
            bits = ["%s=%s" % (k, (v.get("pixels") if not v.get("missing") else "MISSING")) for k, v in row["layers"].items()]
            print("   F%02d %s flat=%s" % (row["frame"], " ".join(bits), (row["flatVsCommittedFrame"] or {}).get("pixels")))
    out = os.path.join(HERE, "master-vs-export.json")
    json.dump({"schemaVersion": 1, "clips": results}, open(out, "w", encoding="utf-8"), indent=2)
    print("wrote", out)


if __name__ == "__main__":
    main()
