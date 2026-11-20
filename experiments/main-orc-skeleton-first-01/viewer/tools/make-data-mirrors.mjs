// Gera os espelhos file:// dos JSONs REAIS de movimento para o visualizador.
// Chamada a ser re-executada pelo DEV de motion (ou por você) sempre que
// ../poses.json ou ../sequence.json mudarem:
//   node viewer/tools/make-data-mirrors.mjs
// Se os JSONs reais ainda não existem, grava espelhos vazios (null) para que a
// página carregue por file:// sem erro de rede e avise honestamente na tela.
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const EXP = path.resolve(__dirname, '../..');        // experiments/main-orc-skeleton-first-01
const VIEWER = path.join(EXP, 'viewer');
const DATA = path.join(VIEWER, 'data');
fs.mkdirSync(DATA, { recursive: true });

const POSES_SRC = process.env.POSES_FILE || 'poses.json';
const SEQUENCE_SRC = process.env.SEQUENCE_FILE || 'sequence.json';
const jobs = [
  { src: path.join(EXP, POSES_SRC), out: path.join(DATA, 'poses.js'), globalName: '__SV_DATA_POSES', label: 'poses' },
  { src: path.join(EXP, SEQUENCE_SRC), out: path.join(DATA, 'sequence.js'), globalName: '__SV_DATA_SEQUENCE', label: 'sequence' },
];

for (const job of jobs) {
  if (!fs.existsSync(job.src)) {
    fs.writeFileSync(job.out,
      '// Espelho VAZIO: o JSON real ainda não existe.\n'
      + '// Quando experiments/main-orc-skeleton-first-01/' + job.label + '.json for gravado, rode:\n'
      + '//   node viewer/tools/make-data-mirrors.mjs\n'
      + 'window.' + job.globalName + ' = null;\n');
    console.log('[stub ] ' + path.relative(EXP, job.out) + ' (JSON real ausente)');
    continue;
  }
  let obj;
  try {
    obj = JSON.parse(fs.readFileSync(job.src, 'utf8'));
  } catch (e) {
    console.error('[erro ] ' + job.src + ': JSON inválido — ' + e.message);
    process.exitCode = 1;
    continue;
  }
  const sha = crypto.createHash('sha256').update(fs.readFileSync(job.src)).digest('hex');
  fs.writeFileSync(job.out,
    '// Espelho gerado automaticamente de ' + path.relative(EXP, job.src) + '\n'
    + '// sha256=' + sha + '\n'
    + '// geradoEm=' + new Date().toISOString() + ' · não editar à mão; gere com: node viewer/tools/make-data-mirrors.mjs\n'
    + 'window.' + job.globalName + ' = ' + JSON.stringify(obj, null, 2) + ';\n');
  console.log('[ok   ] ' + path.relative(EXP, job.out) + ' ← ' + path.relative(EXP, job.src) + ' (sha256 ' + sha.slice(0, 12) + '…)');
}
