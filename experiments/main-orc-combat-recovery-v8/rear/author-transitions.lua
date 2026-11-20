-- V7 full back_l cycles: manual pose plans, same-view joint-measured donors.
-- All raster authorship/rotation/export executes inside Aseprite. No generation.
local root=app.fs.currentPath;local E='experiments/main-orc-combat-recovery-v8/rear'
local function abs(p)return app.fs.joinPath(root,p)end
local function read(p)local f=assert(io.open(abs(p),'r'));local a=json.decode(f:read('*a'));f:close();return a end
local function blank(w,h)local a=Image(w,h,ColorMode.RGB);a:clear();return a end
local function load(p)return Image{fromFile=abs(p)}end
local function save(a,p)app.fs.makeAllDirectories(app.fs.filePath(abs(p)));a:saveAs(abs(p))end
local function crop(a)local b=blank(128,128);b:drawImage(a,Point(-64,-64));return b end
local pc=app.pixelColor;local function rgb(r,g,b)return pc.rgba(r,g,b,255)end
local ink=rgb(12,15,18);local dark=rgb(25,27,31);local steel=rgb(54,60,64);local light=rgb(79,85,89);local burgundy=rgb(57,28,33);local redlight=rgb(78,38,42)
local plan=read(E..'/transition-plan.json');local kind=app.params.kind or 'Sword';assert(kind=='Sword' or kind=='Axe');local cfg=plan.clips[kind]
local function inside(x,y,poly)local hit=false;local j=#poly;for i=1,#poly do local a,b=poly[i],poly[j];if (a[2]>y)~=(b[2]>y)and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1]then hit=not hit end;j=i end;return hit end
local function polygon(im,poly,col)for y=0,127 do for x=0,127 do if inside(x+.5,y+.5,poly)then im:drawPixel(x,y,col)end end end end
local function line(im,x0,y0,x1,y1,c)
 x0,y0,x1,y1=math.floor(x0+.5),math.floor(y0+.5),math.floor(x1+.5),math.floor(y1+.5)
 local dx,dy=math.abs(x1-x0),-math.abs(y1-y0);local sx,sy=x0<x1 and 1 or -1,y0<y1 and 1 or -1;local er=dx+dy
 while true do if x0>=0 and x0<im.width and y0>=0 and y0<im.height then im:drawPixel(x0,y0,c)end;if x0==x1 and y0==y1 then break end;local e2=2*er;if e2>=dy then er=er+dy;x0=x0+sx end;if e2<=dx then er=er+dx;y0=y0+sy end end
end
local donors={}
for name,d in pairs(plan.donors)do local source=crop(load(d.source));local arm=blank(128,128);local hand=blank(128,128)
 for _,r in ipairs(d.rows)do for x=r[2],r[3]do local c=source:getPixel(x,r[1]);arm:drawPixel(x,r[1],c);if(d.handRowsMax and r[1]<=d.handRowsMax)or(d.handRowsMin and r[1]>=d.handRowsMin)then hand:drawPixel(x,r[1],c)end end end
 donors[name]={arm=arm,hand=hand,meta=d}
end
local def=read('characters/orc-v1/source/combat-rescue-v5/combat/weapons/'..kind..'/weapon.json');local ws=app.open(abs(def.master));local item=blank(96,96);item:drawSprite(ws,1);ws:close()
local function clearOldArm(body,f)
 local src=f.sourceFrame
 if kind=='Axe'and src==8 then for y=88,94 do for x=82,86 do body:drawPixel(x,y,0)end end end
 -- Axe hoist sources have their old glove LEFT of the Sword cutoff. Remove
 -- the whole old hand, not only the rightmost half of the generated member.
 if kind=='Axe'and(src==3 or src==4)then
  for y=10,25 do for x=(src==3 and 82 or 79),127 do body:drawPixel(x,y,0)end end
  for y=26,31 do for x=(src==3 and 91 or 87),127 do body:drawPixel(x,y,0)end end
 end
 for y=10,94 do for x=80,127 do
  local cutoff=999
  if src==1 then if y>=43 then cutoff=87 end
  elseif src<=4 then if y<=42 then cutoff=92 elseif y<=56 then cutoff=86 elseif y<=64 then cutoff=92 end
  elseif src==5 then if y<=44 then cutoff=92 elseif y<=66 then cutoff=85 end
  else if y<=48 then cutoff=94 elseif y<=77 then cutoff=80 else cutoff=85 end end
  if x>=cutoff then body:drawPixel(x,y,0)end
 end end
