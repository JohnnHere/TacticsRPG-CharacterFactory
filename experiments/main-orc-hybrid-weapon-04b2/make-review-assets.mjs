import fs from "node:fs";
import path from "node:path";
import { PNG } from "pngjs";

const ROOT = process.cwd();
const EXP_DIR = path.join(ROOT, "experiments/main-orc-hybrid-weapon-04b2");
const SRC_CLIP_DIR = path.join(ROOT, "characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword");

function loadPng(filePath) {
  return PNG.sync.read(fs.readFileSync(filePath));
}

function savePng(png, filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, PNG.sync.write(png));
}

function createCanvas(width, height, bg = [18, 22, 28, 255]) {
  const png = new PNG({ width, height });
  for (let i = 0; i < width * height; i++) {
    const idx = i * 4;
    png.data[idx] = bg[0];
    png.data[idx + 1] = bg[1];
    png.data[idx + 2] = bg[2];
    png.data[idx + 3] = bg[3];
  }
  return png;
}

function blitScaledNearest(dst, src, sx, sy, sw, sh, dx, dy, scale) {
  for (let y = 0; y < sh; y++) {
    const srcY = sy + y;
    if (srcY < 0 || srcY >= src.height) continue;
    for (let x = 0; x < sw; x++) {
      const srcX = sx + x;
      if (srcX < 0 || srcX >= src.width) continue;
      const si = (srcY * src.width + srcX) * 4;
      const a = src.data[si + 3];
      if (a === 0) continue;
      const r = src.data[si];
      const g = src.data[si + 1];
      const b = src.data[si + 2];
      for (let py = 0; py < scale; py++) {
        const outY = dy + y * scale + py;
        if (outY < 0 || outY >= dst.height) continue;
        for (let px = 0; px < scale; px++) {
          const outX = dx + x * scale + px;
          if (outX < 0 || outX >= dst.width) continue;
          const di = (outY * dst.width + outX) * 4;
          dst.data[di] = r;
          dst.data[di + 1] = g;
          dst.data[di + 2] = b;
          dst.data[di + 3] = 255;
        }
      }
    }
  }
}

function drawCrosshair(dst, cx, cy, size, color = [255, 90, 90, 255]) {
  for (let d = -size; d <= size; d++) {
    const x1 = cx + d;
    const y1 = cy;
    if (x1 >= 0 && x1 < dst.width && y1 >= 0 && y1 < dst.height) {
      const i = (y1 * dst.width + x1) * 4;
      dst.data[i] = color[0];
      dst.data[i + 1] = color[1];
      dst.data[i + 2] = color[2];
      dst.data[i + 3] = color[3];
    }
    const x2 = cx;
    const y2 = cy + d;
    if (x2 >= 0 && x2 < dst.width && y2 >= 0 && y2 < dst.height) {
      const i = (y2 * dst.width + x2) * 4;
      dst.data[i] = color[0];
      dst.data[i + 1] = color[1];
      dst.data[i + 2] = color[2];
      dst.data[i + 3] = color[3];
    }
  }
}

function buildRepresentativeReview2x() {
  // 4 representative frames: F02, F05, F08, F11
  // 6 rows: Original, Variant A, Variant B, Body-Only, Weapon-Only A, Weapon-Only B
  const repFrames = [2, 5, 8, 11];
  const cropX = 48;
  const cropY = 40;
  const cropW = 192;
  const cropH = 176;
  const scale = 2;
  const cellW = cropW * scale;
  const cellH = cropH * scale;
  const pad = 8;

  const cols = repFrames.length;
  const rows = 6;
  const canvas = createCanvas(cols * (cellW + pad) + pad, rows * (cellH + pad) + pad, [36, 40, 50, 255]);

  for (let c = 0; c < cols; c++) {
    const fIdx = repFrames[c];
    const fCode = String(fIdx).padStart(2, "0");
    const sources = [
      loadPng(path.join(SRC_CLIP_DIR, "frames", `${fCode}.png`)),
      loadPng(path.join(EXP_DIR, "full/a/composite", `${fCode}.png`)),
      loadPng(path.join(EXP_DIR, "full/b/composite", `${fCode}.png`)),
      loadPng(path.join(EXP_DIR, "full/a/body-only", `${fCode}.png`)),
      loadPng(path.join(EXP_DIR, "full/a/weapon-only", `${fCode}.png`)),
      loadPng(path.join(EXP_DIR, "full/b/weapon-only", `${fCode}.png`)),
    ];

    for (let r = 0; r < rows; r++) {
      const dx = pad + c * (cellW + pad);
      const dy = pad + r * (cellH + pad);
      blitScaledNearest(canvas, sources[r], cropX, cropY, cropW, cropH, dx, dy, scale);
    }
  }

  savePng(canvas, path.join(EXP_DIR, "representative-review-2x.png"));
}

