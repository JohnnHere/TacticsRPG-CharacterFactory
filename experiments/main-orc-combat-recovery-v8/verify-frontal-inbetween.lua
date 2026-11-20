-- Read-only proof against all saved masters; raster exports must match exactly.
local function eq(a,b) assert(a.width==b.width and a.height==b.height);for y=0,a.height-1 do for x=0,a.width-1 do assert(a:getPixel(x,y)==b:getPixel(x,y),'saved master/export mismatch') end end end
local function render(s,i) local a=Image(s.width,s.height);a:clear();a:drawSprite(s,i);return a end
for _,d in ipairs({'front_r','front_l'}) do
 local p='characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/'..d..'-sword'
 for _,kind in ipairs({'composite','body','hand','native'}) do
  local s=app.open(p..'/source/'..kind..'.aseprite');assert(#s.frames==14)
  local total=0
  for i=1,14 do
   total=total+s.frames[i].duration*1000
   local ix=string.format('%02d',i-1)
   local path=p..(kind=='composite' and '/' or kind=='body' and '/layers/body/' or kind=='hand' and '/layers/handFront/' or '/native/')..ix..'.png'
   eq(render(s,i),Image{fromFile=path})
  end
  print(d..' '..kind..' saved master/export exact; duration '..total..' ms')
  s:close()
 end
end
