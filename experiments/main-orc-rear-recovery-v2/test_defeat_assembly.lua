-- Lua script to test assembling front_r and front_l Defeat
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Assembling front_r and front_l Defeat Test ===")

for _, d in ipairs({ "front_r", "front_l" }) do
  local cand_native = file(string.format("experiments/main-orc-rear-recovery-v2/raw/defeat_%s_04_candidate.png", d))
  local newTermImg = Image{ fromFile = cand_native }
  
  local s = Sprite(256, 256, ColorMode.RGB)
  s.layers[1].name = "Defeat"
  
  local durations = { 0.07, 0.095, 0.115, 0.13, 0.29 }
  
  -- Load frames 0..3 from complete-v1
  for i = 1, 4 do
    if i > 1 then s:newEmptyFrame() end
    local p = file(string.format("characters/orc-v1/source/complete-v1/%s/Defeat/%02d.png", d, i - 1))
    local fImg = Image{ fromFile = p }
    s:newCel(s.layers[1], i, fImg, Point(0, 0))
    s.frames[i].duration = durations[i]
  end
  
  -- Frame 5 (idx 4): new terminal ground collapse
  -- Centered in 256x256 composite canvas (offset +64, +64)
  local compTerm = Image(256, 256, ColorMode.RGB)
  compTerm:clear()
  compTerm:drawImage(newTermImg, Point(64, 64))
  
  s:newEmptyFrame()
  s:newCel(s.layers[1], 5, compTerm, Point(0, 0))
  s.frames[5].duration = durations[5]
  
  s:newTag(1, 5).name = "Defeat"
  local gifPath = file(string.format("experiments/main-orc-rear-recovery-v2/defeat_%s_test.gif", d))
  s:saveAs(gifPath)
  s:close()
  print("Saved: " .. gifPath)
end
