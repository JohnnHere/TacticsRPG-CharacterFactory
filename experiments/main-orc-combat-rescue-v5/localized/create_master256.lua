local app = app

-- Open fixed native 128 master
local native = app.open("characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed.aseprite")
if not native then
    print("FAILED to open walk-back_l-fixed.aseprite")
    return
end
print("Native master: " .. native.width .. "x" .. native.height .. " frames: " .. #native.frames .. " layers: " .. #native.layers)

-- Create new 256x256 composite master sprite
local sprite = Sprite(256, 256)
-- Ensure exactly 8 frames
while #sprite.frames < 8 do
    sprite:newFrame()
end
while #sprite.frames > 8 do
    sprite.frames[#sprite.frames]:delete()
end

local layer = sprite.layers[1]
print("Created 256 composite master with " .. #sprite.frames .. " frames")

for fi = 1, 8 do
    local nframe = native.frames[fi]
    local ncel = native.layers[1]:cel(nframe)
    local cframe = sprite.frames[fi]
    
    -- Build 256x256 image with native art at bodyOffset (64,64)
    local img = Image(256, 256)
    img:clear()
    if ncel and ncel.image then
        img:drawImage(ncel.image, 64, 64)
    end
    
    -- Replace existing cel on this frame/layer (newCel replaces at same frame)
    local existing = layer:cel(cframe)
    if existing then
        existing.image = img
    else
        layer:newCel(cframe, img, 0, 0)
    end
    
    -- Set frame duration 160ms
    cframe.duration = 160
end

local out = "characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed-256.aseprite"
sprite:saveAs(out)
print("Saved 256 master: " .. out)
print("256 master: " .. sprite.width .. "x" .. sprite.height .. " frames: " .. #sprite.frames)
