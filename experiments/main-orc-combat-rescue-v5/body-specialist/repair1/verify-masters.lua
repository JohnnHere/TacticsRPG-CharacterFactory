local src='./characters/orc-v1/source/combat-rescue-v5/body-specialist/repair1/'
local out='./experiments/main-orc-combat-rescue-v5/body-specialist/repair1/'
local f=io.open(out..'reexport-timing.json','w');f:write('[')
for i,kind in ipairs({'native','composite'}) do
 local s=app.open(src..'03-impact-'..kind..'.aseprite')
 if i>1 then f:write(',') end
 f:write('{"kind":"'..kind..'","durationSeconds":'..s.frames[1].duration..',"frames":'..#s.frames..'}')
 app.command.SaveFileAs{ui=false,filename=out..'03-impact-'..kind..'-reexport.png'}
 s:close()
end
f:write(']');f:close()
