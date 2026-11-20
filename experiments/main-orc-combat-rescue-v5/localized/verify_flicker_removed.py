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

def full_colordiff(a, b):
    pa=a.load(); pb=b.load()
    n=0
    for y in range(128):
        for x in range(128):
            va=pa[x,y]; vb=pb[x,y]
            if va[3]>0 and vb[3]>0 and va!=vb:
                n+=1
    return n

def region_colordiff(imA, imB, x0,x1,y0,y1):
    pa=imA.load(); pb=imB.load(); n=0
    for y in range(y0,y1):
        for x in range(x0,x1):
            va=pa[x,y]; vb=pb[x,y]
            if va[3]>0 and vb[3]>0 and va!=vb:
                n+=1
    return n

print("Fixed frame size:", fixed[0].size)
print()
print("=== Right arm NATIVE region x[64,83) y[55,101): same-geometry color diffs ===")
print("pair        BEFORE(orig full)   AFTER(fixed right-arm)")
tot_before=0; tot_after=0
for i in range(4):
    j=i+4
    b = full_colordiff(orig[i], orig[j])
    af = region_colordiff(fixed[i], fixed[j], 64,83,55,101)
    tot_before+=b; tot_after+=af
    print(f"F{i:02d}/F{j:02d}  before={b:5d}   after={af:5d}")
print(f"TOTAL before={tot_before}  right-arm after={tot_after}")

print()
print("=== Left arm NATIVE region x[44,63) y[55,101) ===")
tot_after=0
for i in range(4):
    j=i+4
    af = region_colordiff(fixed[i], fixed[j], 44,63,55,101)
    tot_after+=af
    print(f"F{i:02d}/F{j:02d}  left-arm after={af:5d}")
print(f"TOTAL left-arm after={tot_after}")

print()
print("=== Specific bright outlier: native (73,20) across fixed frames ===")
for i in range(8):
    print(f"  F{i} fixed native(73,20) = {fixed[i].load()[73,20]}")

print()
print("=== Torso pixel (native 56,26) unchanged? ===")
for i in range(8):
    ov = orig[i].load()[120, 90]   # composite (120,90) = native (56,26)
    fv = fixed[i].load()[56, 26]
    mark = " <-- CHANGED!" if ov != fv else ""
    print(f"  F{i}: before={ov} after={fv}{mark}")
