from pathlib import Path
import json,hashlib
E=Path('experiments/main-orc-rear-reconstruction-v4/specialist');R=E/'recovery'
assert Path.cwd().name=='TacticsRPG-CharacterFactory'
R.mkdir(exist_ok=True)
# The prepared artwork/params are retained. The author script already contains
# the authorized technical recovery patch; inventory distinguishes that fact.
before={str(p).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(E.rglob('*'))if p.is_file()and 'profile'not in p.parts and 'recovery'not in p.parts and p.name!='author-impact.lua'}
(R/'retained-partial-inventory.json').write_text(json.dumps(before,indent=2)+'\n',encoding='utf-8')
(R/'before-params.lua').write_bytes((E/'params.lua').read_bytes())
p=(E/'params.lua').read_text(encoding='utf-8')
assert "name = 'iter02'"in p and "outDir = 'experiments/main-orc-rear-reconstruction-v4/specialist/iter'"in p
p=p.replace("name = 'iter02'","name = 'impact-recovered'").replace("outDir = 'experiments/main-orc-rear-reconstruction-v4/specialist/iter'","outDir = 'characters/orc-v1/source/rear-reconstruction-v4-specialist/impact-recovered'")
(R/'params-frozen.lua').write_text(p,encoding='utf-8')
print('Retained partial artifacts inventoried:',len(before))
