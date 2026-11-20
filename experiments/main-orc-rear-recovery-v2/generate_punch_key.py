import os
import json
import base64
from io import BytesIO
from PIL import Image

raw_dir = 'experiments/main-orc-rear-recovery-v2/raw'
os.makedirs(raw_dir, exist_ok=True)

# Load approved back_r_base.png
p_base = 'experiments/main-orc-complete-v1/pixellab-recovery/back_r_base.png'
base_img = Image.open(p_base).convert('RGBA')
w, h = base_img.size

buf = BytesIO()
base_img.save(buf, format='PNG')
base_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

# Create binary RGB mask
# Inpaint right torso and right arm (x >= 48, y in [18..88])
mask = Image.new('RGB', (w, h), (0, 0, 0))
for y in range(18, 88):
    for x in range(48, 126):
        mask.putpixel((x, y), (255, 255, 255))

buf_m = BytesIO()
mask.save(buf_m, format='PNG')
mask_b64 = base64.b64encode(buf_m.getvalue()).decode('utf-8')

payload = {
    "description": "128x128 pixel art sprite of an armored orc warrior seen from behind 3/4 rear right view throwing a powerful punch forward away into the distance. Right arm is fully extended in a forward right punch strike with straight elbow and closed iron gauntlet fist punching away into background towards upper right. Left arm in guard, broad armored back with dorsal spine plate visible from behind, dynamic torso commitment, clean pixel art on transparent background",
    "image_base64": base_b64,
    "mask_image_base64": mask_b64,
    "crop_to_mask": True,
    "no_background": True,
    "seed": 20261028
}

req_path = os.path.join(raw_dir, 'req_punch_impact_key.json')
with open(req_path, 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)

print(f"Wrote punch impact key request to {req_path}")
