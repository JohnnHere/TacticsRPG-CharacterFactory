from PIL import Image
import os

frames_dir = 'experiments/main-orc-rear-recovery-v2/raw/frames'

# 3x3 grid of all 9 frames
grid = Image.new('RGBA', (128 * 3, 128 * 3), (0, 0, 0, 0))
for i in range(9):
    p = os.path.join(frames_dir, f"frame_{i:02d}.png")
    im = Image.open(p)
    gx = (i % 3) * 128
    gy = (i // 3) * 128
    grid.paste(im, (gx, gy))

grid.save('experiments/main-orc-rear-recovery-v2/qa_grid_raw_9frames.png')
print("Saved experiments/main-orc-rear-recovery-v2/qa_grid_raw_9frames.png")

# Also save a 1x8 GIF preview (frames 0..7)
frames = [Image.open(os.path.join(frames_dir, f"frame_{i:02d}.png")) for i in range(8)]
frames[0].save(
    'experiments/main-orc-rear-recovery-v2/qa_raw_loop_8f.gif',
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0,
    disposal=2
)
print("Saved experiments/main-orc-rear-recovery-v2/qa_raw_loop_8f.gif")
