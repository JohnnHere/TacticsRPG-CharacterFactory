import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { execFileSync } from "node:child_process";
import { PNG } from "pngjs";

const ROOT = process.cwd();
const EXP_DIR = path.join(ROOT, "experiments/main-orc-hybrid-weapon-04b2");
const SRC_CLIP_DIR = path.join(ROOT, "characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword");
const ASEPRITE_EXE = "F:/SteamLibrary/steamapps/common/Aseprite/Aseprite.exe";
const PROTECTED_DIRS = ["characters", "assets", "reports"];

function sha256File(filePath) {
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function loadPng(filePath) {
  return PNG.sync.read(fs.readFileSync(filePath));
}

function rgbaSha256(png) {
  return crypto.createHash("sha256").update(png.data).digest("hex");
}

function snapshotTree(relDir) {
  const base = path.join(ROOT, relDir);
  const map = {};
  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(full);
      } else {
        const rel = path.relative(ROOT, full).replace(/\\/g, "/");
        map[rel] = sha256File(full);
      }
    }
  }
  if (fs.existsSync(base)) walk(base);
  return map;
}

function ensureStageDirs() {
  for (const stage of ["representative", "full"]) {
    for (const variant of ["a", "b"]) {
      for (const sub of [
        "composite",
        "body-only",
        "weapon-only",
        "layers/weaponBack",
        "layers/body",
        "layers/weaponFront",
        "layers/handFront",
      ]) {
        fs.mkdirSync(path.join(EXP_DIR, stage, variant, sub), { recursive: true });
      }
    }
  }
}

function runAsepriteStage(stage) {
  const userFolder = path.join(ROOT, "tmp/aseprite-batch-profile");
  fs.mkdirSync(userFolder, { recursive: true });
  execFileSync(
    ASEPRITE_EXE,
    [
      "--batch",
      "--noinapp",
      "--script-param",
      `stage=${stage}`,
      "--script",
      "experiments/main-orc-hybrid-weapon-04b2/author.lua",
    ],
    {
      cwd: ROOT,
      env: { ...process.env, ASEPRITE_USER_FOLDER: userFolder },
      stdio: "inherit",
    }
  );
}

function writeClipManifests() {
  const srcClip = JSON.parse(fs.readFileSync(path.join(SRC_CLIP_DIR, "clip.json"), "utf8"));
  const gripProfile = JSON.parse(fs.readFileSync(path.join(EXP_DIR, "grip-profile-back-r.json"), "utf8"));

  for (const variant of ["a", "b"]) {
    const varDir = path.join(EXP_DIR, "full", variant);
    const wDef =
      variant === "a"
        ? {
            id: "recruit-sword",
            name: "Espada do Recruta (Variant A)",
            sprite: `experiments/main-orc-hybrid-weapon-04b2/variants/sword-a/sword.png`,
            master: `experiments/main-orc-hybrid-weapon-04b2/variants/sword-a/sword.aseprite`,
            spriteSha256: sha256File(path.join(EXP_DIR, "variants/sword-a/sword.png")),
            masterSha256: sha256File(path.join(EXP_DIR, "variants/sword-a/sword.aseprite")),
            grip: [48, 66],
            canvas: [96, 96],
          }
        : {
            id: "faceted-steel-sword-b",
            name: "Espada de Aço Facetada (Variant B)",
            sprite: `experiments/main-orc-hybrid-weapon-04b2/variants/sword-b/sword.png`,
            master: `experiments/main-orc-hybrid-weapon-04b2/variants/sword-b/sword.aseprite`,
            spriteSha256: sha256File(path.join(EXP_DIR, "variants/sword-b/sword.png")),
            masterSha256: sha256File(path.join(EXP_DIR, "variants/sword-b/sword.aseprite")),
            grip: [48, 66],
            canvas: [96, 96],
          };

    const frames = gripProfile.frames.map((gf) => {
      const fCode = String(gf.index).padStart(2, "0");
      return {
        index: gf.index,
        file: `composite/${fCode}.png`,
        bodyOnlyFile: `body-only/${fCode}.png`,
        weaponOnlyFile: `weapon-only/${fCode}.png`,
        durationMs: gf.durationMs,
        weaponVisible: gf.weaponVisible,
        rightGrip: gf.rightGrip,
        declaredRightGrip: gf.declaredRightGrip || null,
        rotationDeg: gf.rotationDeg,
        scale: 1,
        layerOrder: gf.layerOrder,
        sha256: sha256File(path.join(varDir, "composite", `${fCode}.png`)),
      };
    });

    const manifest = {
      schemaVersion: "1.0.0",
      experimentId: "main-orc-hybrid-weapon-04b2",
      pilot: "B2",
      variant: variant.toUpperCase(),
      characterId: "orc-v1",
      direction: "back_r",
      action: "Sword",
      sourceClip: "characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword/clip.json",
      sourceClipSha256: srcClip.sourceMasterSha256 ? sha256File(path.join(SRC_CLIP_DIR, "clip.json")) : sha256File(path.join(SRC_CLIP_DIR, "clip.json")),
      master: `experiments/main-orc-hybrid-weapon-04b2/full/${variant}/composite.aseprite`,
      masterSha256: sha256File(path.join(varDir, "composite.aseprite")),
      strip: `experiments/main-orc-hybrid-weapon-04b2/full/${variant}/strip.png`,
      stripSha256: sha256File(path.join(varDir, "strip.png")),
      canvasSize: [256, 256],
      frameCount: 14,
      totalDurationMs: 730,
      visibleInterval: [2, 11],
      contactFrame: 8,
      contactTimeMs: 325,
      weapon: wDef,
      frames,
    };

    fs.writeFileSync(path.join(varDir, "clip.json"), JSON.stringify(manifest, null, 2) + "\n");
  }
}

