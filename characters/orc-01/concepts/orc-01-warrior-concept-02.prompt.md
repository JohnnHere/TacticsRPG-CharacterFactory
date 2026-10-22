# Registro do prompt — Orc Warrior concept 02

- Ferramenta: OpenAI image_gen (ferramenta integrada da conversa)
- Modelo: não exposto pela ferramenta
- Entrada: `concepts/orc-01-warrior-concept-01.png` — revisão de arte existente
- Referências de projeto: âncora global de estilo e piloto como referência de leitura/implementação, preservadas no handoff
- Saída: conceito isolado, fundo transparente; ambas as mãos vazias
- Objetivo: remover a arma do conceito base. O machado não foi criado como asset separado nesta revisão.

## Prompt enviado

```text
Use case: precise-object-edit
Asset type: revised Orc Warrior character concept/reference art for a tactical RPG.
Input image: Image 1 is the current Orc Warrior concept and is the edit target.
Primary request: Remove the battle axe from the character so the concept shows the weapon-independent character asset. The character's right hand should be empty, in a natural relaxed but ready pose, with no object.
Change only: erase the entire axe head, haft, and any weapon pixels, then adjust only the right hand and wrist slightly if needed so they read naturally empty-handed. Preserve the transparent background.
Keep unchanged: the Orc's face, hair, tusks, body proportions, armor, asymmetric shoulder plate, red cloth, palette, boots, pose, expression, pixel-art rendering, shading, canvas framing, and transparent background. Preserve the same established character identity and overall silhouette as much as possible.
Constraints: no weapon in either hand; no sword, axe, shield, bow, staff, scabbard, holster, or weapon silhouette; do not add replacement gear, effects, text, scenery, extra props, or characters. This is a character-base concept; weapons are authored as separate assets and are only shown when equipped and invoked by an action.
Avoid: redesigning the character, changing outfit colors or armor, changing anatomy, adding empty holsters, soft repainting, blur, 3D, or any changes outside the requested weapon removal.
```
