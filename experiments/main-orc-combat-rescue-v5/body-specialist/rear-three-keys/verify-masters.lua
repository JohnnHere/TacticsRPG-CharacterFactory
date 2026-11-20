local src='./characters/orc-v1/source/combat-rescue-v5/body-specialist/rear-three-keys/'
local out='./experiments/main-orc-combat-rescue-v5/body-specialist/rear-three-keys/'
local records={}
for _,group in ipairs({'back_r-Sword','back_l-Sword','back_l-Axe'}) do
 for key=1,3 do for _,kind in ipairs({'native','body256'}) do
  local name=group..'/'..string.format('%02d',key)..'-'..kind
  local s=app.open(src..name..'.aseprite');local img=Image(s.width,s.height,ColorMode.RGB);img:drawSprite(s,1)
  img:saveAs(out..'reexports/'..group..'-'..string.format('%02d',key)..'-'..kind..'.png')
  records[#records+1]={group=group,key=key,kind=kind,width=s.width,height=s.height,frames=#s.frames,layers=#s.layers,durationSeconds=s.frames[1].duration}
  s:close()
 end end
end
local f=io.open(out..'reexport-metadata.json','w');f:write(json.encode(records));f:close()
