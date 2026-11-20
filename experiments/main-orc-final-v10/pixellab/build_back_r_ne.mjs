import fs from "node:fs";
import { createRequire } from "node:module";
const { PNG } = createRequire("c:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory/package.json")("pngjs");

const ROOT = "c:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory";
const EXP  = `${ROOT}/experiments/main-orc-final-v10/pixellab`;
const AUDIT = "C:/Users/João Orlando/.gemini/antigravity/brain/5fe480f6-d661-411c-b120-c9742e395c32/scratch/audit";

const first_kp = [
  {"x":0.5467,"y":0.1641,"label":"NOSE","z_index":-2},
  {"x":0.4941,"y":0.2728,"label":"NECK","z_index":0},
  {"x":0.6337,"y":0.2785,"label":"RIGHT SHOULDER","z_index":-1},
  {"x":0.7001,"y":0.4571,"label":"RIGHT ELBOW","z_index":-2},
  {"x":0.7481,"y":0.6035,"label":"RIGHT ARM","z_index":-2},
  {"x":0.3545,"y":0.2671,"label":"LEFT SHOULDER","z_index":-1},
  {"x":0.2881,"y":0.4548,"label":"LEFT ELBOW","z_index":-2},
  {"x":0.2858,"y":0.5990,"label":"LEFT ARM","z_index":-2},
  {"x":0.5673,"y":0.5623,"label":"RIGHT HIP","z_index":0},
  {"x":0.6360,"y":0.7638,"label":"RIGHT KNEE","z_index":-1},
  {"x":0.6406,"y":0.9286,"label":"RIGHT LEG","z_index":0},
  {"x":0.4231,"y":0.5646,"label":"LEFT HIP","z_index":0},
  {"x":0.3751,"y":0.7592,"label":"LEFT KNEE","z_index":-1},
  {"x":0.3247,"y":0.9194,"label":"LEFT LEG","z_index":0},
  {"x":0.5696,"y":0.1504,"label":"RIGHT EYE","z_index":-1},
  {"x":0.5261,"y":0.1458,"label":"LEFT EYE","z_index":-1},
  {"x":0.5650,"y":0.1458,"label":"RIGHT EAR","z_index":0},
  {"x":0.4941,"y":0.1412,"label":"LEFT EAR","z_index":0},
];

const baseMap = Object.fromEntries(first_kp.map(j => [j.label, j]));
const LABELS = first_kp.map(j => j.label);

function makePose({
  dxHead = 0, dyHead = 0,
  rSh = [0.634, 0.279, -1, 134], rEl = [0.700, 0.457, -2, 136], rWr = [0.748, 0.604, -2, 138],
  lSh = [0.355, 0.267, -1, 134], lEl = [0.288, 0.455, -2, 136], lWr = [0.286, 0.599, -2, 138],
  rHip = [0.567, 0.562], rKn = [0.636, 0.764],
  lHip = [0.423, 0.565], lKn = [0.375, 0.759],
}) {
  const pts = {};
  for (const k of ["NOSE", "NECK", "RIGHT EYE", "LEFT EYE", "RIGHT EAR", "LEFT EAR"]) {
    pts[k] = {
      label: k,
      x: Number((baseMap[k].x + dxHead).toFixed(5)),
      y: Number((baseMap[k].y + dyHead).toFixed(5)),
      z_index: baseMap[k].z_index,
    };
  }
  for (const [lbl, t] of [
    ["RIGHT SHOULDER", rSh], ["RIGHT ELBOW", rEl], ["RIGHT ARM", rWr],
    ["LEFT SHOULDER", lSh],  ["LEFT ELBOW", lEl],  ["LEFT ARM", lWr],
  ]) {
    pts[lbl] = { label: lbl, x: Number(t[0].toFixed(5)), y: Number(t[1].toFixed(5)), z_index: t[2], depth: t[3] };
  }
  pts["RIGHT HIP"]  = { label: "RIGHT HIP",  x: Number(rHip[0].toFixed(5)), y: Number(rHip[1].toFixed(5)), z_index: 0 };
  pts["RIGHT KNEE"] = { label: "RIGHT KNEE", x: Number(rKn[0].toFixed(5)),  y: Number(rKn[1].toFixed(5)),  z_index: -1 };
  pts["RIGHT LEG"]  = { ...baseMap["RIGHT LEG"] };
  pts["LEFT HIP"]   = { label: "LEFT HIP",   x: Number(lHip[0].toFixed(5)), y: Number(lHip[1].toFixed(5)), z_index: 0 };
  pts["LEFT KNEE"]  = { label: "LEFT KNEE",  x: Number(lKn[0].toFixed(5)),  y: Number(lKn[1].toFixed(5)),  z_index: -1 };
  pts["LEFT LEG"]   = { ...baseMap["LEFT LEG"] };
  return LABELS.map(l => pts[l]);
}

