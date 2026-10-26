"""Read-only art audit, protection hashes and QA previews; never edits authored raster."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,subprocess,shutil
R=Path(__file__).resolve().parents[1];E=R/'experiments/main-orc-weapon-rescue-v3';E.mkdir(parents=True,exist_ok=True)
read=lambda p:json.loads((R/p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (E/'protected-art.json').exists():
 protected={str(p.relative_to(R)).replace('\\','/'):sha(p) for folder in ['characters','assets/weapons','ideas'] for p in (R/folder).rglob('*') if p.is_file() and p.suffix.lower() in ['.png','.aseprite','.ase']}
 (E/'protected-art.json').write_text(json.dumps(protected,indent=2),encoding='utf-8')
 (E/'initial-git-status.txt').write_text(subprocess.check_output(['git','status','--short'],cwd=R).decode('utf-8'),encoding='utf-8')
 shutil.copytree(R/'Biblioteca de Arte/Personagens Jogaveis/Orc V1',E/'previous-review')
 for p in ['characters/orc-v1/character.json','characters/orc-v1/assets.json','characters/orc-v1/source/equipment-current.json','assets/weapons/recruit-sword/weapon.json','assets/weapons/militia-axe/weapon.json']:
  target=E/'before-metadata'/p;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/p,target)
report={'status':'AUDITED_BEFORE_ART_CHANGES','character':read('reports/orc-production-current.json'),'sourceTruth':{'concept':'characters/orc-v1/concepts/concept-selected.png','master':'characters/orc-v1/source/aseprite/concept-selected.aseprite','idle':'characters/orc-v1/source/studies/Idle/clip.json','walk':'characters/orc-v1/source/studies/Walk/clip.json','rejectedEquipment':'characters/orc-v1/source/equipment-v2/equipment-manifest.json'},'weapons':{},'findings':{'artwork':'Axe head and haft oversized. Sword hilt/guard need one-hand proportion check.','body':'V2 skeleton request changes only right-arm joints; torso, shoulder, hips and feet fixed. Garment/legs frozen in composition.','composition':'Hand-independent angle track 250..610 degrees, common rotated palm/fingers instead of pose-specific anatomy; weapon always front, no perspective views.','playback':'Same 1315ms family for Sword/Axe, full circular recovery; persistent armed rest/walk conflicts with latest decision.','preview':'Actual PNGs/timings match canvas; no preview smoothing/scale mismatch explains the artistic failures.','gates':'Character selected for future integration. reviews.json empty; no full direction/runtime gates. V1 and V2 attacks artistically rejected.','conflicts':['AGENTS/ASEPRITE/handoff historical V4 active counts are obsolete; only orc-v1 is current.','character.json equipmentPreview points to v1 while equipment-current/config point to v2.','character appearance body still says grey despite selected green masters.','Persistent armed Idle/Walk and shared Sword/Axe motion explicitly superseded by latest request.']},'policy':{'Idle':False,'Walk':False,'Rest':False,'Inspection':False,'Attack':'Declared visible interval only','Hit':False,'Defeat':False,'AfterAttack':False},'scope':'Two separate front_r attack profiles; no Unity, other views or jobs; no automatic artistic approval'}
for wid in ['recruit-sword','militia-axe']:
 w=read(f'assets/weapons/{wid}/weapon.json');im=Image.open(R/w['sprite']).convert('RGBA');bbox=im.getbbox();report['weapons'][wid]={'metadata':w,'bbox':bbox,'heightPx':bbox[3]-bbox[1],'widthPx':bbox[2]-bbox[0]}
 scale=6;out=Image.new('RGB',(606,606),(40,45,49));out.paste(im.resize((576,576),Image.Resampling.NEAREST),(30,30),im.resize((576,576),Image.Resampling.NEAREST));d=ImageDraw.Draw(out)
 for n in range(0,96,10):
  d.line((30+n*6,30,30+n*6,606),fill=(60,70,75));d.text((30+n*6,10),str(n),fill='white');d.line((30,30+n*6,606,30+n*6),fill=(60,70,75));d.text((5,30+n*6),str(n),fill='white')
 out.save(E/f'{wid}-before-grid.png')
(E/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'protectedArtFiles':len(read('experiments/main-orc-weapon-rescue-v3/protected-art.json')),'weapons':{k:{'width':v['widthPx'],'height':v['heightPx']} for k,v in report['weapons'].items()},'audit':str(E/'audit.json')}))
