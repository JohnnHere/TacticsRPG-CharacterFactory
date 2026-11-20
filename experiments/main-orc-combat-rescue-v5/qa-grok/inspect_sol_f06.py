"""Read-only QA of grip-specialist front_r/Sword F06. No production edits."""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory")
REP = ROOT / "characters/orc-v1/source/combat-rescue-v5/grip-specialist/F06"
PARENT_BODY = ROOT / "characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword/layers/body/06.png"
OUT = ROOT / "experiments/main-orc-combat-rescue-v5/qa-grok/evidence"
OUT.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def rgba(im):
    return im.convert("RGBA")


def diff_count(a, b):
    pa, pb = a.load(), b.load()
    n = 0
    samples = []
    for y in range(a.size[1]):
        for x in range(a.size[0]):
            if pa[x, y] != pb[x, y]:
                n += 1
                if len(samples) < 12:
                    samples.append({"xy": [x, y], "a": list(pa[x, y]), "b": list(pb[x, y])})
    return n, samples


def flood(px, w, h, seed, pred):
    seen = set()
    stack = [seed]
    while stack:
        x, y = stack.pop()
        if (x, y) in seen or x < 0 or y < 0 or x >= w or y >= h or not pred(x, y):
            continue
        seen.add((x, y))
        stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return seen


