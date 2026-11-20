from pathlib import Path
from PIL import Image,ImageDraw
E=Path('experiments/main-orc-rear-recovery-v2')
O=E/'qa-revision-1-repair';O.mkdir(exist_ok=True)
P=Path('characters/orc-v1/source/rear-recovery-v2')
specs={'SwordL':P/'back_l/Sword/Attack-representative-v1','AxeR':P/'back_r/Axe/Attack-representative-v1','AxeL':P/'back_l/Axe/Attack-representative-v1','SwordR':P/'back_r/Sword/Attack-representative-v2'}
def qa(im,scale=4):
    bg=Image.new('RGBA',im.size,(43,50,56,255));bg.alpha_composite(im);return bg.convert('RGB').resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
for key,p in specs.items():
    sheet=Image.new('RGB',(4*512,2*550),(24,29,33));d=ImageDraw.Draw(sheet)
    for i in range(8):
        im=Image.open(p/'layers/body'/f'{i:02}.png').convert('RGBA').crop((64,64,192,192))
        x=i%4*512;y=i//4*550;sheet.paste(qa(im),(x,y+24));d.text((x+6,y+6),f'{key} F{i:02} native128',(245,240,220))
    sheet.save(O/f'{key}-before.png')
for key,i,box in [('SwordL',5,(15,0,100,60)),('SwordL',4,(20,0,110,60)),('AxeR',1,(70,5,125,65)),('AxeR',2,(70,0,125,50)),('AxeR',4,(65,28,128,85)),('AxeR',5,(65,28,128,85)),('AxeL',2,(75,0,120,35))]:
    im=Image.open(specs[key]/'layers/body'/f'{i:02}.png').convert('RGBA').crop((64,64,192,192))
    out=qa(im.crop(box),10);d=ImageDraw.Draw(out)
    for x in range(box[0],box[2]):
        if x%5==0:d.text(((x-box[0])*10,0),str(x),fill=(255,130,70))
    for y in range(box[1],box[3]):
        if y%5==0:d.text((0,(y-box[1])*10),str(y),fill=(255,130,70))
    out.save(O/f'{key}-F{i:02}-grid.png')
