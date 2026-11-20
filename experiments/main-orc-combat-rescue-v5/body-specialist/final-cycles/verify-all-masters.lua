-- verify-all-masters.lua
-- Inspects native128.aseprite and body256.aseprite for all 3 cycles

local cycles = {
  "back_r-Sword-full",
  "back_l-Sword-full",
  "back_l-Axe-full"
}

local roots = {
  "characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/",
  "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/"
}

local report = {}

for _, c in ipairs(cycles) do
  for _, root in ipairs(roots) do
    local prefix = root .. c .. "/"
    
    -- Verify native128
    local n = Sprite{fromFile = prefix .. "native128.aseprite"}
    assert(n ~= nil, "Failed to open native128: " .. prefix)
    assert(#n.frames == 12, "Wrong frame count in native128: " .. #n.frames)
    assert(n.width == 128 and n.height == 128, "Wrong native dimensions")
    assert(#n.layers == 1 and n.layers[1].name == "body", "Wrong layer in native128")
    
    local n_durations = {}
    for i = 1, #n.frames do
      table.insert(n_durations, math.floor(n.frames[i].duration * 1000 + 0.5))
      local cel = n.layers[1]:cel(i)
      assert(cel ~= nil, "Missing cel in native128 frame " .. i)
      assert(cel.position.x == 0 and cel.position.y == 0, "Wrong cel position in native128")
    end
    n:close()
    
    -- Verify body256
    local b = Sprite{fromFile = prefix .. "body256.aseprite"}
    assert(b ~= nil, "Failed to open body256: " .. prefix)
    assert(#b.frames == 12, "Wrong frame count in body256: " .. #b.frames)
    assert(b.width == 256 and b.height == 256, "Wrong body256 dimensions")
    assert(#b.layers == 1 and b.layers[1].name == "body", "Wrong layer in body256")
    
    local b_durations = {}
    for i = 1, #b.frames do
      table.insert(b_durations, math.floor(b.frames[i].duration * 1000 + 0.5))
      local cel = b.layers[1]:cel(i)
      assert(cel ~= nil, "Missing cel in body256 frame " .. i)
      assert(cel.position.x == 64 and cel.position.y == 64, "Wrong cel position in body256: " .. cel.position.x .. "," .. cel.position.y)
    end
    b:close()
    
    print(string.format("VERIFIED %s (%s): 12 frames, cel (64,64), durations: %s", c, root:sub(1,10), table.concat(n_durations, ",")))
  end
end

print("ALL MASTERS VERIFIED PERFECTLY!")
