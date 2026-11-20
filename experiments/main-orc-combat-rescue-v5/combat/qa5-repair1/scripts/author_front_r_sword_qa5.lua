-- Author qa5-repair1/front_r/Sword in Aseprite with real anatomical grip and handFront enclosure
local envRoot = "C:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory"

local srcBodyDir = envRoot .. "/characters/orc-v1/source/combat-rescue-v5/combat/front_r/Sword/layers/body"
local srcNativeDir = envRoot .. "/characters/orc-v1/source/combat-rescue-v5/combat/front_r/Sword/native"
local weaponPng = envRoot .. "/characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/recruit-sword.png"
local outDir = envRoot .. "/characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword"

app.fs.makeAllDirectories(outDir)
app.fs.makeAllDirectories(outDir .. "/source")
app.fs.makeAllDirectories(outDir .. "/frames")
app.fs.makeAllDirectories(outDir .. "/native")
app.fs.makeAllDirectories(outDir .. "/layers/weaponBack")
app.fs.makeAllDirectories(outDir .. "/layers/body")
app.fs.makeAllDirectories(outDir .. "/layers/weaponFront")
app.fs.makeAllDirectories(outDir .. "/layers/handFront")

local durations = {30, 65, 35, 50, 45, 65, 35, 35, 100, 55, 80, 45, 90}

-- Real anatomical coordinates measured on the actual posed body frames (256x256 composite space)
-- In recruit-sword (front_r.png, 128x128), rightGrip = (48, 66), pommel = (47, 73..78), crossguard = (35..60, 54..59), blade tip = (47, 7).
-- At deg = 0, the sword points straight UP (-90 deg in screen space). +deg rotates clockwise (+90 = right, +180 = down, -90 = left).
local anatomy = {
    [1]  = {vis=false, sh={104,102}, el={92,118},  wr={94,133},  pa={96,138},  box={91,133,101,144}, ang=0,    layer="weaponFront"},
    [2]  = {vis=false, sh={104,103}, el={95,115},  wr={98,122},  pa={101,125}, box={96,120,105,130}, ang=0,    layer="weaponFront"},
    [3]  = {vis=true,  sh={104,103}, el={93,117},  wr={96,126},  pa={100,130}, box={94,124,105,136}, ang=-28,  layer="weaponFront"}, -- F02: first-grip-hold (blade up-left -118 deg)
    [4]  = {vis=true,  sh={105,100}, el={87,108},  wr={83,116},  pa={81,119},  box={76,113,87,125},  ang=-24,  layer="weaponFront"}, -- F03: windup-back (blade cocked high up-left -114 deg)
    [5]  = {vis=true,  sh={105,97},  el={85,103},  wr={79,109},  pa={76,111},  box={71,105,82,117},  ang=-30,  layer="weaponFront"}, -- F04: windup-hold (blade coiled high up-left -120 deg)
    [6]  = {vis=true,  sh={107,98},  el={89,104},  wr={84,109},  pa={80,111},  box={75,105,86,117},  ang=-14,  layer="weaponFront"}, -- F05: slash-drive (blade sweeping through top arc -104 deg)
    [7]  = {vis=true,  sh={112,102}, el={126,109}, wr={136,111}, pa={142,115}, box={136,109,148,121},ang=78,   layer="weaponFront"}, -- F06: slash-release (blade slashing across right -12 deg)
    [8]  = {vis=true,  sh={114,103}, el={132,117}, wr={145,124}, pa={152,129}, box={146,122,158,135},ang=108,  layer="weaponFront"}, -- F07: impact-hold (blade extended forward-down-right +18 deg)
    [9]  = {vis=true,  sh={110,104}, el={126,129}, wr={141,139}, pa={148,143}, box={142,137,154,149},ang=128,  layer="weaponFront"}, -- F08: follow-through (blade low down-right +38 deg)
    [10] = {vis=true,  sh={106,105}, el={109,129}, wr={118,144}, pa={122,149}, box={116,143,128,155},ang=115,  layer="weaponFront"}, -- F09: recover-start (+25 deg)
    [11] = {vis=true,  sh={104,104}, el={97,122},  wr={104,136}, pa={109,141}, box={103,135,115,147},ang=95,   layer="weaponFront"}, -- F10: recover-mid (+5 deg)
    [12] = {vis=false, sh={104,103}, el={95,120},  wr={99,136},  pa={102,140}, box={96,135,107,145}, ang=0,    layer="weaponFront"},
    [13] = {vis=false, sh={104,102}, el={92,118},  wr={94,133},  pa={96,138},  box={91,133,101,144}, ang=0,    layer="weaponFront"}
}

