local app = app

local sprite = app.open("characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed-256.aseprite")
if not sprite then
    print("FAILED to open 256 master")
    return
end
print("Opened: " .. sprite.width .. "x" .. sprite.height .. " frames: " .. #sprite.frames)

-- Print current durations
for fi, frame in ipairs(sprite.frames) do
    print("  Frame " .. (fi-1) .. " duration: " .. frame.duration)
end

-- Set all durations to 160ms
for fi, frame in ipairs(sprite.frames) do
    frame.duration = 160
end

-- Verify
print("After setting:")
for fi, frame in ipairs(sprite.frames) do
    print("  Frame " .. (fi-1) .. " duration: " .. frame.duration)
end

sprite:saveAs("characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed-256.aseprite")
print("Saved with fixed durations.")
