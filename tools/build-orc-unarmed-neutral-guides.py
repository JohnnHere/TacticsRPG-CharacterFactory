"""Layout of actual approved pose silhouettes; guide only, never runtime art."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageFilter
root=Path('.')
for direction in ['front_l','back_r','back_l']:
 sheet=Image.new('RGBA',(128*5,128),(0,0,0,0));sources=[]
 for i in range(5):
  p=root/f'characters/orc-01/sprites/Animations/Attack/attack_{direction}_{i:02d}.png';im=Image.open(p).convert('RGBA');alpha=im.getchannel('A');inner=alpha.filter(ImageFilter.MinFilter(3));pose=Image.new('RGBA',im.size,(42,42,48,0));pose.putalpha(alpha);fill=Image.new('RGBA',im.size,(148,148,156,255));pose.paste(fill,(0,0),inner);sheet.paste(pose,(i*128,0));sources.append({'file':p.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 target=root/f'characters/orc-unarmed-{direction}-neutral-guide-v1.png';sheet.resize((2560,512),Image.Resampling.NEAREST).save(target)
 target.with_suffix('.json').write_text(json.dumps({'source':'Approved actual Warrior five punch frames','operation':'Same registered alpha silhouettes; flat neutral interior and outline; exact nearest4x layout','notRuntimeAsset':True,'direction':direction,'sources':sources},indent=2)+'\n',encoding='utf-8')
