-- Repair only weaponBack/weaponFront F07..F09. Body and glove are untouched.
local E='experiments/main-orc-artistic-reconstruction-v6/rear/back-l-sword-groundfix'
local C='characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword'
local function abs(p) return app.fs.joinPath(app.fs.currentPath,p) end
local function read(p) local f=assert(io.open(abs(p),'r'));local s=f:read('*a');f:close();return json.decode(s) end
local function blank(w,h) local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function equal(a,b,msg)
 assert(a.width==b.width and a.height==b.height,msg..' dimensions')
 for y=0,a.height-1 do for x=0,a.width-1 do assert(a:getPixel(x,y)==b:getPixel(x,y),msg..' pixel '..x..','..y) end end
end
local clip=read(C..'/clip.json');local plan=read(E..'/binding-plan.json')
local def=read(clip.weaponDefinition);local wsp=app.open(abs(def.master));local weapon=blank(96,96);weapon:drawSprite(wsp,1);wsp:close()
local spr=app.open(abs(clip.master));assert(#spr.layers==4 and #spr.frames==12)
local layers={};local positions={}
for _,l in ipairs(spr.layers) do layers[l.name]=l end
for i=1,12 do
 assert(math.abs(spr.frames[i].duration*1000-clip.durationsMs[i])<.1)
 positions[i]={}
 for _,name in ipairs(clip.layerOrder) do
  local cel=layers[name]:cel(i);positions[i][name]=cel and {cel.position.x,cel.position.y} or false
  local im=blank(256,256);if cel then im:drawImage(cel.image,cel.position) end
  equal(im,Image{fromFile=abs(clip.frames[i].layers[name].png)},'before '..name..' '..i)
 end
end
for _,index in ipairs({7,8,9}) do
 local f=plan.frames[index+1];local wb,wf=blank(256,256),blank(256,256)
 local rad=f.angleAfter*math.pi/180;local ca,sa=math.cos(rad),math.sin(rad)
 local gx,gy=f.grip[1],f.grip[2]
 for y=0,255 do for x=0,255 do
  local dx,dy=x-gx,y-gy
  local u=math.floor(ca*dx+sa*dy+def.grip[1]+.5);local v=math.floor(-sa*dx+ca*dy+def.grip[2]+.5)
  if u>=0 and u<96 and v>=0 and v<96 then local col=weapon:getPixel(u,v)
   if app.pixelColor.rgbaA(col)>0 then
    assert(y<190,'Weapon must remain ABOVE groundY190')
    local dst=v>=def.grip[2]-7 and wb or wf;dst:drawPixel(x,y,col)
   end
  end
 end end
 spr:newCel(layers.weaponBack,index+1,wb,Point(0,0));spr:newCel(layers.weaponFront,index+1,wf,Point(0,0))
end
-- Save the existing four-layer composite master; never save the native body.
spr:saveAs(abs(clip.master));spr:close()
local reopened=app.open(abs(clip.master));local strip=blank(256*12,256)
local weaponOnly=Sprite(256,256,ColorMode.RGB);weaponOnly.layers[1].name='weaponBack';local front=weaponOnly:newLayer();front.name='weaponFront'
for i=1,12 do
 assert(math.abs(reopened.frames[i].duration*1000-clip.durationsMs[i])<.1)
 if i>1 then weaponOnly:newEmptyFrame() end;weaponOnly.frames[i].duration=clip.durationsMs[i]/1000
 for _,l in ipairs(reopened.layers) do
  local cel=l:cel(i);local im=blank(256,256);if cel then im:drawImage(cel.image,cel.position) end
  local changed=(i>=8 and i<=10) and (l.name=='weaponBack' or l.name=='weaponFront')
  if not changed then equal(im,Image{fromFile=abs(clip.frames[i].layers[l.name].png)},'unchanged '..l.name..' '..i) end
  if l.name=='body' or l.name=='handFront' then
   local pos=positions[i][l.name];assert((not pos and not cel) or (cel and cel.position.x==pos[1] and cel.position.y==pos[2]),'Body/glove cel position changed')
  end
  if changed then im:saveAs(abs(clip.frames[i].layers[l.name].png)) end
  if l.name=='weaponBack' or l.name=='weaponFront' then weaponOnly:newCel(l.name=='weaponBack' and weaponOnly.layers[1] or front,i,im,Point(0,0)) end
 end
 local comp=blank(256,256);comp:drawSprite(reopened,i);strip:drawImage(comp,Point((i-1)*256,0))
 if i>=8 and i<=10 then comp:saveAs(abs(clip.frames[i].png)) else equal(comp,Image{fromFile=abs(clip.frames[i].png)},'unchanged composite '..i) end
end
strip:saveAs(abs(clip.compositeStrip));weaponOnly:saveAs(abs(C..'/source/weapon-binding.aseprite'));weaponOnly:close();reopened:close()
-- Second reopening verifies saved masters and horizontal strip against exports.
local saved=app.open(abs(clip.master));local wm=app.open(abs(C..'/source/weapon-binding.aseprite'));local savedStrip=Image{fromFile=abs(clip.compositeStrip)}
for i=1,12 do
 local frame=blank(256,256);frame:drawSprite(saved,i);equal(frame,Image{fromFile=abs(clip.frames[i].png)},'reopened composite '..i)
 local tile=blank(256,256);tile:drawImage(savedStrip,Point(-(i-1)*256,0));equal(frame,tile,'reopened strip '..i)
 assert(math.abs(wm.frames[i].duration*1000-clip.durationsMs[i])<.1)
 for _,l in ipairs(wm.layers) do local im=blank(256,256);local cel=l:cel(i);if cel then im:drawImage(cel.image,cel.position) end;equal(im,Image{fromFile=abs(clip.frames[i].layers[l.name].png)},'reopened weapon master '..i) end
end
saved:close();wm:close()
local f=assert(io.open(abs(E..'/roundtrip.json'),'w'));f:write(json.encode({savedCompositeReopened=true,savedWeaponMasterReopened=true,frames=12,weaponFramesChanged={7,8,9},bodyAndGlovePixelsAndPositionsPreserved=true,timingPreserved=true,stripTilesVerified=12,weaponAboveGroundAsserted=true}));f:close()
