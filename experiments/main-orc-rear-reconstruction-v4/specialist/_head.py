from PIL import Image
import numpy as np
D='experiments/main-orc-rear-reconstruction-v4/specialist/donors/'
def head(p):
    a=np.array(Image.open(p).convert('RGBA')).astype(int)
    m=(a[:,:,3]>0)&(a[:,:,1]>a[:,:,0]+25)&(a[:,:,1]>a[:,:,2]+25)
    ys,xs=np.where(m);return (xs.min(),ys.min(),xs.max(),ys.max(),round(xs.mean(),1),round(ys.mean(),1))
def feet(p):
    a=np.array(Image.open(p).convert('RGBA')).astype(int)[:,:,3]>0
    ys,xs=np.where(a);return (ys.max(), xs[ys==ys.max()].min(),xs[ys==ys.max()].max())
for p in ['characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/native/%02d.png'%i for i in range(8)]+[D+'sword-body-representative-v3-back_r-%d.png'%i for i in (0,5,6)]:
    print(p[-40:],head(p),feet(p))
