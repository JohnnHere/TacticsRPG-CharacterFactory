import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const { PNG } = createRequire("c:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory/package.json")("pngjs");

const ROOT = "c:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory";
const EXP = `${ROOT}/experiments/main-orc-final-v10/pixellab`;
const UPLOAD_URL = "https://api.pixellab.ai/v2/uploads/eyJ1IjogIjI5YjRhZjhmLWVhOWMtNDcxZC04OWJjLTE4MWUwM2VjYjU3NyIsICJleHAiOiAxNzk1MTE5NTE2fQ.PENKdYOLi-60TI_did32UNM-day18vyZxPhWwd7DGTM";

function crop128(srcRel, outName) {
  const src = PNG.sync.read(fs.readFileSync(path.join(ROOT, srcRel)));
  if (src.width === 128 && src.height === 128) {
    fs.writeFileSync(path.join(EXP, outName), PNG.sync.write(src));
    return;
  }
  const out = new PNG({ width: 128, height: 128 });
  for (let y = 0; y < 128; y++) {
    for (let x = 0; x < 128; x++) {
      const sk = ((y + 64) * 256 + (x + 64)) * 4;
      const dk = (y * 128 + x) * 4;
      out.data[dk] = src.data[sk];
      out.data[dk+1] = src.data[sk+1];
      out.data[dk+2] = src.data[sk+2];
      out.data[dk+3] = src.data[sk+3];
    }
  }
  fs.writeFileSync(path.join(EXP, outName), PNG.sync.write(out));
}

crop128("characters/orc-v1/source/complete-v1/front_r/Idle/00.png", "front_r_base_128.png");
crop128("characters/orc-v1/source/complete-v1/front_l/Idle/00.png", "front_l_base_128.png");
crop128("characters/orc-v1/source/complete-v1/back_l/Idle/00.png", "back_l_base_128.png");

async function uploadPng(fileName) {
  const buf = fs.readFileSync(path.join(EXP, fileName));
  const fd = new FormData();
  fd.append("file", new Blob([buf], { type: "image/png" }), fileName);
  const res = await fetch(UPLOAD_URL, { method: "POST", body: fd });
  if (!res.ok) throw new Error(`Upload failed ${fileName}: ${res.status} ${await res.text()}`);
  return await res.json();
}

const refs = {};
for (const [key, fname] of [
  ["front_r", "front_r_base_128.png"],
  ["front_l", "front_l_base_128.png"],
  ["back_l",  "back_l_base_128.png"],
]) {
  const r = await uploadPng(fname);
  refs[key] = r.ref;
  console.log(`${key} -> ${r.ref}`);
}
fs.writeFileSync(path.join(EXP, "unarmed_uploads.json"), JSON.stringify(refs, null, 2) + "\n");
