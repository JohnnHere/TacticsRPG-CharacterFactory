"""
V7 ECON DEV - T1: numeric forensics of the reported "conspicuous white flash on the left side"
during playback of the rear Sword attack.

Method (no human visual perception available - everything below is measured):
  L = 0.2126R + 0.7152G + 0.0722B  (stored sRGB, 0..255)
  S = (max-min)/max
  LIGHT = alpha>=128 and L>=150 and S<=0.30
          The character palette tops out at L=177.7, so "white" here means the light neutral
          grey family (153..177), not 200+.
  FLASH METRIC (temporal isolation, motion tolerant):
          for frame i take the LIGHT mask, keep only pixels whose 5x5 neighbourhood contains
          no LIGHT pixel in BOTH neighbour frames (i-1 and i+1). Motion of the whole body is
          therefore tolerated up to +-2 px, so a "stable highlight that merely moves" scores 0
          while something that appears and disappears scores its full area.
  Also reported: raw LIGHT totals per half-canvas, so a strength collapse (highlight shrinks
  4x) is visible even when the feature itself persists.

Read-only. Nothing outside this folder is written.
"""
import hashlib
import json
import os
from collections import Counter, deque

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6")
LAYERS = ["weaponBack", "body", "weaponFront", "handFront"]
LIGHT_L = 150.0
LIGHT_S = 0.30
NEIGHBOURHOOD = 2


def lum(r, g, b):
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def sat(r, g, b):
    mx = max(r, g, b)
    return 0.0 if mx == 0 else (mx - min(r, g, b)) / mx


def load(p):
    with Image.open(p) as im:
        return im.convert("RGBA")


def px_of(p):
    return list(load(p).getdata())


def light_mask(px, w, h):
    return [a >= 128 and lum(r, g, b) >= LIGHT_L and sat(r, g, b) <= LIGHT_S for (r, g, b, a) in px]


