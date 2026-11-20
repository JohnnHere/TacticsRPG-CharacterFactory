import json

with open('characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json') as f:
    d = json.load(f)

for cell in d['cells']:
    if 'Sword' in cell['action'] or 'Axe' in cell['action']:
        print(f"{cell['direction']} {cell['action']}: {cell['clipJson']}")
