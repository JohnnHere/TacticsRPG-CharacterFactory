# Reimaginado — proporção e olhar natural

Data: 2026-10-24. **REJEITADO PELO CRIADOR.** [Abrir comparação animada com o Ágil](orc-pixellab-refinement-v5/review.html).

O criador rejeitou a cabeça excessivamente grande e a expressão frontal de encarar a câmera na revisão anterior. Indicou o Veterano Ágil como referência de caminhada natural. A instrução anterior “full frontal, two equally visible eyes” foi uma sobrecorreção do agente, não um requisito do criador.

O criador rejeitou esta candidata por parecer cabeça de outro personagem, estar torta e usar paleta incompatível. A afirmação anterior de preservação satisfatória da identidade não foi sustentada pela revisão humana. Não reutilizar esta peça. Nova correção em andamento a partir exclusivamente do próprio Reimaginado.

## Alteração

Nova peça de cabeça menor, levemente inclinada, com olhar de três quartos ao longo da marcha. O Ágil foi usado como referência visual explícita de proporção/ângulo; o Reimaginado original foi usado como referência de identidade, pele e equipamento. A cabeça não foi simplesmente virada simetricamente para a câmera. Corpo, braços, pernas, passada e tempos de oito quadros/100 ms foram preservados.

Pedido pelo MCP oficial `create_image_pro`, com duas referências rotuladas. Job `06c04c2d-2aa3-4a6b-8d50-114acc333518`; quatro propostas preservadas em `experiments/pixellab-orc-refinement-v5/07-NaturalHead/raw/`. Proposta 1 selecionada para composição. A proposta 2 copiou roupa/corpo do Ágil e não foi usada. Custo retornado: dez gerações para o lote; sem nova geração de movimento.

O Aseprite posicionou a peça na referência de corpo original e a registrou nos oito quadros. Não houve redimensionamento de personagem ou cópia do rosto do Ágil. Scripts `tools/aseprite/preview-natural-head-v5.lua` e `tools/aseprite/apply-natural-head-v5.lua`; plano e procedência em `experiments/pixellab-orc-refinement-v5/`. Máscara específica do crânio/pescoço, preservando os ombros. Isso não implementa um rig universal.

## Evidência e arquivos

- `reports/orc-pixellab-refinement-v5/review.html`: Ágil, versão anterior e correção, reprodução sincronizada e ampliação da cabeça.
- `reports/orc-pixellab-refinement-v5/walk-contact.png`: oito poses nativas inspecionadas.
- `characters/orc-pixellab-07/source/aseprite/walk-study.aseprite`: mestre atual.
- `reports/orc-pixellab-refinement-v5-check.json`: exportação exata de oito quadros/tempos, zero alterações fora da máscara registrada e arquivos protegidos preservados.
- `experiments/pixellab-orc-refinement-v5/before-manifest.json`: versão anterior preservada por hash.

A página foi renderizada para inspeção visual local; captura em `reports/orc-pixellab-refinement-v5/comparison.png`. A galeria geral foi atualizada, e a apresentação v4 foi fixada à sua versão anterior deste Walk para evitar misturar históricos. Fichas de outros personagens, conceito e Idle do Reimaginado, aprovação do Soldado e projeto Unity preservados. A nova cabeça continua candidata; não foi registrada aprovação artística automática.
