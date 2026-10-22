import hashlib,json
from pathlib import Path
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
batches=json.loads(Path('characters/orc-combat-directions-batch-v2.json').read_text(encoding='utf-8'));calls=[]
for b in batches:
 rear=b['direction']=='back_l';archer=b['id']=='orc-01-archer' and b['direction']=='front_l'
 if not (rear and b['id'] not in ['orc-01-squire','orc-01-archer'] or archer):continue
 folder=Path(b['folder']);name='attack-hands-v3'
 if archer:
  body='Three-quarter FRONT looking SCREEN LEFT. The anatomical LEFT shoulder is at the RIGHT side of the image, with LEFT arm extending ACROSS THE CHEST towards screen left. RIGHT shoulder is at image LEFT, RIGHT elbow bends backwards to screen right, RIGHT fist draws beside the left-facing cheek. Never aim with the arm attached to the image-left shoulder. Think left-handed position in the image but anatomically right-handed archer.'
 else:
  body='Three-quarter BACK looking SCREEN LEFT. Anatomical RIGHT shoulder is on the RIGHT SIDE OF THE IMAGE. The ACTIVE arm MUST start at that image-RIGHT shoulder. Reach that right arm diagonally ACROSS BEHIND/ABOVE THE HEAD towards screen left. Anatomical LEFT shoulder at image LEFT stays LOW, its hand near stomach and mostly hidden. Do NOT extend or lift the image-left upper arm. Viewer sees the active RIGHT upper arm along the RIGHT edge of the back. The fist/palm can reach left only by crossing ABOVE the back/head. Rear shoulder blade muscles and garment back stay visible. Do not turn the chest towards camera.'
 action=b['action']['poses'].replace('screen right','screen left').replace('screen-right','screen-left')
 prompt=f'''Draw FIVE new chronological Attack pixel-art poses of the SAME Orc {b['job']} in reference1, one horizontal row with generous transparent margins and empty gaps. Correct anatomical handedness is the main purpose. {body}

Sequence: {action}

Reference1 is the approved outfit and camera. Reference2 is only the current attempted motion: its action ARM IS WRONG and MUST BE RE-DRAWN using the opposite anatomical arm as specified above. Keep its outfit, identity and rear/front camera, but correct the arm connection. Do not copy the erroneous image-left active arm in rear views. Exactly FIVE complete full-body figures with fully visible hands/boots, stable physical scale, logical standing height100 pixels, maximum logical width116 pixels. Especially the Rogue: compact short step, no long stretched rear leg. All hands EMPTY, NO weapon, bow, string, arrow, quiver, dagger, shield, staff, orb, projectile, effect or carried object. Clothing matches approved reference1 exactly. Bald mature robust olive Orc, Rogue's charcoal hood stays raised. Crisp squared chunky pixels, own-outfit palette, dark outline, no AA. True transparent background, no haze/shadow/ground/text. Re-draw anatomy independently; do not mirror an existing image.'''
 refs=[b['references'][0],{'file':str(folder/'sheet.png').replace('\\','/'),'sha256':sha(folder/'sheet.png')}]
 (folder/f'{name}.prompt.md').write_text(prompt,encoding='utf-8')
 calls.append({**b,'generationName':name,'generationStates':{'Attack':5},'prompt':prompt,'promptFile':str(folder/f'{name}.prompt.md').replace('\\','/'),'references':refs})
Path('characters/orc-combat-hands-v3.json').write_text(json.dumps(calls,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(len(calls),'targeted right-hand corrections prepared')
