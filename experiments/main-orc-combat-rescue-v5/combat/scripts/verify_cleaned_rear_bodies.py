from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

CLEAN_ROOT = Path("experiments/main-orc-combat-rescue-v5/combat/cleaned_rear_bodies")
SHEET_PATH = Path("experiments/main-orc-combat-rescue-v5/combat/sheets/cleaned_rear_bodies_4x8.png")

cols = 8
rows = 4
cell = 256
sheet = Image.new("RGBA", (cols * cell, rows * cell), (28, 32, 38, 255))
draw = ImageDraw.Draw(sheet)

tags = ["back_r_sword", "back_r_axe", "back_l_sword", "back_l_axe"]
for r_idx, tag in enumerate(tags):
    im0 = np.array(Image.open(CLEAN_ROOT / tag / "00.png").convert("RGBA"))
    for i in range(8):
        im = np.array(Image.open(CLEAN_ROOT / tag / f"{i:02d}.png").convert("RGBA"))
        vis = im[:, :, 3] > 0
        ys, xs = np.where(vis)
        xmin, xmax = int(xs.min()), int(xs.max())
        ymin, ymax = int(ys.min()), int(ys.max())
        assert ymax == 126, f"groundY mismatch in {tag} F{i:02d}: {ymax}"
        assert xmin >= 2 and xmax <= 125 and ymin >= 2, (
            f"Border violation in {tag} F{i:02d}: x={xmin}..{xmax}, y={ymin}..{ymax}"
        )
        if "back_r" in tag:
            off_diff = int(np.any(im[10:85, :42] != im0[10:85, :42], axis=2).sum())
        else:
            off_diff = int(np.any(im[10:85, 86:] != im0[10:85, 86:], axis=2).sum())
        assert off_diff == 0, f"Off-hand diff in {tag} F{i:02d}: {off_diff}"

        up = Image.fromarray(im).resize((cell, cell), Image.NEAREST)
        x0, y0 = i * cell, r_idx * cell
        sheet.alpha_composite(up, (x0, y0))
        draw.rectangle([x0, y0, x0 + cell - 1, y0 + cell - 1], outline=(55, 62, 72, 255), width=1)
        draw.text((x0 + 8, y0 + 8), f"{tag} F{i:02d} (layers-off)\nx={xmin}..{xmax} y={ymin}..{ymax}", fill=(235, 240, 245, 255))

# Also verify Sword vs Axe distinctness!
for d in ["back_r", "back_l"]:
    diffs = []
    for i in range(1, 8):
        im_s = np.array(Image.open(CLEAN_ROOT / f"{d}_sword" / f"{i:02d}.png").convert("RGBA"))
        im_a = np.array(Image.open(CLEAN_ROOT / f"{d}_axe" / f"{i:02d}.png").convert("RGBA"))
        diffs.append(int(np.any(im_s != im_a, axis=2).sum()))
    print(f"{d} Sword vs Axe body pixel diffs F01..F07:", diffs)

sheet.save(SHEET_PATH)
print("Saved cleaned rear bodies sheet:", SHEET_PATH)