const swordKps = [
  // P01 -> F01 body-prep (coil right)
  makePose({ dxHead: -0.008, dyHead: 0.004,
    rSh: [0.642, 0.282, 1, 142], rEl: [0.735, 0.435, 2, 150], rWr: [0.762, 0.545, 3, 154],
    lSh: [0.350, 0.268, -1, 130], lEl: [0.280, 0.452, -2, 132], lWr: [0.272, 0.595, -2, 134] }),
  // P02 -> F02 establish-grip (smooth mid-lift at right side, forearm angled cleanly up!)
  makePose({ dxHead: -0.006, dyHead: 0.000,
    rSh: [0.645, 0.270, 1, 140], rEl: [0.758, 0.375, 2, 148], rWr: [0.778, 0.285, 2, 148],
    lSh: [0.350, 0.270, -1, 130], lEl: [0.278, 0.454, -2, 132], lWr: [0.268, 0.596, -2, 134] }),
  // P03 -> F03 anticipation (raised above right shoulder)
  makePose({ dxHead: -0.004, dyHead: -0.005,
    rSh: [0.640, 0.252, 1, 134], rEl: [0.752, 0.245, 1, 138], rWr: [0.725, 0.132, 1, 136],
    lSh: [0.352, 0.274, -1, 132], lEl: [0.278, 0.456, -2, 134], lWr: [0.266, 0.598, -2, 136] }),
  // P04 -> F04 coil (high overhead coil)
  makePose({ dxHead: 0.000, dyHead: -0.008,
    rSh: [0.632, 0.240, 0, 130], rEl: [0.718, 0.175, 0, 132], rWr: [0.658, 0.085, 0, 128],
    lSh: [0.354, 0.278, -1, 134], lEl: [0.280, 0.458, -1, 136], lWr: [0.266, 0.600, -1, 138] }),
  // P05 -> F05 apex-hold (peak overhead coil)
  makePose({ dxHead: 0.004, dyHead: -0.010,
    rSh: [0.625, 0.236, 0, 126], rEl: [0.692, 0.150, 0, 126], rWr: [0.612, 0.072, -1, 122],
    lSh: [0.356, 0.280, 0, 136], lEl: [0.282, 0.460, 0, 138], lWr: [0.266, 0.602, 0, 140] }),
  // P06 -> F06 apex-descent (driving forward-up-right into NE!)
  makePose({ dxHead: 0.018, dyHead: 0.004,
    rSh: [0.650, 0.248, -2, 116], rEl: [0.768, 0.218, -3, 108], rWr: [0.838, 0.210, -4, 102],
    lSh: [0.348, 0.282, 1, 144],  lEl: [0.268, 0.462, 2, 148],  lWr: [0.242, 0.598, 2, 150],
    rHip: [0.575, 0.565], rKn: [0.642, 0.766], lHip: [0.430, 0.566], lKn: [0.380, 0.760] }),
  // P07 -> F07 slash-release (full NE diagonal drive!)
  makePose({ dxHead: 0.028, dyHead: 0.014,
    rSh: [0.660, 0.262, -2, 112], rEl: [0.790, 0.305, -3, 104], rWr: [0.875, 0.345, -4, 98],
    lSh: [0.342, 0.286, 2, 148],  lEl: [0.258, 0.464, 3, 152],  lWr: [0.228, 0.596, 3, 156],
    rHip: [0.580, 0.570], rKn: [0.646, 0.770], lHip: [0.435, 0.570], lKn: [0.384, 0.762] }),
  // P08 -> F08 CONTACT (325ms NE diagonal cleave impact!)
  makePose({ dxHead: 0.034, dyHead: 0.022,
    rSh: [0.662, 0.276, -2, 110], rEl: [0.785, 0.375, -3, 102], rWr: [0.865, 0.445, -4, 96],
    lSh: [0.340, 0.290, 2, 150],  lEl: [0.254, 0.466, 3, 154],  lWr: [0.224, 0.596, 3, 158],
    rHip: [0.584, 0.574], rKn: [0.650, 0.774], lHip: [0.438, 0.574], lKn: [0.386, 0.764] }),
  // P09 -> F09 follow-through (sweeping diagonally across in front of chest into NE!)
  makePose({ dxHead: 0.028, dyHead: 0.024,
    rSh: [0.650, 0.282, -3, 108], rEl: [0.742, 0.402, -4, 100], rWr: [0.788, 0.498, -5, 96],
    lSh: [0.344, 0.288, 2, 148],  lEl: [0.260, 0.464, 3, 152],  lWr: [0.232, 0.598, 3, 156],
    rHip: [0.580, 0.574], rKn: [0.646, 0.772], lHip: [0.435, 0.574], lKn: [0.384, 0.764] }),
  // P10 -> F10 recover-bridge (pulling back into guard)
  makePose({ dxHead: 0.014, dyHead: 0.012,
    rSh: [0.642, 0.280, -1, 124], rEl: [0.730, 0.425, -1, 130], rWr: [0.775, 0.515, -1, 132],
    lSh: [0.350, 0.276, -1, 138], lEl: [0.276, 0.458, -1, 140], lWr: [0.264, 0.598, -1, 142],
    rHip: [0.573, 0.568], rKn: [0.640, 0.768], lHip: [0.428, 0.568], lKn: [0.378, 0.761] }),
  // P11 -> F11 settle-grip (clean right guard)
  makePose({ dxHead: 0.006, dyHead: 0.004,
    rSh: [0.638, 0.278, -1, 132], rEl: [0.715, 0.445, -1, 136], rWr: [0.762, 0.555, -1, 138],
    lSh: [0.352, 0.270, -1, 134], lEl: [0.284, 0.456, -2, 136], lWr: [0.278, 0.599, -2, 138] }),
  // P12 -> F12 disarm-settle (relaxing into Idle F00)
  makePose({ dxHead: 0.000, dyHead: 0.000,
    rSh: [0.634, 0.279, -1, 134], rEl: [0.702, 0.456, -2, 136], rWr: [0.750, 0.598, -2, 138],
    lSh: [0.355, 0.267, -1, 134], lEl: [0.288, 0.455, -2, 136], lWr: [0.286, 0.599, -2, 138] }),
];

