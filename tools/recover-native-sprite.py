"""Reconstruct a newly authored sprite source; never use on concept/Hero art.

Uses MIT Pixel Art Fixer, pinned in tools/pixel-production.md. Explicit target
grid reconstruction is reported as forced, not as a detected/lossless grid.
No animation, mirroring, skeleton, or artistic approval is performed here.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from pixelfixer.api import process


def sha(data):
    return hashlib.sha256(data).hexdigest()


def recover(input_path, output_path, content_height=None, colors=48, palette_path=None, quiet=False, seed=42):
    input_path, output_path = Path(input_path), Path(output_path)
    if "concepts" in input_path.parts or "hero-reference" in input_path.parts:
        raise ValueError("Use a newly authored sprite source, not concept/Hero art.")
    original = input_path.read_bytes()
    arr = np.array(Image.open(io.BytesIO(original)).convert("RGBA"))
    mask = (arr[:, :, 3] >= 160).astype(np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    if count <= 1:
        raise ValueError("Empty source")
    main = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    kept = labels == main
    removed = int(np.count_nonzero(mask) - np.count_nonzero(kept))
    arr[~kept] = 0
    arr[kept, 3] = 255
    ys, xs = np.where(kept)
    bounds = [int(xs.min()), int(ys.min()), int(xs.max()+1), int(ys.max()+1)]
    arr = arr[bounds[1]:bounds[3], bounds[0]:bounds[2]].copy()
    options = {"k_colors": colors, "low_memory": True}
    if content_height:
        options["force_step"] = arr.shape[0] / content_height
    # The dependency seeds sampling but not cv2.kmeans' global RNG. Reset it
    # per asset so later rebuilds do not depend on prior quantization calls.
    cv2.setRNGSeed(seed)
    result = process(arr, **options)
    low = np.array(Image.open(io.BytesIO(result.pop("png"))).convert("RGBA"))
    low[:, :, 3] = np.where(low[:, :, 3] >= 128, 255, 0)
    low[low[:, :, 3] == 0] = 0
    opaque = low[:, :, 3] > 0
    # Palette reduction is explicit native-pixel finishing, not an alpha blur.
    pixels = low[:, :, :3][opaque]
    palette_record = None
    if palette_path:
        ref_bytes = Path(palette_path).read_bytes()
        ref = np.array(Image.open(io.BytesIO(ref_bytes)).convert("RGBA"))
        palette = np.unique(ref[ref[:, :, 3] > 0, :3], axis=0)
        if len(palette) > colors:
            raise ValueError("Reference palette exceeds color limit")
        lab = cv2.cvtColor(pixels.reshape(1, -1, 3).astype(np.float32)/255,
                           cv2.COLOR_RGB2Lab).reshape(-1, 3)
        pal_lab = cv2.cvtColor(palette.reshape(1, -1, 3).astype(np.float32)/255,
                               cv2.COLOR_RGB2Lab).reshape(-1, 3)
        indices = ((lab[:,None,:]-pal_lab[None,:,:])**2).sum(axis=2).argmin(axis=1)
        low[:, :, :3][opaque] = palette[indices]
        palette_record = {"file": str(palette_path), "sha256": sha(ref_bytes),
                          "colors": len(palette), "mapping": "nearest CIELAB"}
    else:
        palette_image = Image.fromarray(pixels.reshape(1, -1, 3)).quantize(
            colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        low[:, :, :3][opaque] = np.array(palette_image.convert("RGB")).reshape(-1, 3)
    ys, xs = np.where(opaque)
    low = low[ys.min():ys.max()+1, xs.min():xs.max()+1]
    h, w = low.shape[:2]
    if h > 126 or w > 126:
        raise ValueError(f"Recovered art {w}x{h} exceeds 128 canvas; no auto-resize")
    canvas = np.zeros((128, 128, 4), dtype=np.uint8)
    x, y = (128-w)//2, 127-h
    canvas[y:y+h, x:x+w] = low
    output_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(canvas).save(output_path)
    Image.fromarray(canvas).resize((512, 512), Image.Resampling.NEAREST).save(
        output_path.with_name(output_path.stem + "-4x.png"))
    report = {"source": str(input_path), "sourceSha256": sha(original), "opencvQuantizationSeed":seed,
              "output": str(output_path), "outputSha256": sha(output_path.read_bytes()),
              "method": "Pixel Art Fixer structural grid reconstruction + native palette finishing",
              "detector": result, "requestedContentHeight": content_height,
              "sourceCrop": bounds, "sourceDisconnectedOpaquePixelsRemoved": removed,
              "sourceAlphaThreshold": 160, "nativeAlphaThreshold": 128,
              "nativeContentSize": [w, h], "nativeOffset": [x, y],
              "paletteLimit": colors, "sharedPalette": palette_record,
              "nativeColors": len(np.unique(low[low[:,:,3]>0,:3],axis=0)),
              "partialAlphaPixels": int(np.count_nonzero((canvas[:,:,3]>0)&(canvas[:,:,3]<255))),
              "artisticApproval": "PENDING_CREATOR", "isHandDrawn": False}
    output_path.with_suffix(".json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if not quiet:
        print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--content-height", type=int)
    parser.add_argument("--colors", type=int, default=48)
    parser.add_argument("--palette", help="Reference native PNG for one shared palette")
    args = parser.parse_args()
    recover(args.input, args.output, args.content_height, args.colors, args.palette)
