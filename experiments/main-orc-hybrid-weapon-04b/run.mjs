// Pilot B1 — front_r. Reuses the Experiment 04 composition mechanism.
// Stages: `full` (author in Aseprite) then `verify` (prove reuse, grip, timing, artefacts).
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {PNG} from 'pngjs';

const E = 'experiments/main-orc-hybrid-weapon-04b';
const E4 = 'experiments/main-orc-hybrid-weapon-04';
const SRC = 'characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_r-sword';
const GRIP = {2:[103,130],3:[90,119],4:[98,100],5:[98,89],6:[127,101],7:[155,114],8:[158,132],9:[159,148],10:[134,147],11:[110,150]};
const hash = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const json = (p, v) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, JSON.stringify(v, null, 2) + '\n'); };
const walk = p => fs.readdirSync(p, {withFileTypes: true}).flatMap(d => d.isDirectory() ? walk(path.join(p, d.name)) : [path.join(p, d.name)]);
const clip = JSON.parse(fs.readFileSync(SRC + '/clip.json'));
const stage = process.argv[2] ?? 'full';

if (stage === 'full') {
  json(E + '/protected-before.json', Object.fromEntries(['characters', 'assets', 'reports'].flatMap(walk).map(p => [p, hash(p)])));
  const r = spawnSync('F:/SteamLibrary/steamapps/common/Aseprite/Aseprite.exe',
    ['--batch', '--noinapp', '--script', E + '/author.lua'],
    {windowsHide: true, encoding: 'utf8', timeout: 600000,
     env: {...process.env, ASEPRITE_USER_FOLDER: path.resolve(E, 'batch-profile')}});
  fs.writeFileSync(E + '/full-aseprite.log', (r.stdout ?? '') + '\n' + (r.stderr ?? ''));
  if (r.status !== 0) { console.error(r.stdout, r.stderr); throw new Error('Aseprite falhou: ' + r.status); }
  console.log(r.stdout.trim());
}

