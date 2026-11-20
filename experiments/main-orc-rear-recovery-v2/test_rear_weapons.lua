-- Lua script to test assembling back_r Sword and Axe with new dynamic body poses
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Assembling back_r Sword & Axe Candidate Test ===")

-- 1. SWORD
local swordCandDir = file("experiments/main-orc-rear-recovery-v2/sword_test")
app.fs.makeAllDirectories(swordCandDir)

local sword_slash_body = Image{ fromFile = file("experiments/main-orc-rear-recovery-v2/raw/clean_sword_slash_r.png") }
local sword_slash_comp = Image(256, 256, ColorMode.RGB)
sword_slash_comp:clear()
sword_slash_comp:drawImage(sword_slash_body, Point(64, 64))

local s_sword = Sprite(256, 256, ColorMode.RGB)
s_sword.layers[1].name = "Sword Attack"

local sword_durations = { 0.03, 0.065, 0.035, 0.05, 0.045, 0.065, 0.035, 0.035, 0.10, 0.055, 0.08, 0.045, 0.09 }

for i = 1, 13 do
  if i > 1 then s_sword:newEmptyFrame() end
  local p = file(string.format("characters/orc-v1/source/complete-v1/back_r/Sword/Attack/%02d.png", i - 1))
  local origComp = Image{ fromFile = p }
  
  local outComp = Image(256, 256, ColorMode.RGB)
  outComp:clear()
  
  -- For drive and strike-follow-through (frames 6, 7, 8 -> i=7, 8, 9), inject our driving body pose with sword overlay
  if i >= 7 and i <= 9 then
    -- Layer body
    outComp:drawImage(sword_slash_comp, Point(0, 0))
    -- Overlay weaponFront/weaponBack from complete-v1 layers
    local wf_p = file(string.format("characters/orc-v1/source/complete-v1/back_r/Sword/Attack/layers/weaponFront/%02d.png", i - 1))
    local wb_p = file(string.format("characters/orc-v1/source/complete-v1/back_r/Sword/Attack/layers/weaponBack/%02d.png", i - 1))
    if app.fs.isFile(wb_p) then
      local wb = Image{ fromFile = wb_p }
      outComp:drawImage(wb, Point(0, 0))
    end
    if app.fs.isFile(wf_p) then
      local wf = Image{ fromFile = wf_p }
      outComp:drawImage(wf, Point(0, 0))
    end
  else
    outComp:drawImage(origComp, Point(0, 0))
  end
  
  s_sword:newCel(s_sword.layers[1], i, outComp, Point(0, 0))
  s_sword.frames[i].duration = sword_durations[i]
end

s_sword:newTag(1, 13).name = "Attack"
s_sword:saveAs(file("experiments/main-orc-rear-recovery-v2/sword_back_r_test.gif"))
s_sword:close()
print("Saved sword_back_r_test.gif")

-- 2. AXE
local axe_cocked_body = Image{ fromFile = file("experiments/main-orc-rear-recovery-v2/test_axe_r_clean.png") }
local axe_cocked_comp = Image(256, 256, ColorMode.RGB)
axe_cocked_comp:clear()
axe_cocked_comp:drawImage(axe_cocked_body, Point(64, 64))

local s_axe = Sprite(256, 256, ColorMode.RGB)
s_axe.layers[1].name = "Axe Attack"

local axe_durations = { 0.04, 0.065, 0.035, 0.08, 0.155, 0.035, 0.115, 0.11, 0.13, 0.05, 0.09, 0.10 }

for i = 1, 12 do
  if i > 1 then s_axe:newEmptyFrame() end
  local p = file(string.format("characters/orc-v1/source/complete-v1/back_r/Axe/Attack/%02d.png", i - 1))
  local origComp = Image{ fromFile = p }
  
  local outComp = Image(256, 256, ColorMode.RGB)
  outComp:clear()
  
  -- For cocked-shoulder (frame 4 -> i=5), inject our heavy overhead cocked body pose
  if i == 5 then
    outComp:drawImage(axe_cocked_comp, Point(0, 0))
    local wf_p = file(string.format("characters/orc-v1/source/complete-v1/back_r/Axe/Attack/layers/weaponFront/%02d.png", i - 1))
    local wb_p = file(string.format("characters/orc-v1/source/complete-v1/back_r/Axe/Attack/layers/weaponBack/%02d.png", i - 1))
    if app.fs.isFile(wb_p) then
      local wb = Image{ fromFile = wb_p }
      outComp:drawImage(wb, Point(0, 0))
    end
    if app.fs.isFile(wf_p) then
      local wf = Image{ fromFile = wf_p }
      outComp:drawImage(wf, Point(0, 0))
    end
  else
    outComp:drawImage(origComp, Point(0, 0))
  end
  
  s_axe:newCel(s_axe.layers[1], i, outComp, Point(0, 0))
  s_axe.frames[i].duration = axe_durations[i]
end

s_axe:newTag(1, 12).name = "Attack"
s_axe:saveAs(file("experiments/main-orc-rear-recovery-v2/axe_back_r_test.gif"))
s_axe:close()
print("Saved axe_back_r_test.gif")
