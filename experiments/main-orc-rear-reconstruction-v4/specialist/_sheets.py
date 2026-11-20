from PIL import Image, ImageDraw
import glob
D='experiments/main-orc-rear-reconstruction-v4/specialist/donors/'
def sheet(prefix,n,out,S=2,cols=6,box=(20,0,128,128)):
    ims=[]
    for i in range(n):
        im=Image.open(f'{D}{prefix}-{i}.png').convert('RGBA')
        if im.size!=(128,128): print(prefix,im.size)
        ims.append(im.crop(box))
    w,h=ims[0].size
    rows=(n+cols-1)//cols
    sh=Image.new('RGBA',(cols*(w*S+6)+6,rows*(h*S+16)+6),(60,80,60,255))
    dr=ImageDraw.Draw(sh)
    for i,im in enumerate(ims):
        x=6+(i%cols)*(w*S+6);y=6+(i//cols)*(h*S+16)
        sh.alpha_composite(im.resize((w*S,h*S),Image.NEAREST),(x,y+12));dr.text((x,y),f'{prefix} F{i:02d}',fill=(255,255,0,255))
    sh.save(out)
O='experiments/main-orc-rear-reconstruction-v4/specialist/'
sheet('axe-back_r',12,O+'_d-axe-orig.png',cols=6)
sheet('sword-body-representative-v3-back_r',8,O+'_d-sword-v3.png',cols=4)
sheet('axe-body-representative-v2-back_r',8,O+'_d-axe-v2.png',cols=4)
