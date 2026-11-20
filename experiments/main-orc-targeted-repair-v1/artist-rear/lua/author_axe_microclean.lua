-- targeted-repair-v1 / back_r Axe micro-cleanup (forked masters only).
-- Programmatic Aseprite authorship by the agent.
-- Two defect classes only, both proven on the published freeze:
--   1) isolated detached pixels: a 2px fragment on the native top border (native 80,0-81,0
--      = composite 144-145,64) and a 1px fragment floating in empty space (native 107,87
--      = composite 171,151). Both were verified detached with 8-connectivity and viewed
--      at 16x; neither belongs to any silhouette, strap or weapon.
--   2) one row below the declared ground line: in frame index 1 the body has 8 opaque
--      pixels at composite y=191 (native y=127) while the clip declares groundY=190
--      (nativeGroundY=126) and all other frames stop exactly at 190. The rule applied is
--      geometric (no opaque body pixel below the declared ground), not chromatic.
-- No recolouring, no palette change, no weapon, no timing, no other frame touched.
local root = app.fs.currentPath
local function f(p) return app.fs.joinPath(root, p) end

local P = "experiments/main-orc-targeted-repair-v1/artist-rear/candidate/aseprite/"
local jobs = {
  {
    path = P .. "axe-attack-representative-v1-microclean.aseprite",
    offset = {0, 0},
    strays = {{3, 144, 64}, {3, 145, 64}, {7, 171, 151}},
    groundRow = {2, 190},
  },
  {
    path = P .. "axe-body-representative-v1-microclean.aseprite",
    offset = {0, 0},
    strays = {{3, 144, 64}, {3, 145, 64}, {7, 171, 151}},
    groundRow = {2, 190},
  },
  {
    path = P .. "axe-body-representative-v1-back_r-microclean.aseprite",
    offset = {0, 0},
    strays = {{3, 80, 0}, {3, 81, 0}, {7, 107, 87}},
    groundRow = {2, 126},
  },
}

for _, job in ipairs(jobs) do
  local spr = app.open(f(job.path))
  assert(spr, "not opened: " .. job.path)
  print(string.format("MASTER %s  %dx%d frames=%d layers=%d", job.path, spr.width, spr.height, #spr.frames, #spr.layers))
  -- pick the body layer by name, fall back to the first layer
  local bodyLayer
  for _, l in ipairs(spr.layers) do if l.name == "body" then bodyLayer = l end end
  if bodyLayer == nil then bodyLayer = spr.layers[1] end

  local cleared, verified = 0, 0
  for _, s in ipairs(job.strays) do
    local frameIndex, cx, cy = s[1], s[2], s[3]
    local x, y = cx + job.offset[1], cy + job.offset[2]
    local cel = bodyLayer:cel(spr.frames[frameIndex])
    assert(cel, "missing cel")
    local px, py = x - cel.position.x, y - cel.position.y
    assert(px >= 0 and py >= 0 and px < cel.image.width and py < cel.image.height,
      string.format("target %d,%d outside cel image (%dx%d)", x, y, cel.image.width, cel.image.height))
    local pxValue = cel.image:getPixel(px, py)
    local a = app.pixelColor.rgbaA(pxValue)
    assert(a > 0, string.format("expected opaque stray at %d,%d frame %d", x, y, frameIndex))
    verified = verified + 1
    print(string.format("  stray frame %d  %d,%d  rgba(%d,%d,%d,%d) -> cleared",
      frameIndex, x, y, app.pixelColor.rgbaR(pxValue), app.pixelColor.rgbaG(pxValue), app.pixelColor.rgbaB(pxValue), a))
    cel.image:drawPixel(px, py, app.pixelColor.rgba(0, 0, 0, 0))
    cleared = cleared + 1
  end

  -- ground contract: no opaque body pixel below the declared ground row
  local frameIndex, groundY = job.groundRow[1], job.groundRow[2]
  local cel = bodyLayer:cel(spr.frames[frameIndex])
  assert(cel, "missing cel")
  local rowCleared = 0
  for y = groundY + 1, spr.height - 1 do
    for x = 0, spr.width - 1 do
      local px, py = x - cel.position.x, y - cel.position.y
      if px >= 0 and py >= 0 and px < cel.image.width and py < cel.image.height then
        local v = cel.image:getPixel(px, py)
        if app.pixelColor.rgbaA(v) > 0 then
          print(string.format("  below-ground frame %d  %d,%d  rgba(%d,%d,%d,%d) -> cleared",
            frameIndex, x, y, app.pixelColor.rgbaR(v), app.pixelColor.rgbaG(v), app.pixelColor.rgbaB(v), app.pixelColor.rgbaA(v)))
          cel.image:drawPixel(px, py, app.pixelColor.rgba(0, 0, 0, 0))
          rowCleared = rowCleared + 1
        end
      end
    end
  end
  cleared = cleared + rowCleared
  print(string.format("  below-ground pixels cleared: %d (ground row %d)", rowCleared, groundY))

  -- assert nothing remains below the ground line anywhere in the clip
  local remaining = 0
  for i, fr in ipairs(spr.frames) do
    local c = bodyLayer:cel(fr)
    if c then
      for y = groundY + 1, spr.height - 1 do
        for x = 0, spr.width - 1 do
          local px, py = x - c.position.x, y - c.position.y
          if px >= 0 and py >= 0 and px < c.image.width and py < c.image.height
            and app.pixelColor.rgbaA(c.image:getPixel(px, py)) > 0 then remaining = remaining + 1 end
        end
      end
    end
  end
  spr:saveAs(f(job.path))
  print(string.format("  saved. straysVerified=%d pixelsCleared=%d belowGroundRemaining=%d", verified, cleared, remaining))
end
