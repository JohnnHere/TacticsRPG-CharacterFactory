import os
import json
import base64
from io import BytesIO
from PIL import Image

raw_dir = 'experiments/main-orc-rear-recovery-v2/raw'
os.makedirs(raw_dir, exist_ok=True)

# Load back_r_base.png
p_base_r = 'experiments/main-orc-complete-v1/pixellab-recovery/back_r_base.png'
base_r = Image.open(p_base_r).convert('RGBA')
w, h = base_r.size

buf_r = BytesIO()
base_r.save(buf_r, format='PNG')
b64_r = base64.b64encode(buf_r.getvalue()).decode('utf-8')

# Mask for right side arm/torso: x in [45..126], y in [15..88]
mask_r = Image.new('RGB', (w, h), (0, 0, 0))
for y in range(15, 88):
    for x in range(45, 126):
        mask_r.putpixel((x, y), (255, 255, 255))

buf_mr = BytesIO()
mask_r.save(buf_mr, format='PNG')
b64_mr = base64.b64encode(buf_mr.getvalue()).decode('utf-8')

# Request 1: back_r Sword slash pose
req_sword_r = {
    "description": "128x128 pixel art sprite of an armored orc warrior seen from behind 3/4 rear right view in a one-handed sword slash attack pose. Right arm is raised and sweeping across in a powerful slashing motion, fist closed in a tight grip around an invisible sword hilt, empty hands with no weapon drawn, broad armored back with dorsal spine plate visible from behind, dynamic torso rotation driving the slash forward, clean pixel art on transparent background",
    "image_base64": b64_r,
    "mask_image_base64": b64_mr,
    "crop_to_mask": True,
    "no_background": True,
    "seed": 20261028
}

with open(os.path.join(raw_dir, 'req_sword_slash_r.json'), 'w', encoding='utf-8') as f:
    json.dump(req_sword_r, f, ensure_ascii=False)

# Request 2: back_r Axe overhead chop pose
req_axe_r = {
    "description": "128x128 pixel art sprite of an armored orc warrior seen from behind 3/4 rear right view in an overhead heavy axe chopping attack pose. Right arm is raised high above shoulder cocked back for a heavy overhead downward chop, fist closed in a tight grip around an invisible axe handle, empty hands with no weapon drawn, broad armored back with dorsal spine plate visible from behind, heavy shoulder commitment, clean pixel art on transparent background",
    "image_base64": b64_r,
    "mask_image_base64": b64_mr,
    "crop_to_mask": True,
    "no_background": True,
    "seed": 20261029
}

with open(os.path.join(raw_dir, 'req_axe_chop_r.json'), 'w', encoding='utf-8') as f:
    json.dump(req_axe_r, f, ensure_ascii=False)

print("Wrote req_sword_slash_r.json and req_axe_chop_r.json")
