-- Compose the representative PixelLab-assisted body cycle with the unchanged
-- independent recruit sword. All raster transforms and saves occur in Aseprite.
local root=app.fs.currentPath
local function file(p) return app.fs.joinPath(root,p) end
local flog=io.open(file("experiments/main-orc-rear-recovery-v2/generated-sword-compose.log"),"w")
local function log(s) if flog then flog:write(s.."\n"); flog:flush() end end
log("script-start")
local function blank() local im=Image(256,256,ColorMode.RGB); im:clear(); return im end
local function alpha(p) return app.pixelColor.rgbaA(p) end
local out="characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2"
local compMaster="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-attack-representative-v2.aseprite"
local bodyMaster="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-body-representative-v2.aseprite"
local handMaster="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-hand-front-representative-v2.aseprite"
local nativeMaster="characters/orc-v1/source/aseprite/rear-recovery-v2/native/sword-body-representative-v2-back_r.aseprite"
log("paths-defined")
app.fs.makeAllDirectories(file(out.."/layers/body")); log("body-dir")
app.fs.makeAllDirectories(file(out.."/layers/weaponBack")); log("weaponBack-dir")
app.fs.makeAllDirectories(file(out.."/layers/weaponFront")); log("weaponFront-dir")
app.fs.makeAllDirectories(file(out.."/layers/handFront")); log("handFront-dir")
app.fs.makeAllDirectories(file(out.."/native")); log("native-dir")
app.fs.makeAllDirectories(app.fs.filePath(file(compMaster))); app.fs.makeAllDirectories(app.fs.filePath(file(bodyMaster))); app.fs.makeAllDirectories(app.fs.filePath(file(handMaster))); app.fs.makeAllDirectories(app.fs.filePath(file(nativeMaster)))
log("masters-dirs")
local durations={90,80,90,80,100,80,100,110}
-- Hand centers read from the generated body's own native 1x frames (then +64
-- for the 256 canvas): f1 horizontal reach, f2/f3 cocked fist, f4 strike,
-- f5 follow-through and f6 lowered recovery. Anchors sit in visible gauntlet
-- clusters; never pick an arbitrary nearby torso/pauldron pixel.
local grips={{0,0},{175,106},{166,76},{164,84},{183,92},{181,121},{170,127},{0,0}}
-- Forward arc: release clears the body to NE, then continues right and down-right.
local angles={0,325,20,345,60,100,135,0}
local flip={false,false,false,false,true,true,false,false}
local visible={false,true,true,true,true,true,true,false}
local behind={false,false,true,true,false,false,false,false}
local phases={"guard-start","reach-close-fist","cock-high","load-back","slash-release","impact-follow-through","lowered-recovery","return-guard"}
local bodyFrames,backFrames,frontFrames,handFrames,flatFrames,nativeFrames={},{},{},{},{},{}
local item=Image{fromFile=file("assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png")}
log("item-loaded "..item.width.."x"..item.height)
local itemGrip={48,66}

local function transform(target,angle,flipX,depthBehind)
  local back,front=blank(),blank(); local rad=angle*math.pi/180; local c,s=math.cos(rad),math.sin(rad)
  for y=2,253 do for x=2,253 do
    local dx,dy=x-target[1],y-target[2]
    local rx=c*dx+s*dy; local ry=-s*dx+c*dy
    if flipX then rx=-rx end
    local u=math.floor(rx+itemGrip[1]+0.5); local v=math.floor(ry+itemGrip[2]+0.5)
    if u>=0 and u<item.width and v>=0 and v<item.height then
      local q=item:getPixel(u,v)
      if alpha(q)>=128 then
        -- Frame 2–3 are the explicitly chosen across-the-dorsal cock poses:
        -- hilt/pommel behind the body, distal blade brought over the plate.
        local bladeFront=depthBehind and v<itemGrip[2]-10
        local dst=(depthBehind and not bladeFront) and back or front
        dst:drawPixel(x,y,app.pixelColor.rgba(app.pixelColor.rgbaR(q),app.pixelColor.rgbaG(q),app.pixelColor.rgbaB(q),255))
      end
    end
  end end
  return back,front
