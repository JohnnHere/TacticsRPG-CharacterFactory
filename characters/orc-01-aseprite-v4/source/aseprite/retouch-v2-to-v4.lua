-- Retouch approved V2 pixels INSIDE Aseprite. No reconstruction or new anatomy.
-- The preserved V2 reference layer remains pixel-identical and hidden.
local root=assert(app.params.root);local output=assert(app.params.output)
app.fs.makeAllDirectories(output)
local function file(p)return app.fs.joinPath(root,p)end
local function color(h,a)return app.pixelColor.rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),a or 255)end
local function hex(p)return string.format('%02x%02x%02x',app.pixelColor.rgbaR(p),app.pixelColor.rgbaG(p),app.pixelColor.rgbaB(p))end
local function render(s,f)local i=Image(s.width,s.height,ColorMode.RGB);i:clear();i:drawSprite(s,f);return i end
local V2='characters/orc-01/source/aseprite/combat-refinement-v2/'
local fork='characters/orc-01/source/aseprite/orc-v4-retouch/source/'
local originalAttack=app.open(file(V2..'Attack/attack_front_r.aseprite'))
local neutral=render(originalAttack,1);originalAttack:close()
local darks={['010000']=true,['010001']=true,['020101']=true,['030201']=true,['050302']=true,['040402']=true,['040201']=true,['040302']=true,['030302']=true}
local iron={['645d59']=true,['5b5148']=true,['373337']=true,['484347']=true,['544e50']=true,['796f5b']=true,['a3967b']=true,['cdb69c']=true,['e4d8d3']=true,['fafaf9']=true,['3f3c3f']=true,['4c474b']=true}
local skin={['aa874c']=true,['baab60']=true,['6e664a']=true,['877c5a']=true,['bdaf67']=true,['beac5c']=true,['958963']=true}
-- Explicit per-pose patches chosen after inspecting the approved V2 pixels.
-- Format x,y,target RGB, optional material gate. No silhouettes are redrawn.
local neutralPatches={
 {67,36,'d0844d','eye'}, {66,35,'080604','eye'},
 {68,44,'6e664a','skin'},{69,44,'6e664a','skin'},
 {43,55,'baab60','skin'},{42,56,'baab60','skin'},{43,58,'aa874c','skin'},{44,59,'6e664a','skin'},
 {78,46,'cdb69c','iron'},{79,47,'e4d8d3','iron'},{80,48,'cdb69c','iron'},{81,49,'a3967b','iron'},
 {82,53,'5b5148','iron'},{83,54,'484347','iron'},
 {89,74,'cdb69c','iron'},{88,76,'645d59','iron'},{88,77,'484347','iron'},
 {65,69,'cdb69c','iron'},{64,69,'645d59','iron'}
}
local patches={
 Attack={neutralPatches,
  {{67,36,'d0844d','eye'},{66,35,'080604','eye'},{69,45,'6e664a','skin'},
   {78,47,'cdb69c','iron'},{79,48,'e4d8d3','iron'},{80,49,'a3967b','iron'},{81,52,'5b5148','iron'},
   {43,57,'baab60','skin'},{44,60,'6e664a','skin'}},
  {{69,38,'d0844d','eye'},{68,38,'cdb69c','eye'},{68,37,'080604','eye'},
   {56,52,'baab60','skin'},{57,52,'baab60','skin'},{58,54,'aa874c','skin'},
   {64,57,'6e664a','skin'},{65,57,'6e664a','skin'},
   {83,49,'d69c63','leather'},{84,49,'b4673a','leather'},
   {80,67,'cdb69c','iron'},{79,68,'e4d8d3','iron'},{79,69,'645d59','iron'}},
  {{68,37,'d0844d','eye'},{67,36,'080604','eye'},{70,45,'6e664a','skin'},
   {81,48,'cdb69c','iron'},{82,49,'e4d8d3','iron'},{83,50,'a3967b','iron'},
   {50,55,'baab60','skin'},{51,58,'6e664a','skin'}},
  neutralPatches},
 Hit={
  {{66,33,'d0844d','eye'},{65,32,'080604','eye'},{67,40,'6e664a','skin'},
   {47,54,'baab60','skin'},{48,56,'aa874c','skin'},{49,59,'6e664a','skin'},
   {83,44,'cdb69c','iron'},{84,45,'e4d8d3','iron'},{85,46,'a3967b','iron'},
   {71,70,'cdb69c','iron'}},
  {{71,43,'d0844d','eye'},{70,42,'6e664a','skin'},
   {38,52,'baab60','skin'},{39,54,'aa874c','skin'},{40,58,'6e664a','skin'},
   {78,49,'cdb69c','iron'},{79,50,'e4d8d3','iron'},{80,51,'a3967b','iron'},
   {84,62,'cdb69c','iron'},{84,64,'645d59','iron'},{83,66,'484347','iron'}},
  neutralPatches}
}
local report={method='Localized Aseprite retouch over approved V2; same design and inherited raster provenance',newImageGenerationCalls=0,newAnatomyGeneration=false,documents={}}
local function export(s,id,originals,edits)
 local dir=app.fs.joinPath(output,id);app.fs.makeAllDirectories(dir)
 local source=app.fs.joinPath(output,id..'.aseprite');s:saveAs(source)
 local rec={id=id,width=s.width,height=s.height,source=source,layers={},frames={}}
 for _,l in ipairs(s.layers)do table.insert(rec.layers,{name=l.name,visible=l.isVisible})end
 local strip=nil;if s.width==128 then strip=Image(s.width*#s.frames,s.height,ColorMode.RGB);strip:clear()end
 for f=1,#s.frames do
  local image=render(s,f);local name=string.format('%s_front_r_%02d.png',id,f-1);image:saveAs(app.fs.joinPath(dir,name))
  local delta=Image(s.width,s.height,ColorMode.RGB);delta:clear();local changed,alphaChanged=0,0
  for y=0,s.height-1 do for x=0,s.width-1 do local old,new=originals[f]:getPixel(x,y),image:getPixel(x,y)
   if old~=new then changed=changed+1;delta:drawPixel(x,y,color('f05678',220))end
   if app.pixelColor.rgbaA(old)~=app.pixelColor.rgbaA(new)then alphaChanged=alphaChanged+1 end
  end end
  delta:saveAs(app.fs.joinPath(dir,string.format('delta_%02d.png',f-1)))
  if strip then strip:drawImage(image,Point((f-1)*128,0))end
  table.insert(rec.frames,{file=name,durationMs=math.floor(s.frames[f].duration*1000+.5),changedPixels=changed,changedAlphaPixels=alphaChanged,edits=edits[f]})
 end
 if strip then strip:saveAs(app.fs.joinPath(dir,'native-strip.png'))end
 table.insert(report.documents,rec)
end
for _,id in ipairs({'Attack','Hit'})do
 local s=app.open(file(fork..id:lower()..'-front-r.aseprite'))
 local originals={};for f=1,#s.frames do originals[f]=render(s,f)end
 s.layers[1].name='V2 preserved reference - hidden';s.layers[1].isVisible=false
 local work=s:newLayer();work.name='V4 working poses - approved reuse'
 local detail=s:newLayer();detail.name='V4 local cluster retouch'
 local edits={}
 for f=1,#s.frames do
  local rest=(id=='Attack' and f==5)or(id=='Hit' and f==3)
  local base=Image(rest and neutral or originals[f]);local overlay=Image(128,128,ColorMode.RGB);overlay:clear()
  local stats={canonicalNeutralReuse=rest,nearBlackCleanup=0,localPaint=0,eyeCorrections=0}
  local function paint(x,y,h,group)
   local old=base:getPixel(x,y);assert(app.pixelColor.rgbaA(old)==255,'Retouch outside opaque approved art')
   local current=overlay:getPixel(x,y);if app.pixelColor.rgbaA(current)==0 then current=old end
   local new=color(h);if current~=new then overlay:drawPixel(x,y,new);stats[group]=stats[group]+1 end
  end
  -- Consolidate near-identical black shades, preserving pure black and ink080604.
  for y=0,127 do for x=0,127 do local p=base:getPixel(x,y)
   if app.pixelColor.rgbaA(p)==255 and darks[hex(p)]then paint(x,y,'080604','nearBlackCleanup')end
  end end
  for _,p in ipairs(patches[id][f])do
   local x,y,h,gate=p[1],p[2],p[3],p[4];local old=base:getPixel(x,y);local oldHex=hex(old)
   local permitted=gate=='eye' or(gate=='skin' and skin[oldHex])or(gate=='iron' and iron[oldHex])or(gate=='leather' and (oldHex=='b4673a'or oldHex=='d0844d'or oldHex=='924e2c'or oldHex=='884829'))
   if permitted then paint(x,y,h,gate=='eye' and 'eyeCorrections' or 'localPaint')end
  end
  s:newCel(work,f,base,Point(0,0));s:newCel(detail,f,overlay,Point(0,0));edits[f]=stats
 end
 export(s,id:lower(),originals,edits);s:close()
end
-- Concept: retain original resolution, face, anatomy, palette and silhouette.
-- Local metal finishing only, using colors sampled from the SAME approved PNG.
local s=app.open(file('characters/orc-01-refinement-v2/concepts/warrior-refinement-v2.png'))
local original=render(s,1);s.layers[1].name='V2 preserved reference - hidden';s.layers[1].isVisible=false
local work=s:newLayer();work.name='V4 concept - original geometry'
local base=Image(original);local fringe=0
for y=0,s.height-1 do for x=0,s.width-1 do
 local p=base:getPixel(x,y);local a=app.pixelColor.rgbaA(p)
 -- Only almost invisible peripheral alpha; opaque design is never trimmed.
 if a>0 and a<=12 then base:drawPixel(x,y,0);fringe=fringe+1 end
end end
local detail=s:newLayer();detail.name='Review map - selective iron edits - hidden';detail.isVisible=false
local overlay=Image(s.width,s.height,ColorMode.RGB);overlay:clear();local retouched=0
local function metalPixel(x,y,sampleX,sampleY)
 local old=original:getPixel(x,y);local new=original:getPixel(sampleX,sampleY)
 local r,g,b=app.pixelColor.rgbaR(old),app.pixelColor.rgbaG(old),app.pixelColor.rgbaB(old)
 -- Neutral warm iron only; excludes skin/red/leather and keeps original alpha.
 if app.pixelColor.rgbaA(old)>=240 and math.abs(r-g)<40 and math.abs(g-b)<35 and r>50 then
  local painted=app.pixelColor.rgba(app.pixelColor.rgbaR(new),app.pixelColor.rgbaG(new),app.pixelColor.rgbaB(new),app.pixelColor.rgbaA(old))
  if old~=painted then base:drawPixel(x,y,painted);overlay:drawPixel(x,y,painted);retouched=retouched+1 end
 end
end
-- Six individual pixels on the existing rivet: adjacent source colors only.
-- Broad facet repaint was rejected visually and is archived in iterations/.
metalPixel(829,345,829,344);metalPixel(830,345,829,344)
metalPixel(830,346,830,345);metalPixel(831,346,830,345)
metalPixel(832,347,831,347);metalPixel(832,348,831,348)
s:newCel(work,1,base,Point(0,0));s:newCel(detail,1,overlay,Point(0,0));s.frames[1].duration=.1
export(s,'concept',{original},{{lowAlphaFringeCleanup=fringe,selectiveMetalPixels=retouched,faceAndBodyRedraw=false}});s:close()
local f=assert(io.open(app.fs.joinPath(output,'retouch-report.json'),'w'));f:write(json.encode(report));f:close()
print('V4 retouched approved V2 pixels; preserved reference layers; source design not regenerated')
