from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")

# Let's inspect raw_unarmed_r frames 00..08 and punch_impact_key_back_r / punch_impact_key_back_l
print("=== Raw frames_unarmed_r (00..08) ===")
raw_u_dir = ROOT / "experiments/main-orc-rear-recovery-v2/raw/frames_unarmed_r"
f0 = np.array(Image.open(raw_u_dir / "frame_00.png").convert("RGBA"))
for i in range(9):
    fi = np.array(Image.open(raw_u_dir / f"frame_{i:02d}.png").convert("RGBA"))
    diff = np.any(fi != f0, axis=2)
    vis = fi[:, :, 3] > 0
    xs = np.where(vis)[1]
    ys = np.where(vis)[0]
    print(f"  frame_{i:02d}: vis={int(np.sum(vis))} bbox=[{xs.min()},{ys.min()}..{xs.max()},{ys.max()}] diff_vs_00={int(np.sum(diff))}px")

# Let's inspect raw/pixellab-skeleton-v3/back_r (00..06) and back_r_axe (00..06)
# Wait: why did raw/pixellab-skeleton-v3/back_r have diff=5944px vs back_r_axe?
# Let's check what raw/pixellab-skeleton-v3/back_r actually is!
print("\n=== Comparing raw/pixellab-skeleton-v3/back_r vs back_r_base.png ===")
base_r = np.array(Image.open(ROOT / "experiments/main-orc-complete-v1/pixellab-recovery/back_r_base.png").convert("RGBA"))
base_l = np.array(Image.open(ROOT / "experiments/main-orc-complete-v1/pixellab-recovery/back_l_base.png").convert("RGBA"))
for sub, base in [("back_r", base_r), ("back_r_axe", base_r), ("back_l", base_l), ("back_l_axe", base_l)]:
    print(f"\nSubfolder {sub}:")
    for i in range(7):
        im = np.array(Image.open(ROOT / f"experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/{sub}/{i:02d}.png").convert("RGBA"))
        diff_base = int(np.sum(np.any(im != base, axis=2)))
        # check right arm area (x >= 78, y = 0..85) and left arm area (x <= 50, y = 0..85)
        vis = im[:, :, 3] > 0
        r_arm = vis[:85, 78:]
        l_arm = vis[:85, :50]
        ry, rx = np.where(r_arm)
        ly, lx = np.where(l_arm)
        r_box = f"x=[{rx.min()+78}..{rx.max()+78}] y=[{ry.min()}..{ry.max()}]" if len(rx) else "none"
        l_box = f"x=[{lx.min()}..{lx.max()}] y=[{ly.min()}..{ly.max()}]" if len(lx) else "none"
        print(f"  [{i:02d}]: diff_vs_base={diff_base}px | left_upper={l_box} | right_upper={r_box}")
