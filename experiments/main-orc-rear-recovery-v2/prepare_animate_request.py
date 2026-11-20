import os
import json
import base64
from io import BytesIO
from PIL import Image

raw_dir = 'experiments/main-orc-rear-recovery-v2/raw'
os.makedirs(raw_dir, exist_ok=True)

# Load approved back_r_base.png
base_path = 'experiments/main-orc-complete-v1/pixellab-recovery/back_r_base.png'
base_img = Image.open(base_path).convert('RGBA')

buf = BytesIO()
base_img.save(buf, format='PNG')
base_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

# Prepare payload for animate_image
# frame_count = 8 (even number per schema)
# first_frame_base64 = approved back_r_base
# last_frame_base64 = approved back_r_base (pinned loop)
# action = clear away-facing alternating support/pass/lift prompt
payload = {
    "action": "armored orc warrior locomotion walk cycle seen from behind 3/4 rear right view walking away from camera. Alternating natural strides: one supporting foot planted firmly on ground, opposite leg with clear swing and knee/foot lift, rear popliteal crease, calf greaves and angled boot heels, solid perspective on transparent background",
    "frame_count": 8,
    "first_frame_base64": base_b64,
    "last_frame_base64": base_b64,
    "no_background": True,
    "seed": 20261026
}

req_path = os.path.join(raw_dir, 'animate_walk_req.json')
with open(req_path, 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)

print(f"Wrote animate_image request to {req_path}")
