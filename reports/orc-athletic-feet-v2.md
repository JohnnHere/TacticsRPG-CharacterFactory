# Atlético — limpeza dos pés e Biblioteca de Arte

2026-10-24. Criador avaliou positivamente os estudos atuais e pediu somente correção da sombra clara dos pés do Atlético, mais fluidez e organização dos arquivos. Vídeo `Gravando 2026-10-24 174040.mp4` (2,9 s).

## Retoque local

O defeito era uma franja cinza-clara opaca conectada à transparência externa das botas, variando entre poses. Novo fork da fonte pelo editor-fork: `characters/orc-pixellab-11/source/aseprite/athletic-feet-v2/`. O Lua `tools/aseprite/clean-athletic-foot-fringe.lua`, executado no Aseprite, removeu 106 pixels de matte exterior distribuídos nos oito quadros. Apenas quatro cores verificadas, abaixo de y98 e alcançáveis a partir do fundo transparente, foram removidas. O restante da arte permaneceu idêntico. Fonte anterior/PNGs preservados em `experiments/orc-athletic-feet-v2/before/`; coordenadas e cores removidas em `retouch.json`.

A origem permanece PixelLab Skeleton V3; a intervenção nova é autoria programática local do agente no Aseprite, não desenho manual ou nova geração PixelLab. Nenhuma cobrança nova ou chamada de geração. Não houve alteração raster externa, troca de cabeça, mudança do corpo, novas poses ou mudança do tempo: Walk de oito quadros/100 ms, ciclo 800 ms. A limpeza elimina a borda tremeluzente; o preview pré-carrega os quadros antes de iniciar para evitar engasgos na primeira volta. Não confundir isso com criação de novos intermediários.

## Biblioteca de consulta

Pasta: **Biblioteca de Arte**, na raiz desta fábrica. Entrada: `Biblioteca de Arte/index.html`.

- `Orcs Atuais/<numero - nome>/`: oito Orcs, inclusive os dois Infantes e o Atlético.
- `Conceito/`: PNG; `Idle/Quadros/` e `Walk/Quadros/`: sequência nativa e `clip.json` da ação com os tempos.
- `Mestres Aseprite/`: conceito, Idle e Walk editáveis.
- Cada personagem tem `index.html` e `ORIGEM.json` para navegar e identificar suas fontes.
- `Ideias Futuras/`: Vigia do Passo e Matriarca separados para NPCs e/ou jogáveis exclusivos/únicos, somente conceitos existentes.
- `LEIA-ME.md`: instruções; `catalogo.json`: mapeamento fonte/cópia e SHA256.

São 180 arquivos de arte copiados sem alterar bytes, com os quadros atuais. A biblioteca é uma cópia autossuficiente de consulta/entrega; fontes canônicas e histórico continuam em characters/ e ideas/. Não mover os originais nem quebrar os caminhos da pipeline. Atualizar com `tmp/pixel-venv/Scripts/python.exe tools/build-art-library.py`. O construtor detecta edições diretas na biblioteca antes de sobrescrever arte e preserva entregas anteriores quando a origem muda. V4/07 descartados ficam fora das opções atuais.

## Verificação e limite

`reports/orc-athletic-feet-v2-check.json`: 106 alterações exclusivamente na máscara exterior registrada, corpo e timing preservados, arte não relacionada intacta. `reports/art-library-check.json`: 180 hashes, 200 links locais, oito conceitos, 16 clipes, 144 quadros comparados ao render do navegador, abertura local e layout móvel sem erros JavaScript. `reports/orc-all-review-check.json`: página canônica também atualizada. Doctor e Aseprite disponíveis.

Nenhum arquivo do jogo Unity foi alterado. Próxima etapa sugerida pelo criador será no jogo, em pedido separado. Esta sessão limita-se à correção e organização. Feedback positivo registrado em `reports/orc-study-feedback-2026-10-24.json`; novo retoque continua disponível para avaliação, sem conceder Gates completos ou seleção de produção automaticamente.
