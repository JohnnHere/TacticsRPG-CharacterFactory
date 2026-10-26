# Aprovado e adotado como padrão — 2026-10-25

Criador e agente aprovaram o meio-termo. Ele é o Idle selecionado do Infante e a referência artística para novos Idles. Diretriz canônica: docs/IDLE_ART_STANDARD.md; evidência em characters/orc-pixellab-05/source/creator-approval-idle-balanced-v3.json. A decisão substitui o estado de candidata descrito no histórico abaixo.

# Infante de Ferro — terceira opção de Idle

2026-10-25. Pedido: opinião de leitura jogável e criação de um meio-termo entre o anterior e o mais sutil. Nenhuma integração Unity autorizada nesta comparação.

## Terceira candidata

Novo fork Aseprite `characters/orc-pixellab-05/source/aseprite/infante-idle-balanced-v3/`, mestre `source/infante-idle-balanced.aseprite`. O Lua `tools/aseprite/balance-infante-idle-v3.lua` reaproveita poses completas originais 0,1,5,6,7, mantendo os pixels dessas poses exatamente. Head excursion 2 px; tempos 400/450/500/450/400 ms, ciclo total 2200 ms. Fonte de geração herdada: PixelLab animate_image, registrada no clip original; nova intervenção é somente seleção de poses e timing executada no Aseprite, sem geração ou cobrança nova.

| Versão | Oscilação vertical da cabeça | Ciclo | Quadros |
|---|---:|---:|---:|
| Anterior | 4 px | 1,6 s | 8 |
| Mais sutil | 1 px | 2,8 s | 4 |
| Meio-termo | 2 px | 2,2 s | 5 |

As medidas descrevem a cabeça, não amplitude universal do corpo. Nenhuma compressão de tronco, redimensionamento, colagem regional, blend ou perda de detalhes foi introduzida. Clip candidato independente: `characters/orc-pixellab-05/source/studies/IdleCandidates/balanced-v3/clip.json`. O Idle atual sutil e todas as artes anteriores permaneceram intactos. Terceira opinião não implica seleção ou aprovação.

## Opinião de uso

Preferência do agente para Idle normal de combate: meio-termo, por combinar presença visível e menor agitação em grupos. O anterior transmite esforço/tensão; o mais sutil favorece repouso. Julgamento visual de preview, sem alegação de teste em jogo. Confirmar leitura com múltiplas unidades, distância da câmera e transições em futura integração autorizada; não decidir responsividade do gameplay somente pelo número de quadros do Idle.

## Biblioteca e validação

Comparação portátil das três opções em `Biblioteca de Arte/Estudos Comparativos/Infante de Ferro - Idle/index.html`, também acessível no topo do índice principal e nas fichas. Cada versão inclui PNGs, mestre e tempos. Catálogo próprio com 20 hashes de arte. Registro de navegação em `docs/ART_LIBRARY_COMPARISONS.json`, mantido pelo construtor da biblioteca. Atualizar a comparação com `tools/build-infante-idle-options.py`; biblioteca com `tools/build-art-library.py`.

Exportação Aseprite PASS: cinco quadros comparados no build `dist/editor/infante-idle-balanced-v3/fb2f13aed6d3dc12fd29/`. Comparação no navegador PASS: 17 quadros (8/4/5) conferidos, 20 hashes, três canvases, zoom nativo 128, abertura local e mobile sem erros JavaScript. Evidências `reports/orc-idle-balanced-v3/check.json` e `experiments/orc-infante-idle-balanced-v3/check.json`. Biblioteca principal continua com oito Orcs e 16 clipes, seleção atual preservada; ideias futuras e pendência da armadura do Ágil preservadas.

Próximo: criador comparar e escolher uma das três opções; sem seleção automática, produção de armas ou alterações no jogo.
