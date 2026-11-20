-- V7 ECON DEV: read-only dump of a composite master.
-- Reads V7_MASTER (aseprite path) and V7_OUT (output dir) from the environment so the
-- same script can be reused for every clip. Exports, per frame: canvas-space layer PNGs
-- (honouring cel.position) and a flattened PNG. Nothing is modified in the source sprite.
local masterPath = os.getenv("V7_MASTER")
local outDir = os.getenv("V7_OUT")
if not masterPath or not outDir then
  print("ERROR: set V7_MASTER and V7_OUT")
  return
end

local function abs(p)
  if p:match("^%a:") then return p end
  return app.fs.joinPath(app.fs.currentPath, p)
end

local function ensureDir(path)
  app.fs.makeAllDirectories(path)
end

ensureDir(abs(outDir) .. "/layers")
ensureDir(abs(outDir) .. "/flat")

local sprite = app.open(abs(masterPath))
if not sprite then
  print("ERROR: cannot open " .. masterPath)
  return
end

print("SPRITE " .. masterPath)
print("SIZE " .. sprite.width .. "x" .. sprite.height .. " frames=" .. #sprite.frames)

for li, layer in ipairs(sprite.layers) do
  print(string.format("LAYER %d name=%s visible=%s opacity=%d blend=%s",
    li, layer.name, tostring(layer.isVisible), layer.opacity, tostring(layer.blendMode)))
end

for fi, frame in ipairs(sprite.frames) do
  print(string.format("FRAME %d durationSec=%.6f", fi - 1, frame.duration))
end

for fi, frame in ipairs(sprite.frames) do
  for li, layer in ipairs(sprite.layers) do
    local cel = layer:cel(frame)
    if cel then
      print(string.format("CEL f=%d l=%s x=%d y=%d w=%d h=%d",
        fi - 1, layer.name, cel.position.x, cel.position.y, cel.image.width, cel.image.height))
    else
      print(string.format("CEL f=%d l=%s empty", fi - 1, layer.name))
    end
  end
end

for li, layer in ipairs(sprite.layers) do
  local dir = abs(outDir) .. "/layers/" .. layer.name
  ensureDir(dir)
  for fi, frame in ipairs(sprite.frames) do
    local img = Image(sprite.spec)
    local cel = layer:cel(frame)
    if cel then
      img:drawImage(cel.image, cel.position)
    end
    img:saveAs(string.format("%s/%02d.png", dir, fi - 1))
  end
end

for fi, frame in ipairs(sprite.frames) do
  local img = Image(sprite.spec)
  for _, layer in ipairs(sprite.layers) do
    local cel = layer:cel(frame)
    if cel and layer.isVisible then
      img:drawImage(cel.image, cel.position)
    end
  end
  img:saveAs(string.format("%s/flat/%02d.png", abs(outDir), fi - 1))
end

print("DONE")