if (stage === 'verify') {
  const png = p => PNG.sync.read(fs.readFileSync(p));
  const srcWeaponCache = {};
  const srcWeapon = idx => {
    if (srcWeaponCache[idx]) return srcWeaponCache[idx];
    const w = 256, h = 256;
    const acc = new Uint8Array(w * h * 4);
    for (const layer of ['weaponBack', 'weaponFront']) {
      const p = `${SRC}/layers/${layer}/${String(idx).padStart(2, '0')}.png`;
      if (!fs.existsSync(p)) continue;
      const d = png(p).data;
      for (let i = 0; i < acc.length; i += 4) {
        if (d[i + 3] > 0) { acc[i] = d[i]; acc[i + 1] = d[i + 1]; acc[i + 2] = d[i + 2]; acc[i + 3] = d[i + 3]; }
      }
    }
    return (srcWeaponCache[idx] = acc);
  };

  // 1. body + handFront must be byte-identical to the front_r source on both variants
  const reuse = [];
  for (const f of clip.frames) {
    const fn = `F${String(f.index).padStart(2, '0')}.png`;
    for (const n of ['body', 'handFront']) {
      const src = `${SRC}/layers/${n}/${String(f.index).padStart(2, '0')}.png`;
      const a = `${E}/full/a/layers/${n}/${fn}`, b = `${E}/full/b/layers/${n}/${fn}`;
      reuse.push({frame: f.index, layer: n,
        aEqualsSource: hash(src) === hash(a),
        bEqualsSource: hash(src) === hash(b),
        aEqualsB: hash(a) === hash(b),
        rgbaEqual: png(src).data.equals(png(a).data) && png(a).data.equals(png(b).data)});
    }
  }

  // 2. weapon-only comparison in canvas space.
  // The source art is not a pixel-exact rigid rotation of the asset (Aseprite resampling
  // leaves a ~1 px boundary noise), so the guard region is defined along the blade axis with
  // a safety margin instead of an exact v threshold. s = 66 - v, positive toward the tip.
  // A guard-region change is only acceptable if it is ink over ink: the blade's own dark
  // outline spilling one pixel at the base must never repaint the guard's metal.
  const GUARD_S = 9;
  const INK_MAX = 40;
  const B_ITEM = png(`${E}/variants/sword-b/sword.png`).data;
  const itemPx = (u, v) => { const i = (v * 96 + u) * 4; return [B_ITEM[i], B_ITEM[i + 1], B_ITEM[i + 2], B_ITEM[i + 3]]; };
  const itemCols = v => {
    const cols = [];
    for (let u = 0; u < 96; u++) if (itemPx(u, v)[3] > 0) cols.push(u);
    return cols;
  };
  const weapon = [];
  for (const idx of Object.keys(GRIP).map(Number)) {
    const fn = `F${String(idx).padStart(2, '0')}.png`;
    const A = png(`${E}/full/a/weapon-only/${fn}`).data;
    const B = png(`${E}/full/b/weapon-only/${fn}`).data;
    const S = srcWeapon(idx);
    const [gx, gy] = GRIP[idx];
    const rot = clip.frames[idx].rotationDeg;
    const a = rot * Math.PI / 180, ca = Math.cos(a), sa = Math.sin(a);
    let silhouette = 0, changed = 0, guardChanged = 0, guardNonInk = 0, bladeChanged = 0;
    let aVsSource = 0, leftover = 0;
    // A pixel only counts as changed when its coverage changes or, if covered, its colour changes.
    // RGB under alpha 0 is meaningless and must not be compared.
    const differs = (d1, d2, i) => {
      const o1 = d1[i + 3] > 0, o2 = d2[i + 3] > 0;
      if (o1 !== o2) return true;
      if (!o1) return false;
      return d1[i] !== d2[i] || d1[i + 1] !== d2[i + 1] || d1[i + 2] !== d2[i + 2];
    };
    const maxCh = (d, i) => Math.max(d[i], d[i + 1], d[i + 2]);
    for (let y = 0; y < 256; y++) for (let x = 0; x < 256; x++) {
      const i = (y * 256 + x) * 4;
      const opA = A[i + 3] > 0, opB = B[i + 3] > 0;
      if (opA !== opB) silhouette++;
      const d = differs(A, B, i);
      if (d) changed++;
      if (differs(S, A, i)) aVsSource++;
      const dx = x - gx, dy = y - gy;
      const u = Math.floor(48 + dx * ca + dy * sa + 0.5);
      const v = Math.floor(66 - dx * sa + dy * ca + 0.5);
      const s = 66 - v;
      if (d) {
        if (s < GUARD_S) {
          guardChanged++;
          if (maxCh(A, i) > INK_MAX || maxCh(B, i) > INK_MAX) guardNonInk++;
        } else bladeChanged++;
      }
      // Leftover: an original blade pixel that still carries the recruit-sword colour
      // instead of the colour the B asset prescribes for that coordinate.
      if (u >= 0 && u < 96 && v >= 0 && v <= 54 && opA && opB && !d) {
        const cols = itemCols(v);
        if (cols.length) {
          const uc = Math.min(Math.max(u, cols[0]), cols[cols.length - 1]);
          const c = itemPx(uc, v);
          if (c[0] !== B[i] || c[1] !== B[i + 1] || c[2] !== B[i + 2]) leftover++;
        }
      }
    }
    weapon.push({frame: idx, silhouetteChangedPixels: silhouette, changedPixels: changed,
                 guardRegionChangedPixels: guardChanged, guardRegionNonInkPixels: guardNonInk,
                 bladeRegionChangedPixels: bladeChanged, leftoverOriginalBladePixels: leftover,
                 variantAVsSourcePixels: aVsSource});
  }

  // 3. timing preserved
  const durations = JSON.parse(fs.readFileSync(E + '/full/a/frame-durations.json'));
  const durationsB = JSON.parse(fs.readFileSync(E + '/full/b/frame-durations.json'));
  const timingOk = JSON.stringify(durations) === JSON.stringify(clip.durationsMs)
    && JSON.stringify(durationsB) === JSON.stringify(clip.durationsMs);

  // 4. protected trees untouched
  const before = JSON.parse(fs.readFileSync(E + '/protected-before.json'));
  const changedProtected = Object.keys(before).filter(p => !fs.existsSync(p) || hash(p) !== before[p]);
  const added = ['characters', 'assets', 'reports'].flatMap(walk).filter(p => !(p in before));

  // 5. sword assets reused byte-for-byte from Experiment 04
  const assetReuse = {};
  for (const v of ['a', 'b']) {
    for (const ext of ['png', 'aseprite']) {
      const p = `${E}/variants/sword-${v}/sword.${ext}`;
      const q = `${E4}/variants/sword-${v}/sword.${ext}`;
      assetReuse[`sword-${v}.${ext}`] = fs.existsSync(p) && fs.existsSync(q) && hash(p) === hash(q);
    }
  }

  const status =
    reuse.every(r => r.aEqualsSource && r.bEqualsSource && r.aEqualsB && r.rgbaEqual)
    && weapon.every(w => w.silhouetteChangedPixels === 0 && w.guardRegionNonInkPixels === 0
                      && w.variantAVsSourcePixels === 0 && w.leftoverOriginalBladePixels <= 20)
    && timingOk && changedProtected.length === 0 && added.length === 0
      ? 'PASS' : 'FAIL';

  json(E + '/verification.json', {
    status, direction: 'front_r', sourceClip: SRC, sourceClipSha256: hash(SRC + '/clip.json'),
    acceptanceCriteria: [
      'body and handFront byte-identical to the front_r source in both variants',
      'variant A byte-identical to the original weapon layers',
      'variant B never changes the weapon silhouette',
      'variant B never repaints guard-region pixels with a non-ink colour',
      'leftover original-blade pixels <= 20 per frame',
      'frame durations preserved',
      'no file under characters/, assets/ or reports/ changed or added',
    ],
    guardRegionDefinition: `along-axis distance from grip s < ${GUARD_S} px is guard/handle; ink means max channel <= ${INK_MAX}`,
    bodyHandReuse: {comparisons: reuse.length, rows: reuse},
    weaponComparison: weapon,
    timing: {declared: clip.durationsMs, variantA: durations, variantB: durationsB, preserved: timingOk},
    assetReuse,
    protectedFiles: Object.keys(before).length, protectedChanged: changedProtected, protectedAdded: added,
  });
  console.log(JSON.stringify({status, comparisons: reuse.length,
    bodyIdentical: reuse.every(r => r.aEqualsSource && r.bEqualsSource),
    silhouetteChanged: weapon.reduce((s, w) => s + w.silhouetteChangedPixels, 0),
    guardChanged: weapon.reduce((s, w) => s + w.guardRegionChangedPixels, 0),
    guardNonInk: weapon.reduce((s, w) => s + w.guardRegionNonInkPixels, 0),
    leftover: weapon.reduce((s, w) => s + w.leftoverOriginalBladePixels, 0),
    bladeChanged: weapon.reduce((s, w) => s + w.bladeRegionChangedPixels, 0),
    aVsSource: weapon.reduce((s, w) => s + w.variantAVsSourcePixels, 0),
    timelineChanged: changedProtected.length, added, timingOk, assetReuse}, null, 2));
}
