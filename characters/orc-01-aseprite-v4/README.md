# Orc Warrior V4 — retoque da V2 aprovada

**Estudo de animações aprovado e aplicado à produção dos oito Orcs.** [Seleção vigente e documentação](../../docs/ORC_ASEPRITE_V4.md); aprovação específica em reports/animation-approval.json. O conceito deste pacote permanece separado dessa aprovação. Mesmo indivíduo e equipamento, preservando os pixels aprovados da V2. A V3 não foi usada.

- [Comparador V2 × V4](../../reports/orc-aseprite-v4/review.html).
- [Documentação](../../reports/orc-aseprite-retouch-v4.md).
- Mestres: `source/aseprite/retouched/{concept,attack,hit}.aseprite`.
- Instruções dos retoques: `source/aseprite/retouch-v2-to-v4.lua`.

Conceito1254×1254 praticamente preservado: limpeza de alfa≤12 e seis pixels de rebite. Attack5/Hit3 front_r: íris, sombras/reflexos pontuais, redução de tons quase pretos e pose neutra aprovada reutilizada nos retornos. Mesma paleta nativa, contagem e duração dos clipes V2. A alteração das silhuetas de retorno é explícita; demais máscaras são preservadas.

Edição por Lua no runtime do Aseprite sobre arte V2. Não é desenho manual nem nova geração de imagem; a procedência histórica da V2 permanece. V2 original em camadas ocultas conferidas RGBA exatas. Referência/trabalho/retoque não são um rig de corpo/roupa/equipamento.

O script de reprodução regrava os derivados a partir da V2; não executá-lo sobre edições manuais a preservar. Copie a fonte e use o ciclo edição salva/exportação/revisão para a próxima iteração. Gate1 V4 permanece pendente; os clipes são estudos de revisão do design V2 aprovado, não um pacote completo de produção autoaprovado.
