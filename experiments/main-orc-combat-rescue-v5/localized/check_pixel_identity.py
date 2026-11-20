from PIL import Image
import os

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)

def load(p):
    return Image.open(p).convert("RGBA")

ORIG = "characters/orc-v1/source/rear-recovery-v2/back_l/Walk"
FIXED = "characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk"
print("Pixel-content comparison fixed vs orig composite (256x256):")
all_identical = True
for i in range(8):
    a = load(f"{ORIG}/{i:02d}.png")
    b = load(f"{FIXED}/{i:02d}.png")
    pa, pb = a.load(), b.load()
    diffs = 0
    for y in range(256):
        for x in range(256):
            if pa[x,y] != pb[x,y]:
                diffs += 1
    mark = "IDENTICAL" if diffs==0 else f"{diffs} px DIFFER"
    if diffs != 0:
        all_identical = False
    print(f"F{i:02d}: {mark}")
print("\nALL pixel-identical:", all_identical)
