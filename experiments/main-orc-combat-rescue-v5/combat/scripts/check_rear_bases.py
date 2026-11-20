import json
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")

# Let's check the base images used in rear-recovery-v2
for label, p in [
    ("back_r_Idle_00", ROOT / "characters/orc-v1/source/complete-v1/back_r/Idle/00.png"),
    ("back_l_Idle_00", ROOT / "characters/orc-v1/source/complete-v1/back_l/Idle/00.png"),
    ("back_r_base_rec", ROOT / "experiments/main-orc-complete-v1/pixellab-recovery/back_r_base.png"),
    ("back_l_base_rec", ROOT / "experiments/main-orc-complete-v1/pixellab-recovery/back_l_base.png"),
    ("v4_back_r_F00", ROOT / "characters/orc-v1/source/rear-reconstruction-v4/back_r/Sword/native/00.png"),
    ("v4_back_l_F00", ROOT / "characters/orc-v1/source/rear-reconstruction-v4/back_l/Sword/native/00.png"),
]:
    if p.exists():
        im = np.array(Image.open(p).convert("RGBA"))
        if im.shape[0] == 256:
            im = im[64:192, 64:192]
        vis = im[:, :, 3] > 0
        ys, xs = np.where(vis)
        print(f"{label}: vis={int(np.sum(vis))} bbox=[{xs.min()},{ys.min()}..{xs.max()},{ys.max()}]")
