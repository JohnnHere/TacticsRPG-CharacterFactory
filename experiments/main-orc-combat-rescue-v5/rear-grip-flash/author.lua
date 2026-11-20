-- Authoring script for back_r/Axe F04 (apex) and F07 (impact)
-- Executed strictly in Aseprite batch with exclusive profile
-- Produced by DEV ESPECIALISTA PEGADA (Gemini Flash Antigravity)

local E = 'experiments/main-orc-combat-rescue-v5/rear-grip-flash'
local C = 'characters/orc-v1/source/combat-rescue-v5/rear-grip-flash'

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
assert(clip.direction == 'back_r', 'Clip must be back_r')
assert(clip.category == 'Axe', 'Clip must be Axe')

-- Verify target frames F04 and F07
local f04_meta = clip.frames[5] -- 1-indexed for F04
assert(f04_meta.index == 4 and f04_meta.durationMs == 110 and f04_meta.phase == 'validated-apex', 'F04 metadata mismatch')

local f07_meta = clip.frames[8] -- 1-indexed for F07
assert(f07_meta.index == 7 and f07_meta.durationMs == 110 and f07_meta.phase == 'validated-impact', 'F07 metadata mismatch')

-- 2. Open body master
local bodyMasterSpr = app.open(file(clip.bodyMaster))
assert(bodyMasterSpr.width == 256 and bodyMasterSpr.height == 256, 'Body master must be 256x256')
assert(#bodyMasterSpr.frames == 12, 'Body master must have 12 frames')

local body_f04 = blank(256, 256)
body_f04:drawSprite(bodyMasterSpr, 5)
equal(body_f04, Image{ fromFile = file(f04_meta.png) }, 'Body F04 png verification')

local body_f07 = blank(256, 256)
body_f07:drawSprite(bodyMasterSpr, 8)
equal(body_f07, Image{ fromFile = file(f07_meta.png) }, 'Body F07 png verification')
bodyMasterSpr:close()

-- 3. Open weapon definition and master
local weaponDef = readJson('characters/orc-v1/source/combat-rescue-v5/combat/weapons/Axe/weapon.json')
local weaponMasterSpr = app.open(file(weaponDef.master))
local weaponImg = blank(96, 96)
weaponImg:drawSprite(weaponMasterSpr, 1)
weaponMasterSpr:close()
equal(weaponImg, Image{ fromFile = file(weaponDef.sprite) }, 'Weapon sprite verification')

-- 4. Configurations for the two keys
local keys = {
  {
    key = 'F04',
    sourceIndex = 4,
    phase = 'validated-apex',
    durationMs = 110,
    body = body_f04,
    bodyPng = f04_meta.png,
    nativeBodyPng = f04_meta.nativePng,
    gripItem = {36, 55},
    gripBody = {139, 72},
    angleDeg = 330,
    gripSectionV = {50, 57},
    gloveRows = {
      {67, 138, 143},
      {68, 137, 142},
      {69, 136, 141},
      {70, 136, 141},
      {71, 136, 140},
      {72, 136, 140},
      {73, 136, 140},
      {74, 136, 141},
      {75, 136, 141},
      {76, 137, 141},
      {77, 137, 142},
      {78, 139, 142}
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
  {
    key = 'F07',
    sourceIndex = 7,
    phase = 'validated-impact',
    durationMs = 110,
    body = body_f07,
    bodyPng = f07_meta.png,
    nativeBodyPng = f07_meta.nativePng,
    gripItem = {36, 55},
    gripBody = {157, 146},
    angleDeg = 120,
    gripSectionV = {50, 57},
    gloveRows = {
      {142, 155, 159},
      {143, 154, 160},
      {144, 153, 161},
      {145, 153, 161},
      {146, 153, 161},
      {147, 154, 161},
      {148, 155, 160},
      {149, 156, 159}
    },
    retouch = {
      {156, 144, app.pixelColor.rgba(92, 50, 48, 255)},
      {157, 144, app.pixelColor.rgba(92, 50, 48, 255)},
      {155, 143, app.pixelColor.rgba(78, 42, 43, 255)},
      {158, 145, app.pixelColor.rgba(78, 42, 43, 255)},
      {156, 146, app.pixelColor.rgba(27, 15, 22, 255)},
      {159, 146, app.pixelColor.rgba(27, 15, 22, 255)}
    }
  }
}

local authoredKeys = {}

for _, cfg in ipairs(keys) do
  local wb = blank(256, 256)
  local wf = blank(256, 256)
  local hf = blank(256, 256)
  local body = cfg.body

  local rad = cfg.angleDeg * math.pi / 180
  local cosA = math.cos(rad)
  local sinA = math.sin(rad)
  local gwX, gwY = cfg.gripItem[1], cfg.gripItem[2]
  local gbX, gbY = cfg.gripBody[1], cfg.gripBody[2]

  -- Draw weapon into weaponBack and weaponFront
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
          -- Leather grip inside glove goes behind body into weaponBack
          local dstLayer = (v >= cfg.gripSectionV[1] and v <= cfg.gripSectionV[2]) and wb or wf
          dstLayer:drawPixel(x, y, p)
        end
      end
    end
  end

  -- Copy genuine glove rows into handFront
  for _, row in ipairs(cfg.gloveRows) do
    local y = row[1]
    for x = row[2], row[3] do
      local p = body:getPixel(x, y)
      assert(app.pixelColor.rgbaA(p) == 255, string.format("%s: Non-opaque glove pixel at (%d, %d)", cfg.key, x, y))
      hf:drawPixel(x, y, p)
    end
  end

  -- Apply local authentic retouch pixels (inside glove only!)
  for _, ret in ipairs(cfg.retouch) do
    local rx, ry, col = ret[1], ret[2], ret[3]
    assert(app.pixelColor.rgbaA(body:getPixel(rx, ry)) == 255,
      string.format("%s: Retouch outside body at (%d, %d)", cfg.key, rx, ry))
    hf:drawPixel(rx, ry, col)
  end

  -- Paths for this key
  local keyDir = C .. '/' .. cfg.key
  app.fs.makeAllDirectories(file(keyDir .. '/source'))

  -- Create single-frame master composite.aseprite
  local compMasterPath = keyDir .. '/source/composite.aseprite'
  local compSpr = Sprite(256, 256, ColorMode.RGB)
  local layerNames = {'weaponBack', 'body', 'weaponFront', 'handFront'}
  local layerImages = {wb, body, wf, hf}
  for i, name in ipairs(layerNames) do
    local l = (i == 1) and compSpr.layers[1] or compSpr:newLayer()
    l.name = name
    compSpr:newCel(l, 1, layerImages[i], Point(0, 0))
  end
  compSpr.frames[1].duration = cfg.durationMs / 1000.0
  compSpr:saveAs(file(compMasterPath))
  compSpr:close()

  -- Create body-256.aseprite
  local body256MasterPath = keyDir .. '/source/body-256.aseprite'
  local b256Spr = Sprite(256, 256, ColorMode.RGB)
  b256Spr.layers[1].name = 'body'
  b256Spr:newCel(b256Spr.layers[1], 1, body, Point(0, 0))
  b256Spr.frames[1].duration = cfg.durationMs / 1000.0
  b256Spr:saveAs(file(body256MasterPath))
  b256Spr:close()

  -- Create hand-256.aseprite
  local hand256MasterPath = keyDir .. '/source/hand-256.aseprite'
  local h256Spr = Sprite(256, 256, ColorMode.RGB)
  h256Spr.layers[1].name = 'handFront'
  h256Spr:newCel(h256Spr.layers[1], 1, hf, Point(0, 0))
  h256Spr.frames[1].duration = cfg.durationMs / 1000.0
  h256Spr:saveAs(file(hand256MasterPath))
  h256Spr:close()

  -- Reopen saved composite.aseprite and export PNGs from it
  local savedComp = app.open(file(compMasterPath))
  local comp256 = blank(256, 256)
  comp256:drawSprite(savedComp, 1)
  save(comp256, keyDir .. '/composite-256.png')

  local nativeBody = blank(128, 128)
  local nativeComposite = blank(128, 128)
  local docMeta = {
    canvas = {256, 256},
    nativeCanvas = {128, 128},
    durationMs = math.floor(savedComp.frames[1].duration * 1000 + 0.5),
    layers = {}
  }

  for _, l in ipairs(savedComp.layers) do
    local layer256 = blank(256, 256)
    local cel = l:cel(1)
    if cel then
      layer256:drawImage(cel.image, cel.position)
    end
    save(layer256, keyDir .. '/layers/' .. l.name .. '.png')

    local layer128 = blank(128, 128)
    layer128:drawImage(layer256, Point(-64, -64))
    save(layer128, keyDir .. '/native/layers/' .. l.name .. '.png')

    if l.name == 'body' then
      nativeBody:drawImage(layer128)
      equal(layer256, body, cfg.key .. ' body layer preservation')
    end

    docMeta.layers[#docMeta.layers + 1] = {
      name = l.name,
      position = cel and {cel.position.x, cel.position.y} or nil
    }
  end

  nativeComposite:drawImage(comp256, Point(-64, -64))
  save(nativeBody, keyDir .. '/body-128.png')
  save(nativeComposite, keyDir .. '/composite-native-128.png')
  savedComp:close()

  -- Create body-128.aseprite
  local body128MasterPath = keyDir .. '/source/body-128.aseprite'
  local b128Spr = Sprite(128, 128, ColorMode.RGB)
  b128Spr.layers[1].name = 'body'
  b128Spr:newCel(b128Spr.layers[1], 1, nativeBody, Point(0, 0))
  b128Spr.frames[1].duration = cfg.durationMs / 1000.0
  b128Spr:saveAs(file(body128MasterPath))
  b128Spr:close()

  -- Save source-document.json
  local docJsonFile = assert(io.open(file(keyDir .. '/source-document.json'), 'w'))
  docJsonFile:write(json.encode(docMeta))
  docJsonFile:close()

  authoredKeys[cfg.key] = {
    cfg = cfg,
    wb = wb,
    body = body,
    wf = wf,
    hf = hf,
    nativeBody = nativeBody
  }
end

-- 5. Build combined 2-frame masters in root rear-grip-flash/source/
app.fs.makeAllDirectories(file(C .. '/source'))

-- Combined composite.aseprite (2 frames)
local combComp = Sprite(256, 256, ColorMode.RGB)
local combLayerNames = {'weaponBack', 'body', 'weaponFront', 'handFront'}
local combLayers = {}
for i, name in ipairs(combLayerNames) do
  local l = (i == 1) and combComp.layers[1] or combComp:newLayer()
  l.name = name
  combLayers[name] = l
end

combComp.frames[1].duration = keys[1].durationMs / 1000.0
combComp:newCel(combLayers['weaponBack'], 1, authoredKeys['F04'].wb, Point(0, 0))
combComp:newCel(combLayers['body'], 1, authoredKeys['F04'].body, Point(0, 0))
combComp:newCel(combLayers['weaponFront'], 1, authoredKeys['F04'].wf, Point(0, 0))
combComp:newCel(combLayers['handFront'], 1, authoredKeys['F04'].hf, Point(0, 0))

local fr2 = combComp:newFrame()
combComp.frames[2].duration = keys[2].durationMs / 1000.0
combComp:newCel(combLayers['weaponBack'], 2, authoredKeys['F07'].wb, Point(0, 0))
combComp:newCel(combLayers['body'], 2, authoredKeys['F07'].body, Point(0, 0))
combComp:newCel(combLayers['weaponFront'], 2, authoredKeys['F07'].wf, Point(0, 0))
combComp:newCel(combLayers['handFront'], 2, authoredKeys['F07'].hf, Point(0, 0))

combComp:saveAs(file(C .. '/source/composite.aseprite'))
combComp:close()

-- Combined body-256.aseprite (2 frames)
local combBody256 = Sprite(256, 256, ColorMode.RGB)
combBody256.layers[1].name = 'body'
combBody256.frames[1].duration = keys[1].durationMs / 1000.0
combBody256:newCel(combBody256.layers[1], 1, authoredKeys['F04'].body, Point(0, 0))
combBody256:newFrame()
combBody256.frames[2].duration = keys[2].durationMs / 1000.0
combBody256:newCel(combBody256.layers[1], 2, authoredKeys['F07'].body, Point(0, 0))
combBody256:saveAs(file(C .. '/source/body-256.aseprite'))
combBody256:close()

-- Combined body-128.aseprite (2 frames)
local combBody128 = Sprite(128, 128, ColorMode.RGB)
combBody128.layers[1].name = 'body'
combBody128.frames[1].duration = keys[1].durationMs / 1000.0
combBody128:newCel(combBody128.layers[1], 1, authoredKeys['F04'].nativeBody, Point(0, 0))
combBody128:newFrame()
combBody128.frames[2].duration = keys[2].durationMs / 1000.0
combBody128:newCel(combBody128.layers[1], 2, authoredKeys['F07'].nativeBody, Point(0, 0))
combBody128:saveAs(file(C .. '/source/body-128.aseprite'))
combBody128:close()

-- Combined hand-256.aseprite (2 frames)
local combHand256 = Sprite(256, 256, ColorMode.RGB)
combHand256.layers[1].name = 'handFront'
combHand256.frames[1].duration = keys[1].durationMs / 1000.0
combHand256:newCel(combHand256.layers[1], 1, authoredKeys['F04'].hf, Point(0, 0))
combHand256:newFrame()
combHand256.frames[2].duration = keys[2].durationMs / 1000.0
combHand256:newCel(combHand256.layers[1], 2, authoredKeys['F07'].hf, Point(0, 0))
combHand256:saveAs(file(C .. '/source/hand-256.aseprite'))
combHand256:close()

print('SUCCESS: Authored F04 and F07 rear axe grips, saved single and combined masters, exported all layers and composites.')
