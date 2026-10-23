-- Verify the original pixels inside SAVED masters; never saves these documents.
local root=assert(app.params.root)
local function file(p)return app.fs.joinPath(root,p)end
local f=assert(io.open(file('reports/orc-production-v4-plan.json'),'r'));local plan=json.decode(f:read('*a'));f:close()
local count=0
for _,job in ipairs(plan.jobs)do
 local s=app.open(file(job.source));local reference=nil
 for _,l in ipairs(s.layers)do l.isVisible=false;if l.name=='Previous approved baseline - hidden'then reference=l end end
 assert(reference,'Missing saved reference layer: '..job.id);reference.isVisible=true
 for n=1,#s.frames do
  local image=Image(s.width,s.height,ColorMode.RGB);image:clear();image:drawSprite(s,n)
  local expected=Image{fromFile=file('reports/orc-production-v4-before/'..job.before[n])}
  for y=0,s.height-1 do for x=0,s.width-1 do assert(image:getPixel(x,y)==expected:getPixel(x,y),'Saved reference differs: '..job.id..' frame '..n)end end
  count=count+1
 end
 s:close()
end
print('PASS: '..count..' original cels exact inside saved V4 masters; no document saved')
