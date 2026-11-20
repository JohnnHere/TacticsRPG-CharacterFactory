import json

with open('characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json') as f:
    d = json.load(f)

for cell in d['cells']:
    print(f"{cell['direction']} {cell['action']}: status={cell['status']} candidateStatus={cell.get('candidateStatus')}")