const axeKps = [
  // P01 -> F01 prep
  makePose({ dxHead: -0.010, dyHead: 0.006,
    rSh: [0.644, 0.284, 1, 142], rEl: [0.740, 0.430, 2, 150], rWr: [0.766, 0.535, 3, 154],
    lSh: [0.350, 0.270, -1, 130], lEl: [0.278, 0.454, -2, 132], lWr: [0.270, 0.596, -2, 134] }),
  // P02 -> F02 establish-grip
  makePose({ dxHead: -0.008, dyHead: 0.000,
    rSh: [0.646, 0.268, 1, 140], rEl: [0.760, 0.365, 2, 148], rWr: [0.776, 0.275, 2, 148],
    lSh: [0.350, 0.272, -1, 130], lEl: [0.278, 0.456, -2, 132], lWr: [0.268, 0.598, -2, 134] }),
  // P03 -> F03 anticipation hoist
  makePose({ dxHead: -0.002, dyHead: -0.008,
    rSh: [0.636, 0.244, 0, 132], rEl: [0.735, 0.195, 0, 134], rWr: [0.685, 0.098, 0, 132],
    lSh: [0.354, 0.278, -1, 134], lEl: [0.280, 0.458, -1, 136], lWr: [0.266, 0.600, -1, 138] }),
  // P04 -> F04 155ms heavy overhead coil!
  makePose({ dxHead: 0.004, dyHead: -0.012,
    rSh: [0.624, 0.232, 0, 126], rEl: [0.688, 0.140, 0, 126], rWr: [0.602, 0.062, -1, 122],
    lSh: [0.358, 0.284, 0, 138], lEl: [0.284, 0.462, 0, 140], lWr: [0.268, 0.604, 0, 142] }),
  // P05 -> F05 cleave drive into NE!
  makePose({ dxHead: 0.024, dyHead: 0.010,
    rSh: [0.656, 0.258, -2, 114], rEl: [0.785, 0.275, -3, 106], rWr: [0.865, 0.295, -4, 100],
    lSh: [0.344, 0.286, 2, 146],  lEl: [0.260, 0.464, 3, 150],  lWr: [0.232, 0.598, 3, 154],
    rHip: [0.578, 0.570], rKn: [0.645, 0.770], lHip: [0.434, 0.570], lKn: [0.382, 0.762] }),
  // P06 -> F06 115ms HEAVY IMPACT crouch into NE!
  makePose({ dxHead: 0.038, dyHead: 0.030,
    rSh: [0.664, 0.288, -2, 108], rEl: [0.785, 0.395, -3, 100], rWr: [0.862, 0.478, -4, 95],
    lSh: [0.338, 0.296, 2, 152],  lEl: [0.252, 0.472, 3, 156],  lWr: [0.222, 0.604, 3, 160],
    rHip: [0.586, 0.582], rKn: [0.652, 0.780], lHip: [0.440, 0.582], lKn: [0.388, 0.770] }),
  // P07 -> F07 110ms weight settle
  makePose({ dxHead: 0.032, dyHead: 0.032,
    rSh: [0.654, 0.292, -3, 108], rEl: [0.755, 0.418, -4, 100], rWr: [0.812, 0.515, -5, 96],
    lSh: [0.342, 0.294, 2, 150],  lEl: [0.258, 0.470, 3, 154],  lWr: [0.228, 0.602, 3, 158],
    rHip: [0.582, 0.582], rKn: [0.648, 0.780], lHip: [0.436, 0.582], lKn: [0.385, 0.768] }),
  // P08 -> F08 130ms wrench recovery
  makePose({ dxHead: 0.016, dyHead: 0.016,
    rSh: [0.644, 0.282, -1, 122], rEl: [0.738, 0.415, -1, 128], rWr: [0.788, 0.500, -1, 130],
    lSh: [0.348, 0.280, -1, 138], lEl: [0.274, 0.460, -1, 140], lWr: [0.260, 0.600, -1, 142],
    rHip: [0.574, 0.570], rKn: [0.641, 0.770], lHip: [0.429, 0.570], lKn: [0.379, 0.762] }),
  // P09 -> F09 disarm-rise (50ms)
  makePose({ dxHead: 0.006, dyHead: 0.006,
    rSh: [0.638, 0.279, -1, 132], rEl: [0.715, 0.446, -2, 136], rWr: [0.760, 0.568, -2, 138],
    lSh: [0.353, 0.269, -1, 134], lEl: [0.285, 0.456, -2, 136], lWr: [0.280, 0.599, -2, 138] }),
  // P10 -> F10 shoulder-reset (90ms)
  makePose({ dxHead: 0.000, dyHead: 0.000,
    rSh: [0.634, 0.279, -1, 134], rEl: [0.702, 0.456, -2, 136], rWr: [0.750, 0.600, -2, 138],
    lSh: [0.355, 0.267, -1, 134], lEl: [0.288, 0.455, -2, 136], lWr: [0.286, 0.599, -2, 138] }),
];

