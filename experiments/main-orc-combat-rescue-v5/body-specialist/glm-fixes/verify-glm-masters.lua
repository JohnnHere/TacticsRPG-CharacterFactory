-- verify-glm-masters.lua
-- Reabre os mestres glm-fixes (2 ciclos x 2 raízes) e confere frames/durações/camada/cel.
local expected = {
  ["back_r-Sword-full"] = {40,60,60,70,70,40,40,90,70,70,60,60},
  ["back_l-Axe-full"]   = {70,80,90,100,110,50,60,110,100,100,100,130},
}
local roots = {
  "characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/",
  "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes/",
}
for name, times in pairs(expected) do
  for _, root in ipairs(roots) do
    local prefix = root .. name .. "/"
    local n = Sprite{fromFile = prefix .. "native128.aseprite"}
    assert(n and #n.frames == 12 and n.width == 128 and n.height == 128, "bad native128 " .. prefix)
    assert(#n.layers == 1 and n.layers[1].name == "body", "bad layer " .. prefix)
    local ds = {}
    for i = 1, 12 do
      local ms = math.floor(n.frames[i].duration * 1000 + 0.5)
      assert(ms == times[i], "duration mismatch " .. name .. " frame " .. i .. ": " .. ms)
      local cel = n.layers[1]:cel(i)
      assert(cel and cel.position.x == 0 and cel.position.y == 0, "cel pos native " .. i)
      ds[#ds+1] = ms
    end
    n:close()
    local b = Sprite{fromFile = prefix .. "body256.aseprite"}
    assert(b and #b.frames == 12 and b.width == 256 and b.height == 256, "bad body256 " .. prefix)
    assert(#b.layers == 1 and b.layers[1].name == "body", "bad layer256 " .. prefix)
    for i = 1, 12 do
      local ms = math.floor(b.frames[i].duration * 1000 + 0.5)
      assert(ms == times[i], "duration256 mismatch " .. name .. " frame " .. i)
      local cel = b.layers[1]:cel(i)
      assert(cel and cel.position.x == 64 and cel.position.y == 64, "cel pos 256 " .. i)
    end
    b:close()
    print("VERIFIED " .. name .. " @ " .. root:sub(1, 12) .. " durations: " .. table.concat(ds, ","))
  end
end
print("ALL GLM MASTERS VERIFIED")
