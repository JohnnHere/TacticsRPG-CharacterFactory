# Orc V3 — autoria integral no Aseprite e comparação com a V2

Data: 2026-10-22. **V2 aprovada pelo criador; V3 candidata, não aplicada.**

[Abrir comparação interativa](orc-aseprite-v3/review.html) · [Procedência e hashes](orc-aseprite-authorship-v3.json) · [Manifesto comparativo](orc-aseprite-comparison-v3.json).

## Pedido e interpretação

O criador esclareceu que a produção deve acontecer **toda no Aseprite** e pediu a mesma demonstração do lote anterior: conceito Warrior, Attack e Hit, agora comparados com a V2 já aprovada. Isso foi implementado como nova autoria dos pixels no runtime Lua do editor. Não houve chamada image_gen, importação de pixels da V2 para formar a V3, redução de conceito, reconstrução de grade ou acabamento raster externo.

O agente escreveu os desenhos, os contornos, os clusters de sombra/luz e as poses explicitamente em Lua. O Aseprite executou esse desenho e criou as fontes/cels e todos os PNGs. **É autoria programática do agente dentro do Aseprite, não desenho manual com mouse e não uma função de IA generativa do editor.** A arte observada como referência não foi amostrada ou rastreada pelo script. A API oficial documenta a criação de [imagens e pixels](https://www.aseprite.org/api/image) e [sprites, camadas, cels e quadros](https://www.aseprite.org/api/sprite).

## Entregas e localização

Pacote isolado: `characters/orc-01-aseprite-v3/`. Mesmo identityId do Orc aprovado; mesma intenção de roupa, mãos vazias e ombro esquerdo anatômico protegido. As diferenças de desenho são candidatas, não nova identidade aprovada.

| Entrega | Arquivo mestre | Derivado para revisão |
|---|---|---|
| Estudo de conceito nativo | `source/aseprite/authored/concept.aseprite` | `concepts/aseprite-native-v3.png` |
| Attack front_r, cinco quadros | `source/aseprite/authored/attack.aseprite` | `source/aseprite/authored/attack/attack_front_r_00..04.png` |
| Hit front_r, três quadros | `source/aseprite/authored/hit.aseprite` | `source/aseprite/authored/hit/hit_front_r_00..02.png` |
| Instruções de autoria | `source/aseprite/author-orc-v3.lua` | Código original e hash na procedência |
| Contrato do exportador | `source/aseprite/editor.json` | Build imutável e preview Aseprite |
| Componentes para inspeção | fontes acima, sem alteração | `source/aseprite/components/`, 81 PNGs renderizados pelo Aseprite |

Canvas 128×128 RGBA, transparência binária, chão126. Há nove camadas regionais em cada documento: tecido traseiro; perna/bota distante; perna/bota próxima; torso/couraça; braço esquerdo blindado; pano do pescoço; cabeça/rosto; cinto/tabardo; braço direito exposto. Tags identificam os três estudos. Essas camadas foram desenhadas desde a origem, não obtidas por segmentação automática de uma imagem pronta.

São camadas **regionais**, com anatomia/roupa ainda combinadas em alguns componentes. Não formam um rig universal de corpo e equipamento. Ocultar a couraça não revela um torso nu acabado; ocultar o braço não implementa arma equipada no jogo.

## Comparação controlada

- V2 e V3 usam os mesmos cinco quadros de Attack e três de Hit, ambos em 128×128.
- Mesmas durações: Attack 80/110/50/90/120 ms, total450; Hit 50/100/90 ms, total240. A repetição é apenas para revisão; suporte desses tempos no Unity não foi demonstrado.
- A pose neutra da V3 é intencionalmente idêntica na abertura/fechamento do Attack e na recuperação final do Hit. Quadros repetidos de retorno não são contados como desenhos novos distintos.
- O conceito V2 tem resolução alta, enquanto o estudo V3 foi concebido diretamente em 128×128. O comparador informa ambas as resoluções; o conceito não é um teste em resolução igual. Os clipes nativos são a comparação em resolução igual.
- O comparador permite pausa, quadro manual, velocidade, zoom1× a4×, troca de fundo e isolamento de cabeça/braço/camadas. Os componentes exibidos também são exports do Aseprite.

## Avaliação do resultado atual

A V3 demonstra controle explícito de pixels, paleta, cels, camadas, oclusão regional, poses e reexecução determinística. Ela é tecnicamente editável e inspecionável no Aseprite.

**A qualidade visual desta V3 ainda é inferior à V2 em anatomia, fidelidade do rosto, riqueza de materiais e volume.** A silhueta e o sombreamento são mais simples e a movimentação tem menos nuance. Duas primeiras tentativas foram preservadas em `source/aseprite/iterations/draft-01/` e `draft-02/`; o terceiro desenho ajustou proporção da cabeça, planos musculares, joelhos, brilhos do metal e a temperatura da pele. Isso não autoriza promover o resultado como refinamento artístico aprovado.

Não recomendo substituir a V2 apenas por a V3 ter sido produzida no Aseprite. A decisão de ferramenta mestre já está estabelecida pelo criador; a escolha do melhor desenho depende de aprovação artística. Este experimento mede a autoria atual do agente por Lua, **não o teto de qualidade do Aseprite**. Um artista trabalhando no mesmo editor pode produzir outro acabamento, e scripts adicionais não garantem automaticamente melhor anatomia.

## Procedência, reprodução e custos

`author-orc-aseprite-v3.lua` começa com imagens vazias e desenhos de coordenadas explícitas. Não carrega imagens de entrada. `tools/author-orc-aseprite-v3.mjs` só orquestra processos Aseprite ocultos, verifica hashes e chama o exportador. `tools/aseprite/export-orc-v3-components.lua` abre as fontes próprias e renderiza os componentes para o comparador; não altera as fontes salvas. HTML/Node/Python apenas organizam documentação, testes e previews.

Uma execução independente em `tmp/` produziu fontes `.aseprite` e PNGs com os mesmos bytes. O relatório mede o tempo local dessa reexecução, na ordem de centenas de milissegundos nesta máquina. **Isso não é o tempo total de criação:** desenhar, escrever e revisar o código exigiu tempo e tokens do agente. Não foi medida uma porcentagem de economia, nem feita uma comparação equivalente de custo entre autoria Lua e image_gen. Reexecutar o script e exportar não chama um modelo ou serviço externo.

## Validações

- Doctor: referências íntegras, Aseprite Steam1.3.18.6 disponível.
- Três fontes, nove quadros exportados e nove comparações RGBA exatas com o render da autoria.
- Reexecução independente: PNGs e fontes idênticos; versão do editor e código registrados.
- 1.151 arquivos protegidos do acervo original continuam inalterados.
- Suite local:13/13 testes PASS, incluindo o novo controle de que `prepare` orienta autoria no Aseprite e não geração image_gen.
- Comparador:81 componentes carregados;16 comparações exatas dos quadros V2/V3 em canvas;3 controles de composição por camada conferidos; zero erros JavaScript. Evidência em `orc-aseprite-comparison-check-v3.json`.
- A avaliação visual foi feita no preview nativo e no comparador. PlayMode Unity:NOT_RUN. Nenhuma aprovação V3 foi criada.

## Como abrir, editar e reproduzir

Abra os três arquivos `.aseprite` acima na interface quando desejar. O processo automatizado não disputa a janela aberta nem usa buffers não salvos. Uma edição artística no documento salvo deve ser exportada pelo manifesto; não execute novamente o autor Lua sobre uma edição manual que queira conservar.

Para **exportar uma edição salva**:

1. Faça uma cópia da fonte/manifesto para uma nova versão antes de editar.
2. Após a edição, atualize ou remova o `sourceSha256` e o `compare` daquele job na cópia de trabalho: eles fixam os pixels atuais e devem rejeitar mudanças não revisadas.
3. Execute `node src/cli.mjs editor-export --manifest CAMINHO/editor.json` e revise o build retornado. Não aplique candidatos sem o marco artístico correspondente.

Para **reproduzir o estudo por código**, preservando primeiro qualquer edição manual:

```powershell
node tools/author-orc-aseprite-v3.mjs
node tools/package-orc-aseprite-v3.mjs
node tools/build-orc-aseprite-comparison-v3.mjs
tmp/pixel-venv/Scripts/python.exe tools/check-orc-aseprite-comparison-v3.py
```

O comando de autoria regrava os derivados desse estudo a partir do Lua. Não deve ser confundido com um watcher de fontes editadas manualmente. A fonte mestre de uma edição manual passa a ser o `.aseprite` salvo; o script preservado documenta a origem, não tem precedência sobre a edição mais recente escolhida pelo artista.

## Decisões persistidas e próximos passos

A aprovação expressa da V2 foi registrada em `characters/orc-01-refinement-v2/reviews.json` para conceito, e em `reports/creator-approval-v2.json` daquele pacote para os arquivos mostrados. Os estudos aprovados não equivalem a um novo Gate base/consistency completo ou Gate em jogo e não foram aplicados ao acervo antigo.

A política **toda autoria no Aseprite** foi registrada em AGENTS, README, WORKFLOW e ASEPRITE, no help/doctor e nos novos handoffs de `prepare`. Os documentos históricos conservam a procedência anterior. O repositório principal permaneceu sem alteração enquanto a nova direção artística é comparada.

Próximo marco: avaliar se algum aspecto da V3 deve ser aproveitado, solicitar refinamento do desenho dentro do Aseprite ou rejeitar esta candidata. Até essa decisão, conservar a V2 como referência aprovada e a V3 isolada. Nenhuma outra roupa/vista, arma, cenário ou runtime foi declarado concluído por este estudo.
