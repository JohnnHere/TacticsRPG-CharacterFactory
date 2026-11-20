from PIL import Image
import numpy as np

base = Image.open('experiments/main-orc-rear-recovery-v2/raw/frames_unarmed_r/frame_00.png').convert('RGBA')
key = Image.open('experiments/main-orc-rear-recovery-v2/raw/punch_impact_key_back_r.png').convert('RGBA')

arr_b = np.array(base)
arr_k = np.array(key)

# Let's inspect the pixels where key has green skin or dark outline in the neck/head region:
# y from 6 to 35, x from 55 to 80
for y in range(6, 36):
    row_b = []
    row_k = []
    for x in range(50, 85):
        pb = arr_b[y, x]
        pk = arr_k[y, x]
        cb = '#' if pb[3] > 10 and pb[1] > pb[0] else ('.' if pb[3] > 10 else ' ')
        ck = '#' if pk[3] > 10 and pk[1] > pk[0] else ('.' if pk[3] > 10 else ' ')
        row_b.append(cb)
        row_k.append(ck)
    print(f"y={y:02d} b: {''.join(row_b)} | k: {''.join(row_k)}")
