from PIL import Image
import numpy as np
D='experiments/main-orc-rear-reconstruction-v4/specialist/donors/'
b=np.array(Image.open('characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/native/05.png').convert('RGBA')).astype(int)
for n in ('sword-body-representative-v3-back_r-5','sword-body-representative-v3-back_r-6','axe-body-representative-v2-back_r-5','axe-body-representative-v2-back_r-4'):
    d=np.array(Image.open(D+n+'.png').convert('RGBA')).astype(int)
    diff=(np.abs(b-d).sum(2)>0)
    ys,xs=np.where(diff)
    print(n,diff.sum(),(xs.min(),ys.min(),xs.max(),ys.max()) if diff.sum() else None)
    # diff outside arm region
    m=diff.copy(); m[:, 81:]=False
    ys,xs=np.where(m); print('  left of x81:',m.sum(),(xs.min(),ys.min(),xs.max(),ys.max()) if m.sum() else None)