const desc =
  "Adult muscular green orc warrior seen from behind in three-quarter north-east view, " +
  "bald green occipital skull, powerful arms with dark steel spiked shoulder plates, " +
  "chainmail sleeves, articulated bracers and closed empty brown leather gauntlets, " +
  "dark broad back plate with spinal ridge, red cloth tassets, dark steel greaves and grounded boots. " +
  "Empty hands, completely unarmed. Refined tactical pixel art with clean clusters and dark outlines.";

const uploadRef = "upload:f5e0fae9-90cf-4699-bf8f-13ea2d20d810";

fs.writeFileSync(`${EXP}/sword_ne_request.json`, JSON.stringify({
  description: desc,
  action: "unarmed right-arm overhead reaching motion",
  direction: "north-east",
  view: "low top-down",
  no_background: true,
  seed: 73042,
  first_frame_url: uploadRef,
  first_frame_keypoints: first_kp,
  keypoints: swordKps,
}, null, 2));

fs.writeFileSync(`${EXP}/axe_ne_request.json`, JSON.stringify({
  description: desc,
  action: "unarmed heavy right-arm overhead chop motion",
  direction: "north-east",
  view: "low top-down",
  no_background: true,
  seed: 74042,
  first_frame_url: uploadRef,
  first_frame_keypoints: first_kp,
  keypoints: axeKps,
}, null, 2));

