-- Synthetic integration-test data; this is not project artwork.
local out = assert(app.params.output)
local s = Sprite(16,16,ColorMode.RGB)
s.layers[1].name="Body"
local body=s.layers[1]
local front=s:newLayer();front.name="Foreground"
s:newEmptyFrame();s:newEmptyFrame()
for i,ms in ipairs({80,120,160}) do s.frames[i].duration=ms/1000 end
for i=1,2 do
  local im=Image(16,16,ColorMode.RGB);im:drawPixel(2,12,app.pixelColor.rgba(220,50,30,255));s:newCel(body,i,im)
end
local im=Image(16,16,ColorMode.RGB);im:drawPixel(2,12,app.pixelColor.rgba(30,50,220,255));s:newCel(front,1,im)
local tag=s:newTag(1,2);tag.name="first-two"
local slice=s:newSlice(Rectangle(1,2,3,4));slice.name="socket"
s:saveAs(out.."/animation.aseprite")
s:close()
local t=Sprite(24,24,ColorMode.RGB)
t.gridBounds=Rectangle(0,0,8,8)
app.command.NewLayer{ name="Terrain", tilemap=true }
local layer=app.layer
assert(layer.isTilemap,"Tilemap fixture was not created")
app.useTool{tool="pencil",color=Color(255,30,20),points={Point(1,1),Point(9,1)},layer=layer}
local cel=layer:cel(1)
local image=cel.image:clone()
image:drawPixel(1,0,image:getPixel(1,0) | 0x80000000)
cel.image=image
cel.position=Point(8,8)
layer.tileset.name="fixture-tiles"
-- Same name, different identity: the bridge must not key libraries by name.
t:newTileset(Rectangle(0,0,8,8),2).name="fixture-tiles"
t:saveAs(out.."/tilemap.aseprite")
