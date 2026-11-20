# V6 — correções frontais localizadas do Orc V1 (checkpoint DEV)

Checkpoint: **V6_FRONTAL_LOCAL_FIXES_READY**. Estado técnico: **TECHNICALLY_COMPLETE**. Estado artístico: **VISUAL_REVIEW_REQUIRED**, `PENDING_CREATOR`. Este DEV não é QA nem orquestrador: a entrega para aqui; integração e QA independente são do orquestrador. Nenhuma aprovação do criador é reivindicada.

## Escopo entregue

Quatro células frontais corrigidas em `characters/orc-v1/source/artistic-reconstruction-v6/frontal/` (cópias integrais; fontes V5 em `combat-rescue-v5/grip-specialist/` permanecem **byte-idênticas** — 316 hashes verificados):

| Célula | Edições | Ilhas removidas | Quadros tocados |
|---|---:|---:|---:|
| front_l/Sword (`front_l-Sword-full`) | 108 | 0 | 13/13 |
| front_r/Sword (`full-front-r-sword`) | 111 | 2 | 13/13 |
| front_r/Axe (`front_r-Axe-full`) | 115 | 2 | 12/12 |
| front_l/Axe (`front_l-Axe-full`) | 111 | 2 | 10/12 |
| **Total** | **445** | **6** | **48** |

Cada célula teve os três mestres atualizados e reabertos/verificados: `source/composite.aseprite` (256, camadas weaponBack/body/weaponFront/handFront), `source/body.aseprite` (256) e `source/native.aseprite` (128). Tempos, coreografia, poses, arma independente, luvas e bookends desarmados preservados (durações asseridas contra os `durationsMs` do V5; camadas weaponBack/weaponFront/handFront byte-idênticas ao snapshot "antes").

## ALVO 1 — axila persistente de front_l/Sword: causa raiz confirmada

Forense estrutural provou primeiro que o corpo da grip-specialist é **byte-idêntico à baseline parental** `combat/front_l/Sword` em todos os 13 quadros (as 4 células idem nas suas direções). O artefato não foi introduzido pelo passe V5: está **herdado na camada body da baseline frontal** e sobreviveu às correções anteriores porque é de 1 pixel.

Duas classes confirmadas na região sob a axila do braço atacante:

1. **Ilha flutuante desconectada `rgba(0,0,1,255)`** — pixel quase-preto, 8-conectividade zero com o corpo, sob a axila do lado do atacante: `front_r/Sword` e `front_r/Axe` F01–F02 em `(25,67)` nativo; `front_l/Axe` F01–F02 em `(102,67)` nativo. 6 instâncias, removidas (alfa 0). Em `front_l/Sword` a ilha não existe; o artefato persistente relatado nesta célula é a classe 2 (ex.: ponto claro `(96,61)` nativo no F00/F12, lado do atacante, sob a axila erguida).
2. **Pontos claros neutros isolados** — L≥170, neutros (Δcanais<45), sem vizinho 4-conectado claro, cor `176..237` cinza-aço sobre armadura escura (L 2–73)/pele verde: 439 instâncias em 48 quadros (21 por quadro de guarda; 1–6 no swing). Incluem os 'W' do rosto/peitoral/ombro nos mapas ASCII.

Correção determinística, 1 pixel por entrada: **mediana dos vizinhos opacos escuros** (L<120; fallback L<160; fallback ink `12,15,18`); ilhas → transparente. Sem escurecimento global, recolor ou cobertura aleatória. Plano em [fixes-plan.json](fixes-plan.json).

## ALVO 2 — contornos claros: confirmados × mantidos

- Varredura L≥185 fora das camadas de arma: **zero clusters** (body e composto) — não há halo grande.
- Com L≥170 neutro e isolado: 439 pixels confirmados e corrigidos. Contextos 5×5 dos pontos de guarda ([forensic5-dot-contexts.txt](forensic5-dot-contexts.txt)) mostram vizinhança escura — nenhum corresponde a specular legítimo (no estilo V1 specular ocorre em arestas/clusters 'l').
- **Mantidos de propósito:** highlights 'l' (140–170) interiores; brilhos metálicos das camadas de arma; 1 pixel por célula em F03 com conexão apenas diagonal ([quasi-floating](fixes-plan.json), chave `quasiFloatingObservations`) — ligado ao corpo por canto, não confirmado como defeito, não corrigido para não arriscar arte legítima.

