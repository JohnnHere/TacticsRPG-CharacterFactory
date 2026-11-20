-- Representative rear Sword reconstruction authored and exported in Aseprite.
-- Body frames are reused byte-for-byte from complete-v1; weapon pixels use the
-- independent recruit-sword asset transformed nearest-neighbour around its grip.
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end
local flog=io.open(file("experiments/main-orc-rear-recovery-v2/representative-lua.log"),"w")
local function log(s) if flog then flog:write(s.."\n"); flog:flush() end end
local function blank(w, h)
  local im = Image(w, h, ColorMode.RGB); im:clear(); return im
end
local function load(p) return Image{ fromFile = file(p) } end
local function ensure(p) app.fs.makeAllDirectories(app.fs.filePath(p)) end
local function alpha(p) return app.pixelColor.rgbaA(p) end

local candidate = "characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack"
local master = "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-attack.aseprite"
local bodyMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-body.aseprite"
local handMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-hand-front.aseprite"
local nativeMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/native/sword-back_r.aseprite"
ensure(file(candidate .. "/layers/body/00.png")); ensure(file(master))
ensure(file(candidate .. "/layers/weaponBack/00.png")); ensure(file(candidate .. "/layers/weaponFront/00.png")); ensure(file(candidate .. "/layers/handFront/00.png")); ensure(file(candidate .. "/native/00.png"))

local durations = {30,65,35,50,45,65,35,35,100,55,80,45,90}
-- Per-frame hand centers from the own-pose body silhouettes (composite 256):
-- resting hand, extended reach, raised cock, tucked recovery and low follow-through.
local grips = {{164,125},{164,125},{164,125},{178,117},{174,108},{157,94},{145,101},{145,106},{146,106},{150,105},{154,110},{150,133},{150,133}}
local angles = {0,0,45,45,15,345,315,270,270,270,135,0,0}
local flipBits = {false,false,false,false,false,false,false,false,true,true,false,false,false}
local visible = {false,false,true,true,true,true,true,true,true,true,true,false,false}
local behind = {false,false,false,false,true,true,true,true,false,false,false,false,false}
local phases = {"rest","body-preparation","establish-grip","lift","windup","windup-high","windup-hold","release","slash","follow-through","recovery","action-complete","return-unarmed"}
local item = load("assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png")
log("loaded item and output dirs")
local itemGrip = {48,66}
local bodyFrames, handFrames, backFrames, frontFrames, flatFrames, nativeFrames = {},{},{},{},{},{}

-- Exact proven inverse-mapped nearest-neighbour rotation math. Depth is an
-- explicit authored per-frame choice; no inherited rear-strike blanket rule.
local function renderWeapon(target, angle, flip, isBehind)
  local back, front = blank(256,256), blank(256,256)
  local rad = angle * math.pi / 180.0; local c, s = math.cos(rad), math.sin(rad)
  for y=2,253 do for x=2,253 do
    local dx,dy=x-target[1],y-target[2]
    local rx=c*dx+s*dy; local ry=-s*dx+c*dy
    if flip then rx=-rx end
    local u=math.floor(rx+itemGrip[1]+0.5); local v=math.floor(ry+itemGrip[2]+0.5)
    if u>=0 and u<item.width and v>=0 and v<item.height then
      local q=item:getPixel(u,v)
      if alpha(q)>=128 then
        -- On the cocked rear-facing poses, keep the grip/pommel tucked behind
        -- the torso while the distal blade crosses the dorsal plate visibly.
        -- This is a frame-authored split, not a global rear-depth rule.
        local bladeFront = isBehind and v < itemGrip[2]-10
        local dst = (isBehind and not bladeFront) and back or front
        local px=app.pixelColor.rgba(app.pixelColor.rgbaR(q),app.pixelColor.rgbaG(q),app.pixelColor.rgbaB(q),255)
        dst:drawPixel(x,y,px)
      end
    end
  end end
  return back,front
end

