from PIL import Image
import os

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)
ED = "characters/orc-v1/source/combat-rescue-v5/localized/frames"
ORIG_CLIP = "characters/orc-v1/source/rear-recovery-v2/back_l/Walk"

def load(p):
    return Image.open(p).convert("RGBA")

fixed = [load(f"{ED}/f{i:02d}.png") for i in range(8)]
orig = [load(f"{ORIG_CLIP}/{i:02d}.png") for i in range(8)]

# Native arm regions (composite arm y[70,100] -> native y[6,36]; composite x right[128,146]->native[64,82]; left[108,126]->native[44,62])
RARM = (64, 83, 6, 37)   # x0,x1,y0,y1 native
LARM = (44, 63, 6, 37)

def region_diff(a, b, reg):
    x0,x1,y0,y1 = reg
    pa=a.load(); pb=b.load(); n=0
    for y in range(y0,y1):
        for x in range(x0,x1):
            va=pa[x,y]; vb=pb[x,y]
            if va[3]>0 and vb[3]>0 and va!=vb:
                n+=1
    return n

print("=== RIGHT arm native x[64,83) y[6,37]: BEFORE vs AFTER half-cycle diff ===")
for i in range(4):
    j=i+4
    b = region_diff(orig[i], orig[j], RARM)
    a = region_diff(fixed[i], fixed[j], RARM)
    print(f"F{i:02d}/F{j:02d}: before={b:4d}  after={a:4d}  {'FIXED' if a < b else 'UNCHANGED'}")
print()
print("=== LEFT arm native x[44,63) y[6,37] ===")
for i in range(4):
    j=i+4
    b = region_diff(orig[i], orig[j], LARM)
    a = region_diff(fixed[i], fixed[j], LARM)
    print(f"F{i:02d}/F{j:02d}: before={b:4d}  after={a:4d}  {'FIXED' if a < b else 'UNCHANGED'}")

print()
print("=== Non-arm torso region native x[60,68) y[40,70] should be UNCHANGED ===")
for i in range(8):
    ov = orig[i].load()[64, 55]
    fv = fixed[i].load()[64, 55]
    mark = " <-- CHANGED!" if ov != fv else ""
    print(f"  F{i} (64,55): before={ov} after={fv}{mark}")
