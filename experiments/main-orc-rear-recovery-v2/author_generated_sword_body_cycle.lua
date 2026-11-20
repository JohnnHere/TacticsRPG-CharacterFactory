-- Import a single returned PixelLab skeleton-v3 representative into Aseprite.
-- The reference/base and generated frames remain an EMPTY-HAND body cycle.
local root=app.fs.currentPath
local function file(p) return app.fs.joinPath(root,p) end
local flog=io.open(file("experiments/main-orc-rear-recovery-v2/generated-cycle-author.log"),"w")
local function log(s) if flog then flog:write(s.."\n"); flog:flush() end end
local input="experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_r"
local compDir="characters/orc-v1/source/rear-recovery-v2/back_r/Sword/body-cycle-generated-v1"
local nativeMaster="characters/orc-v1/source/aseprite/rear-recovery-v2/native/sword-body-cycle-generated-back_r-v1.aseprite"
local compMaster="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-body-cycle-generated-v1.aseprite"
local durations={90,80,90,80,100,80,100,120}
local names={"guard-start","reach-close-fist","cock-high","load-back","slash-release","impact-follow-through","lowered-recovery","return-guard"}
app.fs.makeAllDirectories(file(compDir.."/composite"))
app.fs.makeAllDirectories(file(compDir.."/native"))
app.fs.makeAllDirectories(app.fs.filePath(file(nativeMaster)))
app.fs.makeAllDirectories(app.fs.filePath(file(compMaster)))
log("directories created")
local nativeFrames,compFrames={},{}
for i=0,7 do
  log("frame "..i)
  local source=i==0 and "characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack/native/00.png" or (input.."/"..string.format("%02d.png",i-1))
  log("load "..source)
  local im=Image{fromFile=file(source)}
  log("loaded "..im.width.."x"..im.height)
  assert(im.width==128 and im.height==128,"skeleton-v3 frame must be native 128x128: "..source)
  nativeFrames[i+1]=im
  local comp=Image(256,256,ColorMode.RGB); comp:clear(); comp:drawImage(im,Point(64,64)); compFrames[i+1]=comp
  im:saveAs(file(compDir.."/native/"..string.format("%02d.png",i)))
  comp:saveAs(file(compDir.."/composite/"..string.format("%02d.png",i)))
end
local function save(path,w,h,layerName,frames)
  log("save "..path)
  local s=Sprite(w,h,ColorMode.RGB); s.layers[1].name=layerName
  for i=1,#frames do
    if i>1 then s:newEmptyFrame() end
    s:newCel(s.layers[1],i,frames[i],Point(0,0)); s.frames[i].duration=durations[i]/1000
  end
  s:newTag(1,#frames).name="Attack"; s:saveAs(file(path)); s:close()
  log("saved "..path)
end
save(nativeMaster,128,128,"Sword_body_back_r",nativeFrames)
save(compMaster,256,256,"empty-hand-body",compFrames)
local strip=Image(128*8,128,ColorMode.RGB); strip:clear()
for i=1,8 do strip:drawImage(nativeFrames[i],Point((i-1)*128,0)) end
strip:saveAs(file(compDir.."/native-strip.png"))
print("Saved separate Aseprite native128 and composite256 empty-hand body cycle; no weapon layers attached.")
log("done")
if flog then flog:close() end
