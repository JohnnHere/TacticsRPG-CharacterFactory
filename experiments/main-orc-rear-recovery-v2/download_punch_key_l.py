import json
import base64

with open('experiments/main-orc-rear-recovery-v2/raw/res_poll_punch_key_l.json') as f:
    d = json.load(f)

img_entry = d['content'][1]
b64_data = img_entry['data']
out_path = 'experiments/main-orc-rear-recovery-v2/raw/punch_impact_key_back_l.png'

with open(out_path, 'wb') as f:
    f.write(base64.b64decode(b64_data))

print(f"Saved {out_path} ({len(b64_data)} b64 chars)")