def bbox(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return [min(xs), min(ys), max(xs), max(ys)] if pts else None


def main():
    rep_hash = sha256(REP / "representative.json")
    rep = json.loads((REP / "representative.json").read_text(encoding="utf-8"))
    body = rgba(Image.open(REP / "layers/body.png"))
    parent = rgba(Image.open(PARENT_BODY))
    hand = rgba(Image.open(REP / "layers/handFront.png"))
    wback = rgba(Image.open(REP / "layers/weaponBack.png"))
    wfront = rgba(Image.open(REP / "layers/weaponFront.png"))
    composite = rgba(Image.open(REP / "composite-256.png"))
    native = rgba(Image.open(REP / "composite-native-128.png"))
    body128 = rgba(Image.open(REP / "body-128.png"))

    declared = {
        "representative": "e9daacf07836ade4d66cd58a1cc97ffa25733001f535a50f9053ecbf2742ac1e",
        "composite": rep["frames"][0]["sha256"],
        "body": rep["frames"][0]["layers"]["body"]["sha256"],
        "hand": rep["frames"][0]["layers"]["handFront"]["sha256"],
        "weaponBack": rep["frames"][0]["layers"]["weaponBack"]["sha256"],
        "weaponFront": rep["frames"][0]["layers"]["weaponFront"]["sha256"],
        "native": rep["frames"][0]["compositeNativeSha256"],
        "body128": rep["frames"][0]["nativeSha256"],
    }
    actual = {
        "representative": rep_hash,
        "composite": sha256(REP / "composite-256.png"),
        "body": sha256(REP / "layers/body.png"),
        "hand": sha256(REP / "layers/handFront.png"),
        "weaponBack": sha256(REP / "layers/weaponBack.png"),
        "weaponFront": sha256(REP / "layers/weaponFront.png"),
        "native": sha256(REP / "composite-native-128.png"),
        "body128": sha256(REP / "body-128.png"),
    }
    body_delta, body_samples = diff_count(body, parent)
    crop = body.crop((64, 64, 192, 192))
    native_body_delta, _ = diff_count(crop, body128)

    # alpha-over check
    over = Image.new("RGBA", body.size, (0, 0, 0, 0))
    for layer in (wback, body, wfront, hand):
        over = Image.alpha_composite(over, layer)
    over_delta, _ = diff_count(over, composite)
    native_crop = composite.crop((64, 64, 192, 192))
    native_delta, _ = diff_count(native_crop, native)

    bp, hp, wp, fp = body.load(), hand.load(), wback.load(), wfront.load()
    w, h = body.size

    def opaque(px, x, y):
        return px[x, y][3] > 0

    # Brown glove cluster near claimed palm, 4-connected among brownish opaque body pixels.
    def brownish(x, y):
        r, g, b, a = bp[x, y]
        return a > 0 and r > 40 and r > g + 8 and r > b + 8 and g < 120

    glove_seed = None
    for y in range(109, 120):
        for x in range(152, 160):
            if brownish(x, y):
                glove_seed = (x, y)
                break
        if glove_seed:
            break
    glove = flood(bp, w, h, glove_seed, brownish) if glove_seed else set()

    # Steel-ish opaque near claimed forearm, then walk along connected body to see reach.
    def steelish(x, y):
        r, g, b, a = bp[x, y]
        return a > 0 and abs(r - g) < 18 and abs(g - b) < 18 and 40 < r < 170

    # Full body connectivity from a torso seed, then separate arm masses by cutting.
    # Trace the crossing arm by walking rightward from a left-shoulder seed along opaque pixels
    # in the chest band, recording the path, without using Sol's coordinates as a mask.
    chest_band = []
    for x in range(90, 175):
        col = [y for y in range(90, 140) if opaque(bp, x, y)]
        if col:
            chest_band.append({"x": x, "ymin": min(col), "ymax": max(col), "n": len(col)})

    # Two candidate hands: brown masses.
    brown_components = []
    visited = set()
    for y in range(80, 180):
        for x in range(80, 200):
            if (x, y) in visited or not brownish(x, y):
                continue
            comp = flood(bp, w, h, (x, y), brownish)
            visited |= comp
            if len(comp) >= 6:
                brown_components.append({"n": len(comp), "bbox": bbox(comp), "seed": [x, y]})

    # Connectivity of claimed palm pixel to claimed shoulder through ANY opaque body pixel.
    palm = (155, 114)
    shoulder = (118, 102)
    hip = (156, 142)
    cuff = (142, 115)

    def connected(a, b):
        if not opaque(bp, *a):
            # snap to nearest opaque within 3px
            for r in range(0, 4):
                for dy in range(-r, r + 1):
                    for dx in range(-r, r + 1):
                        p = (a[0] + dx, a[1] + dy)
                        if 0 <= p[0] < w and 0 <= p[1] < h and opaque(bp, *p):
                            a = p
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
        seen = flood(bp, w, h, a, lambda x, y: opaque(bp, x, y))
        return b in seen or any(abs(b[0] - x) <= 1 and abs(b[1] - y) <= 1 for x, y in seen), len(seen), a

    # The whole sprite is one connected component, so raw flood does not separate arms.
    # Separate by removing the torso core (x 96-130, y 96-150) and flooding the remaining right-side masses.
    torso_block = {(x, y) for x in range(100, 128) for y in range(96, 155) if opaque(bp, x, y)}

    def outside_torso(x, y):
        return opaque(bp, x, y) and (x, y) not in torso_block

    right_masses = []
    vis2 = set()
    for y in range(80, 190):
        for x in range(128, 190):
            if (x, y) in vis2 or not outside_torso(x, y):
                continue
            comp = flood(bp, w, h, (x, y), outside_torso)
            vis2 |= comp
            if len(comp) >= 8:
                right_masses.append({"n": len(comp), "bbox": bbox(comp)})

    # handFront stats
    hand_pts = [(x, y) for y in range(h) for x in range(w) if hp[x, y][3]]
    hand_on_body = 0
    hand_on_empty = 0
    hand_colors = {}
    for x, y in hand_pts:
        key = tuple(hp[x, y][:3])
        hand_colors[str(key)] = hand_colors.get(str(key), 0) + 1
        if bp[x, y][3]:
            hand_on_body += 1
        else:
            hand_on_empty += 1
    # new vs body color at same pixel
    recolored = []
    for x, y in hand_pts:
        if bp[x, y][3] and tuple(hp[x, y][:3]) != tuple(bp[x, y][:3]):
            recolored.append({"xy": [x, y], "body": list(bp[x, y]), "hand": list(hp[x, y])})

    # weapon pixels near palm
    def layer_pts(px):
        return [(x, y) for y in range(90, 160) for x in range(120, 200) if px[x, y][3]]

    wb_pts = layer_pts(wp)
    wf_pts = layer_pts(fp)
    # overlap of weaponFront with handFront and with body glove
    wf_under_hand = sum(1 for x, y in wf_pts if hp[x, y][3])
    wf_under_body = sum(1 for x, y in wf_pts if bp[x, y][3])
    wb_under_body = sum(1 for x, y in wb_pts if bp[x, y][3])
    wb_under_hand = sum(1 for x, y in wb_pts if hp[x, y][3])

    # visible weapon after body+hand occlusion, in grip window
    visible_guardish = []
    visible_leather = []
    for y in range(90, 160):
        for x in range(120, 210):
            # topmost visible of weapon layers if not covered by hand or body
            if hp[x, y][3] or bp[x, y][3]:
                continue
            src = None
            if fp[x, y][3]:
                src = fp[x, y]
                visible_guardish.append((x, y, src[:3]))
            elif wp[x, y][3]:
                src = wp[x, y]
                visible_leather.append((x, y, src[:3]))

    report = {
        "representativeSha256": rep_hash,
        "shaMatch": {k: actual[k] == declared[k] for k in declared},
        "actualSha": actual,
        "bodyRgbaDeltaVsParentF06": body_delta,
        "bodyDeltaSamples": body_samples,
        "nativeEqualsBodyCrop": native_body_delta == 0,
        "alphaOverMatchesComposite": over_delta == 0,
        "nativeEqualsCompositeCrop": native_delta == 0,
        "durationMs": rep["frames"][0]["durationMs"],
        "sourceFrameIndex": rep["frames"][0]["sourceFrameIndex"],
        "gloveSeed": glove_seed,
        "brownGloveComponent": {"n": len(glove), "bbox": bbox(glove)},
        "brownComponents": brown_components,
        "chestBand": chest_band[::4],
        "rightMassesOutsideTorsoCore": right_masses,
        "landmarksOpaque": {
            "palm155_114": list(bp[155, 114]),
            "wrist151_114": list(bp[151, 114]),
            "cuff142_115": list(bp[142, 115]),
            "forearm139_112": list(bp[139, 112]),
            "elbow128_110": list(bp[128, 110]),
            "shoulder118_102": list(bp[118, 102]),
            "hip156_142": list(bp[156, 142]),
            "firstPass157_112": list(bp[157, 112]),
        },
        "handFront": {
            "opaque": len(hand_pts),
            "bbox": bbox(hand_pts),
            "onBody": hand_on_body,
            "onEmpty": hand_on_empty,
            "recoloredVsBody": recolored,
            "colors": hand_colors,
        },
        "weaponNearGrip": {
            "weaponBack": {"n": len(wb_pts), "bbox": bbox(wb_pts), "underBody": wb_under_body, "underHand": wb_under_hand},
            "weaponFront": {"n": len(wf_pts), "bbox": bbox(wf_pts), "underBody": wf_under_body, "underHand": wf_under_hand},
            "visibleWeaponFrontNotCovered": len(visible_guardish),
            "visibleWeaponBackNotCovered": len(visible_leather),
        },
    }
    (OUT / "sol_f06_metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    # Untinted sheets.
    # 1. native 128 at 4x, body and composite, no labels tint
    sheet = Image.new("RGB", (128 * 4 * 2 + 24, 128 * 4 + 8), (16, 18, 22))
    sheet.paste(body128.resize((512, 512), Image.NEAREST), (4, 4))
    sheet.paste(native.resize((512, 512), Image.NEAREST), (520, 4))
    sheet.save(OUT / "sol_f06_native128_4x.png")

    # 2. grip window untinted: body, weaponBack, weaponFront, hand, composite at 10x
    box = (130, 90, 190, 155)
    layers = [body, wback, wfront, hand, composite]
    zoom = Image.new("RGB", (5 * 60 * 8 + 20, 65 * 8 + 8), (12, 12, 14))
    for i, im in enumerate(layers):
        crop_i = im.crop(box).resize((60 * 8, 65 * 8), Image.NEAREST)
        bg = Image.new("RGB", crop_i.size, (18, 20, 24))
        bg.paste(crop_i, mask=crop_i.split()[-1])
        zoom.paste(bg, (6 + i * 60 * 8, 4))
    zoom.save(OUT / "sol_f06_grip_untinted.png")

    # 3. arm trace sheet: body 6x of upper torso, plus a connectivity paint I will view
    arm = body.crop((70, 70, 190, 180))
    arm_z = arm.resize((120 * 6, 110 * 6), Image.NEAREST)
    bg = Image.new("RGB", arm_z.size, (16, 18, 22))
    bg.paste(arm_z, mask=arm_z.split()[-1])
    bg.save(OUT / "sol_f06_body_arms.png")

    # paint brown components and a horizontal scan of the crossing arm
    paint = body.crop((70, 70, 190, 180)).convert("RGBA")
    pp = paint.load()
    # mark brown glove component in the crop by leaving it, draw a 1px outline later in a side image
    mark = Image.new("RGBA", body.size, (0, 0, 0, 0))
    mp = mark.load()
    for x, y in glove:
        mp[x, y] = (220, 160, 40, 255)
    # second brown components that are not the glove
    for comp in brown_components:
        seed = tuple(comp["seed"])
        comp_pts = flood(bp, w, h, seed, brownish)
        if comp_pts == glove:
            continue
        for x, y in comp_pts:
            if mp[x, y][3] == 0:
                mp[x, y] = (80, 180, 220, 255)
    mark_crop = mark.crop((70, 70, 190, 180)).resize((120 * 6, 110 * 6), Image.NEAREST)
    # side by side body and marked
    pair = Image.new("RGB", (120 * 6 * 2 + 12, 110 * 6 + 8), (16, 18, 22))
    pair.paste(bg, (4, 4))
    marked_bg = bg.copy()
    marked_bg.paste(mark_crop, mask=mark_crop.split()[-1])
    pair.paste(marked_bg, (120 * 6 + 8, 4))
    pair.save(OUT / "sol_f06_arm_trace.png")

    print(json.dumps({
        "sha": rep_hash,
        "shaOk": all(report["shaMatch"].values()),
        "bodyDelta": body_delta,
        "over": over_delta,
        "native": native_delta,
        "glove": report["brownGloveComponent"],
        "brown": brown_components,
        "masses": right_masses,
        "landmarks": report["landmarksOpaque"],
        "hand": report["handFront"],
        "weapon": report["weaponNearGrip"],
    }, indent=2))


if __name__ == "__main__":
    main()
