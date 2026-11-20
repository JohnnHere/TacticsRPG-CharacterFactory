import json,math
from pathlib import Path
p=Path('experiments/main-orc-combat-recovery-v7/rear-alt/joint-plan.json');a=json.loads(p.read_text())
def measure(s,e,w,p):
 u=math.dist(s,e);f=math.dist(e,w);v=[s[j]-e[j]for j in range(2)];t=[w[j]-e[j]for j in range(2)];ang=math.degrees(math.acos(sum(v[j]*t[j]for j in range(2))/(u*f)))
 return {'shoulder':s,'elbow':e,'wrist':w,'palm':p,'humerusPx':round(u,3),'forearmPx':round(f,3),'elbowInteriorDeg':round(ang,3)}
a['impact']={'base':'characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword/layers/body/07.png','donor':'characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword/layers/body/07.png','sourceJoints':measure([83,48],[89,64],[95,83],[94,89]),'translation':[15,-8],'joints':measure([83,48],[104,56],[110,75],[109,81]),'grip':[109,81],'weaponAngleDeg':115,'durationMs':80}
p.write_text(json.dumps(a,indent=2))
# Reuse verified Aseprite save/reopen/export plumbing, author a different arm.
base=Path('experiments/main-orc-combat-recovery-v7/rear-alt/author-apex.lua').read_text(encoding='utf-8-sig')
base=base.replace('local p=plan.apex','local p=plan.impact')
start=base.index('-- Reconstruct only the arm envelope');end=base.index('local gx,gy=p.grip')
replacement='''-- Clear the entire source arm, retaining torso/waist to its left.
for y=49,77 do for x=80,127 do body:drawPixel(x,y,0)end end
local rows={}
for y=64,66 do rows[#rows+1]={y,84,98}end
rows[#rows+1]={67,83,101}
for y=68,72 do rows[#rows+1]={y,82,101}end
for y=73,78 do rows[#rows+1]={y,84,103}end
for y=79,83 do rows[#rows+1]={y,87,104}end
for y=84,90 do rows[#rows+1]={y,88,104}end
rows[#rows+1]={91,89,102};rows[#rows+1]={92,90,101};rows[#rows+1]={93,92,99};rows[#rows+1]={94,94,97}
for _,r in ipairs(rows)do for x=r[2],r[3]do body:drawPixel(x,r[1],0)end end
local dark=rgb(25,27,31);local steel=rgb(54,60,64);local lit=rgb(79,85,89);local burgundy=rgb(57,28,33)
local outer={{81,47},{87,46},{104,49},{111,54},{112,59},{108,64},{102,65},{91,59},{82,54}}
polygon(body,outer,ink)
polygon(body,{{84,49},{88,48},{103,51},{109,55},{109,59},{105,62},{102,62},{92,57},{84,53}},burgundy)
local mesh={{92,51},{102,51},{109,55},{109,59},{105,62},{101,61},{94,56}}
polygon(body,mesh,dark)
for y=50,63 do for x=91,110 do if inside(x+.5,y+.5,mesh)then
local u,v=x%3,y%3;local c=dark;if(u==0 and v==0)or(u==1 and v==1)then c=steel elseif u==1 and v==0 then c=lit end;body:drawPixel(x,y,c)
end end end
line(body,88,49,91,55,steel)
local donorMask=blank(128,128);local copied=0
for _,r in ipairs(rows)do for x=r[2],r[3]do local c=donor:getPixel(x,r[1]);if pc.rgbaA(c)>0 then local xx,yy=x+15,r[1]-8;body:drawPixel(xx,yy,c);donorMask:drawPixel(xx,yy,c);copied=copied+1 end end end
local hfNative=blank(128,128)
for _,r in ipairs(rows)do if r[1]>=83 then for x=r[2],r[3]do local xx,yy=x+15,r[1]-8;local c=body:getPixel(xx,yy);if pc.rgbaA(c)>0 then hfNative:drawPixel(xx,yy,c)end end end end
'''
base=base[:start]+replacement+base[end:]
base=base.replace("C..'/apex'","C..'/impact'").replace("rear/back_l-sword/frames/03.png","rear/back_l-sword/frames/07.png").replace("E..'/apex-","E..'/impact-")
base=base.replace("local points={{88,39},{111,37},{105,25},{100,19}}","local points={{83,48},{104,56},{110,75},{109,81}}")
base=base.replace("line(annotated,152,103,175,101,rgb(255,190,60));line(annotated,175,101,169,89,rgb(80,210,255))","line(annotated,147,112,168,120,rgb(255,190,60));line(annotated,168,120,174,139,rgb(80,210,255))")
base=base.replace("E..'/author-result.json'","E..'/impact-author-result.json'").replace("pose='apex'","pose='impact'")
Path('experiments/main-orc-combat-recovery-v7/rear-alt/author-impact.lua').write_text(base,encoding='utf-8')
