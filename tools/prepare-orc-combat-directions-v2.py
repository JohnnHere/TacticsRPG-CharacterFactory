import json,hashlib
from pathlib import Path
old=json.loads(Path('characters/orc-combat-directions-batch-v1.json').read_text(encoding='utf-8'));new=[]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for b in old:
 d=b['direction'];facing='LEFT' if d.endswith('_l') else 'RIGHT';rear=d.startswith('back');root=Path(b['folder']);keep_reactions=b['id'] in ['orc-01-squire','orc-01-archer'] and rear
 if keep_reactions:folder=root;name='attack-corrected-v2';states={'Attack':5};kind='FIVE Attack figures in ONE horizontal row, no other rows'
 else:folder=Path(str(root).replace('combat-directions-v1','combat-directions-v2'));name='sheet';states=b['states'];kind='THIRTEEN figures in THREE rows of FIVE equal cells: TOP5 Attack; MIDDLE3 Hit in first3 cells with final2 cells EMPTY; BOTTOM5 Defeat'
 folder.mkdir(parents=True,exist_ok=True)
 camera=f'three-quarter BACK facing SCREEN {facing}, back of head and back garment visible, NO CHEST or front face' if rear else 'three-quarter FRONT facing SCREEN LEFT, face and chest point LEFT in EVERY drawing, never face RIGHT'
 action=b['action']['poses'].replace('screen-right','screen-'+facing.lower()).replace('screen right','screen '+facing.lower())
 extra=''
 if b['id'].endswith('archer'):extra=f'Bow mime: anatomically LEFT hand aims fully SCREEN {facing}; RIGHT hand draws next to the jaw facing {facing}. The RIGHT ELBOW must protrude on viewer '+('RIGHT' if rear else 'LEFT')+' side. Do not swap drawing/aiming arms. Both aiming and drawing wrists can project towards the same screen side, but elbows bind to the correct shoulders.'
 elif b['id'].endswith('squire'):extra='The small iron cap covers the anatomical LEFT shoulder, which MUST NOT drive the strike. Raise and swing the plain russet anatomical RIGHT sleeve. The capped LEFT arm stays low guarding, never raised overhead. Keep the cap attached to the same shoulder.'
 elif b['id'].endswith('acolyte'):extra='Raise the anatomical RIGHT open palm in blessing. Its shoulder projects viewer '+('RIGHT' if rear else 'LEFT')+'. The left hand rests on heart and is mostly hidden from rear.'
 else:extra='The anatomical RIGHT arm starts at the shoulder projecting viewer '+('RIGHT' if rear else 'LEFT')+f' and acts towards SCREEN {facing}; the LEFT hand supports/guards. Keep that same action arm in follow-through, never switch arms.'
 prompt=f'''Create a NEW native-style pixel-art animation SOURCE SHEET of the SAME Orc {b['job']} in reference1. Reference1 alone defines the approved CAMERA, anatomy, outfit, palette and accessories. Draw {kind}. Camera for EVERY pose: {camera}. All attacks aim SCREEN {facing}. Never turn towards the opposite screen side. Do not mirror an image.

Attack5 chronological: {action}
CRITICAL ANATOMY: {extra}

{'' if keep_reactions else 'Reference2 is ONLY the matching-camera neutral grey Hit3/Defeat5 motion guide. MIDDLE HIT3: backward recoil, absorb impact with bent knees, regain ready. BOTTOM DEFEAT5: upright stagger, buckle knees, kneel supported by hand, tip onto side with curled knees, fully collapsed curled on side. Same physical body size as standing while height decreases; never shrink a standing figure. Match the camera of reference1 throughout all rows, including reactions/falling. No frontal chest in rear views. Final curled body fits logical110-pixel width in128 canvas.'}

OUTFIT: {json.loads(Path('characters',b['id'],'character.json').read_text(encoding='utf-8'))['outfit']['description']}
Same mature brutal olive Orc, bald scalp (or approved raised charcoal hood for Rogue), compact robust body, approved face/proportions. EXACT front/rear garment, straps, belt, pouches and asymmetry from reference1. Body and clothes ONLY, empty hands: NO held/carried/sheathed weapons, bow, bowstring, arrow, quiver, staff, shield, dagger, projectile, orb, effect or other object, even for mimed attack.

Full bodies and boots/hands visible, equal physical scale, large transparent margins/gaps; figures do not touch or overlap, no cropped last figure. Crisp chunky square logical pixels, deliberate clusters, 40-48-color own-outfit native style, dark one-pixel outline, upper-left light, no antialiasing or gradients. TRUE TRANSPARENT background, no floor, shadow, haze, grid, text, labels or scene. Exactly {5 if keep_reactions else 13} separate complete figures; {kind}. Camera {d}, all aimed SCREEN {facing}.'''
 prompt_file=folder/(name+'.prompt.md');prompt_file.write_text(prompt+'\n',encoding='utf-8');refs=[{'file':f"characters/{b['id']}/source/directions-v1/{d}/native-4x.png"}]
 if not keep_reactions:refs.append({'file':f'characters/orc-combat-{d}-reaction-guide-v1.png'})
 for ref in refs:ref['sha256']=sha(ref['file'])
 new.append({**b,'folder':folder.as_posix(),'promptFile':prompt_file.as_posix(),'prompt':prompt,'references':refs,'generationName':name,'generationStates':states,'preserveReactionSource':keep_reactions})
Path('characters/orc-combat-directions-batch-v2.json').write_text(json.dumps(new,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print('Prepared21 camera-first sheets:4 Attack-only replacements reuse32 reaction drawings;17 full sheets.')
