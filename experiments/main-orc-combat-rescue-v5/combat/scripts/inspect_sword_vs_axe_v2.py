from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")

print("=== 1. Comparing SwordR v2 vs AxeR v2 ===")
for i in range(8):
    fn = f"{i:02d}.png"
    sr = np.array(Image.open(ROOT / f"characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/native/{fn}").convert("RGBA"))
    ar = np.array(Image.open(ROOT / f"characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/native/{fn}").convert("RGBA"))
    sr_v4 = np.array(Image.open(ROOT / f"characters/orc-v1/source/rear-reconstruction-v4/back_r/Sword/native/{fn}").convert("RGBA"))
    print(f"  F{i:02d}: SwordR_v2 vs AxeR_v2 diff={int(np.sum(np.any(sr!=ar, axis=2)))}px | SwordR_v2 vs SwordR_v4 diff={int(np.sum(np.any(sr!=sr_v4, axis=2)))}px")

print("\n=== 2. Inspecting raw/pixellab-skeleton-v3/back_r (7 frames) vs back_r_axe (7 frames) ===")
for sub in ["back_r", "back_r_axe", "back_l", "back_l_axe"]:
    print(f"\nRaw {sub}:")
    for i in range(7):
        p = ROOT / f"experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/{sub}/{i:02d}.png"
        im = np.array(Image.open(p).convert("RGBA"))
        vis = im[:, :, 3] > 0
        xs = np.where(vis)[1]
        ys = np.where(vis)[0]
        # check right side x>=80 and left side x<=48
        r_pts = np.argwhere(vis[:, 80:])
        l_pts = np.argwhere(vis[:, :48])
        r_str = f"cnt={len(r_pts)} x=[{r_pts[:,1].min()+80}..{r_pts[:,1].max()+80}] y=[{r_pts[:,0].min()}..{r_pts[:,0].max()}]" if len(r_pts) else "none"
        l_str = f"cnt={len(l_pts)} x=[{l_pts[:,1].min()}..{l_pts[:,1].max()}] y=[{l_pts[:,0].min()}..{l_pts[:,0].max()}]" if len(l_pts) else "none"
        print(f"  [{i:02d}]: bbox=[{xs.min()},{ys.min()}..{xs.max()},{ys.max()}] | left(x<48): {l_str} | right(x>=80): {r_str}")
