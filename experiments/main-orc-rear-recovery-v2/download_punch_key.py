import urllib.request
from PIL import Image

job_id = '8ad79f7a-fa6e-47db-b002-8849121482f9'
url = f"https://api.pixellab.ai/mcp/images/{job_id}/download?index=0"
out_path = 'experiments/main-orc-rear-recovery-v2/raw/punch_impact_key_back_r.png'

req = urllib.request.Request(url, headers={'User-Agent': 'TacticsRPG-CharacterFactory/0.1'})
with urllib.request.urlopen(req) as resp, open(out_path, 'wb') as f:
    f.write(resp.read())

im = Image.open(out_path)
print(f"Downloaded punch key: size={im.size}, bbox={im.getbbox()}")
# inspect right arm / fist extension
pts = [(x, y) for y in range(20, 80) for x in range(85, 128) if im.getpixel((x, y))[3] > 128]
if pts:
    max_x = max(p[0] for p in pts)
    min_y = min(p[1] for p in pts)
    print(f"Right arm/fist extension: max_x={max_x}, min_y={min_y}")
