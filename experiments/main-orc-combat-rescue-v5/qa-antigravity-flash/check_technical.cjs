const fs = require('fs');
const { PNG } = require('pngjs');

function analyzePng(path) {
    if (!fs.existsSync(path)) return { error: 'Not found: ' + path };
    const data = fs.readFileSync(path);
    const png = PNG.sync.read(data);
    let minX = png.width, maxX = -1, minY = png.height, maxY = -1;
    let haloPixels = 0;
    let opaquePixels = 0;

    for (let y = 0; y < png.height; y++) {
        for (let x = 0; x < png.width; x++) {
            const idx = (png.width * y + x) << 2;
            const a = png.data[idx + 3];
            if (a > 0) {
                opaquePixels++;
                if (x < minX) minX = x;
                if (x > maxX) maxX = x;
                if (y < minY) minY = y;
                if (y > maxY) maxY = y;
                const r = png.data[idx];
                const g = png.data[idx + 1];
                const b = png.data[idx + 2];
                if (r > 190 && g > 190 && b > 190) {
                    haloPixels++;
                }
            }
        }
    }
    return { width: png.width, height: png.height, minX, maxX, minY, maxY, opaquePixels, haloPixels };
}

console.log('=== REAR BODY KEYS ===');
const rearDirs = [
    'experiments/main-orc-combat-rescue-v5/body-specialist/back_r-Sword-keys',
    'experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Sword-keys',
    'experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Axe-keys'
];

for (const dir of rearDirs) {
    console.log('\nDir:', dir);
    for (let k = 1; k <= 3; k++) {
        const nativePng = dir + '/0' + k + '-native.png';
        const body256Png = dir + '/0' + k + '-body256.png';
        console.log('  Key ' + k + ' Native:', analyzePng(nativePng));
        console.log('  Key ' + k + ' Body256:', analyzePng(body256Png));
    }
}

console.log('\n=== FRONTAL GRIP CYCLES ===');
const frontDirs = [
    { dir: 'experiments/main-orc-combat-rescue-v5/grip-specialist/front_l-Sword-full', frames: 13, hidden: [0, 1, 11, 12], visible: [2, 10] },
    { dir: 'experiments/main-orc-combat-rescue-v5/grip-specialist/front_r-Axe-full', frames: 12, hidden: [0, 1, 9, 10, 11], visible: [2, 8] },
    { dir: 'experiments/main-orc-combat-rescue-v5/grip-specialist/front_l-Axe-full', frames: 12, hidden: [0, 1, 9, 10, 11], visible: [2, 8] }
];

for (const f of frontDirs) {
    console.log('\nDir:', f.dir);
    console.log('  Native Strip:', analyzePng(f.dir + '/native-strip.png'));
    console.log('  Composite Strip:', analyzePng(f.dir + '/composite-strip.png'));
    for (let i = 0; i < f.frames; i++) {
        const frameStr = (i < 10 ? '0' : '') + i + '.png';
        const p = f.dir + '/' + frameStr;
        const res = analyzePng(p);
        const isHidden = f.hidden.includes(i);
        console.log('  Frame ' + i + (isHidden ? ' (hidden)' : ' (visible)') + ':', { maxY: res.maxY, haloPixels: res.haloPixels });
    }
}
