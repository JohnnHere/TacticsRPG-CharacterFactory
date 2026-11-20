import json
import base64

for d in ['front_r', 'front_l']:
    with open(f'experiments/main-orc-rear-recovery-v2/raw/res_poll_defeat_{d}.json') as f:
        data = json.load(f)
    img_b64 = data['content'][1]['data']
    out_p = f'experiments/main-orc-rear-recovery-v2/raw/defeat_{d}_04_candidate.png'
    with open(out_p, 'wb') as f:
        f.write(base64.b64decode(img_b64))
    print(f'Saved {out_p} ({len(img_b64)} chars)')
