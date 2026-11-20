import os
import json
import base64
from io import BytesIO
from PIL import Image

raw_dir = 'experiments/main-orc-rear-recovery-v2/raw'
os.makedirs(raw_dir, exist_ok=True)

# Load back_l_base.png
p_base_l = 'experiments/main-orc-complete-v1/pixellab-recovery/back_l_base.png'
base_l = Image.open(p_base_l).convert('RGBA')
w, h = base_l.size

buf_l = BytesIO()
base_l.save(buf_l, format='PNG')
b64_l = base64.b64encode(buf_l.getvalue()).decode('utf-8')

# Mask for left side arm/torso: x in [0..80], y in [15..88]
mask_l = Image.new('RGB', (w, h), (0, 0, 0))
for y in range(15, 88):
    for x in range(2, 80):
        mask_l.putpixel((x, y), (255, 255, 255))

buf_ml = BytesIO()
mask_l.save(buf_ml, format='PNG')
b64_ml = base64.b64encode(buf_ml.getvalue()).decode('utf-8')

# Request 1: back_l Sword slash pose
req_sword_l = {
    "description": "128x128 pixel art sprite of an armored orc warrior seen from behind 3/4 rear left view in a one-handed sword slash attack pose. Left arm is raised and sweeping across in a powerful slashing motion, fist closed in a tight grip around an invisible sword hilt, empty hands with no weapon drawn, broad armored back with dorsal spine plate visible from behind, dynamic torso rotation driving the slash forward, clean pixel art on transparent background",
    "image_base64": b64_l,
    "mask_image_base64": b64_ml,
    "crop_to_mask": True,
    "no_background": True,
    "seed": 20261028
}

with open(os.path.join(raw_dir, 'req_sword_slash_l.json'), 'w', encoding='utf-8') as f:
    json.dump(req_sword_l, f, ensure_ascii=False)

# Request 2: back_l Axe overhead chop pose
req_axe_l = {
    "description": "128x128 pixel art sprite of an armored orc warrior seen from behind 3/4 rear left view in an overhead heavy axe chopping attack pose. Left arm is raised high above shoulder cocked back for a heavy overhead downward chop, fist closed in a tight grip around an invisible axe handle, empty hands with no weapon drawn, broad armored back with dorsal spine plate visible from behind, heavy shoulder commitment, clean pixel art on transparent background",
    "image_base64": b64_l,
    "mask_image_base64": b64_ml,
    "crop_to_mask": True,
    "no_background": True,
    "seed": 20261029
}

with open(os.path.join(raw_dir, 'req_axe_chop_l.json'), 'w', encoding='utf-8') as f:
    json.dump(req_axe_l, f, ensure_ascii=False)

print("Wrote req_sword_slash_l.json and req_axe_chop_l.json")
