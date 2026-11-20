import json
from PIL import Image
import numpy as np

for d in ['front_r', 'front_l']:
    p = f'characters/orc-v1/source/complete-v1/{d}/Unarmed/clip.json'
    with open(p) as f:
        data = json.load(f)
    print(f'=== {d} Unarmed ===')
    print('totalDuration:', data.get('totalDurationMs'), 'durations:', data.get('durationsMs'))
    
    strip = Image.new('RGBA', (256 * len(data['frames']), 256))
    for fr in data['frames']:
        png = 'characters/orc-v1/source/complete-v1/' + fr['png'] if not fr['png'].startswith('characters') else fr['png']
        im = Image.open(png).convert('RGBA')
        arr = np.array(im)
        ys, xs = np.where(arr[:, :, 3] > 10)
        idx = fr['index']
        print(f"  Frame {idx:02d} ({fr.get('phase'):22s}, {fr.get('durationMs')}ms): bbox x=[{xs.min()},{xs.max()}] y=[{ys.min()},{ys.max()}] w={xs.max()-xs.min()+1} h={ys.max()-ys.min()+1}")
        strip.paste(im, (idx * 256, 0))
    strip.save(f'experiments/main-orc-rear-recovery-v2/front_unarmed_{d}_strip.png')
    print(f'Saved experiments/main-orc-rear-recovery-v2/front_unarmed_{d}_strip.png')
