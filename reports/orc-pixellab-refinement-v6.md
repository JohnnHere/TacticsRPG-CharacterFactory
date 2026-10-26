# Reimaginado — reparo com identidade própria

Data: 2026-10-24. Estado: **REJEITADA PELO CRIADOR** — vídeo posterior mostrou pescoço desconexo e marcha oscilando para os lados. [Revisão atual com todos os Orcs e novo Walk v7](orc-pixellab-v4-comparison/review.html). [Comparação V6 histórica](orc-pixellab-refinement-v6/review.html). A V5 também foi rejeitada pelo criador por cabeça de aparência alheia, paleta incompatível e inclinação inadequada.

## Restrições vigentes

- Nenhuma imagem ou peça do Ágil entra na criação desta cabeça. A referência de naturalidade não autoriza transferência de feições, crânio ou cor.
- Fontes exclusivamente do próprio Reimaginado 07: Walk anterior às trocas de cabeça e seu reparo frontal anterior, preservados nos históricos v4.
- Cores do reparo ajustadas no Aseprite à paleta exata amostrada da cabeça original do 07.
- Encaixe por quadro acompanha a base do pescoço/cachecol e tronco, não o deslocamento da face lateral antiga.
- Preservar corpo, braços, pernas, passada, tempos, conceito, Idle e demais personagens.

## Execução e procedência

`inpaint_image` pelo MCP oficial, apenas com imagens do próprio 07. Primeira tentativa (`07-OwnHead`) preservou um olhar excessivamente lateral e não foi escolhida como solução final. Foram estudadas duas reconstruções proporcionais no Aseprite a partir do reparo frontal do próprio 07; ficaram como estudos intermediários. Segunda tentativa (`07-OwnAngle`) parte desse estudo próprio para corrigir a orientação sem rosto alheio.

Todos os pedidos/resultados e intermediários estão em `experiments/pixellab-orc-refinement-v6/`. Nenhuma produção raster externa; as alterações de pixels, paleta, composição e mestre são feitas no Aseprite. Scripts em `tools/aseprite/own-head-perspective-v6.lua` e `tools/aseprite/apply-own-head-v6.lua`. A V5 permanece preservada em `before/` com manifesto SHA256.

Nova candidata requer avaliação do criador. Evidência técnica nunca aprova semelhança facial, expressão ou naturalidade do movimento.

## Resultado e limites

Selecionado `07-OwnAngle`, job `663e7a0d-a58d-42c0-b70e-4642b8c49e19`. A peça final foi composta no Aseprite com cores restritas às amostras do próprio rosto original. O encaixe acompanha a base do pescoço/cachecol; deslocamento horizontal máximo nesta sequência é de um pixel para cada lado, em vez dos três pixels herdados da face antiga.

As oito poses e a reprodução renderizada foram inspecionadas. Mestre: `characters/orc-pixellab-07/source/aseprite/walk-study.aseprite`. Mantidos oito quadros de 100 ms. Evidência em `reports/orc-pixellab-refinement-v6-check.json`: exportação exata, zero alterações fora da máscara de cabeça/pescoço, zero cores de cabeça fora da paleta original e fontes protegidas dos demais personagens/conceito/Idle intactas. Captura da comparação em `reports/orc-pixellab-refinement-v6/comparison.png`.

Duas chamadas de reparo MCP retornaram cobrança de dez gerações cada; total reportado de 20 nesta rodada. Nenhuma imagem do Ágil ou de outro personagem foi enviada. Sem nova geração da passada, aprovação automática ou integração Unity. Handoffs, manifesto atual e galeria geral atualizados; página V5 fixada ao seu histórico e marcada como rejeitada.
