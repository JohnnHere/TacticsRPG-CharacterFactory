local dir='experiments/main-orc-combat-recovery-v7/rear'
local out=Image(128*12,128,ColorMode.RGB);out:clear()
for i=0,11 do local p=string.format('%s/raw/axe/%02d.png',dir,i);local im=Image{fromFile=p};out:drawImage(im,Point(i*128,0)) end
out:saveAs(dir..'/axe-raw-strip.png')