local wepImg = Image{ fromFile=weaponPng }
local gripPivotX, gripPivotY = 48, 66

-- Helper: rotate weapon image around (gripPivotX, gripPivotY) and place pivot at (targetX, targetY) on a 256x256 Image
local function renderRotatedWeapon(deg, targetX, targetY)
    local out = Image(256, 256, ColorMode.RGB)
    local rad = math.rad(deg)
    local cosA = math.cos(rad)
    local sinA = math.sin(rad)
    -- Iterate over bounding area around targetX, targetY
    for dy = -90, 90 do
        for dx = -90, 90 do
            local sx = math.floor(gripPivotX + dx * cosA + dy * sinA + 0.5)
            local sy = math.floor(gripPivotY - dx * sinA + dy * cosA + 0.5)
            if sx >= 0 and sx < wepImg.width and sy >= 0 and sy < wepImg.height then
                local px = wepImg:getPixel(sx, sy)
                if app.pixelColor.rgbaA(px) > 0 then
                    local ox, oy = targetX + dx, targetY + dy
                    if ox >= 0 and ox < 256 and oy >= 0 and oy < 256 then
                        out:drawPixel(ox, oy, px)
                    end
                end
            end
        end
    end
    return out
end

-- Helper: Author anatomical handFront that uses the REAL gauntlet/fist pixels of the body + anatomical finger/thumb wrap over the handle shaft and continuous wrist-to-forearm bridge, while leaving crossguard and pommel clear
local function renderAnatomicalHandFront(bodyImg, wepLayerImg, a)
    local out = Image(256, 256, ColorMode.RGB)
    local px, py = a.pa[1], a.pa[2]
    local wx, wy = a.wr[1], a.wr[2]

    -- Blade unit vector after rotation `a.ang` (original blade direction in recruit-sword.png is straight UP: (0, -1), i.e. -90 deg)
    local totalRad = math.rad(-90 + a.ang)
    local ux, uy = math.cos(totalRad), math.sin(totalRad) -- points from grip (48,66) toward guard (y=57) and blade tip (y=7)
    local nx, ny = -uy, ux -- perpendicular across handle width (x=45..50)

    -- Direction from palm center toward forearm wrist
    local wdx, wdy = wx - px, wy - py
    local wLen = math.max(math.sqrt(wdx * wdx + wdy * wdy), 1.0)
    local wux, wuy = wdx / wLen, wdy / wLen
    -- Choose `nx, ny` so +t always points toward the wrist/forearm side and -t points toward the outer knuckle edge
    if (nx * wux + ny * wuy) < 0 then
        nx, ny = -nx, -ny
    end

    -- Palette from the actual Orc V1 gauntlet/hand (steel gauntlet cuff + dark-rimmed leather fingers with iron knuckle studs)
    local cInk      = app.pixelColor.rgba(12, 15, 18, 255)
    local cLeatherD = app.pixelColor.rgba(46, 30, 22, 255)
    local cLeatherM = app.pixelColor.rgba(74, 48, 35, 255)
    local cLeatherH = app.pixelColor.rgba(98, 66, 48, 255)
    local cSteelD   = app.pixelColor.rgba(46, 52, 61, 255)
    local cSteelM   = app.pixelColor.rgba(72, 80, 92, 255)
    local cSteelH   = app.pixelColor.rgba(105, 115, 130, 255)

    -- 1. First, bridge the real forearm/wrist gauntlet cuff from (wx, wy) into (px, py) using actual body pixels where available,
    --    never crossing into the crossguard (s > 4.2) or pommel (s < -4.5).
    local steps = math.max(math.abs(px - wx), math.abs(py - wy), 1)
    for k = 0, steps do
        local u = k / steps
        local cx = math.floor(wx + (px - wx) * u + 0.5)
        local cy = math.floor(wy + (py - wy) * u + 0.5)
        for oy = -3, 3 do
            for ox = -3, 3 do
                if (ox * ox + oy * oy) <= 10 then
                    local tx, ty = cx + ox, cy + oy
                    local dx, dy = tx - px, ty - py
                    local s = dx * ux + dy * uy
                    local t = dx * nx + dy * ny
                    -- Stay strictly between pommel and crossguard, on the wrist/cuff side (t >= -1.5)
                    if s >= -4.2 and s <= 4.0 and t >= -1.5 then
                        local bpx = bodyImg:getPixel(tx, ty)
                        if app.pixelColor.rgbaA(bpx) > 0 then
                            out:drawPixel(tx, ty, bpx)
                        elseif u <= 0.65 and (ox * ox + oy * oy) <= 5 then
                            out:drawPixel(tx, ty, (ox == 0 and oy == 0) and cSteelM or cSteelD)
                        end
                    end
                end
            end
        end
    end

    -- 2. Second, sculpt 4 articulated fingers + thumb lock wrapping directly across the wooden handle shaft at (px, py)
    --    In recruit-sword.png, relative to grip (48, 66):
    --      s = +6.0 .. +11.0 is the steel crossguard (stays 100% visible)
    --      s = -5.2 .. +5.4 is the wooden handle shaft (width t = -3.2 .. +3.2)
    --      s = -12.0 .. -5.8 is the steel pommel (stays 100% visible)
    for dy = -7, 7 do
        for dx = -7, 7 do
            local gx, gy = px + dx, py + dy
            if gx >= 0 and gx < 256 and gy >= 0 and gy < 256 then
                local s = dx * ux + dy * uy
                local t = dx * nx + dy * ny
                local wpx = wepLayerImg:getPixel(gx, gy)
                local onWep = (app.pixelColor.rgbaA(wpx) > 0)
                -- Enclose every wooden handle pixel in s = [-5.0 .. +5.4], plus the compact finger block |t| <= 3.4
                if (s >= -5.0 and s <= 5.4 and onWep and math.abs(t) <= 3.8) or (s >= -4.3 and s <= 5.0 and math.abs(t) <= 3.2) then
                    local sInt = math.floor(s + 0.5)
                    -- 4 distinct fingers separated by dark inter-finger creases along `s`:
                    --   sInt = 4..5 : index finger + thumb lock under crossguard
                    --   sInt = 3    : crease
                    --   sInt = 1..2 : middle finger
                    --   sInt = 0    : crease
                    --   sInt = -2..-1: ring finger
                    --   sInt = -3   : crease
                    --   sInt = -5..-4: pinky finger above pommel
                    local isCrease = (sInt == 3 or sInt == 0 or sInt == -3)
                    if t <= -2.3 then
                        -- Outer knuckle silhouette contour (dark ink edge)
                        out:drawPixel(gx, gy, cInk)
                    elseif s >= 3.6 and t >= 0.0 and t <= 2.6 then
                        -- Thumb wrapping around the wrist side right behind the crossguard
                        out:drawPixel(gx, gy, (t >= 1.5) and cLeatherM or cLeatherH)
                    elseif t >= 1.8 then
                        -- Back-of-hand / gauntlet steel plate meeting the wrist cuff
                        out:drawPixel(gx, gy, (t >= 2.6) and cSteelD or (isCrease and cSteelM or cSteelH))
                    elseif t >= 0.3 then
                        -- Iron knuckle ridge across the back of the fingers
                        out:drawPixel(gx, gy, isCrease and cLeatherD or cSteelM)
                    elseif t >= -1.2 then
                        -- Curled leather fingers wrapping over the handle center
                        out:drawPixel(gx, gy, isCrease and cInk or cLeatherH)
                    else
                        -- Finger tips tucking into the palm shadow
                        out:drawPixel(gx, gy, isCrease and cInk or cLeatherD)
                    end
                end
            end
        end
    end

    return out
