-- QA-only nearest-neighbour before/after crops, assembled inside Aseprite.
local root=app.fs.currentPath
local function file(p) return app.fs.joinPath(root,p) end
for _,d in ipairs({"front_r","front_l"}) do
 local base=Image{fromFile=file("characters/orc-v1/source/complete-v1/"..d.."/Unarmed/02.png")}
 local cand=Image{fromFile=file("characters/orc-v1/source/rear-recovery-v2/"..d.."/Unarmed/02.png")}
 local x0=d=="front_r" and 136 or 72; local y0=96; local w,h=64,56; local scale=4
 local out=Image(w*scale*2,h*scale,ColorMode.RGB); out:clear()
 for y=0,h-1 do for x=0,w-1 do
  local a=base:getPixel(x0+x,y0+y); local b=cand:getPixel(x0+x,y0+y)
  for yy=0,scale-1 do for xx=0,scale-1 do
   out:drawPixel(x*scale+xx,y*scale+yy,a)
   out:drawPixel((w+x)*scale+xx,y*scale+yy,b)
  end end
 end end
 out:saveAs(file("experiments/main-orc-rear-recovery-v2/"..d.."-f02-before-after-clean-qa.png"))
end
print("Saved Aseprite QA crops for both F02 candidates.")
