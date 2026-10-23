# Orc V4 — retoque da V2 aprovada dentro do Aseprite

2026-10-22. Registro histórico da candidata original. **Atualização: animações aprovadas e aplicadas aos oito Orcs por autorização do criador.** [Produção vigente, comparação e documentação](../docs/ORC_ASEPRITE_V4.md). O conceito deste estudo permanece separado da aprovação de animações. Os resultados e limites abaixo descrevem a entrega original antes da propagação.

[Abrir comparador V2 × V4](orc-aseprite-v4/review.html) · [Procedência e métricas](orc-aseprite-retouch-v4.json) · [Conferência final](orc-aseprite-final-check-v4.json).

## Objetivo e fontes de autoridade

O pedido foi executar o refinamento sobre a arte aprovada da V2, preservando o nível visual já alcançado, e comparar com uma V4 editada no Aseprite. A V3 não foi usada como base.

Foram relidos AGENTS, VISUAL_IDENTITY, WORKFLOW, ROADMAP, EQUIPMENT_AND_ACTIONS e o contrato correspondente, manifesto de referências, DOCUMENT_INDEX, DESIGN_DECISIONS, ART_DIRECTION e CHARACTER_PIPELINE. Foram inspecionados âncora, piloto pertinente, conceito V2, os oito quadros V2 em ampliação e detalhes de rosto/metal. ART_DIRECTION, CHARACTER_PIPELINE e DESIGN_DECISIONS do snapshot coincidem por SHA256 com os arquivos do projeto principal na conferência final.

Critérios aplicados: rosto adulto/bestial e identidade individual preservados; proporção tática e materiais da V2 mantidos; mãos vazias; ombro blindado assimétrico mantido; contraste/clusteres revisados sem converter o indivíduo em outro desenho. A âncora orienta acabamento, não fornece anatomia/paleta para copiar do humano. As inspirações já documentadas não autorizam descaracterizar um conceito aprovado.

## O que mudou

### Conceito

Mesma resolução1254×1254 e mesma arte aprovada. Rosto, anatomia, roupa e composição não foram redesenhados.

- Removidos39.102 pixels quase transparentes, com alfa entre1 e12/255, mantendo pixels com alfa acima desse limite.
- Seis pixels RGB de um rebite foram ajustados usando cores vizinhas já existentes. O alfa desses pixels foi conservado.
- Fora dessa limpeza e dos seis pixels, o conceito é idêntico à V2. **A mudança é principalmente técnica e quase imperceptível; não é um novo conceito artisticamente redesenhado.**

Uma tentativa intermediária de repintar facetas do metal produziu faixas artificiais na ampliação e foi rejeitada. Código e fonte daquela tentativa estão em `characters/orc-01-aseprite-v4/source/aseprite/iterations/retouch-01/`. Ela não integra o resultado final.

### Attack e Hit front_r

O desenho nativo aprovado foi reaproveitado. Nenhum sprite foi reconstruído a partir do conceito e nenhuma anatomia foi desenhada por formas programadas.

- Íris aquecidas com cores já existentes na paleta nativa V2; ajustes pontuais de sobrancelha/sombra.
- Pequenos retoques de clusters de pele e metal, limitados por coordenadas e material original. O código e as contagens permitem auditar o alcance, sem inferir melhoria pela quantidade de pixels alterados.
- Nove cores quase pretas foram consolidadas na tinta080604 já existente; preto puro e os demais materiais foram conservados. Boa parte das diferenças numéricas é visualmente muito discreta.
- O último quadro de Attack e o último de Hit reutilizam a pose neutra inicial do Attack aprovada na V2. Após os mesmos retoques, entrada e dois retornos são RGBA idênticos na V4.
- Mantidos5 quadros de Attack e3 de Hit, canvas128×128, chão126 e alfa binário. Sem escala ou espelhamento.
- Mesmas durações: Attack80/110/50/90/120ms, total450; Hit50/100/90ms, total240.

Nos seis quadros sem substituição de retorno, a máscara de alfa/silhueta permanece idêntica à V2. Nos dois retornos, a silhueta muda para a da pose neutra reaproveitada:195 pixels de alfa diferentes no fim de Attack e479 no fim de Hit. Isso é explícito e não deve ser descrito como simples retoque de cor.

O reuso remove variações de desenho da posição de repouso entre estes estudos; **o efeito na fluidez e a possibilidade de a recuperação parecer abrupta exigem sua avaliação**. Não foi demonstrada compatibilidade visual com o Idle do acervo legado nem integração do retorno no Unity.

## Como foi feito no Aseprite

1. O Gate conceito V2 e os hashes dos estudos aprovados foram conferidos.
2. `editor-fork` criou cópias de trabalho das duas fontes V2: `characters/orc-01/source/aseprite/orc-v4-retouch/`, com manifesto e lineage.
3. `retouch-v2-to-v4.lua`, executado pelo Aseprite em lote oculto, abriu essas fontes. O conceito original foi aberto no Aseprite sem redimensionamento.
4. Cada fonte V4 preserva o conteúdo V2 em uma camada de referência oculta. Nos clipes, há camada de poses de trabalho e camada de retoques locais. No conceito, o trabalho preserva alfa parcial; um mapa de alterações fica oculto para não compor alfa adicional sobre a pintura original.
5. O Aseprite gravou mestres `.aseprite`, PNGs, tiras de contato e mapas de diferenças. Node/Python apenas organizaram metadados, construíram previews e compararam pixels, sem editar a arte.
6. O exportador criou build imutável verificado. As fontes V2, originais de produção e repositório Unity permaneceram inalterados.