end

-- Create 256x256 master sprite with 4 layers
local spr = Sprite(256, 256, ColorMode.RGB)
spr.filename = outDir .. "/master256.aseprite"

local lWepBack = spr.layers[1]
lWepBack.name = "weaponBack"
local lBody = spr:newLayer()
lBody.name = "body"
local lWepFront = spr:newLayer()
lWepFront.name = "weaponFront"
local lHandFront = spr:newLayer()
lHandFront.name = "handFront"

for i = 2, 13 do
    spr:newEmptyFrame()
end

for i = 1, 13 do
    spr.frames[i].duration = durations[i] / 1000.0
    local fn = string.format("%02d.png", i - 1)
    local bodyImg = Image{ fromFile = srcBodyDir .. "/" .. fn }
    spr:newCel(lBody, i, bodyImg, Point(0, 0))

    local a = anatomy[i]
    local wbImg = Image(256, 256, ColorMode.RGB)
    local wfImg = Image(256, 256, ColorMode.RGB)
    local hfImg = Image(256, 256, ColorMode.RGB)

    if a.vis then
        local rotWep = renderRotatedWeapon(a.ang, a.pa[1], a.pa[2])
        if a.layer == "weaponBack" then
            wbImg = rotWep
        else
            wfImg = rotWep
        end
        hfImg = renderAnatomicalHandFront(bodyImg, rotWep, a)
    end

    spr:newCel(lWepBack, i, wbImg, Point(0, 0))
    spr:newCel(lWepFront, i, wfImg, Point(0, 0))
    spr:newCel(lHandFront, i, hfImg, Point(0, 0))

    -- Export individual layer PNGs
    wbImg:saveAs(outDir .. "/layers/weaponBack/" .. fn)
    bodyImg:saveAs(outDir .. "/layers/body/" .. fn)
    wfImg:saveAs(outDir .. "/layers/weaponFront/" .. fn)
    hfImg:saveAs(outDir .. "/layers/handFront/" .. fn)

    -- Composite 256 frame
    local comp = Image(256, 256, ColorMode.RGB)
    comp:drawImage(wbImg, Point(0, 0))
    comp:drawImage(bodyImg, Point(0, 0))
    comp:drawImage(wfImg, Point(0, 0))
    comp:drawImage(hfImg, Point(0, 0))
    comp:saveAs(outDir .. "/" .. fn)
    comp:saveAs(outDir .. "/frames/" .. fn)

    -- Copy preserved native 128 frame (body-only native crop [64,64])
    local natImg = Image{ fromFile = srcNativeDir .. "/" .. fn }
    natImg:saveAs(outDir .. "/native/" .. fn)
