-- Create a blank 128x128 master inside Aseprite for an independent text request.
local out=assert(app.params.output)
local sprite=Sprite(128,128,ColorMode.RGB)
sprite.layers[1].name='Blank PixelLab text-generation canvas'
sprite.frames[1].duration=.15
sprite:saveAs(out)
sprite:close()
print('Created blank 128x128 PixelLab canvas: '..out)