Trata-se de **edição programática por Lua dentro do Aseprite sobre pixels V2**, não desenho manual com mouse. A origem anterior image_gen da V2 continua registrada: importar e retocar não torna toda a imagem uma autoria nova feita do zero no editor. Não houve nova chamada de geração de imagem ou acabamento raster externo.

As camadas são referência, trabalho e retoque; não simulam separação anatômica de corpo/roupa ou um rig de equipamento.

## Arquivos entregues

Pacote: `characters/orc-01-aseprite-v4/`.

| Arquivo | Função |
|---|---|
| `concepts/v4-retouched-concept.png` | Conceito importado sem reescala para revisão |
| `source/aseprite/retouched/concept.aseprite` | Mestre do conceito na mesma resolução da V2 |
| `source/aseprite/retouched/attack.aseprite` | Mestre Attack5 com V2 preservada e retoque separado |
| `source/aseprite/retouched/hit.aseprite` | Mestre Hit3 com V2 preservada e retoque separado |
| `source/aseprite/retouch-v2-to-v4.lua` | Todas as instruções dos novos retoques |
| `source/aseprite/editor.json` | Contrato de exportação com hashes e comparação dos PNGs |
| `source/aseprite/provenance.json` | Procedência, fontes, mudanças por quadro, hashes e build |
| `reports/orc-aseprite-v4/review.html` na raiz | Comparador com mesmos pixels, escala e timings |

Build final: `dist/editor/orc-v2-to-v4-retouch/2256ba7a47d165f0dbea/`. O manifesto/procedência registra o caminho efetivo; builds anteriores da tentativa rejeitada permanecem apenas como histórico.

## Conferências executadas

- Aseprite Steam1.3.18.6 disponível; doctor sem erros de referências.
- Exportação:3 fontes,9 quadros,9 comparações RGBA idênticas com os renders produzidos pelo editor.
- Nove cels V2 de referência, incluindo conceito, reabertos dentro dos mestres V4 e conferidos pixel a pixel com os PNGs originais. As fontes foram fechadas sem salvar as mudanças temporárias de visibilidade da verificação.
- Paleta nativa:zero cores novas em relação à união dos quadros V2; zero alteração de silhueta não planejada.
- Os três quadros neutros V4 são RGBA idênticos.
- Conceito:mesma resolução; todas as alterações de alfa limitadas ao limiar declarado; apenas seis mudanças RGB fora dessa limpeza.
- Comparador Edge headless:16 comparações exatas de canvas V2/V4,8 alternâncias da camada de retoque conferidas, controles de retorno/quadro/velocidade/zoom/fundo/mapa de diferenças e zero erros JavaScript. Exibição file:// e leitura exata via HTTP de loopback. Evidência: `orc-aseprite-comparison-check-v4.json`.
- 1.151 arquivos protegidos da produção e os11 arquivos V2 especificamente vinculados à revisão permanecem inalterados. Aprovação V2 atual válida; aprovação V4 pendente. Evidência: `orc-aseprite-final-check-v4.json`.

O número de pixels diferentes inclui a consolidação de preto, mudanças quase invisíveis e os retornos reutilizados. Não mede valor artístico. Não foi executada uma nova suite global nesta etapa; as conferências acima são específicas da entrega V4.

## Como revisar

Abra o comparador. Verifique Attack e Hit em movimento e use **Comparar retorno** para parar nos dois quadros que receberam a pose neutra. Use meia velocidade e quadro manual para verificar a recuperação.

Desligue **Retoques locais da V4** para ver a pose de trabalho antes da correção de tinta/íris/clusteres. O retorno neutro reaproveitado continua presente nesse modo. O mapa rosa exibe todos os pixels RGBA diferentes em relação à V2, inclusive alterações quase imperceptíveis de preto; ele não é uma ilustração de melhorias.

O conceito deve continuar praticamente igual. Não esperar uma nova expressão, anatomia ou roupa: esses elementos foram mantidos porque já estavam aprovados.

Para editar no Aseprite, abra os mestres e conserve uma nova cópia antes de mudanças. O `.aseprite` salvo é o mestre da edição mais recente escolhida. **Não rode novamente o script de retoque sobre alterações manuais que queira preservar**: ele reproduz a revisão a partir da V2. O manifesto fixado por hash e `compare` rejeita mudanças; use um novo fork/manifesto de trabalho para exportar uma edição futura.

## Reprodução técnica do lote

Com fontes aprovadas e fork já presentes:

```powershell
node tools/retouch-orc-v4.mjs
node tools/build-orc-comparison-v4.mjs
tmp/pixel-venv/Scripts/python.exe tools/check-orc-comparison-v4.py
```

Os previews `working_*.png` são derivados auxiliares exportados por `tools/aseprite/export-v4-working.lua` dentro do Aseprite. A verificação das referências usa `tools/aseprite/verify-v4-reference.lua`. A exportação normal de fontes salvas continua sendo `editor-export --manifest ...`, sem reexecutar o autor de retoques.

## Próximo marco

Avaliar separadamente limpeza do conceito, retoques nativos e recuperação dos dois clipes. Não considerar a V4 aprovada por passar nas conferências. Nenhum candidato foi aplicado; nenhum Gate em jogo, nova roupa/vista ou suporte a armas/eventos/runtime foi declarado. O projeto principal permanece sem escrita.
