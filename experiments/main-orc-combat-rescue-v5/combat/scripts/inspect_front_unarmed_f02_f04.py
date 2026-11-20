from pathlib import Path
from PIL import Image
import numpy as np

V2_UNARMED = Path("characters/orc-v1/source/rear-recovery-v2/front_r/Unarmed/native")

for i in range(5):
    im = np.array(Image.open(V2_UNARMED / f"0{i}.png").convert("RGBA"))
    vis = im[:, :, 3] > 0
    # Left side (x < 46)
    l_ys, l_xs = np.where(vis[:, :46])
    # Right side (x > 72)
    r_ys, r_xs = np.where(vis[:, 73:])
    r_xs = r_xs + 73
    print(f"front_r/Unarmed F0{i}: left_arm bbox=({l_xs.min()},{l_ys.min()}..{l_xs.max()},{l_ys.max()}), right_arm bbox=({r_xs.min()},{r_ys.min()}..{r_xs.max()},{r_ys.max()})")

# Print pixel diff between F02 and F04 on torso/legs (46 <= x <= 74)
im0 = np.array(Image.open(V2_UNARMED / "00.png").convert("RGBA"))
im2 = np.array(Image.open(V2_UNARMED / "02.png").convert("RGBA"))
im3 = np.array(Image.open(V2_UNARMED / "03.png").convert("RGBA"))
im4 = np.array(Image.open(V2_UNARMED / "04.png").convert("RGBA"))

print("Diff F02 vs F00 on left side (x <= 45):", int(np.any(im2[:, :46] != im0[:, :46], axis=2).sum()))
print("Diff F02 vs F04 on center/legs (44 <= x <= 76, y >= 62):", int(np.any(im2[62:, 44:77] != im4[62:, 44:77], axis=2).sum()))
