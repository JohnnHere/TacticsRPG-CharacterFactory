"""Read-only coordinate measurement helper for Aseprite Lua scripts.
Does NOT write or modify any artwork PNGs."""
import json
import numpy as np
from pathlib import Path
from PIL import Image

ROOT = Path(r"c:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory")
EXP = ROOT / "experiments/main-orc-final-v10"

# 1. Measure V5 back_r right-arm fist positions in F05, F06, F07 (256x256 space)
for idx in [4, 5, 6, 7]:
    p = ROOT / f"characters/orc-v1/source/combat-rescue-v5/combat/back_r/Sword/layers/body/{idx:02d}.png"
    a = np.array(Image.open(p).convert("RGBA"))
    # find rightmost opaque pixels & leather pixels on x >= 150
    sub = a[85:175, 148:205]
    al = sub[:,:,3] > 0
    r, g, b = sub[:,:,0].astype(int), sub[:,:,1].astype(int), sub[:,:,2].astype(int)
    leather = al & (r >= 42) & (r - g >= 10) & (g - b >= 4)
    ys, xs = np.where(leather)
    ay, ax = np.where(al)
    print(f"V5 back_r Sword F{idx:02d}: arm x=[{ax.min()+148}..{ax.max()+148}] y=[{ay.min()+85}..{ay.max()+85}] | leather centroid=({xs.mean()+148:.1f}, {ys.mean()+85:.1f}) x=[{xs.min()+148}..{xs.max()+148}] y=[{ys.min()+85}..{ys.max()+85}]")

# 2. Measure raw_sword_nw (00..11) and raw_axe_nw (00..09) leather fist clusters in 256-space (+64,+64)
for sub_name, n in [("raw_sword_nw", 12), ("raw_axe_nw", 10)]:
    print(f"\n--- {sub_name} ---")
    for i in range(n):
        a = np.array(Image.open(EXP / "pixellab" / sub_name / f"{i:02d}.png").convert("RGBA"))
        al = a[:,:,3] > 0
        r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
        leather = al & (r >= 42) & (r <= 145) & (r - g >= 10) & (g - b >= 4)
        # Filter out left resting hand (which sits around 256-space x=89..100, y=132..148)
        mask_active = np.zeros_like(leather)
        for y in range(128):
            for x in range(128):
                gx, gy = x + 64, y + 64
                # Left resting hand is at gx <= 104 and gy >= 126
                if gx <= 105 and gy >= 125:
                    continue
                # Tassets red cloth is at gx in 102..152 and gy >= 134
                if 102 <= gx <= 152 and gy >= 134:
                    continue
                # Upper left red sleeve is at gx in 96..114 and gy in 104..118 (unless i in 5..8)
                if i not in (5, 6, 7, 8) and gx <= 118:
                    continue
                if leather[y, x]:
                    mask_active[y, x] = True
        ys, xs = np.where(mask_active)
        if len(xs) > 0:
            print(f"  {i:02d}: active_leather count={len(xs):3d} center=({xs.mean()+64:.1f}, {ys.mean()+64:.1f}) box=[{xs.min()+64}..{xs.max()+64}, {ys.min()+64}..{ys.max()+64}]")
        else:
            print(f"  {i:02d}: no distinct active_leather outside torso")
