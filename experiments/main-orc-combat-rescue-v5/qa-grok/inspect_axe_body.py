"""Read-only QA inspection of qa5-repair1 back_r/Axe body layers."""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory")
CLIP = ROOT / "characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/back_r/Axe/clip.json"
OUT = ROOT / "experiments/main-orc-combat-rescue-v5/qa-grok/evidence"
OUT.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load(rel: str) -> Image.Image:
    return Image.open(ROOT / rel).convert("RGBA")


def opaque(px, x, y):
    return px[x, y][3] > 0


def main():
    clip_hash = sha256(CLIP)
    clip = json.loads(CLIP.read_text(encoding="utf-8"))
    report = {
        "clipSha256": clip_hash,
        "declaredCheckpointSha": "ae5ecf1c313e8bebfde96bf8dd687ced4f10699cf075b1e2508c1dd723cf269e",
        "clipShaMatchesCheckpoint": clip_hash == "ae5ecf1c313e8bebfde96bf8dd687ced4f10699cf075b1e2508c1dd723cf269e",
        "frameCount": clip["frameCount"],
        "durationsMs": clip["durationsMs"],
        "visibleInterval": clip["visibleInterval"],
        "frames": [],
    }
    for key in (
        "bodyMaster",
        "bodyMaster256",
        "nativeMaster",
        "nativeMaster128",
        "master",
        "master256",
        "nativeStrip",
        "compositeStrip",
    ):
        rel = clip[key]
        digest = sha256(ROOT / rel)
        declared = clip.get(key + "Sha256")
        report[key] = {"path": rel, "sha256": digest, "declared": declared, "match": digest == declared}

    bodies = []
    natives = []
    for fr in clip["frames"]:
        body = load(fr["layers"]["body"]["png"])
        native = load(fr["nativePng"])
        root_png = load(fr["png"])
        body_sha = sha256(ROOT / fr["layers"]["body"]["png"])
        native_sha = sha256(ROOT / fr["nativePng"])
        w, h = body.size
        px = body.load()
        # native must equal center crop 64,64,128,128 of body
        crop = body.crop((64, 64, 192, 192))
        crop_match = list(crop.getdata()) == list(native.getdata())
        root_eq_body = list(root_png.getdata()) == list(body.getdata())
        bright = 0
        green = []
        opaque_n = 0
        min_y = 999
        max_y = -1
        # right-side raised pixels: x>=150 on 256 canvas (anatomical right, screen right)
        right_top = None
        left_col_changed = 0
        low_changed = 0
        total_changed = 0
        brown = 0
        # axe-like isolated bright steel is not used; count saturated brown shaft-like pixels
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if a == 0:
                    continue
                opaque_n += 1
                min_y = min(min_y, y)
                max_y = max(max_y, y)
                if r > 190 and g > 190 and b > 190:
                    bright += 1
                if g > r + 18 and g > b + 12 and g > 70:
                    green.append((x, y))
                if x >= 150 and (right_top is None or y < right_top[1]):
                    right_top = (x, y)
                if r > 40 and r > g + 12 and r > b + 8 and g < 90 and b < 70:
                    brown += 1
        scalp_top = min((y for _, y in green), default=None)
        scalp_span = None
        if green:
            scalp_span = [
                min(x for x, _ in green),
                min(y for _, y in green),
                max(x for x, _ in green),
                max(y for _, y in green),
            ]
        # hand above crown: opaque non-green pixel with y < scalp_top and x > scalp right edge - 4
        above = []
        if scalp_top is not None:
            for y in range(scalp_top):
                for x in range(w):
                    r, g, b, a = px[x, y]
                    if a and not (g > r + 18 and g > b + 12 and g > 70):
                        above.append((x, y, (r, g, b)))
        bodies.append(body)
        natives.append(native)
        # overlay emptiness is noted, not judged
        overlays = {}
        for name in ("weaponBack", "weaponFront", "handFront"):
            im = load(fr["layers"][name]["png"])
            n = sum(1 for p in im.getdata() if p[3])
            overlays[name] = n
        report["frames"].append(
            {
                "index": fr["index"],
                "phase": fr["phase"],
                "durationMs": fr["durationMs"],
                "bodySha": body_sha,
                "bodyShaMatch": body_sha == fr["layers"]["body"]["sha256"],
                "nativeSha": native_sha,
                "nativeShaMatch": native_sha == fr["nativeSha256"],
                "bodySize": [w, h],
                "nativeSize": list(native.size),
                "nativeEqualsBodyCrop64": crop_match,
                "rootPngEqualsBody": root_eq_body,
                "opaque": opaque_n,
                "bboxBottom": max_y,
                "brightOver190": bright,
                "brownish": brown,
                "scalpTopY": scalp_top,
                "scalpSpan": scalp_span,
                "rightmostColumnTop": right_top,
                "pixelsAboveScalp": len(above),
                "aboveScalpSample": above[:8],
                "overlayOpaque": overlays,
            }
        )

    f0 = bodies[0].load()
    for i, body in enumerate(bodies):
        if i == 0:
            report["frames"][i]["diffVsF00"] = {"total": 0, "leftXlt90": 0, "lowerYge194": 0}
            continue
        px = body.load()
        total = left = low = 0
        w, h = body.size
        for y in range(h):
            for x in range(w):
                if px[x, y] != f0[x, y]:
                    total += 1
                    if x < 90:
                        left += 1
                    if y >= 194:
                        low += 1
        report["frames"][i]["diffVsF00"] = {
            "total": total,
            "leftXlt90": left,
            "lowerYge194": low,
        }

    # connectivity of anatomical right arm: flood from a shoulder seed on screen-right torso
    # seed chosen per frame by scanning x=150..190, y=90..110 for opaque
    chain = []
    for i, body in enumerate(bodies):
        px = body.load()
        w, h = body.size
        seed = None
        for y in range(88, 112):
            for x in range(140, 175):
                if px[x, y][3]:
                    seed = (x, y)
                    break
            if seed:
                break
        if not seed:
            chain.append({"frame": i, "seed": None})
            continue
        seen = set()
        stack = [seed]
        minx = miny = 999
        maxx = maxy = -1
        while stack:
            x, y = stack.pop()
            if (x, y) in seen or x < 0 or y < 0 or x >= w or y >= h or px[x, y][3] == 0:
                continue
            seen.add((x, y))
            minx, miny = min(minx, x), min(miny, y)
            maxx, maxy = max(maxx, x), max(maxy, y)
            stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
        # components of opaque pixels with x>=130 that are NOT in the body flood
        extra = []
        visited = set()
        for y in range(h):
            for x in range(130, w):
                if px[x, y][3] == 0 or (x, y) in seen or (x, y) in visited:
                    continue
                comp = []
                st = [(x, y)]
                while st:
                    cx, cy = st.pop()
                    if (cx, cy) in visited or cx < 130 or cy < 0 or cx >= w or cy >= h or px[cx, cy][3] == 0:
                        continue
                    visited.add((cx, cy))
                    comp.append((cx, cy))
                    st.extend(((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)))
                if len(comp) >= 4:
                    xs = [p[0] for p in comp]
                    ys = [p[1] for p in comp]
                    extra.append({"n": len(comp), "bbox": [min(xs), min(ys), max(xs), max(ys)]})
        chain.append(
            {
                "frame": i,
                "seed": seed,
                "component": len(seen),
                "bbox": [minx, miny, maxx, maxy],
                "detachedRightClustersGe4": extra,
            }
        )
    report["rightArmConnectivity"] = chain

    # sheets: body 3x, arm zoom 4x from 256, lower body 3x
    sheet = Image.new("RGB", (8 * 128 * 3 + 16, 128 * 3 + 28), (18, 20, 24))
    arm = Image.new("RGB", (8 * 160 * 2 + 16, 180 * 2 + 28), (18, 20, 24))
    low = Image.new("RGB", (8 * 128 * 3 + 16, 80 * 3 + 28), (18, 20, 24))
    draw_s = ImageDraw.Draw(sheet)
    draw_a = ImageDraw.Draw(arm)
    draw_l = ImageDraw.Draw(low)
    for i, body in enumerate(bodies):
        native = body.crop((64, 64, 192, 192))
        z = native.resize((128 * 3, 128 * 3), Image.NEAREST)
        sheet.paste(z, (8 + i * 128 * 3, 24))
        draw_s.text((8 + i * 128 * 3, 4), f"F{i:02d} body-crop", fill=(220, 220, 220))
        # right arm window on 256: x 120-230, y 40-170
        crop_a = body.crop((110, 40, 230, 180))
        za = crop_a.resize((120 * 2, 140 * 2), Image.NEAREST)
        arm.paste(za, (8 + i * 160 * 2, 24))
        draw_a.text((8 + i * 160 * 2, 4), f"F{i:02d} arm", fill=(220, 220, 220))
        crop_l = native.crop((0, 48, 128, 128))
        zl = crop_l.resize((128 * 3, 80 * 3), Image.NEAREST)
        low.paste(zl, (8 + i * 128 * 3, 24))
        draw_l.text((8 + i * 128 * 3, 4), f"F{i:02d} hips", fill=(220, 220, 220))
    sheet.save(OUT / "axe_body_layers_off.png")
    arm.save(OUT / "axe_body_arm_zoom.png")
    low.save(OUT / "axe_body_lower.png")

    # F05-F07-F00 contact sheet at 4x native
    seq = Image.new("RGB", (4 * 128 * 4 + 20, 128 * 4 + 28), (18, 20, 24))
    ds = ImageDraw.Draw(seq)
    for j, i in enumerate((5, 6, 7, 0)):
        native = bodies[i].crop((64, 64, 192, 192)).resize((128 * 4, 128 * 4), Image.NEAREST)
        seq.paste(native, (8 + j * 128 * 4, 24))
        ds.text((8 + j * 128 * 4, 4), f"F{i:02d}", fill=(230, 230, 210))
    seq.save(OUT / "axe_body_recovery.png")

    (OUT / "axe_body_metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({
        "clipSha": clip_hash,
        "match": report["clipShaMatchesCheckpoint"],
        "masters": {k: report[k]["match"] for k in ("bodyMaster", "nativeMaster", "master", "nativeStrip")},
        "frames": [
            {
                "i": f["index"],
                "phase": f["phase"],
                "sha": f["bodyShaMatch"] and f["nativeShaMatch"] and f["nativeEqualsBodyCrop64"],
                "bright": f["brightOver190"],
                "above": f["pixelsAboveScalp"],
                "scalp": f["scalpTopY"],
                "rightTop": f["rightmostColumnTop"],
                "brown": f["brownish"],
                "diff": f["diffVsF00"],
                "overlays": f["overlayOpaque"],
                "detached": chain[f["index"]]["detachedRightClustersGe4"],
            }
            for f in report["frames"]
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
