from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")
f02 = np.array(Image.open(ROOT / "characters/orc-v1/source/rear-recovery-v2/front_r/Unarmed/02.png").convert("RGBA"))[64:192, 64:192]
sw06 = np.array(Image.open(ROOT / "characters/orc-v1/source/complete-v1/front_r/Unarmed/02.png").convert("RGBA"))[64:192, 64:192]

diff = np.any(f02 != sw06, axis=-1)
ys, xs = np.where(diff)
print(f"F02 vs Sword[06] diff count: {len(xs)}, x={xs.min()}..{xs.max()}, y={ys.min()}..{ys.max()}")
for y in range(ys.min(), ys.max()+1):
    for x in range(xs.min(), xs.max()+1):
        if diff[y, x]:
            r, g, b, a = f02[y, x]
            # print summary of rows
            pass
    row = "".join("#" if diff[y, x] else "." for x in range(xs.min(), xs.max()+1))
    print(f"y={y:02d} (x={xs.min()}..{xs.max()}): {row}")
