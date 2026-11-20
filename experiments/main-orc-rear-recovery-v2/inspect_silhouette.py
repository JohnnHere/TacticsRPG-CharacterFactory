from PIL import Image
import os

frames_dir = 'experiments/main-orc-rear-recovery-v2/raw/frames'

for i in range(9):
    p = os.path.join(frames_dir, f"frame_{i:02d}.png")
    im = Image.open(p)
    
    # Calculate non-zero pixel count in lower half (y >= 75)
    lower_pts = [(x, y) for y in range(75, 128) for x in range(128) if im.getpixel((x, y))[3] > 128]
    # Calculate head top (minimum y where alpha > 128)
    head_y = min(y for y in range(128) for x in range(128) if im.getpixel((x, y))[3] > 128)
    
    # Calculate centroid of lower body
    avg_x = sum(p[0] for p in lower_pts) / len(lower_pts)
    avg_y = sum(p[1] for p in lower_pts) / len(lower_pts)
    
    print(f"Frame {i:02d}: head_y={head_y}, lower_pixels={len(lower_pts)}, lower_cx={avg_x:.2f}, lower_cy={avg_y:.2f}")
