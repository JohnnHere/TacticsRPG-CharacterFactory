from PIL import Image
import os

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)

def load(p):
    return Image.open(p).convert("RGBA")

def sample(im, pts):
    px = im.load()
    return [px[x][y] if False else px[x, y] for (x, y) in pts]

print("=" * 70)
print("back_l Walk: right-arm edge column x=137-139 across all frames")
print("(half-cycle-apart frames F0/F4, F1/F5, etc. should MATCH if no flicker)")
print("=" * 70)
clip = "characters/orc-v1/source/rear-recovery-v2/back_l/Walk"
frames = [load(f"{clip}/{i:02d}.png") for i in range(8)]
pts = [(137, y) for y in range(70, 90)]
for i in range(8):
    vals = sample(frames[i], pts)
    # compress: print unique colors with count
    from collections import Counter
    c = Counter(vals)
    print(f"F{i:02d}: {dict(c)}")

print()
print("back_l Walk: compare F00 vs F04 at right arm x=137 y=70..89")
f0 = load(f"{clip}/00.png"); f4 = load(f"{clip}/04.png")
px0 = f0.load(); px4 = f4.load()
for y in range(70, 90):
    v0 = px0[137, y]; v4 = px4[137, y]
    mark = " <-- DIFF" if v0 != v4 else ""
    print(f"  y={y}: F00={v0}  F04={v4}{mark}")

print()
print("back_l Walk: compare F01 vs F05 at right arm x=137 y=70..89")
f1 = load(f"{clip}/01.png"); f5 = load(f"{clip}/05.png")
px1 = f1.load(); px5 = f5.load()
for y in range(70, 90):
    v1 = px1[137, y]; v5 = px5[137, y]
    mark = " <-- DIFF" if v1 != v5 else ""
    print(f"  y={y}: F01={v1}  F05={v5}{mark}")

print()
print("=" * 70)
print("front_r Walk: cloth between-legs column x=128-129 across all frames")
print("=" * 70)
clip = "characters/orc-v1/source/complete-v1/front_r/Walk"
frames = [load(f"{clip}/{i:02d}.png") for i in range(16)]
pts = [(128, y) for y in range(100, 130)]
for i in range(16):
    vals = sample(frames[i], pts)
    from collections import Counter
    c = Counter(vals)
    print(f"F{i:02d}: {dict(c)}")
