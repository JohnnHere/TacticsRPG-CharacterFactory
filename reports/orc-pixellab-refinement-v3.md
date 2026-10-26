# Revisão corretiva dos Orcs — 2026-10-23

Estado: **CONCLUÍDO PARA REVISÃO DO CRIADOR**. PixelLab Pro confirmado pelo criador. [Abrir comparação animada antes/depois](orc-pixellab-refinement-v3/review.html). Aprovação artística pendente; Unity não alterado.

## Feedback autoritativo

Os Idles 04/05/06/07 do refino v2 foram rejeitados por imagem quebrada/deformação. A caminhada 07 foi rejeitada por andar torto; a 04 continuou inadequada. O PASS de arquivos/pixels não aprovava arte; a avaliação visual do agente foi insuficiente. O método regional de compressão/translação do torso está retirado deste fluxo. A solicitação do criador para reduzir exagero de respiração não justifica o defeito introduzido.

Infante: rosto e armadura apreciados, cabelo precisa mudar. Ágil: rebranding completo, atlético, sem volume inchado, menos cores, armadura imponente e flexível para agilidade. Não inferir aprovação integral de conceito/clipe.

Vigia e Matriarca reservados integralmente em `ideas/unique-characters-or-npcs/orc-pixellab-08` e `ideas/unique-characters-or-npcs/orc-pixellab-09`. Conforme correção do criador, são ideias de **personagens únicos jogáveis OU NPCs**; não personagens genéricos nem cânone racial. IDs originais retidos para preservar links/procedência.

Snapshot imutável da rodada anterior: `experiments/pixellab-orc-refinement-v3/before-manifest.json` (**369 arquivos**). O log inicial de 407 contava também as cópias de ideias após gravar o manifesto; a contagem autoritativa preservada é 369. Nenhuma escrita no Unity.

## Pedidos reais

- Novo Ágil: Create image, seletor **Pro**, sem estilo/referência, fundo removido; histórico `20261023182646.json`, arquivo `2026-10-23_18-26-46 - Create S-XL image (pro) - 005`. Quatro propostas preservadas, saída 1 escolhida como candidata, seed `1848142418.0`. Paleta carvão/couro/oliva, cintura definida e armadura articulada compacta.
- A chamada anterior de Idle do Soldado pela extensão Pro retornou quatro PNGs. Ficou preservada no histórico, sem ser importada como o novo clipe MCP. A chamada anterior de Walk 07 não tinha saída local recuperável. Nenhuma delas foi apresentada como entrega final.

## MCP instalado e usado

[Guia completo de configuração e retomada](../docs/PIXELLAB_MCP.md). MCP oficial configurado no arquivo de usuário do Codex, credencial fora do projeto, conexão autenticada e catálogo de ferramentas obtido. Sete animações enviadas pelo protocolo MCP e concluídas. Cada resultado confirmou cobrança de duas gerações: **14 gerações reportadas nessas sete chamadas**. Não inclui conceitos e chamadas anteriores da extensão; não representa custo total da sessão nem economia de tokens medida.

As sete chamadas usam **`animate_image`**, que não oferece seletor de modelo. Registrar o nome real em vez de atribuir o rótulo Pro ao modelo por causa da licença. Cada uma recebe seu conceito próprio como primeiro e último quadro, 128×128, oito quadros gerados e transparência. A saída contém nove PNGs: entrada intacta mais oito resultados. O Aseprite empacota apenas os oito resultados no clipe e preserva os nove no mestre bruto. Pedidos, job IDs, resultados e PNGs em `experiments/pixellab-orc-refinement-v3/mcp/` e em `source/pixellab-results/<estado>/refinement-v3/` dos pacotes.

## Alterações e inspeção

| Personagem | Alteração |
|---|---|
| Veterano Ágil | Rebranding Pro completo; novos Idle e Walk |
| Infante de Ferro | Coque removido, coroa careca redesenhada no Aseprite; novos Idle e Walk acompanham o cabelo |
| Soldado da Vala | Idle novo; Walk anterior preservado |
| Veterano V4 reimaginado | Idle novo e Walk com corpo mais alinhado e alternância de passos |

O retoque do Infante alterou **114 pixels apenas em x52..79/y0..11**; face e armadura fora dessa região ficaram exatamente preservadas no conceito. Script específico `tools/aseprite/refine-infante-scalp-v3.lua`, sem rig universal ou deformação regional do tronco. As animações são redesenhos do PixelLab e podem variar detalhes; a preservação exata descrita refere-se ao retoque do conceito.

As sete folhas de poses foram inspecionadas. Os novos movimentos têm corpos contínuos, sem a emenda regional antiga; as caminhadas 04/05/07 articulam e alternam pernas, mantendo predominantemente a vista frontal de três quartos. Não são uma vista frontal ortográfica nem aprovação para produção. Idles usam 200 ms/quadro (1600 ms); Walks novos 100 ms/quadro (800 ms), tempos autorados no mestre para revisão. Há pequenas variações generativas de rosto/materiais que continuam sujeitas ao julgamento do criador.

## Evidência e arquivos

- `reports/orc-pixellab-refinement-v3-check.json`: **12 mestres/68 quadros**, exportação exata e tempos; 369 arquivos anteriores preservados por hash; retoque limitado ao couro cabeludo confirmado.
- `reports/orc-pixellab-refinement-v3-review-check.json`: **160 comparações RGBA visíveis**, reprodução avançando, passo a passo, layout móvel, abertura por arquivo e zero erros JavaScript.
- `reports/orc-pixellab-refinement-v3/review.html`: comparação antes/depois, conceitos, Idle/Walk e ideias reservadas.
- `reports/orc-pixellab-v4-comparison/review.html`: oito opções genéricas/produção, incluindo V4; ideias únicas fora desse grupo.

Handoffs, fichas, ativos, prompts e contagens atualizados. A página histórica v2 foi fixada ao snapshot para não misturar seus quadros com arquivos atuais. Os testes técnicos não substituem revisão artística; nenhum gate aprovado automaticamente, nenhuma receita racial promovida e nenhuma alteração no repositório Unity.

Os 24 PNGs excedentes dos Walks anteriores de 16 quadros foram preservados fora das pastas ativas, em `source/iterations/pre-v3-stale-frame-files/Walk/`, além do snapshot. Mapa em `reports/orc-pixellab-v3-preserved-unused-frames.json`; os clipes atuais têm oito PNGs cada, sem arquivos antigos misturados.

O nome de arquivo “S-XL” não é evidência de uso gratuito: a UI selecionada estava em Pro. Registrar modelo real, comando e plano separadamente. Os custos anunciados não provam débito efetivo; não quantificar economia de tokens não medida.
