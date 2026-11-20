from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

ROOT = Path(".")
SHEETS_DIR = ROOT / "experiments/main-orc-combat-rescue-v5/combat/sheets"
SHEETS_DIR.mkdir(parents=True, exist_ok=True)

# 1. Inspect raw skeleton-v3 sequences vs v4 native strips
# Let's build a single overview PNG stacking:
# Row 0: raw/pixellab-skeleton-v3/back_r (00..06)
# Row 1: raw/pixellab-skeleton-v3/back_r_axe (00..06)
# Row 2: raw/pixellab-skeleton-v3/back_l (00..06)
# Row 3: raw/pixellab-skeleton-v3/back_l_axe (00..06)
# Row 4: raw/frames_unarmed_r (00..07)
# Row 5: v4 back_r/Sword native (00..07)
# Row 6: v4 back_r/Axe native (00..07)
# Row 7: v4 back_l/Sword native (00..07)
# Row 8: v4 back_l/Axe native (00..07)

rows = [
    ("raw_back_r", [ROOT / f"experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_r/{i:02d}.png" for i in range(7)]),
    ("raw_back_r_axe", [ROOT / f"experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_r_axe/{i:02d}.png" for i in range(7)]),
    ("raw_back_l", [ROOT / f"experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l/{i:02d}.png" for i in range(7)]),
    ("raw_back_l_axe", [ROOT / f"experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l_axe/{i:02d}.png" for i in range(7)]),
    ("raw_unarmed_r", [ROOT / f"experiments/main-orc-rear-recovery-v2/raw/frames_unarmed_r/frame_{i:02d}.png" for i in range(8)]),
    ("v4_back_r_sword", [ROOT / f"characters/orc-v1/source/rear-reconstruction-v4/back_r/Sword/native/{i:02d}.png" for i in range(8)]),
    ("v4_back_r_axe", [ROOT / f"characters/orc-v1/source/rear-reconstruction-v4/back_r/Axe/native/{i:02d}.png" for i in range(8)]),
    ("v4_back_l_sword", [ROOT / f"characters/orc-v1/source/rear-reconstruction-v4/back_l/Sword/native/{i:02d}.png" for i in range(8)]),
    ("v4_back_l_axe", [ROOT / f"characters/orc-v1/source/rear-reconstruction-v4/back_l/Axe/native/{i:02d}.png" for i in range(8)]),
]

sheet = Image.new("RGBA", (8 * 128, len(rows) * 128), (20, 22, 26, 255))
for r_idx, (label, paths) in enumerate(rows):
    for c_idx, p in enumerate(paths):
        if p.exists():
            im = Image.open(p).convert("RGBA")
            sheet.alpha_composite(im, (c_idx * 128, r_idx * 128))
sheet.save(SHEETS_DIR / "stage_a_rear_bodies_overview.png")

# 2. Build Unarmed 4-view overview (4 rows x 5 cols of 128x128)
u_sheet = Image.new("RGBA", (5 * 128, 4 * 128), (20, 22, 26, 255))
for r_idx, d in enumerate(["front_r", "front_l", "back_r", "back_l"]):
    for c_idx in range(5):
        p = ROOT / f"characters/orc-v1/source/rear-recovery-v2/{d}/Unarmed/{c_idx:02d}.png"
        im = Image.open(p).convert("RGBA").crop((64, 64, 192, 192))
        u_sheet.alpha_composite(im, (c_idx * 128, r_idx * 128))
u_sheet.save(SHEETS_DIR / "stage_a_unarmed_4views.png")

# 3. Print ASCII art of the striking arm/fist in front_r/Unarmed F00..F04
# Let's check which side is the punch in front_r/Unarmed!
print("=== Front_R Unarmed: Inspecting both arms across F00..F04 ===")
for idx in range(5):
    p = ROOT / f"characters/orc-v1/source/rear-recovery-v2/front_r/Unarmed/{idx:02d}.png"
    nat = np.array(Image.open(p).convert("RGBA"))[64:192, 64:192]
    print(f"\n--- front_r/Unarmed F{idx:02d} (x=8..55, y=35..78, step 2) ---")
    for y in range(35, 78, 2):
        line = []
        for x in range(8, 112, 2):
            r, g, b, a = nat[y, x]
            if a == 0:
                ch = "."
            elif g > r + 12 and g > b + 12:
                ch = "G" # green skin
            elif r > g + 18 and r > 55:
                ch = "R" # red-brown leather/strap
            elif r < 22 and g < 22 and b < 25:
                ch = "#" # dark outline
            elif r > 90 and g > 90 and b > 90:
                ch = "H" # bright steel highlight
            else:
                ch = "s" # steel/armor
            line.append(ch)
        print(f"y={y:02d}: " + "".join(line))
