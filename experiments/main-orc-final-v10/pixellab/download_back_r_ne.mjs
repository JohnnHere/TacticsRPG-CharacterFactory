import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const { PNG } = createRequire("c:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory/package.json")("pngjs");

const EXP = "c:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory/experiments/main-orc-final-v10/pixellab";
const AUDIT = "C:/Users/João Orlando/.gemini/antigravity/brain/5fe480f6-d661-411c-b120-c9742e395c32/scratch/audit";

const jobs = [
  { id: "811eedb1-f2e2-4be8-9c1d-65710145d7d3", dir: "raw_sword_ne", count: 12 },
  { id: "0e3f685a-3222-4e5c-9883-5f330ce815f0", dir: "raw_axe_ne", count: 10 },
];

for (const job of jobs) {
  const outDir = path.join(EXP, job.dir);
  fs.mkdirSync(outDir, { recursive: true });
  for (let i = 0; i < job.count; i++) {
    const url = `https://api.pixellab.ai/mcp/images/${job.id}/download?index=${i}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Download failed ${url}: ${res.status}`);
    const buf = Buffer.from(await res.arrayBuffer());
    const fName = String(i).padStart(2, "0") + ".png";
    fs.writeFileSync(path.join(outDir, fName), buf);
  }
  console.log(`Downloaded ${job.count} frames to ${outDir}`);
}

// Render 2x contact sheets (6 cols x 2 rows per sheet) with 10px subtle grid in 128x128 space (256x256 offset +64,+64)
function renderSheet(dir, count, outPng) {
  const cols = 6;
  const rows = Math.ceil(count / cols);
  const scale = 2;
  const cell = 128 * scale + 8;
  const out = new PNG({ width: cols * cell, height: rows * cell });
  for (let i = 0; i < out.data.length; i += 4) {
    out.data[i] = 30; out.data[i + 1] = 34; out.data[i + 2] = 44; out.data[i + 3] = 255;
  }
  for (let idx = 0; idx < count; idx++) {
    const png = PNG.sync.read(fs.readFileSync(path.join(EXP, dir, String(idx).padStart(2, "0") + ".png")));
    const cx = (idx % cols) * cell + 4;
    const cy = Math.floor(idx / cols) * cell + 4;
    for (let y = 0; y < 128; y++) {
      for (let x = 0; x < 128; x++) {
        const k = (y * 128 + x) * 4;
        const a = png.data[k + 3] / 255;
        const isGrid = (x % 16 === 0 || y % 16 === 0);
        const bgR = isGrid ? 58 : 42, bgG = isGrid ? 66 : 48, bgB = isGrid ? 82 : 60;
        const r = Math.round(png.data[k] * a + bgR * (1 - a));
        const g = Math.round(png.data[k + 1] * a + bgG * (1 - a));
        const b = Math.round(png.data[k + 2] * a + bgB * (1 - a));
        for (let dy = 0; dy < scale; dy++) {
          for (let dx = 0; dx < scale; dx++) {
            const ok = ((cy + y * scale + dy) * out.width + (cx + x * scale + dx)) * 4;
            out.data[ok] = r; out.data[ok + 1] = g; out.data[ok + 2] = b; out.data[ok + 3] = 255;
          }
        }
      }
    }
  }
  fs.mkdirSync(AUDIT, { recursive: true });
  fs.writeFileSync(path.join(AUDIT, outPng), PNG.sync.write(out));
  console.log(`Rendered ${outPng}`);
}

renderSheet("raw_sword_ne", 12, "raw_sword_ne_2x.png");
renderSheet("raw_axe_ne", 10, "raw_axe_ne_2x.png");
