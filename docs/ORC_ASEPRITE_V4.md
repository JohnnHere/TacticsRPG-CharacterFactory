# Orcs — referência de produção Aseprite V4

Revisão aplicada em 2026-10-22 aos oito pacotes: Warrior, Squire, Archer, Apprentice Mage, Acolyte, Rogue, Scout e Brawler. São roupas do mesmo indivíduo. O criador autorizou: “vamos aplicar a V4 do Aseprite nas animações de todos os Orcs que criamos”. Evidência completa e escopo: [aprovação da propagação](../reports/orc-production-v4-approval.json).

## Resultado e onde consultar

- [Comparação animada antes × V4](../reports/orc-production-v4/review.html): oito roupas, seis ações e quatro vistas; pausa, quadro, velocidade, zoom e fundo.
- [Seleção vigente](../reports/orc-production-current.json): ponto de entrada para fontes, aprovação, relatório de aplicação e exportação. Ler este arquivo antes de reutilizar os Orcs.
- [Pacotes locais completos](../reports/orc-production-v4-export.json): destinos concretos, índice e ZIP. Contêm 896 PNGs ativos e 216 fontes mestre.
- [Auditoria da produção](../reports/aseprite-production-audit-v4.json) e [conferência visual/técnica](../reports/orc-production-v4-check.json).

O conjunto contém 192 referências de animação (8 roupas × 6 ações × 4 vistas), apoiadas em 184 fontes animadas distintas. Unarmed reutiliza Attack no Warrior e Brawler. As outras seis roupas têm seu soco independente. São 856 PNGs animados únicos e 40 PNGs estáticos. As 32 fontes estáticas são reutilizadas sem alteração; total de 216 fontes selecionadas.

## O que foi aplicado

Warrior Attack e Hit front_r usam exatamente os oito quadros da V4 aprovada, incluindo os retoques de olhos, sombras e reflexos. A V4 foi construída sobre a V2; seus pixels herdados mantêm a procedência original.

Nas demais animações foram adaptados somente os ajustes compatíveis sobre a própria roupa e vista:

1. Consolidar os nove tons quase pretos definidos no estudo V4. Cada roupa usa o tom existente mais próximo de `080604` em sua própria paleta. Preto puro, cores dos tecidos, pele e metal são preservados fora desse conjunto. Não se aplica a paleta do Warrior às outras roupas.
2. Attack e Unarmed terminam na sua própria pose inicial. Hit termina na pose inicial do Attack da mesma roupa/vista. O retorno do soco das seis roupas permanece na sua guarda específica. Não se substituem os gestos de arco/conjuração pelo soco do Warrior.
3. Attack e Unarmed usam `[80,110,50,90,120]` ms; Hit usa `[50,100,90]` ms. Totais permanecem 450 e 240 ms. Idle, Walk e Defeat mantêm seus tempos e poses, recebendo apenas a limpeza de tons quase pretos. Defeat conserva a pose final caída.

Os retoques por coordenadas de olhos e materiais pertencem aos dois clipes revisados do Warrior. Não foram transpostos cegamente a outros rostos/poses. Conceitos, quatro bases e fallbacks não foram substituídos. A V4 de conceito continua um estudo separado; esta autorização é para animações.

## Fontes e procedência

Em cada pacote, `source/aseprite/orc-production-v4/editor.json` seleciona os masters em `source/`. Os PNGs de conferência ficam em `clips/<ação>-<vista>/frames/`; `native-strip.png` é a folha derivada. As camadas originais permanecem ocultas, com uma camada adicional contendo os quadros da baseline anterior. As camadas de trabalho e limpeza são editáveis. Não equivalem a um rig de corpo/roupa separado.

Os PNGs baseline ativos ficam nos slots `sprites/Animations/`. Os suplementos novos usam `actions/basic-unarmed/v4/`; os antigos `v1` permanecem como histórico. `characters/orc-equipment-actions-v1.json` aponta para os frames/fontes atuais, com hashes e tempos. O `v1` no nome desse arquivo é a versão do contrato de ações, não a revisão artística.

Toda transformação artística desta entrega aconteceu por Lua dentro do Aseprite Steam, em processo batch oculto `--noinapp`. Node organiza/copía arquivos e verifica pixels; Pillow constrói pranchas de revisão e valida; navegador demonstra os PNGs. Nenhuma chamada a geração de imagem ou edição raster externa foi usada. A origem histórica image_gen/LibreSprite dos pixels anteriores continua registrada.

## Como o fluxo funciona