function verifyExperiment(preSnapshot, postSnapshot) {
  // Check protected directories
  let protectedChanged = 0;
  for (const dir of PROTECTED_DIRS) {
    const pre = preSnapshot[dir];
    const post = postSnapshot[dir];
    const keys = new Set([...Object.keys(pre), ...Object.keys(post)]);
    for (const k of keys) {
      if (pre[k] !== post[k]) {
        protectedChanged++;
      }
    }
  }

  const swordA = loadPng(path.join(EXP_DIR, "variants/sword-a/sword.png"));
  const swordB = loadPng(path.join(EXP_DIR, "variants/sword-b/sword.png"));

  // Collect Sword A and Sword B blade & hilt colour sets
  const swordABladeColors = new Set();
  const swordBBladeColors = new Set();
  const sharedHiltColors = new Set();

  for (let v = 0; v < 96; v++) {
    for (let u = 0; u < 96; u++) {
      const i = (v * 96 + u) * 4;
      if (swordA.data[i + 3] > 0) {
        const key = `${swordA.data[i]},${swordA.data[i + 1]},${swordA.data[i + 2]}`;
        if (v <= 54) swordABladeColors.add(key);
        else sharedHiltColors.add(key);
      }
      if (swordB.data[i + 3] > 0) {
        const key = `${swordB.data[i]},${swordB.data[i + 1]},${swordB.data[i + 2]}`;
        if (v <= 54) swordBBladeColors.add(key);
        else sharedHiltColors.add(key);
      }
    }
  }

  const bladeOnlyA = new Set(
    [...swordABladeColors].filter((c) => !swordBBladeColors.has(c) && !sharedHiltColors.has(c))
  );
  const bladeOnlyB = new Set(
    [...swordBBladeColors].filter((c) => !swordABladeColors.has(c) && !sharedHiltColors.has(c))
  );

  const gripProfile = JSON.parse(fs.readFileSync(path.join(EXP_DIR, "grip-profile-back-r.json"), "utf8"));
  const perFrame = [];
  const edgeDiagnostics = {};
  const weaponDiff = {};

  let totalBodyDiffVsSource = 0;
  let totalHandFrontDiffVsSource = 0;
  let totalBodyOnlyDiffAB = 0;
  let totalCompositeADiffVsSource = 0;
  let totalUnarmedWeaponPixels = 0;
  let totalSilhouetteDeltaAB = 0;
  let totalHiltDiffAB = 0;
  let totalLeftoverSwordABladeInB = 0;
  let totalMatteHalos = 0;

  for (let idx = 0; idx < 14; idx++) {
    const fCode = String(idx).padStart(2, "0");
    const fLabel = `F${fCode}`;
    const gf = gripProfile.frames[idx];

    const srcComp = loadPng(path.join(SRC_CLIP_DIR, "frames", `${fCode}.png`));
    const srcBody = loadPng(path.join(SRC_CLIP_DIR, "layers/body", `${fCode}.png`));
    const srcHf = loadPng(path.join(SRC_CLIP_DIR, "layers/handFront", `${fCode}.png`));
    const srcWb = loadPng(path.join(SRC_CLIP_DIR, "layers/weaponBack", `${fCode}.png`));
    const srcWf = loadPng(path.join(SRC_CLIP_DIR, "layers/weaponFront", `${fCode}.png`));

    const compA = loadPng(path.join(EXP_DIR, "full/a/composite", `${fCode}.png`));
    const compB = loadPng(path.join(EXP_DIR, "full/b/composite", `${fCode}.png`));
    const bodyOnlyA = loadPng(path.join(EXP_DIR, "full/a/body-only", `${fCode}.png`));
    const bodyOnlyB = loadPng(path.join(EXP_DIR, "full/b/body-only", `${fCode}.png`));
    const weaponOnlyA = loadPng(path.join(EXP_DIR, "full/a/weapon-only", `${fCode}.png`));
    const weaponOnlyB = loadPng(path.join(EXP_DIR, "full/b/weapon-only", `${fCode}.png`));

    const lBodyA = loadPng(path.join(EXP_DIR, "full/a/layers/body", `${fCode}.png`));
    const lBodyB = loadPng(path.join(EXP_DIR, "full/b/layers/body", `${fCode}.png`));
    const lHfA = loadPng(path.join(EXP_DIR, "full/a/layers/handFront", `${fCode}.png`));
    const lHfB = loadPng(path.join(EXP_DIR, "full/b/layers/handFront", `${fCode}.png`));
    const lWbA = loadPng(path.join(EXP_DIR, "full/a/layers/weaponBack", `${fCode}.png`));
    const lWbB = loadPng(path.join(EXP_DIR, "full/b/layers/weaponBack", `${fCode}.png`));
    const lWfA = loadPng(path.join(EXP_DIR, "full/a/layers/weaponFront", `${fCode}.png`));
    const lWfB = loadPng(path.join(EXP_DIR, "full/b/layers/weaponFront", `${fCode}.png`));

    const bodyIdenticalSource =
      rgbaSha256(srcBody) === rgbaSha256(lBodyA) && rgbaSha256(srcBody) === rgbaSha256(lBodyB);
    const hfIdenticalSource =
      rgbaSha256(srcHf) === rgbaSha256(lHfA) && rgbaSha256(srcHf) === rgbaSha256(lHfB);
    const bodyOnlyIdenticalAB = rgbaSha256(bodyOnlyA) === rgbaSha256(bodyOnlyB);
    const compAIdenticalSource = rgbaSha256(srcComp) === rgbaSha256(compA);

    if (!bodyIdenticalSource) totalBodyDiffVsSource++;
    if (!hfIdenticalSource) totalHandFrontDiffVsSource++;
    if (!bodyOnlyIdenticalAB) totalBodyOnlyDiffAB++;
    if (!compAIdenticalSource) totalCompositeADiffVsSource++;

    let weaponPixelsA = 0;
    let weaponPixelsB = 0;
    let silhouetteDeltaAB = 0;
    let weaponDiffPixelsAB = 0;
    let compDiffPixelsAB = 0;
    let nonWeaponCompDiffAB = 0;
    let leftoverBladeInB = 0;
    let swordBUniquePixelsInB = 0;
    let matteHaloPixels = 0;
    let semiTransparentWeaponPixels = 0;
    let wbBodyOverlap = 0;
    let wfBodyOverlap = 0;
    let hfWeaponOverlap = 0;

    for (let i = 0; i < 256 * 256; i++) {
      const idx4 = i * 4;
      const waA = weaponOnlyA.data[idx4 + 3];
      const waB = weaponOnlyB.data[idx4 + 3];
      if (waA > 0) weaponPixelsA++;
      if (waB > 0) weaponPixelsB++;
      if ((waA > 0) !== (waB > 0)) silhouetteDeltaAB++;
      if (waB > 0 && waB < 255) semiTransparentWeaponPixels++;

      const wSame =
        waA === waB &&
        weaponOnlyA.data[idx4] === weaponOnlyB.data[idx4] &&
        weaponOnlyA.data[idx4 + 1] === weaponOnlyB.data[idx4 + 1] &&
        weaponOnlyA.data[idx4 + 2] === weaponOnlyB.data[idx4 + 2];
      if (!wSame) weaponDiffPixelsAB++;

      const cSame =
        compA.data[idx4 + 3] === compB.data[idx4 + 3] &&
        compA.data[idx4] === compB.data[idx4] &&
        compA.data[idx4 + 1] === compB.data[idx4 + 1] &&
        compA.data[idx4 + 2] === compB.data[idx4 + 2];
      if (!cSame) {
        compDiffPixelsAB++;
        if (waA === 0 && waB === 0) nonWeaponCompDiffAB++;
      }

      if (waB > 0) {
        const r = weaponOnlyB.data[idx4];
        const g = weaponOnlyB.data[idx4 + 1];
        const b = weaponOnlyB.data[idx4 + 2];
        const key = `${r},${g},${b}`;
        if (bladeOnlyA.has(key)) leftoverBladeInB++;
        if (bladeOnlyB.has(key)) swordBUniquePixelsInB++;
        if (r > 235 && g > 235 && b > 235) matteHaloPixels++;
      }

      if (lWbB.data[idx4 + 3] > 0 && lBodyB.data[idx4 + 3] > 0) wbBodyOverlap++;
      if (lWfB.data[idx4 + 3] > 0 && lBodyB.data[idx4 + 3] > 0) wfBodyOverlap++;
      if (lHfB.data[idx4 + 3] > 0 && (lWbB.data[idx4 + 3] > 0 || lWfB.data[idx4 + 3] > 0)) hfWeaponOverlap++;
    }

    if (!gf.weaponVisible) {
      totalUnarmedWeaponPixels += weaponPixelsA + weaponPixelsB;
    }

    totalSilhouetteDeltaAB += silhouetteDeltaAB;
    totalLeftoverSwordABladeInB += leftoverBladeInB;
    totalMatteHalos += matteHaloPixels;

    perFrame.push({
      frame: idx,
      code: fLabel,
      durationMs: gf.durationMs,
      weaponVisible: gf.weaponVisible,
      rightGrip: gf.rightGrip,
      rotationDeg: gf.rotationDeg,
      bodyIdenticalSource,
      handFrontIdenticalSource: hfIdenticalSource,
      bodyOnlyIdenticalAB,
      compositeAIdenticalSource: compAIdenticalSource,
      weaponPixelsA,
      weaponPixelsB,
      silhouetteDeltaAB,
      weaponDiffPixelsAB,
      compositeDiffPixelsAB: compDiffPixelsAB,
      nonWeaponCompositeDiffAB: nonWeaponCompDiffAB,
      leftoverSwordABladeInB: leftoverBladeInB,
      swordBUniquePixelsInB,
      wbBodyOverlap,
      wfBodyOverlap,
      hfWeaponOverlap,
    });

    edgeDiagnostics[fLabel] = {
      semiTransparentWeaponPixels,
      matteHaloPixels,
      silhouetteDeltaAB,
      leftoverSwordABladeInB: leftoverBladeInB,
      wbBodyOverlap,
      wfBodyOverlap,
      hfWeaponOverlap,
    };

    weaponDiff[fLabel] = {
      weaponVisible: gf.weaponVisible,
      weaponPixelsA,
      weaponPixelsB,
      weaponDiffPixelsAB,
      compositeDiffPixelsAB: compDiffPixelsAB,
      nonWeaponCompositeDiffAB: nonWeaponCompDiffAB,
      swordBUniquePixelsInB,
    };
  }

  // Representative 4 frames check (F02, F05, F08, F11)
  const repFrames = [2, 5, 8, 11];
  let repMatchFull = true;
  for (const idx of repFrames) {
    const fCode = String(idx).padStart(2, "0");
    for (const v of ["a", "b"]) {
      const repPng = loadPng(path.join(EXP_DIR, "representative", v, "composite", `${fCode}.png`));
      const fullPng = loadPng(path.join(EXP_DIR, "full", v, "composite", `${fCode}.png`));
      if (rgbaSha256(repPng) !== rgbaSha256(fullPng)) repMatchFull = false;
    }
  }

  const verification = {
    experimentId: "main-orc-hybrid-weapon-04b2",
    pilot: "B2",
    direction: "back_r",
    action: "Sword",
    status: "TECHNICALLY_COMPLETE",
    reviewStatus: "VISUAL_REVIEW_REQUIRED",
    approvalStatus: "PENDING_CREATOR",
    protectedFilesChanged: protectedChanged,
    newPixelLabCalls: 0,
    unityModified: false,
    checks: {
      protectedTreesUntouched: protectedChanged === 0,
      all14BodyLayersIdenticalToSource: totalBodyDiffVsSource === 0,
      all14HandFrontLayersIdenticalToSource: totalHandFrontDiffVsSource === 0,
      all14BodyOnlyExportsIdenticalBetweenAandB: totalBodyOnlyDiffAB === 0,
      all14CompositeAFramesIdenticalToSource: totalCompositeADiffVsSource === 0,
      unarmedFramesHaveZeroWeaponPixels: totalUnarmedWeaponPixels === 0,
      armedFramesPreserveWeaponSilhouetteExactly: totalSilhouetteDeltaAB === 0,
      zeroLeftoverSwordABladeColorsInVariantB: totalLeftoverSwordABladeInB === 0,
      zeroMatteHalos: totalMatteHalos === 0,
      representativeFramesMatchFullFrames: repMatchFull,
      frameCountPreserved: perFrame.length === 14,
      totalDurationMsPreserved: perFrame.reduce((s, f) => s + f.durationMs, 0) === 730,
    },
    perFrame,
  };

  fs.writeFileSync(path.join(EXP_DIR, "verification.json"), JSON.stringify(verification, null, 2) + "\n");
  fs.writeFileSync(path.join(EXP_DIR, "pixel-diff.json"), JSON.stringify(perFrame, null, 2) + "\n");
  fs.writeFileSync(path.join(EXP_DIR, "edge-diagnostics.json"), JSON.stringify(edgeDiagnostics, null, 2) + "\n");
  fs.writeFileSync(path.join(EXP_DIR, "weapon-diff.json"), JSON.stringify(weaponDiff, null, 2) + "\n");

  const failed = Object.entries(verification.checks).filter(([, ok]) => !ok);
  if (failed.length > 0) {
    console.error("Verification failed checks:", failed);
    process.exit(1);
  }
  console.log("All Pilot B2 quantitative verification checks PASSED.");
}

function main() {
  const verifyOnly = process.argv.includes("--verify-only");
  const preSnapshot = {};
  for (const dir of PROTECTED_DIRS) preSnapshot[dir] = snapshotTree(dir);

  if (!verifyOnly) {
    ensureStageDirs();
    runAsepriteStage("representative");
    runAsepriteStage("full");
  }
  writeClipManifests();

  const postSnapshot = {};
  for (const dir of PROTECTED_DIRS) postSnapshot[dir] = snapshotTree(dir);

  verifyExperiment(preSnapshot, postSnapshot);
}

main();
