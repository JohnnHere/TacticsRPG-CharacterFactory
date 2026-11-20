-- User correction: follow-through stays at 100 ms. Only frame timing changes.
local times={30,65,35,50,45,35,30,35,35,100,55,80,45,90}
local results={}
local function render(s,i) local a=Image(s.width,s.height);a:clear();a:drawSprite(s,i);return a end
local function equal(a,b) for y=0,a.height-1 do for x=0,a.width-1 do assert(a:getPixel(x,y)==b:getPixel(x,y),'pixel drift') end end end
for _,d in ipairs({'front_r','front_l'}) do
 local p='characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/'..d..'-sword'
 for _,kind in ipairs({'composite','body','hand','native'}) do
  local file=p..'/source/'..kind..'.aseprite'
  local s=assert(app.open(file));assert(#s.frames==14)
  local before={};for i=1,14 do before[i]=render(s,i);s.frames[i].duration=times[i]/1000 end
  s:saveAs(file);s:close();s=assert(app.open(file))
  local total=0;local strip=Image(s.width*14,s.height);strip:clear()
  for i=1,14 do
   assert(math.abs(s.frames[i].duration*1000-times[i])<0.001,'timing mismatch')
   total=total+times[i]
   local im=render(s,i);equal(im,before[i])
   local ix=string.format('%02d',i-1)
   local path=p..(kind=='composite' and '/' or kind=='body' and '/layers/body/' or kind=='hand' and '/layers/handFront/' or '/native/')..ix..'.png'
   im:saveAs(path)
   if kind=='composite' then
    im:saveAs(p..'/frames/'..ix..'.png')
    for _,l in ipairs(s.layers) do
     local li=Image(256,256);li:clear();local cel=l:cel(i)
     if cel then li:drawImage(cel.image,cel.position) end
     li:saveAs(p..'/layers/'..l.name..'/'..ix..'.png')
    end
   end
   strip:drawImage(im,Point((i-1)*s.width,0))
  end
  assert(total==730)
  if kind=='composite' then strip:saveAs(p..'/composite-strip.png') end
  if kind=='native' then strip:saveAs(p..'/native-strip.png') end
  table.insert(results,{direction=d,master=kind,frames=14,durationsMs=times,totalDurationMs=total,pixelsPreserved=true,reopenedSavedMaster=true})
  s:close()
 end
end
local f=assert(io.open('experiments/main-orc-combat-recovery-v8/frontal-inbetween-retime-result.json','w'))
f:write(json.encode({status='TECHNICALLY_COMPLETE',results=results}));f:close()
