local out='./characters/orc-v1/source/combat-rescue-v5/body-specialist/'
local exp='./experiments/main-orc-combat-rescue-v5/body-specialist/'
local f=io.open(exp..'reexport-timing.json','w');f:write('[')
for i,name in ipairs({'01-hoist','02-apex','03-impact'}) do
 local s=app.open(out..name..'-native.aseprite')
 if i>1 then f:write(',') end
 f:write('{"key":"'..name..'","durationSeconds":'..s.frames[1].duration..'}')
 app.command.SaveFileAs{ui=false,filename=exp..name..'-reexport.png'}
 s:close()
end
f:write(']');f:close()
