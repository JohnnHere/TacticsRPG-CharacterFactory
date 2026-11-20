# Postmortem — frente de geração back_l V7

A frente de geração está encerrada por decisão do criador: 23 gerações consumidas, nenhum ciclo produzido por esta frente. O criador informou que a via manual de outra sessão passou os cinco critérios de ápice com custo zero; este registro não constitui revisão independente dessa pose nem aprovação artística. Estado desta frente: `ARTISTIC_REVISION_REQUIRED`.

## Tentativas e contabilidade

Saldo de gerações, não dinheiro. Créditos em USD observados: $0.00. Os saldos intermediários marcados com * são deduzidos dos recibos individuais, não leituras independentes da conta; os limites de cada bloco foram medidos. Uma primeira submissão Sword foi recusada por validação de tamanho do campo `action`, antes da criação de job, sem cobrança.

| Tentativa | Job | Seed | Gerações | Saldo antes → depois | Resultado |
|---|---|---:|---:|---|---|
| Sword 12 poses 128 | `3c317a5e-6d18-40df-8821-916cff08e5ef` | 71031 | 3 | 1282,70 → 1279,70* | Punho elevado fundido/oculto no ombro. |
| Axe 12 poses 128 | `5778d0c6-df27-4c7c-b5d7-7dd1fb939795` | 71032 | 3 | 1279,70* → 1276,70* | Punho elevado não identificável. |
| Sword 12 poses 128, segunda tentativa | `b05b3cb0-7b89-4ef1-a936-7a5c17398dd0` | 71033 | 3 | 1276,70* → 1273,70 | Mão mais separada no ápice; descida/impacto sem cadeia inequívoca. |
| Reconstrução local de membro no Aseprite | Sem job | — | 0 | 1273,70 → 1273,70 | Prova isolada, sem arco até impacto; ver correção do critério abaixo. |
| Skeleton, três poses 256 | `d9170a8b-948a-4571-b1a1-08baebf57674` | 71034 | 2 | 1273,70 → 1271,70 | Luva cortada na borda superior no ápice; palma e punho indistintos no impacto. |
| Inpaint localizado 256 | `5b340119-9828-49ea-8858-9f86cce77044` | 71035 | 10 | 1271,70 → 1261,70 | Braço visível, palma ambígua; sem prova de cadeia ao longo do golpe. |
| Skeleton final, três poses 256 | `b1c5f72d-ba1e-41e3-83e9-33297f978c98` | 71036 | 2 | 1261,70 → 1259,70 | No meio da descida a extremidade virou massa contínua com a braçadeira; palma não identificável. |

Total: 3+3+3+2+10+2 = **23 gerações**, de 1282,70 para 1259,70. Pedidos, recibos e raws estão nesta pasta; `get_image` do último job teve erro de conexão com o banco, mas os três arquivos foram obtidos pelo download direto e o saldo confirmou o custo. Não houve compras.

O primeiro critério de punho acima do topo do crânio foi retirado pelo orquestrador: não se deve usar essa condição para descartar doadores. O critério atual exige ponta da lâmina acima do crânio, punho acima do ombro, antebraço em espaço negativo, cotovelo legível e mão distinguível, sem membro amputado ou duplicado. Nenhuma composição de lâmina foi feita nos testes acima, portanto sua ponta não foi medida. Reavaliar o teste local com o critério corrigido; ele não comprova, sozinho, o arco completo.

## Hipótese técnica

Os raws 128 mostram contorno escuro de braço, luva e espaldeira concorrendo por poucos pixels; a espessura não foi segmentada nem medida. Quando a projeção do membro cruza a cabeça, a espaldeira ou a placa dorsal, o contorno pode se integrar à massa do torso. Os esqueletos fornecem projeções e profundidades, mas não garantem que o modelo reconstrua um volume anatômico contínuo: uma flexão ou distância projetada curta pode colapsar antebraço e cotovelo. A falta de espaço negativo explicitamente planejado agrava a ambiguidade; afastar o punho na segunda tentativa melhorou o ápice, sem resolver a descida. A armadura larga e escura pode ainda competir com a preservação da pose e identidade.

São hipóteses compatíveis com a inspeção, não causas internas comprovadas do modelo. A tentativa 256 mostra que aumentar a resolução sozinho não garante cadeia legível; o ápice anterior foi cortado pelo próprio limite superior do canvas. A regra anterior de punho acima do crânio também distorceu a avaliação: sua falha não prova falha anatômica.

## Doadores e medidas disponíveis

Todas as coordenadas abaixo são **estimativas visuais**, em pixels com origem no canto superior esquerdo, não medições segmentadas ou juntas 3D. Espaldeiras e contornos ocultam as articulações; confirmar manualmente antes de reutilizar.

- Base `raw/sword2/04.png` e doador da mesma vista e indivíduo `raw/sword2/05.png`: recorte distal x=92..108, y=3..32, sem escala, usado em `local-apex-test.aseprite` por `local-apex-test.lua`. Estimativas na composição 128: ombro [84,35], cotovelo [99,35], punho [100,17], palma [97,10], topo do crânio y≈9. Há abertura aparente entre cabeça e antebraço. A classificação anterior de falha por punho abaixo do topo do crânio é superada pelo critério corrigido; a ligação da lâmina e o arco ainda não foram avaliados.
- `characters/orc-v1/source/combat-rescue-v5/body-specialist/02-apex-native.png`: doador da mesma vista inspecionado; antebraço alto junto à cabeça, espaço negativo menos claro. Não foram estabelecidas coordenadas articulares confiáveis; não foi usado no recorte local.
- `characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword/` e `back_l-axe/`: poses da mesma vista inspecionadas como referência, mas os ciclos foram rejeitados pelo criador quanto à técnica; não tratar a técnica V6 como aprovada. Em `experiments/main-orc-artistic-reconstruction-v6/rear/anatomy-plan.json` há regiões de luva e pontos de pegada documentados pela rodada V6, que devem ser verificados nos pixels antes de reutilização.
- Inpaint `inpaint-result.png`, 256: ombro ~[167,64], cotovelo ~[198,70], punho ~[198,37], palma ~[194,22], topo do crânio ~y=17; palma ambígua. Rejeição anterior baseada unicamente na altura em relação ao crânio está superada.
- Job final `raw/apex-final/00.png`, 256: ombro ~[169,64], cotovelo ~[196,76], punho ~[202,41], palma ~[204,30], topo do crânio ~y=19. Punho aproximadamente 23 px acima do centro estimado do ombro; existe abertura aparente. Em F01 o extremo ~[213,80] não permite separar palma e punho; em F02 extremo ~[207,143], cadeia e orientação da palma incertas. A ponta da lâmina não foi testada.

## Recomendação para personagens futuros

Definir primeiro a ação física e os critérios perceptivos por vista e escala de jogo, sem impor geometria inadequada à perspectiva. Antes de pedir uma sequência paga, testar um keyframe de ápice e outro de impacto desarmados, com espaço negativo, cotovelo e palma inspecionados na resolução final; comparar também a transição. Medir e selecionar doadores da mesma vista e do mesmo indivíduo, preservando fontes e registrando recortes e juntas. Se a geração não demonstrar essas condições, mudar o método em vez de repetir lotes; reconstrução manual no Aseprite é uma alternativa demonstrada pelo criador para este caso. Compor o item independente apenas depois, com luva específica de cada pose, e avaliar o arco e a ponta em velocidade e escala reais. Testes técnicos e semelhança de esqueletos não equivalem a aprovação artística.
