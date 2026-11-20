from pathlib import Path
from PIL import Image,ImageDraw
import json
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/F02-F08');C=Path('characters/orc-v1/source/combat-rescue-v5/grip-specialist')
parent=json.loads(Path('characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword/clip.json').read_text());anatomy=json.loads((E/'anatomy.json').read_text())
for idx,box in [(2,(89,116,119,142)),(8,(138,130,177,161))]:
 key=f'F{idx:02}';f=parent['frames'][idx]
 out=Image.new('RGB',(1152,890),(43,44,49));d=ImageDraw.Draw(out)
 for ci,(label,fp)in enumerate([('CORPO sem arma',f['layers']['body']['png']),('PASSE rejeitado qa5-repair1',f['png']),('PROPOSTA '+key,str(C/key/'composite-256.png'))]):
  im=Image.open(fp).convert('RGBA');out.paste(im,(ci*384+64,26),im);d.text((ci*384+6,5),label,fill='white')
  detail=im.crop(box).resize(((box[2]-box[0])*8,(box[3]-box[1])*8),Image.Resampling.NEAREST);out.paste(detail,(ci*384+12,330),detail)
  d.text((ci*384+6,305),'Detalhe real 8x - sem interpolacao',fill='white')
  small=im.resize((128,128),Image.Resampling.NEAREST);out.paste(small,(ci*384+12,640),small);d.text((ci*384+6,620),'Canvas128 / corpo64px',fill='white')
 d.text((12,800),'Canvas256 completo no topo. Os recortes de detalhe sao apenas diagnosticos.',fill='white')
 if idx==8:d.text((12,824),'F08: equipamento ultrapassa o canvas corporal128; nao encolher nem cortar a espada.',fill=(230,198,100))
 out.save(E/(key+'-before-after.png'))
 body=Image.open(f['layers']['body']['png']).convert('RGBA');crop=(88,92,173,151)if idx==2 else(102,98,175,160)
 im=body.crop(crop).resize(((crop[2]-crop[0])*7,(crop[3]-crop[1])*7),Image.Resampling.NEAREST)
 o=Image.new('RGB',(1150,650),(43,44,49));o.paste(im,(24,30),im);dd=ImageDraw.Draw(o)
 for n,(label,point)in enumerate(anatomy[key]['landmarks'].items()):
  x,y=24+(point[0]-crop[0])*7,30+(point[1]-crop[1])*7;co=(255,203,80)if label=='palm'else(80,215,170)
  dd.ellipse((x-3,y-3,x+3,y+3),outline=co,width=2);dd.text((x+5,y-8),str(n+1),fill=co);dd.text((660,45+n*28),f'{n+1}. {label}: {point}',fill=co)
 dd.text((24,530),anatomy[key]['observation'][:115],fill='white');dd.text((24,555),anatomy[key]['observation'][115:],fill='white')
 dd.text((24,590),'Landmarks interpretados na arte achatada. Nao sao dados esqueleticos recuperados.',fill='white');o.save(E/(key+'-anatomy-annotated.png'))
print('Two representative comparison/annotation layouts saved. F06 untouched.')