def components(mask, w, h, min_px=1):
    seen = [False] * (w * h)
    out = []
    for s in range(w * h):
        if not mask[s] or seen[s]:
            continue
        q = deque([s])
        seen[s] = True
        pix = []
        while q:
            i = q.popleft()
            pix.append(i)
            y, x = divmod(i, w)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        j = ny * w + nx
                        if mask[j] and not seen[j]:
                            seen[j] = True
                            q.append(j)
        if len(pix) >= min_px:
            xs = [p % w for p in pix]
            ys = [p // w for p in pix]
            out.append(
                {
                    "indices": pix,
                    "count": len(pix),
                    "bbox": [min(xs), min(ys), max(xs), max(ys)],
                    "cx": sum(xs) / len(pix),
                    "cy": sum(ys) / len(pix),
                }
            )
    out.sort(key=lambda c: (-c["count"], c["bbox"]))
    return out


def describe(comp, px, w):
    cols = Counter(tuple(px[i]) for i in comp["indices"])
    dom, domn = cols.most_common(1)[0]
    return {
        "pixels": comp["count"],
        "bbox": comp["bbox"],
        "side": "left" if comp["cx"] < w / 2 else "right",
        "centroid": [round(comp["cx"], 1), round(comp["cy"], 1)],
        "dominantRgba": list(dom),
        "dominantShare": round(domn / comp["count"], 3),
        "colours": [[list(c), n] for c, n in cols.most_common(5)],
    }


def dilated(mask, w, h, r):
    out = [False] * (w * h)
    for idx, on in enumerate(mask):
        if not on:
            continue
        y, x = divmod(idx, w)
        for ny in range(max(0, y - r), min(h, y + r + 1)):
            base = ny * w
            for nx in range(max(0, x - r), min(w, x + r + 1)):
                out[base + nx] = True
    return out


def temporal_isolation(masks, i, w, h):
    """Light pixels at frame i with no light pixel within +-2 px in BOTH neighbours."""
    n = len(masks)
    prev = dilated(masks[i - 1], w, h, NEIGHBOURHOOD) if i - 1 >= 0 else [False] * (w * h)
    nxt = dilated(masks[i + 1], w, h, NEIGHBOURHOOD) if i + 1 < n else [False] * (w * h)
    out = [False] * (w * h)
    for idx in range(w * h):
        out[idx] = masks[i][idx] and not prev[idx] and not nxt[idx]
    return out


def analyse(clip_dir, label):
    cj = json.load(open(os.path.join(clip_dir, "clip.json"), encoding="utf-8"))
    n = cj["frameCount"]
    first = load(os.path.join(clip_dir, "frames", "00.png"))
    w, h = first.size

    frames = [px_of(os.path.join(clip_dir, "frames", "%02d.png" % i)) for i in range(n)]
    layer = {lay: [px_of(os.path.join(clip_dir, "layers", lay, "%02d.png" % i)) for i in range(n)] for lay in LAYERS}
    native = [px_of(os.path.join(clip_dir, "native", "%02d.png" % i)) for i in range(n)]
    nsize = load(os.path.join(clip_dir, "native", "00.png")).size

    body_masks = [light_mask(layer["body"][i], w, h) for i in range(n)]
    comp_masks = [light_mask(frames[i], w, h) for i in range(n)]
    weapon_px = []
    for i in range(n):
        row = []
        for idx in range(w * h):
            a = layer["weaponBack"][i][idx]
            b = layer["weaponFront"][i][idx]
            row.append(a if a[3] >= b[3] else b)
        weapon_px.append(row)
    weapon_masks = [
        [a or b for a, b in zip(light_mask(layer["weaponBack"][i], w, h), light_mask(layer["weaponFront"][i], w, h))]
        for i in range(n)
    ]

    palette_max = max(lum(*p[:3]) for f in frames for p in f if p[3] > 0)

    per_frame = []
    for i in range(n):
        iso = temporal_isolation(body_masks, i, w, h)
        iso_clusters = [describe(c, layer["body"][i], w) for c in components(iso, w, h, min_px=4)]
        all_clusters = [describe(c, layer["body"][i], w) for c in components(body_masks[i], w, h, min_px=4)]
        wclusters = [describe(c, weapon_px[i], w) for c in components(weapon_masks[i], w, h, min_px=4)]
        left = sum(1 for idx in range(w * h) if body_masks[i][idx] and idx % w < w // 2)
        right = sum(body_masks[i]) - left
        wleft = sum(1 for idx in range(w * h) if weapon_masks[i][idx] and idx % w < w // 2)
        wright = sum(weapon_masks[i]) - wleft
        per_frame.append(
            {
                "frame": i,
                "durationMs": cj["durationsMs"][i],
                "bodyLightPixels": {"left": left, "right": right, "total": left + right},
                "weaponLightPixels": {"left": wleft, "right": wright, "total": wleft + wright},
                "bodyLightClusters": all_clusters,
                "weaponLightClusters": wclusters,
                "temporallyIsolatedBodyLight": iso_clusters,
                "temporallyIsolatedBodyLightTotal": sum(c["pixels"] for c in iso_clusters),
            }
        )

    # body luminance means (style continuity check)
    lum_means = []
    for i in range(n):
        vals = [lum(*p[:3]) for p in layer["body"][i] if p[3] >= 128]
        lum_means.append(round(sum(vals) / len(vals), 2) if vals else None)

    # native (128) body crop check
    native_rows = []
    for i in range(n):
        m = light_mask(native[i], nsize[0], nsize[1])
        left = sum(1 for idx in range(nsize[0] * nsize[1]) if m[idx] and idx % nsize[0] < nsize[0] // 2)
        native_rows.append({"frame": i, "lightLeft": left, "lightTotal": sum(m)})

    # boundaries: strength collapse of the left-half body highlight
    bounds = []
    for i in range(n - 1):
        a = per_frame[i]["bodyLightPixels"]["left"]
        b = per_frame[i + 1]["bodyLightPixels"]["left"]
        bounds.append({"fromFrame": i, "toFrame": i + 1, "leftLightDelta": b - a, "ratio": round(b / a, 3) if a else None})

    return {
        "label": label,
        "clip": os.path.relpath(clip_dir, ROOT).replace("\\", "/"),
        "canvas": [w, h],
        "nativeCanvas": list(nsize),
        "frameCount": n,
        "durationsMs": cj["durationsMs"],
        "visibleInterval": cj.get("visibleInterval"),
        "layerOrder": cj.get("layerOrder"),
        "paletteMaxLuminance": round(palette_max, 2),
        "bodyMeanLuminancePerFrame": lum_means,
        "perFrame": per_frame,
        "nativeLightPerFrame": native_rows,
        "leftLightBoundaries": bounds,
        "bookendHashes": {
            "bodyF00Sha256": hashlib.sha256(open(os.path.join(clip_dir, "layers", "body", "00.png"), "rb").read()).hexdigest(),
            "bodyF11Sha256": hashlib.sha256(open(os.path.join(clip_dir, "layers", "body", "%02d.png" % (n - 1)), "rb").read()).hexdigest(),
        },
    }


def idle_compare(clip_dir, idle_dir, n):
    out = []
    for i, f in [(0, "00.png"), (n - 1, "%02d.png" % (n - 1))]:
        a = os.path.join(clip_dir, "layers", "body", f)
        b = os.path.join(idle_dir, "00.png")
        out.append(
            {
                "clipBody": os.path.relpath(a, ROOT).replace("\\", "/"),
                "idleBody": os.path.relpath(b, ROOT).replace("\\", "/"),
                "byteIdentical": hashlib.sha256(open(a, "rb").read()).hexdigest()
                == hashlib.sha256(open(b, "rb").read()).hexdigest(),
            }
        )
    return out


def main():
    clips = []
    for folder, label, idle in [
        ("back_l-sword", "back_l/Sword", os.path.join(ROOT, "characters", "orc-v1", "source", "complete-v1", "back_l", "Idle")),
        ("back_r-sword", "back_r/Sword", os.path.join(ROOT, "characters", "orc-v1", "source", "complete-v1", "back_r", "Idle")),
    ]:
        d = os.path.join(V6, "rear", folder)
        r = analyse(d, label)
        r["bookendVsIdle"] = idle_compare(d, idle, r["frameCount"])
        clips.append(r)

    mast = json.load(open(os.path.join(HERE, "master-vs-export.json"), encoding="utf-8"))
    master_ok = all(c["summary"]["masterMatchesExportedLayers"] for c in mast["clips"])

    candidates = []
    for c in clips:
        for row in c["perFrame"]:
            for k in row["temporallyIsolatedBodyLight"]:
                if k["pixels"] >= 8:
                    candidates.append(
                        {
                            "clip": c["label"],
                            "frame": row["frame"],
                            "durationMs": row["durationMs"],
                            "layer": "body",
                            "pixels": k["pixels"],
                            "bbox": k["bbox"],
                            "side": k["side"],
                            "dominantRgba": k["dominantRgba"],
                            "dominantShare": k["dominantShare"],
                            "colours": k["colours"],
                            "presentInPrev": False,
                            "presentInNext": False,
                            "metric": "temporally isolated light cluster (>=8 px, no light within +-2 px in either neighbour)",
                        }
                    )
        # bookend strength collapse of the left highlight
        rows = c["perFrame"]
        if rows[0]["bodyLightPixels"]["left"] >= 40:
            candidates.append(
                {
                    "clip": c["label"],
                    "frame": 0,
                    "durationMs": rows[0]["durationMs"],
                    "layer": "body",
                    "pixels": rows[0]["bodyLightPixels"]["left"],
                    "bbox": "aggregate: left-half body light",
                    "side": "left",
                    "dominantRgba": None,
                    "dominantShare": None,
                    "presentInPrev": None,
                    "presentInNext": rows[1]["bodyLightPixels"]["left"],
                    "metric": "left-half body LIGHT total collapses at the F00->F01 cut and recovers at F10->F11",
                    "detail": {
                        "F00_left": rows[0]["bodyLightPixels"]["left"],
                        "F01_left": rows[1]["bodyLightPixels"]["left"],
                        "F10_left": rows[-2]["bodyLightPixels"]["left"],
                        "F11_left": rows[-1]["bodyLightPixels"]["left"],
                        "clustersF00": [k for k in rows[0]["bodyLightClusters"] if k["side"] == "left"],
                        "clustersF01": [k for k in rows[1]["bodyLightClusters"] if k["side"] == "left"],
                    },
                }
            )
    candidates.sort(key=lambda c: -c["pixels"])

    payload = {
        "schemaVersion": 1,
        "task": "T1 - white-flash forensics, rear Sword attacks",
        "revision": "main-orc-combat-recovery-v7",
        "inputFreeze": {
            "manifest": "characters/orc-v1/source/artistic-reconstruction-v6/candidate28manifest.json",
            "manifestSha256": "5d68b52d3e2b2a0931d689afb5a9dd438c178835d05efb02a5fb2bcf0c64b7ca",
            "status": "V6 artistically REJECTED by the creator; this analysis is read-only and fixes nothing.",
        },
        "perceptionCaveat": "No images were available to this worker. Every statement is a numeric measurement; no claim of seeing the flash is made.",
        "thresholds": {
            "light": {"alphaMin": 128, "luminanceMin": LIGHT_L, "saturationMax": LIGHT_S},
            "isolationNeighbourhoodPx": NEIGHBOURHOOD,
            "clusterMinPx": 4,
            "candidateMinPx": 8,
        },
        "surfaceCheck": {
            "masterEqualsExportedLayers": master_ok,
            "detail": "experiments/main-orc-combat-recovery-v7/forensics/master-vs-export.json - fresh Aseprite export of the saved master compared pixel-by-pixel with layers/*.png and frames/*.png",
            "alphaOverRecompose": "0 differing pixels (see recompose check in report.md)",
            "conclusion": "The light structure is in the saved master, in the exported layer PNGs and in the composite alike: it is authored content, not an export or compositing artefact.",
        },
        "clips": clips,
        "candidates": candidates,
    }
    os.makedirs(HERE, exist_ok=True)
    with open(os.path.join(HERE, "white-flash.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("palette max L:", [c["paletteMaxLuminance"] for c in clips])
    for c in clips:
        print("\n###", c["label"], c["clip"])
        print("  bookend==idle:", c["bookendVsIdle"])
        for row in c["perFrame"]:
            iso = row["temporallyIsolatedBodyLightTotal"]
            print(
                "  F%02d %4dms bodyLightL/R=%3d/%3d weaponL/R=%3d/%3d iso=%3d meanL=%s"
                % (
                    row["frame"],
                    row["durationMs"],
                    row["bodyLightPixels"]["left"],
                    row["bodyLightPixels"]["right"],
                    row["weaponLightPixels"]["left"],
                    row["weaponLightPixels"]["right"],
                    iso,
                    c["bodyMeanLuminancePerFrame"][row["frame"]],
                )
            )
        print("  left-light boundaries:", [(b["fromFrame"], b["toFrame"], b["leftLightDelta"]) for b in c["leftLightBoundaries"]])
    print("\ncandidates (>=8px isolated, plus bookend aggregate):")
    for k in candidates:
        print("  ", k["clip"], "F%02d" % k["frame"], k["pixels"], k["bbox"], k["side"], k["dominantRgba"])
    print("wrote", os.path.join(HERE, "white-flash.json"))


if __name__ == "__main__":
    main()
