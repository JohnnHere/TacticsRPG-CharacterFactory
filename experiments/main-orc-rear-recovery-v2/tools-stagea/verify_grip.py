#!/usr/bin/env python3
"""Stage A: grip connectivity + weapon visibility in the COMPOSITE (real cause test).

For every weapon-clip frame:
  weaponVisiblePct  = weapon-layer opaque px still visible in the composite
                      (low % => blade occluded by body / drawn behind torso)
  armNearHandPct    = body-layer opaque px touching a 3px dilation of the
                      handFront glove (low % => arm does not reach the grip)
"""
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "characters/orc-v1/source/complete-v1"
OUT = ROOT / "experiments/main-orc-rear-recovery-v2/diagnosis"

TARGETS = [(d, a) for d in ("back_r", "back_l", "front_r", "front_l")
           for a in ("Sword", "Axe")]


def alpha(im, thr=8):
    return im.getchannel("A").point(lambda v: 255 if v > thr else 0)


def dilate(mask, r=3):
    w, h = mask.size
    src = mask.load()
    out = mask.copy()
    op = out.load()
    for y in range(h):
        for x in range(w):
            if src[x, y]:
                for dy in range(-r, r + 1):
                    yy = y + dy
                    if 0 <= yy < h:
                        for dx in range(-r, r + 1):
                            xx = x + dx
                            if 0 <= xx < w:
                                op[xx, yy] = 255
    return out


def stats(path_weapon, path_comp, path_body, path_hand):
    wim = Image.open(path_weapon).convert("RGBA")
    cim = Image.open(path_comp).convert("RGBA")
    bim = Image.open(path_body).convert("RGBA")
    wa = alpha(wim)
    if wa.getbbox() is None:
        return None
    ca = alpha(cim)
    ba = alpha(bim)
    # weapon pixels visible in composite: weapon opaque AND composite color equals
    # weapon color at that pixel (composite keeps weapon where not covered by body)
    wp = wim.load(); cp = cim.load(); bp = bim.load()
    wcount = visible = 0
    for y in range(256):
        for x in range(256):
            if wp[x, y][3] > 8:
                wcount += 1
                c = cp[x, y]
                if c[3] > 8 and (c[0], c[1], c[2]) == (wp[x, y][0], wp[x, y][1], wp[x, y][2]):
                    visible += 1
    res = {"weaponPx": wcount,
           "weaponVisiblePct": round(100.0 * visible / max(wcount, 1), 1)}
    # arm connectivity to glove
    if path_hand and path_hand.exists():
        him = Image.open(path_hand).convert("RGBA")
        ha = alpha(him)
        hb = ha.getbbox()
        if hb is None:
            res["handPx"] = 0
        else:
            hp = ha.load(); bp2 = ba.load()
            hand_n = sum(1 for y in range(hb[1], hb[3])
                         for x in range(hb[0], hb[2]) if hp[x, y])
            res["handPx"] = hand_n
            grown = dilate(ha, 3)
            g = grown.load()
            touch = 0
            for y in range(256):
                for x in range(256):
                    if g[x, y] and bp2[x, y]:
                        touch += 1
            res["bodyNearHandPx"] = touch
            res["armReachRatio"] = round(touch / max(hand_n, 1), 2)
    return res


def main():
    report = {}
    for d, a in TARGETS:
        base = SRC / d / a / "Attack"
        if not base.exists():
            continue
        rows = []
        for f in sorted(base.glob("[0-9][0-9].png")):
            i = f.stem
            layers = base / "layers"
            hand = layers / "handFront" / f"{i}.png"
            # weapon layer: whichever is non-empty
            weapon = None
            for ln in ("weaponFront", "weaponBack"):
                p = layers / ln / f"{i}.png"
                if p.exists() and Image.open(p).convert("RGBA").getchannel("A").getbbox():
                    weapon = p
                    break
            body = layers / "body" / f"{i}.png"
            row = {"frame": int(i)}
            if weapon is None:
                row["note"] = "no weapon layer"
            else:
                row["weaponLayer"] = weapon.parent.name
                row.update(stats(weapon, f, body, hand if hand.exists() else None))
            rows.append(row)
        report[f"{d}/{a}"] = rows
    (OUT / "grip.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    for k, rows in report.items():
        print(f"== {k}")
        for r in rows:
            print("   ", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
