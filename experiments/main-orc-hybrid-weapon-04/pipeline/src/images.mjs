import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';
import { write, pngFiles, slash, expectedSlots, hash, now } from './core.mjs';

export function decode(p) {
  const buffer = fs.readFileSync(p);
  if (buffer.length < 33 || !buffer.subarray(0, 8).equals(Buffer.from([137,80,78,71,13,10,26,10]))) throw Error('Assinatura PNG invalida.');
  const width = buffer.readUInt32BE(16), height = buffer.readUInt32BE(20);
  if (width < 1 || height < 1 || width * height > 16_777_216) throw Error('PNG muito grande ou dimensoes invalidas (limite 16M pixels).');
  return { image: PNG.sync.read(buffer), colorType: buffer[25], sha256: hash(buffer) };
}
export function measure(image) {
  const { width, height, data } = image;
  let left = width, right = -1, top = height, bottom = -1, transparent = 0, partial = 0;
  const colors = new Set();
  for (let y = 0; y < height; y++) for (let x = 0; x < width; x++) {
    const i = (y * width + x) * 4, a = data[i + 3];
    if (a === 0) { transparent++; continue; }
    left = Math.min(left, x); right = Math.max(right, x); top = Math.min(top, y); bottom = Math.max(bottom, y);
    if (a < 255) partial++;
    colors.add(`${data[i]},${data[i+1]},${data[i+2]}`);
  }
  return { width, height, left, right, top, bottom, contentHeight: bottom < 0 ? 0 : bottom - top + 1, transparent, partial, colorCount: colors.size };
}
export function validate(spec, dir, stage) {
  const checks = [], measurements = [], expected = expectedSlots(spec, stage), all = expectedSlots(spec), root = path.join(dir, 'sprites');
  const add = (file, check, status, detail) => checks.push({ file, check, status, detail });
  for (const slot of expected) if (!fs.existsSync(path.join(root, slot))) add(slot, 'required', 'FAIL', 'Arquivo ausente.');
  const pixels = new Map();
  for (const p of pngFiles(root)) {
    const rel = slash(path.relative(root, p));
    try {
      const { image, colorType, sha256 } = decode(p), m = measure(image);
      measurements.push({ file: rel, sha256, ...m });
      const check = (name, valid, detail) => add(rel, name, valid ? 'PASS' : 'FAIL', detail);
      check('naming', all.includes(rel), 'Nome e inventario conforme ficha.');
      check('canvas', m.width === spec.profile.width && m.height === spec.profile.height, `${m.width}x${m.height}`);
      check('rgba', colorType === 6 && image.depth === 8, `PNG tipo=${colorType}; profundidade=${image.depth}; requerido RGBA 8-bit.`);
      check('content', m.contentHeight > 0 && m.transparent > 0, `altura=${m.contentHeight}, transparentes=${m.transparent}`);
      if (spec.profile.groundY !== null) check('ground', m.bottom === spec.profile.groundY, `bottom=${m.bottom}; alvo=${spec.profile.groundY}; origem no topo.`);
      else add(rel, 'ground', 'NOT_RUN', 'Perfil sem linha de chao.');
      if (m.partial > 0) add(rel, 'alpha', 'WARNING', `${m.partial} pixels com alfa parcial; inspecionar bordas.`);
      if (m.left === 0 || m.right === m.width-1 || m.top === 0 || m.bottom === m.height-1) add(rel, 'clipping', 'WARNING', 'Pixels tocam a borda.');
      const pixelHash = hash(Buffer.concat([Buffer.from(`${image.width}x${image.height}:`), image.data]));
      if (pixels.has(pixelHash)) add(rel, 'duplicate', 'WARNING', `Pixels identicos a ${pixels.get(pixelHash)}.`);
      pixels.set(pixelHash, rel);
    } catch (error) { add(rel, 'decode', 'FAIL', error.message); }
  }
  for (const d of ['back_l','back_r','front_r','front_l']) {
    const idle = measurements.filter(x => x.file.startsWith(`Animations/Idle/idle_${d}_`));
    if (idle.length > 1) add(`Idle/${d}`, 'bob', Math.max(...idle.map(x => x.top))-Math.min(...idle.map(x => x.top)) <= 2 ? 'PASS' : 'FAIL', 'Amplitude do topo <=2px; contatos ainda exigem revisao.');
  }
  add('.', 'art', 'REQUIRES_HUMAN_REVIEW', 'Identidade entre vistas, anatomia, silhueta, clusters, luz, mao dominante e loop.');
  add('.', 'unity', 'NOT_RUN', 'Import/Resources.Load/PlayMode nao executados.');
  const summary = Object.fromEntries(['PASS','FAIL','WARNING','NOT_RUN','REQUIRES_HUMAN_REVIEW'].map(s => [s, checks.filter(c => c.status === s).length]));
  return { schemaVersion: 1, characterId: spec.id, stage, createdAt: now(), summary, measurements, checks };
}
// Source-over compositing in the authored pixel grid. No scaling, mirroring or automatic retouch.
export function composite(images, width, height) {
  const out = new PNG({ width, height });
  for (const img of images) {
    if (img.width !== width || img.height !== height) throw Error('Camada com canvas diferente; nenhuma reescala automatica.');
    for (let i = 0; i < out.data.length; i += 4) {
      const sa = img.data[i+3]/255, da = out.data[i+3]/255, a = sa+da*(1-sa);
      if (!a) continue;
      for (let c = 0; c < 3; c++) out.data[i+c] = Math.round((img.data[i+c]*sa+out.data[i+c]*da*(1-sa))/a);
      out.data[i+3] = Math.round(a*255);
    }
  }
  return out;
}
export function savePNG(p, img) { write(p, PNG.sync.write(img, { colorType: 6, inputColorType: 6, bitDepth: 8 })); }
export function contactSheet(paths, dest, tile = 256, columns = 4) {
  if (!paths.length) throw Error('Nenhuma imagem para preview.');
  const out = new PNG({ width: tile*columns, height: tile*Math.ceil(paths.length/columns) });
  for (let y = 0; y < out.height; y++) for (let x = 0; x < out.width; x++) {
    const i = (y*out.width+x)*4, color = (Math.floor(x/8)+Math.floor(y/8))%2 ? 65 : 45;
    out.data[i]=out.data[i+1]=out.data[i+2]=color; out.data[i+3]=255;
  }
  paths.forEach((p, index) => {
    const src = decode(p).image, scale = Math.min(tile/src.width, tile/src.height);
    const w = Math.max(1, Math.floor(src.width*scale)), h = Math.max(1, Math.floor(src.height*scale));
    const ox = index%columns*tile+Math.floor((tile-w)/2), oy = Math.floor(index/columns)*tile+Math.floor((tile-h)/2);
    for (let y=0;y<h;y++) for(let x=0;x<w;x++) {
      const si = (Math.min(src.height-1,Math.floor(y/scale))*src.width+Math.min(src.width-1,Math.floor(x/scale)))*4;
      const di = ((y+oy)*out.width+x+ox)*4, a=src.data[si+3]/255;
      for(let c=0;c<3;c++) out.data[di+c]=Math.round(src.data[si+c]*a+out.data[di+c]*(1-a));
    }
  });
  savePNG(dest, out);
}
