local app = app

local sprite = app.open("characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed-256.aseprite")
if not sprite then
    print("FAILED to open 256 master")
    return
end
print("Opened: " .. sprite.width .. "x" .. sprite.height .. " frames: " .. #sprite.frames)

-- Set all durations to 160ms = 0.160 seconds
for fi, frame in ipairs(sprite.frames) do
    frame.duration = 0.160
end

-- Verify
print("After setting to 0.160s (160ms):")
for fi, frame in ipairs(sprite.frames) do
    print("  Frame " .. (fi-1) .. " duration: " .. frame.duration .. " s")
end

sprite:saveAs("characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed-256.aseprite")
print("Saved with correct durations.")
