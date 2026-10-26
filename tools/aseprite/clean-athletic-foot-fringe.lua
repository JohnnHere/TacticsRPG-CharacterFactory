-- Local Aseprite retouch: remove exterior matte fringe only, preserve body/poses.
local root=assert(app.params.root)
local function file(p)return app.fs.joinPath(root,p)end
local master='characters/orc-pixellab-11/source/aseprite/athletic-feet-v2/source/athletic-walk.aseprite'
local out='experiments/orc-athletic-feet-v2/cleaned'
app.fs.makeAllDirectories(file(out))
local sprite=app.open(file(master));sprite.layers[1].name='PixelLab Walk + Aseprite exterior boot matte cleanup'
local pc=app.pixelColor
local matte={['122,123,110']=true,['110,112,100']=true,['136,143,143']=true,['91,92,86']=true}
local report={tool='Aseprite Lua',script='tools/aseprite/clean-athletic-foot-fringe.lua',minimumY=98,frames={}}
for frame=1,#sprite.frames do
 local im=Image(128,128,ColorMode.RGB);im:clear();im:drawSprite(sprite,frame)
 local seen,queue,removed={}, {}, {}
 local function visit(x,y)
  if x<0 or x>=128 or y<0 or y>=128 then return end
  local key=y*128+x;if seen[key]then return end
  local c=im:getPixel(x,y);local alpha=pc.rgbaA(c)
  local candidate=y>=98 and alpha>0 and matte[pc.rgbaR(c)..','..pc.rgbaG(c)..','..pc.rgbaB(c)]
  if alpha==0 or candidate then
   seen[key]=true;queue[#queue+1]={x,y}
   if candidate then removed[#removed+1]={x=x,y=y,rgba={pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c),alpha}}end
  end
 end
 for x=0,127 do visit(x,0);visit(x,127)end
 for y=0,127 do visit(0,y);visit(127,y)end
 local n=1;while n<=#queue do local p=queue[n];n=n+1;visit(p[1]-1,p[2]);visit(p[1]+1,p[2]);visit(p[1],p[2]-1);visit(p[1],p[2]+1)end
 for _,p in ipairs(removed)do im:drawPixel(p.x,p.y,0)end
 sprite:newCel(sprite.layers[1],frame,im,Point(0,0))
 im:saveAs(file(out..string.format('/%02d.png',frame-1)))
 report.frames[#report.frames+1]={frame=frame-1,removed=removed,count=#removed,durationMs=math.floor(sprite.frames[frame].duration*1000+.5)}
end
sprite:saveAs(file(master));sprite:close()
local f=assert(io.open(file('experiments/orc-athletic-feet-v2/retouch.json'),'w'));f:write(json.encode(report));f:close()
print('Exterior boot matte removed in Aseprite; original poses/timing and pixels above y98 preserved.')
