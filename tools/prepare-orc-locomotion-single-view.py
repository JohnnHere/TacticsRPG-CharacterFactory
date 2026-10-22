import json,hashlib,shutil
from pathlib import Path
from PIL import Image
batches=json.loads(Path('characters/orc-locomotion-directions-batch-v1.json').read_text(encoding='utf-8'));new=[]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
rejected=json.loads(Path('tmp/orc-directions-rejected.json').read_text(encoding='utf-8'));folder=Path(batches[0]['folder']);shutil.copy2(rejected['source'],folder/'rejected-30-pose-attempt-01.png');rejected.update({'source':'rejected-30-pose-attempt-01.png','sourceSha256':sha(folder/'rejected-30-pose-attempt-01.png'),'promptFile':'sheet.prompt.md','promptSha256':sha(folder/'sheet.prompt.md'),'references':batches[0]['references']});(folder/'rejected-30-pose-attempt-01.json').write_text(json.dumps(rejected,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
for k,d in enumerate(['front_l','back_r','back_l']):
 full=Image.open('characters/orc-locomotion-directions-silhouettes-v1.png');full.crop((0,k*512,1536,(k+1)*512)).save(f'characters/orc-locomotion-{d}-silhouettes-v1.png')
for b in batches:
 spec=json.loads(Path(f"characters/{b['id']}/character.json").read_text(encoding='utf-8'))
 for d in ['front_l','back_r','back_l']:
  folder=Path(b['folder'])/d;folder.mkdir(parents=True,exist_ok=True)
  camera={'front_l':'three-quarter FRONT facing SCREEN LEFT, face and chest visible','back_r':'three-quarter BACK facing SCREEN RIGHT, occiput/back visible, NO frontal face or chest','back_l':'three-quarter BACK facing SCREEN LEFT, occiput/back visible, NO frontal face or chest'}[d]
  refs=[f'characters/orc-locomotion-{d}-silhouettes-v1.png',f"characters/{b['id']}/source/directions-v1/{d}/native-4x.png",f"{b['folder']}/approved-idle-front.png"]
  prompt=f'''Create ONE new pixel-art animation SOURCE SHEET for the SAME Orc {b['job']} in reference2. Exactly TEN separate complete figures: TWO horizontal rows of equal cells. TOP row FOUR Idle poses in first4 cells, last2 cells empty transparent. BOTTOM row SIX Walk poses, one per cell. Match reference1's layout/poses ONLY; reference1 has grey silhouettes with no outfit. Reference2 is the creator-approved native {d} outfit, proportions and camera. Reference3 is approved front Idle for restrained breathing amplitude only, NOT camera. All ten figures MUST have camera {camera}. This is {d}, not any other direction. Keep that viewpoint in BOTH rows, including all Walk frames. Do not show front face in rear views.

TOP Idle4: planted feet, quiet neutral exhale, tiny inhale, tiny peak, soft exhale. At peak at most ONE logical pixel chest expansion per side, never inflate torso or spread elbows. One-pixel maximum head/shoulder bob. Four genuinely distinct drawings, same pose/anatomy/outfit, loop4->1.
BOTTOM Walk6: reference1's exact six alternating foot poses in order. Right lead, right weight transfer/left passing, left step through, left lead, left weight transfer/right passing, right step through returning1. Include both halves of complete cycle, naturally counter-swing empty arms, restrained cloth movement. Never mirror a pose or retain the same leading foot for all6.

Outfit EXACTLY reference2: {spec['outfit']['description']}. Preserve rear garment shape, every strap, pouch, shoulder piece and asymmetric accessory on its correct anatomical side as visible in reference2. Never use heavy Warrior armor. {('Keep charcoal hood raised, open face only if front camera, rear hood on back view.' if spec['job']['id']=='rogue' else 'Keep entirely bald exposed scalp; no hair.')} Same mature olive Orc, compact robust body and tactical100-logical-pixel height, lower tusks and brutal face if visible in this camera. No held/carried/sheathed weapons, shields, bows, quivers, arrows, staffs, props or VFX.

Each full figure SAME size, head-to-body ratio and native logical pixel grid throughout. Generous transparent gaps, no touching, no cropped hands/boots, ample margins below bottom row. Chunky square logical pixels, deliberate clusters, 40-48-color native style, one-cell dark outline, upper-left light. No painted texture, blur, smooth gradients or antialiasing. Genuine transparent background; no ground shadow, scene, halo, checkerboard or labels. Exactly4 top and6 bottom figures, not12. Do NOT turn any character towards another camera. Independently drawn {d}, no image mirroring.'''
  (folder/'sheet.prompt.md').write_text(prompt+'\n',encoding='utf-8')
  new.append({'id':b['id'],'job':b['job'],'direction':d,'folder':folder.as_posix(),'promptFile':(folder/'sheet.prompt.md').as_posix(),'prompt':prompt,'references':[{'file':r,'sha256':sha(r)} for r in refs],'baseApprovalDigest':b['baseApprovalDigest'],'palette':b['palette']})
Path('characters/orc-locomotion-single-view-batch-v1.json').write_text(json.dumps(new,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('21 single-view sheets prepared; failed 30-pose source preserved.')
