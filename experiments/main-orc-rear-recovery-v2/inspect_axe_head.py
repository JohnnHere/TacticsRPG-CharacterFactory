from PIL import Image
import numpy as np

for name in ['clean_axe_chop_r', 'clean_axe_chop_l']:
    im = Image.open(f'experiments/main-orc-rear-recovery-v2/raw/{name}.png').convert('RGBA')
    arr = np.array(im)
    alpha = arr[:, :, 3]
    # Check green pixels in head column x in [45..75]
    for y in range(0, 30):
        row = arr[y, 45:75]
        green_pts = np.where((row[:, 3] > 10) & (row[:, 1] > row[:, 0]))[0]
        if len(green_pts) > 0:
            print(f"{name} y={y:02d}: {len(green_pts)} green pixels")
