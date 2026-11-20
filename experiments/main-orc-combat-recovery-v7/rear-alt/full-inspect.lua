local root=app.fs.currentPath;local function abs(p)return app.fs.joinPath(root,p)end
for _,kind in ipairs({'sword','axe'})do
local out=Image(128*6,128*2,ColorMode.RGB);out:clear()
for i=0,11 do local raw=Image{fromFile=abs('characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-'..kind..'/layers/body/'..string.format('%02d',i)..'.png')};local im=Image(128,128,ColorMode.RGB);im:clear();im:drawImage(raw,Point(-64,-64));out:drawImage(im,Point((i%6)*128,math.floor(i/6)*128))end
out:resize(1536,512);out:saveAs(abs('experiments/main-orc-combat-recovery-v7/rear-alt/full-inspect-'..kind..'.png'))
end
