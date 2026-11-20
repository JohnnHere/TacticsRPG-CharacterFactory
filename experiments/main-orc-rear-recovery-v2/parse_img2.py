import json
import base64
from io import BytesIO
from PIL import Image

with open('tmp/get_img2_res.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for i, c in enumerate(d.get('content', [])):
    t = c.get('type')
    print(f"Item {i}: type={t}")
    if t == 'image':
        data = c.get('data')
        img = Image.open(BytesIO(base64.b64decode(data)))
        out_path = 'experiments/main-orc-rear-recovery-v2/walk_back_r_key_contact2.png'
        img.save(out_path)
        print(f"Saved image to {out_path}, size={img.size}, mode={img.mode}")
    elif t == 'text':
        print(f"Text: {c.get('text')[:300]}")
