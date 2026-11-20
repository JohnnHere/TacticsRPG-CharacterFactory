local a=Image{fromFile='characters/orc-v1/source/combat-rescue-v5/body-specialist/02-apex-native.png'}
local s=Sprite(128,128,ColorMode.RGB);s:newCel(s.layers[1],1,a,Point(0,0));app.activeSprite=s;app.command.SpriteSize{ui=false,width=512,height=512,method='nearest-neighbor'};s:saveCopyAs('experiments/main-orc-combat-recovery-v7/rear/donor-apex-4x.png');s:close()
