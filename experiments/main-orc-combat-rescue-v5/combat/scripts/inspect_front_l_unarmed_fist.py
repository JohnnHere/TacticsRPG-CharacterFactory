from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")

for idx in [1, 2, 3, 4]:
    p = ROOT / f"characters/orc-v1/source/rear-recovery-v2/front_l/Unarmed/{idx:02d}.png"
    nat = np.array(Image.open(p).convert("RGBA"))[64:192, 64:192]
    print(f"\n=== front_l/Unarmed F{idx:02d} (x=20..65, y=42..68, step 1) ===")
    for y in range(42, 69):
        line = []
        for x in range(20, 65):
            r, g, b, a = nat[y, x]
            if a == 0:
                ch = "."
            elif g > r + 10 and g > b + 10:
                ch = "G"
            elif r > g + 15 and r > 50:
                ch = "R"
            elif r < 22 and g < 22 and b < 25:
                ch = "#"
            elif r > 90 and g > 90 and b > 90:
                ch = "H"
            else:
                ch = "s"
            line.append(ch)
        print(f"y={y:02d}: " + "".join(line))
