from PIL import Image, ImageDraw
d='characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/native/'
def grid(i,box,S,out,src=d):
    im=Image.open(src+f'{i:02d}.png').convert('RGBA').crop(box)
    w,h=im.size
    bg=Image.new('RGBA',im.size,(60,80,60,255));bg.alpha_composite(im)
    big=bg.resize((w*S,h*S),Image.NEAREST)
    dr=ImageDraw.Draw(big)
    for x in range(box[0],box[2]):
        if x%10==0:
            dr.line([( (x-box[0])*S,0),((x-box[0])*S,h*S)],fill=(255,255,0,120));dr.text(((x-box[0])*S+2,2),str(x),fill=(255,255,0,255))
    for y in range(box[1],box[3]):
        if y%10==0:
            dr.line([(0,(y-box[1])*S),(w*S,(y-box[1])*S)],fill=(0,255,255,120));dr.text((2,(y-box[1])*S+2),str(y),fill=(0,255,255,255))
    big.save(out)
import sys
for i in (0,3,4,5,6):
    grid(i,(60,20,126,110),8,f'experiments/main-orc-rear-reconstruction-v4/specialist/_z{i}.png')
