# Correção da roupa traseira back_r — 2026-10-19

Ferramenta: OpenAI image_gen integrada; modelo não exposto.
Entradas: back_r-generated.png (alvo); back_l-generated.png (consistência da roupa).
Invariantes: corpo, anatomia/assimetrias, facing back_r e mãos vazias. Remover apenas tecido vermelho longo traseiro.
Resultado reconstruído em grade nativa com a mesma receita/paleta da base; versão anterior preservada em source como rejeitada.

## Prompt real

Use case: precise-object-edit for directional game sprite source.
Image 1 is the edit target: Orc Warrior BACK_R view. Image 2 is the BACK_L view of the same individual, serving as reference for the rear outfit only.
Correct ONLY the lower rear clothing of image 1 to match image 2: remove the long red cloth hanging down from the REAR belt. The red scarf around the neck remains. Rear hips should show short brown leather hip panels and dark charcoal trousers, exactly as image 2; there is NO long red rear tabard or cape. The red FRONT tabard remains on the unseen front side.
Preserve image 1's BACK_R direction facing screen right and away, exact body proportions, empty hands, bald olive head, armor, anatomical LEFT metal pauldron and bracer on screen LEFT/far side, anatomical RIGHT bare shoulder and leather bracer on screen RIGHT/near side, harness/backplate, brown boots, pose, palette, pixel-cluster rendering and transparent background. Do not mirror, change facing, add a weapon, enlarge details, change the boots, or change anything outside rear lower clothing. Pixel-art sprite source with coarse clean native-pixel blocks, no antialiasing, no floor shadow, halo or text.
