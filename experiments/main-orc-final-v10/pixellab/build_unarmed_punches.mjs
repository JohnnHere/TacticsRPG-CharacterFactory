import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const { PNG } = createRequire("c:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory/package.json")("pngjs");

const ROOT = "c:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory";
const EXP = `${ROOT}/experiments/main-orc-final-v10/pixellab`;
const AUDIT = "C:/Users/João Orlando/.gemini/antigravity/brain/5fe480f6-d661-411c-b120-c9742e395c32/scratch/audit";

const uploads = JSON.parse(fs.readFileSync(path.join(EXP, "unarmed_uploads.json"), "utf8"));
const nwSwordReq = JSON.parse(fs.readFileSync(path.join(EXP, "sword_nw_request.json"), "utf8"));

const kpFrontR = [
  {"x":0.5754,"y":0.1664,"label":"NOSE","z_index":0},
  {"x":0.5166,"y":0.2737,"label":"NECK","z_index":-1},
  {"x":0.3562,"y":0.2726,"label":"RIGHT SHOULDER","z_index":-1},
  {"x":0.2847,"y":0.4434,"label":"RIGHT ELBOW","z_index":0},
  {"x":0.2754,"y":0.6072,"label":"RIGHT ARM","z_index":0},
  {"x":0.6770,"y":0.2749,"label":"LEFT SHOULDER","z_index":-1},
  {"x":0.7047,"y":0.4480,"label":"LEFT ELBOW","z_index":0},
  {"x":0.7647,"y":0.6049,"label":"LEFT ARM","z_index":0},
  {"x":0.4485,"y":0.5588,"label":"RIGHT HIP","z_index":-1},
  {"x":0.3908,"y":0.7596,"label":"RIGHT KNEE","z_index":0},
  {"x":0.3470,"y":0.9142,"label":"RIGHT LEG","z_index":-1},
  {"x":0.5939,"y":0.5634,"label":"LEFT HIP","z_index":-1},
  {"x":0.6539,"y":0.7526,"label":"LEFT KNEE","z_index":0},
  {"x":0.6424,"y":0.9049,"label":"LEFT LEG","z_index":-1},
  {"x":0.5454,"y":0.1457,"label":"RIGHT EYE","z_index":-1},
  {"x":0.5916,"y":0.1433,"label":"LEFT EYE","z_index":-1},
  {"x":0.4924,"y":0.1387,"label":"RIGHT EAR","z_index":-2},
  {"x":0.5685,"y":0.1318,"label":"LEFT EAR","z_index":-2},
];

const kpFrontL = [
  {"x":0.4208,"y":0.1664,"label":"NOSE","z_index":0},
  {"x":0.4797,"y":0.2737,"label":"NECK","z_index":-1},
  {"x":0.3193,"y":0.2749,"label":"RIGHT SHOULDER","z_index":-1},
  {"x":0.2916,"y":0.4480,"label":"RIGHT ELBOW","z_index":0},
  {"x":0.2316,"y":0.6026,"label":"RIGHT ARM","z_index":0},
  {"x":0.6401,"y":0.2726,"label":"LEFT SHOULDER","z_index":-1},
  {"x":0.7116,"y":0.4434,"label":"LEFT ELBOW","z_index":0},
  {"x":0.7208,"y":0.6072,"label":"LEFT ARM","z_index":0},
  {"x":0.4000,"y":0.5634,"label":"RIGHT HIP","z_index":-1},
  {"x":0.3424,"y":0.7526,"label":"RIGHT KNEE","z_index":0},
  {"x":0.3539,"y":0.9049,"label":"RIGHT LEG","z_index":-1},
  {"x":0.5478,"y":0.5611,"label":"LEFT HIP","z_index":-1},
  {"x":0.6031,"y":0.7596,"label":"LEFT KNEE","z_index":0},
  {"x":0.6493,"y":0.9142,"label":"LEFT LEG","z_index":-1},
  {"x":0.4047,"y":0.1433,"label":"RIGHT EYE","z_index":-1},
  {"x":0.4508,"y":0.1457,"label":"LEFT EYE","z_index":-1},
  {"x":0.4254,"y":0.1318,"label":"RIGHT EAR","z_index":-2},
  {"x":0.5039,"y":0.1387,"label":"LEFT EAR","z_index":-2},
];

