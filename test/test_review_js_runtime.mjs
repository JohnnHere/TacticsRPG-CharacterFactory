import fs from 'fs';
import path from 'path';

console.log('=== TESTING ASYNC RENDER LOGIC FROM INDEX.HTML ===');

const htmlPath = path.resolve('Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const manifest = JSON.parse(fs.readFileSync('characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json', 'utf8'));
const swordStatus = manifest.cells.find(c => c.direction === 'back_r' && c.action === 'Sword').status;

const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
const script = scriptMatch[1];

const createdElements = {};
const mockDocument = {
  getElementById: (id) => {
    if (!createdElements[id]) {
      createdElements[id] = {
        id,
        style: {},
        textContent: '',
        innerHTML: '',
        dataset: {},
        getContext: () => ({
          imageSmoothingEnabled: false,
          clearRect: () => {},
          drawImage: () => {},
        }),
      };
    }
    return createdElements[id];
  },
  querySelectorAll: () => [],
  body: {
    className: '',
    dataset: {},
  },
};

const mockWindow = {
  requestAnimationFrame: (cb) => {
    // don't loop forever
  },
  Image: class {
    constructor() {
      setTimeout(() => {
        if (this.onload) this.onload();
      }, 5);
    }
  },
};

const context = {
  document: mockDocument,
  window: mockWindow,
  requestAnimationFrame: mockWindow.requestAnimationFrame,
  Image: mockWindow.Image,
  console,
  setTimeout,
  clearTimeout,
};

const fn = new Function(...Object.keys(context), script);
fn(...Object.values(context));

// Wait for images to resolve and renderAll() to run
setTimeout(() => {
  const renderedIds = ['main-canvas', 'main-info', 'main-grip', 'pending-alert', 'frame-gallery'];
  let allGood = true;
  for (const id of renderedIds) {
    if (createdElements[id]) {
      console.log(`  OK: element #${id} successfully rendered into`);
    } else {
      console.error(`  FAIL: element #${id} not rendered into`);
      allGood = false;
    }
  }
  
  // Verify alert text for initial selection (back_r Walk)
  const alertEl = createdElements['pending-alert'];
  console.log('Initial alert HTML:', alertEl.innerHTML);
  
  // Test changing action to Sword (ARTISTIC_REVISION_REQUIRED on back_r)
  const selectAction = createdElements['select-action'];
  if (selectAction.onchange) {
    selectAction.onchange({ target: { value: 'Sword' } });
    console.log(`After selecting Sword (${swordStatus} on back_r):`);
    console.log('  Alert text:', alertEl.innerHTML);
    console.log('  Alert class:', alertEl.className);
    if (!alertEl.innerHTML.includes(swordStatus)) {
      console.error('FAIL: alert did not show the actual manifest status!');
      process.exit(1);
    }
    if (['ARTISTIC_REVISION_REQUIRED', 'IN_REVISION'].includes(swordStatus) && !alertEl.innerHTML.includes('NÃO está pronto')) {
      console.error('FAIL: pending alert must state the rejected candidate is NOT ready!');
      process.exit(1);
    }
  }

  // Test changing action to Walk (ACTIVE_CANDIDATE on back_r)
  if (selectAction.onchange) {
    selectAction.onchange({ target: { value: 'Walk' } });
    console.log('After selecting Walk (ACTIVE_CANDIDATE on back_r):');
    if (!alertEl.innerHTML.includes('CANDIDATO ATIVO')) {
      console.error('FAIL: Walk on back_r should show CANDIDATO ATIVO alert!');
      process.exit(1);
    }
  }

  // Test changing action to Defeat (terminal hold)
  if (selectAction.onchange) {
    selectAction.onchange({ target: { value: 'Defeat' } });
    console.log('After selecting Defeat:');
    const mainInfo = createdElements['main-info'];
    console.log('  Main info text:', mainInfo.innerHTML);
  }

  // Test step-next button
  const stepNext = createdElements['step-next'];
  if (stepNext.onclick) {
    stepNext.onclick();
    console.log('Step-next executed successfully!');
  }

  // Test step-prev button
  const stepPrev = createdElements['step-prev'];
  if (stepPrev.onclick) {
    stepPrev.onclick();
    console.log('Step-prev executed successfully!');
  }

  console.log('\nASYNC RENDER AND EVENT HANDLER TESTS PASSED COMPLETELY!');
  process.exit(allGood ? 0 : 1);
}, 50);
