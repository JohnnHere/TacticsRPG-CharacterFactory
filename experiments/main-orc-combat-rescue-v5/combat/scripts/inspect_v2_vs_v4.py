import json
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")

print("=== 1. Comparing rear-recovery-v2 (with QA-revision-1-repair) vs rear-reconstruction-v4 ===")
for d in ["back_r", "back_l"]:
    for a in ["Sword", "Axe"]:
        v2_sub = "Attack-representative-v2" if (d == "back_r" and a == "Sword") else "Attack-representative-v1"
        v2_dir = ROOT / f"characters/orc-v1/source/rear-recovery-v2/{d}/{a}/{v2_sub}"
        v4_dir = ROOT / f"characters/orc-v1/source/rear-reconstruction-v4/{d}/{a}"
        print(f"\nClip {d}/{a}:")
        for i in range(8):
            fn = f"{i:02d}.png"
            v2_nat = np.array(Image.open(v2_dir / "native" / fn).convert("RGBA"))
            v4_nat = np.array(Image.open(v4_dir / "native" / fn).convert("RGBA"))
            diff_nat = int(np.sum(np.any(v2_nat != v4_nat, axis=2)))
            v2_comp = np.array(Image.open(v2_dir / fn).convert("RGBA"))
            v4_comp = np.array(Image.open(v4_dir / fn).convert("RGBA"))
            diff_comp = int(np.sum(np.any(v2_comp != v4_comp, axis=2)))
            print(f"  F{i:02d}: native_diff={diff_nat}px, comp_diff={diff_comp}px")

print("\n=== 2. Comparing raw pixellab-skeleton-v3 back_r vs back_r_axe ===")
for i in range(7):
    fn = f"{i:02d}.png"
    p_sr = ROOT / f"experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_r/{fn}"
    p_ar = ROOT / f"experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_r_axe/{fn}"
    p_sl = ROOT / f"experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l/{fn}"
    p_al = ROOT / f"experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l_axe/{fn}"
    sr = np.array(Image.open(p_sr).convert("RGBA"))
    ar = np.array(Image.open(p_ar).convert("RGBA"))
    sl = np.array(Image.open(p_sl).convert("RGBA"))
    al = np.array(Image.open(p_al).convert("RGBA"))
    print(f"  raw[{i:02d}]: back_r vs back_r_axe diff={int(np.sum(np.any(sr!=ar, axis=2)))}px | back_l vs back_l_axe diff={int(np.sum(np.any(sl!=al, axis=2)))}px")

print("\n=== 3. Inspecting Unarmed front_r and front_l striking arm / fist across F00..F04 ===")
# In front_r (SE), the striking arm is the orc's right arm (viewer-left, x < 64) or left arm (viewer-right, x > 64)?
# Let's check where the motion happens between F00, F01, F02, F03, F04 in front_r and front_l!
for d in ["front_r", "front_l", "back_r", "back_l"]:
    u_dir = ROOT / f"characters/orc-v1/source/rear-recovery-v2/{d}/Unarmed"
    f0 = np.array(Image.open(u_dir / "00.png").convert("RGBA"))[64:192, 64:192]
    print(f"\n{d}/Unarmed differences vs F00 (native 128x128):")
    for i in range(1, 5):
        fi = np.array(Image.open(u_dir / f"{i:02d}.png").convert("RGBA"))[64:192, 64:192]
        diff = np.any(fi != f0, axis=2)
        left_half = int(np.sum(diff[:, :64]))
        right_half = int(np.sum(diff[:, 64:]))
        vis_fi = fi[:, :, 3] > 0
        xs = np.where(vis_fi)[1]
        ys = np.where(vis_fi)[0]
        # Also check upper arm / fist extremities (x min and x max in y=25..80)
        mid_y = vis_fi[25:80, :]
        mxs = np.where(mid_y)[1]
        print(f"  F{i:02d}: diff_left(x<64)={left_half}px, diff_right(x>=64)={right_half}px | mid_y(25..80) x_range=[{mxs.min()}..{mxs.max()}]")