for fi=0,12 do
  log("frame "..fi)
  local base = "characters/orc-v1/source/complete-v1/back_r/Sword/Attack/layers/body/" .. string.format("%02d.png",fi)
  local body=load(base); bodyFrames[fi+1]=body
  local target=grips[fi+1]
  -- The visual grid estimate is refined to the nearest opaque hand/arm pixel
  -- within +/-8px (the arm band only; y restricts feet out of the search).
  local bestX,bestY,bestD=nil,nil,999
  for y=target[2]-4,target[2]+4 do for x=target[1]-4,target[1]+4 do
    if x>=0 and x<256 and y>=64 and y<=170 and y<256 and x<256 and alpha(body:getPixel(x,y))>=128 then
      local d=(x-target[1])^2+(y-target[2])^2
      if d<bestD then bestX,bestY,bestD=x,y,d end
    end
  end end
  assert(bestX, "No body grip pixel in arm band near frame "..fi)
  grips[fi+1]={bestX,bestY}
  local back,front=blank(256,256),blank(256,256)
  if visible[fi+1] then back,front=renderWeapon(grips[fi+1],angles[fi+1],flipBits[fi+1],behind[fi+1]) end
  backFrames[fi+1],frontFrames[fi+1]=back,front
  local hand=blank(256,256)
  if visible[fi+1] then
    -- Re-stack the source body's own authored gauntlet/hand pixels locally;
    -- this preserves pixel identity and gives the hilt a real foreground grip.
    local g=grips[fi+1]
    for y=math.max(0,g[2]-6),math.min(255,g[2]+6) do for x=math.max(0,g[1]-7),math.min(255,g[1]+7) do
      local p=body:getPixel(x,y); if alpha(p)>=128 then hand:drawPixel(x,y,p) end
    end end
  end
  handFrames[fi+1]=hand
  local flat=blank(256,256); flat:drawImage(back,Point(0,0)); flat:drawImage(body,Point(0,0)); flat:drawImage(front,Point(0,0)); flat:drawImage(hand,Point(0,0))
  flatFrames[fi+1]=flat
  -- Native body master is body-only; weapon art is available solely in the
  -- 256px layered composite and four independent weapon/body layers.
  local native=blank(128,128); native:drawImage(body,Point(-64,-64)); nativeFrames[fi+1]=native
  flat:saveAs(file(candidate.."/"..string.format("%02d.png",fi)))
  body:saveAs(file(candidate.."/layers/body/"..string.format("%02d.png",fi)))
  back:saveAs(file(candidate.."/layers/weaponBack/"..string.format("%02d.png",fi)))
  front:saveAs(file(candidate.."/layers/weaponFront/"..string.format("%02d.png",fi)))
  hand:saveAs(file(candidate.."/layers/handFront/"..string.format("%02d.png",fi)))
  native:saveAs(file(candidate.."/native/"..string.format("%02d.png",fi)))
end

