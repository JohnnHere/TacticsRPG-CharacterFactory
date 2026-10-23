-- Read-only verification of saved master references and exports.
local root=assert(app.params.root)
local function file(p)return app.fs.joinPath(root,p)end
local base='characters/orc-01-art-lab-v5'
local f=assert(io.open(file(base..'/source/art-lab-render.json'),'r'));local variants=json.decode(f:read('*a'));f:close()
local original=app.open(file('characters/orc-01-aseprite-v4/source/aseprite/orc-art-lab-v5-baseline/source/concept-front-r.aseprite'))
local reference=Image(original.width,original.height,ColorMode.RGB);reference:clear();reference:drawSprite(original,1);original:close()
local result={status='PASS',hiddenReferencesExact=0,savedMasterExportsExact=0,variants={}}
for _,v in ipairs(variants)do
 local s=app.open(file(v.source));assert(#s.layers==4 and #s.frames==1)
 assert(not s.layers[1].isVisible and s.layers[2].isVisible and s.layers[3].isVisible and s.layers[4].isVisible)
 local cel=s.layers[1]:cel(1);assert(cel and cel.position.x==0 and cel.position.y==0)
 local rendered=Image(s.width,s.height,ColorMode.RGB);rendered:clear();rendered:drawSprite(s,1)
 local png=app.open(file(v.png));local exported=Image(png.width,png.height,ColorMode.RGB);exported:clear();exported:drawSprite(png,1);png:close()
 local refExact,exportExact=true,true
 for y=0,s.height-1 do for x=0,s.width-1 do
  if cel.image:getPixel(x,y)~=reference:getPixel(x,y)then refExact=false end
  if rendered:getPixel(x,y)~=exported:getPixel(x,y)then exportExact=false end
 end end
 assert(refExact,'Hidden reference modified: '..v.id);assert(exportExact,'Saved export differs: '..v.id)
 result.hiddenReferencesExact=result.hiddenReferencesExact+1;result.savedMasterExportsExact=result.savedMasterExportsExact+1
 result.variants[#result.variants+1]={id=v.id,hiddenReferenceExact=true,exportExact=true,layers=4,width=s.width,height=s.height}
 s:close()
end
local o=assert(io.open(file('reports/orc-art-lab-v5-source-check.json'),'w'));o:write(json.encode(result));o:close()
print('PASS: five saved masters, five exact hidden V4 references and five exact PNG exports.')
