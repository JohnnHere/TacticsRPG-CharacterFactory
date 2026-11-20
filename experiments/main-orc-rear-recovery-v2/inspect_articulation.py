import numpy as np
from PIL import Image

for i in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
    im = Image.open(f'experiments/main-orc-rear-recovery-v2/raw/frames_unarmed_r/frame_{i:02d}.png').convert('RGBA')
    arr = np.array(im)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 10)
    print(f"frame_{i:02d}: x=[{xs.min()},{xs.max()}], y=[{ys.min()},{ys.max()}], w={xs.max()-xs.min()+1}, h={ys.max()-ys.min()+1}")

im_k = Image.open('experiments/main-orc-rear-recovery-v2/raw/punch_impact_key_back_r.png').convert('RGBA')
arr_k = np.array(im_k)
ys_k, xs_k = np.where(arr_k[:, :, 3] > 10)
print(f"impact_k: x=[{xs_k.min()},{xs_k.max()}], y=[{ys_k.min()},{ys_k.max()}], w={xs_k.max()-xs_k.min()+1}, h={ys_k.max()-ys_k.min()+1}")
