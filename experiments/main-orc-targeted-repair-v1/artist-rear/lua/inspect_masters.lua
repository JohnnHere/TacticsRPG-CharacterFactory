-- Inspect the back_r/Sword masters used by the targeted-repair-v1 candidate.
-- Read-only: prints canvas, frame count, frame durations and layer tree.
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end
local targets = {
  "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-attack-representative-v2.aseprite",
  "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-body-representative-v2.aseprite",
  "characters/orc-v1/source/aseprite/rear-recovery-v2/native/sword-body-representative-v2-back_r.aseprite",
}
for _, t in ipairs(targets) do
  local ok, spr = pcall(function() return app.open(file(t)) end)
  if not ok or not spr then
    print("MISSING " .. t)
  else
    print(string.format("MASTER %s  %dx%d frames=%d", t, spr.width, spr.height, #spr.frames))
    for i, fr in ipairs(spr.frames) do
      local cels = 0
      for _, cel in ipairs(fr.cels) do cels = cels + 1 end
      print(string.format("  frame %d  duration=%.1fms cels=%d", i, fr.duration, cels))
    end
    local function walk(layer, depth)
      print(string.format("  %sLAYER %q visible=%s pixels=%s blend=%d opacity=%d",
        string.rep("  ", depth), layer.name, tostring(layer.isVisible),
        tostring(layer.isPixel), layer.blendMode, layer.opacity))
      for _, child in ipairs(layer.layers or {}) do walk(child, depth + 1) end
    end
    for _, layer in ipairs(spr.layers) do walk(layer, 1) end
    spr:close()
  end
end
