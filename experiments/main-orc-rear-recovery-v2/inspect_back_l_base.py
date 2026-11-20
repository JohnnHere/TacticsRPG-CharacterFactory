from PIL import Image
import numpy as np

img = Image.open('characters/orc-v1/source/complete-v1/back_l/Directions/base.png').convert('RGBA')
arr = np.array(img)
ys, xs = np.where(arr[:, :, 3] > 10)
print(f"back_l base composite bbox x=[{xs.min()},{xs.max()}] y=[{ys.min()},{ys.max()}] w={xs.max()-xs.min()+1}")
print(f"native (offset -64,-64): x=[{xs.min()-64},{xs.max()-64}] y=[{ys.min()-64},{ys.max()-64}]")