1. `tools/prepare-orc-production-v4.mjs` verifica os gates e hashes antigos, fotografa os arquivos, usa editor-fork para cada roupa e chama `tools/aseprite/propagate-orc-v4.lua`. Exporta builds imutáveis dos 216 masters. A preparação recusa sobrescrever uma V4 já preparada.
2. `tools/build-orc-production-review-v4.mjs` constrói a comparação e `tools/check-orc-production-v4.py` verifica todos os quadros e controles. Não alteram a arte.
3. `tools/apply-orc-production-v4.mjs` exige essas verificações, aplica a baseline pelo bridge com backup, grava suplementos separados, atualiza a matriz de ações e registra a autorização real do criador nos oito Gates de consistência. A aprovação identifica explicitamente uma propagação autorizada; testes não concedem aprovação artística. Gate em jogo permanece ausente.
4. `tools/export-orc-production-v4.mjs` monta os oito pacotes completos com fontes, PNGs, hashes, aprovação, procedência e tempos. Saídas são imutáveis e verificadas. O suplemento usa o caminho normalizado do contrato `Actions/basic-unarmed/v1/` dentro dos pacotes.

Comandos seguros para verificar ou reexportar a seleção atual:

```powershell
node src/cli.mjs doctor
node tools/audit-aseprite-production.mjs
node tools/export-orc-production-v4.mjs
& 'tmp/pixel-venv/Scripts/python.exe' tools/package-orc-production-v4.py
```

O auditor padrão detecta a seleção atual e escreve `reports/aseprite-production-audit-v4.json`. Manifestos, auditorias e builds V1 continuam históricos. Os exportadores históricos `export-orc-actions-v1.mjs` e verificadores/aprovadores V1 não devem ser usados para restabelecer a seleção antiga. Próximas edições partem do manifesto V4 de cada roupa via `editor-fork`, com novo nome; as receitas Lua desta entrega não devem sobrescrever retoques manuais posteriores.

## Validação e limites

Todos os 856 quadros animados distintos foram comparados com suas referências anteriores; os originais foram preservados. Nos clipes adaptados, alterações de silhueta ficam restritas aos retornos declarados. Paletas próprias, RGBA128, alfa binário e chão126 passaram. Os oito quadros diretos do Warrior são RGBA idênticos à V4 aprovada.

O navegador verificou 192 clipes e 1.792 renderizações RGBA exatas de antes/depois, sem erros JavaScript; arquivo local, HTTP, fundo, zoom, quadro e velocidade funcionam. São 896 referências animadas contando os 40 quadros reutilizados de Warrior/Brawler. Essa coincidência numérica com os 896 PNGs ativos não significa que as duas contagens tenham o mesmo escopo. A suíte local passou 14/14 testes, incluindo fechamento de pose intencional, rejeição de duplicatas indevidas e tempos vinculados à aprovação.

O exportador conserva os tempos em `factory-animations.json` e `factory-actions.json`. O runtime atual do Unity ainda usa o piloto e playback fixo; não foi estendido a consumir estes tempos ou carregar Orcs/equipamentos. Aplicação nesta entrega significa produção local da fábrica e staging. Não houve cópia de assets, alteração de GUID, Core, cena, rig ou playback no jogo. O repositório principal recebeu somente documentação autorizada.

Não foi medida uma porcentagem de economia de tokens. O lote reaproveita as fontes e automatiza operações locais; isso reduz repetição e novas gerações, enquanto decisões e revisão artística continuam necessárias.

## Histórico e recuperação

`reports/orc-production-v4-before/` conserva os PNGs/metadados anteriores e a matriz antiga. Os 216 masters originais e builds antigos permanecem intactos; o bridge também gravou backups baseline em `source/aseprite-history/`. O relatório de aplicação aponta para esses backups.

Uma restauração deve ser feita como nova revisão: escolher os arquivos do snapshot/build anterior, restabelecer conjuntamente sprites, matriz e referências de suplemento, validar os digests e registrar a decisão correspondente. Não misturar PNGs antigos com hashes/reviews V4 nem executar aprovadores antigos para forçar gates. Os novos suplementos V4 são separados e podem permanecer arquivados ao restaurar a seleção.

## Direcionamento para próximas implementações

Usar Aseprite como mestre, consultar a seleção atual, avaliar reuso direto/adaptado antes de criar e preservar identidade/roupa/ação. Fazer fork da fonte aprovada, editar pixels existentes quando compatíveis e revisar diferenças em escala nativa. A V4 é referência local de acabamento e continuidade dos Orcs; a âncora global continua a definir o estilo. Nova anatomia, equipamento, arma, cenário ou estado exige sua própria avaliação de compatibilidade e evidência.
