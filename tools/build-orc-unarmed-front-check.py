from pathlib import Path
p=Path('tools/check-orc-combat-front-preview.py').read_text(encoding='utf-8')
a=p.index('for clip in manifest');b=p.index('class Quiet',a)
p=p[:a]+"""for c in manifest['classes']:
    for i,f in enumerate(c['clips']['Attack']['frames']):expected[(c['id'],'Attack',i)]=hashlib.sha256(Image.open(root/'characters'/f).convert('RGBA').tobytes()).hexdigest()
"""+p[b:]
for old,new in [
 ('orc-combat-front-validation-v1.json','orc-unarmed-front-review-data-v1.json'),
 ('review-orc-combat-front-v1.html','review-orc-unarmed-front-v1.html'),
 ('==91','==40'),
 ("[('Attack',5),('Hit',3),('Defeat',5)]","[('Attack',5)]"),
 ("select_option('#state','Defeat')","select_option('#state','Attack')"),
 ("'loadedAnimationPng':91","'loadedAnimationPng':40"),
 ("'states':['Attack','Hit','Defeat']","'states':['Attack']"),
 ('orc-combat-front-{state.lower()}','orc-unarmed-front-{state.lower()}'),
 ('orc-combat-front-browser-v1.json','orc-unarmed-front-browser-v1.json'),
 ('PENDING_CREATOR_COMBAT_FRONT_REVIEW','PENDING_CREATOR_UNARMED_FRONT_REVIEW'),
 ('7 per state','8 per state'),('7/7 PASS','8/8 PASS'),
 ('91 PNGs loaded','40 PNGs loaded'),('91/91 canvas','40/40 canvas')]:p=p.replace(old,new)
Path('tools/check-orc-unarmed-front-preview.py').write_text(p,encoding='utf-8')
