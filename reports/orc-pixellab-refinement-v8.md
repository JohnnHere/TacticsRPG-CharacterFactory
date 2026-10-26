# Reimaginado — Walk V8 em avaliação

Data: 2026-10-24. Nova candidata entregue; **aprovação artística pendente do criador**. V7 rejeitada por cabeça torta e marcha diagonal, conforme vídeo `Gravando 2026-10-24 160109.mp4`. Não promover V7 como referência aprovada.

## O que mudou

O conceito original do 07 está em três quartos. Nas tentativas anteriores houve tanto pedido `south-east` quanto incompatibilidade entre referência visual e poses frontais. Nesta candidata, uma edição de corpo inteiro do próprio conceito produziu primeiro uma referência frontal. Ela preserva a intenção de identidade, paleta oliva/carmesim, roupa e materiais; é uma geração nova, portanto não há garantia de identidade pixel a pixel. O conceito selecionado e o Idle originais permaneceram intactos.

A referência frontal condicionou oito quadros completos do Walk via Skeleton V3. A cabeça foi gerada junto ao pescoço e tronco, sem corte/transplante ou uso de cabeça do Ágil. Ombros, pescoço e cabeça mantêm eixo frontal; os pés têm faixas de apoio separadas. A passada é mais contida que a do Ágil e a vista é frontal, enquanto o guia é em três quartos: isso é uma adaptação, não reprodução idêntica de movimento.

## Como o Ágil foi reutilizado

Os oito quadros atuais do Walk 04 foram enviados somente ao estimador oficial de pontos `POST /v2/estimate-skeleton`, indicado pela documentação do MCP. Os conceitos próprio original e próprio frontal também foram estimados. Dez respostas de 18 pontos preservadas no experimento: uma geração total, 0,1 por chamada.

As fases de avanço/apoio, levantamento dos pés e oscilação do quadril foram medidas no guia e reprojetadas para profundidade frontal, com menor elevação dos pés e anatomia da própria referência. Braços recebem contrafase contida. Olhos/orelhas nivelados e nariz/pescoço no eixo do tronco. Metadados reproduzíveis em `tools/prepare-orc-frontal-v8.py` e `experiments/pixellab-orc-refinement-v8/07-frontal-motion-plan.json`.

**Nenhum pixel do Ágil foi usado pelo modelo que desenha a animação ou a referência frontal.** A geração recebe somente imagem do próprio 07 e poses adaptadas. O estimador de movimento recebeu as imagens do guia; não confundir extração de pontos com condicionamento visual de identidade.

## Pedidos e custos reais — PixelLab Pro ativo

| Operação | Job | Resultado / gerações |
|---|---|---|
| Primeira tentativa Skeleton | `7c92a53d-2a58-4728-8f06-1d37451b161e` | GPU worker descartou; servidor informou zero cobrança |
| Base frontal `edit_image_pro_flash` | `087584eb-369f-4ce2-b777-6baf4fd87cfc` | Concluída, 6 cobradas, seed 8241602 |
| Walk escolhido para avaliação `animate_with_skeleton_v3` | `5435edd1-d91d-49de-831d-5cd7e27a4431` | Concluído, 3 cobradas, seed 8241603 |
| Alternativa `animate_image` | `9a7c5a40-63cc-452a-9e1c-3ac4f5a0a1af` | Concluída, 2 cobradas, seed 8241604; descartada por maior deriva lateral e variação de face/proporção |
| Dez estimadores de pontos | Respostas `*-skeleton.json` | 1 geração total |

Total desta rodada: **12 gerações**, conforme recibos de conclusão e uso dos estimadores. Plano Pro não significa que todo modelo se chame Pro: a base usou Pro Flash; animação escolhida usou Skeleton V3 beta. Pedidos e recibos em `experiments/pixellab-orc-refinement-v8/`, sem credenciais.

## Mestres e preservação

- Referência frontal: `characters/orc-pixellab-07/source/aseprite/walk-frontal-reference-v8.aseprite`.
- Walk: `characters/orc-pixellab-07/source/aseprite/walk-study.aseprite`, oito quadros de 100 ms, ciclo de 800 ms.
- Fonte bruta: `source/pixellab-results/Walk/refinement-v8/`; Skeleton devolve oito quadros reais, sem entrada repetida. A alternativa direta devolveu nove imagens: entrada + oito; não foi selecionada.
- Versão anterior completa: `experiments/pixellab-orc-refinement-v8/before/orc-pixellab-07/`, manifesto SHA256 preservado. Quadros excedentes antigos foram movidos para `source/iterations/pre-v8-extra-frames/Walk/`, fora da sequência ativa.
- Conceito e Idle do 07 conferidos contra snapshot; demais mestres protegidos conferidos. Soldado aprovado, Infante cabeludo, V4 selecionada e Unity preservados.

Geração em nuvem pelo PixelLab; importação, fontes mestre e exportação no Aseprite batch isolado, sem controlar a sessão gráfica do usuário. Não é desenho manual. Nenhuma edição raster externa foi aplicada à arte; ferramentas externas montaram somente apresentações e validações.

## Revisão e limites

Página canônica: [todos os Orcs](orc-pixellab-v4-comparison/review.html). No topo, Ágil e Reimaginado sincronizados em oito quadros/100 ms; abaixo, os 11 conceitos e 18 clipes existentes, incluindo Infante cabeludo. Vigia e Matriarca permanecem ideias de únicos jogáveis ou NPCs, somente conceito nesta etapa.

Conferência Aseprite: oito quadros exportados iguais aos originais gerados, sem alterar pixels visíveis. Conferência do navegador: 154 quadros comparados com PNGs reais, 11 conceitos, 18 clipes, abertura local e layout móvel sem erro JavaScript. Evidências: `reports/orc-pixellab-refinement-v8-check.json` e `reports/orc-all-review-check.json`. Folhas de quadros e captura da comparação em `reports/orc-pixellab-refinement-v8/`.

Essas verificações comprovam integridade e apresentação, não naturalidade perfeita nem aprovação artística. A candidata evita a mistura anterior de orientações, mas a avaliação final de passada, rosto e identidade permanece do criador. Nenhum Gate ou seleção de produção foi concedido automaticamente.
