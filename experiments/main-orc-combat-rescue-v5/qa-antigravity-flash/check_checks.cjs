const fs = require('fs');
const { PNG } = require('pngjs');

function compareLayers(frontDir, hiddenFrames, visibleInterval) {
    const checks = JSON.parse(fs.readFileSync(frontDir + '/checks.json', 'utf8'));
    console.log(frontDir, 'checks summary:');
    console.log('  bodyRgbaDeltaAllFrames:', checks.bodyRgbaDeltaAllFrames);
    console.log('  hiddenFramesClean:', checks.hiddenFramesClean);
    console.log('  gripConnectedAllVisible:', checks.gripConnectedAllVisible);
    console.log('  allGroundYExact:', checks.allGroundYExact);
}

const frontDirs = [
    'experiments/main-orc-combat-rescue-v5/grip-specialist/front_l-Sword-full',
    'experiments/main-orc-combat-rescue-v5/grip-specialist/front_r-Axe-full',
    'experiments/main-orc-combat-rescue-v5/grip-specialist/front_l-Axe-full'
];

for (const d of frontDirs) {
    compareLayers(d);
}
