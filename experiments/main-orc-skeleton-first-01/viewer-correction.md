# Correção do visualizador — leia junto com o viewer-brief.md

## O fundo de sobreposição é 256×256, não 128×128

Use como fundo:

`characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/frames/02.png`

Ela tem **256×256**. É a mesma imagem que o PixelLab vai usar como referência, e as frações `x`/`y`
dos JSON são relativas a ela.

- Linha do chão: `y = 190` de 256, fração **0.7422**.
- Ampliação na tela: 2× ou 3×.

Se `poses.json` ou `sequence.json` declararem `reference` apontando para 128, ignore e use a de 256,
registrando a divergência no seu relatório.

## Sobre a ausência dos JSON de movimento

Outro DEV está produzindo `poses.json` e `sequence.json`. Eles podem não existir quando você começar.

Faça assim:

1. Escreva o visualizador contra o esquema do brief.
2. Para conseguir **provar** que a página funciona sem inventar o movimento do outro DEV, crie um
   fixture sintético em `viewer/fixtures/sample-poses.json` e `viewer/fixtures/sample-sequence.json`,
   claramente rotulado como sintético, com um esqueleto simples de teste.
3. A página deve carregar os arquivos reais quando existirem e avisar na tela quando não existirem.
   Um parâmetro de URL `?fixture=1` pode carregar o fixture para demonstração.
4. No relatório, diga explicitamente que o movimento real ainda não existia quando você verificou, e
   que a prova foi feita com fixture.

Nunca embuta uma sequência inventada e apresente como se fosse a do outro DEV.
