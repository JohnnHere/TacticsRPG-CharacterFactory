-- Lua script to test assembling back_r Unarmed
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Assembling back_r Unarmed Test ===")

local rawDir = file("experiments/main-orc-rear-recovery-v2/raw")
local framesDir = app.fs.joinPath(rawDir, "frames_unarmed_r")

local baseImg = Image{ fromFile = app.fs.joinPath(framesDir, "frame_00.png") }
local f02Img = Image{ fromFile = app.fs.joinPath(framesDir, "frame_02.png") }
local f03Img = Image{ fromFile = app.fs.joinPath(framesDir, "frame_03.png") }
local impactImg = Image{ fromFile = app.fs.joinPath(rawDir, "punch_impact_key_back_r.png") }
local f05Img = Image{ fromFile = app.fs.joinPath(framesDir, "frame_05.png") }
local f06Img = Image{ fromFile = app.fs.joinPath(framesDir, "frame_06.png") }
local f07Img = Image{ fromFile = app.fs.joinPath(framesDir, "frame_07.png") }

-- Let's inspect the collar/neck in impactImg vs baseImg
-- In impactImg, let's make sure the head cranium and collar match the character volume
-- The impact key has dy=+1 to align feet at 126
local cleanImpact = Image(128, 128, ColorMode.RGB)
cleanImpact:clear()
cleanImpact:drawImage(impactImg, Point(0, 1)) -- dy=+1

-- Copy base cranium and nape outline where base has solid occipital bone and neck armor
-- y from 6 to 22, x from 55 to 76
for y = 6, 20 do
  for x = 55, 76 do
    local pb = baseImg:getPixel(x, y)
    -- If base has green skin or dark outline
    local a = app.pixelColor.rgbaA(pb)
    if a > 10 then
      cleanImpact:drawPixel(x, y + 1, pb)
    end
  end
end

-- Save clean impact frame
cleanImpact:saveAs(file("experiments/main-orc-rear-recovery-v2/punch_impact_clean.png"))

-- Option A: 5-frame sequence matching complete-v1
-- 0: base (dy=+1) [80ms]
-- 1: f03 coil (dy=+1) [110ms]
-- 2: cleanImpact (already dy=+1) [60ms]
-- 3: f05 recoil/follow-through (dy=+2) [90ms]
-- 4: f07 recovery (dy=+1) [110ms]

local s5 = Sprite(128, 128, ColorMode.RGB)
s5.layers[1].name = "Unarmed_back_r"

local frames5 = {
  { img = baseImg, dy = 1, dur = 0.08 },
  { img = f03Img, dy = 1, dur = 0.11 },
  { img = cleanImpact, dy = 0, dur = 0.06 }, -- cleanImpact already offset
  { img = f05Img, dy = 2, dur = 0.09 },
  { img = f07Img, dy = 1, dur = 0.11 }
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
s5:saveAs(file("experiments/main-orc-rear-recovery-v2/punch_test_5f.gif"))
s5:close()

-- Option B: 6-frame sequence with anticipation step
-- 0: base [70ms]
-- 1: f02 anticipation [70ms]
-- 2: f03 deep coil [80ms]
-- 3: cleanImpact [60ms]
-- 4: f05 recoil [90ms]
-- 5: f07 recovery [110ms]

local s6 = Sprite(128, 128, ColorMode.RGB)
s6.layers[1].name = "Unarmed_back_r"

local frames6 = {
  { img = baseImg, dy = 1, dur = 0.07 },
  { img = f02Img, dy = 1, dur = 0.07 },
  { img = f03Img, dy = 1, dur = 0.08 },
  { img = cleanImpact, dy = 0, dur = 0.06 },
  { img = f05Img, dy = 2, dur = 0.09 },
  { img = f07Img, dy = 1, dur = 0.11 }
}

for i = 1, #frames6 do
  if i > 1 then s6:newEmptyFrame() end
  local im = Image(128, 128, ColorMode.RGB)
  im:clear()
  im:drawImage(frames6[i].img, Point(0, frames6[i].dy))
  s6:newCel(s6.layers[1], i, im, Point(0, 0))
  s6.frames[i].duration = frames6[i].dur
end
s6:newTag(1, #frames6).name = "Attack"
s6:saveAs(file("experiments/main-orc-rear-recovery-v2/punch_test_6f.gif"))
s6:close()

print("Saved punch_test_5f.gif and punch_test_6f.gif")
