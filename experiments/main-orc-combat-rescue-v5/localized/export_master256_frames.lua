local app = app

local sprite = app.open("characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed-256.aseprite")
if not sprite then
    print("FAILED to open 256 master")
    return
end
print("Opened 256 master: " .. sprite.width .. "x" .. sprite.height .. " frames: " .. #sprite.frames)

local outdir = "experiments/main-orc-combat-rescue-v5/localized/master256_export"
os.execute("mkdir \"" .. outdir .. "\"")

local layer = sprite.layers[1]
for fi, frame in ipairs(sprite.frames) do
    local index = fi - 1
    local cel = layer:cel(frame)
    if cel and cel.image then
        local img = Image(sprite.width, sprite.height)
        img:clear()
        img:drawImage(cel.image, cel.position.x, cel.position.y)
        local path = outdir .. "/m" .. string.format("%02d", index) .. ".png"
        img:saveAs(path)
        print("Exported " .. path .. " duration=" .. frame.duration)
    else
        print("No cel on frame " .. index)
    end
end

print("Done exporting 256 master frames.")
