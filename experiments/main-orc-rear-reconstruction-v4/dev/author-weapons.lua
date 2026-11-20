-- Programmatic hand-authored material clusters inside Aseprite. Source alpha,
-- silhouette, canvas, grip and category preserved. No luminance filtering.
local C='characters/orc-v1/source/rear-reconstruction-v4/weapons'
local function file(p)return app.fs.joinPath(app.fs.currentPath,p)end
local function blank(w,h)local i=Image(w,h,ColorMode.RGB);i:clear();return i end
local function color(r,g,b)return app.pixelColor.rgba(r,g,b,255)end
local ink=color(16,20,23)
local ironDark=color(37,43,47);local iron=color(61,69,74)
local ironLight=color(87,98,104);local steel=color(127,140,145);local edge=color(174,186,186)
local woodDark=color(49,32,25);local wood=color(83,54,34);local woodLight=color(116,80,45)
local leatherDark=color(29,25,25);local leather=color(57,42,32);local leatherLight=color(86,64,43)
local function poly(x,y,p)local yes=false;local j=#p;for i=1,#p do local a,b=p[i],p[j];if(a[2]>y)~=(b[2]>y)and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1]then yes=not yes end;j=i end;return yes end
local function editWeapon(category,id)
 local src='assets/weapons/'..id..'/source/rescue-v3/'..id..'.aseprite'
 local s=app.open(file(src));assert(s.width==96 and s.height==96 and #s.frames==1)
 local original=blank(96,96);original:drawSprite(s,1)
 local planes,bevel,haft,bindings=blank(96,96),blank(96,96),blank(96,96),blank(96,96)
 local function put(im,x,y,c)if app.pixelColor.rgbaA(original:getPixel(x,y))>0 then im:drawPixel(x,y,c)end end
 local function run(im,y,x1,x2,c)for x=x1,x2 do put(im,x,y,c)end end
 if category=='Axe'then
  -- The head's broad forged face is organized into three intentional planes.
  for y=17,34 do for x=48,64 do
   if poly(x+.5,y+.5,{{49,18},{57,17},{62,18},{63,24},{59,29},{52,34},{49,35},{51,29},{53,24},{50,22}})then
    put(planes,x,y,iron)
   end
   if poly(x+.5,y+.5,{{51,18},{58,18},{60,20},{58,23},{53,26},{51,23}})then put(planes,x,y,ironLight)end
   if poly(x+.5,y+.5,{{53,25},{59,23},{60,26},{57,29},{51,34},{50,33}})then put(planes,x,y,ironDark)end
  end end
  -- Strong socket and a restrained top ridge; the hollow eye remains hollow.
  for _,r in ipairs({{17,42,46},{17,48,58},{18,41,41},{19,41,41},{20,41,41},{21,42,43},{22,44,46}})do run(planes,r[1],r[2],r[3],steel)end
  for _,r in ipairs({{18,44,46},{22,42,43},{23,43,47},{24,44,47}})do run(planes,r[1],r[2],r[3],ironDark)end
  -- Curved cutting bevel: dark outer silhouette, lighter inset cutting plane.
  local rows={{16,62,62},{17,62,63},{18,63,63},{19,63,64},{20,63,64},{21,63,64},{22,63,64},{23,62,64},{24,62,63},{25,61,63},{26,60,62},{27,59,61},{28,58,60},{29,57,59},{30,56,58},{31,55,57},{32,54,56},{33,53,55},{34,51,53},{35,50,51}}
  for _,r in ipairs(rows)do
   run(bevel,r[1],r[2],r[3],steel)
   if r[1]>=19 and r[1]<=26 then put(bevel,r[3],r[1],edge)end
  end
  -- Short reflected streaks, not repeated white noise across the face.
  run(planes,19,54,57,steel);run(planes,20,55,57,ironLight)
  put(planes,51,21,ironDark);put(planes,52,21,ironDark)
  -- Exposed ash haft: same bent silhouette and exact original grip.
  for y=27,40 do for x=37,47 do
   if poly(x+.5,y+.5,{{41,27},{45,28},{46,31},{44,36},{42,40},{38,40},{39,35},{40,31}})then put(haft,x,y,wood)end
  end end
  for _,r in ipairs({{28,41,41},{29,41,41},{30,41,42},{31,41,42},{32,41,41},{33,40,41},{34,40,40},{35,39,40},{36,39,39},{37,38,39},{38,38,38}})do run(haft,r[1],r[2],r[3],woodLight)end
  for _,r in ipairs({{29,44,44},{30,44,44},{31,44,44},{32,43,44},{33,43,43},{34,42,43},{35,42,42},{36,41,42},{37,40,41},{38,40,40}})do run(haft,r[1],r[2],r[3],woodDark)end
  -- Existing leather grip: organize bands with a lit upper-left edge.
  for y=42,56 do for x=31,40 do
   if poly(x+.5,y+.5,{{37,42},{40,43},{38,49},{37,54},{39,56},{33,56},{31,53},{32,48},{35,44}})then put(bindings,x,y,leatherDark)end
  end end
  for _,r in ipairs({{43,36,38},{44,35,36},{46,34,37},{47,33,34},{49,32,36},{50,32,33},{52,32,35},{53,32,33},{55,34,37}})do run(bindings,r[1],r[2],r[3],leather)end
  for _,p in ipairs({{36,43},{34,46},{33,49},{32,52},{34,55}})do put(bindings,p[1],p[2],leatherLight)end
  -- A small iron collar separates grip from pommel.
  run(bindings,57,35,39,ironDark);run(bindings,58,34,40,ironLight)
 else
  -- Light sword polish only: fuller seam, guard bevel and leather clarity.
  for y=23,51 do put(planes,48,y,ironDark)end
  for y=18,44 do put(bevel,46,y,steel)end
  run(bevel,56,41,54,steel);run(planes,57,41,54,ironDark)
  for _,r in ipairs({{61,46,48},{63,46,47},{65,46,47},{67,46,47},{69,46,48}})do run(bindings,r[1],r[2],r[3],leatherLight)end
  put(bindings,49,61,leatherDark);put(bindings,49,63,leatherDark);put(bindings,49,65,leatherDark);put(bindings,49,67,leatherDark)
 end
 local out=C..'/'..category;app.fs.makeAllDirectories(file(out))
 for _,v in ipairs({{'forged-plane-retouch',planes},{'cutting-bevel',bevel},{'wood-haft',haft},{'leather-bindings',bindings}})do
  local l=s:newLayer();l.name=v[1];s:newCel(l,1,v[2],Point(0,0))
 end
 s:saveAs(file(out..'/'..id..'.aseprite'));s:close()
 local saved=app.open(file(out..'/'..id..'.aseprite'));local im=blank(96,96);im:drawSprite(saved,1);im:saveAs(file(out..'/'..id..'.png'));saved:close()
 print(category..' separate editable fork saved and freshly exported.')
end
editWeapon('Axe','militia-axe');editWeapon('Sword','recruit-sword')
