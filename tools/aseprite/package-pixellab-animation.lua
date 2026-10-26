-- Package unchanged official PixelLab archive frames inside Aseprite.
local root=assert(app.params.root);local f=assert(io.open(app.params.plan,'r'));local p=json.decode(f:read('*a'));f:close()
local duration=(p.durationMs or 100)/1000
local skipFirst=p.firstImageIsReference~=false
local function file(v)return app.fs.joinPath(root,v)end
local raw=Sprite(128,128,ColorMode.RGB);raw.layers[1].name=skipFirst and 'PixelLab raw archive - input plus generated frames' or 'PixelLab raw skeleton frames - no echoed input'
local clip=Sprite(128,128,ColorMode.RGB);clip.layers[1].name='PixelLab generated motion - unretouched'
app.fs.makeAllDirectories(file(p.output))
for i,src in ipairs(p.images)do
 local opened=app.open(file(src));local im=Image(128,128,ColorMode.RGB);im:clear();im:drawSprite(opened,1);opened:close()
 if i>1 then raw:newEmptyFrame()end
 raw:newCel(raw.layers[1],i,im,Point(0,0));raw.frames[i].duration=duration
 if not skipFirst or i>1 then
  local ci=skipFirst and i-1 or i
  if ci>1 then clip:newEmptyFrame()end
  clip:newCel(clip.layers[1],ci,im,Point(0,0));clip.frames[ci].duration=duration
  im:saveAs(file(p.output..string.format('/%02d.png',ci-1)))
 end
end
raw:saveAs(file(p.rawMaster));clip:saveAs(file(p.master));raw:close();clip:close()
print('Saved '..(#p.images-(skipFirst and 1 or 0))..' unretouched PixelLab motion frames, '..(duration*1000)..' ms review timing.')
