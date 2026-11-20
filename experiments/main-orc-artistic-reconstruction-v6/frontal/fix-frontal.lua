-- V6 frontal surgical fixes: isolated bright dots + floating (0,0,1) islands in body layer.
-- Runs ONLY in Aseprite batch. Fill colors precomputed deterministically in fixes-plan.json.
local E='experiments/main-orc-artistic-reconstruction-v6/frontal'
local C='characters/orc-v1/source/artistic-reconstruction-v6/frontal'
local function abs(p) return app.fs.joinPath(app.fs.currentPath,p) end
local function read(p) local f=assert(io.open(abs(p),'r'));local s=f:read('*a');f:close();return json.decode(s) end
local function save(im,p) app.fs.makeAllDirectories(app.fs.filePath(abs(p)));im:saveAs(abs(p)) end
local pc=app.pixelColor
local plan=read(E..'/fixes-plan.json').plan
local CELLS={
 ['front_l/Sword']='front_l-Sword-full',
 ['front_r/Sword']='full-front-r-sword',
 ['front_r/Axe']='front_r-Axe-full',
 ['front_l/Axe']='front_l-Axe-full'}
local summary={}
for key,slug in pairs(CELLS) do
 local cellPlan=plan[key]
 assert(cellPlan,'no plan for '..key)
 local applied,framesTouched=0,0
 -- masters: composite(256,4 layers), body(256), native(128)
 local comp=app.open(abs(C..'/'..slug..'/source/composite.aseprite'))
 local bodyM=app.open(abs(C..'/'..slug..'/source/body.aseprite'))
 local nat=app.open(abs(C..'/'..slug..'/source/native.aseprite'))
 assert(comp.width==256 and comp.height==256,'composite canvas')
 assert(nat.width==128 and nat.height==128,'native canvas')
 local bodyLayer=nil
 for _,l in ipairs(comp.layers) do if l.name=='body' then bodyLayer=l end end
 assert(bodyLayer,'body layer not found in composite master')
 -- apply to a sprite image with coordinate space selection
 local function applyTo(sprite,layer,nativeSpace,fid,edits)
  local fi=fid+1
  assert(fi<=#sprite.frames,'frame out of range '..fid)
  local cel=layer:cel(fi)
  assert(cel,'missing cel fi '..fid)
  assert(cel.position.x==0 and cel.position.y==0,'cel offset '..tostring(cel.position))
  local img=cel.image
  for _,e in ipairs(edits) do
   local x,y=e.x,e.y
   if not nativeSpace then x=x+64;y=y+64 end
   assert(x>=0 and x<img.width and y>=0 and y<img.height,'edit outside '..fid)
   local before=img:getPixel(x,y)
   local target=pc.rgba(e.to[1],e.to[2],e.to[3],e.to[4])
   img:drawPixel(x,y,target)
   assert(img:getPixel(x,y)==target,'apply failed')
   applied=applied+1
  end
 end
 -- apply; composite+body use composite coords, native uses native coords
 for fid=0,15 do
  local fidk=string.format('%02d',fid)
  local edits=cellPlan[fidk]
  if edits then
   framesTouched=framesTouched+1
   applyTo(comp,bodyLayer,false,fid,edits)
   applyTo(bodyM,bodyM.layers[1],false,fid,edits)
   applyTo(nat,nat.layers[1],true,fid,edits)
  end
 end
 assert(#comp.frames>=1 and #bodyM.frames>=1 and #nat.frames>=1)
 comp:saveAs(abs(C..'/'..slug..'/source/composite.aseprite'))
 bodyM:saveAs(abs(C..'/'..slug..'/source/body.aseprite'))
 nat:saveAs(abs(C..'/'..slug..'/source/native.aseprite'))
 comp:close();bodyM:close();nat:close()
 summary[#summary+1]=string.format('%s applied=%d frames=%d',key,applied,framesTouched)
end
print(table.concat(summary,' | '))
-- PHASE 2: reopen saved masters, verify pixels+durations, export derivatives.
local applied2=0
for key,slug in pairs(CELLS) do
 local cellPlan=plan[key]
 local v5=read('characters/orc-v1/source/combat-rescue-v5/grip-specialist/'..slug..'/clip.json')
 local comp=app.open(abs(C..'/'..slug..'/source/composite.aseprite'))
 local bodyM=app.open(abs(C..'/'..slug..'/source/body.aseprite'))
 local nat=app.open(abs(C..'/'..slug..'/source/native.aseprite'))
 assert(#comp.frames==v5.frameCount and #nat.frames==v5.frameCount,'frame count mismatch '..key)
 local bodyLayer=nil
 for _,l in ipairs(comp.layers) do if l.name=='body' then bodyLayer=l end end
 assert(bodyLayer,'body layer missing on reopen')
 local function verifyIn(sprite,layer,nativeSpace,fid,edits)
  local fi=fid+1
  local cel=layer:cel(fi);assert(cel,'verify: no cel '..fid)
  local img=cel.image
  for _,e in ipairs(edits) do
   local x,y=e.x,e.y
   if not nativeSpace then x=x+64;y=y+64 end
   local got=img:getPixel(x,y)
   local want=pc.rgba(e.to[1],e.to[2],e.to[3],e.to[4])
   assert(got==want,string.format('%s F%02d (%d,%d) got=%d want=%d',key,fid,x,y,got,want))
   applied2=applied2+1
  end
 end
 for fid=0,15 do
  local fidk=string.format('%02d',fid)
  local edits=cellPlan[fidk]
  local dur=v5.durationsMs[fid+1]
  if dur then
   assert(math.abs(comp.frames[fid+1].duration*1000-dur)<0.1,'comp duration F'..fid)
   assert(math.abs(nat.frames[fid+1].duration*1000-dur)<0.1,'nat duration F'..fid)
  end
  if edits then
   verifyIn(comp,bodyLayer,false,fid,edits)
   verifyIn(bodyM,bodyM.layers[1],false,fid,edits)
   verifyIn(nat,nat.layers[1],true,fid,edits)
  end
 end
 -- exports from REOPENED (saved) masters
 local n=#comp.frames
 local cstrip=Image(n*256,256,ColorMode.RGB);cstrip:clear()
 local nstrip=Image(n*128,128,ColorMode.RGB);nstrip:clear()
 for fi=1,n do
  local ix=string.format('%02d',fi-1)
  local fr=Image(256,256,ColorMode.RGB);fr:clear();fr:drawSprite(comp,fi);save(fr,C..'/'..slug..'/frames/'..ix..'.png')
  cstrip:drawImage(fr,Point((fi-1)*256,0))
  local nr=Image(128,128,ColorMode.RGB);nr:clear();nr:drawSprite(nat,fi);save(nr,C..'/'..slug..'/native/'..ix..'.png')
  nstrip:drawImage(nr,Point((fi-1)*128,0))
  local bcel=bodyLayer:cel(fi);assert(bcel,'body cel '..fi)
  assert(bcel.position.x==0 and bcel.position.y==0,'body cel offset')
  assert(bcel.image.width==256 and bcel.image.height==256,'body cel size')
  save(Image(bcel.image),C..'/'..slug..'/layers/body/'..ix..'.png')
 end
 save(cstrip,C..'/'..slug..'/composite-strip.png')
 save(nstrip,C..'/'..slug..'/native-strip.png')
 comp:close();bodyM:close();nat:close()
 summary[#summary+1]=key..' exported '..n..' frames'
end
print(table.concat(summary,' | '))
print('VERIFY_OK applied2='..applied2)

