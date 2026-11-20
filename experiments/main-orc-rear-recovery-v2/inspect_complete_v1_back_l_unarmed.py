import json
from PIL import Image
import numpy as np

with open('characters/orc-v1/source/complete-v1/back_l/Unarmed/clip.json') as f:
    d = json.load(f)

print(f"back_l/Unarmed: {len(d['frames'])} frames, durations={d.get('durationsMs')}")
for fr in d['frames']:
    img = Image.open(fr['png']).convert('RGBA')
    arr = np.array(img)
    ys, xs = np.where(arr[:, :, 3] > 10)
    print(f"idx={fr['index']} phase={fr['phase']} bbox x=[{xs.min()},{xs.max()}] y=[{ys.min()},{ys.max()}] w={xs.max()-xs.min()+1}")
