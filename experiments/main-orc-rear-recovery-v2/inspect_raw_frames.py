import os
from PIL import Image

frames_dir = 'experiments/main-orc-rear-recovery-v2/raw/frames'

print("=== Raw Animation Frames Inspection ===")
for i in range(9):
    p = os.path.join(frames_dir, f"frame_{i:02d}.png")
    im = Image.open(p)
    bbox = im.getbbox()
    bottom_y = bbox[3] - 1
    
    # Analyze feet at y >= 110
    pts = [(x, y) for y in range(110, 128) for x in range(128) if im.getpixel((x, y))[3] > 128]
    if pts:
        l_pts = [p for p in pts if p[0] < 64]
        r_pts = [p for p in pts if p[0] >= 64]
        l_min_y = min(p[1] for p in l_pts) if l_pts else None
        l_max_y = max(p[1] for p in l_pts) if l_pts else None
        r_min_y = min(p[1] for p in r_pts) if r_pts else None
        r_max_y = max(p[1] for p in r_pts) if r_pts else None
        print(f"Frame {i:02d}: top={bbox[1]}, bottom={bottom_y}, Left foot Y=({l_min_y}..{l_max_y}), Right foot Y=({r_min_y}..{r_max_y})")
    else:
        print(f"Frame {i:02d}: bbox={bbox}")
