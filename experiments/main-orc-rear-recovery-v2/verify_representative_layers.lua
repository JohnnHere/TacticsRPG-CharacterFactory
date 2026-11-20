local root=app.fs.currentPath
local function file(p) return app.fs.joinPath(root,p) end
local checks={
 {"characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-attack-representative-v2.aseprite",{"weaponBack","body","weaponFront","handFront"},{90,80,90,80,100,80,100,110}},
 {"characters/orc-v1/source/aseprite/rear-recovery-v2/native/sword-body-representative-v2-back_r.aseprite",{"Sword_body_back_r"},{90,80,90,80,100,80,100,110}},
 {"characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-attack.aseprite",{"weaponBack","body","weaponFront","handFront"},{30,65,35,50,45,65,35,35,100,55,80,45,90}},
 {"characters/orc-v1/source/aseprite/rear-recovery-v2/composite/front_r/unarmed-attack.aseprite",{"body"},{80,110,50,90,120}},
 {"characters/orc-v1/source/aseprite/rear-recovery-v2/composite/front_l/unarmed-attack.aseprite",{"body"},{80,110,50,90,120}},
 {"characters/orc-v1/source/aseprite/rear-recovery-v2/native/sword-back_r.aseprite",{"Sword_back_r"},{30,65,35,50,45,65,35,35,100,55,80,45,90}},
 {"characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-front_r.aseprite",{"Unarmed_front_r"},{80,110,50,90,120}},
 {"characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-front_l.aseprite",{"Unarmed_front_l"},{80,110,50,90,120}}
}
for _,c in ipairs(checks) do
 local s=Sprite{fromFile=file(c[1])}
 assert(#s.layers==#c[2],c[1].." layer count")
 assert(#s.frames==#c[3],c[1].." frame count")
 for li,name in ipairs(c[2]) do assert(s.layers[li].name==name,c[1].." layer order/name "..li) end
 for fi,ms in ipairs(c[3]) do assert(math.floor(s.frames[fi].duration*1000+0.5)==ms,c[1].." frame duration "..(fi-1)) end
 print("PASS "..c[1].." frames="..#s.frames.." layers="..table.concat(c[2],","))
 s:close()
end