const kpBackL = nwSwordReq.first_frame_keypoints;

function poseBuilder(firstKp) {
  const base = Object.fromEntries(firstKp.map(j => [j.label, j]));
  const labels = firstKp.map(j => j.label);
  return ({ dxHead = 0, dyHead = 0, rSh, rEl, rWr, lSh, lEl, lWr, rHip, rKn, lHip, lKn }) => {
    const pts = {};
    for (const k of ["NOSE", "NECK", "RIGHT EYE", "LEFT EYE", "RIGHT EAR", "LEFT EAR"]) {
      pts[k] = {
        label: k,
        x: Number((base[k].x + dxHead).toFixed(5)),
        y: Number((base[k].y + dyHead).toFixed(5)),
        z_index: base[k].z_index,
      };
    }
    const setArm = (lbl, val) => {
      if (!val) { pts[lbl] = { ...base[lbl] }; return; }
      pts[lbl] = { label: lbl, x: Number(val[0].toFixed(5)), y: Number(val[1].toFixed(5)), z_index: val[2], depth: val[3] };
    };
    setArm("RIGHT SHOULDER", rSh); setArm("RIGHT ELBOW", rEl); setArm("RIGHT ARM", rWr);
    setArm("LEFT SHOULDER",  lSh); setArm("LEFT ELBOW",  lEl); setArm("LEFT ARM",  lWr);
    pts["RIGHT HIP"]  = rHip ? { label: "RIGHT HIP",  x: Number(rHip[0].toFixed(5)), y: Number(rHip[1].toFixed(5)), z_index: base["RIGHT HIP"].z_index } : { ...base["RIGHT HIP"] };
    pts["RIGHT KNEE"] = rKn  ? { label: "RIGHT KNEE", x: Number(rKn[0].toFixed(5)),  y: Number(rKn[1].toFixed(5)),  z_index: base["RIGHT KNEE"].z_index } : { ...base["RIGHT KNEE"] };
    pts["RIGHT LEG"]  = { ...base["RIGHT LEG"] };
    pts["LEFT HIP"]   = lHip ? { label: "LEFT HIP",   x: Number(lHip[0].toFixed(5)),  y: Number(lHip[1].toFixed(5)),  z_index: base["LEFT HIP"].z_index } : { ...base["LEFT HIP"] };
    pts["LEFT KNEE"]  = lKn  ? { label: "LEFT KNEE",  x: Number(lKn[0].toFixed(5)),   y: Number(lKn[1].toFixed(5)),   z_index: base["LEFT KNEE"].z_index } : { ...base["LEFT KNEE"] };
    pts["LEFT LEG"]   = { ...base["LEFT LEG"] };
    return labels.map(l => pts[l]);
  };
}

