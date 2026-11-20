import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { PNG } from "pngjs";

const ROOT = process.cwd();
const EXP_DIR = path.join(ROOT, "experiments/main-orc-hybrid-weapon-04b2");
const SRC_VARIANTS = path.join(ROOT, "experiments/main-orc-hybrid-weapon-04b/variants");
const CLIP_PATH = path.join(ROOT, "characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword/clip.json");
const LAYERS_DIR = path.join(ROOT, "characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword/layers");
const SWORD_A_PNG = path.join(EXP_DIR, "variants/sword-a/sword.png");

function sha256File(filePath) {
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function copyVariants() {
  for (const variant of ["sword-a", "sword-b"]) {
    const srcDir = path.join(SRC_VARIANTS, variant);
    const dstDir = path.join(EXP_DIR, "variants", variant);
    fs.mkdirSync(dstDir, { recursive: true });
    for (const file of fs.readdirSync(srcDir)) {
      fs.copyFileSync(path.join(srcDir, file), path.join(dstDir, file));
    }
  }
}

function loadPng(filePath) {
  return PNG.sync.read(fs.readFileSync(filePath));
}

function fitBackRGrip() {
  copyVariants();

  const clip = JSON.parse(fs.readFileSync(CLIP_PATH, "utf8"));
  const swordA = loadPng(SWORD_A_PNG);
  const srcPts = [];
  for (let v = 0; v < swordA.height; v++) {
    for (let u = 0; u < swordA.width; u++) {
      const idx = (v * swordA.width + u) * 4;
      if (swordA.data[idx + 3] > 0) {
        srcPts.push({
          u,
          v,
          r: swordA.data[idx],
          g: swordA.data[idx + 1],
          b: swordA.data[idx + 2],
        });
      }
    }
  }

  const gripU = 48;
  const gripV = 66;
  const meanDu = srcPts.reduce((s, p) => s + (p.u - gripU), 0) / srcPts.length;
  const meanDv = srcPts.reduce((s, p) => s + (p.v - gripV), 0) / srcPts.length;

  const fits = {};
  const gripProfileFrames = [];

  for (const f of clip.frames) {
    const idx = f.index;
    const fName = `F${String(idx).padStart(2, "0")}`;
    if (!f.weaponVisible) {
      gripProfileFrames.push({
        index: idx,
        file: `${String(idx).padStart(2, "0")}.png`,
        role: f.role,
        durationMs: f.durationMs,
        weaponVisible: false,
        rightGrip: null,
        rotationDeg: null,
        scale: 1,
        layerOrder: ["body"],
      });
      continue;
    }

    const wb = loadPng(path.join(LAYERS_DIR, "weaponBack", `${String(idx).padStart(2, "0")}.png`));
    const wf = loadPng(path.join(LAYERS_DIR, "weaponFront", `${String(idx).padStart(2, "0")}.png`));

    const wMap = new Map();
    let wbCount = 0;
    let wfCount = 0;
    for (let y = 0; y < 256; y++) {
      for (let x = 0; x < 256; x++) {
        const i = (y * 256 + x) * 4;
        if (wb.data[i + 3] > 0) {
          wbCount++;
          wMap.set(`${x},${y}`, { x, y, r: wb.data[i], g: wb.data[i + 1], b: wb.data[i + 2], layer: "weaponBack" });
        }
        if (wf.data[i + 3] > 0) {
          wfCount++;
          wMap.set(`${x},${y}`, { x, y, r: wf.data[i], g: wf.data[i + 1], b: wf.data[i + 2], layer: "weaponFront" });
        }
      }
    }
    const wPixels = Array.from(wMap.values());
    const meanX = wPixels.reduce((s, p) => s + p.x, 0) / wPixels.length;
    const meanY = wPixels.reduce((s, p) => s + p.y, 0) / wPixels.length;

    const theta = (f.rotationDeg * Math.PI) / 180;
    const c = Math.cos(theta);
    const s = Math.sin(theta);

    const estGx = meanX - (meanDu * c - meanDv * s);
    const estGy = meanY - (meanDu * s + meanDv * c);

    function scorePivot(gx, gy) {
      let validBladeHilt = 0;
      let colorSad = 0;
      for (const p of wPixels) {
        const dx = p.x - gx;
        const dy = p.y - gy;
        const u = Math.round(dx * c + dy * s + gripU);
        const v = Math.round(-dx * s + dy * c + gripV);
        if (u >= 0 && u < 96 && v >= 0 && v < 96) {
          const si = (v * 96 + u) * 4;
          if (swordA.data[si + 3] > 0) {
            validBladeHilt++;
            colorSad +=
              Math.abs(p.r - swordA.data[si]) +
              Math.abs(p.g - swordA.data[si + 1]) +
              Math.abs(p.b - swordA.data[si + 2]);
          } else {
            colorSad += 400;
          }
        } else {
          colorSad += 800;
        }
      }
      return { validBladeHilt, colorSad };
    }

    const declaredRaw = f.rightGrip;
    const declaredInt = [Math.round(declaredRaw[0]), Math.round(declaredRaw[1])];
    const declaredScore = scorePivot(declaredInt[0], declaredInt[1]);

    let best = null;
    for (let gx = Math.round(estGx) - 6; gx <= Math.round(estGx) + 6; gx++) {
      for (let gy = Math.round(estGy) - 6; gy <= Math.round(estGy) + 6; gy++) {
        const sc = scorePivot(gx, gy);
        if (
          !best ||
          sc.validBladeHilt > best.validBladeHilt ||
          (sc.validBladeHilt === best.validBladeHilt && sc.colorSad < best.colorSad)
        ) {
          best = { gx, gy, ...sc };
        }
      }
    }

    // Use declared integer pivot when it matches or ties best validBladeHilt within 1px, preserving source clip metadata
    const usePivot =
      Math.abs(declaredInt[0] - best.gx) <= 1 && Math.abs(declaredInt[1] - best.gy) <= 1
        ? declaredInt
        : [best.gx, best.gy];

    fits[fName] = {
      frame: idx,
      role: f.role,
      durationMs: f.durationMs,
      rotationDeg: f.rotationDeg,
      declaredRightGrip: declaredRaw,
      declaredIntegerGrip: declaredInt,
      declaredValidWeaponPixels: declaredScore.validBladeHilt,
      declaredColorSad: declaredScore.colorSad,
      centroidEstimate: [Number(estGx.toFixed(2)), Number(estGy.toFixed(2))],
      bestFitGrip: [best.gx, best.gy],
      bestFitValidWeaponPixels: best.validBladeHilt,
      bestFitColorSad: best.colorSad,
      selectedRightGrip: usePivot,
      totalWeaponPixels: wPixels.length,
      weaponBackPixels: wbCount,
      weaponFrontPixels: wfCount,
    };

    gripProfileFrames.push({
      index: idx,
      file: `${String(idx).padStart(2, "0")}.png`,
      role: f.role,
      durationMs: f.durationMs,
      weaponVisible: true,
      rightGrip: usePivot,
      declaredRightGrip: declaredRaw,
      rotationDeg: f.rotationDeg,
      scale: 1,
      weaponBackPixels: wbCount,
      weaponFrontPixels: wfCount,
      layerOrder: ["weaponBack", "body", "weaponFront", "handFront"],
    });
  }

  fs.writeFileSync(path.join(EXP_DIR, "grip-pivot-fit.json"), JSON.stringify(fits, null, 2) + "\n");

  const gripProfile = {
    schemaVersion: "1.0.0",
    experimentId: "main-orc-hybrid-weapon-04b2",
    pilot: "B2",
    direction: "back_r",
    action: "Sword",
    family: "one-handed-sword",
    sourceClip: "characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword/clip.json",
    sourceClipSha256: sha256File(CLIP_PATH),
    sourceMaster: "characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword/source/composite.aseprite",
    sourceMasterSha256: sha256File(
      path.join(ROOT, "characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword/source/composite.aseprite")
    ),
    canvasSize: [256, 256],
    weaponCanvasSize: [96, 96],
    weaponGripAnchor: [48, 66],
    bladeRows: [7, 54],
    bladeGuardSeamRow: 55,
    sharedHiltRows: [55, 79],
    frameCount: 14,
    totalDurationMs: 730,
    visibleInterval: [2, 11],
    contactFrame: 8,
    contactTimeMs: 325,
    representativeFrames: [2, 5, 8, 11],
    representativeRoles: {
      F02: "establish-grip (preparation)",
      F05: "apex-hold (weapon elevation)",
      F08: "contact (impact)",
      F11: "settle-grip (recovery)",
    },
    layerOrder: ["weaponBack", "body", "weaponFront", "handFront"],
    rearDepthConvention: {
      summary:
        "In back_r, weaponBack holds the hilt/pommel behind the torso/arm (and in F06 the leather grip), while weaponFront holds 100% of the blade and crossguard in front of the body, and handFront overlays the gripping gauntlet fingers over the handle.",
      bladeInWeaponBackPixels: 0,
      bladeInWeaponFrontRatio: 1.0,
    },
    frames: gripProfileFrames,
  };

  fs.writeFileSync(path.join(EXP_DIR, "grip-profile-back-r.json"), JSON.stringify(gripProfile, null, 2) + "\n");
  console.log("Wrote grip-pivot-fit.json and grip-profile-back-r.json");
}

fitBackRGrip();
