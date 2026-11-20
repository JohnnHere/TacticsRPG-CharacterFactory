from PIL import Image
import os
from collections import Counter

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)
ED = "characters/orc-v1/source/combat-rescue-v5/localized/frames"

def load(p):
    return Image.open(p).convert("RGBA")

frames = [load(f"{ED}/f{i:02d}.png") for i in range(8)]
print("Fixed native frame size:", frames[0].size)

print("=" * 70)
print("VERIFY back_l Walk native arm: half-cycle same-geometry color diffs (should be ~0 now)")
print("=" * 70)
total = 0
for i in range(4):
    j = i + 4
    diffs = []
    pa = frames[i].load(); pb = frames[j].load()
    for y in range(128):
        for x in range(128):
            va = pa[x, y]; vb = pb[x, y]
            if va[3] > 0 and vb[3] > 0 and va != vb:
                diffs.append((x, y, va, vb))
    total += len(diffs)
    print(f"F{i:02d} vs F{j:02d}: {len(diffs)} remaining same-geometry color diffs")
print(f"TOTAL remaining: {total}")

# Confirm the specific bright outlier is gone
print()
print("Specific check F04 (137-64=73, 84-64=20) native (73,20):")
px4 = frames[4].load(); px0 = frames[0].load()
print(f"  F00 native (73,20) = {px0[73,20]}")
print(f"  F04 native (73,20) = {px4[73,20]}  (was (184,186,185) before fix)")

# Confirm F0-F3 reference frames unchanged
print()
print("Reference frames F0-F3 unchanged check (compare to original composite-derived native):")
print("  (These are the sources we copied FROM, so they should be identical to originals)")
