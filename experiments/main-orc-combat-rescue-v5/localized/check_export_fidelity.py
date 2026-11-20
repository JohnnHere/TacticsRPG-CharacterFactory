from PIL import Image
import os

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)
ED = "characters/orc-v1/source/combat-rescue-v5/localized/frames"
ORIG_CLIP = "characters/orc-v1/source/rear-recovery-v2/back_l/Walk"

def load(p):
    return Image.open(p).convert("RGBA")

print("=== Compare Aseprite-exported fixed frames vs original composite PNGs ===")
print("(For unmodified frames F0-F3 they should be IDENTICAL)")
all_same = True
for i in range(8):
    fx = load(f"{ED}/f{i:02d}.png")
    oc = load(f"{ORIG_CLIP}/{i:02d}.png")
    if fx.size != oc.size:
        print(f"F{i}: SIZE MISMATCH export={fx.size} orig={oc.size}")
        all_same = False
        continue
    pa=fx.load(); pb=oc.load()
    diffs=0
    first=None
    for y in range(128):
        for x in range(128):
            if pa[x,y]!=pb[x,y]:
                diffs+=1
                if first is None:
                    first=(x,y,pa[x,y],pb[x,y])
    mark = " IDENTICAL" if diffs==0 else " DIFFERS"
    if diffs>0:
        all_same=False
    print(f"F{i}: {diffs} px differ {mark}  first={first}")
print("\nALL IDENTICAL:", all_same)
