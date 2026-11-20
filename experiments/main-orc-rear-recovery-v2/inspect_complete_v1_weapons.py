import json, glob, os

for dir_name in ['back_r', 'back_l']:
    for act in ['Sword', 'Axe', 'Defeat']:
        p = f'characters/orc-v1/source/complete-v1/{dir_name}/{act}/clip.json'
        if os.path.exists(p):
            with open(p) as f:
                d = json.load(f)
            print(f"{dir_name}/{act}: {len(d['frames'])} frames, durations={d.get('durationsMs')}")
            for fr in d['frames']:
                print(f"  idx={fr['index']} phase={fr.get('phase')} dur={fr.get('durationMs')} wepVis={fr.get('weaponVisible')}")
        else:
            print(f"{dir_name}/{act}: NOT FOUND")
