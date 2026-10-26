-- Registered head-piece cleanup only; no body scaling or torso deformation.
local f=assert(io.open(app.params.plan,'r'));local plan=json.decode(f:read('*a'));f:close()
for _,job in ipairs(plan.jobs) do
 local reference=app.open(job.reference);local ref=Image(reference.cels[1].image);reference:close()
 local s=Sprite(128,128,ColorMode.RGB);s.layers[1].name=job.label
 for i,frame in ipairs(job.frames) do
  local opened=app.open(frame.input);local im=Image(128,128,ColorMode.RGB);im:drawSprite(opened,1);opened:close()
  for y=job.rect.y,job.rect.y+job.rect.h-1 do for x=job.rect.x,job.rect.x+job.rect.w-1 do
   im:drawPixel(x+frame.dx,y+frame.dy,ref:getPixel(x,y))
  end end
  if i>1 then s:newEmptyFrame() end
  s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=frame.durationMs/1000
  im:saveAs(frame.output)
 end
 s:saveAs(job.master);s:close()
end
