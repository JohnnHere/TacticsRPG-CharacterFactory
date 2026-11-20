local root=app.fs.currentPath
local function p(x) return app.fs.joinPath(root,x) end
for _,slug in ipairs({'front_r-Sword','front_l-Sword'}) do
 local c='characters/orc-v1/source/combat-recovery-v8/frontal/'..slug
 local spr=app.open(p(c..'/source/composite.aseprite'))
 assert(spr and #spr.frames==13)
 app.fs.makeAllDirectories(p(c..'/frames'))
 app.fs.makeAllDirectories(p(c..'/native'))
 for fi=1,#spr.frames do
  local im=Image(256,256,ColorMode.RGB); im:clear(); im:drawSprite(spr,fi); im:saveAs(p(c..'/frames/'..string.format('%02d',fi-1)..'.png'))
 end
 spr:close()
 local nat=app.open(p(c..'/source/native.aseprite'))
 assert(nat and #nat.frames==13)
 for fi=1,#nat.frames do local im=Image(128,128,ColorMode.RGB); im:clear(); im:drawSprite(nat,fi); im:saveAs(p(c..'/native/'..string.format('%02d',fi-1)..'.png')) end
 nat:close()
end
print('EXPORTED')
