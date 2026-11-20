import os
import json
import base64
from io import BytesIO
from PIL import Image

raw_dir = 'experiments/main-orc-rear-recovery-v2/raw'
os.makedirs(raw_dir, exist_ok=True)

# Load native 04
base_img = Image.open('experiments/main-orc-rear-recovery-v2/raw/defeat_front_r_04_native.png').convert('RGBA')
w, h = base_img.size

buf = BytesIO()
base_img.save(buf, format='PNG')
base_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

# Create binary RGB mask
# Mask upper torso, arms and head: x in [35..126], y in [45..126]
mask = Image.new('RGB', (w, h), (0, 0, 0))
for y in range(45, 126):
    for x in range(35, 126):
        mask.putpixel((x, y), (255, 255, 255))

buf_m = BytesIO()
mask.save(buf_m, format='PNG')
mask_b64 = base64.b64encode(buf_m.getvalue()).decode('utf-8')

payload = {
    "description": "128x128 pixel art sprite of an armored orc warrior seen from 3/4 front right perspective completely collapsed flat on the ground defeated and incapacitated. Heavy torso, chest plate and pauldrons are collapsed completely flat against the dirt ground, arms limp and sprawled out on the ground with elbows bent limp at sides, head resting limp against the dirt face down sideways, defeated unconscious pose, maintaining heavy armor plates and dark iron volume on ground, clean pixel art on transparent background",
    "image_base64": base_b64,
    "mask_image_base64": mask_b64,
    "crop_to_mask": True,
    "no_background": True,
    "seed": 20261028
}

req_path = os.path.join(raw_dir, 'req_defeat_front_r.json')
with open(req_path, 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)

print(f"Wrote defeat request for front_r to {req_path}")
