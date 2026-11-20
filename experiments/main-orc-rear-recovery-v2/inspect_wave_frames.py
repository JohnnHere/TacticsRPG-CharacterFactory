from PIL import Image
import os

raw_dir = 'experiments/main-orc-rear-recovery-v2/raw'

print("=== INSPECTION: back_l Walk (Job 64cd4cb7-dba7-4234-9f96-a9da268388fb) ===")
walk_l_dir = os.path.join(raw_dir, 'frames_walk_l')
for i in range(9):
    im = Image.open(os.path.join(walk_l_dir, f"frame_{i:02d}.png"))
    bbox = im.getbbox()
    bottom_y = bbox[3] - 1
    # Check feet
    pts = [(x, y) for y in range(110, 128) for x in range(128) if im.getpixel((x, y))[3] > 128]
    l_pts = [p for p in pts if p[0] < 64]
    r_pts = [p for p in pts if p[0] >= 64]
    l_max_y = max(p[1] for p in l_pts) if l_pts else 0
    r_max_y = max(p[1] for p in r_pts) if r_pts else 0
    print(f"Frame {i:02d}: top={bbox[1]}, bottom={bottom_y}, Left foot Y={l_max_y}, Right foot Y={r_max_y}")

print("\n=== INSPECTION: back_r Unarmed (Job 2ace783c-ff36-499b-b473-52adad36459e) ===")
unarmed_r_dir = os.path.join(raw_dir, 'frames_unarmed_r')
for i in range(9):
    im = Image.open(os.path.join(unarmed_r_dir, f"frame_{i:02d}.png"))
    bbox = im.getbbox()
    bottom_y = bbox[3] - 1
    # Check reach (max x and min x)
    opaque_pts = [(x, y) for y in range(128) for x in range(128) if im.getpixel((x, y))[3] > 128]
    cx = sum(p[0] for p in opaque_pts) / len(opaque_pts)
    cy = sum(p[1] for p in opaque_pts) / len(opaque_pts)
    print(f"Frame {i:02d}: top={bbox[1]}, bottom={bottom_y}, span_x=[{bbox[0]}..{bbox[2]-1}], cx={cx:.1f}, cy={cy:.1f}")
