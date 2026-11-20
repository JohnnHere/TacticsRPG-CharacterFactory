from PIL import Image, ImageDraw
O='experiments/main-orc-rear-reconstruction-v4/specialist/'
B='characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/native/'
def grid(path,box,S,out,step=5):
    im=Image.open(path).convert('RGBA').crop(box)
    w,h=im.size
    bg=Image.new('RGBA',im.size,(60,80,60,255));bg.alpha_composite(im)
    big=bg.resize((w*S,h*S),Image.NEAREST);dr=ImageDraw.Draw(big)
    for x in range(box[0],box[2]):
        if x%step==0: dr.line([((x-box[0])*S,0),((x-box[0])*S,h*S)],fill=(255,255,0,90));dr.text(((x-box[0])*S+2,2),str(x),fill=(255,255,0,255))
    for y in range(box[1],box[3]):
        if y%step==0: dr.line([(0,(y-box[1])*S),(w*S,(y-box[1])*S)],fill=(0,255,255,90));dr.text((2,(y-box[1])*S+2),str(y),fill=(0,255,255,255))
    big.save(out)
grid(B+'06.png',(76,38,112,90),16,O+'_f06arm.png')
grid(B+'00.png',(84,52,108,92),16,O+'_f00arm.png')
grid(B+'05.png',(80,34,124,76),16,O+'_f05arm.png')
