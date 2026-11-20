# Auditoria antes da autoria

Coordenadas compostas; F03 = índice 03 (quarta pose). Medidas da máscara de luva são diagnóstico de suporte, não identificação automática da palma. Eixo longitudinal t=(-sin θ,cos θ), normal n=(cos θ,sin θ). Valores negativos/positivos indicam lados do cabo.

## Sword

| F | Classe | Fase/ms | Grip V6 | média normal da luva (px) | extensão normal | ajuste de assento |
|---|---|---|---|---|---|---|
| 00 | KEEP | guard/90 | None | None | None | [0, 0] |
| 01 | TARGETED_PIXEL_FIX | anticipation-load/80 | [163, 131] | -0.471 | [-6.067, 4.698] | [0, 0] |
| 02 | TARGETED_PIXEL_FIX | anticipation-lift/80 | [168, 98] | -0.224 | [-5.068, 5.242] | [0, 0] |
| 03 | TARGETED_PIXEL_FIX | chamber/110 | [161, 89] | 1.663 | [-3.302, 6.777] | [1, 0] |
| 04 | TARGETED_PIXEL_FIX | loaded-apex/50 | [166, 95] | 0.917 | [-4.048, 6.222] | [0, 0] |
| 05 | TARGETED_PIXEL_FIX | acceleration/40 | [176, 111] | 0.356 | [-4.409, 4.832] | [0, 0] |
| 06 | TARGETED_PIXEL_FIX | descent/40 | [174, 138] | -0.623 | [-3.424, 2.989] | [0, 0] |
| 07 | TARGETED_PIXEL_FIX | impact/80 | [163, 154] | -0.218 | [-4.832, 5.255] | [0, 0] |
| 08 | TARGETED_PIXEL_FIX | follow-through/100 | [158, 161] | -0.48 | [-4.409, 3.503] | [0, 0] |
| 09 | TARGETED_PIXEL_FIX | recovery-release/90 | [159, 155] | -0.333 | [-3.337, 3.424] | [0, 0] |
| 10 | KEEP | recovery-settle/90 | None | None | None | [0, 0] |
| 11 | KEEP | guard-return/100 | None | None | None | [0, 0] |
## Axe

| F | Classe | Fase/ms | Grip V6 | média normal da luva (px) | extensão normal | ajuste de assento |
|---|---|---|---|---|---|---|
| 00 | KEEP | guard/100 | None | None | None | [0, 0] |
| 01 | TARGETED_PIXEL_FIX | anticipation-load/100 | [164, 129] | -0.222 | [-5.725, 5.04] | [0, 0] |
| 02 | TARGETED_PIXEL_FIX | anticipation-lift/110 | [162, 92] | 0.842 | [-5.158, 6.831] | [2, 0] |
| 03 | TARGETED_PIXEL_FIX | chamber/140 | [156, 84] | 0.39 | [-6.256, 6.951] | [2, 0] |
| 04 | TARGETED_PIXEL_FIX | loaded-apex/150 | [151, 82] | 0.342 | [-6.0, 6.0] | [2, 0] |
| 05 | TARGETED_PIXEL_FIX | acceleration/60 | [161, 93] | 1.291 | [-4.954, 8.396] | [2, 0] |
| 06 | TARGETED_PIXEL_FIX | descent/50 | [172, 128] | -1.47 | [-6.161, 2.658] | [0, -1] |
| 07 | TARGETED_PIXEL_FIX | impact/100 | [163, 159] | -1.355 | [-3.424, 2.553] | [0, -1] |
| 08 | TARGETED_PIXEL_FIX | follow-through/140 | [159, 162] | -0.813 | [-4.192, 2.639] | [0, -1] |
| 09 | TARGETED_PIXEL_FIX | recovery-release/130 | [161, 155] | -1.633 | [-5.255, 0.906] | [0, -1] |
| 10 | KEEP | recovery-settle/110 | None | None | None | [0, 0] |
| 11 | KEEP | guard-return/130 | None | None | None | [0, 0] |

Axe F03/F04: máscara longa longitudinalmente inclui punho/bracelete, mas não define dedos curvados. A projeção do cabo passa pela borda esquerda superior da luva enquanto a massa metálica/punho continua abaixo e à direita; o problema visual é fechamento ausente e leitura de apoio inferior. O cabo já estava em weaponBack: não se trata simplesmente de uma camada frontal errada. A rotação e a posição do pomo não são a causa comprovada. Reparo: assento 2 px para dentro da palma nos frames 02–05, reconstrução local de couro/dedos e polegar em ambas as faces do eixo; impacto/recovery sobem assento 1 px. Nenhuma rotação nova.

Sword: preservar pernas, apoios e tronco (não há justificativa para reconstruí-los neste passe); reforçar fechamento da luva em cada pose, assento de F03 +1 px, preservar progressão angular V6 e diferenciação Sword/Axe. Identidade frontal lida: Sword apex breve/release/contact/follow-through; Axe overhead-coil longo/heavy-impact/weight-settle. Tempos traseiros preservados por contrato. Compatibilidade com back_l V7 fica pendente da outra sessão.