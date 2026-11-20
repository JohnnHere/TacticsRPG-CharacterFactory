import json

for path in ['characters/orc-v1/source/complete-v1/front_r/Unarmed/clip.json', 'characters/orc-v1/source/complete-v1/back_r/Unarmed/clip.json']:
    with open(path) as f:
        d = json.load(f)
    print('===', path)
    for fr in d['frames']:
        print(f"idx={fr['index']} phase={fr.get('phase')} duration={fr.get('durationMs')} png={fr.get('png')}")
