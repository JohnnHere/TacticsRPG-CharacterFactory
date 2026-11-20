from pathlib import Path
from PIL import Image
import numpy as np

V2_UNARMED = Path("characters/orc-v1/source/rear-recovery-v2/front_r/Unarmed/native")

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

for i in range(5):
    im = np.array(Image.open(V2_UNARMED / f"0{i}.png").convert("RGBA"))
    print_ascii(im, 40, 110, 26, 62, f"front_r/Unarmed F0{i} FULL UPPER TORSO + RIGHT ARM")