end
local function authorArm(body,f)
 clearOldArm(body,f);local clean=Image(body);local s,e,p=f.shoulder,f.elbow,f.palm
 local dx,dy=e[1]-s[1],e[2]-s[2];local len=math.sqrt(dx*dx+dy*dy);local ux,uy=dx/len,dy/len;local nx,ny=-uy,ux
 local function point(t,n)return {s[1]+t*ux+n*nx,s[2]+t*uy+n*ny}end
 local upper={point(-3,-5),point(len-2,-5),point(len+4,-2),point(len+4,3),point(len-1,6),point(1,6),point(-4,2)}
 polygon(body,upper,ink);local sleeve={point(-1,-3),point(len-2,-3),point(len+2,-1),point(len+2,2),point(len-1,4),point(2,4),point(-2,1)};polygon(body,sleeve,burgundy)
 local mesh={point(7,-3),point(len-2,-3),point(len+1,0),point(len-2,4),point(7,3)};polygon(body,mesh,dark)
 for y=0,127 do for x=0,127 do if inside(x+.5,y+.5,mesh)then
  local along=(x-s[1])*ux+(y-s[2])*uy;local side=(x-s[1])*nx+(y-s[2])*ny;local a,b=math.floor(along)%3,math.floor(side)%3;local c=dark
  if(a==0 and b==0)or(a==1 and b==1)then c=steel elseif a==1 and b==0 then c=light end;body:drawPixel(x,y,c)
 end end end
 local a,b=point(5,-3),point(5,4);line(body,a[1],a[2],b[1],b[2],redlight)
 -- Retain the real pauldron where it overlaps the new proximal arm.
 for y=math.max(0,s[2]-15),math.min(127,s[2]+3)do for x=math.max(0,s[1]-12),math.min(127,s[1]+3)do local c=clean:getPixel(x,y);if pc.rgbaA(c)>0 then body:drawPixel(x,y,c)end end end
 -- A local nearest-neighbour articulation of the measured donor. Only axial
 -- projection changes; transverse thickness stays native. No blending/crossfade.
 local d=donors[f.donor];local a,b=d.meta.elbow,d.meta.palm;local ddx,ddy=b[1]-a[1],b[2]-a[2];local sl=math.sqrt(ddx*ddx+ddy*ddy);local sux,suy=ddx/sl,ddy/sl;local snx,sny=-suy,sux
 local tx,ty=p[1]-e[1],p[2]-e[2];local tl=math.sqrt(tx*tx+ty*ty);local tux,tuy=tx/tl,ty/tl;local tnx,tny=-tuy,tux;local hf=blank(128,128)
 for y=0,127 do for x=0,127 do
  local vx,vy=x-e[1],y-e[2];local along=(vx*tux+vy*tuy)*sl/tl;local across=vx*tnx+vy*tny
  local xx=math.floor(a[1]+along*sux+across*snx+.5);local yy=math.floor(a[2]+along*suy+across*sny+.5)
  if xx>=0 and xx<128 and yy>=0 and yy<128 then local c=d.arm:getPixel(xx,yy);if pc.rgbaA(c)>0 then body:drawPixel(x,y,c)end;local h=d.hand:getPixel(xx,yy);if pc.rgbaA(h)>0 then hf:drawPixel(x,y,h)end end
 end end
 return hf,tl/sl
end
local function debris(im)
 local seen={};local removed={}
 for y=0,127 do for x=0,127 do local key=y*128+x;if not seen[key]and pc.rgbaA(im:getPixel(x,y))>0 then
  local q={{x,y}};seen[key]=true;local head=1
  while head<=#q do local a=q[head];head=head+1;for dy=-1,1 do for dx=-1,1 do local xx,yy=a[1]+dx,a[2]+dy;if xx>=0 and xx<128 and yy>=0 and yy<128 then local k=yy*128+xx;if not seen[k]and pc.rgbaA(im:getPixel(xx,yy))>0 then seen[k]=true;q[#q+1]={xx,yy}end end end end end
  if #q<=8 then for _,a in ipairs(q)do removed[#removed+1]={a[1],a[2],im:getPixel(a[1],a[2])};im:drawPixel(a[1],a[2],0)end end
 end end end
 return removed
end

local f=cfg.frames[1];local body=crop(load(f.base));local hfNative,scale=authorArm(body,f);local removed=debris(body)
local wb,wf,hf,b256=blank(256,256),blank(256,256),blank(256,256),blank(256,256);b256:drawImage(body,Point(64,64));hf:drawImage(hfNative,Point(64,64))
local gx,gy=f.palm[1]+64,f.palm[2]+64;local rad=f.weaponAngleDeg*math.pi/180;local ca,sa=math.cos(rad),math.sin(rad)
for y=0,255 do for x=0,255 do local dx,dy=x-gx,y-gy;local u=math.floor(ca*dx+sa*dy+def.grip[1]+.5);local v=math.floor(-sa*dx+ca*dy+def.grip[2]+.5)
if u>=0 and u<96 and v>=0 and v<96 then local c=item:getPixel(u,v);if pc.rgbaA(c)>0 then local back=kind=='Sword'and(v>=60 and v<=70)or(kind=='Axe'and v>=48);local target=back and wb or wf;target:drawPixel(x,y,c)end end end end
local names={'weaponBack','body','weaponFront','handFront'};local ims={wb,b256,wf,hf};local dst=cfg.dest
for j,n in ipairs(names)do save(ims[j],dst..'/layers/'..n..'.png')end
save(body,dst..'/native.png');local sp=Sprite(256,256,ColorMode.RGB)
for j,n in ipairs(names)do local l=j==1 and sp.layers[1]or sp:newLayer();l.name=n;sp:newCel(l,1,ims[j],Point(0,0))end
sp.frames[1].duration=.035;sp:saveAs(abs(dst..'/transition.aseprite'));local comp=blank(256,256);comp:drawSprite(sp,1);save(comp,dst..'/composite.png');sp:close()
local large=Image(comp);large:resize(768,768);save(large,dst..'/composite-large.png');local n=Image(body);n:resize(768,768);save(n,dst..'/body-large.png')
-- Pre-propagation key trio: selected apex, new descent, selected contact.
local clip=read('characters/orc-v1/source/combat-recovery-v7/rear-alt/back_l-'..kind:lower()..'/clip.json');local ids=kind=='Sword'and{7,10}or{7,10}
local tri=blank(256*3,256);tri:drawImage(load(clip.frames[ids[1]].png),Point(0,0));tri:drawImage(comp,Point(256,0));tri:drawImage(load(clip.frames[ids[2]].png),Point(512,0));tri:resize(1536,512);save(tri,dst..'/apex-descent-impact.png')
local out=assert(io.open(abs(dst..'/author-result.json'),'w'));out:write(json.encode({kind=kind,manualJoints=f,projectionScale=scale,detachedPixelsRemoved=removed,generationCalls=0}));out:close()
