import os
import json
import base64
from io import BytesIO
from PIL import Image

res_path = 'experiments/main-orc-rear-recovery-v2/raw/animate_walk_res.json'
frames_dir = 'experiments/main-orc-rear-recovery-v2/raw/frames'
os.makedirs(frames_dir, exist_ok=True)

with open(res_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

img_idx = 0
for c in d.get('content', []):
    if c.get('type') == 'text':
        print("API Response Text:\n", c.get('text'))
    elif c.get('type') == 'image':
        data = c.get('data')
        img = Image.open(BytesIO(base64.b64decode(data)))
        out_name = f"frame_{img_idx:02d}.png"
        out_path = os.path.join(frames_dir, out_name)
        img.save(out_path)
        bbox = img.getbbox()
        print(f"Extracted {out_name}: size={img.size}, bbox={bbox}")
        img_idx += 1

print(f"Total extracted frames: {img_idx}")
