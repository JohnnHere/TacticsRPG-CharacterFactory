import os
import json
import base64
from io import BytesIO
from PIL import Image

raw_dir = 'experiments/main-orc-rear-recovery-v2/raw'
os.makedirs(raw_dir, exist_ok=True)

# 1. Prepare back_l Walk request
p_back_l = 'experiments/main-orc-complete-v1/pixellab-recovery/back_l_base.png'
im_back_l = Image.open(p_back_l).convert('RGBA')
buf_l = BytesIO()
im_back_l.save(buf_l, format='PNG')
b64_back_l = base64.b64encode(buf_l.getvalue()).decode('utf-8')

req_walk_l = {
    "action": "armored orc warrior locomotion walk cycle seen from behind 3/4 rear left view walking away from camera towards northwest. Alternating natural strides: one supporting foot planted firmly on ground, opposite leg with clear swing and knee/foot lift, rear popliteal crease, calf greaves and angled boot heels, solid perspective on transparent background",
    "frame_count": 8,
    "first_frame_base64": b64_back_l,
    "last_frame_base64": b64_back_l,
    "no_background": True,
    "seed": 20261026
}

with open(os.path.join(raw_dir, 'req_walk_back_l.json'), 'w', encoding='utf-8') as f:
    json.dump(req_walk_l, f, ensure_ascii=False)
print("Wrote req_walk_back_l.json")

# 2. Prepare back_r Unarmed request
p_back_r = 'experiments/main-orc-complete-v1/pixellab-recovery/back_r_base.png'
im_back_r = Image.open(p_back_r).convert('RGBA')
buf_r = BytesIO()
im_back_r.save(buf_r, format='PNG')
b64_back_r = base64.b64encode(buf_r.getvalue()).decode('utf-8')

req_unarmed_r = {
    "action": "armored orc warrior unarmed melee strike attack seen from behind 3/4 rear right view facing away from camera. Compact punch attack: coils torso back with clenched heavy iron gauntlet, lunges forward with a powerful forward punch strike extending elbow and closed fist, impact pose followed by natural recoil and recovery back to resting pose. No weapons held, authentic rear plate armor and back perspective on transparent background",
    "frame_count": 8,
    "first_frame_base64": b64_back_r,
    "last_frame_base64": b64_back_r,
    "no_background": True,
    "seed": 20261026
}

with open(os.path.join(raw_dir, 'req_unarmed_back_r.json'), 'w', encoding='utf-8') as f:
    json.dump(req_unarmed_r, f, ensure_ascii=False)
print("Wrote req_unarmed_back_r.json")