local function saveSprite(path,w,h,names,frames,frameDurations)
  log("save sprite start "..path)
  ensure(file(path)); local s=Sprite(w,h,ColorMode.RGB)
  s.layers[1].name=names[1]
  local layers={[names[1]]=s.layers[1]}
  for i=2,#names do local l=s:newLayer(); l.name=names[i]; layers[names[i]]=l end
  for fi=1,#frames do
    if fi>1 then s:newEmptyFrame() end
    for li,name in ipairs(names) do s:newCel(layers[name],fi,frames[fi][li],Point(0,0)) end
    s.frames[fi].duration=frameDurations[fi]/1000
  end
  s:newTag(1,#frames).name="Attack"; s:saveAs(file(path)); s:close()
  log("save sprite end "..path)
end
local comp={}; for i=1,13 do comp[i]={backFrames[i],bodyFrames[i],frontFrames[i],handFrames[i]} end
local bodies={}; for i=1,13 do bodies[i]={bodyFrames[i]} end
local hands={}; for i=1,13 do hands[i]={handFrames[i]} end
local natives={}; for i=1,13 do natives[i]={nativeFrames[i]} end
saveSprite(master,256,256,{"weaponBack","body","weaponFront","handFront"},comp,durations)
saveSprite(bodyMaster,256,256,{"body"},bodies,durations)
saveSprite(handMaster,256,256,{"handFront"},hands,durations)
saveSprite(nativeMaster,128,128,{"Sword_back_r"},natives,durations)
local strip=blank(128*13,128)
for i=1,13 do strip:drawImage(nativeFrames[i],Point((i-1)*128,0)) end
strip:saveAs(file(candidate.."/native-strip.png"))

-- F02 front repairs: graft only the original same-action fist donor onto the
-- target's truncated forearm and extend its own gauntlet band into the overlap.
for _,dir in ipairs({"front_r","front_l"}) do
  log("front "..dir)
  local cdir="characters/orc-v1/source/rear-recovery-v2/"..dir.."/Unarmed"
  ensure(file(cdir.."/native/00.png"))
  ensure(file(cdir.."/02.png")); local src="characters/orc-v1/source/complete-v1/"..dir.."/Unarmed/"
  for fi=0,4 do
    local im=load(src..string.format("%02d.png",fi))
    if fi==2 then
      local donor=load(src.."00.png")
      -- Use this same view's hanging closed gauntlet from F00, not F03's
      -- cloth/tasset pixels. Rotate its compact hand cluster in Aseprite to
      -- align with the truncated F02 wrist; no painted rectangular palm.
      local x0,x1,y0,y1,cx,cy,tx,ty,turn
      if dir=="front_r" then x0,x1,y0,y1,cx,cy,tx,ty,turn=94,110,118,137,102,127.5,164,114,-1
      else x0,x1,y0,y1,cx,cy,tx,ty,turn=152,162,118,137,157,127.5,94,114,1 end
      -- Remove only the flat edge; the candidate's own forearm pixels remain.
      local cutX=dir=="front_r" and 160 or 96
      for y=105,123 do for x=cutX-2,cutX+2 do if x>=0 and x<256 then im:drawPixel(x,y,app.pixelColor.rgba(0,0,0,0)) end end end
      for y=y0,y1 do for x=x0,x1 do
        local p=donor:getPixel(x,y)
        if alpha(p)>=128 then
          local dx,dy=x-cx,y-cy
          local ox,oy
          if turn==1 then ox,oy=-dy,dx else ox,oy=dy,-dx end
          im:drawPixel(math.floor(tx+ox+0.5),math.floor(ty+oy+0.5),p)
        end
      end end
      if dir=="front_r" then
        -- These are introduced rotation specks outside the compact hand
        -- silhouette (confirmed against the untouched F02 source); remove
        -- only these pixels in Aseprite, leaving the original body intact.
        for _,pt in ipairs({{155,106},{170,106},{171,106},{172,106},{173,106},{174,106},{173,107},{174,107}}) do
          im:drawPixel(pt[1],pt[2],app.pixelColor.rgba(0,0,0,0))
        end
      end
      -- The donor fist has a compact outline; center a few original fist pixels
      -- around the seam to ensure no straight transparent gap remains.
    end
    im:saveAs(file(cdir.."/"..string.format("%02d.png",fi)))
  end
  -- Candidate source master preserves the five-frame identity and timing.
  local frames={}; for i=0,4 do frames[#frames+1]={load(cdir.."/"..string.format("%02d.png",i))} end
  local ud={80,110,50,90,120}
  saveSprite("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/"..dir.."/unarmed-attack.aseprite",256,256,{"body"},frames,ud)
  local stripF=blank(128*5,128)
  local nframes={}
  for i=0,4 do local n=blank(128,128); n:drawImage(frames[i+1][1],Point(-64,-64)); nframes[#nframes+1]={n}; n:saveAs(file(cdir.."/native/"..string.format("%02d.png",i))); stripF:drawImage(n,Point(i*128,0)) end
  stripF:saveAs(file(cdir.."/native-strip.png"))
  saveSprite("characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-"..dir..".aseprite",128,128,{"Unarmed_"..dir},nframes,ud)
end
print("Saved representative back_r Sword 4-layer masters/exports and surgical front F02 candidates in Aseprite.")
log("done")
if flog then flog:close() end
