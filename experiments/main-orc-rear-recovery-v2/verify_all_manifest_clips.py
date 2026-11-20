import json
import os

with open('characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json') as f:
    manifest = json.load(f)

print(f"=== Validating {len(manifest['cells'])} Manifest Cells ===")
missing = 0
for cell in manifest['cells']:
    path = cell['clipJson']
    exists = os.path.exists(path)
    if not exists:
        print(f"[MISSING] {cell['cellId']} -> {path}")
        missing += 1
    else:
        # Check if valid JSON and has frames
        with open(path) as cf:
            cd = json.load(cf)
            num_fr = len(cd.get('frames', []))
            print(f"[OK] {cell['cellId']:16s} ({cell['status']:16s}) -> {path} ({num_fr} frames)")

if missing == 0:
    print("ALL 28 CELLS VERIFIED AND ACCESSIBLE!")
else:
    print(f"ERROR: {missing} cells missing clip.json!")
