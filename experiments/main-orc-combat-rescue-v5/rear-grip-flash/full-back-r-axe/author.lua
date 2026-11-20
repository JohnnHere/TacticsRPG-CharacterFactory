-- Authoring script for full 12-frame back_r/Axe combat cycle
-- Strict attack-only-v1 policy: visibleInterval [2, 8] (F02..F08) with bookends F00..F01 & F09..F11 transparent
-- Zero body RGBA delta, 1100ms preserved timing, F04/F07 exact byte preservation
-- Executed in Aseprite batch with exclusive profile
-- DEV ESPECIALISTA PEGADA (Gemini Flash Antigravity)

local E = 'experiments/main-orc-combat-rescue-v5/rear-grip-flash/full-back-r-axe'
local C = 'characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/full-back-r-axe'

local function file(p) return app.fs.joinPath(app.fs.currentPath, p) end
local function blank(w, h)
  local im = Image(w, h, ColorMode.RGB)
  im:clear()
  return im
end
local function readJson(p)
  local f = assert(io.open(file(p), 'r'))
  local content = f:read('*a')
  f:close()
  return json.decode(content)
end
local function save(im, p)
  app.fs.makeAllDirectories(app.fs.filePath(file(p)))
  im:saveAs(file(p))
end
local function equal(a, b, msg)
  assert(a.width == b.width and a.height == b.height, (msg or '') .. ': Dimensions differ')
  for y = 0, a.height - 1 do
    for x = 0, a.width - 1 do
      local p1 = a:getPixel(x, y)
      local p2 = b:getPixel(x, y)
      assert(p1 == p2 or (app.pixelColor.rgbaA(p1) == 0 and app.pixelColor.rgbaA(p2) == 0),
        string.format("%s: Pixel mismatch at (%d, %d)", msg or 'Image', x, y))
    end
  end
end

-- 1. Read input clip metadata
local clip = readJson('characters/orc-v1/source/combat-rescue-v5/body-specialist/full-back-r-axe/clip.json')
assert(clip.frameCount == 12, 'Clip must have 12 frames')
assert(clip.totalDurationMs == 1100, 'Clip total duration must be 1100ms')
assert(clip.direction == 'back_r', 'Clip must be back_r')
assert(clip.category == 'Axe', 'Clip must be Axe')