end

for fi=0,7 do
  log("frame "..fi)
  local bp="characters/orc-v1/source/rear-recovery-v2/back_r/Sword/body-cycle-generated-v1/composite/"..string.format("%02d.png",fi)
  local body=Image{fromFile=file(bp)}; assert(body.width==256 and body.height==256,"body composite size")
  bodyFrames[fi+1]=body
  local wb,wf,hand=blank(),blank(),blank()
  if visible[fi+1] then
    local g=grips[fi+1]
    log("grip "..g[1]..","..g[2].." alpha="..alpha(body:getPixel(g[1],g[2])))
    assert(alpha(body:getPixel(g[1],g[2]))>=128,"measured fist grip is not opaque on body at frame "..fi)
    wb,wf=transform(g,angles[fi+1],flip[fi+1],behind[fi+1])
    -- Re-stack the generated frame's own closed gauntlet at the verified joint.
    for y=math.max(0,g[2]-5),math.min(255,g[2]+5) do for x=math.max(0,g[1]-5),math.min(255,g[1]+5) do
      local p=body:getPixel(x,y); if alpha(p)>=128 then hand:drawPixel(x,y,p) end
    end end
  end
  backFrames[fi+1],frontFrames[fi+1],handFrames[fi+1]=wb,wf,hand
  local composite=blank(); composite:drawImage(wb,Point(0,0)); composite:drawImage(body,Point(0,0)); composite:drawImage(wf,Point(0,0)); composite:drawImage(hand,Point(0,0)); flatFrames[fi+1]=composite
  local native=Image(128,128,ColorMode.RGB); native:clear(); native:drawImage(body,Point(-64,-64)); nativeFrames[fi+1]=native
  composite:saveAs(file(out.."/"..string.format("%02d.png",fi)))
  body:saveAs(file(out.."/layers/body/"..string.format("%02d.png",fi)))
  wb:saveAs(file(out.."/layers/weaponBack/"..string.format("%02d.png",fi)))
  wf:saveAs(file(out.."/layers/weaponFront/"..string.format("%02d.png",fi)))
  hand:saveAs(file(out.."/layers/handFront/"..string.format("%02d.png",fi)))
  native:saveAs(file(out.."/native/"..string.format("%02d.png",fi)))
end
local function save(path,w,h,names,frames)
  log("save "..path)
  local s=Sprite(w,h,ColorMode.RGB); s.layers[1].name=names[1]; local ls={[names[1]]=s.layers[1]}
  for i=2,#names do local l=s:newLayer(); l.name=names[i]; ls[names[i]]=l end
  for fi=1,#frames do
    if fi>1 then s:newEmptyFrame() end
    for li,n in ipairs(names) do s:newCel(ls[n],fi,frames[fi][li],Point(0,0)) end
    s.frames[fi].duration=durations[fi]/1000
  end
  s:newTag(1,#frames).name="Attack"; s:saveAs(file(path)); s:close()
  log("saved "..path)
end
local comp,body,hand,native={},{},{},{}
for i=1,8 do comp[i]={backFrames[i],bodyFrames[i],frontFrames[i],handFrames[i]}; body[i]={bodyFrames[i]}; hand[i]={handFrames[i]}; native[i]={nativeFrames[i]} end
save(compMaster,256,256,{"weaponBack","body","weaponFront","handFront"},comp)
save(bodyMaster,256,256,{"body"},body)
save(handMaster,256,256,{"handFront"},hand)
save(nativeMaster,128,128,{"Sword_body_back_r"},native)
local strip=Image(128*8,128,ColorMode.RGB); strip:clear()
for i=1,8 do strip:drawImage(nativeFrames[i],Point((i-1)*128,0)) end
strip:saveAs(file(out.."/native-strip.png"))
print("Saved Aseprite 4-layer representative back_r Sword cycle with body-only native128 masters.")
log("done")
if flog then flog:close() end
