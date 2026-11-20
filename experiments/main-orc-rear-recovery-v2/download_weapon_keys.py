import json
import base64

names = ['sword_slash_r', 'axe_chop_r', 'sword_slash_l', 'axe_chop_l']

for name in names:
    with open(f'experiments/main-orc-rear-recovery-v2/raw/res_poll_{name}.json') as f:
        data = json.load(f)
    img_b64 = data['content'][1]['data']
    out_p = f'experiments/main-orc-rear-recovery-v2/raw/{name}.png'
    with open(out_p, 'wb') as f:
        f.write(base64.b64decode(img_b64))
    print(f'Saved {out_p} ({len(img_b64)} chars)')
