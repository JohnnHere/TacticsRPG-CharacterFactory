-- Official PixelLab whole-body reference imported unchanged, not manual drawing.
local root=assert(app.params.root)
local sprite=app.open(app.fs.joinPath(root,'experiments/pixellab-orc-refinement-v8/frontal-reference.png'))
sprite.layers[1].name='PixelLab Pro Flash own frontal reference - unretouched'
sprite:saveAs(app.fs.joinPath(root,'characters/orc-pixellab-07/source/aseprite/walk-frontal-reference-v8.aseprite'))
sprite:close()
