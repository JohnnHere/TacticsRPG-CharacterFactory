from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")

# Let's inspect F02 and F03 of front_r/Unarmed around the right arm (x=65..108, y=42..68)
f02 = np.array(Image.open(ROOT / "characters/orc-v1/source/rear-recovery-v2/front_r/Unarmed/02.png").convert("RGBA"))[64:192, 64:192]
f03 = np.array(Image.open(ROOT / "characters/orc-v1/source/rear-recovery-v2/front_r/Unarmed/03.png").convert("RGBA"))[64:192, 64:192]

print("=== F02 right punch gauntlet (x=80..108, y=44..60) ===")
for y in range(44, 61):
    row_str = []
    for x in range(80, 108):
        r, g, b, a = f02[y, x]
        if a == 0: ch = "."
        elif r < 22 and g < 22 and b < 25: ch = "#"
        elif r > g + 15 and r > 50: ch = "R"
        elif r > 90 and g > 90 and b > 90: ch = "H"
        else: ch = "s"
        row_str.append(ch)
    print(f"y={y:02d}: " + "".join(row_str))

print("\n=== F03 right arm area (x=72..108, y=38..68) ===")
for y in range(38, 69):
    row_str = []
    for x in range(72, 108):
        r, g, b, a = f03[y, x]
        if a == 0: ch = "."
        elif r < 22 and g < 22 and b < 25: ch = "#"
        elif r > g + 15 and r > 50: ch = "R"
        elif r > 90 and g > 90 and b > 90: ch = "H"
        else: ch = "s"
        row_str.append(ch)
    print(f"y={y:02d}: " + "".join(row_str))
