local root=app.fs.currentPath
local function path(p) return app.fs.joinPath(root,p) end
local function save(im,p) app.fs.makeAllDirectories(app.fs.filePath(path(p))); im:saveAs(path(p)) end
local function rgb(c) return app.pixelColor.rgbaR(c),app.pixelColor.rgbaG(c),app.pixelColor.rgbaB(c),app.pixelColor.rgbaA(c) end
local function lum(r,g,b) return (r*299+g*587+b*114)/1000 end
local jobs={
 {slug='front_r-Sword',x=132,y=104},
 {slug='front_l-Sword',x=123,y=104}
}
for _,j in ipairs(jobs) do
 local base='characters/orc-v1/source/combat-recovery-v8/frontal/'..j.slug..'/source/composite.aseprite'
 local spr=app.open(path(base)); assert(spr and spr.width==256 and spr.height==256,'bad source '..j.slug)
 local wf,body
 for _,l in ipairs(spr.layers) do if l.name=='weaponFront' then wf=l elseif l.name=='body' then body=l end end
 assert(wf and body,'required separated layers '..j.slug)
 local changes=0
 for fi=1,#spr.frames do
  local cel=wf:cel(fi)
  if cel then
   local img=cel.image
   -- Anti-flash: lower only neutral specular metal highlights on the independent weapon layer.
   -- F02 gets a deliberate soft ceiling; F05-F07 use the same restrained steel range.
   if fi==3 or fi==6 or fi==7 or fi==8 or fi==11 or fi==13 then
    for y=0,img.height-1 do for x=0,img.width-1 do
     local c=img:getPixel(x,y); local r,g,b,a=rgb(c)
     if a>0 and lum(r,g,b)>=160 and math.abs(r-g)<28 and math.abs(g-b)<32 then
      local ceiling=(fi==3 and 132 or (fi>=6 and fi<=8 and 142 or 150))
      local k=ceiling/math.max(1,lum(r,g,b)); local nr,ng,nb=math.floor(r*k),math.floor(g*k),math.floor(b*k)
      img:drawPixel(x,y,app.pixelColor.rgba(nr,ng,nb,a)); changes=changes+1
     end
    end end
   end
  end
  -- Exact chest glint pixel gets controlled luminance through the sequence; no anatomy pixels move.
  local bc=body:cel(fi)
  if bc and j.x>=0 and j.x<bc.image.width and j.y>=0 and j.y<bc.image.height then
   local c=bc.image:getPixel(j.x,j.y); local r,g,b,a=rgb(c)
   if a>0 and lum(r,g,b)>180 then
    local target=({[1]=165,[2]=158,[3]=152,[4]=150,[5]=148,[6]=145,[7]=145,[8]=148,[9]=152,[10]=158,[11]=162,[12]=165,[13]=168})[fi]
    local k=target/lum(r,g,b)
    bc.image:drawPixel(j.x,j.y,app.pixelColor.rgba(math.floor(r*k),math.floor(g*k),math.floor(b*k),a)); changes=changes+1
   end
  end
 end
 spr:saveAs(path(base)); spr:close()
 print(j.slug..' edited_pixels='..changes)
end
