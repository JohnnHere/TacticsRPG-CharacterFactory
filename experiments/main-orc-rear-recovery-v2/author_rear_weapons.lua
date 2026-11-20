-- Aseprite Lua authoring script for rear Sword and Axe
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Authoring Rear Sword & Axe Candidates ===")

-- Durations
local sword_durations = { 0.03, 0.065, 0.035, 0.05, 0.045, 0.065, 0.035, 0.035, 0.10, 0.055, 0.08, 0.045, 0.09 }
local axe_durations = { 0.04, 0.065, 0.035, 0.08, 0.155, 0.035, 0.115, 0.11, 0.13, 0.05, 0.09, 0.10 }

local sword_slash_r = Image{ fromFile = file("experiments/main-orc-rear-recovery-v2/raw/clean_sword_slash_r.png") }
local axe_chop_r = Image{ fromFile = file("experiments/main-orc-rear-recovery-v2/test_axe_r_clean.png") }
local sword_slash_l = Image{ fromFile = file("experiments/main-orc-rear-recovery-v2/raw/clean_sword_slash_l.png") }
local axe_chop_l = Image{ fromFile = file("experiments/main-orc-rear-recovery-v2/test_axe_l_clean.png") }

local actions_def = {
  { dir = "back_r", weapon = "Sword", numFrames = 13, durations = sword_durations, keyImg = sword_slash_r, keyFrames = { 7, 8, 9 } },
  { dir = "back_r", weapon = "Axe", numFrames = 12, durations = axe_durations, keyImg = axe_chop_r, keyFrames = { 5, 6 } },
  { dir = "back_l", weapon = "Sword", numFrames = 13, durations = sword_durations, keyImg = sword_slash_l, keyFrames = { 7, 8, 9 } },
  { dir = "back_l", weapon = "Axe", numFrames = 12, durations = axe_durations, keyImg = axe_chop_l, keyFrames = { 5, 6 } }
}

for _, act in ipairs(actions_def) do
  local candDir = file(string.format("characters/orc-v1/source/rear-recovery-v2/%s/%s/Attack", act.dir, act.weapon))
  local natMaster = file(string.format("characters/orc-v1/source/aseprite/rear-recovery-v2/native/%s-%s.aseprite", string.lower(act.weapon), act.dir))
  local compMaster = file(string.format("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/%s/%s-attack.aseprite", act.dir, string.lower(act.weapon)))
  
  app.fs.makeAllDirectories(candDir)
  app.fs.makeAllDirectories(app.fs.filePath(natMaster))
  app.fs.makeAllDirectories(app.fs.filePath(compMaster))
  
  local keyComp = Image(256, 256, ColorMode.RGB)
  keyComp:clear()
  keyComp:drawImage(act.keyImg, Point(64, 64))
  
  local compFrames = {}
  local natFrames = {}
  
  for i = 1, act.numFrames do
    local basePng = file(string.format("characters/orc-v1/source/complete-v1/%s/%s/Attack/%02d.png", act.dir, act.weapon, i - 1))
    local origComp = Image{ fromFile = basePng }
    
    local outComp = Image(256, 256, ColorMode.RGB)
    outComp:clear()
    
    local isKey = false
    for _, kf in ipairs(act.keyFrames) do
      if i == kf then isKey = true break end
    end
    
    if isKey then
      outComp:drawImage(keyComp, Point(0, 0))
      local wb_p = file(string.format("characters/orc-v1/source/complete-v1/%s/%s/Attack/layers/weaponBack/%02d.png", act.dir, act.weapon, i - 1))
      local wf_p = file(string.format("characters/orc-v1/source/complete-v1/%s/%s/Attack/layers/weaponFront/%02d.png", act.dir, act.weapon, i - 1))
      if app.fs.isFile(wb_p) then outComp:drawImage(Image{ fromFile = wb_p }, Point(0, 0)) end
      if app.fs.isFile(wf_p) then outComp:drawImage(Image{ fromFile = wf_p }, Point(0, 0)) end
    else
      outComp:drawImage(origComp, Point(0, 0))
    end
    
    compFrames[i] = outComp
    outComp:saveAs(app.fs.joinPath(candDir, string.format("%02d.png", i - 1)))
    
    local natImg = Image(128, 128, ColorMode.RGB)
    natImg:clear()
    natImg:drawImage(outComp, Point(-64, -64))
    natFrames[i] = natImg
  end
  
  -- Native strip
  local strip = Image(128 * act.numFrames, 128, ColorMode.RGB)
  strip:clear()
  for i = 1, act.numFrames do
    strip:drawImage(natFrames[i], Point((i - 1) * 128, 0))
  end
  strip:saveAs(app.fs.joinPath(candDir, "native-strip.png"))
  
  -- Masters
  local s_nat = Sprite(128, 128, ColorMode.RGB)
  s_nat.layers[1].name = string.format("%s_%s", act.weapon, act.dir)
  for i = 1, act.numFrames do
    if i > 1 then s_nat:newEmptyFrame() end
    s_nat:newCel(s_nat.layers[1], i, natFrames[i], Point(0, 0))
    s_nat.frames[i].duration = act.durations[i]
  end
  s_nat:newTag(1, act.numFrames).name = "Attack"
  s_nat:saveAs(natMaster)
  s_nat:close()
  
  local s_comp = Sprite(256, 256, ColorMode.RGB)
  s_comp.layers[1].name = string.format("%s attack body", act.weapon)
  for i = 1, act.numFrames do
    if i > 1 then s_comp:newEmptyFrame() end
    s_comp:newCel(s_comp.layers[1], i, compFrames[i], Point(0, 0))
    s_comp.frames[i].duration = act.durations[i]
  end
  s_comp:newTag(1, act.numFrames).name = "Attack"
  s_comp:saveAs(compMaster)
  s_comp:close()
  
  print(string.format("Saved %s %s masters and strip", act.dir, act.weapon))
end

print("=== Authoring Rear Weapons Complete ===")
