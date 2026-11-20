import json

with open('characters/orc-v1/source/complete-v1/back_r/Sword/Attack/clip.json') as f:
    d = json.load(f)

print('=== back_r Sword ===')
print('layerOrder:', d.get('layerOrder'))
print('visibleInterval:', d.get('visibleInterval'))
for fr in d['frames']:
    print(f"frame {fr['index']:02d}: phase={fr.get('phase'):22s} grip={fr.get('grip')} wepVis={fr.get('weaponVisible')} wepLayer={fr.get('weaponLayer')}")

with open('characters/orc-v1/source/complete-v1/back_r/Axe/Attack/clip.json') as f:
    da = json.load(f)

print('\n=== back_r Axe ===')
print('layerOrder:', da.get('layerOrder'))
print('visibleInterval:', da.get('visibleInterval'))
for fr in da['frames']:
    print(f"frame {fr['index']:02d}: phase={fr.get('phase'):22s} grip={fr.get('grip')} wepVis={fr.get('weaponVisible')} wepLayer={fr.get('weaponLayer')}")
