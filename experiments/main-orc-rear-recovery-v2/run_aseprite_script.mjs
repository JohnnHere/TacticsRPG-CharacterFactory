import path from 'node:path';
import { ROOT } from '../../src/core.mjs';
import { checkAseprite, executeAseprite } from '../../src/aseprite.mjs';

const script = process.argv[2];
if (!script) {
  console.error("Usage: node run_aseprite_script.mjs <script.lua>");
  process.exit(1);
}

const ed = checkAseprite();
if (ed.status !== 'AVAILABLE') {
  console.error("Aseprite not available:", ed.error);
  process.exit(1);
}

const fullScript = path.resolve(ROOT, script);
console.log(`Executing Aseprite script: ${fullScript}`);
const res = executeAseprite(ed.executable, ['--script', fullScript]);
console.log("Aseprite finished successfully.");
if (res.stdout) console.log(res.stdout);
if (res.stderr) console.error(res.stderr);
