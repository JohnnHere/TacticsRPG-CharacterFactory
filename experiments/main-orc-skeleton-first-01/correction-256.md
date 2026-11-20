# Correção de contrato — leia isto antes de gravar qualquer JSON

Duas mudanças. Elas não se contradizem com o resto do brief; substituem apenas o que citam.

## Mudança 1 — o espaço de coordenadas é 256×256, não 128×128

O criador autorizou gastar créditos do PixelLab, então as poses serão convertidas em arte real por
`animate_with_skeleton_v3`. Isso obriga a unificar o espaço.

A imagem de referência que o PixelLab vai usar é:

`characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/frames/02.png`

Ela tem **256×256**, o corpo está deslocado em `bodyOffset [64,64]` e o chão fica em `groundY 190`.

Portanto expresse **todas** as frações `x`/`y` em relação a essa imagem de 256×256, com `y` para
baixo. O chão é a fração `y = 190/256 = 0.7422`. Não converta depois: gere já nesse espaço.

Se você já gravou algo em 128, a conversão é:

- `x256 = 0.25 + 0.5 × x128`
- `y256 = 0.25 + 0.5 × y128`

Registre no relatório se precisou converter.

## Mudança 2 — a pose 0 tem de corresponder à imagem de referência

`02.png` é o quadro `establish-grip`, já armado. O provedor avisa que um esqueleto que não
corresponde à imagem "custa transparência e precisão de cor silenciosamente".

Então o esqueleto da **pose 0 (`ready`)** deve descrever a postura que **aquele corpo já está**, e a
sequência parte dela. As outras quatro poses continuam sendo antecipação, golpe, seguimento e
recuperação.

## O que não muda

Tudo o mais do `motion-brief.md` continua valendo: cinco poses, dezesseis rótulos COCO-18 exigidos
mais os dois olhos e as duas orelhas, punho = `RIGHT ARM`, `LEFT`/`RIGHT` do personagem, `z_index`,
`depth` opcional, campos de empunhadura obrigatórios, quatorze quadros em `sequence.json` na grade de
730 ms com as fases do `clip.json`, e as sete metas mensuráveis.

## O que você deve fazer agora

1. Ler `characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/frames/02.png` e medir nele onde
   estão cabeça, ombros, cotovelos, punhos, quadris, joelhos e tornozelos, para a pose 0 ficar fiel.
2. Gravar `poses.json` e `sequence.json` no espaço de 256×256.
3. Escrever o `report.md` com as tabelas pedidas.

Não chame PixelLab. A chamada é minha, depois que eu revisar suas poses.