-- 2. Open body master
local bodyMasterSpr = app.open(file(clip.bodyMaster))
assert(bodyMasterSpr.width == 256 and bodyMasterSpr.height == 256, 'Body master must be 256x256')
assert(#bodyMasterSpr.frames == 12, 'Body master must have 12 frames')

-- 3. Open weapon definition and master
local weaponDef = readJson('characters/orc-v1/source/combat-rescue-v5/combat/weapons/Axe/weapon.json')
local weaponMasterSpr = app.open(file(weaponDef.master))
local weaponImg = blank(96, 96)
weaponImg:drawSprite(weaponMasterSpr, 1)
weaponMasterSpr:close()
equal(weaponImg, Image{ fromFile = file(weaponDef.sprite) }, 'Weapon sprite verification')

local gwX, gwY = 36, 55
local gripSectionV = {50, 57}

-- 4. Active configurations for all 12 frames
local frameConfigs = {
  -- F00: guard (70ms) - weapon hidden
  { index = 0, phase = "guard", durationMs = 70, visible = false },
  -- F01: load-begin (80ms) - weapon hidden
  { index = 1, phase = "load-begin", durationMs = 80, visible = false },
  -- F02: elbow-hoist (90ms) - weapon visible
  {
    index = 2, phase = "elbow-hoist", durationMs = 90, visible = true,
    grip = {158, 71}, angleDeg = 305,
    rows = {{69, 154, 156}, {70, 154, 158}, {71, 154, 159}},
    retouch = {
      {156, 70, app.pixelColor.rgba(83, 44, 45, 255)},
      {155, 71, app.pixelColor.rgba(45, 23, 29, 255)}
    }
  },
  -- F03: validated-hoist (100ms) - weapon visible
  {
    index = 3, phase = "validated-hoist", durationMs = 100, visible = true,
    grip = {147, 72}, angleDeg = 318,
    rows = {
      {68, 146, 149}, {69, 145, 150}, {70, 144, 149}, {71, 144, 149},
      {72, 144, 148}, {73, 144, 147}, {74, 144, 147}, {75, 145, 148},
      {76, 145, 148}, {77, 145, 148}
    },
    retouch = {
      {146, 70, app.pixelColor.rgba(45, 26, 31, 255)},
      {146, 71, app.pixelColor.rgba(45, 26, 31, 255)},
      {147, 72, app.pixelColor.rgba(30, 18, 25, 255)},
      {147, 74, app.pixelColor.rgba(27, 15, 22, 255)},
      {145, 71, app.pixelColor.rgba(36, 24, 30, 255)}
    }
  },
  -- F04: validated-apex (110ms) - EXACT ACCEPTED KEY
  {
    index = 4, phase = "validated-apex", durationMs = 110, visible = true,
    grip = {139, 72}, angleDeg = 330,
    rows = {
      {67, 138, 143}, {68, 137, 142}, {69, 136, 141}, {70, 136, 141},
      {71, 136, 140}, {72, 136, 140}, {73, 136, 140}, {74, 136, 141},
      {75, 136, 141}, {76, 137, 141}, {77, 137, 142}, {78, 139, 142}
    },
    retouch = {
      {138, 70, app.pixelColor.rgba(45, 26, 31, 255)},
      {138, 71, app.pixelColor.rgba(45, 26, 31, 255)},
      {137, 72, app.pixelColor.rgba(45, 26, 31, 255)},
      {139, 70, app.pixelColor.rgba(27, 15, 22, 255)},
      {139, 73, app.pixelColor.rgba(27, 15, 22, 255)},
      {137, 71, app.pixelColor.rgba(37, 19, 26, 255)}
    }
  },
  -- F05: drop-initiation (50ms) - weapon visible
  {
    index = 5, phase = "drop-initiation", durationMs = 50, visible = true,
    grip = {147, 81}, angleDeg = 15,
    rows = {
      {76, 145, 150}, {77, 144, 150}, {78, 144, 149}, {79, 144, 148},
      {80, 144, 148}, {81, 144, 148}, {82, 144, 148}, {83, 144, 147},
      {84, 144, 148}, {85, 144, 148}, {86, 144, 148}, {87, 144, 148}
    },
    retouch = {
      {146, 80, app.pixelColor.rgba(40, 40, 46, 255)},
      {146, 81, app.pixelColor.rgba(49, 51, 55, 255)},
      {147, 79, app.pixelColor.rgba(35, 35, 41, 255)},
      {147, 82, app.pixelColor.rgba(24, 24, 30, 255)},
      {145, 80, app.pixelColor.rgba(37, 19, 26, 255)}
    }
  },
  -- F06: forward-down-cleave (60ms) - weapon visible
  {
    index = 6, phase = "forward-down-cleave", durationMs = 60, visible = true,
    grip = {172, 130}, angleDeg = 75,
    rows = {
      {127, 169, 174}, {128, 170, 174}, {129, 170, 174}, {130, 170, 174},
      {131, 170, 174}, {132, 170, 174}, {133, 170, 174}, {134, 170, 174},
      {135, 170, 174}, {136, 170, 173}
    },
    retouch = {
      {172, 129, app.pixelColor.rgba(67, 34, 38, 255)},
      {172, 130, app.pixelColor.rgba(78, 42, 43, 255)},
      {171, 128, app.pixelColor.rgba(37, 19, 26, 255)},
      {173, 131, app.pixelColor.rgba(78, 42, 43, 255)},
      {171, 130, app.pixelColor.rgba(57, 29, 32, 255)}
    }
  },
  -- F07: validated-impact (110ms) - EXACT ACCEPTED KEY
  {
    index = 7, phase = "validated-impact", durationMs = 110, visible = true,
    grip = {157, 146}, angleDeg = 120,
    rows = {
      {142, 155, 159}, {143, 154, 160}, {144, 153, 161}, {145, 153, 161},
      {146, 153, 161}, {147, 154, 161}, {148, 155, 160}, {149, 156, 159}
    },
    retouch = {
      {156, 144, app.pixelColor.rgba(92, 50, 48, 255)},
      {157, 144, app.pixelColor.rgba(92, 50, 48, 255)},
      {155, 143, app.pixelColor.rgba(78, 42, 43, 255)},
      {158, 145, app.pixelColor.rgba(78, 42, 43, 255)},
      {156, 146, app.pixelColor.rgba(27, 15, 22, 255)},
      {159, 146, app.pixelColor.rgba(27, 15, 22, 255)}
    }
  },
  -- F08: recover-low (100ms) - weapon visible
  {
    index = 8, phase = "recover-low", durationMs = 100, visible = true,
    grip = {160, 150}, angleDeg = 105,
    rows = {
      {146, 155, 158}, {147, 156, 159}, {148, 157, 159}, {149, 157, 159},
      {150, 157, 159}, {151, 157, 160}, {153, 160, 165}, {154, 160, 165},
      {155, 159, 164}, {156, 159, 163}
    },
    retouch = {
      {161, 154, app.pixelColor.rgba(92, 49, 45, 255)},
      {162, 154, app.pixelColor.rgba(78, 42, 43, 255)},
      {160, 155, app.pixelColor.rgba(36, 20, 25, 255)},
      {163, 155, app.pixelColor.rgba(27, 15, 22, 255)},
      {161, 153, app.pixelColor.rgba(54, 27, 32, 255)}
    }
  },
  -- F09: recover-pelvis (100ms) - weapon hidden
  { index = 9, phase = "recover-pelvis", durationMs = 100, visible = false },
  -- F10: recover-guard (100ms) - weapon hidden
  { index = 10, phase = "recover-guard", durationMs = 100, visible = false },
  -- F11: guard-return (130ms) - weapon hidden
  { index = 11, phase = "guard-return", durationMs = 130, visible = false }
}

-- 5. Process all 12 frames
local processedFrames = {}

for i, cfg in ipairs(frameConfigs) do
  local fi = cfg.index + 1
  local body = blank(256, 256)
  body:drawSprite(bodyMasterSpr, fi)
  equal(body, Image{ fromFile = file(clip.frames[fi].png) }, string.format("F%02d body png verification", cfg.index))

  local wb = blank(256, 256)
  local wf = blank(256, 256)
  local hf = blank(256, 256)

  if cfg.visible then
    local rad = cfg.angleDeg * math.pi / 180
    local cosA = math.cos(rad)
    local sinA = math.sin(rad)
    local gbX, gbY = cfg.grip[1], cfg.grip[2]

    for y = 0, 255 do
      for x = 0, 255 do
        local dx = x - gbX
        local dy = y - gbY
        local rx = cosA * dx + sinA * dy
        local ry = -sinA * dx + cosA * dy
        local u = math.floor(rx + gwX + 0.5)
        local v = math.floor(ry + gwY + 0.5)
        if u >= 0 and u < 96 and v >= 0 and v < 96 then
          local p = weaponImg:getPixel(u, v)
          if app.pixelColor.rgbaA(p) > 0 then
            local dstLayer = (v >= gripSectionV[1] and v <= gripSectionV[2]) and wb or wf
            dstLayer:drawPixel(x, y, p)
          end
        end
      end
    end

    for _, row in ipairs(cfg.rows) do
      local y = row[1]
      for x = row[2], row[3] do
        local p = body:getPixel(x, y)
        assert(app.pixelColor.rgbaA(p) == 255, string.format("F%02d: Non-opaque glove pixel at (%d, %d)", cfg.index, x, y))
        hf:drawPixel(x, y, p)
      end
    end

    for _, ret in ipairs(cfg.retouch) do
      local rx, ry, col = ret[1], ret[2], ret[3]
      assert(app.pixelColor.rgbaA(body:getPixel(rx, ry)) == 255,
        string.format("F%02d: Retouch outside body at (%d, %d)", cfg.index, rx, ry))
      hf:drawPixel(rx, ry, col)
    end
  end

  local nativeBody = blank(128, 128)
  nativeBody:drawImage(body, Point(-64, -64))
  equal(nativeBody, Image{ fromFile = file(clip.frames[fi].nativePng) }, string.format("F%02d native body verification", cfg.index))

  processedFrames[i] = {
    cfg = cfg,
    wb = wb,
    body = body,
    wf = wf,
    hf = hf,
    nativeBody = nativeBody
  }
end
bodyMasterSpr:close()

-- 6. Build the canonical 12-frame masters
app.fs.makeAllDirectories(file(C .. '/source'))

-- 6.1 Composite 256 master (12 frames, 4 layers)
local compMasterPath = C .. '/source/composite.aseprite'
local compSpr = Sprite(256, 256, ColorMode.RGB)
local layerNames = {'weaponBack', 'body', 'weaponFront', 'handFront'}
local layers = {}
for i, name in ipairs(layerNames) do
  local l = (i == 1) and compSpr.layers[1] or compSpr:newLayer()
  l.name = name
  layers[name] = l
end

for fi = 1, 12 do
  if fi > 1 then compSpr:newFrame() end
  local pf = processedFrames[fi]
  compSpr.frames[fi].duration = pf.cfg.durationMs / 1000.0
  compSpr:newCel(layers['weaponBack'], fi, pf.wb, Point(0, 0))
  compSpr:newCel(layers['body'], fi, pf.body, Point(0, 0))
  compSpr:newCel(layers['weaponFront'], fi, pf.wf, Point(0, 0))
  compSpr:newCel(layers['handFront'], fi, pf.hf, Point(0, 0))
end
compSpr:saveAs(file(compMasterPath))
compSpr:close()

-- 6.2 Body 256 master (12 frames, 1 layer)
local body256MasterPath = C .. '/source/body256.aseprite'
local b256Spr = Sprite(256, 256, ColorMode.RGB)
b256Spr.layers[1].name = 'body'
for fi = 1, 12 do
  if fi > 1 then b256Spr:newFrame() end
  local pf = processedFrames[fi]
  b256Spr.frames[fi].duration = pf.cfg.durationMs / 1000.0
  b256Spr:newCel(b256Spr.layers[1], fi, pf.body, Point(0, 0))
end
b256Spr:saveAs(file(body256MasterPath))
b256Spr:close()

-- 6.3 Hand 256 master (12 frames, 1 layer)
local hand256MasterPath = C .. '/source/hand256.aseprite'
local h256Spr = Sprite(256, 256, ColorMode.RGB)
h256Spr.layers[1].name = 'handFront'
for fi = 1, 12 do
  if fi > 1 then h256Spr:newFrame() end
  local pf = processedFrames[fi]
  h256Spr.frames[fi].duration = pf.cfg.durationMs / 1000.0
  h256Spr:newCel(h256Spr.layers[1], fi, pf.hf, Point(0, 0))
end
h256Spr:saveAs(file(hand256MasterPath))
h256Spr:close()

-- 6.4 Native 128 master (12 frames, 1 layer)
local native128MasterPath = C .. '/source/native128.aseprite'
local n128Spr = Sprite(128, 128, ColorMode.RGB)
n128Spr.layers[1].name = 'body'
for fi = 1, 12 do
  if fi > 1 then n128Spr:newFrame() end
  local pf = processedFrames[fi]
  n128Spr.frames[fi].duration = pf.cfg.durationMs / 1000.0
  n128Spr:newCel(n128Spr.layers[1], fi, pf.nativeBody, Point(0, 0))
end
n128Spr:saveAs(file(native128MasterPath))
n128Spr:close()

-- 7. Reopen saved masters and export all production PNGs
local savedComp = app.open(file(compMasterPath))
assert(#savedComp.frames == 12, 'Saved composite must have 12 frames')

local compStrip = blank(256 * 12, 256)
local nativeBodyStrip = blank(128 * 12, 128)
local nativeCompStrip = blank(128 * 12, 128)

for fi = 1, 12 do
  local idxStr = string.format("%02d", fi - 1)
  local compImg = blank(256, 256)
  compImg:drawSprite(savedComp, fi)
  save(compImg, C .. '/frames/' .. idxStr .. '.png')
  compStrip:drawImage(compImg, Point((fi - 1) * 256, 0))

  for _, l in ipairs(savedComp.layers) do
    local layerImg = blank(256, 256)
    local cel = l:cel(fi)
    if cel then layerImg:drawImage(cel.image, cel.position) end
    save(layerImg, C .. '/layers/' .. l.name .. '/' .. idxStr .. '.png')

    local nativeLayer = blank(128, 128)
    nativeLayer:drawImage(layerImg, Point(-64, -64))
    save(nativeLayer, C .. '/native/layers/' .. l.name .. '/' .. idxStr .. '.png')

    if l.name == 'body' then
      save(nativeLayer, C .. '/native/' .. idxStr .. '.png')
      nativeBodyStrip:drawImage(nativeLayer, Point((fi - 1) * 128, 0))
      equal(layerImg, processedFrames[fi].body, string.format("F%02d re-exported body preservation", fi - 1))
    end
  end

  local nativeComp = blank(128, 128)
  nativeComp:drawImage(compImg, Point(-64, -64))
  save(nativeComp, C .. '/native-composite/' .. idxStr .. '.png')
  nativeCompStrip:drawImage(nativeComp, Point((fi - 1) * 128, 0))
end

savedComp:close()

save(compStrip, C .. '/composite-strip.png')
save(nativeBodyStrip, C .. '/native-strip.png')
save(nativeCompStrip, C .. '/native-composite-strip.png')

print("SUCCESS: 12-frame back_r/Axe cycle authored, masters saved, reopened and re-exported.")
