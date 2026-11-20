import json
import base64
from PIL import Image
from io import BytesIO

with open('tmp/inpaint_walk_k1_res.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for i, c in enumerate(d.get('content', [])):
    t = c.get('type')
    print(f"Item {i}: type={t}")
    if t == 'image':
        data = c.get('data')
        mime = c.get('mimeType')
        print(f"  mime={mime}, length={len(data)}")
        img = Image.open(BytesIO(base64.b64decode(data)))
        out_path = 'experiments/main-orc-rear-recovery-v2/walk_back_r_key_contact1.png'
        img.save(out_path)
        print(f"  Saved image to {out_path}, size={img.size}, mode={img.mode}")
    elif t == 'text':
        print(f"  text: {c.get('text')[:300]}")