## ALVO 3 — grip frontal: verificado, nenhum desvio corrigido

Todos os 9 quadros visíveis das duas células Sword e todos os visíveis das duas de Axe têm luva **sobrepondo o cabo** (`min_manhattan=0`, overlap 14–41 px), inclusive `front_r/Sword` (via centro do bbox da luva, pois o clip.json V5 não registra `grip` por quadro nessa célula). Nenhuma edição de grip foi necessária.

## Limitação declarada e método

**Este DEV trabalhou sem percepção de imagem** (limitação conhecida GLM/Cline neste projeto): toda decisão veio de forense textual Pillow (dumps de coordenadas/cores/alfa, mapas ASCII, componentes conectados, persistência temporal, consistência contra baseline parental) + autoria exclusiva em Aseprite Lua batch (`--batch --noinapp`, perfil exclusivo `tmp/aseprite-v6-frontal-profile`; `Frame.duration` em segundos). Pillow atuou **somente leitura/diagnóstico**; as pranchas before/after são montagem de layout (crop/paste 1:1/NEAREST), sem autoria de pixel de produção. O QA independente deve verificar visualmente. Leitura de movimento/estética em 1× não foi realizada por este DEV.

## Verificação executada

| Cheque | Resultado |
|---|---|
| Lua: reabertura dos 3 mestres por célula; asserção pixel a pixel das 445 edições ×3 espaços; durações vs V5 | PASS (445×3) |
| Python independente: diff pós-vs-antes == plano exato (coords+valores) em composto, nativo e body layer; nenhum pixel fora do plano | PASS (48 quadros) |
| Camadas weaponBack/weaponFront/handFront byte-idênticas ao antes | PASS |
| Contratos: composto == alfa-over das camadas; nativo == crop [64,64] do body; groundY nativo 126; bookends sem arma | PASS |
| Strips regenerados: cada tile == quadro correspondente | PASS |
| Preservação V5: 316 hashes gravados no clip.json V5 revalidados intocados | PASS |
| Referências dos 8 clip.json (V5+V6): 0 caminhos quebrados | PASS |
| Contratos V5 pré-cópia (forense 1): composição/crop/hash 100% | PASS |

**Incidente registrado por transparência:** a primeira exportação gravou os compostos em `frames/` (layout do passe rear) em vez da raiz da célula (layout grip-specialist). Detectado pela verificação independente, corrigido em [export-fix.lua](export-fix.lua), pasta espúria removida; estado final revalidado ALL_OK. Mestres nunca ficaram inconsistentes.

## Evidências

- Plano: [fixes-plan.json](fixes-plan.json) · Verificação: [verify-result.json](verify-result.json) · Forenses: [forensic1-inventory.json](forensic1-inventory.json), [forensic2-geometry.json](forensic2-geometry.json), [forensic3.json](forensic3.json), [forensic4-dots.json](forensic4-dots.json), [forensic5-components.json](forensic5-components.json), [forensic5-armpit-windows.txt](forensic5-armpit-windows.txt), [forensic5-dot-contexts.txt](forensic5-dot-contexts.txt)
- Patch: [patch-manifest.json](patch-manifest.json) · Before/after: [before-after-index.json](before-after-index.json) (48 quadros, zoom 3×) · Preview 1×/0,5×/passo/tático: [preview.html](preview.html)
- Autoria: [fix-frontal.lua](fix-frontal.lua), [export-fix.lua](export-fix.lua) (Aseprite 1.3.18.6, batch --noinapp)

## Contabilidade e limites

- **PixelLab: zero chamadas** nesta frente (nenhuma geração, nenhum saldo consumido).
- Sem escrita em `../TacticsRPG`, sem commits, sem promoção, sem integrar Unity. Idle/Walk/Unarmed/Hit/Defeat e retaguardas fora do escopo. O item independente (Sword/Axe V5) não foi alterado.
- Igualdade de pixels/hashes não comprova qualidade artística: a validade visual das 445 correções de 1 px (leitura em escala de jogo, flicker entre quadros) segue pendente de QA visual independente e do criador.

Próximo marco: orquestrador integra as 4 células V6 ao candidato e submete ao QA independente; depois, revisão do criador. **PARE no checkpoint.**

