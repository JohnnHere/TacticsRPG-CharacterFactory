-- Fresh render from the saved baseline and fork, including real layer sources.
local E="experiments/main-orc-targeted-repair-v1/artist-sword-sol"
local S="characters/orc-v1/source/targeted-repair-sword-sol-v1"
local function f(p)return app.fs.joinPath(app.fs.currentPath,p)end
local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local docs={}
for _,sp in ipairs({
 {"before",E.."/before/source/sword-attack-representative-v2.aseprite",E.."/fresh-before"},
 {"candidate",S.."/source/sword-f05-grip-composite.aseprite",S}
})do
 local s=app.open(f(sp[2]));local out=sp[3];local layers={};for _,l in ipairs(s.layers)do layers[l.name]=l end
 app.fs.makeAllDirectories(f(out.."/composite"));app.fs.makeAllDirectories(f(out.."/native"));app.fs.makeAllDirectories(f(out.."/body-only"))
 for _,n in ipairs({"weaponBack","body","weaponFront","handFront"})do app.fs.makeAllDirectories(f(out.."/layers/"..n))end
 local doc={key=sp[1],source=sp[2],width=s.width,height=s.height,layers={},frames={}}
 for _,l in ipairs(s.layers)do table.insert(doc.layers,l.name)end
 for i=1,8 do
  for _,l in ipairs(s.layers)do l.isVisible=true end
  local full=blank(256,256);full:drawSprite(s,i);full:saveAs(f(out.."/composite/"..string.format("%02d.png",i-1)))
  local fr={index=i-1,durationMs=math.floor(s.frames[i].duration*1000+0.5),cels={}}
  for _,n in ipairs({"weaponBack","body","weaponFront","handFront"})do
   for _,l in ipairs(s.layers)do l.isVisible=l.name==n end
   local im=blank(256,256);im:drawSprite(s,i);im:saveAs(f(out.."/layers/"..n.."/"..string.format("%02d.png",i-1)))
   local c=layers[n]:cel(i);if c then fr.cels[n]={position={c.position.x,c.position.y},imageSize={c.image.width,c.image.height}}end
   if n=="body" then
    im:saveAs(f(out.."/body-only/"..string.format("%02d.png",i-1)))
    local nat=blank(128,128);nat:drawImage(im,Point(-64,-64));nat:saveAs(f(out.."/native/"..string.format("%02d.png",i-1)))
   end
  end
  table.insert(doc.frames,fr)
 end;s:close();table.insert(docs,doc)
end
-- Reopen separate native/body saved masters to prove they match the compound.
for _,sp in ipairs({{"body",256,S.."/source/sword-f05-grip-body.aseprite"},{"native",128,S.."/source/sword-f05-grip-native.aseprite"}})do
 local s=app.open(f(sp[3]));app.fs.makeAllDirectories(f(E.."/source-proof/"..sp[1]))
 for i=1,8 do local im=blank(sp[2],sp[2]);im:drawSprite(s,i);im:saveAs(f(E.."/source-proof/"..sp[1].."/"..string.format("%02d.png",i-1)))end;s:close()
end
local file=io.open(f(E.."/source-document.json"),"w");file:write(json.encode(docs));file:close()
print("Reopened/exported all8 baseline and candidate frames/four layers; separate body/native masters rendered for proof.")
