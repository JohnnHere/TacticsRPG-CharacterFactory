from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")

for idx in range(5):
    v1_p = ROOT / f"characters/orc-v1/source/complete-v1/front_r/Unarmed/{idx:02d}.png"
    v2_p = ROOT / f"characters/orc-v1/source/rear-recovery-v2/front_r/Unarmed/{idx:02d}.png"
    v1 = np.array(Image.open(v1_p).convert("RGBA"))[64:192, 64:192]
    v2 = np.array(Image.open(v2_p).convert("RGBA"))[64:192, 64:192]
    diff = int(np.sum(np.any(v1 != v2, axis=2)))
    print(f"front_r/Unarmed F{idx:02d}: complete-v1 vs rear-recovery-v2 diff = {diff}px")

# Let's inspect F01, F02, F03 of front_r/Unarmed across the entire upper-body (x=10..115, y=28..76, step 2)
for idx in range(5):
    nat = np.array(Image.open(ROOT / f"characters/orc-v1/source/rear-recovery-v2/front_r/Unarmed/{idx:02d}.png").convert("RGBA"))[64:192, 64:192]
    print(f"\n=== FULL WIDTH front_r/Unarmed F{idx:02d} (x=8..112, y=28..74, step 2) ===")
    for y in range(28, 76, 2):
        line = []
        for x in range(8, 112, 2):
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
