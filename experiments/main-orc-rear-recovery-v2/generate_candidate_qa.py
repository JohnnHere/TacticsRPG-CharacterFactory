import os
from PIL import Image, ImageDraw, ImageFont

cand_dir = 'characters/orc-v1/source/rear-recovery-v2/back_r/Walk'
exp_dir = 'experiments/main-orc-rear-recovery-v2'

frames_128 = []
for i in range(8):
    p = os.path.join(exp_dir, f"walk_back_r_{i:02d}.png")
    frames_128.append(Image.open(p))

# 1. 4x2 Grid of the 8 frames (512 x 256)
grid = Image.new('RGBA', (128 * 4, 128 * 2), (20, 24, 28, 255))
draw = ImageDraw.Draw(grid)

for i, f in enumerate(frames_128):
    gx = (i % 4) * 128
    gy = (i // 4) * 128
    # draw ground guide line at y = 126 within cell
    draw.line([(gx, gy + 126), (gx + 127, gy + 126)], fill=(60, 70, 80, 255), width=1)
    grid.paste(f, (gx, gy), f)
    # text label
    draw.text((gx + 4, gy + 4), f"F{i:02d} (160ms)", fill=(200, 220, 240, 255))

grid_path = os.path.join(exp_dir, 'grid-walk-back_r-temporal-candidate.png')
grid.save(grid_path)
print(f"Saved {grid_path}")

# 2. Animated GIF at 1x speed (160ms per frame, 1280ms total)
gif_path = os.path.join(exp_dir, 'walk_back_r_temporal_loop.gif')
frames_128[0].save(
    gif_path,
    save_all=True,
    append_images=frames_128[1:],
    duration=160,
    loop=0,
    disposal=2
)
print(f"Saved {gif_path}")

# 3. Contact sheet (horizontal strip 1024x128)
sheet_path = os.path.join(exp_dir, 'contact_sheet_temporal_8f.png')
strip = Image.open(os.path.join(cand_dir, 'native-strip.png'))
strip.save(sheet_path)
print(f"Saved {sheet_path}")
