from pathlib import Path
from PIL import Image
import numpy as np

CLEAN_ROOT = Path("experiments/main-orc-combat-rescue-v5/combat/cleaned_rear_bodies")

def print_ascii(im, x0, x1, y0, y1, title):
    print(f"=== {title} [native {x0}..{x1}, {y0}..{y1}] ===")
    for y in range(y0, y1 + 1):
        row = []
        for x in range(x0, x1 + 1):
            r, g, b, a = im[y, x]
            if a == 0:
                row.append(".")
            elif r < 22 and g < 22 and b < 25:
                row.append("#")
            elif r > g + 12 and r > 40:
                row.append("R")
            elif g > r + 10:
                row.append("G")
            elif r > 85:
                row.append("H")
            else:
                row.append("s")
        print(f"y={y:03d}(c{y+64:03d}): " + "".join(row))

for tag, side in [
    ("back_r_sword", "right"),
    ("back_r_axe",   "right"),
    ("back_l_sword", "left"),
    ("back_l_axe",   "left"),
]:
    print(f"*** {tag} ***")
    for idx in range(1, 7):
        im = np.array(Image.open(CLEAN_ROOT / tag / f"{idx:02d}.png").convert("RGBA"))
        vis = im[:, :, 3] > 0
        if side == "right":
            m_side = np.zeros_like(vis)
            m_side[:90, 74:] = vis[:90, 74:]
            ys_all, xs_all = np.where(m_side)
            xmax, ymin = int(xs_all.max()), int(ys_all.min())
            if ymin <= 10 and idx in (1, 2):
                # Overhead
                x0, x1 = max(74, xmax - 22), min(127, xmax + 2)
                y0, y1 = max(0, ymin - 1), min(127, ymin + 22)
            else:
                # Lateral/extended/lowered
                m_ext = m_side & (np.arange(128)[None, :] >= xmax - 18)
                eys, exs = np.where(m_ext)
                yc = int(np.median(eys))
                x0, x1 = max(74, xmax - 22), min(127, xmax + 2)
                y0, y1 = max(0, yc - 12), min(127, yc + 12)
            print_ascii(im, x0, x1, y0, y1, f"{tag} F{idx:02d} (comp_x={x0+64}..{x1+64})")
        else:
            m_side = np.zeros_like(vis)
            m_side[:90, :54] = vis[:90, :54]
            ys_all, xs_all = np.where(m_side)
            xmin, ymin = int(xs_all.min()), int(ys_all.min())
            if ymin <= 10 and idx in (1, 2):
                x0, x1 = max(0, xmin - 2), min(54, xmin + 22)
                y0, y1 = max(0, ymin - 1), min(127, ymin + 22)
            else:
                m_ext = m_side & (np.arange(128)[None, :] <= xmin + 18)
                eys, exs = np.where(m_ext)
                yc = int(np.median(eys))
                x0, x1 = max(0, xmin - 2), min(54, xmin + 22)
                y0, y1 = max(0, yc - 12), min(127, yc + 12)
            print_ascii(im, x0, x1, y0, y1, f"{tag} F{idx:02d} (comp_x={x0+64}..{x1+64})")
