from PIL import Image
import os

frames_dir = 'experiments/main-orc-rear-recovery-v2/raw/frames'

for i in range(9):
    p = os.path.join(frames_dir, f"frame_{i:02d}.png")
    im = Image.open(p)
    
    # Analyze left leg vs right leg
    # In back_r (facing northeast / away to the right):
    # Left leg is the near/camera-left leg (x in 25..55)
    # Right leg is the far/camera-right leg (x in 70..105)
    
    l_pts = [(x, y) for y in range(80, 128) for x in range(20, 60) if im.getpixel((x, y))[3] > 128]
    r_pts = [(x, y) for y in range(80, 128) for x in range(65, 105) if im.getpixel((x, y))[3] > 128]
    
    l_max_y = max(p[1] for p in l_pts) if l_pts else 0
    r_max_y = max(p[1] for p in r_pts) if r_pts else 0
    
    l_min_x = min(p[0] for p in l_pts) if l_pts else 0
    l_max_x = max(p[0] for p in l_pts) if l_pts else 0
    r_min_x = min(p[0] for p in r_pts) if r_pts else 0
    r_max_x = max(p[0] for p in r_pts) if r_pts else 0
    
    # Classify phase
    phase = "Passing/Base"
    if l_max_y < r_max_y - 2:
        phase = f"Left leg lifted ({l_max_y}) / Right planted ({r_max_y})"
    elif r_max_y < l_max_y - 2:
        phase = f"Right leg lifted ({r_max_y}) / Left planted ({l_max_y})"
    else:
        phase = f"Both feet near ground (L={l_max_y}, R={r_max_y})"
        
    print(f"Frame {i:02d}: {phase} | L_span=[{l_min_x}..{l_max_x}] R_span=[{r_min_x}..{r_max_x}]")
