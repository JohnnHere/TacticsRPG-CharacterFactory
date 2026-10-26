-- Component-level weapon retouch and reference composition, entirely inside Aseprite.
local root=assert(app.params.root);local function file(p)return app.fs.joinPath(root,p)end
local pc=app.pixelColor;local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function native(p)local s=app.open(file(p));local im=blank(s.width,s.height);im:drawSprite(s,1);s:close();return im end
local function inside(x,y,pts)local c=false;local j=#pts;for i=1,#pts do local a,b=pts[i],pts[j];if(a[2]>y)~=(b[2]>y)and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1]then c=not c end;j=i end;return c end
local function save(im,p)app.fs.makeAllDirectories(app.fs.filePath(file(p)));im:saveAs(file(p))end
local function master(id,images,names)
 local s=Sprite(96,96,ColorMode.RGB)
 for i,im in ipairs(images)do local l=i==1 and s.layers[1]or s:newLayer();l.name=names[i];s:newCel(l,1,im,Point(0,0))end
 local out='assets/weapons/'..id;app.fs.makeAllDirectories(file(out..'/source/rescue-v3'));s:saveAs(file(out..'/source/rescue-v3/'..id..'.aseprite'));local flat=blank(96,96);flat:drawSprite(s,1);save(flat,out..'/sprites/rescue-v3/'..id..'.png');s:close();return flat
end
local sword=native('assets/weapons/recruit-sword/source/v2/recruit-sword.aseprite');local blade=blank(96,96);local hilt=blank(96,96);local guard=blank(96,96)
-- Preserve metal texture and native width; remove six central blade rows and four lower leather rows.
for y=0,95 do if not(y>=35 and y<=40)and not(y>=77 and y<=80)then
 local yy=y-(y>40 and 6 or 0)-(y>80 and 4 or 0)
 for x=0,95 do local q=sword:getPixel(x,y);if y<62 then blade:drawPixel(x,yy,q)elseif y>65 then hilt:drawPixel(x,yy,q)end end
end end
-- Narrow only the guard (26 -> 20 px), preserving a full-size one-hand handle.
for y=62,65 do for x=38,57 do local u=35+math.floor((x-38)*26/20);guard:drawPixel(x,y-6,sword:getPixel(u,y))end end
sword=master('recruit-sword',{blade,guard,hilt},{'Preserved fuller blade, six rows shorter','One-hand guard','Eleven-pixel leather grip and disk pommel'})
local axe=native('assets/weapons/militia-axe/source/v2/militia-axe.aseprite');local head=blank(96,96);local haft=blank(96,96)
local headOutline={{37,10},{49,10},{50,14},{69,14},{73,9},{76,21},{73,36},{65,49},{55,56},{53,44},{49,33},{38,29}}
-- Shaft width and original curved wood/leather texture retained; shorten its length independently.
for y=24,61 do local v=27+math.floor((y-24)*58/38)
 for x=30,51 do if not inside(x,v,headOutline)then haft:drawPixel(x,y,axe:getPixel(x,math.min(84,v)))end end
end
-- Head alone: compact socket, shorter beard, reduced width; not a global resized axe.
for y=13,37 do for x=39,65 do
 local u=37+math.floor((x-39)*39/27);local v=9+math.floor((y-13)*48/25)
 if inside(u,v,headOutline)then head:drawPixel(x,y,axe:getPixel(math.min(95,u),math.min(95,v)))end
end end
-- Join socket and haft using the same material colors; keep rivet/edge clusters legible.
local iron=pc.rgba(58,60,64,255);local light=pc.rgba(134,134,135,255);local dark=pc.rgba(20,20,26,255)
for y=22,26 do for x=42,46 do if pc.rgbaA(haft:getPixel(x,y))==0 then haft:drawPixel(x,y,dark)end end end
head:drawPixel(43,20,light);head:drawPixel(44,21,iron);head:drawPixel(44,20,light)
axe=master('militia-axe',{haft,head},{'Shortened curved haft, original width and grain','Compact forged head and shorter beard'})
local body=native('characters/orc-v1/source/aseprite/concept-selected.aseprite')
local function rotate(im,grip,gx,gy,deg)
 local out=blank(256,256);local r=deg*math.pi/180;local c,s=math.cos(r),math.sin(r)
 for y=0,255 do for x=0,255 do local dx,dy=x-gx,y-gy;local u=math.floor(c*dx+s*dy+grip[1]+.5);local v=math.floor(-s*dx+c*dy+grip[2]+.5);if u>=0 and u<96 and v>=0 and v<96 then out:drawPixel(x,y,im:getPixel(u,v))end end end;return out
end
local handOutline={{30,78},{35,76},{40,79},{41,85},{37,88},{32,87},{29,83}}
for _,w in ipairs({{id='sword',im=sword,grip={48,66},angle=320},{id='axe',im=axe,grip={36,55},angle=325}})do
 local s=Sprite(256,256,ColorMode.RGB);s.layers[1].name='Reference body';local b=blank(256,256);b:drawImage(body,Point(64,64));s:newCel(s.layers[1],1,b,Point(0,0));local wl=s:newLayer();wl.name='Independent weapon reference';s:newCel(wl,1,rotate(w.im,w.grip,99,146,w.angle),Point(0,0));local front=blank(256,256)
 for y=75,89 do for x=28,42 do if inside(x,y,handOutline)then local q=body:getPixel(x,y);if pc.rgbaA(q)>0 then front:drawPixel(x+64,y+64,q)end end end end
 local l=s:newLayer();l.name='Own hand reference occlusion';s:newCel(l,1,front,Point(0,0));local e='experiments/main-orc-weapon-rescue-v3/references/'..w.id;app.fs.makeAllDirectories(app.fs.filePath(file(e..'.aseprite')));s:saveAs(file(e..'.aseprite'));local out=blank(256,256);out:drawSprite(s,1);save(out,e..'.png');s:close()
end
local idle=blank(256,256);idle:drawImage(body,Point(64,64));save(idle,'experiments/main-orc-weapon-rescue-v3/references/rest.png')
