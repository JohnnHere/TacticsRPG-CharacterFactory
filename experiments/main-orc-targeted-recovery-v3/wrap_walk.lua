local root = app.fs.currentPath
local function isAbs(p)
  return string.sub(p, 2, 2) == ":" or string.sub(p, 1, 1) == "/" or string.sub(p, 1, 1) == "\\"
end
local function file(p)
  if isAbs(p) then return p end
  return app.fs.joinPath(root, p)
end

local ok, err = pcall(function()
  dofile(file("experiments/main-orc-targeted-recovery-v3/repair_walk_left_arm.lua"))
end)

if not ok then
  print("LUA ERROR: " .. tostring(err))
end
