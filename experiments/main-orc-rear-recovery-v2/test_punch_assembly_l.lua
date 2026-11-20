-- Lua script to test assembling back_l Unarmed
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Assembling back_l Unarmed Test ===")

local rawDir = file("experiments/main-orc-rear-recovery-v2/raw")
local baseImg = Image{ fromFile = file("experiments/main-orc-complete-v1/pixellab-recovery/back_l_base.png") }
local impactImg = Image{ fromFile = app.fs.joinPath(rawDir, "punch_impact_key_back_l.png") }

-- Load complete-v1 frames 01, 03, 04
local f01Img_comp = Image{ fromFile = file("characters/orc-v1/source/complete-v1/back_l/Unarmed/01.png") }
local f03Img_comp = Image{ fromFile = file("characters/orc-v1/source/complete-v1/back_l/Unarmed/03.png") }
local f04Img_comp = Image{ fromFile = file("characters/orc-v1/source/complete-v1/back_l/Unarmed/04.png") }

-- Extract center 128x128 from composite 256
local function crop128(srcComp)
  local im = Image(128, 128, ColorMode.RGB)
  im:clear()
  im:drawImage(srcComp, Point(-64, -64))
  return im
end

local f01Img = crop128(f01Img_comp)
local f03Img = crop128(f03Img_comp)
local f04Img = crop128(f04Img_comp)

-- Clean impact image: dy=+1 to pin ground at 126
local cleanImpact = Image(128, 128, ColorMode.RGB)
cleanImpact:clear()
cleanImpact:drawImage(impactImg, Point(0, 1))

-- Clear stray pixels near x in [54..60], y in [12..16]
for y = 12, 17 do
  for x = 54, 65 do
    cleanImpact:drawPixel(x, y, app.pixelColor.rgba(0, 0, 0, 0))
  end
end

-- Preserve cranium and nape from baseImg
for y = 6, 20 do
  for x = 50, 72 do
    local pb = baseImg:getPixel(x, y)
    local a = app.pixelColor.rgbaA(pb)
    if a > 10 then
      cleanImpact:drawPixel(x, y + 1, pb)
    end
  end
end

cleanImpact:saveAs(file("experiments/main-orc-rear-recovery-v2/punch_impact_clean_l.png"))

-- 5-frame sequence matching complete-v1 standard
-- 0: base [80ms]
-- 1: f01 coil [110ms]
-- 2: cleanImpact [60ms]
-- 3: f03 follow-through [90ms]
-- 4: f04 recovery [110ms]

local s5 = Sprite(128, 128, ColorMode.RGB)
s5.layers[1].name = "Unarmed_back_l"

local frames5 = {
  { img = baseImg, dy = 1, dur = 0.08, phase = "guard-prep" },
  { img = f01Img, dy = 0, dur = 0.11, phase = "shoulder-coil" },
  { img = cleanImpact, dy = 0, dur = 0.06, phase = "heavy-gauntlet-impact" },
  { img = f03Img, dy = 0, dur = 0.09, phase = "follow-through" },
  { img = f04Img, dy = 0, dur = 0.11, phase = "recovery-settle" }
}

for i = 1, #frames5 do
  if i > 1 then s5:newEmptyFrame() end
  local im = Image(128, 128, ColorMode.RGB)
  im:clear()
  im:drawImage(frames5[i].img, Point(0, frames5[i].dy))
  s5:newCel(s5.layers[1], i, im, Point(0, 0))
  s5.frames[i].duration = frames5[i].dur
end
s5:newTag(1, #frames5).name = "Attack"
s5:saveAs(file("experiments/main-orc-rear-recovery-v2/punch_test_l_5f.gif"))
s5:close()

print("Saved punch_test_l_5f.gif")
