from pathlib import Path
from PIL import Image
import numpy as np

RAW_DIR = Path("experiments/main-orc-combat-rescue-v5/combat/raw")

for tag, side in [
    ("back_r_sword_v1", "right"),
    ("back_r_axe_v1",   "right"),
    ("back_l_sword_v1", "left"),
    ("back_l_axe_v1",   "left"),
    ("back_r_unarmed_v1", "right"),
    ("back_l_unarmed_v1", "left"),
]:
    print(f"=== {tag} ===")
    n_f = 4 if "unarmed" in tag else 7
    for idx in range(n_f):
        im = np.array(Image.open(RAW_DIR / tag / f"{idx:02d}.png").convert("RGBA"))
        vis = im[:, :, 3] > 0
        # Find pixels with red/brown gauntlet strap (R > G + 12 and R > 40) on the attacking side
        if side == "right":
            m_side = np.zeros_like(vis)
            m_side[:90, 74:] = vis[:90, 74:]
            # Also find rightmost extremity (within 8px of xmax on x>=84)
            ys_all, xs_all = np.where(m_side)
            xmax = int(xs_all.max())
            ymin = int(ys_all.min())
            # Strap mask
            strap = m_side & (im[:, :, 0].astype(int) > im[:, :, 1].astype(int) + 12) & (im[:, :, 0] > 40) & (np.arange(128)[None, :] >= 84)
            sys, sxs = np.where(strap)
            # Distal cluster: if xmax >= 108, take x >= xmax - 10; else if ymin <= 10, take y <= ymin + 12 and x >= 82; else take x >= xmax - 10 and y >= 40
            if xmax >= 106:
                dist = m_side & (np.arange(128)[None, :] >= xmax - 10)
            elif ymin <= 10 and idx in (0, 1):
                dist = m_side & (np.arange(128)[:, None] <= ymin + 12) & (np.arange(128)[None, :] >= 82)
            else:
                dist = m_side & (np.arange(128)[None, :] >= xmax - 10) & (np.arange(128)[:, None] >= 40)
            dys, dxs = np.where(dist)
            dcx, dcy = int(np.median(dxs)), int(np.median(dys))
            scx = int(np.median(sxs)) if len(sxs) else -1
            scy = int(np.median(sys)) if len(sys) else -1
            print(f"  F0{idx+1} (raw {idx:02d}): distal=({dcx},{dcy})->comp({dcx+64},{dcy+64}) | strap=({scx},{scy}) | xmax={xmax}, ymin={ymin}")
        else:
            m_side = np.zeros_like(vis)
            m_side[:90, :54] = vis[:90, :54]
            ys_all, xs_all = np.where(m_side)
            xmin = int(xs_all.min())
            ymin = int(ys_all.min())
            strap = m_side & (im[:, :, 0].astype(int) > im[:, :, 1].astype(int) + 12) & (im[:, :, 0] > 40) & (np.arange(128)[None, :] <= 43)
            sys, sxs = np.where(strap)
            if xmin <= 21:
                dist = m_side & (np.arange(128)[None, :] <= xmin + 10)
            elif ymin <= 10 and idx in (0, 1):
                dist = m_side & (np.arange(128)[:, None] <= ymin + 12) & (np.arange(128)[None, :] <= 45)
            else:
                dist = m_side & (np.arange(128)[None, :] <= xmin + 10) & (np.arange(128)[:, None] >= 40)
            dys, dxs = np.where(dist)
            dcx, dcy = int(np.median(dxs)), int(np.median(dys))
            scx = int(np.median(sxs)) if len(sxs) else -1
            scy = int(np.median(sys)) if len(sys) else -1
            print(f"  F0{idx+1} (raw {idx:02d}): distal=({dcx},{dcy})->comp({dcx+64},{dcy+64}) | strap=({scx},{scy}) | xmin={xmin}, ymin={ymin}")
