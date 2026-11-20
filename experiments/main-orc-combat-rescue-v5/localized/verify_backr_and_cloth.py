from PIL import Image
import os
from collections import Counter

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)

def load(p):
    return Image.open(p).convert("RGBA")

print("=" * 70)
print("BACK_r Walk: right arm x=137 half-cycle consistency (should match F0/F4 etc.)")
print("=" * 70)
clip = "characters/orc-v1/source/rear-recovery-v2/back_r/Walk"
frames = [load(f"{clip}/{i:02d}.png") for i in range(8)]
for i in range(4):
    j = i + 4
    diffs = []
    for y in range(60, 100):
        va = frames[i].load()[137, y]; vb = frames[j].load()[137, y]
        if va[3] > 0 and vb[3] > 0 and va != vb:
            diffs.append((y, va, vb))
    print(f"F{i:02d} vs F{j:02d} x=137 right-arm opaque color diffs: {len(diffs)}")
    if diffs:
        c = Counter((va, vb) for (_, va, vb) in diffs)
        for (va, vb), n in c.most_common(5):
            print(f"    {va} -> {vb} x{n}")

print()
print("=" * 70)
print("FRONT_r Walk cloth: bright pixel (>200 sum) locations x=126-131 y=100-132")
print("=" * 70)
clip = "characters/orc-v1/source/complete-v1/front_r/Walk"
frames = [load(f"{clip}/{i:02d}.png") for i in range(16)]
for i in range(16):
    px = frames[i].load()
    br = [(x, y, px[x, y]) for y in range(100, 133) for x in range(126, 132) if px[x, y][3] == 255 and sum(px[x, y][:3]) > 560]
    if br:
        print(f"F{i:02d}: bright={br}")

print()
print("=" * 70)
print("FRONT_l Walk cloth: bright pixel (>200 sum) locations x=122-129 y=100-132")
print("=" * 70)
clip = "characters/orc-v1/source/complete-v1/front_l/Walk"
frames = [load(f"{clip}/{i:02d}.png") for i in range(16)]
for i in range(16):
    px = frames[i].load()
    br = [(x, y, px[x, y]) for y in range(100, 133) for x in range(122, 130) if px[x, y][3] == 255 and sum(px[x, y][:3]) > 560]
    if br:
        print(f"F{i:02d}: bright={br}")

print()
print("=" * 70)
print("back_l Walk: ALL bright pixels (>200 sum) in right arm x=135-142 y=60-100")
print("=" * 70)
clip = "characters/orc-v1/source/rear-recovery-v2/back_l/Walk"
frames = [load(f"{clip}/{i:02d}.png") for i in range(8)]
for i in range(8):
    px = frames[i].load()
    br = [(x, y, px[x, y]) for y in range(60, 101) for x in range(135, 143) if px[x, y][3] == 255 and sum(px[x, y][:3]) > 560]
    print(f"F{i:02d}: right-arm bright={br}")
