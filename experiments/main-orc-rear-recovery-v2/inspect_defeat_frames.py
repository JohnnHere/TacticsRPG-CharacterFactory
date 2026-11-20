import json
from PIL import Image
import numpy as np

for d in ['front_r', 'back_r']:
    p = f'characters/orc-v1/source/complete-v1/{d}/Defeat/clip.json'
    with open(p) as f:
        data = json.load(f)
    print(f'=== {d} Defeat ===')
    for fr in data['frames']:
        png = fr['png']
        im = Image.open(png).convert('RGBA')
        arr = np.array(im)
        ys, xs = np.where(arr[:, :, 3] > 10)
        print(f"idx={fr['index']} phase={fr.get('phase')} dur={fr.get('durationMs')} bbox x=[{xs.min()},{xs.max()}] y=[{ys.min()},{ys.max()}] h={ys.max()-ys.min()+1}")