// Render stick-figure preview over dimmed back_r_base_128.png!
const ref = PNG.sync.read(fs.readFileSync(`${EXP}/back_r_base_128.png`));
const out = new PNG({ width: 12 * 132, height: 2 * 136 });
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
    setPx(x, y, r, g, b); setPx(x+1, y, r, g, b); setPx(x, y+1, r, g, b);
  }
}

const BONES = [
  ["NECK", "RIGHT SHOULDER", [255,140,40]],
  ["RIGHT SHOULDER", "RIGHT ELBOW", [255,210,40]],
  ["RIGHT ELBOW", "RIGHT ARM", [255,255,80]],
  ["NECK", "LEFT SHOULDER", [80,180,255]],
  ["LEFT SHOULDER", "LEFT ELBOW", [80,210,255]],
  ["LEFT ELBOW", "LEFT ARM", [120,240,255]],
  ["RIGHT HIP", "RIGHT KNEE", [180,255,140]],
  ["RIGHT KNEE", "RIGHT LEG", [180,255,140]],
  ["LEFT HIP", "LEFT KNEE", [140,220,180]],
  ["LEFT KNEE", "LEFT LEG", [140,220,180]],
];

[swordKps, axeKps].forEach((list, rIdx) => {
  list.forEach((kp, cIdx) => {
    const ox = cIdx * 132 + 2, oy = rIdx * 136 + 4;
    for (let y = 0; y < 128; y++)
      for (let x = 0; x < 128; x++) {
        const k = (y * 128 + x) * 4;
        if (ref.data[k+3] > 0) setPx(ox + x, oy + y, Math.round(ref.data[k]*0.45), Math.round(ref.data[k+1]*0.45), Math.round(ref.data[k+2]*0.45));
        else setPx(ox + x, oy + y, 34, 38, 48);
      }
    const m = Object.fromEntries(kp.map(p => [p.label, [Math.round(p.x * 128), Math.round(p.y * 128)]]));
    for (const [a, b, col] of BONES) drawLine(ox + m[a][0], oy + m[a][1], ox + m[b][0], oy + m[b][1], col[0], col[1], col[2]);
    const [rx, ry] = m["RIGHT ARM"];
    for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) setPx(ox + rx + dx, oy + ry + dy, 255, 60, 70);
  });
});

fs.writeFileSync(`${AUDIT}/skeleton_ne_preview.png`, PNG.sync.write(out));
console.log("Saved sword_ne_request.json, axe_ne_request.json, and skeleton_ne_preview.png");