// 1. front_r (SE): Heavy RIGHT-HAND cross haymaker punch toward South-East!
// Note: in front_r, character's anatomical RIGHT arm is on screen-LEFT (x=0.356), punching across toward SE (x=0.72..0.82)!
const makeFR = poseBuilder(kpFrontR);
const posesFR = [
  // P01 -> F01 heavy coil back (cock right fist back-up to x=0.20, y=0.44; left guard hand raised slightly)
  makeFR({ dxHead: -0.014, dyHead: 0.006,
    rSh: [0.335, 0.278, 0, 138], rEl: [0.215, 0.395, 1, 144], rWr: [0.210, 0.485, 2, 148],
    lSh: [0.665, 0.276, -1, 132], lEl: [0.720, 0.425, 0, 130], lWr: [0.735, 0.515, 1, 126] }),
  // P02 -> F02 PUNCH IMPACT! Right shoulder rotates forward, right fist drives powerfully into SE (x=0.80, y=0.45)!
  makeFR({ dxHead: 0.032, dyHead: 0.016,
    rSh: [0.435, 0.282, 2, 118], rEl: [0.625, 0.365, 3, 108], rWr: [0.805, 0.445, 4, 96],
    lSh: [0.635, 0.284, -2, 144], lEl: [0.660, 0.450, -2, 148], lWr: [0.695, 0.575, -2, 150],
    rHip: [0.468, 0.564], rKn: [0.405, 0.764], lHip: [0.610, 0.568], lKn: [0.668, 0.758] }),
  // P03 -> F03 Follow-through recoil (fist slightly lower/retracting x=0.72, y=0.49)
  makeFR({ dxHead: 0.020, dyHead: 0.014,
    rSh: [0.405, 0.280, 2, 122], rEl: [0.555, 0.395, 3, 114], rWr: [0.715, 0.488, 4, 104],
    lSh: [0.650, 0.280, -2, 140], lEl: [0.682, 0.450, -1, 142], lWr: [0.728, 0.590, -1, 144],
    rHip: [0.458, 0.562], rKn: [0.398, 0.762], lHip: [0.602, 0.566], lKn: [0.660, 0.755] }),
  // P04 -> F04 Settle guard back to Idle
  makeFR({ dxHead: 0.004, dyHead: 0.002,
    rSh: [0.362, 0.274, 0, 134], rEl: [0.298, 0.440, 1, 134], rWr: [0.305, 0.585, 1, 132],
    lSh: [0.674, 0.275, -1, 134], lEl: [0.702, 0.448, 0, 134], lWr: [0.758, 0.602, 0, 134] }),
];

// 2. front_l (SW): Heavy LEFT-HAND cross haymaker punch toward South-West (asymmetric 4-view warrior punch)!
// Note: in front_l, character's anatomical LEFT arm is on screen-RIGHT (x=0.640), punching across toward SW (x=0.195)!
const makeFL = poseBuilder(kpFrontL);
const posesFL = [
  // P01 -> F01 heavy coil back (cock screen-right arm back to x=0.785)
  makeFL({ dxHead: 0.014, dyHead: 0.006,
    lSh: [0.662, 0.278, 0, 138], lEl: [0.782, 0.395, 1, 144], lWr: [0.788, 0.485, 2, 148],
    rSh: [0.332, 0.276, -1, 132], rEl: [0.276, 0.425, 0, 130], rWr: [0.262, 0.515, 1, 126] }),
  // P02 -> F02 PUNCH IMPACT into SW (x=0.195, y=0.445)!
  makeFL({ dxHead: -0.032, dyHead: 0.016,
    lSh: [0.562, 0.282, 2, 118], lEl: [0.372, 0.365, 3, 108], lWr: [0.195, 0.445, 4, 96],
    rSh: [0.362, 0.284, -2, 144], rEl: [0.336, 0.450, -2, 148], rWr: [0.302, 0.575, -2, 150],
    lHip: [0.528, 0.564], lKn: [0.590, 0.764], rHip: [0.386, 0.568], rKn: [0.328, 0.758] }),
  // P03 -> F03 Follow-through recoil (x=0.285, y=0.488)
  makeFL({ dxHead: -0.020, dyHead: 0.014,
    lSh: [0.592, 0.280, 2, 122], lEl: [0.442, 0.395, 3, 114], lWr: [0.285, 0.488, 4, 104],
    rSh: [0.346, 0.280, -2, 140], rEl: [0.314, 0.450, -1, 142], rWr: [0.268, 0.590, -1, 144],
    lHip: [0.538, 0.562], lKn: [0.598, 0.762], rHip: [0.394, 0.566], rKn: [0.336, 0.755] }),
  // P04 -> F04 Settle guard back to Idle
  makeFL({ dxHead: -0.004, dyHead: 0.002,
    lSh: [0.634, 0.274, 0, 134], lEl: [0.698, 0.440, 1, 134], lWr: [0.692, 0.585, 1, 132],
    rSh: [0.322, 0.275, -1, 134], rEl: [0.294, 0.448, 0, 134], rWr: [0.238, 0.602, 0, 134] }),
];

