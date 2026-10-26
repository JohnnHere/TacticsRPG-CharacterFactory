local root=app.params.root
local base=app.open(app.fs.joinPath(root,'experiments/pixellab-orc-refinement-v4/before/orc-pixellab-07/source/studies/Walk/00.png'))
local original=Image(base.cels[1].image);base:close()
for _,p in ipairs({{index=0,ox=0,oy=-4},{index=1,ox=2,oy=-5}}) do
 local r=app.open(app.fs.joinPath(root,'experiments/pixellab-orc-refinement-v5/07-NaturalHead/raw/'..p.index..'.png'));local ref=Image(r.cels[1].image);r:close()
 local im=Image(original)
 for y=5,28 do for x=53,81 do
  if y<=24 or (x>=60 and x<=79) then im:drawPixel(x,y,ref:getPixel(x-p.ox,y-p.oy)) end
 end end
 local s=Sprite(128,128,ColorMode.RGB);s:newCel(s.layers[1],1,im,Point(0,0));s:saveAs(app.fs.joinPath(root,'experiments/pixellab-orc-refinement-v5/preview-'..p.index..'.aseprite'));im:saveAs(app.fs.joinPath(root,'experiments/pixellab-orc-refinement-v5/preview-'..p.index..'.png'));s:close()
end
