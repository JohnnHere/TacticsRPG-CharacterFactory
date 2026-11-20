from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")

for key, d, a in [("SwordR", "back_r", "Sword"), ("SwordL", "back_l", "Sword"), ("AxeR", "back_r", "Axe"), ("AxeL", "back_l", "Axe")]:
    print(f"\n================ V4 {key} ({d}/{a}) full width x=0..127, y=0..96, step 4y/2x ================")
    for i in range(8):
        im = np.array(Image.open(ROOT / f"characters/orc-v1/source/rear-reconstruction-v4/{d}/{a}/native/{i:02d}.png").convert("RGBA"))
        print(f"--- V4 {key} F{i:02d} ---")
        for y in range(0, 96, 6):
            line = []
            for x in range(0, 128, 2):
                r, g, b, a_val = im[y, x]
                if a_val == 0: ch = "."
                elif g > r + 10 and g > b + 10: ch = "G"
                elif r > g + 15 and r > 50: ch = "R"
                elif r < 22 and g < 22 and b < 25: ch = "#"
                elif r > 90 and g > 90 and b > 90: ch = "H"
                else: ch = "s"
                line.append(ch)
            print(f"y={y:02d}: " + "".join(line))
