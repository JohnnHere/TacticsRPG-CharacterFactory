local f=assert(io.open(app.params.plan,'r'));local p=json.decode(f:read('*a'));f:close()
local opened=app.open(p.reference);local reference=Image(opened.cels[1].image);opened:close()
local s=Sprite(128,128,ColorMode.RGB);s.layers[1].name='PixelLab Pro natural head + preserved original walking body'
for i,frame in ipairs(p.frames) do
 local source=app.open(frame.input);local im=Image(128,128,ColorMode.RGB);im:drawSprite(source,1);source:close()
 for y=5,28 do for x=53,81 do
  if y<=24 or (x>=60 and x<=79) then im:drawPixel(x+frame.dx,y+frame.dy,reference:getPixel(x,y)) end
 end end
 if i>1 then s:newEmptyFrame() end
 s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=frame.durationMs/1000
 im:saveAs(frame.output)
end
s:saveAs(p.master);s:close()
