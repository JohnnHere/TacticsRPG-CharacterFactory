from pathlib import Path
from PIL import Image
import numpy as np

RAW_DIR = Path("experiments/main-orc-combat-rescue-v5/combat/raw")

for tag in ["back_r_sword_v1", "back_r_axe_v1", "back_l_sword_v1", "back_l_axe_v1"]:
    base_name = "back_r_base_128.png" if "back_r" in tag else "back_l_base_128.png"
    im0 = np.array(Image.open(RAW_DIR / base_name).convert("RGBA"))
    print(f"=== {tag} (vs {base_name}) ===")
    for idx in range(7):
        im = np.array(Image.open(RAW_DIR / tag / f"{idx:02d}.png").convert("RGBA"))
        vis = im[:, :, 3] > 0
        ys, xs = np.where(vis)
        if "back_r" in tag:
            off_diff = int(np.any(im[:, :46] != im0[:, :46], axis=2).sum())
        else:
            off_diff = int(np.any(im[:, 82:] != im0[:, 82:], axis=2).sum())
        print(f"  F0{idx+1} (raw {idx:02d}): bbox=({xs.min()},{ys.min()}..{xs.max()},{ys.max()}), off_hand_diff_vs_F00={off_diff}")
