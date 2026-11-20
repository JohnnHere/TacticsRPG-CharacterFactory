-- Authoring script for full 12-frame back_r/Sword combat cycle (730ms)
-- Strict attack-only-v1 policy: visibleInterval [2, 8] (F02..F08) with bookends F00..F01 & F09..F11 transparent
-- Zero body RGBA delta, 730ms preserved timing, F03/F04/F07 structural keys preserved
-- Reuses the method accepted by QA for back_r/Axe and back_l/Sword, adapted to back_r diagonal Sword slash
-- Executed in Aseprite batch with exclusive profile tmp/aseprite-rear-grip-flash-profile
-- DEV ESPECIALISTA PEGADA (Gemini Flash Antigravity)

local E = 'experiments/main-orc-combat-rescue-v5/rear-grip-flash/full-back-r-sword'
local C = 'characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/full-back-r-sword'

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

-- 1. Read input body clip metadata
local bodyClip = readJson('characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/back_r-Sword-full/clip.json')
assert(bodyClip.frameCount == 12, 'Clip must have 12 frames')
assert(bodyClip.totalDurationMs == 730, 'Clip total duration must be 730ms')
assert(bodyClip.direction == 'back_r', 'Clip must be back_r')
assert(bodyClip.category == 'Sword', 'Clip must be Sword')

