exec(open('experiments/main-orc-rear-recovery-v2/qa-revision-1-repair/diagnostics.py',encoding='utf8').read().split('for key,p in specs.items():')[0])
import json
grips={'SwordL':[[0,0],[92,108],[104,70],[127,72],[93,71],[74,95],[100,118],[0,0]],'AxeR':[[0,0],[175,106],[167,73],[167,78],[181,118],[181,122],[156,139],[0,0]],'AxeL':[[0,0],[92,108],[104,78],[104,78],[86,118],[96,141],[99,145],[0,0]]}
out=O/'final';out.mkdir(exist_ok=True)
for key in ['SwordL','AxeR','AxeL']:
 p=specs[key];sheet=Image.new('RGB',(4*512,2*538),(24,29,33));d=ImageDraw.Draw(sheet)
 hands=Image.new('RGB',(6*252,2*252),(24,29,33));h=ImageDraw.Draw(hands)
 for i in range(8):
  im=Image.open(p/f'{i:02}.png').convert('RGBA');x=i%4*512;y=i//4*538
  sheet.paste(qa(im,2),(x,y+24));d.text((x+6,y+6),f'{key} F{i:02} FULL 256 composite',(245,240,220))
  if 1<=i<=6:
   gx,gy=grips[key][i];box=(gx-20,gy-20,gx+22,gy+22)
   hands.paste(qa(im.crop(box),6),((i-1)*252,0));b=Image.open(p/'layers/body'/f'{i:02}.png').convert('RGBA');hands.paste(qa(b.crop(box),6),((i-1)*252,252))
   h.text(((i-1)*252+5,3),f'F{i:02} grip ({gx},{gy})',(245,240,220));h.text(((i-1)*252+5,255),'actual empty glove',(245,240,220))
 sheet.save(out/f'{key}-composite-wholebody.png');hands.save(out/f'{key}-grips.png')
print('Final source-derived composite and hand comparison sheets saved.')
