# Orc — quatro vistas das sete roupas

Pedido e evidencia de aprovacao parcial: "Aprovo as sete bases; produza as outras vistas." Registrado em cada source/native-base-v1/front-r-review.json, com SHA256 da base front_r aprovada. Essa evidencia nao aprova automaticamente as outras vistas ou animacoes. Nenhum Gate base completo foi autoaprovado.

## Producao executada

Sete folhas novas image_gen com front_l/back_r/back_l, uma por classe, e tres correcoes individuais: frontal esquerda do Squire (original repetiu front_r), traseira esquerda do Mage (original repetiu back_r) e lado do no da faixa do Brawler back_l. As fontes rejeitadas parcialmente permanecem preservadas; generation.json e extraction.json registram a selecao real de cada vista. Foram dez chamadas, em vez de gerar cada uma das 21 vistas isoladamente. O modelo exato nao foi exposto pela ferramenta.

O guia de pose compartilhado characters/orc-direction-pose-guide-v1.png reune os tres PNGs nativos correspondentes do Warrior aprovado, somente como referencia de orientacao, com copia por composicao local sem espelhamento ou reescala dos pixels finais. A roupa de cada classe vem do seu conceito e da sua base aprovados. O guia nao e uma fonte runtime de outras roupas. A primeira folha Squire nao utilizou esse guia; os metadados preservam as referencias e prompts efetivamente usados em cada chamada.

As tres figuras de cada folha foram isoladas por componentes de alpha; correcoes selecionadas substituem apenas a fonte da vista indicada. Cada pose passou pelo processo existente de grade alvo explicita Pixel Art Fixer (forced), paleta da propria base front_r e registro inteiro. Nao se reduziram conceitos nem se espelharam sprites para preencher direcoes.

## Inventario e conferencia

- 21 PNGs novos, completando 35 PNGs estaticos (7x fallback + quatro vistas), 128x128 RGBA8, altura100, ground126, alfa parcial zero.
- Todos os novos pixels de cor pertencem a paleta da propria roupa aprovada; 47–48 cores por pacote. As sete bases front_r e fallbacks aprovados permanecem byte a byte intactos.
- Sete validacoes directions: total175 PASS, zero FAIL, sete avisos esperados (fallback igual a front_r). Unity NOT_RUN e revisao humana pendente.
- 28 fontes raster editaveis .aseprite (sete frontais existentes e 21 novas). Todas foram abertas/exportadas pelo LibreSprite 1.3 e comparadas em RGBA: pixels identicos. Nao sao roupas separadas/rig.
- Cada conjunto tem quatro imagens distintas e nenhum par de pixels exatamente espelhados. Esse teste complementa a inspecao artistica, sem provar por si so consistencia de anatomia ou acessorios.
- Preview local Edge headless: 28 imagens carregadas, sete filtros de classe, zoom1x/2x/3x e fundo testados, zero erros JavaScript.

Preview: ../characters/review-orc-directions-v1.html. Inventario e hashes: orc-directions-review-inventory-v1.json em characters/. Relatorios adicionais: orc-directions-import-verification-v1.json, orc-directions-editor-verification-v1.json e orc-directions-review-browser-v1.json/.png. Cada pacote conserva reports/directions-validation-v1.json.

## Fontes e continuacao

Novas fontes em characters/orc-01-<job>/source/directions-v1/: sheet.png, prompt real, generation.json, correcoes quando existentes e subpastas front_l/back_r/back_l com pose-source.png, native.png, native-4x.png, relatorio de processamento, extraction.json e view.aseprite. Fontes/frontais anteriores em source/native-base-v1/. Sprites importados pelo CLI em sprites/Directions/.

Ferramentas reutilizadas: tools/recover-native-sprite.py, write-static-editable.py, CLI import/validate/preview. Novos auxiliares: prepare-orc-direction-sheets.mjs, extract-direction-sheet.py, import-orc-directions.mjs e build-orc-direction-review.mjs. O preparador preserva prompts/referencias reais quando a fonte gerada ja existe; o extrator bloqueia sobrescrita de candidato nativo existente.

Proxima etapa: decisao explicita do criador sobre as quatro vistas; so entao registrar Gate base de cada pacote aprovado e iniciar Idle/Walk por lotes, seguindo depois para acoes adequadas ao Job. Restam 644 quadros animados no inventario baseline (7x92); disparo, casts e sincronizacao de armas exigem trabalho especifico, nao um soco Warrior recolorido. Export e integracao Unity continuam pendentes.
