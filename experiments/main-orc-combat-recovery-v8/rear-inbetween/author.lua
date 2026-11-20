-- Programmatic pixel authorship in Aseprite; no AI, blending or temporal interpolation.
local root=app.fs.currentPath
local E='experiments/main-orc-combat-recovery-v8/rear-inbetween'
local function abs(p)return app.fs.joinPath(root,p)end
local function read(p)local f=assert(io.open(abs(p),'r'));local t=json.decode(f:read('*a'));f:close();return t end
local function blank(w,h)local a=Image(w,h,ColorMode.RGB);a:clear();return a end
local function load(p)return Image{fromFile=abs(p)}end
local function save(a,p)app.fs.makeAllDirectories(app.fs.filePath(abs(p)));a:saveAs(abs(p))end
local pc=app.pixelColor
local function rgb(r,g,b)return pc.rgba(r,g,b,255)end
local ink=rgb(12,15,18)
local function inside(x,y,p)local hit=false;local j=#p;for i=1,#p do local a,b=p[i],p[j];if(a[2]>y)~=(b[2]>y)and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1]then hit=not hit end;j=i end;return hit end
local function poly(im,p,c)for y=0,255 do for x=0,255 do if inside(x+.5,y+.5,p)then im:drawPixel(x,y,c)end end end end
-- Explicit shoulder/elbow/palm plans; the torso and pauldron are inherited.
local configs={
 {direction='back_r',src='rear-fix/back_r-sword',s={151,107},e={171,117},p={172,105},angle=25,cut={{158,75},{185,75},{185,114},{168,118},{155,109}},donorE={165,105},donorP={160.8863,89.1087}},
 {direction='back_l',src='rear/back_l-sword',s={151,103},e={173,111},p={170,103},angle=22,cut={{154,70},{183,70},{183,113},{157,113},{151,104}},donorE={175,101},donorP={164,83}}
}
local names={'weaponBack','body','weaponFront','handFront'}
local durations={30,65,35,50,45,35,30,35,35,100,55,80,45,90}
local def=read('characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/weapon.json')
local ws=app.open(abs(def.master));local item=blank(96,96);item:drawSprite(ws,1);ws:close()
for _,q in ipairs(configs)do
 local src='characters/orc-v1/source/combat-recovery-v8/'..q.src
 local dst='characters/orc-v1/source/combat-recovery-v8/rear-inbetween/'..q.direction..'-sword'
 local c=read(src..'/clip.json');local donor=load(c.frames[6].layers.body.png);local body=Image(donor);local arm=blank(256,256)
 for y=0,255 do for x=0,255 do if inside(x+.5,y+.5,q.cut)then arm:drawPixel(x,y,donor:getPixel(x,y));body:drawPixel(x,y,0)end end end
 -- Draw a closed sleeve with a direction-specific elbow and chainmail clusters.
 local s,e=q.s,q.e;local dx,dy=e[1]-s[1],e[2]-s[2];local len=math.sqrt(dx*dx+dy*dy);local ux,uy=dx/len,dy/len;local nx,ny=-uy,ux
 local function pt(t,n)return {s[1]+t*ux+n*nx,s[2]+t*uy+n*ny}end
 poly(body,{pt(-2,-5),pt(len,-5),pt(len+4,-2),pt(len+4,3),pt(len,6),pt(0,6)},ink)
 local mesh={pt(1,-3),pt(len,-3),pt(len+2,0),pt(len,4),pt(1,4)}
 poly(body,mesh,rgb(35,37,41))
 for y=0,255 do for x=0,255 do if inside(x+.5,y+.5,mesh)then local t=math.floor((x-s[1])*ux+(y-s[2])*uy);local n=math.floor((x-s[1])*nx+(y-s[2])*ny);if t%3==0 and n%3==0 then body:drawPixel(x,y,rgb(79,85,89))elseif t%3==1 and n%3==1 then body:drawPixel(x,y,rgb(54,60,64))end end end end
 -- Re-articulate the same-view gauntlet donor along the authored forearm axis.
 local a,b=q.donorE,q.donorP;local ax,ay=b[1]-a[1],b[2]-a[2];local al=math.sqrt(ax*ax+ay*ay);ax,ay=ax/al,ay/al
 local tx,ty=q.p[1]-e[1],q.p[2]-e[2];local tl=math.sqrt(tx*tx+ty*ty);tx,ty=tx/tl,ty/tl
 local hf=blank(256,256);local hand=load(c.frames[6].layers.handFront.png)
 for y=0,255 do for x=0,255 do local vx,vy=x-e[1],y-e[2];local along=(vx*tx+vy*ty)*al/tl;local cross=-vx*ty+vy*tx;local xx=math.floor(a[1]+along*ax-cross*ay+.5);local yy=math.floor(a[2]+along*ay+cross*ax+.5)
 if xx>=0 and xx<256 and yy>=0 and yy<256 then local col=arm:getPixel(xx,yy);if pc.rgbaA(col)>0 then body:drawPixel(x,y,col)end;hf:drawPixel(x,y,hand:getPixel(xx,yy))end end end
 -- Preserve the actual pauldron at the proximal overlap, without the old distal arm.
 for y=s[2]-13,s[2]+2 do for x=s[1]-13,s[1]+2 do local col=donor:getPixel(x,y);if pc.rgbaA(col)>0 then body:drawPixel(x,y,col)end end end
 local wb,wf=blank(256,256),blank(256,256);local rad=q.angle*math.pi/180;local ca,sa=math.cos(rad),math.sin(rad)
 for y=0,255 do for x=0,255 do local dx,dy=x-q.p[1],y-q.p[2];local u=math.floor(ca*dx+sa*dy+def.grip[1]+.5);local v=math.floor(-sa*dx+ca*dy+def.grip[2]+.5);if u>=0 and u<96 and v>=0 and v<96 then local col=item:getPixel(u,v);if pc.rgbaA(col)>0 then (v>=60 and v<=70 and wb or wf):drawPixel(x,y,col)end end end end
 local new={wb,body,wf,hf};local sp=Sprite(256,256,ColorMode.RGB);local ns=Sprite(128,128,ColorMode.RGB);ns.layers[1].name='body';local ls={}
 for j,n in ipairs(names)do local l=j==1 and sp.layers[1]or sp:newLayer();l.name=n;ls[j]=l end
 for i=1,14 do if i>1 then sp:newEmptyFrame();ns:newEmptyFrame()end;sp.frames[i].duration=durations[i]/1000;ns.frames[i].duration=durations[i]/1000
 local ims={};if i==7 then ims=new else local old=c.frames[i<7 and i or i-1];for j,n in ipairs(names)do ims[j]=load(old.layers[n].png)end end
 for j=1,4 do sp:newCel(ls[j],i,ims[j],Point(0,0))end;local n=blank(128,128);n:drawImage(ims[2],Point(-64,-64));ns:newCel(ns.layers[1],i,n,Point(0,0))end
 app.fs.makeAllDirectories(abs(dst..'/source'));sp:newTag(1,14).name='Attack';ns:newTag(1,14).name='Attack';sp:saveAs(abs(dst..'/source/composite.aseprite'));ns:saveAs(abs(dst..'/source/native.aseprite'));sp:close();ns:close()
 sp=app.open(abs(dst..'/source/composite.aseprite'));ns=app.open(abs(dst..'/source/native.aseprite'));local strip=blank(3584,256);local nstrip=blank(1792,128);local trio=blank(768,256)
 for i=1,14 do assert(math.abs(sp.frames[i].duration*1000-durations[i])<.1);local id=string.format('%02d',i-1);local a=blank(256,256);a:drawSprite(sp,i);save(a,dst..'/frames/'..id..'.png');strip:drawImage(a,Point((i-1)*256,0));if i>=6 and i<=8 then trio:drawImage(a,Point((i-6)*256,0))end
 for _,l in ipairs(sp.layers)do local b=blank(256,256);local cel=l:cel(i);if cel then b:drawImage(cel.image,cel.position)end;save(b,dst..'/layers/'..l.name..'/'..id..'.png')end
 local n=blank(128,128);n:drawSprite(ns,i);save(n,dst..'/native/'..id..'.png');nstrip:drawImage(n,Point((i-1)*128,0))end
 save(strip,dst..'/composite-strip.png');save(nstrip,dst..'/native-strip.png');trio:resize(2304,768);save(trio,E..'/'..q.direction..'-trio.png');sp:close();ns:close()
 local f=assert(io.open(abs(dst..'/source/authorship.json'),'w'));f:write(json.encode({method='Aseprite Lua explicit joint plan, sleeve clusters and same-view gauntlet articulation; no temporal pixel interpolation',plan=q,generationCalls=0,mastersSavedReopened=true}));f:close()
end
