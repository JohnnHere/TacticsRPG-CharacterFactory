# V8 — mapa temporal validado antes de montar os ciclos

| Família | F | Fase | Frontal início/ms | back_r início/ms | back_l início/ms |
|---|---|---|---|---|---|
| Sword | 00 | rest | 0 / 30 | 0 / 30 | 0 / 30 |
| Sword | 01 | body-preparation | 30 / 65 | 30 / 65 | 30 / 65 |
| Sword | 02 | establish-grip | 95 / 35 | 95 / 35 | 95 / 35 |
| Sword | 03 | anticipation | 130 / 50 | 130 / 50 | 130 / 50 |
| Sword | 04 | coil-behind | 180 / 45 | 180 / 45 | 180 / 45 |
| Sword | 05 | apex-hold | 225 / 65 | 225 / 65 | 225 / 65 |
| Sword | 06 | slash-release | 290 / 35 | 290 / 35 | 290 / 35 |
| Sword | 07 | contact | 325 / 35 | 325 / 35 | 325 / 35 |
| Sword | 08 | follow-through | 360 / 100 | 360 / 100 | 360 / 100 |
| Sword | 09 | recoil | 460 / 55 | 460 / 55 | 460 / 55 |
| Sword | 10 | settle-grip | 515 / 80 | 515 / 80 | 515 / 80 |
| Sword | 11 | release-grip | 595 / 45 | 595 / 45 | 595 / 45 |
| Sword | 12 | return-to-guard | 640 / 90 | 640 / 90 | 640 / 90 |
| Axe | 00 | rest | 0 / 40 | 0 / 40 | 0 / 40 |
| Axe | 01 | body-preparation | 40 / 65 | 40 / 65 | 40 / 65 |
| Axe | 02 | establish-grip | 105 / 35 | 105 / 35 | 105 / 35 |
| Axe | 03 | anticipation | 140 / 80 | 140 / 80 | 140 / 80 |
| Axe | 04 | overhead-coil | 220 / 155 | 220 / 155 | 220 / 155 |
| Axe | 05 | cleave-drive | 375 / 35 | 375 / 35 | 375 / 35 |
| Axe | 06 | heavy-impact | 410 / 115 | 410 / 115 | 410 / 115 |
| Axe | 07 | weight-settle | 525 / 110 | 525 / 110 | 525 / 110 |
| Axe | 08 | wrench-recovery | 635 / 130 | 635 / 130 | 635 / 130 |
| Axe | 09 | release-grip | 765 / 50 | 765 / 50 | 765 / 50 |
| Axe | 10 | shoulder-reset | 815 / 90 | 815 / 90 | 815 / 90 |
| Axe | 11 | return-to-guard | 905 / 100 | 905 / 100 | 905 / 100 |

Autoridade: fase pelo índice + relógio acumulado, não contactEvent legado. Sword contato F07/325 ms; Axe heavy-impact F06/410 ms. Os metadados legados dos frontais continuam intactos e estão registrados em temporal-spec.json.

back_l: retirar a abertura/descidas extras do V7; conservar ápice Sword F06→novo F05 e contato F09→novo F07. Uma descida contínua será autorada para Sword F06 e Axe F05 antes de propagar. back_r: pixels selecionados de pegada/contorno preservados; preparação sem arma e poses reaproveitadas na grade.