# Orcs — refinamento PixelLab + Aseprite v2

**Revisão posterior do criador:** Idles 04/05/06/07 rejeitados por deformação; Walk 04/07 inadequados. Os PASS abaixo documentam arquivos, não qualidade aceita. Esta apresentação histórica foi fixada às fontes preservadas; entrega corretiva atual em [rodada v3](orc-pixellab-refinement-v3/review.html). Vigia/Matriarca reservados para personagens únicos jogáveis OU NPCs.

Data: 2026-10-23. **Concluído para revisão do criador.** Aprovação artística: `PENDING_CREATOR`. Integração Unity: `NOT_RUN`.

## Pedido e entregas

O criador identificou pés quase imóveis nas caminhadas 04/07, Idles inadequados nos dois veteranos e exagerado no Soldado da Vala, além de pouca imponência/detalhe no Infante de Ferro. Pediu também mais dois conceitos com padrões visuais diferentes.

| Candidato | Conceito | Idle | Walk |
|---|---|---|---|
| 04 Veterano Ágil | Preservado | Respiração discreta no Aseprite | Novo PixMiniMax, 16 quadros |
| 05 Infante de Ferro | Nova proposta Pro, saída 1 de 4 | Respiração sobre o conceito novo | Novo PixMiniMax, 16 quadros |
| 06 Soldado da Vala | Preservado | Respiração discreta no Aseprite | Preservado |
| 07 Veterano V4 Reimaginado | Preservado | Respiração discreta no Aseprite | Novo PixMiniMax, 16 quadros, câmera/direção explícitas |
| 08 Vigia do Passo | Novo Pro, saída 0 de 4 | Conceito nesta etapa | Conceito nesta etapa |
| 09 Matriarca da Cinza | Novo Pro, saída 2 de 4 | Conceito nesta etapa | Conceito nesta etapa |

A página de entrega é [comparação antes/depois e novos conceitos](orc-pixellab-refinement-v2/review.html), com os dois conceitos novos e comparação dos quatro candidatos anteriores. A [galeria completa](orc-pixellab-v4-comparison/review.html) contém dez opções contando a V4. Ambas foram reconstruídas com os resultados finais.

## Conferência final

Os 14 mestres exportaram 94 quadros com pixels e tempos conferidos pelo bridge Aseprite; os 241 arquivos anteriores mantêm seus hashes. Os quatro Idles preservam exatamente rosto e região inferior. Evidência: `reports/orc-pixellab-refinement-v2-check.json`. As folhas de quadros das três novas caminhadas foram inspecionadas: há alternância e elevação dos pés; o Infante acompanha sua armadura nova. Isso não equivale à aprovação artística nem à validação em jogo.

A apresentação passou em 306 comparações de pixels visíveis, dez cartões da galeria, quatro pares antes/depois, layout móvel e abertura por arquivo local; zero erros JavaScript. Evidência: `reports/orc-pixellab-refinement-review-check.json`. Os novos conceitos 08/09 não receberam animações nesta etapa.

## Como a arte foi feita

**Caminhadas:** extensão oficial PixelLab 0.4.130 no Aseprite Steam 1.3.18.6. Usado **Animate with text (PixMiniMax)**, identificado pela extensão como MiniMax H3. Cada pedido recebe o próprio conceito do candidato, 128×128, 16 quadros, fundo transparente e mãos vazias. Os quadros brutos permanecem intactos; o Aseprite monta o mestre e os PNGs de revisão. O tempo de 80 ms/quadro, ciclo de 1280 ms, foi definido na fábrica para revisão e está salvo no mestre.

O novo prompt descreve alternância, apoio, levantamento, passagem e avanço das botas. No 07, a primeira tentativa tinha passos visíveis mas girava o corpo para uma vista lateral; ela foi excluída da galeria ativa e preservada em `characters/orc-pixellab-07/source/iterations/refinement-v2-walk-turning-attempt/`. A segunda usa direção **south-east** e câmera **low top-down (ca 20 degrees)**, além de pedir a manutenção da orientação do tronco e da cabeça. O 05 reutiliza esses controles. **Definir esses controles depois de Set reference image:** a extensão os redefine como Auto quando a entrada muda.

