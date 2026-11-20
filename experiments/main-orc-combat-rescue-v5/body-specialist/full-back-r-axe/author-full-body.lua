local files={
"experiments/main-orc-combat-rescue-v5/body-specialist/canonical-input.png",
"experiments/main-orc-combat-rescue-v5/body-specialist/full-back-r-axe/entry-1.png",
"experiments/main-orc-combat-rescue-v5/body-specialist/full-back-r-axe/entry-2.png",
"characters/orc-v1/source/combat-rescue-v5/body-specialist/01-hoist-native.png",
"characters/orc-v1/source/combat-rescue-v5/body-specialist/02-apex-native.png",
"experiments/main-orc-combat-rescue-v5/body-specialist/full-back-r-axe/descent-2.png",
"experiments/main-orc-combat-rescue-v5/body-specialist/full-back-r-axe/descent-3.png",
"characters/orc-v1/source/combat-rescue-v5/body-specialist/repair1/03-impact-native.png",
"experiments/main-orc-combat-rescue-v5/body-specialist/full-back-r-axe/recovery-1.png",
"experiments/main-orc-combat-rescue-v5/body-specialist/full-back-r-axe/recovery-2.png",
"experiments/main-orc-combat-rescue-v5/body-specialist/full-back-r-axe/recovery-3.png",
"experiments/main-orc-combat-rescue-v5/body-specialist/canonical-input.png",
}
local times={0.07,0.08,0.09,0.1,0.11,0.05,0.06,0.11,0.1,0.1,0.1,0.13}
local out='./characters/orc-v1/source/combat-rescue-v5/body-specialist/full-back-r-axe/'
local n=Sprite(128,128,ColorMode.RGB);n.layers[1].name='body'
local b=Sprite(256,256,ColorMode.RGB);b.layers[1].name='body'
local ns=Image(128*#files,128,ColorMode.RGB);local bs=Image(256*#files,256,ColorMode.RGB)
for i,path in ipairs(files) do
 if i>1 then n:newFrame();b:newFrame() end
 local img=Image{fromFile=path}
 n.frames[i].duration=times[i];b.frames[i].duration=times[i]
 n:newCel(n.layers[1],i,img,Point(0,0));b:newCel(b.layers[1],i,img,Point(64,64))
 local full=Image(256,256,ColorMode.RGB);full:drawImage(img,Point(64,64))
 img:saveAs(out..'native/'..string.format('%02d',i-1)..'.png')
 full:saveAs(out..'body256/'..string.format('%02d',i-1)..'.png')
 ns:drawImage(img,Point((i-1)*128,0));bs:drawImage(full,Point((i-1)*256,0))
end
n:saveAs(out..'native128.aseprite');b:saveAs(out..'body256.aseprite')
ns:saveAs(out..'native-strip.png');bs:saveAs(out..'body256-strip.png')
n:close();b:close()
