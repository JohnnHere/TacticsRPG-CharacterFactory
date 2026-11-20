import json, hashlib

with open('experiments/main-orc-rear-recovery-v2/production-protection.json') as f:
    prot = json.load(f)

print(f"=== Checking {len(prot['files'])} Baseline Files Against Protection Snapshot ===")
tampered = 0
for rel, exp_sha in prot['files'].items():
    try:
        with open(rel, 'rb') as f:
            cur_sha = hashlib.sha256(f.read()).hexdigest()
        if cur_sha != exp_sha:
            print(f"[TAMPERED] {rel} expected={exp_sha} cur={cur_sha}")
            tampered += 1
    except Exception as e:
        print(f"[MISSING/ERROR] {rel}: {e}")
        tampered += 1

if tampered == 0:
    print(f"BASELINE 100% PROTECTED AND UNTOUCHED ({len(prot['files'])} files verified byte-identical)!")
else:
    print(f"ERROR: {tampered} baseline files modified!")
