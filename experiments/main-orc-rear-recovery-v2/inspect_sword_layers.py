import os
from PIL import Image
import numpy as np

for d in ['front_r', 'back_r']:
    print(f'=== {d} Sword layers ===')
    for i in [2, 5, 6, 7, 8, 10]:
        wb = f'characters/orc-v1/source/complete-v1/{d}/Sword/Attack/layers/weaponBack/{i:02d}.png'
        wf = f'characters/orc-v1/source/complete-v1/{d}/Sword/Attack/layers/weaponFront/{i:02d}.png'
        hf = f'characters/orc-v1/source/complete-v1/{d}/Sword/Attack/layers/handFront/{i:02d}.png'
        
        has_wb = os.path.exists(wb) and np.sum(np.array(Image.open(wb))[:, :, 3] > 10) > 0
        has_wf = os.path.exists(wf) and np.sum(np.array(Image.open(wf))[:, :, 3] > 10) > 0
        has_hf = os.path.exists(hf) and np.sum(np.array(Image.open(hf))[:, :, 3] > 10) > 0
        print(f"frame {i:02d}: weaponBack={has_wb}, weaponFront={has_wf}, handFront={has_hf}")
