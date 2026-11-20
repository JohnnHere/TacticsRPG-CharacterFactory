-- targeted-repair-v1 / representative back_r Sword
-- Programmatic Aseprite authorship by the agent (not manual drawing).
-- Scope: ONLY the handFront layer of the forked composite master.
-- Rule: the fist must occlude the handle it grips. The published handFront was a
-- body-intersect-plus-or-minus-5px box, so 14-21 handle pixels per equipped frame were
-- painted ON TOP of the fist. This script grows the existing handFront patch by BFS,
-- expanding only into body pixels that a weapon layer actually covers, and only within
-- a 7px Chebyshev radius of the declared grip. Source pixels are the body's own; no
-- recolouring, no palette change, no new colours, no other layer touched.
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

local MASTER = "experiments/main-orc-targeted-repair-v1/artist-rear/candidate/aseprite/sword-attack-representative-v1.aseprite"
local MAXDIST = 7
-- declared per-frame grip anchors for back_r/Sword (clip ids 1..6 -> Lua frames 2..7)
local grips = {
  [2] = {175, 106},
  [3] = {166, 76},
  [4] = {164, 84},
  [5] = {183, 92},
  [6] = {181, 121},
  [7] = {170, 127},
}

local spr = app.open(file(MASTER))
assert(spr, "master not opened")
local W, H = spr.width, spr.height

local function layerByName(name)
  for _, l in ipairs(spr.layers) do if l.name == name then return l end end
  error("missing layer " .. name)
end
local bodyL = layerByName("body")
local wbL = layerByName("weaponBack")
local wfL = layerByName("weaponFront")
local hfL = layerByName("handFront")

local function celImage(layer, frameIndex)
  local cel = layer:cel(spr.frames[frameIndex])
  if cel == nil then return nil, 0, 0 end
  return cel.image, cel.position.x, cel.position.y
end

local totalAdded, totalFrames = 0, 0
for i = 1, #spr.frames do
  local hfImg, hfx, hfy = celImage(hfL, i)
  local bodyImg, bx, by = celImage(bodyL, i)
  local wbImg, wbx, wby = celImage(wbL, i)
  local wfImg, wfx, wfy = celImage(wfL, i)
  local grip = grips[i]
  if hfImg == nil or bodyImg == nil or wbImg == nil or wfImg == nil then
    print(string.format("frame %d: skipped (missing cel)", i))
  elseif grip == nil then
    print(string.format("frame %d: unarmed, handFront untouched (%d px)", i, hfImg.width * 0))
  else
    assert(hfx == 0 and hfy == 0, "handFront cel must be at origin")
    assert(bx == 0 and by == 0, "body cel must be at origin")
    local gx, gy = grip[1], grip[2]

    local function bodyAt(x, y)
      local img = bodyImg
      local px, py = x - bx, y - by
      if px < 0 or py < 0 or px >= img.width or py >= img.height then return false end
      return app.pixelColor.rgbaA(img:getPixel(px, py)) > 0
    end
    local function weaponAt(x, y)
      local function at(img, ox, oy)
        local px, py = x - ox, y - oy
        if px < 0 or py < 0 or px >= img.width or py >= img.height then return false end
        return app.pixelColor.rgbaA(img:getPixel(px, py)) > 0
      end
      return at(wbImg, wbx, wby) or at(wfImg, wfx, wfy)
    end

    -- expansion set: body pixels covered by a weapon layer, inside the grip radius
    local expand = {}
    for y = gy - MAXDIST, gy + MAXDIST do
      for x = gx - MAXDIST, gx + MAXDIST do
        if x >= 0 and y >= 0 and x < W and y < H and bodyAt(x, y) and weaponAt(x, y) then
          expand[y * W + x] = true
        end
      end
    end

    local keep, queue = {}, {}
    for y = 0, H - 1 do
      for x = 0, W - 1 do
        local px, py = x - hfx, y - hfy
        if px >= 0 and py >= 0 and px < hfImg.width and py < hfImg.height
          and app.pixelColor.rgbaA(hfImg:getPixel(px, py)) > 0 then
          keep[y * W + x] = true
          queue[#queue + 1] = y * W + x
        end
      end
    end
    local seeds = #queue

    local added = 0
    local head = 1
    while head <= #queue do
      local idx = queue[head]
      head = head + 1
      local x = idx % W
      local y = (idx - x) / W
      for dy = -1, 1 do
        for dx = -1, 1 do
          if not (dx == 0 and dy == 0) then
            local nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and nx < W and ny < H then
              local ni = ny * W + nx
              if expand[ni] and not keep[ni] then
                keep[ni] = true
                queue[#queue + 1] = ni
                added = added + 1
              end
            end
          end
        end
      end
    end

    for _, idx in ipairs(queue) do
      local x = idx % W
      local y = (idx - x) / W
      local px, py = x - hfx, y - hfy
      if px >= 0 and py >= 0 and px < hfImg.width and py < hfImg.height then
        if app.pixelColor.rgbaA(hfImg:getPixel(px, py)) == 0 then
          hfImg:drawPixel(px, py, bodyImg:getPixel(x - bx, y - by))
        end
      end
    end
    totalAdded = totalAdded + added
    totalFrames = totalFrames + 1
    print(string.format("frame %d: grip=%d,%d seeds=%d added=%d totalPatch=%d", i, gx, gy, seeds, added, #queue))
  end
end

spr:saveAs(file(MASTER))
print(string.format("saved %s | equipped frames touched=%d | pixels restored from body=%d", MASTER, totalFrames, totalAdded))
