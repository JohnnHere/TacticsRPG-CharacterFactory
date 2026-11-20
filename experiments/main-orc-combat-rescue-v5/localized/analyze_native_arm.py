from PIL import Image
import os
from collections import Counter

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)
ED = "tmp/opencode_export"

def load(p):
    return Image.open(p).convert("RGBA")

frames = [load(f"{ED}/native_backl_f{i:02d}.png") for i in range(8)]

print("Native frame size:", frames[0].size)
print("=" * 70)
print("back_l Walk NATIVE: right arm column x=73 half-cycle consistency")
print("=" * 70)
for i in range(4):
    j = i + 4
    diffs = []
    for y in range(0, 128):
        va = frames[i].load()[73, y]; vb = frames[j].load()[73, y]
        if va[3] > 0 and vb[3] > 0 and va != vb:
            diffs.append((y, va, vb))
    print(f"F{i:02d} vs F{j:02d} native x=73 right-arm opaque color diffs: {len(diffs)}")
    if diffs:
        c = Counter((va,vb) for (_,va,vb) in diffs)
        for (va,vb), n in c.most_common(4):
            print(f"    {va} -> {vb} x{n}")

print()
print("=" * 70)
print("back_l Walk NATIVE: find arm region (columns with opaque pixels in y range)")
print("=" * 70)
# For frame 0, find x columns that have substantial opaque pixels in upper body (y 20-60)
px0 = frames[0].load()
col_counts = []
for x in range(128):
    cnt = sum(1 for y in range(15, 60) if px0[x,y][3] > 0)
    if cnt > 5:
        col_counts.append((x, cnt))
col_counts.sort(key=lambda t: -t[1])
print("Top opaque columns in upper body F0:", col_counts[:12])
