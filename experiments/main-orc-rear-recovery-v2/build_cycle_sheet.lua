-- QA-only contact sheet of saved 256px attack frames, laid out 4 x 2 at 1x.
local root=app.fs.currentPath
local function file(p) return app.fs.joinPath(root,p) end
local out=Image(1024,512,ColorMode.RGB);out:clear()
local d="characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/"
for i=0,7 do local im=Image{fromFile=file(d..string.format("%02d.png",i))};out:drawImage(im,Point((i%4)*256,math.floor(i/4)*256)) end
out:saveAs(file("experiments/main-orc-rear-recovery-v2/back_r-sword-representative-composite-sheet-qa.png"))
print("Saved 4x2 actual 256px composite cycle sheet.")
