local sprite = app.open("characters/orc-v1/source/aseprite/rear-recovery-v2/native/walk-back_l.aseprite")
if not sprite then
    print("FAILED to open walk-back_l.aseprite")
    return
end
local outdir = "tmp/opencode_export"
os.execute("mkdir " .. outdir)
for fi, frame in ipairs(sprite.frames) do
    local index = fi - 1
    local path = outdir .. "/native_backl_f" .. string.format("%02d", index) .. ".png"
    local cel = sprite.layers[1]:cel(frame)
    if cel and cel.image then
        local img = Image(cel.image)
        -- crop to cel bounds then save full canvas with cel composited
        app.sprite = sprite
        app.frame = frame
        app.refresh()
        -- Use the sprite image at this frame (flatten visible layers)
        local sheet = Image(sprite.width, sprite.height)
        sheet:clear()
        for _, layer in ipairs(sprite.layers) do
            if layer.isVisible then
                local c = layer:cel(frame)
                if c and c.image then
                    sheet:drawImage(c.image, c.position.x, c.position.y)
                end
            end
        end
        sheet:saveAs(path)
        print("Saved " .. path)
    end
end
-- done
