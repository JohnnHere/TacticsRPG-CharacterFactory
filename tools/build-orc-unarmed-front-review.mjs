import fs from 'node:fs';import path from 'node:path';import {ROOT,readJSON} from '../src/core.mjs';
// Reuse the already exercised viewer, adapting its data source and review text.
let source=fs.readFileSync(path.join(ROOT,'tools/build-orc-combat-front-review.mjs'),'utf8');
const first=source.indexOf('const classes='),end=source.indexOf('const data=',first);
source=source.slice(0,first)+"const classes=readJSON(path.join(ROOT,'characters/orc-unarmed-front-review-data-v1.json')).classes;\n"+source.slice(end);
source=source.replace('orc-combat-front-validation-v1.json','orc-unarmed-front-review-data-v1.json');
source=source.replace('counts:{Attack:5,Hit:3,Defeat:5},durations:{Attack:90,Hit:80,Defeat:120}','counts:{Attack:5},durations:{Attack:90}');
source=source.replace('Orc — primeiro lote de combate','Orc — ataque básico desarmado').replace('Orc — combate front_r','Orc — ataque básico desarmado front_r');
source=source.replace('<strong>Attack5, Hit3 e Defeat5 nas sete classes:</strong> 91 quadros novos e 21 clipes editáveis. As quatro vistas de Idle/Walk já estão aprovadas e foram preservadas. Revise este primeiro lote de combate antes das outras vistas.','<strong>Um golpe físico comum nas oito roupas, incluindo Warrior.</strong> Primeiro lote front_r:30 quadros novos, seis fontes editáveis novas e dez quadros reutilizados de Warrior/Brawler. Os clipes de magia, arco e demais gestos anteriores foram preservados.');
source=source.replace('Os gestos de ataque variam por classe. Os sprites mostram corpo e roupa, com mãos vazias; armas, projéteis e efeitos são assets separados ainda pendentes. Confira preparação, gesto principal, recuperação, mão dominante, reação ao impacto e queda. Total atual: 406 PNGs e 105 fontes editáveis ativas; faltam 273 quadros nas outras vistas de combate.','Este é o comando normal Atacar SEM arma: guarda, preparação, soco e recuperação; não é habilidade ou conjuração. Revise roupa, mão ativa, giro do tronco e continuidade. Warrior e Brawler reaproveitam as quatro vistas existentes; faltam90 quadros nas outras três vistas das seis roupas após esta revisão. Armas e integração Unity continuam pendentes.');
source=source.replace('<option>Attack</option><option>Hit</option><option>Defeat</option>','<option>Attack</option>');
source=source.replace('Revisão artística pendente','Revisão do golpe desarmado');
source=source.replace('/reports/combat-front-v1.json','/source/unarmed-front-v1-review.json');
source=source.replace('orc-combat-front-editor-v1.json','orc-unarmed-front-validation-v1.json').replace('review-orc-locomotion-directions-v1.html','review-orc-basic-complete-v1.html').replace('Locomoção aprovada','Baseline de cinco estados preservada');
source=source.replace('review-orc-combat-front-v1.html','review-orc-unarmed-front-v1.html');
source=source.replace("console.log('Combat front_r preview:91 frames,21 clips,3 states,7 classes.');","console.log('Unarmed front_r preview:40 frame references,8 outfits;30 new PNGs,6 new editables.');");
// Evaluate the trusted local builder in a sibling module, preserving its relative imports.
fs.writeFileSync(path.join(ROOT,'tools/build-orc-unarmed-front-review.generated.mjs'),source);
await import('./build-orc-unarmed-front-review.generated.mjs?'+Date.now());
