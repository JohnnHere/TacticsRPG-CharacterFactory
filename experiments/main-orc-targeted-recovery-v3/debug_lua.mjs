import { ROOT } from '../../src/core.mjs';
import { checkAseprite, executeAseprite } from '../../src/aseprite.mjs';

const ed = checkAseprite();
try {
  const res = executeAseprite(ed.executable, ['--script', 'experiments/main-orc-targeted-recovery-v3/author_unarmed_all.lua']);
  console.log("STDOUT:", res.stdout);
  console.log("STDERR:", res.stderr);
} catch (e) {
  console.error("CAUGHT:", e.message);
}
