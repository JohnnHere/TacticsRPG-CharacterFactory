-- probe composite master structure (writes result to file; GUI exe has no captured stdout)
local function abs(p) return app.fs.joinPath(app.fs.currentPath,p) end
local out=assert(io.open(abs('experiments/main-orc-artistic-reconstruction-v6/frontal/probe-out.txt'),'w'))
local function say(s) out:write(s..'\n') end
local slug='front_l-Sword-full'
local sp=app.open(abs('characters/orc-v1/source/artistic-reconstruction-v6/frontal/'..slug..'/source/composite.aseprite'))
say('frames='..#sp.frames..' canvas='..sp.width..'x'..sp.height)
local pc=app.pixelColor
local function walk(layers,depth)
 for _,l in ipairs(layers) do
  local extra=''
  if l.isGroup then
   extra=' GROUP children='..#l.layers
  else
   local ok,cel=pcall(function() return l:cel(13) end)
   if ok and cel then
    local p=cel.image:getPixel(131,89)
    extra=string.format(' cel13 pos=%d,%d size=%dx%d px(131,89)=%d,%d,%d,%d',cel.position.x,cel.position.y,cel.image.width,cel.image.height,pc.rgbaR(p),pc.rgbaG(p),pc.rgbaB(p),pc.rgbaA(p))
   else
    extra=' cel13=nil or error'
   end
  end
  say(string.rep(' ',depth*2)..'L name=['..l.name..'] opacity='..l.opacity..' blend='..tostring(l.blendMode)..' visible='..tostring(l.isVisible)..extra)
  if l.isGroup then walk(l.layers,depth+1) end
 end
end
walk(sp.layers,1)
sp:close()
out:write('PROBE_DONE\n')
out:close()
