# Sword frontal — candidato local

Status artístico: `VISUAL_REVIEW_REQUIRED`, `PENDING_CREATOR`.
Status técnico: `TECHNICALLY_COMPLETE`.

As duas células estão em `characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_r-sword` e `front_l-sword`. Cada uma contém 14 quadros, quatro camadas, quatro mestres Aseprite, PNGs compostos/nativos e strips. As células de origem foram somente lidas. Nenhuma geração por IA, alteração de Axe, commit ou escrita no Unity.

Autoria programática Lua executada no Aseprite 1.3.18.6, preservada em `author-frontal-inbetween.lua`: construção da pose intermediária com clusters da mesma vista, restauração de torso, contorno e sombreamento explícitos de antebraço; arma independente rígida e luva reposicionadas. Sem cross-fade ou interpolação de pixels do corpo. A transformação rígida da arma usa amostragem discreta, sem mistura de cores.

Todos os quadros herdados preservam RGBA de todas as quatro camadas. O maior passo medido do centroide claro da lâmina é 43,3185 px em ambas as direções. O novo corpo contém 15/16 pixels de luminância >=160, acima dos 3 pixels de F05. Não há quadros consecutivos armados idênticos. Revisão artística pelo criador permanece necessária.

**Correção expressa do criador aplicada:** grade final `30,65,35,50,45,35,30,35,35,100,55,80,45,90`, soma 730 ms, contato no índice 8 aos 325 ms. Follow-through preservado em 100 ms. O limite de 45 px aplica-se à nova transição F05→F06; demais passos herdados preservados. A tabela inicial de 700 ms é histórica e superada por essa instrução.

Os oito mestres foram retimados, salvos, reabertos e reexportados no Aseprite. Comparação pixel a pixel confirmou que a correção de timing preservou todas as imagens. Procedência adicional em `retime-frontal-inbetween.lua` e `frontal-inbetween-retime-result.json`. Ambas as células passaram no contrato atualizado. Não há aprovação artística implícita.

Evidências em `frontal-inbetween-verification.json`; verificação dos mestres salvos em `verify-frontal-inbetween.lua`.
