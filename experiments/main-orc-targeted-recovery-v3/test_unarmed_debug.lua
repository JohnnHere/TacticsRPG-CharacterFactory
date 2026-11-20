local root = app.fs.currentPath
local function file(p)
  if app.fs.isAbsolutePath(p) then return p end
  return app.fs.joinPath(root, p)
end
local logFile = io.open("tmp/unarmed_debug.log", "w")
local function log(msg)
  if logFile then logFile:write(msg .. "\n"); logFile:flush() end
  print(msg)
end

log("Starting unarmed debug")
local status, err = pcall(function()
  -- test each block
  log("Test 1: front_r / front_l")
  for _, d in ipairs({ "front_r", "front_l" }) do
    log("Checking " .. d)
    local candDir = file(string.format("characters/orc-v1/source/rear-recovery-v2/%s/Unarmed", d))
    for fi = 1, 5 do
      local p = app.fs.joinPath(candDir, string.format("%02d.png", fi - 1))
      local im = Image{ fromFile = p }
      if not im then error("Missing: " .. p) end
    end
  end
  log("Test 1 OK")

  log("Test 2: back_r")
  local candDirR = file("characters/orc-v1/source/rear-recovery-v2/back_r/Unarmed")
  for fi = 1, 5 do
    local p = app.fs.joinPath(candDirR, string.format("%02d.png", fi - 1))
    local im = Image{ fromFile = p }
    if not im then error("Missing: " .. p) end
  end
  log("Test 2 OK")

  log("Test 3: back_l assets")
  local pBase = file("experiments/main-orc-complete-v1/pixellab-recovery/back_l_base.png")
  local pImp = file("experiments/main-orc-rear-recovery-v2/punch_impact_clean_l.png")
  local imBase = Image{ fromFile = pBase }
  if not imBase then error("Missing: " .. pBase) end
  local imImp = Image{ fromFile = pImp }
  if not imImp then error("Missing: " .. pImp) end
  log("Test 3 OK")
end)

if not status then
  log("ERROR: " .. tostring(err))
else
  log("All pre-checks PASSED")
end
if logFile then logFile:close() end