// 3. back_l (NW): Consistent LEFT-ARM punch straight into North-West (same arm coils in F01 & punches in F02-F03)!
const makeBL = poseBuilder(kpBackL);
const posesBL = [
  // P01 -> F01 coil left elbow back toward camera-left (x=0.26, y=0.50) while right shoulder braces!
  makeBL({ dxHead: 0.008, dyHead: 0.004,
    lSh: [0.342, 0.272, 8, 144], lEl: [0.245, 0.435, 9, 152], lWr: [0.228, 0.535, 10, 156],
    rSh: [0.642, 0.268, 7, 130], rEl: [0.715, 0.438, 7, 132], rWr: [0.702, 0.598, 7, 134] }),
  // P02 -> F02 PUNCH IMPACT into NW! Left shoulder rotates forward-up-left, left fist drives to x=0.145, y=0.355!
  makeBL({ dxHead: -0.024, dyHead: 0.010,
    lSh: [0.312, 0.256, 4, 112], lEl: [0.205, 0.305, 3, 104], lWr: [0.145, 0.348, 2, 96],
    rSh: [0.652, 0.280, 9, 148], rEl: [0.735, 0.445, 10, 152], rWr: [0.732, 0.595, 10, 156],
    lHip: [0.408, 0.618], lKn: [0.362, 0.798], rHip: [0.576, 0.620], rKn: [0.626, 0.798] }),
  // P03 -> F03 Follow-through hold (x=0.165, y=0.425)
  makeBL({ dxHead: -0.018, dyHead: 0.014,
    lSh: [0.320, 0.264, 5, 116], lEl: [0.222, 0.365, 4, 108], lWr: [0.168, 0.435, 3, 100],
    rSh: [0.650, 0.276, 9, 144], rEl: [0.726, 0.442, 9, 148], rWr: [0.718, 0.598, 9, 150],
    lHip: [0.414, 0.618], lKn: [0.368, 0.798], rHip: [0.580, 0.618], rKn: [0.630, 0.798] }),
  // P04 -> F04 Settle guard back to Idle
  makeBL({ dxHead: -0.004, dyHead: 0.002,
    lSh: [0.334, 0.266, 6, 134], lEl: [0.268, 0.442, 6, 136], lWr: [0.232, 0.595, 6, 138],
    rSh: [0.648, 0.266, 9, 134], rEl: [0.711, 0.438, 9, 136], rWr: [0.696, 0.601, 9, 138] }),
];

const descFront =
  "Adult muscular green orc warrior in three-quarter front tactical RPG view, fierce green face with tusks, " +
  "heavy dark steel spiked shoulder pauldrons, dark iron breastplate with red trim, chainmail sleeves, " +
  "spiked steel bracers and closed empty brown leather gauntlets, red tassets, steel greaves and grounded boots. " +
  "Empty hands, completely unarmed, no weapons. Refined pixel art with crisp dark outlines.";

const descBackL = nwSwordReq.description;

fs.writeFileSync(`${EXP}/unarmed_se_request.json`, JSON.stringify({
  description: descFront,
  action: "unarmed heavy right-hand cross punch",
  direction: "south-east",
  view: "low top-down",
  no_background: true,
  seed: 75041,
  first_frame_url: uploads.front_r,
  first_frame_keypoints: kpFrontR,
  keypoints: posesFR,
}, null, 2));

