local src='./characters/orc-v1/source/combat-rescue-v5/body-specialist/full-back-r-axe/'
local out='./experiments/main-orc-combat-rescue-v5/body-specialist/full-back-r-axe/'
local meta={}
for _,entry in ipairs({{'native128.aseprite','native'},{'body256.aseprite','body256'}}) do
 local s=app.open(src..entry[1]);local times={}
 for i=1,#s.frames do
  local image=Image(s.width,s.height,ColorMode.RGB);image:drawSprite(s,i)
  image:saveAs(out..'reexport-'..entry[2]..'/'..string.format('%02d',i-1)..'.png')
  times[#times+1]=s.frames[i].duration
 end
 meta[entry[2]]={width=s.width,height=s.height,frames=#s.frames,durationsSeconds=times,layers=#s.layers}
 s:close()
end
local f=io.open(out..'reexport-metadata.json','w');f:write(json.encode(meta));f:close()