function buildGrip10xBoth() {
  // Contact frame F08 grip close-up at 10x for Variant A and Variant B side by side
  const gripProfile = JSON.parse(fs.readFileSync(path.join(EXP_DIR, "grip-profile-back-r.json"), "utf8"));
  const f08 = gripProfile.frames[8];
  const [gx, gy] = f08.rightGrip;
  const cropSize = 36;
  const sx = Math.round(gx - cropSize / 2);
  const sy = Math.round(gy - cropSize / 2);
  const scale = 10;
  const cell = cropSize * scale;
  const pad = 16;

  const compA = loadPng(path.join(EXP_DIR, "full/a/composite/08.png"));
  const compB = loadPng(path.join(EXP_DIR, "full/b/composite/08.png"));

  const out = createCanvas(cell * 2 + pad * 3, cell + pad * 2, [36, 40, 50, 255]);
  blitScaledNearest(out, compA, sx, sy, cropSize, cropSize, pad, pad, scale);
  blitScaledNearest(out, compB, sx, sy, cropSize, cropSize, pad * 2 + cell, pad, scale);

  const markerOffset = Math.round((gx - sx) * scale);
  const markerOffsetY = Math.round((gy - sy) * scale);
  drawCrosshair(out, pad + markerOffset, pad + markerOffsetY, 5, [255, 80, 80, 255]);
  drawCrosshair(out, pad * 2 + cell + markerOffset, pad + markerOffsetY, 5, [80, 220, 255, 255]);

  savePng(out, path.join(EXP_DIR, "grip-10x-both.png"));
}

function buildReviewHands() {
  const gripProfile = JSON.parse(fs.readFileSync(path.join(EXP_DIR, "grip-profile-back-r.json"), "utf8"));
  const cropSize = 40;
  const scale = 6;
  const outSize = cropSize * scale;

  for (const variant of ["a", "b"]) {
    const handDir = path.join(EXP_DIR, "review/hands", variant);
    fs.mkdirSync(handDir, { recursive: true });
    for (let idx = 0; idx < 14; idx++) {
      const fCode = String(idx).padStart(2, "0");
      const gf = gripProfile.frames[idx];
      const [gx, gy] = gf.rightGrip || [155, 132];
      const sx = Math.round(gx - cropSize / 2);
      const sy = Math.round(gy - cropSize / 2);
      const src = loadPng(path.join(EXP_DIR, "full", variant, "composite", `${fCode}.png`));
      const dst = createCanvas(outSize, outSize, [36, 40, 50, 255]);
      blitScaledNearest(dst, src, sx, sy, cropSize, cropSize, 0, 0, scale);
      if (gf.weaponVisible) {
        const cx = Math.round((gx - sx) * scale);
        const cy = Math.round((gy - sy) * scale);
        drawCrosshair(dst, cx, cy, 4, variant === "a" ? [255, 110, 90, 255] : [90, 220, 255, 255]);
      }
      savePng(dst, path.join(handDir, `${fCode}.png`));
    }
  }
}

buildRepresentativeReview2x();
buildGrip10xBoth();
buildReviewHands();
console.log("Generated representative-review-2x.png, grip-10x-both.png, and review/hands/{a,b}/00..13.png");
