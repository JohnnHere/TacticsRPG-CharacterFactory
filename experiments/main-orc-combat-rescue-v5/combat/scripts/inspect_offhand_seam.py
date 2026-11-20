from pathlib import Path
from PIL import Image
import numpy as np

RAW_DIR = Path("experiments/main-orc-combat-rescue-v5/combat/raw")

def print_ascii(im, x0, x1, y0, y1, title):
    print(f"=== {title} [{x0}..{x1}, {y0}..{y1}] ===")
    for y in range(y0, y1 + 1):
        row = []
        for x in range(x0, x1 + 1):
            r, g, b, a = im[y, x]
            if a == 0:
                row.append(".")
            elif r < 22 and g < 22 and b < 25:
                row.append("#")
            elif r > g + 15:
                row.append("R")
            elif g > r + 10:
                row.append("G")
            elif r > 85:
                row.append("H")
            else:
                row.append("s")
        print(f"y={y:03d}: " + "".join(row))

im0_r = np.array(Image.open(RAW_DIR / "back_r_base_128.png").convert("RGBA"))
im3_r = np.array(Image.open(RAW_DIR / "back_r_sword_v1/02.png").convert("RGBA"))
print_ascii(im0_r, 34, 52, 22, 86, "back_r_base_128 x=34..52")
print_ascii(im3_r, 34, 52, 22, 86, "back_r_sword_v1 raw 02 (F03) x=34..52")

im0_l = np.array(Image.open(RAW_DIR / "back_l_base_128.png").convert("RGBA"))
im3_l = np.array(Image.open(RAW_DIR / "back_l_sword_v1/02.png").convert("RGBA"))
print_ascii(im0_l, 74, 92, 22, 86, "back_l_base_128 x=74..92")
print_ascii(im3_l, 74, 92, 22, 86, "back_l_sword_v1 raw 02 (F03) x=74..92")
