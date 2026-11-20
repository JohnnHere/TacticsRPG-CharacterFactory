import json
import base64
import time
import subprocess
import re
from pathlib import Path

ROOT = Path(".").resolve()
PYTHON = str(ROOT / "tmp/pixel-venv/Scripts/python.exe")
PIXELLAB_TOOL = str(ROOT / "tools/pixellab-mcp.py")

def get_balance():
    tmp_out = ROOT / "tmp/balance-temp.json"
    cmd = [PYTHON, PIXELLAB_TOOL, "--call", "get_balance", "--output", str(tmp_out)]
    subprocess.run(cmd, check=True)
    res = json.loads(tmp_out.read_text(encoding="utf-8"))
    txt = res["content"][0]["text"]
    for line in txt.splitlines():
        if "generations_remaining:" in line:
            return float(line.split(":")[1].strip())
    return None

def b64_of_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")

def run_animate_job(name: str, action: str, first_png: Path, last_png: Path, seed: int, out_dir: Path):
    req_path = out_dir / f"request-{name}.json"
    rec_path = out_dir / f"receipt-{name}.json"
    poll_req_path = out_dir / f"poll-{name}-request.json"
    
    first_b64 = b64_of_file(first_png)
    last_b64 = b64_of_file(last_png)
    
    req_body = {
        "action": action,
        "frame_count": 4,
        "first_frame_base64": first_b64,
        "last_frame_base64": last_b64,
        "no_background": True,
        "seed": seed
    }
    req_path.write_text(json.dumps(req_body, indent=2), encoding="utf-8")
    
    bal_before = get_balance()
    print(f"[{name}] Submitting animate_image... (Balance before: {bal_before})")
    
    cmd_sub = [PYTHON, PIXELLAB_TOOL, "--call", "animate_image", "--input", str(req_path), "--output", str(rec_path)]
    subprocess.run(cmd_sub, check=True)
    
    rec_data = json.loads(rec_path.read_text(encoding="utf-8"))
    rec_text = rec_data["content"][0]["text"]
    
    # parse job_id
    job_id = None
    for line in rec_text.splitlines():
        m = re.search(r"job_id:\s*([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", line)
        if m:
            job_id = m.group(1)
            break
    if not job_id:
        m2 = re.search(r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", rec_text)
        if m2:
            job_id = m2.group(1)
            
    print(f"[{name}] Job ID: {job_id}")
    if not job_id:
        raise RuntimeError(f"Could not parse job_id from {rec_text}")
        
    poll_req_path.write_text(json.dumps({"job_id": job_id}), encoding="utf-8")
    
    # Poll
    final_poll_data = None
    for attempt in range(1, 45):
        time.sleep(5)
        poll_res_path = out_dir / f"poll-{name}-{attempt:02d}.json"
        cmd_poll = [PYTHON, PIXELLAB_TOOL, "--call", "get_image", "--input", str(poll_req_path), "--output", str(poll_res_path)]
        subprocess.run(cmd_poll, check=True)
        
        poll_data = json.loads(poll_res_path.read_text(encoding="utf-8"))
        poll_text = poll_data["content"][0]["text"]
        print(f"[{name}] Poll {attempt}: status={'completed' if 'status: completed' in poll_text else 'processing'}")
        
        if "status: completed" in poll_text:
            final_poll_data = poll_data
            break
            
    if not final_poll_data:
        raise TimeoutError(f"Job {job_id} did not complete in time")
        
    # Extract frames
    frames = []
    idx = 0
    for item in final_poll_data.get("content", []):
        if item.get("type") == "image":
            img_b64 = item.get("data")
            raw_bytes = base64.b64decode(img_b64)
            img_path = out_dir / f"{name}-{idx}.png"
            img_path.write_bytes(raw_bytes)
            frames.append(img_path)
            idx += 1
            
    bal_after = get_balance()
    print(f"[{name}] Completed with {len(frames)} frames. Balance after: {bal_after} (Cost: {bal_before - bal_after if bal_before and bal_after else 'unknown'})")
    return frames
