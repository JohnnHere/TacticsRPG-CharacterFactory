from PIL import Image
import os
from collections import Counter

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)

def load(p):
    return Image.open(p).convert("RGBA")

print("=" * 70)
print("back_r Walk: right arm x=137 composite — look for bright outlier like back_l's (184,186,185)")
print("=" * 70)
clip = "characters/orc-v1/source/rear-recovery-v2/back_r/Walk"
frames = [load(f"{clip}/{i:02d}.png") for i in range(8)]
for i in range(8):
    px = frames[i].load()
    br = [(x,y,px[x,y]) for y in range(70,90) for x in range(135,143) if px[x,y][3]==255 and sum(px[x,y][:3])>450]
    if br:
        print(f"F{i:02d}: right-arm bright={br}")
print("(no output above = no bright outliers)")

print()
print("=" * 70)
print("back_r Walk: half-cycle right-arm same-geometry color diff count (composite x>=130)")
print("=" * 70)
for i in range(4):
    j=i+4
    pa=frames[i].load(); pb=frames[j].load()
    diffs=[]
    for y in range(128):
        for x in range(130,148):
            va=pa[x,y]; vb=pb[x,y]
            if va[3]>0 and vb[3]>0 and va!=vb:
                diffs.append((x,y,va,vb))
    c=Counter((va,vb) for (_,_,va,vb) in diffs)
    top=c.most_common(3)
    print(f"F{i:02d}/F{j:02d}: {len(diffs)} diffs  top={top}")

print()
print("=" * 70)
print("front_r Walk cloth: are bright highlights (231,230,227) at SAME coords across half-cycle (motion or flicker)?")
print("If cloth moves with legs, coords change -> genuine motion, KEEP.")
print("=" * 70)
clip = "characters/orc-v1/source/complete-v1/front_r/Walk"
frames = [load(f"{clip}/{i:02d}.png") for i in range(16)]
# Track bright pixel coords (231,230,227) in cloth zone x[126,132) y[100,133)
for i in range(16):
    px = frames[i].load()
    br = [(x,y) for y in range(100,133) for x in range(126,132) if px[x,y]==(231,230,227,255)]
    print(f"F{i:02d}: bright coords={br}")