**Idles:** refinamento local e programático dentro do Aseprite, reaproveitando exclusivamente o conceito PixelLab do próprio indivíduo. O Lua `tools/aseprite/refine-pixellab-idle.lua` mantém o rosto e a região inferior fixos e comprime/eleva um trecho do tronco em um pixel na inspiração. O mestre tem a arte e uma camada de referência original oculta. São **duas poses sustentadas em oito quadros**, com tempos `[320,160,160,320,320,160,160,320]` ms, total de 1920 ms. As repetições são pausas deliberadas; não são oito poses novas geradas. A comparação de pixels das regiões fixas retorna zero diferenças. Os limites de edição são próprios destes quatro corpos; não constituem um rig universal para outras anatomias.

**Conceitos:** três chamadas Pro separadas, cada uma com quatro propostas preservadas. Infante: silhueta mais alta, gorjal, ombreiras articuladas, chanfrados, rebites e malha. Vigia: indivíduo mais velho, esguio, grisalho, pele azul-acinzentada e couro ocre. Matriarca: Orc veterana de massa corporal robusta, tranças, tecidos índigo, couro, osso/bronze e pele musgo. As culturas/facções e as propostas de anatomia continuam candidatas. Os novos conceitos nasceram de texto, sem estilo, referência visual ou paleta legada. O conceito 07 mantém a procedência histórica de referência V4; nenhuma imagem V4 foi usada nos novos pedidos 05/08/09.

## Arquivos e retomada

Cada pacote guarda o conceito em `concepts/concept-selected.png`, os mestres em `source/aseprite/`, os clipes em `source/studies/Idle|Walk/clip.json`, as saídas brutas em `source/pixellab-results/` e o pedido real em `handoff/prompt-pixellab-actual-request.md` ou no registro do clipe. `source/generation-record.json` relaciona modelo, seed, histórico, saídas e revisão.

Os **241 arquivos anteriores** estão preservados por hash em `experiments/pixellab-orc-refinement-v2/before-manifest.json`. O arquivo `brief.json` dessa pasta registra os pedidos, tentativas e resultados. Os dois conceitos adicionais têm contexto em `experiments/pixellab-orc-extra-directions-v1/` e IDs próprios criados pelo CLI.

Fluxo operacional: abrir o conceito correto → Set reference image → conferir miniatura → definir câmera/direção/16 quadros → enviar o prompt → aguardar o arquivo completo com entrada mais 16 resultados → inspecionar a folha de poses → importar pelo script local → verificar o mestre e a galeria. Não aceitar uma caminhada apenas porque possui quadros diferentes: observar alternância de pernas, pés no ar/apoio, orientação, recorte e fechamento.

Os comandos de empacotamento e revisão ficam em `tools/import-pixellab-animation.mjs`, `tools/refine-pixellab-idles.mjs`, `tools/build-pixellab-refinement-review.mjs`, `tools/verify-pixellab-refinement.mjs` e `tools/check-pixellab-refinement-review.py`. Usar novos forks/iterações após uma aprovação ou edição manual; os scripts desta rodada não são autorização para sobrescrever arte revisada.

## Plano Pro, custo e limites

A extensão anterior continha o nível de plano do pacote baixado antes da assinatura. A atualização oficial pelo menu PixelLab e uma instância nova liberaram as ferramentas Pro; a versão continuou 0.4.130. As permissões foram operadas pelo criador. Não foi necessário ler, copiar ou registrar senha/chave da conta.

A interface anunciou **2 gerações** por caminhada PixMiniMax 128×128/16 quadros e **10–25 gerações** por chamada Pro de conceito. Houve quatro pedidos PixMiniMax, incluindo a tentativa 07 rejeitada por rotação, e três pedidos Pro de conceito. Os quatro Idles não exigiram chamadas novas à nuvem. O débito efetivo, custo monetário e economia de tokens não foram expostos/medidos; não tratá-los como economia financeira comprovada.

Estes são conceitos e estudos de uma vista, com variação de detalhes gerados e alguma oscilação do tronco ainda sujeitas ao julgamento do criador. Validação técnica confirma arquivos, pixels e tempos; aprovação artística permanece humana. Produção completa, outras vistas, ações/equipamentos e integração em jogo exigem seus marcos próprios. As documentações de direção artística do repositório principal só serão atualizadas após a avaliação do criador.