fs.writeFileSync(`${EXP}/unarmed_sw_request.json`, JSON.stringify({
  description: descFront,
  action: "unarmed heavy left-hand cross punch",
  direction: "south-west",
  view: "low top-down",
  no_background: true,
  seed: 75042,
  first_frame_url: uploads.front_l,
  first_frame_keypoints: kpFrontL,
  keypoints: posesFL,
}, null, 2));

fs.writeFileSync(`${EXP}/unarmed_nw_request.json`, JSON.stringify({
  description: descBackL,
  action: "unarmed heavy left-arm punch into north-west",
  direction: "north-west",
  view: "low top-down",
  no_background: true,
  seed: 75043,
  first_frame_url: uploads.back_l,
  first_frame_keypoints: kpBackL,
  keypoints: posesBL,
}, null, 2));

// Stick-figure preview!
const out = new PNG({ width: 4 * 132, height: 3 * 136 });
for (let i = 0; i < out.data.length; i += 4) { out.data[i]=24; out.data[i+1]=28; out.data[i+2]=36; out.data[i+3]=255; }
function setPx(x, y, r, g, b) {
  if (x < 0 || y < 0 || x >= out.width || y >= out.height) return;
  const k = (y * out.width + x) * 4;
  out.data[k]=r; out.data[k+1]=g; out.data[k+2]=b; out.data[k+3]=255;
}
function drawLine(x0, y0, x1, y1, r, g, b) {
  const steps = Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0), 1);
  for (let s = 0; s <= steps; s++) {
    const x = Math.round(x0 + (x1 - x0) * (s / steps));
    const y = Math.round(y0 + (y1 - y0) * (s / steps));
    setPx(x, y, r, g, b); setPx(x+1, y, r, g, b);
  }
}
const BONES = [
  ["NECK", "RIGHT SHOULDER", [255,140,40]], ["RIGHT SHOULDER", "RIGHT ELBOW", [255,210,40]], ["RIGHT ELBOW", "RIGHT ARM", [255,255,80]],
  ["NECK", "LEFT SHOULDER", [80,180,255]],  ["LEFT SHOULDER", "LEFT ELBOW", [80,210,255]],   ["LEFT ELBOW", "LEFT ARM", [120,240,255]],
  ["RIGHT HIP", "RIGHT KNEE", [180,255,140]], ["RIGHT KNEE", "RIGHT LEG", [180,255,140]],
  ["LEFT HIP", "LEFT KNEE", [140,220,180]],   ["LEFT KNEE", "LEFT LEG", [140,220,180]],
];
[
  ["front_r_base_128.png", posesFR],
  ["front_l_base_128.png", posesFL],
  ["back_l_base_128.png",  posesBL],
].forEach(([imgName, list], rIdx) => {
  const ref = PNG.sync.read(fs.readFileSync(path.join(EXP, imgName)));
  list.forEach((kp, cIdx) => {
    const ox = cIdx * 132 + 2, oy = rIdx * 136 + 4;
    for (let y = 0; y < 128; y++) for (let x = 0; x < 128; x++) {
      const k = (y * 128 + x) * 4;
      if (ref.data[k+3] > 0) setPx(ox+x, oy+y, Math.round(ref.data[k]*0.45), Math.round(ref.data[k+1]*0.45), Math.round(ref.data[k+2]*0.45));
      else setPx(ox+x, oy+y, 34, 38, 48);
    }
    const m = Object.fromEntries(kp.map(p => [p.label, [Math.round(p.x*128), Math.round(p.y*128)]]));
    for (const [a, b, col] of BONES) drawLine(ox+m[a][0], oy+m[a][1], ox+m[b][0], oy+m[b][1], col[0], col[1], col[2]);
  });
});
fs.writeFileSync(`${AUDIT}/skeleton_unarmed_preview.png`, PNG.sync.write(out));
console.log("Built unarmed SE/SW/NW requests and skeleton_unarmed_preview.png");
