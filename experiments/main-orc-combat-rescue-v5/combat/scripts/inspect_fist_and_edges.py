import json
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")
RAW_DIR = ROOT / "experiments/main-orc-combat-rescue-v5/combat/raw"
V4_DIR = ROOT / "characters/orc-v1/source/rear-reconstruction-v4"

# 1. Inspect edge-touching regions in detail
def print_ascii(im, x0, x1, y0, y1, title):
    print(f"--- {title} [{x0}..{x1}, {y0}..{y1}] ---")
    for y in range(y0, y1 + 1):
        row = []
        for x in range(x0, x1 + 1):
            r, g, b, a = im[y, x]
            if a == 0:
                row.append(".")
            elif r < 22 and g < 22 and b < 25:
                row.append("#") # dark outline
            elif r > g + 15:
                row.append("R") # red/brown strap
            elif g > r + 10:
                row.append("G") # green skin
            elif r > 85:
                row.append("H") # bright steel highlight
            else:
                row.append("s") # mid/dark steel
        print(f"y={y:03d}: " + "".join(row))

for tag, raw_idx, x0, x1, y0, y1 in [
    ("back_r_sword_v1", 3, 108, 127, 30, 56),
    ("back_l_sword_v1", 2, 0, 22, 16, 40),
    ("back_l_sword_v1", 3, 0, 22, 32, 56),
    ("back_r_axe_v1",   1, 80, 104, 0, 22),
    ("back_l_axe_v1",   0, 20, 44, 0, 22),
    ("back_l_axe_v1",   1, 22, 46, 0, 22),
    ("back_r_unarmed_v1", 1, 108, 127, 22, 44),
]:
    im = np.array(Image.open(RAW_DIR / tag / f"{raw_idx:02d}.png").convert("RGBA"))
    print_ascii(im, x0, x1, y0, y1, f"{tag} raw {raw_idx:02d} (F0{raw_idx+1})")

# 2. Measure the attacking fist center in every frame of our 4 rear weapon raw sequences
print("\n=== Measuring Rear Attacking Fist Centers (native 128 -> composite 256) ===")
for tag, side in [
    ("back_r_sword_v1", "right"),
    ("back_r_axe_v1",   "right"),
    ("back_l_sword_v1", "left"),
    ("back_l_axe_v1",   "left"),
]:
    print(f"*** {tag} ***")
    for idx in range(7):
        im = np.array(Image.open(RAW_DIR / tag / f"{idx:02d}.png").convert("RGBA"))
        vis = im[:, :, 3] > 0
        # Find distal arm extremity
        if side == "right":
            # Look at x >= 76, y <= 88
            mask = np.zeros_like(vis)
            mask[:88, 76:] = vis[:88, 76:]
            ys, xs = np.where(mask)
            if len(xs) > 0:
                # Distal fist is near max(x - 0.4*y) for high frames or max(x) for side frames
                if ys.min() < 15:
                    # overhead/high: take top-most cluster (within y_min..y_min+10)
                    top_m = mask & (np.arange(128)[:, None] <= ys.min() + 9)
                    tys, txs = np.where(top_m)
                    cx, cy = int(np.median(txs)), int(np.median(tys))
                else:
                    # side/extended: take right-most cluster (within x_max-9..x_max)
                    rm = mask & (np.arange(128)[None, :] >= xs.max() - 9)
                    rys, rxs = np.where(rm)
                    cx, cy = int(np.median(rxs)), int(np.median(rys))
                print(f"  F0{idx+1} (raw {idx:02d}): native=({cx},{cy}) -> comp256=({cx+64},{cy+64}) [arm_bbox={xs.min()},{ys.min()}..{xs.max()},{ys.max()}]")
        else:
            # Look at x <= 51, y <= 88
            mask = np.zeros_like(vis)
            mask[:88, :52] = vis[:88, :52]
            ys, xs = np.where(mask)
            if len(xs) > 0:
                if ys.min() < 15:
                    top_m = mask & (np.arange(128)[:, None] <= ys.min() + 9)
                    tys, txs = np.where(top_m)
                    cx, cy = int(np.median(txs)), int(np.median(tys))
                else:
                    lm = mask & (np.arange(128)[None, :] <= xs.min() + 9)
                    lys, lxs = np.where(lm)
                    cx, cy = int(np.median(lxs)), int(np.median(lys))
                print(f"  F0{idx+1} (raw {idx:02d}): native=({cx},{cy}) -> comp256=({cx+64},{cy+64}) [arm_bbox={xs.min()},{ys.min()}..{xs.max()},{ys.max()}]")
