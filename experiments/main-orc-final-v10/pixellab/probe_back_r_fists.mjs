import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const { PNG } = createRequire("c:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory/package.json")("pngjs");

const EXP = "c:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory/experiments/main-orc-final-v10/pixellab";
const AUDIT = "C:/Users/João Orlando/.gemini/antigravity/brain/5fe480f6-d661-411c-b120-c9742e395c32/scratch/audit";

const swordReq = JSON.parse(fs.readFileSync(path.join(EXP, "sword_ne_request.json"), "utf8"));
const axeReq = JSON.parse(fs.readFileSync(path.join(EXP, "axe_ne_request.json"), "utf8"));

function inspectSet(dir, kps, outPng) {
  const cols = 6;
  const rows = Math.ceil(kps.length / cols);
  const scale = 3;
  const cell = 128 * scale + 8;
  const out = new PNG({ width: cols * cell, height: rows * cell });
  for (let i = 0; i < out.data.length; i += 4) { out.data[i]=26; out.data[i+1]=30; out.data[i+2]=40; out.data[i+3]=255; }

  console.log(`\n=== ${dir} ===`);
  for (let idx = 0; idx < kps.length; idx++) {
    const png = PNG.sync.read(fs.readFileSync(path.join(EXP, dir, String(idx).padStart(2, "0") + ".png")));
    const wr = kps[idx].find(p => p.label === "RIGHT ARM");
    const wx = Math.round(wr.x * 128);
    const wy = Math.round(wr.y * 128);

    // Search for opaque pixels around (wx, wy) within radius 14 and find centroid of leather/distal pixels
    let sumX = 0, sumY = 0, cnt = 0;
    let sumLX = 0, sumLY = 0, cntL = 0;
    for (let y = Math.max(0, wy - 10); y <= Math.min(127, wy + 10); y++) {
      for (let x = Math.max(0, wx - 10); x <= Math.min(127, wx + 10); x++) {
        const k = (y * 128 + x) * 4;
        if (png.data[k + 3] > 0) {
          const r = png.data[k], g = png.data[k + 1], b = png.data[k + 2];
          sumX += x; sumY += y; cnt++;
          if (r > b + 8 && r < 130) { sumLX += x; sumLY += y; cntL++; }
        }
      }
    }
    const cx128 = cntL >= 6 ? Math.round(sumLX / cntL) : (cnt > 0 ? Math.round(sumX / cnt) : wx);
    const cy128 = cntL >= 6 ? Math.round(sumLY / cntL) : (cnt > 0 ? Math.round(sumY / cnt) : wy);
    console.log(`raw ${String(idx).padStart(2,"0")}: kp=(${wx+64},${wy+64}) estFist=(${cx128+64},${cy128+64}) [128: (${cx128},${cy128})]`);

    const ox = (idx % cols) * cell + 4;
    const oy = Math.floor(idx / cols) * cell + 4;
    for (let y = 0; y < 128; y++) {
      for (let x = 0; x < 128; x++) {
        const k = (y * 128 + x) * 4;
        const a = png.data[k + 3] / 255;
        let r = Math.round(png.data[k] * a + 40 * (1 - a));
        let g = Math.round(png.data[k + 1] * a + 46 * (1 - a));
        let b = Math.round(png.data[k + 2] * a + 58 * (1 - a));
        // Red crosshair on estFist, cyan dot on kp
        if ((Math.abs(x - cx128) <= 3 && y === cy128) || (Math.abs(y - cy128) <= 3 && x === cx128)) {
          r = 255; g = 40; b = 60;
        }
        if (x === wx && y === wy) { r = 40; g = 255; b = 255; }
        for (let dy = 0; dy < scale; dy++) {
          for (let dx = 0; dx < scale; dx++) {
            const ok = ((oy + y * scale + dy) * out.width + (ox + x * scale + dx)) * 4;
            out.data[ok] = r; out.data[ok + 1] = g; out.data[ok + 2] = b; out.data[ok + 3] = 255;
          }
        }
      }
    }
  }
  fs.writeFileSync(path.join(AUDIT, outPng), PNG.sync.write(out));
}

inspectSet("raw_sword_ne", swordReq.keypoints, "fist_probe_sword_ne_3x.png");
inspectSet("raw_axe_ne", axeReq.keypoints, "fist_probe_axe_ne_3x.png");
