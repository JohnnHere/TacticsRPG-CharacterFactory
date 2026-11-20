import json, os

for dir_name in ['back_r', 'back_l', 'front_r', 'front_l']:
    for weapon in ['Sword', 'Axe']:
        p = f'characters/orc-v1/source/complete-v1/{dir_name}/{weapon}/Attack/clip.json'
        if os.path.exists(p):
            with open(p) as f:
                d = json.load(f)
            print(f"{dir_name}/{weapon}: {len(d['frames'])} frames, totalDur={sum(d.get('durationsMs', []))}ms")
            for fr in d['frames']:
                print(f"  idx={fr['index']} phase={fr.get('phase')} dur={fr.get('durationMs')} wepVis={fr.get('weaponVisible')} wepLayer={fr.get('weaponLayer')}")
        else:
            print(f"{dir_name}/{weapon}: NOT FOUND at {p}")
