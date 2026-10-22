# Tentativa 02 de base — 2026-10-19

Ferramenta: OpenAI image_gen integrada. Modelo: não exposto.
Referências: concept-07 para identidade; piloto nativo para escala.
Objetivo: desenho de aproximadamente 100 pixels em canvas maior, permitindo somente recorte sem reescala.
Resultado: rejeitado. Canvas 1420x1108; conteúdo visível maior que 128x128; 38235 cores e 76427 pixels com alfa parcial no PNG. Sem alteração dos pixels originais.

## Prompt real

Create a single TINY native pixel-art game sprite surrounded by a HUGE empty transparent canvas.
This is NOT a concept illustration. It is a 100-pixel-tall game character. Do not enlarge him to fill the image.
Composition requirement is paramount: the sprite occupies only the central 8 percent of image height and 6 percent of image width. Over 99 percent of image area is EMPTY transparent background. Keep vast transparent margins on all four sides. The full image may be large; only the tiny central sprite will be cropped into a native 128x128 PNG without scaling. Thus actual visible character must be 95-102 ACTUAL IMAGE PIXELS tall and less than 90 pixels wide. Center the tiny figure precisely.
Draw new native pixel clusters at that actual scale: crisp single-image-pixel dark contour, solid opaque cluster colors, no partial transparency, no fine painted texture or antialiasing. About 32 colors. There is no magnified preview, border, inset, text or grid.
Reference image 1 defines ONLY character identity and outfit: bald olive Orc Warrior, mature brutal wide face, lower tusks, black brows, muscular broad shoulders, iron breastplate, crossed brown leather straps, red scarf and torn front tabard, large iron pauldron on anatomical left shoulder (screen right), asymmetric bracers, boots and knee plates. Reinterpret detail for tiny sprite clarity, do NOT paste or reduce the illustration. Reference image 2 is native pilot for actual pixel cluster quality and compact tactical proportions ONLY, not its sword or clothes.
One front_r three-quarter view, face looking screen right, whole body and both boots. Balanced idle stance, fists empty. No weapon held/carried/sheathed, no shield, no cape, no props, no shadow. Entire background truly transparent.
Again, a minuscule 100-image-pixel tall sprite in a huge empty transparent square, NOT a full-image large character illustration.
