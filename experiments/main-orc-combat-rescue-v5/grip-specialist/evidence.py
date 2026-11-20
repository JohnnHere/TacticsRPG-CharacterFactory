from pathlib import Path
from PIL import Image,ImageDraw
import json
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist');C=Path('characters/orc-v1/source/combat-rescue-v5/grip-specialist/F06')
p=json.loads(Path('characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword/clip.json').read_text());frame=p['frames'][6]
tiles=[('CORPO sem arma',frame['layers']['body']['png']),('REJEITADO qa5-repair1',frame['png']),('F06 grip especialista',str(C/'composite-256.png'))]
o=Image.new('RGB',(1152,890),(43,44,49));d=ImageDraw.Draw(o)
for ci,(label,fp)in enumerate(tiles):
 im=Image.open(fp).convert('RGBA');bodyView=im.crop((64,64,192,192)).resize((384,384),Image.Resampling.NEAREST);o.paste(bodyView,(ci*384,24),bodyView);d.text((ci*384+5,5),label,fill='white')
 crop=im.crop((139,103,175,131)).resize((360,280),Image.Resampling.NEAREST);o.paste(crop,(ci*384+12,438),crop);d.text((ci*384+5,420),'Palma/cabo/guarda/pomo -10x',fill='white')
 for j,size in enumerate([128,64]):
  native=im.crop((64,64,192,192)).resize((size,size),Image.Resampling.NEAREST);o.paste(native,(ci*384+200+j*110,730),native)
o.save(E/'F06-before-after.png')
# Annotated diagnostic only. Markers never enter any production sprite.
body=Image.open(frame['layers']['body']['png']).convert('RGBA');o=Image.new('RGB',(1100,740),(43,44,49));d=ImageDraw.Draw(o)
im=body.crop((96,86,168,150)).resize((576,512),Image.Resampling.NEAREST);o.paste(im,(24,32),im)
a=json.loads((E/'anatomy.json').read_text());names={'attackingShoulder':'ombro de ataque','attackingElbow':'cotovelo','forearmSteelMidline':'antebraco metalico','distalSteelCuff':'borda da bracadeira','wristTransition':'transicao do pulso','palmGrip':'palma REAL / grip proposto','knuckleOuterEdge':'contorno dos nos','upperThumbRegion':'regiao superior da luva','inactiveHandAtHip':'mao inativa no quadril'}
for j,(key,point)in enumerate(a['observations'].items()):
 x,y=24+(point[0]-96)*8,32+(point[1]-86)*8;col=(255,202,70)if key=='palmGrip'else(80,210,170)
 d.ellipse((x-3,y-3,x+3,y+3),outline=col,width=2);d.text((x+5,y-10),str(j+1),fill=col);d.text((640,50+j*30),f'{j+1}. {names[key]} {point}',fill=col)
bad=a['rejectedPriorPoint']['point'];x,y=24+(bad[0]-96)*8,32+(bad[1]-86)*8;d.line((x-7,y-7,x+7,y+7),fill=(255,90,90),width=3);d.line((x-7,y+7,x+7,y-7),fill=(255,90,90),width=3)
d.text((640,370),'X vermelho: ponto rejeitado (142,115)',fill=(255,90,90));d.text((640,395),'Fica no metal, antes do pulso/palma.',fill='white')
d.text((24,560),'Pontos obtidos pela imagem sem arma. Sem segmentacao esqueletica inferida como fato.',fill='white')
d.text((24,590),'A faixa da luva de ataque e x152..159 / y109..119. A mao no quadril pertence ao outro braco.',fill='white')
o.save(E/'F06-anatomy-annotated.png')
Image.open(C/'composite-256.png').convert('RGBA').crop((137,100,174,130)).resize((740,600),Image.Resampling.NEAREST).save(E/'F06-grip-final-20x.png')
print('Evidence layouts created; no production pixels modified.')
