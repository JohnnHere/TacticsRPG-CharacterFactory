local root = app.fs.currentPath
local p = app.fs.joinPath(root, "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-attack-representative-v2.aseprite")
print("step1 path=" .. p)
local spr = app.open(p)
print("step2 spr=" .. tostring(spr))
if spr ~= nil then
  print("step3 size=" .. spr.width .. "x" .. spr.height)
end
print("step4 end")
