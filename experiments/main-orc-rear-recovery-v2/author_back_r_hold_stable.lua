-- R2 repair: back_r Sword v3 / Axe v2 — stabilize overhead-hold blade angle + strike timing.
-- Bodies are the EXACT frozen v1/v2 clip body layers (pixel-preserved). Only weapon rotation metadata
-- (hold frames normalized to one angle so the blade does not jitter between identical holds) and
-- frame durations change (hold +20ms, strike -20ms so the snap reads as impact speed, not error).
local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local function alpha(p)return app.pixelColor.rgbaA(p)end
local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function saveSprite(path,w,h,names,frames,durations)
 app.fs.makeAllDirectories(app.fs.filePath(f(path)))
 local s=Sprite(w,h,ColorMode.RGB);s.layers[1].name=names[1];local ls={[names[1]]=s.layers[1]}
 for i=2,#names do local l=s:newLayer();l.name=names[i];ls[names[i]]=l end
 for fi=1,#frames do if fi>1 then s:newEmptyFrame() end;for li,n in ipairs(names) do s:newCel(ls[n],fi,frames[fi][li],Point(0,0)) end;s.frames[fi].duration=durations[fi]/1000 end
 s:newTag(1,#frames).name="Attack";s:saveAs(f(path));s:close()
end
local function handFrontFromBody(body256,gx,gy)
 local layer=blank(256,256)
 for y=math.max(0,gy-5),math.min(255,gy+5) do for x=math.max(0,gx-5),math.min(255,gx+5) do local p=body256:getPixel(x,y);if alpha(p)>0 then layer:drawPixel(x,y,p) end end end
 return layer
end
local function author(config)
 local bodies={}
 for i=1,8 do bodies[i]=Image{fromFile=f(config.prev.."/layers/body/"..string.format("%02d.png",i-1))};assert(bodies[i].width==256 and bodies[i].height==256,"missing prev body "..(i-1)) end
 local item=Image{fromFile=f(config.weapon)};local itemGrip=config.itemGrip
 local function render(target,angle,flipX,isBehind)
  local back,front=blank(256,256),blank(256,256);local rad=angle*math.pi/180;local c,s=math.cos(rad),math.sin(rad)
  for y=2,253 do for x=2,253 do local dx,dy=x-target[1],y-target[2];local rx=c*dx+s*dy;local ry=-s*dx+c*dy;if flipX then rx=-rx end;local u=math.floor(rx+itemGrip[1]+0.5);local v=math.floor(ry+itemGrip[2]+0.5)
   if u>=0 and u<item.width and v>=0 and v<item.height then local p=item:getPixel(u,v);if alpha(p)>=128 then local dst=(isBehind and v>=itemGrip[2]-10) and back or front;dst:drawPixel(x,y,app.pixelColor.rgba(app.pixelColor.rgbaR(p),app.pixelColor.rgbaG(p),app.pixelColor.rgbaB(p),255)) end end
  end end;return back,front
 end
 local compFrames,bodyOnly,natOnly={},{},{}
 app.fs.makeAllDirectories(f(config.out.."/native"));app.fs.makeAllDirectories(f(config.out.."/layers/body"));app.fs.makeAllDirectories(f(config.out.."/layers/weaponBack"));app.fs.makeAllDirectories(f(config.out.."/layers/weaponFront"));app.fs.makeAllDirectories(f(config.out.."/layers/handFront"))
 local strip=Image(128*8,128,ColorMode.RGB);strip:clear()
 for i=1,8 do
  local wb,wf,hand=blank(256,256),blank(256,256),blank(256,256)
  local body256=bodies[i]
  if config.visible[i] then
   local g=config.grips[i];assert(g[1]>=64 and g[1]<192 and g[2]>=64 and g[2]<192,"composite grip outside body canvas")
   wb,wf=render(g,config.angles[i],config.flipBits[i],config.behind[i])
   assert(alpha(body256:getPixel(g[1],g[2]))>=128,"measured grip anchor misses actual body hand at frame "..(i-1))
   hand=handFrontFromBody(body256,g[1],g[2])
  end
  local flat=blank(256,256);flat:drawImage(wb,Point(0,0));flat:drawImage(body256,Point(0,0));flat:drawImage(wf,Point(0,0));flat:drawImage(hand,Point(0,0))
  local nat=Image(128,128,ColorMode.RGB);nat:clear();nat:drawImage(body256,Point(-64,-64))
  local n=string.format("%02d.png",i-1)
  flat:saveAs(f(config.out.."/"..n));nat:saveAs(f(config.out.."/native/"..n))
  wb:saveAs(f(config.out.."/layers/weaponBack/"..n));body256:saveAs(f(config.out.."/layers/body/"..n));wf:saveAs(f(config.out.."/layers/weaponFront/"..n));hand:saveAs(f(config.out.."/layers/handFront/"..n))
  compFrames[i]={wb,body256,wf,hand};bodyOnly[i]={body256};natOnly[i]={nat}
  strip:drawImage(nat,Point((i-1)*128,0))
 end
 strip:saveAs(f(config.out.."/native-strip.png"))
 saveSprite("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/"..config.dir.."/"..config.weaponName.."-attack-"..config.version..".aseprite",256,256,{"weaponBack","body","weaponFront","handFront"},compFrames,config.durations)
 saveSprite("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/"..config.dir.."/"..config.weaponName.."-body-"..config.version..".aseprite",256,256,{"body"},bodyOnly,config.durations)
 saveSprite("characters/orc-v1/source/aseprite/rear-recovery-v2/native/"..config.weaponName.."-body-"..config.version.."-"..config.dir..".aseprite",128,128,{config.weaponName.."_body_"..config.dir},natOnly,config.durations)
 print("R2 saved "..config.dir.." "..config.weaponName.." "..config.version)
end
local configs={
 {version="representative-v3",dir="back_r",weaponName="sword",weapon="assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png",itemGrip={48,66},
  prev="characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2",
  out="characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v3",
  -- hold frames F02/F03 normalized 20/345 -> 350/350; strike F04 100->80ms, hold F03 80->100ms
  grips={{0,0},{175,106},{166,76},{164,84},{183,92},{181,121},{170,127},{0,0}},angles={0,325,350,350,60,100,135,0},durations={90,80,90,100,80,100,100,110},flipBits={false,false,false,false,false,false,false,false},visible={false,true,true,true,true,true,true,false},behind={false,false,true,true,false,false,false,false}},
 {version="representative-v2",dir="back_r",weaponName="axe",weapon="assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png",itemGrip={36,55},
  prev="characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1",
  out="characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v2",
  grips={{0,0},{175,106},{167,73},{167,78},{173,116},{159,121},{156,139},{0,0}},angles={0,315,350,0,70,105,135,0},durations={90,80,90,100,80,100,100,110},flipBits={false,false,false,false,false,false,false,false},visible={false,true,true,true,true,true,true,false},behind={false,false,true,true,false,false,false,false}}
}
for _,c in ipairs(configs) do author(c) end
