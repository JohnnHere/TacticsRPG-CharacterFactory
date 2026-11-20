import sys
from PIL import Image
d='characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/native/'
import os
print(os.listdir(d))
fr=[Image.open(d+f'{i:02d}.png').convert('RGBA') for i in range(8)]
print([f.size for f in fr])
# crop bbox union
import functools
bb=None
for f in fr:
    b=f.getbbox()
    bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
print('union bbox',bb)
S=3
w=bb[2]-bb[0];h=bb[3]-bb[1]
sheet=Image.new('RGBA',(w*S*4+50,h*S*2+30),(70,90,70,255))
for i,f in enumerate(fr):
    c=f.crop(bb).resize((w*S,h*S),Image.NEAREST)
    sheet.alpha_composite(c,(10+(i%4)*(w*S+10),10+(i//4)*(h*S+10)))
sheet.save('experiments/main-orc-rear-reconstruction-v4/specialist/_view-source-body.png')
print(sheet.size)