end

spr:saveCopyAs(outDir .. "/master256.aseprite")
spr:saveCopyAs(outDir .. "/source/composite.aseprite")

-- Also save bodyMaster256, handMaster256, and nativeMaster128 inside outDir and outDir/source
local bodySpr = Sprite(256, 256, ColorMode.RGB)
bodySpr.layers[1].name = "body"
for i = 2, 13 do bodySpr:newEmptyFrame() end
for i = 1, 13 do
    bodySpr.frames[i].duration = durations[i] / 1000.0
    local fn = string.format("%02d.png", i - 1)
    bodySpr:newCel(bodySpr.layers[1], i, Image{ fromFile = outDir .. "/layers/body/" .. fn }, Point(0, 0))
end
bodySpr:saveCopyAs(outDir .. "/bodyMaster256.aseprite")
bodySpr:saveCopyAs(outDir .. "/source/body.aseprite")
bodySpr:close()

local handSpr = Sprite(256, 256, ColorMode.RGB)
handSpr.layers[1].name = "handFront"
for i = 2, 13 do handSpr:newEmptyFrame() end
for i = 1, 13 do
    handSpr.frames[i].duration = durations[i] / 1000.0
    local fn = string.format("%02d.png", i - 1)
    handSpr:newCel(handSpr.layers[1], i, Image{ fromFile = outDir .. "/layers/handFront/" .. fn }, Point(0, 0))
end
handSpr:saveCopyAs(outDir .. "/handMaster256.aseprite")
handSpr:saveCopyAs(outDir .. "/source/hand.aseprite")
handSpr:close()

local natSpr = Sprite(128, 128, ColorMode.RGB)
natSpr.layers[1].name = "body"
for i = 2, 13 do natSpr:newEmptyFrame() end
for i = 1, 13 do
    natSpr.frames[i].duration = durations[i] / 1000.0
    local fn = string.format("%02d.png", i - 1)
    natSpr:newCel(natSpr.layers[1], i, Image{ fromFile = outDir .. "/native/" .. fn }, Point(0, 0))
end
natSpr:saveCopyAs(outDir .. "/nativeMaster128.aseprite")
natSpr:saveCopyAs(outDir .. "/source/native.aseprite")
natSpr:close()

-- Build native-strip.png (13*128 x 128) and composite-strip.png (13*256 x 256)
local natStrip = Image(13 * 128, 128, ColorMode.RGB)
local compStrip = Image(13 * 256, 256, ColorMode.RGB)
for i = 1, 13 do
    local fn = string.format("%02d.png", i - 1)
    natStrip:drawImage(Image{ fromFile = outDir .. "/native/" .. fn }, Point((i - 1) * 128, 0))
    compStrip:drawImage(Image{ fromFile = outDir .. "/" .. fn }, Point((i - 1) * 256, 0))
end
natStrip:saveAs(outDir .. "/native-strip.png")
compStrip:saveAs(outDir .. "/composite-strip.png")

spr:close()
print("SUCCESS_FRONT_R_SWORD_QA5_REPAIR1")
