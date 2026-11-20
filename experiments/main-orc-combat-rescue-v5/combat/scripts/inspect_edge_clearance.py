from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")
RAW_DIR = ROOT / "experiments/main-orc-combat-rescue-v5/combat/raw"

jobs = [
    ("back_r_sword_v1", 7),
    ("back_l_sword_v1", 7),
    ("back_r_axe_v1",   7),
    ("back_l_axe_v1",   7),
    ("back_r_unarmed_v1", 4),
    ("back_l_unarmed_v1", 4),
]

for tag, n in jobs:
    print(f"=== {tag} ===")
    for i in range(n):
        im = np.array(Image.open(RAW_DIR / tag / f"{i:02d}.png").convert("RGBA"))
        vis = im[:, :, 3] > 0
        ys, xs = np.where(vis)
        top_touch = int(np.sum(vis[0, :]))
        left_touch = int(np.sum(vis[:, 0]))
        right_touch = int(np.sum(vis[:, 127]))
        bot_touch = int(np.sum(vis[127, :]))
        print(f"  raw {i:02d} (F0{i+1}): bbox=[{xs.min()},{ys.min()}..{xs.max()},{ys.max()}] edge_touch=(top:{top_touch}, left:{left_touch}, right:{right_touch}, bot:{bot_touch})")
