-- Aseprite timeline variant: whole original poses; no deformation or repainting.
local root=assert(app.params.root)
local function file(p)return app.fs.joinPath(root,p)end
local base='characters/orc-pixellab-05/source/aseprite/infante-idle-balanced-v3'
local original=app.open(file(base..'/source/infante-idle.aseprite'))
local frames={1,2,6,7,8};local durations={400,450,500,450,400}
local out='characters/orc-pixellab-05/source/studies/IdleCandidates/balanced-v3'
app.fs.makeAllDirectories(file(out))
local sprite=Sprite(original.width,original.height,ColorMode.RGB)
sprite.layers[1].name='PixelLab complete poses - balanced Aseprite breathing timeline'
for i,f in ipairs(frames)do
 local im=Image(original.width,original.height,ColorMode.RGB);im:clear();im:drawSprite(original,f)
 if i>1 then sprite:newEmptyFrame()end
 sprite:newCel(sprite.layers[1],i,im,Point(0,0));sprite.frames[i].duration=durations[i]/1000
 im:saveAs(file(out..string.format('/%02d.png',i-1)))
end
sprite:newTag(1,5).name='Idle'
sprite:saveAs(file(base..'/source/infante-idle-balanced.aseprite'))
sprite:close();original:close()
