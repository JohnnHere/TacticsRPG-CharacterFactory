local app = app
local sprite = app.open("characters/orc-v1/source/aseprite/rear-recovery-v2/native/walk-back_l.aseprite")
if not sprite then
    print("FAILED to open walk-back_l.aseprite")
    return
end
print("=== walk-back_l.aseprite ===")
print("frames:", sprite.frames.count)
print("width:", sprite.width, "height:", sprite.height)
print("layers:", sprite.layers.count)
for i, layer in ipairs(sprite.layers) do
    print(string.format("  layer[%d] name=%s visible=%s opacity=%d celCount=%d",
        i-1, layer.name, tostring(layer.isVisible), layer.opacity, #layer.cels))
    for ci, cel in ipairs(layer.cels) do
        print(string.format("    cel[%d] frameIndex=%d position=(%d,%d) bounds=(%d,%d,%d,%d)",
            ci-1, cel.frame.frameNumber-1, cel.position.x, cel.position.y,
            cel.bounds.x, cel.bounds.y, cel.bounds.width, cel.bounds.height))
    end
end
app.close(sprite)
