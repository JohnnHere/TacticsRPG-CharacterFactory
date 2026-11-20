const fs = require('fs');
const { PNG } = require('pngjs');

const cycles = [
    { name: 'back_r-Sword-full', dir: 'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/native' },
    { name: 'back_l-Sword-full', dir: 'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/native' },
    { name: 'back_l-Axe-full', dir: 'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/native' },
    { name: 'full-back-r-axe', dir: 'characters/orc-v1/source/combat-rescue-v5/body-specialist/full-back-r-axe/native' }
];

for (const c of cycles) {
    console.log(`\n=== ${c.name} ===`);
    for (let i = 0; i < 12; i++) {
        const frameStr = (i < 10 ? '0' : '') + i + '.png';
        const p = `${c.dir}/${frameStr}`;
        if (!fs.existsSync(p)) {
            console.log(`  Frame ${i}: NOT FOUND`);
            continue;
        }
        const data = fs.readFileSync(p);
        const png = PNG.sync.read(data);
        let halo = 0;
        let brightPixels = 0; // r > 180, g > 180, b > 180
        let maxY = -1, minY = png.height, minX = png.width, maxX = -1;
        let totalOpaque = 0;

        for (let y = 0; y < png.height; y++) {
            for (let x = 0; x < png.width; x++) {
                const idx = (png.width * y + x) << 2;
                const a = png.data[idx + 3];
                if (a > 0) {
                    totalOpaque++;
                    if (y > maxY) maxY = y;
                    if (y < minY) minY = y;
                    if (x < minX) minX = x;
                    if (x > maxX) maxX = x;
                    const r = png.data[idx];
                    const g = png.data[idx + 1];
                    const b = png.data[idx + 2];
                    if (r > 190 && g > 190 && b > 190) halo++;
                    if (r > 180 && g > 180 && b > 180) brightPixels++;
                }
            }
        }
        console.log(`  Frame ${i} (${frameStr}): maxY=${maxY}, minX=${minX}, maxX=${maxX}, opaque=${totalOpaque}, halos=${halo}, bright=${brightPixels}`);
    }
}
