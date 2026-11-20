-- Scoped recomposition AFTER Root's accepted body-only checkpoint.
-- Aseprite saves and reopens all masters before writing their derivatives.
local E="experiments/main-orc-rear-recovery-v2"
local O=E.."/qa-revision-1-repair"
local C="characters/orc-v1/source/rear-recovery-v2/"
local M="characters/orc-v1/source/aseprite/rear-recovery-v2/"
local function f(p)return app.fs.joinPath(app.fs.currentPath,p)end
local function blank(w,h)local b=Image(w,h,ColorMode.RGB);b:clear();return b end
local function load(p)return Image{fromFile=f(p)}end
local function alpha(p)return app.pixelColor.rgbaA(p)end
local durations={90,80,90,80,100,80,100,110}
local names={"weaponBack","body","weaponFront","handFront"}
local specs={
 {key="SwordL",dir="back_l",action="Sword",name="sword",grips={{0,0},{92,108},{104,70},{127,72},{93,71},{74,95},{100,118},{0,0}},angles={0,270,350,20,240,215,200,0}},
 {key="AxeR",dir="back_r",action="Axe",name="axe",grips={{0,0},{175,106},{167,73},{167,78},{181,118},{181,122},{156,139},{0,0}},angles={0,315,350,0,70,105,135,0}},
 {key="AxeL",dir="back_l",action="Axe",name="axe",grips={{0,0},{92,108},{104,78},{104,78},{86,118},{96,141},{99,145},{0,0}},angles={0,270,315,350,315,270,235,0}}
}
local function renderAxe(grip,angle)
 local item=load("assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png")
 local out=blank(256,256);local r=angle*math.pi/180;local c,s=math.cos(r),math.sin(r)
 for y=2,253 do for x=2,253 do
  local dx,dy=x-grip[1],y-grip[2]
  local u,v=math.floor(c*dx+s*dy+36.5),math.floor(-s*dx+c*dy+55.5)
  if u>=0 and u<item.width and v>=0 and v<item.height then local p=item:getPixel(u,v);if alpha(p)>=128 then out:drawPixel(x,y,p) end end
 end end;return out
end
local function realFingers(body,oldMask,grip)
 local out=blank(256,256)
 -- Preserve the existing hand silhouette mask only where the repaired BODY
 -- has actual glove pixels. Never carry over old displaced forearm patches.
 for y=grip[2]-5,grip[2]+5 do for x=grip[1]-5,grip[1]+5 do
  if alpha(oldMask:getPixel(x,y))>0 then local p=body:getPixel(x,y);if alpha(p)>0 then out:drawPixel(x,y,p) end end
 end end;return out
end
local function save(path,w,layerNames,frames)
 local s=Sprite(w,w,ColorMode.RGB);local ls={};s.layers[1].name=layerNames[1];ls[1]=s.layers[1]
 for i=2,#layerNames do ls[i]=s:newLayer();ls[i].name=layerNames[i] end
 for i=1,8 do if i>1 then s:newEmptyFrame() end;for j=1,#ls do s:newCel(ls[j],i,frames[i][j],Point(0,0)) end;s.frames[i].duration=durations[i]/1000 end
 s:newTag(1,8).name="Attack";s:saveAs(f(path));s:close()
end
for _,sp in ipairs(specs) do
 local out=C..sp.dir.."/"..sp.action.."/Attack-representative-v1"
 local frames,bodies,natives={},{},{}
 local src=app.open(f(O.."/checkpoint/source/"..sp.key.."-body-256.aseprite"))
 for i=1,8 do
  local n=string.format("%02d.png",i-1);local b=blank(256,256);b:drawSprite(src,i)
  local wb,wf,h=load(out.."/layers/weaponBack/"..n),load(out.."/layers/weaponFront/"..n),load(out.."/layers/handFront/"..n)
  if sp.key=="AxeR" and (i==2 or i==5 or i==6) then
   wb=blank(256,256);wf=renderAxe(sp.grips[i],sp.angles[i]);h=blank(256,256)
   -- Tight actual closed-glove polygon, around its knuckles and thumb only.
   local gx,gy=sp.grips[i][1],sp.grips[i][2]
   for y=gy-3,gy+4 do for x=gx-4,gx+3 do
    if math.abs(x-gx)+math.abs(y-gy)<=6 then local p=b:getPixel(x,y);if alpha(p)>0 then h:drawPixel(x,y,p) end end
   end end
  elseif i>=2 and i<=7 then h=realFingers(b,h,sp.grips[i]) end
  if i==1 or i==8 then wb,wf,h=blank(256,256),blank(256,256),blank(256,256) end
  frames[i]={wb,b,wf,h};bodies[i]={b};local nat=blank(128,128);nat:drawImage(b,Point(-64,-64));natives[i]={nat}
 end;src:close()
 local comp=M.."composite/"..sp.dir.."/"..sp.name.."-attack-representative-v1.aseprite"
 local body=M.."composite/"..sp.dir.."/"..sp.name.."-body-representative-v1.aseprite"
 local native=M.."native/"..sp.name.."-body-representative-v1-"..sp.dir..".aseprite"
 save(comp,256,names,frames);save(body,256,{"body"},bodies);save(native,128,{sp.name.."_body_"..sp.dir},natives)
 -- Actual final exports from reopened saved masters.
 local s=app.open(f(comp));local bs=app.open(f(body));local ns=app.open(f(native))
 app.fs.makeAllDirectories(f(out.."/body-only"))
 local strip=blank(1024,128);local comps=blank(1024,512);local noWeapon=blank(1024,512)
 for i=1,8 do
  local n=string.format("%02d.png",i-1)
  for _,l in ipairs(s.layers)do l.isVisible=true end
  local flat=blank(256,256);flat:drawSprite(s,i);flat:saveAs(f(out.."/"..n));comps:drawImage(flat,Point((i-1)%4*256,math.floor((i-1)/4)*256))
  local b=blank(256,256);b:drawSprite(bs,i);b:saveAs(f(out.."/body-only/"..n));noWeapon:drawImage(b,Point((i-1)%4*256,math.floor((i-1)/4)*256))
  local nat=blank(128,128);nat:drawSprite(ns,i);nat:saveAs(f(out.."/native/"..n));strip:drawImage(nat,Point((i-1)*128,0))
  for _,ln in ipairs(names)do
   for _,l in ipairs(s.layers)do l.isVisible=l.name==ln end
   local im=blank(256,256);im:drawSprite(s,i);im:saveAs(f(out.."/layers/"..ln.."/"..n))
  end
 end
 strip:saveAs(f(out.."/native-strip.png"));strip:saveAs(f(out.."/body-only-strip.png"));comps:saveAs(f(out.."/composite-sheet-qa.png"));noWeapon:saveAs(f(out.."/weapon-layers-off-qa.png"))
 s:close();bs:close();ns:close()
 print("Canonical saved and reopened: "..sp.key.." body/native/composite, four layers; 730 ms")
end
