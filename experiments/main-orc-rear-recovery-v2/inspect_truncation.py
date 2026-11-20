from PIL import Image
import numpy as np

im2 = Image.open('characters/orc-v1/source/complete-v1/front_r/Unarmed/02.png').convert('RGBA')
arr2 = np.array(im2)
# Find the truncated edge on right side (x in [150..170], y in [130..160] composite)
for y in range(130, 160, 2):
    xs = np.where(arr2[y, :, 3] > 10)[0]
    if len(xs) > 0:
        print(f"y={y}: xs=[{xs.min()},{xs.max()}] edge_color={arr2[y, xs.max()][:3]}")
