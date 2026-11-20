# Correção da lâmina — tabela verificada

`BLADE = 0,2305` derivado de 59,01 px medidos do cabo à ponta no canvas 96×96 da arma,
desenhada praticamente em escala 1:1 no composto de 256. Chão em `0,7422`.

| Quadro | Fase | Direção antes | Direção depois | Ponta (x, y) | Dentro |
|---|---|---|---|---|---|
| F00 | rest | (0.336, -0.941) | (0.34, -0.94) | (0.758, 0.260) | sim |
| F01 | body-preparation | (0.3351, -0.9422) | (0.34, -0.94) | (0.759, 0.260) | sim |
| F02 | establish-grip | (0.3072, -0.9516) | (0.31, -0.95) | (0.739, 0.250) | sim |
| F03 | anticipation | (0.2659, -0.964) | (0.27, -0.96) | (0.708, 0.231) | sim |
| F04 | coil-behind | (0.1587, -0.9873) | (0.16, -0.99) | (0.633, 0.160) | sim |
| F05 | apex-hold | (0, -1) | (0, -1) | (0.570, 0.051) | sim |
| F06 | apex-descent | (-0.4804, -0.877) | (-0.36, -0.93) | (0.485, 0.105) | sim |
| F07 | slash-release | (-0.9546, -0.2979) | (-0.9, -0.44) | (0.368, 0.297) | sim |
| F08 | contact | (-0.6604, 0.751) | (-0.66, 0.75) | (0.426, 0.681) | sim |
| F09 | follow-through | (-0.3015, 0.9535) | (-0.75, 0.66) | (0.405, 0.691) | sim |
| F10 | recoil | (-0.1158, 0.9933) | (-0.85, 0.53) | (0.399, 0.663) | sim |
| F11 | settle-grip | (0.0721, 0.9974) | (-0.7, 0.2) | (0.382, 0.608) | sim |
| F12 | release-grip | (0.2965, 0.955) | (-0.2, -0.6) | (0.544, 0.330) | sim |
| F13 | return-to-guard | (0.3393, 0.9407) | (0.34, -0.94) | (0.703, 0.334) | sim |

Descida monotônica de F05 a F08: 0.051 → 0.105 → 0.297 → 0.681
