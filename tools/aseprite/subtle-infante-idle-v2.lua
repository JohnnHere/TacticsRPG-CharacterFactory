-- Aseprite timeline finishing only: reuse complete original poses, no raster deformation.
local root=assert(app.params.root)
local function file(p)return app.fs.joinPath(root,p)end
local original=app.open(file('characters/orc-pixellab-05/source/aseprite/infante-idle-subtle-v2/source/infante-idle.aseprite'))
local selected={1,2,7,8};local durations={650,750,750,650}
local out='experiments/orc-infante-idle-subtle-v2/after';app.fs.makeAllDirectories(file(out))
local sprite=Sprite(original.width,original.height,ColorMode.RGB)
sprite.layers[1].name='Original PixelLab complete poses - reduced breathing excursion'
for i,source in ipairs(selected)do
 local im=Image(original.width,original.height,ColorMode.RGB);im:clear();im:drawSprite(original,source)
 if i>1 then sprite:newEmptyFrame()end
 sprite:newCel(sprite.layers[1],i,im,Point(0,0));sprite.frames[i].duration=durations[i]/1000
 im:saveAs(file(out..string.format('/%02d.png',i-1)))
end
sprite:newTag(1,4).name='Idle'
sprite:saveAs(file('characters/orc-pixellab-05/source/aseprite/infante-idle-subtle-v2/source/infante-idle-subtle.aseprite'))
sprite:close();original:close()
print('Whole-pose Idle: source frames 0,1,6,7; no pixel edits; 2800 ms cycle.')
