from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")

for idx in [1, 2, 3, 4]:
    v1_p = ROOT / f"characters/orc-v1/source/complete-v1/front_r/Unarmed/{idx:02d}.png"
    v2_p = ROOT / f"characters/orc-v1/source/rear-recovery-v2/front_r/Unarmed/{idx:02d}.png"
    v1 = np.array(Image.open(v1_p).convert("RGBA"))[64:192, 64:192]
    v2 = np.array(Image.open(v2_p).convert("RGBA"))[64:192, 64:192]
    print(f"\n=== complete-v1 front_r/Unarmed F{idx:02d} (x=65..110, y=42..68, step 1) ===")
    for y in range(42, 69, 2):
        line = []
        for x in range(65, 110):
            r, g, b, a = v1[y, x]
            if a == 0: ch = "."
            elif g > r + 10 and g > b + 10: ch = "G"
            elif r > g + 15 and r > 50: ch = "R"
            elif r < 22 and g < 22 and b < 25: ch = "#"
            elif r > 90 and g > 90 and b > 90: ch = "H"
            else: ch = "s"
            line.append(ch)
        print(f"y={y:02d}: " + "".join(line))
