from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")

for sub, side_x in [("back_r", (72, 128)), ("back_r_axe", (72, 128)), ("back_l", (0, 56)), ("back_l_axe", (0, 56))]:
    print(f"\n================ {sub} (x={side_x[0]}..{side_x[1]-1}, y=0..68, step 2) ================")
    for i in range(7):
        im = np.array(Image.open(ROOT / f"experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/{sub}/{i:02d}.png").convert("RGBA"))
        print(f"--- {sub} [{i:02d}] ---")
        for y in range(0, 68, 4):
            line = []
            for x in range(side_x[0], side_x[1], 2):
                r, g, b, a = im[y, x]
                if a == 0: ch = "."
                elif g > r + 10 and g > b + 10: ch = "G"
                elif r > g + 15 and r > 50: ch = "R"
                elif r < 22 and g < 22 and b < 25: ch = "#"
                elif r > 90 and g > 90 and b > 90: ch = "H"
                else: ch = "s"
                line.append(ch)
            print(f"y={y:02d}: " + "".join(line))
