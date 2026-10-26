# Infante de Ferro — Idle mais sutil

2026-10-25. Pedido identificado no vídeo `Gravando 2026-10-25 013958.mp4` (2,67 s): Infante de Ferro sem cabelo, pacote 05. Somente o Idle desse personagem foi refinado; o Atlético e demais artes foram preservados.

## Acabamento no Aseprite

Fonte original PixelLab `animate_image`, job `6c7911df-6147-41a0-9cc9-2c2c43ca668f`, oito quadros a 200 ms. Novo fork `characters/orc-pixellab-05/source/aseprite/infante-idle-subtle-v2/`, com fonte original de oito quadros preservada e mestre novo `source/infante-idle-subtle.aseprite`.

O Lua `tools/aseprite/subtle-infante-idle-v2.lua` selecionou as poses completas originais 0,1,6,7, próximas do repouso. Elas limitam a oscilação vertical da cabeça a 1 px, frente aos 4 px do ciclo original. Tempos 650/750/750/650 ms: ciclo de 2800 ms, antes 1600 ms. É redução da amplitude por seleção das poses, além de ajuste de cadência. Não houve redimensionamento, compressão de faixas do tronco, blend/transparência, colagem de cabeça ou alteração dos pixels dessas poses.

Nenhuma geração nova, chamada PixelLab ou cobrança. Procedência herdada preservada: edição de timeline programática do agente executada no Aseprite, não desenho manual novo. Conceito, Walk e armadura não foram redesenhados. A escolha estética continua disponível para avaliação do criador.

## Recuperação e revisão

Snapshot de metadados/PNGs/mestre original em `experiments/orc-infante-idle-subtle-v2/before/`. Quadros antigos excedentes saíram da sequência ativa para `source/iterations/pre-subtle-idle-v2/`. A biblioteca arquiva as cópias anteriores em `Biblioteca de Arte/Historico de Entregas/`; não deixa PNGs obsoletos nas pastas de quadros ativas. O construtor confere hashes e preserva cópias editadas pelo usuário.

Comparação anterior × sutil: `reports/orc-idle-subtle-v2/review.html`. Biblioteca atualizada em `Biblioteca de Arte/index.html`; todos os oito Orcs/16 clipes e Vigia/Matriarca na área separada de ideias futuras. A pendência de melhorar a armadura do Ágil foi preservada.

## Validação

Exportação Aseprite: quatro quadros comparados, PASS; build `dist/editor/infante-idle-subtle-v2/5fcd7b54640283071756/`. Pixel-a-pixel: novas poses iguais às fontes selecionadas. Arte protegida conferida em `reports/orc-idle-subtle-v2/check.json`. Biblioteca: 176 hashes, 200 links locais, 140 quadros comparados ao canvas, abertura local/mobile e zero erros JavaScript, conforme `reports/art-library-check.json`.

Nenhuma arma produzida e nenhum arquivo Unity alterado. Próximo: criador avaliar sutileza do Idle antes de passar ao machado; nenhum Gate ou produção completa promovidos automaticamente.
