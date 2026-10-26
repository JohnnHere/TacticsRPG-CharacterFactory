-- Repackage three newly generated PixelLab cels in Aseprite. No pixel changes.
local root=assert(app.params.root)
local function file(p)return app.fs.joinPath(root,p)end
local original=app.open(file('characters/orc-pixellab-01/source/aseprite/concept-raw.aseprite'))
local selected={{id='orc-pixellab-01',frame=2},{id='orc-pixellab-02',frame=3},{id='orc-pixellab-03',frame=5}}
for _,c in ipairs(selected)do
 local im=Image(original.width,original.height,ColorMode.RGB);im:clear();im:drawSprite(original,c.frame)
 local s=Sprite(im.width,im.height,ColorMode.RGB);s.layers[1].name='PixelLab original - unretouched';s:newCel(s.layers[1],1,im,Point(0,0));s.frames[1].duration=.15
 local base='characters/'..c.id
 s:saveAs(file(base..'/source/aseprite/concept-selected.aseprite'));im:saveAs(file(base..'/concepts/concept-selected.png'));s:close()
end
original:close();print('Three new PixelLab concepts selected; exact original pixels preserved.')
