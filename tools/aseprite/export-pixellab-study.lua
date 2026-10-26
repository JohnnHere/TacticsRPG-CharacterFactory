-- Saved-study export only. No old artwork, drawing, rescaling or conditioning.
local root=assert(app.params.root);local id=assert(app.params.id)
local base='characters/'..id
local function file(p)return app.fs.joinPath(root,p)end
local source=base..'/source/aseprite/concept-raw.aseprite'
local s=app.open(file(source));local frames={}
app.fs.makeAllDirectories(file(base..'/concepts'))
for n=1,#s.frames do
 local im=Image(s.width,s.height,ColorMode.RGB);im:clear();im:drawSprite(s,n)
 local count=0;for y=0,s.height-1 do for x=0,s.width-1 do if app.pixelColor.rgbaA(im:getPixel(x,y))>0 then count=count+1 end end end
 if count>0 then local name=base..'/concepts/candidate-'..string.format('%02d',n-1)..'.png';im:saveAs(file(name));frames[#frames+1]={frame=n-1,png=name,opaquePixels=count}end
end
local f=assert(io.open(file(base..'/source/concept-frames.json'),'w'));f:write(json.encode({source=source,width=s.width,height=s.height,frames=frames}));f:close();s:close();print('Exported '..#frames..' nonempty raw candidates; master unchanged.')
