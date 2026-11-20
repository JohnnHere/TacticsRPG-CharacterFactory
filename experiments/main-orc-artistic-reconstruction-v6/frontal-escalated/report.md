# Correção cirúrgica V6-QA-01 — front_l/Sword

TECHNICALLY_COMPLETE · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR.

## Causa raiz e intervenção

A região herdada do V5 contém uma cunha opaca conectada ao contorno do torso, sob a manga do braço atacante em F03–F04 (índices 03/04, arquivos 03.png e 04.png). A comparação RGBA da janela composta [140..154,108..127] confirmou identidade V5/V6 antes da intervenção. Visualmente, a borda inferior da axila avança irregularmente para o espaço negativo; não é ilha flutuante. A limpeza anterior, dirigida a ilhas desconectadas e pontos claros, não corrigia essa geometria. Não há evidência suficiente para atribuir o resíduo a uma pose doadora específica.

Autoria programática em Lua dentro do Aseprite 1.3.18.6, batch --noinapp, perfil exclusivo tmp/aseprite-v6-axilla-profile. Foi retirada a extensão opaca inferior e recomposta uma borda escalonada com INK (12,15,18), articulando o lado do peitoral com a abertura sob o braço. Sem preenchimento retangular, translação, mudança de pose ou alteração de arma. O plano de coordenadas está em edit-plan.json; author.lua aplica no espaço real de cel.position, salva, reabre e exporta os mestres.

## Medições e preservação

| Quadro | Pixels RGBA alterados no corpo | Alterações de alfa | Caixa composta inclusiva |
|---|---:|---:|---|
| F03 | 30 | 23 | 147,116–153,122 |
| F04 | 28 | 20 | 147,115–151,122 |
| F00–F02 e F05–F12 | 0 | 0 | — |

Os 58 pixels alterados estão inteiramente na janela autorizada. Os demais pixels e os vizinhos F02/F05 foram preservados. As três camadas weaponBack/weaponFront/handFront reexportadas do composto reaberto são RGBA idênticas à origem nos 13 quadros. Bookends preservados. Os 328 arquivos de origem do diretório frontal, incluindo os outros três clipes, mantêm SHA-256 idêntico ao snapshot inicial. Nenhuma escrita em Unity; nenhuma geração PixelLab.

Três mestres salvos e reabertos: composite.aseprite (256, quatro camadas), body.aseprite (256), native.aseprite (128). Os 13 tempos foram conferidos em todos: 30/65/35/50/45/65/35/35/100/55/80/45/90 ms = 730 ms. Nenhuma atribuição de duração foi necessária; a API usa segundos. Corpo do composto e body master conferidos pixel a pixel; native master/reexport é recorte exato do corpo em [64,64], sem arma. Ground declarado permanece 190/126. hand.aseprite herdado sem edição.

clip.json contém caminhos novos e hashes reais dos mestres e derivados. patch-manifest.json contém exatamente uma célula. Evidência objetiva: verification.json, reopen-result.json e protected-before.json. Python/Pillow foi usado somente para leitura, medição e montagem/ampliação de previews sem autoria dos sprites.

## Superfície de entrega e limites

- axilla-before-after-8x.png: janela exata antes/depois em 8× para F03/F04.
- before-F03/F04-axilla-8x.png e after-F03/F04-axilla-8x.png: janelas individuais.
- before-13-frames.png e after-13-frames.png: folhas completas de 13 quadros, tempos legendados.
- after-context-F03.png e after-context-F04.png: contexto ampliado.

Inspeção visual local das ampliações realizada para orientar o recorte. Estas conferências são de execução/preservação, não constituem QA independente nem aprovação artística. A aceitação perceptiva e a continuidade em reprodução permanecem para QA e criador. Sem promoção, integração ou alteração de documentos globais. Intervenção encerrada nesta entrega.
