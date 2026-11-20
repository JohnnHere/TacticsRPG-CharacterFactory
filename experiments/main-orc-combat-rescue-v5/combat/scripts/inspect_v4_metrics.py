from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")

base_r = np.array(Image.open(ROOT / "characters/orc-v1/source/rear-reconstruction-v4/back_r/Sword/native/00.png").convert("RGBA"))
base_l = np.array(Image.open(ROOT / "characters/orc-v1/source/rear-reconstruction-v4/back_l/Sword/native/00.png").convert("RGBA"))

for key, d, a, base in [
    ("SwordR", "back_r", "Sword", base_r),
    ("AxeR", "back_r", "Axe", base_r),
    ("SwordL", "back_l", "Sword", base_l),
    ("AxeL", "back_l", "Axe", base_l),
]:
    print(f"\n=== V4 {key} ({d}/{a}) arm/artifact analysis ===")
    for i in range(8):
        im = np.array(Image.open(ROOT / f"characters/orc-v1/source/rear-reconstruction-v4/{d}/{a}/native/{i:02d}.png").convert("RGBA"))
        vis = im[:, :, 3] > 0
        diff = np.any(im != base, axis=2)
        # In back_r, attacking arm is right side (x >= 76), off-hand is left side (x <= 48)
        # In back_l, attacking arm is left side (x <= 52), off-hand is right side (x >= 80)
        if d == "back_r":
            atk_pts = np.argwhere(vis[:, 78:]) # x offset +78
            off_diff = int(np.sum(diff[:, :48]))
            atk_x = [int(atk_pts[:,1].min()+78), int(atk_pts[:,1].max()+78)] if len(atk_pts) else []
            atk_y = [int(atk_pts[:,0].min()), int(atk_pts[:,0].max())] if len(atk_pts) else []
            # Find distal tip (max x or min y if raised)
            if len(atk_pts):
                if atk_y[0] < 18:
                    # raised arm: find x at min y
                    top_pts = atk_pts[atk_pts[:,0] <= atk_y[0] + 4]
                    tip = (int(top_pts[:,1].mean()+78), int(top_pts[:,0].mean()))
                else:
                    # extended arm: find y at max x
                    ext_pts = atk_pts[atk_pts[:,1] >= atk_pts[:,1].max() - 4]
                    tip = (int(ext_pts[:,1].mean()+78), int(ext_pts[:,0].mean()))
            else:
                tip = None
            print(f"  F{i:02d}: atk_arm_x={atk_x} y={atk_y} tip={tip} | off_hand_diff={off_diff}px")
        else:
            atk_pts = np.argwhere(vis[:, :50])
            off_diff = int(np.sum(diff[:, 80:]))
            atk_x = [int(atk_pts[:,1].min()), int(atk_pts[:,1].max())] if len(atk_pts) else []
            atk_y = [int(atk_pts[:,0].min()), int(atk_pts[:,0].max())] if len(atk_pts) else []
            if len(atk_pts):
                if atk_y[0] < 18:
                    top_pts = atk_pts[atk_pts[:,0] <= atk_y[0] + 4]
                    tip = (int(top_pts[:,1].mean()), int(top_pts[:,0].mean()))
                else:
                    ext_pts = atk_pts[atk_pts[:,1] <= atk_pts[:,1].min() + 4]
                    tip = (int(ext_pts[:,1].mean()), int(ext_pts[:,0].mean()))
            else:
                tip = None
            print(f"  F{i:02d}: atk_arm_x={atk_x} y={atk_y} tip={tip} | off_hand_diff={off_diff}px")
            if off_diff > 0:
                od_pts = np.argwhere(diff[:, 80:])
                print(f"       off_hand_diff bbox: x=[{od_pts[:,1].min()+80}..{od_pts[:,1].max()+80}] y=[{od_pts[:,0].min()}..{od_pts[:,0].max()}]")
