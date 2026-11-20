import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const { PNG } = createRequire("c:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory/package.json")("pngjs");

const EXP = "c:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory/experiments/main-orc-final-v10/pixellab";

const jobs = [
  { id: "9429288a-db3c-40b2-9db8-f8d66b517ff4", dir: "raw_unarmed_se", count: 4 },
  { id: "fd4b355a-0403-4992-a5ba-855f14550e76", dir: "raw_unarmed_sw", count: 4 },
  { id: "d4d6952b-5375-49b9-ad14-7e27557b22d4", dir: "raw_unarmed_nw", count: 4 },
];

for (const job of jobs) {
  const outDir = path.join(EXP, job.dir);
  fs.mkdirSync(outDir, { recursive: true });
  for (let i = 0; i < job.count; i++) {
    const res = await fetch(`https://api.pixellab.ai/mcp/images/${job.id}/download?index=${i}`);
    if (!res.ok) throw new Error(`Failed ${job.id} #${i}: ${res.status}`);
    fs.writeFileSync(path.join(outDir, String(i).padStart(2, "0") + ".png"), Buffer.from(await res.arrayBuffer()));
  }
  console.log(`Downloaded ${job.dir}`);
}

// Also measure outer weapon-hand coordinates in front_r & front_l Idle/00.png (x < 105 for front_r, x > 150 for front_l)
for (const [d, x0, x1] of [["front_r", 80, 106], ["front_l", 150, 176]]) {
  const p = PNG.sync.read(fs.readFileSync(`c:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory/characters/orc-v1/source/complete-v1/${d}/Idle/00.png`));
  let sx = 0, sy = 0, c = 0;
  for (let y = 128; y <= 148; y++) {
    for (let x = x0; x <= x1; x++) {
      const k = (y * 256 + x) * 4;
      if (p.data[k + 3] > 0) { sx += x; sy += y; c++; }
    }
  }
  console.log(`${d} outer resting hand centroid: (${Math.round(sx/c)}, ${Math.round(sy/c)}) [count=${c}]`);
}
