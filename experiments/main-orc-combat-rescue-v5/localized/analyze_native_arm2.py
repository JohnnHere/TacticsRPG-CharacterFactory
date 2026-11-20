from PIL import Image
import os
from collections import Counter

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)
ED = "tmp/opencode_export"

def load(p):
    return Image.open(p).convert("RGBA")

frames = [load(f"{ED}/native_backl_f{i:02d}.png") for i in range(8)]

# Find arm pixels in frame 0: opaque pixels on right side (x>65) and left side (x<62) in mid-upper body
px0 = frames[0].load()
print("Right-side (x>65) opaque pixels in F0, grouped by y:")
rows = {}
for y in range(128):
    cnt = sum(1 for x in range(66, 128) if px0[x,y][3] > 0)
    if cnt > 0:
        rows[y] = cnt
ys = sorted(rows.items())
print(ys[:30])

print()
print("Left-side (x<62) opaque pixels in F0, grouped by y:")
rowsL = {}
for y in range(128):
    cnt = sum(1 for x in range(0, 62) if px0[x,y][3] > 0)
    if cnt > 0:
        rowsL[y] = cnt
ysL = sorted(rowsL.items())
print(ysL[:30])
