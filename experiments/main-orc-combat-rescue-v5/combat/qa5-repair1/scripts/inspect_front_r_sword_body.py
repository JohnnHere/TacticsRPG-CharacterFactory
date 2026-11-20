import os, json
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
SWORD_BODY_DIR = os.path.join(ROOT, "characters/orc-v1/source/combat-rescue-v5/combat/front_r/Sword/layers/body")
DIAG_DIR = os.path.join(ROOT, "experiments/main-orc-combat-rescue-v5/combat/qa5-repair1/diagnostics")
os.makedirs(DIAG_DIR, exist_ok=True)

# Let's render a 4x zoom sheet of the right arm/hand region on front_r/Sword F00..F12
# In 256x256 composite, the body sits in [64..191, 64..191].
# The right arm/gauntlet in front_r is on the viewer's right or center-right (x: 100..185, y: 80..165).
crop_box = (64, 68, 176, 172) # 112x104 region covering both arms and full torso
scale = 4
cell_w = (crop_box[2] - crop_box[0]) * scale
cell_h = (crop_box[3] - crop_box[1]) * scale

cols = 5
rows = 3
sheet = Image.new("RGBA", (cols * (cell_w + 8) + 8, rows * (cell_h + 24) + 8), (28, 32, 38, 255))
draw = ImageDraw.Draw(sheet)

for idx in range(13):
    p = os.path.join(SWORD_BODY_DIR, f"{idx:02d}.png")
    im = Image.open(p).convert("RGBA")
    sub = im.crop(crop_box).resize((cell_w, cell_h), Image.NEAREST)
    
    # Draw a 10px coordinate grid (in composite 256 coords) on the zoomed image
    sdraw = ImageDraw.Draw(sub)
    for gx in range(70, 176, 10):
        sx = (gx - crop_box[0]) * scale
        sdraw.line([(sx, 0), (sx, cell_h)], fill=(255, 255, 255, 60), width=1)
        sdraw.text((sx + 2, 2), str(gx), fill=(200, 220, 255, 180))
    for gy in range(70, 172, 10):
        sy = (gy - crop_box[1]) * scale
        sdraw.line([(0, sy), (cell_w, sy)], fill=(255, 255, 255, 60), width=1)
        sdraw.text((2, sy + 2), str(gy), fill=(200, 220, 255, 180))

    c = idx % cols
    r = idx // cols
    ox = 8 + c * (cell_w + 8)
    oy = 8 + r * (cell_h + 24)
    sheet.paste(sub, (ox, oy))
    draw.text((ox + 4, oy + cell_h + 4), f"front_r/Sword F{idx:02d} (body only, 256-coords)", fill=(240, 240, 240, 255))

out_path = os.path.join(DIAG_DIR, "front_r_sword_body_grid.png")
sheet.save(out_path)
print("Saved:", out_path)
