local root=assert(app.params.root);local function file(p)return app.fs.joinPath(root,p)end
local function read(p)local f=assert(io.open(file(p),'r'));local d=json.decode(f:read('*a'));f:close();return d end
local green=read('experiments/infante-green-skin-v1/retouch.json');local sampled=read('experiments/infante-green-skin-v3/palette.json');local v3={};for _,p in ipairs(sampled.ramp)do v3[table.concat(p.fromGreenV1,',')]=p.to end
local palette={};for _,p in ipairs(green.palette)do local c=v3[table.concat(p[2],',')];palette[string.format('%d,%d,%d',p[1][1],p[1][2],p[1][3])]=app.pixelColor.rgba(c[1],c[2],c[3],255)end
local rows={[6]={64,70},[7]={62,71},[8]={61,72},[9]={61,73},[10]={61,73},[11]={61,74},[12]={61,77},[13]={60,77},[14]={60,77},[15]={60,77},[16]={59,77},[17]={59,77},[18]={60,77},[19]={60,77},[20]={62,77},[21]={62,77},[22]={63,77},[23]={63,77},[24]={64,77},[25]={65,76},[26]={66,75}}
local offsets={{0,-1},{0,-1},{-1,0},{-1,1},{-1,0},{-1,-1},{-1,-1},{0,0},{0,1},{0,1},{0,0},{0,-1},{0,-1},{-1,0},{-1,1},{-1,0}}
local src=app.open(file('characters/orc-pixellab-05/source/aseprite/walk-study.aseprite'));local s=Sprite(128,128,ColorMode.RGB);s.layers[1].name='Inherited Infante Walk + selected Warcraft green skin'
local out='characters/orc-v1/source/studies/Walk';app.fs.makeAllDirectories(file(out))
for i=1,#src.frames do
 local im=Image(128,128,ColorMode.RGB);im:clear();im:drawSprite(src,i);local dx,dy=offsets[i][1],offsets[i][2]
 for y,span in pairs(rows)do for x=span[1],span[2]do
  local tooth=(y==23 or y==24)and((x>=68 and x<=72)or x==77)
  if not tooth then local c=im:getPixel(x+dx,y+dy);local target=palette[app.pixelColor.rgbaR(c)..','..app.pixelColor.rgbaG(c)..','..app.pixelColor.rgbaB(c)];if target and app.pixelColor.rgbaA(c)>0 then im:drawPixel(x+dx,y+dy,target)end end
 end end
 if i>1 then s:newEmptyFrame()end
 s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=src.frames[i].duration;im:saveAs(file(out..string.format('/%02d.png',i-1)))
end
s:saveAs(file('characters/orc-v1/source/aseprite/walk-study.aseprite'));s:close();src:close()
