import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const DIRECTIONS = ['back_l', 'back_r', 'front_r', 'front_l'];
export const now = () => new Date().toISOString();
export const hash = data => crypto.createHash('sha256').update(data).digest('hex');
export const readJSON = p => JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
export function write(p, data) { fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p, data); }
export const json = (p, data) => write(p, JSON.stringify(data, null, 2) + '\n');
export const slash = p => p.split(path.sep).join('/');
export const slug = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
export function id(value) {
  if (typeof value !== 'string' || !/^[a-z][a-z0-9_-]{1,63}$/.test(value)) throw Error('ID: 2-64 caracteres; letra inicial, minusculas, numeros, _ ou -.');
  return value;
}
// Resolve through existing ancestors as well: a symlink must not escape the workspace.
export function inside(root, relative) {
  const base = path.resolve(root), dest = path.resolve(base, relative);
  const isInside = (a, b) => b === a || (!path.relative(a, b).startsWith('..' + path.sep) && path.relative(a, b) !== '..' && !path.isAbsolute(path.relative(a, b)));
  if (!isInside(base, dest)) throw Error(`Caminho fora do pacote: ${relative}`);
  if (fs.existsSync(base)) {
    const realBase = fs.realpathSync(base);
    let ancestor = dest;
    while (!fs.existsSync(ancestor)) ancestor = path.dirname(ancestor);
    // base may be new; only enforce real ancestry when ancestor is below base.
    if (isInside(base, ancestor) && !isInside(realBase, fs.realpathSync(ancestor))) throw Error('Link simbolico fora do pacote.');
  }
  return dest;
}
export function files(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(e => {
    if (e.isSymbolicLink()) throw Error(`Link simbolico nao permitido: ${e.name}`);
    const p = path.join(dir, e.name);
    return e.isDirectory() ? files(p) : [p];
  }).sort();
}
export const pngFiles = dir => files(dir).filter(p => /\.png$/i.test(p));
export const charDir = name => inside(path.join(ROOT, 'characters'), id(name));
export function loadCharacter(name) {
  const dir = charDir(name), spec = readJSON(path.join(dir, 'character.json'));
  if (spec.id !== name || spec.schemaVersion !== 1) throw Error('Ficha incompativel.');
  const p = spec.profile;
  if (!p || !Number.isInteger(p.width) || !Number.isInteger(p.height) || p.width < 1 || p.height < 1 || p.width > 2048 || p.height > 2048) throw Error('Canvas invalido (1..2048).');
  if (p.groundY !== null && (!Number.isInteger(p.groundY) || p.groundY < 0 || p.groundY >= p.height)) throw Error('groundY invalido.');
  if (!(p.ppu > 0)) throw Error('PPU deve ser positivo.');
  for (const [state, count] of Object.entries(p.counts)) {
    if (!/^[A-Z][a-z]+$/.test(state) || !Number.isInteger(count) || count < 1 || count > 16) throw Error('Estado/contagem invalida.');
  }
  for (const recipe of spec.styleRecipes??[]) {
    if(hash(fs.readFileSync(inside(ROOT,recipe.path)))!==recipe.sha256) throw Error('Receita visual versionada alterada.');
    for(const image of recipe.images) if(hash(fs.readFileSync(inside(ROOT,image.path)))!==image.sha256) throw Error('Referencia visual versionada alterada.');
  }
  return { dir, spec };
}
export function expectedSlots(spec, stage = 'full') {
  if (!['base', 'directions', 'full'].includes(stage)) throw Error('stage: base, directions ou full.');
  const prefix = spec.id.replaceAll('-', '_');
  const slots = [`${prefix}_mvp1_static_128.png`];
  if (stage === 'base') return slots;
  slots.push(...DIRECTIONS.map(d => `Directions/${prefix}_dir_${d}.png`));
  if (stage === 'full') for (const [state, count] of Object.entries(spec.profile.counts)) {
    for (const d of DIRECTIONS) for (let i = 0; i < count; i++) slots.push(`Animations/${state}/${state.toLowerCase()}_${d}_${String(i).padStart(2, '0')}.png`);
  }
  return slots;
}
export function assertSlot(spec, slot) {
  if (!expectedSlots(spec).includes(slot)) throw Error(`Slot nao previsto na ficha: ${slot}`);
  return slot;
}
export function digest(spec, dir, gate) {
  let paths = gate === 'concept' ? pngFiles(path.join(dir, 'concepts')) : pngFiles(path.join(dir, 'sprites'));
  if (gate === 'base') paths = paths.filter(p => expectedSlots(spec, 'directions').includes(slash(path.relative(path.join(dir, 'sprites'), p))));
  const refs = readJSON(path.join(ROOT, 'references/manifest.json'));
  return hash(JSON.stringify({ spec, localContracts:['config/style.json','catalogs/races.json','catalogs/jobs.json'].map(p=>[p,hash(fs.readFileSync(path.join(ROOT,p)))]), references: refs.files.map(x => [x.path, x.sha256]), files: paths.map(p => [slash(path.relative(dir, p)), hash(fs.readFileSync(p))]) }));
}
export function approval(spec, dir, gate) {
  const p = path.join(dir, 'reviews.json');
  const last = (fs.existsSync(p) ? readJSON(p) : []).filter(x => x.gate === gate).at(-1);
  return last?.decision === 'approved' && last.digest === digest(spec, dir, gate) ? last : null;
}
export function catalogEntry(kind, query) {
  const list = readJSON(path.join(ROOT, 'catalogs', `${kind}.json`));
  const entry = list.find(e => e.id === query || e.name.toLowerCase() === query?.toLowerCase());
  if (!entry) throw Error(`${kind}: '${query}' nao encontrado. Use catalog --kind ${kind}.`);
  return entry;
}
export const escapeHTML = v => String(v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
