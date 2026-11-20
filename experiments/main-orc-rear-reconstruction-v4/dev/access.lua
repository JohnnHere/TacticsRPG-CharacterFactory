print('Aseprite '..tostring(app.version))
local p='characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/axe-attack-representative-v1.aseprite'
local s=app.open(p); assert(s and #s.frames==8)
local f=io.open('experiments/main-orc-rear-reconstruction-v4/dev/access-source.json','w')
f:write(json.encode({version=tostring(app.version),source=p,width=s.width,height=s.height,frames=#s.frames,layers=#s.layers})); f:close();s:close()
