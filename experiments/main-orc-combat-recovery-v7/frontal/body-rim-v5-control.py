import json, os
from collections import deque
from PIL import Image
ROOT=os.getcwd()
ORDER=["weaponBack","body","weaponFront","handFront"]
T=145.0
def lum(c): return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def load(p):
    with Image.open(p) as im: return im.convert('RGBA')
def exterior(alpha,w,h):
    bg=[False]*(w*h); q=deque()
    for x in range(w):
        for y in (0,h-1):
            i=y*w+x
            if alpha[i]<128 and not bg[i]: bg[i]=True; q.append(i)
    for y in range(h):
        for x in (0,w-1):
            i=y*w+x
            if alpha[i]<128 and not bg[i]: bg[i]=True; q.append(i)
    while q:
        i=q.popleft(); y,x=divmod(i,w)
        for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=nx<w and 0<=ny<h:
                j=ny*w+nx
                if alpha[j]<128 and not bg[j]: bg[j]=True; q.append(j)
    return bg
srcs={'front_l-Sword-full':('characters/orc-v1/source/combat-rescue-v5/grip-specialist/front_l-Sword-full','characters/orc-v1/source/combat-recovery-v7/frontal/front_l-Sword-full'),
      'front_l-Axe-full':('characters/orc-v1/source/combat-rescue-v5/grip-specialist/front_l-Axe-full','characters/orc-v1/source/combat-recovery-v7/frontal/front_l-Axe-full'),
      'front_r-Axe-full':('characters/orc-v1/source/combat-rescue-v5/grip-specialist/front_r-Axe-full','characters/orc-v1/source/combat-recovery-v7/frontal/front_r-Axe-full'),
      'full-front-r-sword':('characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword','characters/orc-v1/source/combat-recovery-v7/frontal/full-front-r-sword')}
res={}
for clip,(v5,v7) in srcs.items():
    a,b=(os.path.join(ROOT,v5),os.path.join(ROOT,v7))
    n=json.load(open(os.path.join(b,'clip.json'),encoding='utf-8'))['frameCount']
    hits5=[];hits7=[]
    for i in range(n):
        ix='%02d.png'%i
        for tgt,dst in ((a,hits5),(b,hits7)):
            comp=load(os.path.join(tgt,ix)); px=list(comp.getdata()); w,h=comp.size
            alpha=[p[3] for p in px]; ext=exterior(alpha,w,h)
            own=[None]*(w*h)
            for name in ORDER:
                lp=list(load(os.path.join(tgt,'layers',name,ix)).getdata())
                for k in range(w*h):
                    if own[k] is None and lp[k][3]>=128: own[k]=name
            for k in range(w*h):
                if alpha[k]<128 or lum(px[k])<T or own[k]!='body': continue
                x,y=k%w,k//w
                if any(ext[(y+dy)*w+(x+dx)] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=x+dx<w and 0<=y+dy<h):
                    dst.append((i,x,y,tuple(px[k][:3])))
    s5=set(hits5); s7=set(hits7)
    print(clip,'v5=%d v7=%d common=%d onlyV5=%s onlyV7=%s'%(len(hits5),len(hits7),len(s5&s7),sorted(s5-s7),sorted(s7-s5)))
    res[clip]={'v5':len(hits5),'v7':len(hits7),'common':len(s5&s7),'onlyV5':sorted(map(list,s5-s7)),'onlyV7':sorted(map(list,s7-s5))}
json.dump({'threshold':T,'clips':res},open(os.path.join(ROOT,'experiments','main-orc-combat-recovery-v7','frontal','detect','body-rim-v5-control.json'),'w',encoding='utf-8'),indent=2)
