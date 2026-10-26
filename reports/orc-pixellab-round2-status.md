# Orc PixelLab + Aseprite — rodada de comparação 2

**Data:** 2026-10-23  
**Estado:** quatro conceitos e oito estudos de animação prontos; aprovação artística pendente  
**Integração Unity:** não executada

## Escopo

Foram preparados quatro conceitos Orc em Aseprite com a extensão oficial PixelLab, cada um com Idle e Walk de oito quadros. Os candidatos 04–06 foram gerados sem imagens de referência. O candidato 07 é a única exceção: a V4 foi carregada pelo controle **Set style** para orientar cor, materiais e contraste; a geração produziu uma imagem nova, sem copiar pixels.

O plano PixelLab Pro autenticado funcionou. Três chamadas de conceito Pro (05–07) concluíram sem problema de login. O candidato 04 foi gerado pelo modelo Pixen S-XL antes da assinatura; sua geração Pro anterior à assinatura tinha sido bloqueada, mas não impediu este lote.

## Candidatos

| ID | Direção | Geração do conceito | Animações |
|---|---|---|---|
| `orc-pixellab-04` | **Veterano Ágil** — calvo, atlético, lenço carmim e ferro escuro | Pixen S-XL, somente texto | Idle/Walk, 8 quadros cada |
| `orc-pixellab-05` | **Infante de Ferro** — infantaria pesada, armadura gunmetal, pele cinza e pano vinho | PixelLab Pro, somente texto | Idle/Walk, 8 quadros cada |
| `orc-pixellab-06` | **Soldado da Vala** — magro, curvado, couro gasto e peças de metal assimétricas | PixelLab Pro, somente texto | Idle/Walk, 8 quadros cada |
| `orc-pixellab-07` | **Veterano V4 Reimaginado** — paleta oliva/carmesim, ferro escuro e ombreira assimétrica | PixelLab Pro; V4 apenas como referência de estilo | Idle/Walk, 8 quadros cada |

Cada pacote mantém o PNG do conceito em `concepts/`, mestre `.aseprite` em `source/aseprite/`, arquivos brutos e histórico em `source/pixellab-results/`, e quadros derivados em `source/studies/`. Os oito clipes usam 100 ms por quadro na galeria de revisão; o arquivo de origem do PixelLab não especifica duração.

## Procedência e custos observáveis

- A extensão PixelLab oficial v0.4.130 foi usada dentro do Aseprite.
- Houve três gerações de conceito Pro e duas imagens Pixen S-XL para o candidato 04 (uma alternativa cortada e uma selecionada), além de oito pedidos de animação no **Animate with Text (v3)**.
- A interface anunciava 1 geração por imagem Pixen S-XL, 10–25 por pedido de imagem Pro e 1–8 por pedido de animação; o débito real da conta não é exposto pela extensão.
- A fila de animação processou os pedidos em série em segundo plano, levando aproximadamente 6–12 minutos por clipe nesta sessão.
- No pacote de animação 05, apenas os valores RGB ocultos sob pixels totalmente transparentes diferem entre a imagem inicial e o conceito; alfa e todos os pixels visíveis são idênticos. O importador preserva os PNGs brutos e registra essa diferença sem tratar pixels invisíveis como erro.
- O prompt real enviado ao PixelLab no candidato 07 está no histórico local. A extensão concatenou a descrição longa com uma segunda descrição curta; o pedido e o resultado foram mantidos sem gastar uma geração adicional.

## Leitura preliminar

A direção de silhueta é suficientemente variada para comparação: 05 é o mais pesado, 06 é o mais esguio, e 07 carrega mais claramente as cores e materiais da V4. Apesar do prompt atlético, a arte 04 ainda parece relativamente robusta. Cada clipe tem oito quadros visualmente distintos e começa com alfa e cores visíveis iguais ao conceito; os quadros finais não coincidem pixel a pixel com o início, então o fechamento dos loops ainda pede avaliação/refino. No Idle 05, o último quadro também varia mais a orientação do corpo; julgue o loop completo na galeria.

Estes são estudos de conceito e movimento. Nenhum foi aprovado como sprite de produção. Todas as fichas e clipes mantêm `PENDING_CREATOR`; não houve alteração do projeto Unity nem das documentações do repositório principal.

## Revisão visual

Abra `reports/orc-pixellab-v4-comparison/review.html` para comparar a V4, os três primeiros conceitos PixelLab e as quatro opções desta rodada. A página permite selecionar Conceito, Idle ou Walk por cartão, reproduzir todos os clipes, avançar quadro a quadro, mudar zoom, velocidade e fundo.

Os prompts reais de cada conceito estão em `handoff/prompt-pixellab-actual-request.md` e `source/generation-record.json`. Os arquivos `prompt-pixellab-submitted.md` preservam prompts planejados ou tentativas históricas quando isso difere do pedido bem-sucedido. O quarto pacote traz `handoff/handoff.json` com os hashes da V4 e da amostra de estilo usada.
