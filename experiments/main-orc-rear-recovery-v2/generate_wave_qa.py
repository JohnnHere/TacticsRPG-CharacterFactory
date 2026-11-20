import os
from PIL import Image, ImageDraw

exp_dir = 'experiments/main-orc-rear-recovery-v2'

# 1. back_l Walk QA (8 frames)
frames_walk_l = [Image.open(os.path.join(exp_dir, f"walk_back_l_{i:02d}.png")) for i in range(8)]

grid_walk_l = Image.new('RGBA', (128 * 4, 128 * 2), (20, 24, 28, 255))
draw_l = ImageDraw.Draw(grid_walk_l)
for i, f in enumerate(frames_walk_l):
    gx = (i % 4) * 128
    gy = (i // 4) * 128
    draw_l.line([(gx, gy + 126), (gx + 127, gy + 126)], fill=(60, 70, 80, 255), width=1)
    grid_walk_l.paste(f, (gx, gy), f)
    draw_l.text((gx + 4, gy + 4), f"F{i:02d} (160ms)", fill=(200, 220, 240, 255))

grid_walk_l_path = os.path.join(exp_dir, 'grid-walk-back_l-temporal-candidate.png')
grid_walk_l.save(grid_walk_l_path)
print(f"Saved {grid_walk_l_path}")

gif_walk_l_path = os.path.join(exp_dir, 'walk_back_l_temporal_loop.gif')
frames_walk_l[0].save(
    gif_walk_l_path,
    save_all=True,
    append_images=frames_walk_l[1:],
    duration=160,
    loop=0,
    disposal=2
)
print(f"Saved {gif_walk_l_path}")

# 2. back_r Unarmed QA (9 frames)
frames_unarmed_r = [Image.open(os.path.join(exp_dir, f"unarmed_back_r_{i:02d}.png")) for i in range(9)]
durations_ms = [40, 60, 60, 50, 50, 80, 60, 80, 100]

grid_unarmed_r = Image.new('RGBA', (128 * 3, 128 * 3), (20, 24, 28, 255))
draw_u = ImageDraw.Draw(grid_unarmed_r)
labels = ["Rest", "Antic.1", "Coil.2", "Lunge.3", "Thrust.4", "Impact.5", "Recoil.6", "Recover.7", "Terminal.8"]

for i, f in enumerate(frames_unarmed_r):
    gx = (i % 3) * 128
    gy = (i // 3) * 128
    draw_u.line([(gx, gy + 126), (gx + 127, gy + 126)], fill=(60, 70, 80, 255), width=1)
    grid_unarmed_r.paste(f, (gx, gy), f)
    draw_u.text((gx + 4, gy + 4), f"F{i:02d} {labels[i]} ({durations_ms[i]}ms)", fill=(240, 210, 180, 255))

grid_unarmed_r_path = os.path.join(exp_dir, 'grid-unarmed-back_r-candidate.png')
grid_unarmed_r.save(grid_unarmed_r_path)
print(f"Saved {grid_unarmed_r_path}")

gif_unarmed_r_path = os.path.join(exp_dir, 'unarmed_back_r_candidate.gif')
frames_unarmed_r[0].save(
    gif_unarmed_r_path,
    save_all=True,
    append_images=frames_unarmed_r[1:],
    duration=durations_ms,
    loop=0,
    disposal=2
)
print(f"Saved {gif_unarmed_r_path}")
