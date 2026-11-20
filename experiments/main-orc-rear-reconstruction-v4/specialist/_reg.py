from PIL import Image
import numpy as np
D='experiments/main-orc-rear-reconstruction-v4/specialist/donors/'
b=np.array(Image.open('characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/native/05.png').convert('RGBA')).astype(int)
d=np.array(Image.open(D+'sword-body-representative-v3-back_r-6.png').convert('RGBA')).astype(int)
def score(dx,dy,reg):
    x0,y0,x1,y1=reg
    B=b[y0:y1,x0:x1]
    Dd=d[y0-dy:y1-dy,x0-dx:x1-dx]
    return (np.abs(B-Dd).sum(2)>0).mean()
for reg in [(66,22,93,42),(40,30,80,60),(40,60,80,90)]:
    best=sorted(((score(dx,dy,reg),dx,dy) for dx in range(-1,6) for dy in range(-4,4)))[:3]
    print(reg,best)
