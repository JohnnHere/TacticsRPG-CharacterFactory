import base64
import json
from io import BytesIO
from PIL import Image

base_path = 'experiments/main-orc-complete-v1/pixellab-recovery/back_r_base.png'
base_img = Image.open(base_path).convert('RGBA')
width, height = base_img.size

buf = BytesIO()
base_img.save(buf, format='PNG')
base_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

mask_img = Image.new('RGB', (width, height), (0, 0, 0))
mask_x, mask_y = 16, 66
mask_w, mask_h = 96, 62

for y in range(mask_y, mask_y + mask_h):
    for x in range(mask_x, mask_x + mask_w):
        mask_img.putpixel((x, y), (255, 255, 255))

mask_buf = BytesIO()
mask_img.save(mask_buf, format='PNG')
mask_b64 = base64.b64encode(mask_buf.getvalue()).decode('utf-8')

payload = {
    "description": "128x128 pixel art sprite of an armored orc warrior seen from behind 3/4 rear right view walking away from camera. Stride contact pose: left leg steps forward away into background with knee bent away; right leg trails behind with heel lifted showing rear boot heel and sole angled away. Popliteal knee creases, iron calf greaves, split leather tassets over chainmail, grounded on transparent background.",
    "image_base64": base_b64,
    "mask_image_base64": mask_b64,
    "crop_to_mask": True,
    "no_background": True,
    "seed": 20261027
}

with open('tmp/inpaint_walk_k2_req.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)

print("Wrote tmp/inpaint_walk_k2_req.json")
