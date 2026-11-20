import os
import urllib.request
import json

raw_dir = 'experiments/main-orc-rear-recovery-v2/raw'

def download_frames(job_id, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print(f"Downloading frames for job {job_id} into {out_dir}...")
    for i in range(9):
        url = f"https://api.pixellab.ai/mcp/images/{job_id}/download?index={i}"
        out_path = os.path.join(out_dir, f"frame_{i:02d}.png")
        req = urllib.request.Request(url, headers={'User-Agent': 'TacticsRPG-CharacterFactory/0.1'})
        with urllib.request.urlopen(req) as resp, open(out_path, 'wb') as f:
            f.write(resp.read())
        print(f"  Frame {i:02d}: {os.path.getsize(out_path)} bytes")

if __name__ == '__main__':
    job_walk_l = '64cd4cb7-dba7-4234-9f96-a9da268388fb'
    job_unarmed_r = '2ace783c-ff36-499b-b473-52adad36459e'
    download_frames(job_walk_l, os.path.join(raw_dir, 'frames_walk_l'))
    download_frames(job_unarmed_r, os.path.join(raw_dir, 'frames_unarmed_r'))
    print("Done downloading wave frames.")
