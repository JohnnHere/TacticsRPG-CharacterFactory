-- All artistic transformations execute inside Aseprite. No scaling/mirroring.
local root=assert(app.params.root)
local function file(p)return app.fs.joinPath(root,p)end
local f=assert(io.open(file(app.params.plan),'r'));local plan=json.decode(f:read('*a'));f:close()
local function render(s,n)local i=Image(s.width,s.height,ColorMode.RGB);i:clear();i:drawSprite(s,n);return i end
local function rgb(p)return string.format('%02x%02x%02x',app.pixelColor.rgbaR(p),app.pixelColor.rgbaG(p),app.pixelColor.rgbaB(p))end
local function color(h)return app.pixelColor.rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255)end
local darks={['010000']=true,['010001']=true,['020101']=true,['030201']=true,['050302']=true,['040402']=true,['040201']=true,['040302']=true,['030302']=true}
local reports={}
for _,job in ipairs(plan.jobs)do
 local original=app.open(file(job.original));local refs={}
 for n=1,#original.frames do refs[n]=render(original,n)end
 local s=original
 if job.directV4 then s=app.open(file(job.directV4))end
 local sourceImages={};for n=1,#s.frames do sourceImages[n]=render(s,n)end
 local neutral=nil
 if job.returnSource then local a=app.open(file(job.returnSource));neutral=render(a,1);a:close()end
 -- Existing original layers remain archived and hidden in the saved master.
 for _,l in ipairs(s.layers)do l.isVisible=false end
 local reference=s:newLayer();reference.name='Previous approved baseline - hidden';reference.isVisible=false
 local work=s:newLayer();work.name='V4 working poses - own outfit and view'
 local detail=s:newLayer();detail.name='V4 near-black cluster cleanup'
 local rec={id=job.id,frames={}}
 local strip=Image(s.width*#s.frames,s.height,ColorMode.RGB);strip:clear()
 app.fs.makeAllDirectories(file(job.directory..'/frames'))
 app.fs.makeAllDirectories(file(job.directory..'/reference'))
 for n=1,#s.frames do
  s:newCel(reference,n,refs[n],Point(0,0))
  refs[n]:saveAs(file(job.directory..string.format('/reference/%02d.png',n-1)))
  local isReturn=neutral and n==#s.frames
  local base=Image(isReturn and neutral or sourceImages[n]);local overlay=Image(s.width,s.height,ColorMode.RGB);overlay:clear()
  local cleaned=0
  if not job.directV4 then
   for y=0,s.height-1 do for x=0,s.width-1 do local p=base:getPixel(x,y)
    if app.pixelColor.rgbaA(p)==255 and darks[rgb(p)] and rgb(p)~=job.ink then overlay:drawPixel(x,y,color(job.ink));cleaned=cleaned+1 end
   end end
  end
  s:newCel(work,n,base,Point(0,0));s:newCel(detail,n,overlay,Point(0,0))
  s.frames[n].duration=job.durationsMs[n]/1000
  local output=render(s,n);output:saveAs(file(job.directory..string.format('/frames/%02d.png',n-1)));strip:drawImage(output,Point((n-1)*s.width,0))
  local changed,alpha=0,0
  for y=0,s.height-1 do for x=0,s.width-1 do local a,b=refs[n]:getPixel(x,y),output:getPixel(x,y)
   if a~=b then changed=changed+1 end
   if app.pixelColor.rgbaA(a)~=app.pixelColor.rgbaA(b)then alpha=alpha+1 end
  end end
  table.insert(rec.frames,{changedPixels=changed,changedAlphaPixels=alpha,nearBlackCleanup=cleaned,canonicalReturn=isReturn and true or false,directApprovedV4=job.directV4 and true or false})
 end
 s:saveAs(file(job.source));strip:saveAs(file(job.directory..'/native-strip.png'))
 s:close();if job.directV4 then original:close()end
 table.insert(reports,rec)
 print(job.id)
end
local o=assert(io.open(file(plan.result),'w'));o:write(json.encode(reports));o:close()
