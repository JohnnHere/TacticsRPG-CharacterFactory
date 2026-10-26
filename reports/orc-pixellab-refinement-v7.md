# Reimaginado — caminhada completa e revisão de todos os Orcs

Data: 2026-10-24. **REJEITADA PELO CRIADOR**: cabeça ainda inadequada e marcha diagonal. O próprio pedido técnico da V7 usava south-east; isso não atendia ao ajuste frontal esperado. [Abrir todos os Orcs: conceito, Idle e Walk](orc-pixellab-v4-comparison/review.html). Rodada corretiva seguinte em `reports/orc-pixellab-refinement-v8.md`.

## Pedido e diagnóstico

O vídeo do criador (`Gravando 2026-10-24 153812.mp4`, 4 s/30 fps) mostra pescoço desconexo e marcha mudando de orientação de um lado para o outro. As revisões anteriores de cabeça preservaram um ciclo corporal que também estava inadequado. O pedido atual autoriza corrigir o Walk completo; a antiga regra de preservar aquela passada não se aplica a este caso.

## Produção da nova caminhada

Usado o MCP oficial nativo **`animate_with_skeleton_v3` (beta)**, com **apenas o conceito original do próprio Orc 07** como imagem de entrada. Nenhuma imagem do Ágil ou de outro personagem foi fornecida. Cabeça, pescoço e corpo foram desenhados em conjunto em cada quadro, sem recorte ou enxerto de cabeça e sem compressão de faixas do tronco.

O agente anotou os 18 pontos COCO-18 da pose de referência e definiu 12 poses específicas deste corpo. O plano fixa os centros horizontais dos quadris e a relação entre cabeça/pescoço/ombros, com orientação south-east. As botas percorrem faixas separadas e avançam/recuam no mesmo vetor; o pé em balanço levanta, enquanto o outro sustenta o corpo. Braços têm balanço oposto e o tronco sobe/desce discretamente. Isso é um plano específico deste Orc, não um rig racial universal.

Job `d74b8d98-ddb7-43b3-a5c3-967b6ea53504`; recibo retornou **3 gerações cobradas**. Fonte, pedido, pontos e recibos em `experiments/pixellab-orc-refinement-v7/`. Foram retornados exatamente **12 quadros completos**, sem eco da imagem de entrada. O empacotador Aseprite recebeu `firstImageIsReference:false`, preservando todos os quadros sem descartar a primeira pose.

Mestres em `characters/orc-pixellab-07/source/aseprite/walk-study.aseprite` e `walk-raw.aseprite`; PNGs atuais e manifesto em `source/studies/Walk/`; saídas brutas e cópia da referência em `source/pixellab-results/Walk/refinement-v7/`. Autoria generativa PixelLab; composição dos mestres/exportação no Aseprite. Tempos autorados para revisão: **12 × 90 ms = 1080 ms por ciclo**. PNGs gerados não foram alterados durante o empacotamento.

O plano de poses controla a direção desejada, mas a geração é probabilística. A sequência completa, os detalhes do pescoço e a reprodução foram inspecionados; avaliação artística e naturalidade continuam sob julgamento do criador. Não apresentar métricas de arquivo como prova de aprovação artística.

## Galeria conjunta permanente

A página canônica agora mostra **11 conceitos e 18 clipes existentes**, com conceito, Idle e Walk visíveis simultaneamente em cada cartão:

1. Orc Warrior V4 selecionado.
2. Veterano da Vanguarda.
3. Quebra-Linhas.
4. Campeão de Bronze.
5. Veterano Ágil.
6. Infante de Ferro atual.
7. Soldado da Vala — aprovação do criador preservada no seu escopo.
8. Veterano V4 Reimaginado — Walk v7 em revisão.
9. Vigia do Passo — ideia de personagem único jogável ou NPC.
10. Matriarca da Cinza — ideia de personagem único jogável ou NPC.
11. Infante de Ferro — Cabeleira Negra, com seu conceito, Idle e Walk de 16 quadros preservados.

Vigia e Matriarca têm apenas os conceitos solicitados originalmente: os painéis Idle/Walk informam que esses movimentos não foram produzidos, sem simulação. Links históricos dão acesso às revisões anteriores, ao laboratório de cinco conceitos Aseprite e às variantes de Job da produção V4.

**Reconstrução:** `node tools/build-orc-all-review.mjs`. Esse é o construtor canônico da revisão conjunta, usando o extrator histórico `build-pixellab-v4-comparison.mjs` internamente. Ponteiro separado de produção: `reports/orc-study-current-review.json`. Não alterar a seleção de produção para atualizar uma página de estudos.

## Conferência e continuidade

- `reports/orc-pixellab-refinement-v7-check.json`: mestre/12 quadros/tempos exportados exatamente, snapshot anterior preservado e mestres protegidos dos demais personagens/conceito/Idle intactos.
- `reports/orc-all-review-check.json`: 11 conceitos carregados, 18 animações, 158 comparações RGBA no navegador; Infante cabeludo incluído; abertura local e layout móvel conferidos; zero erros JavaScript.
- Folhas de poses, ampliação diagnóstica do pescoço e capturas da página em `reports/orc-pixellab-refinement-v7/`. As ampliações são previews, não pixels de produção.

Só o Walk 07 foi substituído. Conceitos, demais Idles/Walks, aprovação do Soldado, ideias de personagens únicos e seleção de produção V4 foram preservados. V6 marcada como rejeitada e fixada ao histórico. Nenhuma integração Unity, aprovação automática ou alteração de direção artística no repositório principal.
