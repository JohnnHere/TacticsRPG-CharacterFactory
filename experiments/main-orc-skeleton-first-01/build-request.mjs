import fs from 'node:fs';
import path from 'node:path';

// Assembles the final request file for the single authorized PixelLab call.
// It does not call PixelLab itself: the request is written to disk so the exact
// payload can be audited before the Orchestrator issues the generation.

const ROOT = path.resolve(import.meta.dirname, '../..');
const EXPERIMENT = path.resolve(import.meta.dirname);
const REFERENCE = path.join(ROOT, 'characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/frames/02.png');

const payload = JSON.parse(fs.readFileSync(path.join(EXPERIMENT, 'pixellab-payload.json'), 'utf8'));
const base64 = fs.readFileSync(REFERENCE).toString('base64');

const request = {
  ...payload,
  first_frame_base64: base64,
};

const outPath = path.join(EXPERIMENT, 'pixellab-request.json');
fs.writeFileSync(outPath, JSON.stringify(request));

const check = JSON.parse(fs.readFileSync(outPath, 'utf8'));
console.log(`request: ${outPath}`);
console.log(`tamanho: ${(fs.statSync(outPath).size / 1024).toFixed(1)} KB`);
console.log(`quadros keypoints: ${check.keypoints.length}`);
console.log(`first_frame_keypoints: ${check.first_frame_keypoints.length} juntas`);
console.log(`referência embutida: ${(base64.length / 1024).toFixed(1)} KB base64`);
console.log(`direção ${check.direction} | view ${check.view} | template ${check.template_id} | seed ${check.seed}`);