-- 2. Open body master
local bodyMasterSpr = app.open(file(bodyClip.bodyMaster))
assert(bodyMasterSpr.width == 256 and bodyMasterSpr.height == 256, 'Body master must be 256x256')
assert(#bodyMasterSpr.frames == 12, 'Body master must have 12 frames')

-- 3. Open weapon definition and master
local weaponDef = readJson('characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/weapon.json')
local weaponMasterSpr = app.open(file(weaponDef.master))
local weaponImg = blank(96, 96)
weaponImg:drawSprite(weaponMasterSpr, 1)
weaponMasterSpr:close()
equal(weaponImg, Image{ fromFile = file(weaponDef.sprite) }, 'Weapon sprite verification')

local gwX, gwY = 48, 66
local gripSectionV = {60, 70}

-- 4. Active configurations for all 12 frames
local frameConfigs = {
  -- F00: guard (40ms) - weapon hidden
  { index = 0, phase = "guard", durationMs = 40, visible = false },
  -- F01: chamber-init (60ms) - weapon hidden
  { index = 1, phase = "chamber-init", durationMs = 60, visible = false },
  -- F02: hoist-lift (60ms) - weapon visible
  {
    index = 2, phase = "hoist-lift", durationMs = 60, visible = true,
    grip = {168, 114}, angleDeg = 355,
    rows = {
      {109, 163, 172}, {110, 163, 172}, {111, 163, 172}, {112, 163, 172},
      {113, 163, 172}, {114, 163, 172}, {115, 163, 172}, {116, 163, 172}
    },
    retouch = {
      {167, 113, app.pixelColor.rgba(45, 26, 31, 255)},
      {168, 113, app.pixelColor.rgba(45, 26, 31, 255)},
      {167, 115, app.pixelColor.rgba(35, 20, 25, 255)},
      {168, 115, app.pixelColor.rgba(27, 15, 22, 255)}
    }
  },
  -- F03: 01-hoist (70ms) - weapon visible (STRUCTURAL KEY)
  {
    index = 3, phase = "01-hoist", durationMs = 70, visible = true,
    grip = {164, 108}, angleDeg = 10,
    rows = {
      {104, 159, 169}, {105, 159, 169}, {106, 159, 169}, {107, 159, 169},
      {108, 159, 169}, {109, 159, 169}, {110, 159, 169}, {111, 159, 169}
    },
    retouch = {
      {163, 107, app.pixelColor.rgba(45, 26, 31, 255)},
      {164, 107, app.pixelColor.rgba(45, 26, 31, 255)},
      {163, 109, app.pixelColor.rgba(35, 20, 25, 255)},
      {164, 109, app.pixelColor.rgba(27, 15, 22, 255)}
    }
  },
  -- F04: 02-apex (70ms) - weapon visible (STRUCTURAL KEY)
  {
    index = 4, phase = "02-apex", durationMs = 70, visible = true,
    grip = {180, 116}, angleDeg = 45,
    rows = {
      {112, 174, 186}, {113, 174, 186}, {114, 174, 186}, {115, 174, 186},
      {116, 174, 186}, {117, 174, 186}, {118, 174, 186}, {119, 174, 186}
    },
    retouch = {
      {179, 115, app.pixelColor.rgba(45, 26, 31, 255)},
      {180, 115, app.pixelColor.rgba(45, 26, 31, 255)},
      {179, 117, app.pixelColor.rgba(35, 20, 25, 255)},
      {180, 117, app.pixelColor.rgba(27, 15, 22, 255)},
      {178, 116, app.pixelColor.rgba(37, 19, 26, 255)}
    }
  },
  -- F05: slash-cleave (40ms) - weapon visible
  {
    index = 5, phase = "slash-cleave", durationMs = 40, visible = true,
    grip = {172, 131}, angleDeg = 80,
    rows = {
      {126, 168, 176}, {127, 168, 176}, {128, 168, 176}, {129, 168, 177},
      {130, 169, 178}, {131, 169, 178}, {132, 169, 178}
    },
    retouch = {
      {171, 130, app.pixelColor.rgba(45, 26, 31, 255)},
      {172, 130, app.pixelColor.rgba(45, 26, 31, 255)},
      {171, 131, app.pixelColor.rgba(35, 20, 25, 255)},
      {172, 131, app.pixelColor.rgba(27, 15, 22, 255)}
    }
  },
  -- F06: slash-descent (40ms) - weapon visible (GLM REPAIRED)
  {
    index = 6, phase = "slash-descent", durationMs = 40, visible = true,
    grip = {162, 135}, angleDeg = 105,
    rows = {
      {131, 157, 166}, {132, 157, 166}, {133, 157, 166}, {134, 157, 166},
      {135, 157, 166}, {136, 157, 166}, {137, 157, 166}, {138, 157, 166}
    },
    retouch = {
      {161, 134, app.pixelColor.rgba(45, 26, 31, 255)},
      {162, 134, app.pixelColor.rgba(45, 26, 31, 255)},
      {161, 136, app.pixelColor.rgba(35, 20, 25, 255)},
      {162, 136, app.pixelColor.rgba(27, 15, 22, 255)}
    }
  },
  -- F07: 03-impact (90ms) - weapon visible (STRUCTURAL KEY)
  {
    index = 7, phase = "03-impact", durationMs = 90, visible = true,
    grip = {151, 147}, angleDeg = 125,
    rows = {
      {143, 146, 155}, {144, 146, 155}, {145, 146, 155}, {146, 146, 155},
      {147, 146, 154}, {148, 146, 154}, {149, 146, 153}, {150, 146, 152}
    },
    retouch = {
      {150, 146, app.pixelColor.rgba(45, 26, 31, 255)},
      {151, 146, app.pixelColor.rgba(45, 26, 31, 255)},
      {150, 147, app.pixelColor.rgba(35, 20, 25, 255)},
      {151, 147, app.pixelColor.rgba(27, 15, 22, 255)}
    }
  },
  -- F08: recover-low (70ms) - weapon visible
  {
    index = 8, phase = "recover-low", durationMs = 70, visible = true,
    grip = {159, 146}, angleDeg = 120,
    rows = {
      {142, 156, 164}, {143, 156, 164}, {144, 156, 164}, {145, 156, 164},
      {146, 156, 164}, {147, 156, 164}, {148, 156, 164}, {149, 156, 164}
    },
    retouch = {
      {158, 145, app.pixelColor.rgba(45, 26, 31, 255)},
      {159, 145, app.pixelColor.rgba(45, 26, 31, 255)},
      {158, 146, app.pixelColor.rgba(35, 20, 25, 255)},
      {159, 146, app.pixelColor.rgba(27, 15, 22, 255)}
    }
  },
  -- F09: recover-pelvis (70ms) - weapon hidden
  { index = 9, phase = "recover-pelvis", durationMs = 70, visible = false },
  -- F10: recover-guard (60ms) - weapon hidden
  { index = 10, phase = "recover-guard", durationMs = 60, visible = false },
  -- F11: guard-return (60ms) - weapon hidden
  { index = 11, phase = "guard-return", durationMs = 60, visible = false }
}

-- 5. Process all 12 frames
local processedFrames = {}

for i, cfg in ipairs(frameConfigs) do
  local fi = cfg.index + 1
  local body = blank(256, 256)
  body:drawSprite(bodyMasterSpr, fi)
  equal(body, Image{ fromFile = file(bodyClip.frames[fi].compositePng.path) }, string.format("F%02d body png verification", cfg.index))

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
  equal(nativeBody, Image{ fromFile = file(bodyClip.frames[fi].nativePng.path) }, string.format("F%02d native body verification", cfg.index))

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

-- 6. Build canonical 12-frame masters
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
compSpr:newTag(1, 12).name = 'Attack'
compSpr:saveAs(file(compMasterPath))
compSpr:close()

-- 6.2 Body 256 master (12 frames, 1 layer)
local bodyMasterPath = C .. '/source/body.aseprite'
local bSpr = Sprite(256, 256, ColorMode.RGB)
bSpr.layers[1].name = 'body'
for fi = 1, 12 do
  if fi > 1 then bSpr:newFrame() end
  local pf = processedFrames[fi]
  bSpr.frames[fi].duration = pf.cfg.durationMs / 1000.0
  bSpr:newCel(bSpr.layers[1], fi, pf.body, Point(0, 0))
end
bSpr:newTag(1, 12).name = 'Attack'
bSpr:saveAs(file(bodyMasterPath))
bSpr:saveAs(file(C .. '/source/body256.aseprite'))
bSpr:close()

-- 6.3 Hand 256 master (12 frames, 1 layer)
local handMasterPath = C .. '/source/hand.aseprite'
local hSpr = Sprite(256, 256, ColorMode.RGB)
hSpr.layers[1].name = 'handFront'
for fi = 1, 12 do
  if fi > 1 then hSpr:newFrame() end
  local pf = processedFrames[fi]
  hSpr.frames[fi].duration = pf.cfg.durationMs / 1000.0
  hSpr:newCel(hSpr.layers[1], fi, pf.hf, Point(0, 0))
end
hSpr:newTag(1, 12).name = 'Attack'
hSpr:saveAs(file(handMasterPath))
hSpr:saveAs(file(C .. '/source/hand256.aseprite'))
hSpr:close()

-- 6.4 Native 128 master (12 frames, 1 layer)
local nativeMasterPath = C .. '/source/native.aseprite'
local nSpr = Sprite(128, 128, ColorMode.RGB)
nSpr.layers[1].name = 'body'
for fi = 1, 12 do
  if fi > 1 then nSpr:newFrame() end
  local pf = processedFrames[fi]
  nSpr.frames[fi].duration = pf.cfg.durationMs / 1000.0
  nSpr:newCel(nSpr.layers[1], fi, pf.nativeBody, Point(0, 0))
end
nSpr:newTag(1, 12).name = 'Attack'
nSpr:saveAs(file(nativeMasterPath))
nSpr:saveAs(file(C .. '/source/native128.aseprite'))
nSpr:close()

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

print("SUCCESS: 12-frame back_r/Sword cycle authored, masters saved, reopened and re-exported.")
