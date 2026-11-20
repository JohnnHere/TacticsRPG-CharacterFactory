import json, hashlib
from pathlib import Path

ROOT = Path('.').resolve()
EXP_GRIP = ROOT / 'experiments/main-orc-combat-rescue-v5/grip-specialist'
CHAR_GRIP = ROOT / 'characters/orc-v1/source/combat-rescue-v5/grip-specialist'

def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

dirs = ['front_l-Sword-full', 'front_r-Axe-full', 'front_l-Axe-full']

for d in dirs:
    exp_d = EXP_GRIP / d
    char_d = CHAR_GRIP / d
    
    cp_path = exp_d / 'checkpoint.json'
    cp = json.loads(cp_path.read_text(encoding='utf-8'))
    
    cp['clipSha256'] = sha256_file(char_d / 'clip.json')
    cp['masterSha256'] = sha256_file(char_d / 'source/composite.aseprite')
    cp['representativeSha256'] = sha256_file(char_d / 'representative.json')
    cp['checksSha256'] = sha256_file(exp_d / 'checks.json')
    cp['previewSha256'] = sha256_file(exp_d / 'index.html')
    if (exp_d / 'preview-check.json').exists():
        cp['previewCheckSha256'] = sha256_file(exp_d / 'preview-check.json')
    
    # Save checkpoint.json
    cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (char_d / 'checkpoint.json').write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    
    # Now update report.md with reportSha256 if needed
    rep_path = exp_d / 'report.md'
    cp['reportSha256'] = sha256_file(rep_path)
    
    cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (char_d / 'checkpoint.json').write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Updated checkpoint.json for {d} (SHA: {sha256_file(cp_path)})")

print("All checkpoints updated.")
