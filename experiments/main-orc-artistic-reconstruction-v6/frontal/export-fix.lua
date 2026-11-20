-- Re-export derivatives from the SAVED fixed masters to the V5-grip-specialist layout:
-- root NN.png (composite), native/NN.png, layers/body/NN.png, strips. Verify + report to file.
local E='experiments/main-orc-artistic-reconstruction-v6/frontal'
local C='characters/orc-v1/source/artistic-reconstruction-v6/frontal'
local function abs(p) return app.fs.joinPath(app.fs.currentPath,p) end
local function read(p) local f=assert(io.open(abs(p),'r'));local s=f:read('*a');f:close();return json.decode(s) end
local function save(im,p) app.fs.makeAllDirectories(app.fs.filePath(abs(p)));im:saveAs(abs(p)) end
local pc=app.pixelColor
local out=assert(io.open(abs(E..'/export-out.txt'),'w'))
local function say(s) out:write(s..'\n') end
local plan=read(E..'/fixes-plan.json').plan
local CELLS={
 ['front_l/Sword']='front_l-Sword-full',
 ['front_r/Sword']='full-front-r-sword',
 ['front_r/Axe']='front_r-Axe-full',
 ['front_l/Axe']='front_l-Axe-full'}
local allOk=true
for key,slug in pairs(CELLS) do
 local cellPlan=plan[key]
 local v5=read('characters/orc-v1/source/combat-rescue-v5/grip-specialist/'..slug..'/clip.json')
 local comp=app.open(abs(C..'/'..slug..'/source/composite.aseprite'))
 local nat=app.open(abs(C..'/'..slug..'/source/native.aseprite'))
 assert(#comp.frames==v5.frameCount and #nat.frames==v5.frameCount,'frames '..key)
 local bodyLayer=nil
 for _,l in ipairs(comp.layers) do if l.name=='body' then bodyLayer=l end end
 assert(bodyLayer,'body layer '..key)
 local verified=0
 for fid=0,#comp.frames-1 do
  local edits=cellPlan[string.format('%02d',fid)]
  local dur=v5.durationsMs[fid+1]
  assert(math.abs(comp.frames[fid+1].duration*1000-dur)<0.1,'dur comp '..key..fid)
  assert(math.abs(nat.frames[fid+1].duration*1000-dur)<0.1,'dur nat '..key..fid)
  if edits then
   local bcel=bodyLayer:cel(fid+1);assert(bcel,'bcel '..key..fid)
   for _,e in ipairs(edits) do
    local got=bcel.image:getPixel(e.x+64,e.y+64)
    local want=pc.rgba(e.to[1],e.to[2],e.to[3],e.to[4])
    assert(got==want,key..' F'..fid..' body cel mismatch')
    verified=verified+1
   end
  end
  local fr=Image(256,256,ColorMode.RGB);fr:clear();fr:drawSprite(comp,fid+1);save(fr,C..'/'..slug..'/'..string.format('%02d',fid)..'.png')
  local nr=Image(128,128,ColorMode.RGB);nr:clear();nr:drawSprite(nat,fid+1);save(nr,C..'/'..slug..'/native/'..string.format('%02d',fid)..'.png')
  if edits then
   for _,e in ipairs(edits) do
    local gp=fr:getPixel(e.x+64,e.y+64)
    assert(gp==pc.rgba(e.to[1],e.to[2],e.to[3],e.to[4]) or (e.to[4]==0 and pc.rgbaA(gp)==0),'render mismatch '..key..' F'..fid)
   end
  end
 end
 local n=#comp.frames
 local cstrip=Image(n*256,256,ColorMode.RGB);cstrip:clear()
 local nstrip=Image(n*128,128,ColorMode.RGB);nstrip:clear()
 for fi=1,n do
  local fr=Image(256,256,ColorMode.RGB);fr:clear();fr:drawSprite(comp,fi);cstrip:drawImage(fr,Point((fi-1)*256,0))
  local nr=Image(128,128,ColorMode.RGB);nr:clear();nr:drawSprite(nat,fi);nstrip:drawImage(nr,Point((fi-1)*128,0))
  local bcel=bodyLayer:cel(fi)
  assert(bcel.position.x==0 and bcel.position.y==0 and bcel.image.width==256,'body cel '..key..fi)
  save(Image(bcel.image),C..'/'..slug..'/layers/body/'..string.format('%02d',fi-1)..'.png')
 end
 save(cstrip,C..'/'..slug..'/composite-strip.png')
 save(nstrip,C..'/'..slug..'/native-strip.png')
 comp:close();nat:close()
 say(key..' OK verified='..verified..' frames='..n)
end
say('EXPORT_DONE allOk='..tostring(allOk))
out:close()
