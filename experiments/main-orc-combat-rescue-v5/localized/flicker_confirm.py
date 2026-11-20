from PIL import Image
import os
from collections import Counter

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)

def load(p):
    return Image.open(p).convert("RGBA")

def diff_same_geometry(a, b):
    """Pixels where both frames are opaque (alpha>0 in both) but color differs."""
    pa = a.load(); pb = b.load()
    w, h = a.size
    diffs = []
    for y in range(h):
        for x in range(w):
            va = pa[x, y]; vb = pb[x, y]
            if va[3] > 0 and vb[3] > 0 and va != vb:
                diffs.append((x, y, va, vb))
    return diffs

print("=" * 70)
print("BACK_l WALK: half-cycle pair flicker (same pose, opaque pixels, color differs)")
print("=" * 70)
clip = "characters/orc-v1/source/rear-recovery-v2/back_l/Walk"
frames = [load(f"{clip}/{i:02d}.png") for i in range(8)]
for i in range(4):
    j = i + 4
    diffs = diff_same_geometry(frames[i], frames[j])
    # focus on right arm x>=130 and left arm x<=120
    right = [d for d in diffs if d[0] >= 130]
    left = [d for d in diffs if d[0] <= 120]
    center = [d for d in diffs if 121 <= d[0] <= 129]
    print(f"\nF{i:02d} vs F{j:02d}: total_samegeom_color_diff={len(diffs)}  rightArm={len(right)}  leftArm={len(left)}  center={len(center)}")
    # show right arm diffs (the confirmed flicker zone)
    if right:
        c = Counter((d[2], d[3]) for d in right)
        print(f"  Right-arm unique transitions (top 8):")
        for (va, vb), n in c.most_common(8):
            print(f"     {va} -> {vb}  x{n}")

print()
print("=" * 70)
print("FRONT_r WALK: cloth between-legs half-cycle flicker (x=126-131, y=100-132)")
print("=" * 70)
clip = "characters/orc-v1/source/complete-v1/front_r/Walk"
frames = [load(f"{clip}/{i:02d}.png") for i in range(16)]
for i in range(8):
    j = i + 8
    a = frames[i]; b = frames[j]
    pa = a.load(); pb = b.load()
    diffs = []
    for y in range(100, 132):
        for x in range(126, 132):
            va = pa[x, y]; vb = pb[x, y]
            if va[3] > 0 and vb[3] > 0 and va != vb:
                diffs.append((x, y, va, vb))
    print(f"F{i:02d} vs F{j:02d}: cloth-zone diffs={len(diffs)}")
    if diffs:
        c = Counter((d[2], d[3]) for d in diffs)
        for (va, vb), n in c.most_common(6):
            print(f"     {va} -> {vb}  x{n}")

print()
print("=" * 70)
print("FRONT_l WALK: cloth between-legs half-cycle flicker (x=122-129, y=100-132)")
print("=" * 70)
clip = "characters/orc-v1/source/complete-v1/front_l/Walk"
frames = [load(f"{clip}/{i:02d}.png") for i in range(16)]
for i in range(8):
    j = i + 8
    a = frames[i]; b = frames[j]
    pa = a.load(); pb = b.load()
    diffs = []
    for y in range(100, 132):
        for x in range(122, 130):
            va = pa[x, y]; vb = pb[x, y]
            if va[3] > 0 and vb[3] > 0 and va != vb:
                diffs.append((x, y, va, vb))
    print(f"F{i:02d} vs F{j:02d}: cloth-zone diffs={len(diffs)}")
    if diffs:
        c = Counter((d[2], d[3]) for d in diffs)
        for (va, vb), n in c.most_common(6):
            print(f"     {va} -> {vb}  x{n}")

print()
print("=" * 70)
print("DEFEAT: hands F02/F03 and terminal F04 — partial alpha + bright pixels")
print("=" * 70)
for direction, clip in [
    ("front_r", "characters/orc-v1/source/rear-recovery-v2/front_r/Defeat"),
    ("front_l", "characters/orc-v1/source/rear-recovery-v2/front_l/Defeat"),
]:
    print(f"\n--- {direction} Defeat ---")
    for fi in [2, 3, 4]:
        im = load(f"{clip}/{fi:02d}.png")
        px = im.load()
        partial = [(x, y, px[x, y]) for y in range(256) for x in range(256) if 0 < px[x, y][3] < 255]
        bright = [(x, y, px[x, y]) for y in range(256) for x in range(256) if px[x, y][3] == 255 and sum(px[x, y][:3]) > 600]
        print(f"  F{fi}: partial-alpha={len(partial)} bright(>600)={len(bright)}")
        if partial[:5]:
            print(f"    partial samples: {partial[:5]}")
        if bright[:5]:
            print(f"    bright samples: {bright[:5]}")
