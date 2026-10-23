-- Preview derivatives from native masters. Never edits a saved source.
local root=assert(app.params.root);local base=app.fs.joinPath(root,'characters/orc-01-aseprite-v4/source/aseprite/retouched')
for _,id in ipairs({'attack','hit'})do
 local s=app.open(app.fs.joinPath(base,id..'.aseprite'));s.layers[3].isVisible=false
 for f=1,#s.frames do local i=Image(128,128,ColorMode.RGB);i:clear();i:drawSprite(s,f);i:saveAs(app.fs.joinPath(base,id,string.format('working_%02d.png',f-1)))end
 s:close()
end
print('8 working-pose previews exported; local retouch layer hidden, masters unchanged')
