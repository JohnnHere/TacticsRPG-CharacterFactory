-- Aseprite-only composition of authorized body cycles; body and weapon remain independent.
-- Body and weapon remain independent; source PNGs below are exports from saves.
local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local function alpha(p)return app.pixelColor.rgbaA(p)end
local durations={90,80,90,80,100,80,100,110}
local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function saveSprite(path,w,h,names,frames)
 app.fs.makeAllDirectories(app.fs.filePath(f(path)))
 local s=Sprite(w,h,ColorMode.RGB);s.layers[1].name=names[1];local ls={[names[1]]=s.layers[1]}
 for i=2,#names do local l=s:newLayer();l.name=names[i];ls[names[i]]=l end
 for fi=1,#frames do if fi>1 then s:newEmptyFrame() end;for li,n in ipairs(names) do s:newCel(ls[n],fi,frames[fi][li],Point(0,0)) end;s.frames[fi].duration=durations[fi]/1000 end
 s:newTag(1,#frames).name="Attack";s:saveAs(f(path));s:close()
end
local function handFrontFromBody(body,cx,cy)
 local layer=blank(256,256)
 -- Restack only actual per-frame fist pixels around the measured grip.
 for y=math.max(0,cy-5),math.min(127,cy+5) do for x=math.max(0,cx-5),math.min(127,cx+5) do local p=body:getPixel(x,y);if alpha(p)>0 then layer:drawPixel(x+64,y+64,p) end end end
 return layer
end
local function author(config)
 local bodies={}
 bodies[1]=Image{fromFile=f(config.base)}
 assert(bodies[1].width==128 and bodies[1].height==128)
 for i=1,7 do bodies[i+1]=Image{fromFile=f(config.cleaned.."/"..string.format("%02d.png",i-1))};assert(bodies[i+1].width==128 and bodies[i+1].height==128) end
 local layeredData={}
 local function fillWeapons()
  local item=Image{fromFile=f(config.weapon)};local itemGrip=config.itemGrip
  local backFrames,frontFrames,compositeFrames,nativeFrames,layerFrames={},{},{},{},{}
  local function render(target,angle,flipX,isBehind)
   local back,front=blank(256,256),blank(256,256);local rad=angle*math.pi/180;local c,s=math.cos(rad),math.sin(rad)
   for y=2,253 do for x=2,253 do local dx,dy=x-target[1],y-target[2];local rx=c*dx+s*dy;local ry=-s*dx+c*dy;if flipX then rx=-rx end;local u=math.floor(rx+itemGrip[1]+0.5);local v=math.floor(ry+itemGrip[2]+0.5)
    if u>=0 and u<item.width and v>=0 and v<item.height then local p=item:getPixel(u,v);if alpha(p)>=128 then local dst=(isBehind and v>=itemGrip[2]-10) and back or front;dst:drawPixel(x,y,app.pixelColor.rgba(app.pixelColor.rgbaR(p),app.pixelColor.rgbaG(p),app.pixelColor.rgbaB(p),255)) end end
   end end;return back,front
  end
  for i=1,8 do
   local wb,wf,hand=blank(256,256),blank(256,256),blank(256,256)
   if config.visible[i] then
    local g=config.grips[i];assert(g[1]>=64 and g[1]<192 and g[2]>=64 and g[2]<192,"composite grip outside body canvas")
    wb,wf=render(g,config.angles[i],config.flipBits[i],config.behind[i])
    local dx,dy=g[1]-64,g[2]-64
    assert(alpha(bodies[i]:getPixel(dx,dy))>=128,"measured grip anchor misses actual body hand at frame "..(i-1))
    hand=handFrontFromBody(bodies[i],dx,dy)
   end
   -- Snapshot after the hand edit so body layer and native128 match exactly.
   local body256=blank(256,256);body256:drawImage(bodies[i],Point(64,64))
   local flat=blank(256,256);flat:drawImage(wb,Point(0,0));flat:drawImage(body256,Point(0,0));flat:drawImage(wf,Point(0,0));flat:drawImage(hand,Point(0,0))
   local nat=Image(128,128,ColorMode.RGB);nat:clear();nat:drawImage(bodies[i],Point(0,0))
   backFrames[i],frontFrames[i],compositeFrames[i],nativeFrames[i],layerFrames[i]=wb,wf,flat,nat,{wb,body256,wf,hand}
  end
  return backFrames,frontFrames,compositeFrames,nativeFrames,layerFrames
 end
 local back,front,composite,native,layers=fillWeapons()
 app.fs.makeAllDirectories(f(config.out.."/native"));app.fs.makeAllDirectories(f(config.out.."/layers/body"));app.fs.makeAllDirectories(f(config.out.."/layers/weaponBack"));app.fs.makeAllDirectories(f(config.out.."/layers/weaponFront"));app.fs.makeAllDirectories(f(config.out.."/layers/handFront"))
 for i=1,8 do
  composite[i]:saveAs(f(config.out.."/"..string.format("%02d.png",i-1)));native[i]:saveAs(f(config.out.."/native/"..string.format("%02d.png",i-1)))
  layers[i][1]:saveAs(f(config.out.."/layers/weaponBack/"..string.format("%02d.png",i-1)));layers[i][2]:saveAs(f(config.out.."/layers/body/"..string.format("%02d.png",i-1)));layers[i][3]:saveAs(f(config.out.."/layers/weaponFront/"..string.format("%02d.png",i-1)));layers[i][4]:saveAs(f(config.out.."/layers/handFront/"..string.format("%02d.png",i-1)))
 end
 local compPath="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/"..config.dir.."/"..config.weaponName.."-attack-representative-v1.aseprite"
 local bodyPath="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/"..config.dir.."/"..config.weaponName.."-body-representative-v1.aseprite"
 local nativePath="characters/orc-v1/source/aseprite/rear-recovery-v2/native/"..config.weaponName.."-body-representative-v1-"..config.dir..".aseprite"
 local compFrames,bodyOnly,nativeOnly={},{},{}
 for i=1,8 do compFrames[i]=layers[i];bodyOnly[i]={layers[i][2]};nativeOnly[i]={native[i]} end
 saveSprite(compPath,256,256,{"weaponBack","body","weaponFront","handFront"},compFrames)
 saveSprite(bodyPath,256,256,{"body"},bodyOnly)
 saveSprite(nativePath,128,128,{config.weaponName.."_body_"..config.dir},nativeOnly)
 local strip=Image(128*8,128,ColorMode.RGB);strip:clear();local noWeapons=Image(128*8,128,ColorMode.RGB);noWeapons:clear()
 for i=1,8 do local b=Image(128,128,ColorMode.RGB);b:clear();b:drawImage(bodies[i],Point(0,0));strip:drawImage(native[i],Point((i-1)*128,0));noWeapons:drawImage(b,Point((i-1)*128,0)) end
 strip:saveAs(f(config.out.."/native-strip.png"));noWeapons:saveAs(f(config.out.."/body-only-strip.png"))
 local sheet=Image(256*4,256*2,ColorMode.RGB);sheet:clear();for i=1,8 do sheet:drawImage(composite[i],Point(((i-1)%4)*256,math.floor((i-1)/4)*256)) end;sheet:saveAs(f(config.out.."/composite-sheet-qa.png"))
 print("Saved "..config.dir.." "..config.weaponName.." 4-layer composite, independent body masters, native128 and 256 exports.")
end
local configs={
 {dir="back_l",weaponName="sword",weapon="assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png",itemGrip={48,66},base="experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png",cleaned="experiments/main-orc-rear-recovery-v2/back_l-sword-cleaned-native",out="characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1",grips={{0,0},{92,108},{104,70},{127,72},{93,71},{74,95},{100,118},{82,127}},angles={0,270,350,20,240,215,200,0},flipBits={false,false,false,false,false,false,false,false},visible={false,true,true,true,true,true,true,false},behind={false,false,false,true,true,false,false,false}},
 {dir="back_r",weaponName="axe",weapon="assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png",itemGrip={36,55},base="experiments/main-orc-rear-recovery-v2/inputs/back_r-axe-native128.png",cleaned="experiments/main-orc-rear-recovery-v2/axe-r-cleaned-native",out="characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1",grips={{0,0},{167,98},{167,73},{167,78},{173,116},{159,121},{156,139},{0,0}},angles={0,315,350,0,70,105,135,0},flipBits={false,false,false,false,false,false,false,false},visible={false,true,true,true,true,true,true,false},behind={false,false,true,true,false,false,false,false}},
 {dir="back_l",weaponName="axe",weapon="assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png",itemGrip={36,55},base="experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png",cleaned="experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native",out="characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1",grips={{0,0},{92,108},{104,78},{104,78},{86,118},{96,141},{99,145},{0,0}},angles={0,270,315,350,315,270,235,0},flipBits={false,false,false,false,false,false,false,false},visible={false,true,true,true,true,true,true,false},behind={false,false,false,true,true,false,false,false}}
}
local axeLOnly=os.getenv("ASEPRITE_AXE_L_ONLY")=="1"
for _,c in ipairs(configs) do
 if not axeLOnly or (c.dir=="back_l" and c.weaponName=="axe") then author(c) end
end
print("Representative source authoring in Aseprite complete; QA review still required.")
