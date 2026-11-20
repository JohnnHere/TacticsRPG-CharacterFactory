import os
import urllib.request

frames_dir = 'experiments/main-orc-rear-recovery-v2/raw/frames'
os.makedirs(frames_dir, exist_ok=True)

job_id = '1bdc9771-10f8-4a2a-ab7e-ce066a79175e'

for i in range(9):
    url = f"https://api.pixellab.ai/mcp/images/{job_id}/download?index={i}"
    out_path = os.path.join(frames_dir, f"frame_{i:02d}.png")
    print(f"Downloading frame {i} from {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'TacticsRPG-CharacterFactory/0.1'})
    with urllib.request.urlopen(req) as resp, open(out_path, 'wb') as f:
        f.write(resp.read())
    print(f"  Saved {out_path} ({os.path.getsize(out_path)} bytes)")

print("All 9 frames downloaded successfully.")
