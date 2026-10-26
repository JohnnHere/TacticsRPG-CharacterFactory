# Orcs — ajustes pontuais e novo Infante

Revisão do criador em 2026-10-23. Estado: **CONCLUÍDO PARA REVISÃO**. [Comparação animada](orc-pixellab-refinement-v4/review.html).

## Feedback e escopo

- Ágil: correção anterior muito boa; eliminar sombra preta que tremia na cabeça ao andar.
- Infante: conceito melhor, mas pés da caminhada anterior preferidos. Recuperar essa passada, mantendo conceito sem coque.
- Soldado da Vala: **aprovado pelo criador**. Conceito registrado pelo comando review; estudos da vista exibida registrados por hashes em `characters/orc-pixellab-06/source/creator-approval-v4.json`. Não abrange vistas ausentes, equipamento ou jogo real.
- Reimaginado: caminhada muito boa, mas cabeça olhava para o lado. Ajustar só a orientação da cabeça.
- Novo indivíduo 10: Infante de Ferro — Cabeleira Negra, inspirado nos Uruk-hai cinematográficos, preservando linguagem de rosto/armadura do 05, com cabelo longo, proporções mais altas/esguias e musculatura atlética. Não substitui 05.

## Métodos e procedência

A gravação fornecida pelo criador foi inspecionada; tem 40,83 s a 30 fps. Imagens de inspeção em `reports/orc-pixellab-refinement-v4/video/`; o vídeo original continua em Downloads. As imagens extraídas servem apenas como evidência, não como pixels de produção.

Ágil: o rosto/testa mudava de sombreamento entre quadros. Reutilizada uma única peça de cabeça do próprio Walk, registrada por quadro e aplicada dentro do Aseprite. Não houve regeneração da passada, escala ou compressão do corpo.

Infante: restaurados os 16 quadros/80 ms da caminhada preferida, preservada no snapshot anterior. Retoque da coroa careca aplicado no Aseprite com registro por quadro; todo o restante da passada permanece exato, inclusive pés e pernas.

Reimaginado: a referência original e o pedido antigo de preservar a orientação mantinham o olhar lateral. Uma primeira correção MCP não girou o rosto o suficiente e foi preservada sem seleção. A segunda, por `inpaint_image`, produz rosto frontal. Essa peça foi registrada nos oito quadros da caminhada, dentro do Aseprite; o restante do corpo e os passos são os mesmos.

Essas edições são específicas de três fontes e não constituem rig universal. São composição/limpeza de peças no editor, sem repetir a deformação regional rejeitada dos Idles.

Novo Infante: `create_image_pro`, com o conceito 05 autorizado como referência de rosto e armadura. Quatro propostas preservadas; saída 2 selecionada como candidata. Cada animação usa exclusivamente seu próprio conceito como início/fim; Idle de oito quadros, Walk de 16. Fontes em `characters/orc-pixellab-10/`; jobs, pedidos e resultados em `experiments/pixellab-orc-refinement-v4/`. Modelo Pro no conceito; `animate_image` não oferece seletor de modelo, independentemente da licença Pro da conta.

## Revisão

Preservados 409 arquivos anteriores por hash. Conferência dos 15 mestres Aseprite e seus 101 quadros: PASS. Zero pixels alterados fora dos retângulos registrados da cabeça nos três Walks retocados; zero alterações nos pés/pernas da passada anterior do Infante; zero diferenças na peça de cabeça registrada do Ágil. Evidência: `reports/orc-pixellab-refinement-v4-check.json`. Esses limites demonstram o escopo da edição, não aprovação artística.

A página passou em 186 comparações de pixels visíveis, reprodução, passo a passo, abertura por arquivo e layout móvel; zero erros JavaScript. Evidência: `reports/orc-pixellab-refinement-v4-review-check.json`. Folhas nativas e capturas da apresentação permanecem em `reports/orc-pixellab-refinement-v4/`.

Custos retornados pelo MCP nesta rodada: conceito Pro com quatro opções, 10 gerações; duas tentativas de reparo da cabeça, 10 cada; Idle novo, 2; Walk novo, 4. Total reportado: **36 gerações**. Os retoques e reaproveitamento locais do Ágil e Infante não fizeram chamadas novas à nuvem. Nenhuma economia de tokens foi medida.

As fichas, contagens, fontes, hashes e handoffs foram atualizados. A galeria geral inclui o novo indivíduo como opção adicional; a apresentação v3 foi fixada ao snapshot anterior, evitando mistura de seus dados com os quadros atuais.

Soldado aprovado permanece preservado. As demais correções e o novo indivíduo continuam pendentes de revisão artística do criador. Não houve atualização de receita racial, integração Unity nem alteração de direção artística no repositório principal.
