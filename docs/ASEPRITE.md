# Aseprite na Character Factory

Producao Orc vigente: [Aseprite V4 aplicada](ORC_ASEPRITE_V4.md), com [ponteiro de selecao](../reports/orc-production-current.json). O auditor abaixo detecta a revisao ativa; a manifestacao V1 e seus builds sao historicos. Para novas edicoes, usar o editor.json V4 da propria roupa como entrada de editor-fork.

## Politica de autoria vigente — 2026-10-22

Para aprimorar arte ja aprovada, usar fork e retoques sobre os pixels aprovados. A candidata [V4 sobre V2](../reports/orc-aseprite-v4/review.html) preserva o desenho, com referencias V2 ocultas nos masters e [documentacao auditavel](../reports/orc-aseprite-retouch-v4.md). O redesenho simplificado V3 nao e um modelo de qualidade a reutilizar.

Por decisao do criador, toda producao artistica acontece no Aseprite e a fonte `.aseprite` salva e mestre. PNGs sao derivados. Autoria por Lua no runtime do editor e permitida e deve ser identificada como programatica. Nao usar geracao de imagens ou processamento raster externo para produzir arte nova sem nova instrucao explicita. Legados mantem procedencia; importar uma imagem gerada nao a transforma em autoria original Aseprite. Metadados, testes e previews externos sao permitidos sem alteracao da arte. Caso real: [V3 versus V2](../reports/orc-aseprite-v3/review.html), [procedencia](../reports/orc-aseprite-authorship-v3.json).

Para a explicação completa da entrega, arquitetura, ciclo dos arquivos, evidências e recuperação de falhas, consulte [Integração Aseprite — documentação de ponta a ponta](ASEPRITE_INTEGRATION_V1.md). Este arquivo é o guia operacional resumido.

Integracao local implementada em 2026-10-22 para Aseprite 1.3.x, inclusive Steam. Usa Node/pngjs existentes, sem dependencia nova ou API. Executa processos separados com `--batch --noinapp`, janela oculta e timeout. Nao controla mouse/teclado nem acessa buffers nao salvos. Salve no editor antes de exportar.

## Configuracao

Esta maquina ja esta configurada para `F:\SteamLibrary\steamapps\common\Aseprite\Aseprite.exe`.

```powershell
node src/cli.mjs editor-check
node src/cli.mjs doctor
node src/cli.mjs editor-config --input 'F:\SteamLibrary\steamapps\common\Aseprite'
```

Editor-config valida o caminho e grava config/aseprite.local.json, ignorado pelo Git. Em execucao: ASEPRITE_PATH > arquivo local > descoberta por instalacoes padrao, registro/bibliotecas Steam e PATH. A letra do disco nao fica no codigo compartilhado. Doctor informa a disponibilidade sem bloquear comandos antigos; editor-check retorna 1 quando o editor esta ausente. Erros de uso/gates/exportacao retornam 2.

## Revisar um asset existente

```powershell
node tools/audit-aseprite-production.mjs
node src/cli.mjs editor-fork --manifest reports/aseprite-production-manifest-v1.json --id orc-01 --job orc-01-00 --name orc-idle-fr-v2
```

O exemplo cria `characters/orc-01/source/aseprite/orc-idle-fr-v2/source/orc-01-00.aseprite`, com editor.json e lineage.json na pasta acima. Abra essa copia no Aseprite, edite e salve. A fonte original e preservada. O fork remove compare/sourceSha256 do manifesto de trabalho e conserva o contrato de canvas/timing/destinos. As fontes atuais sao cels raster completos; corpo/roupa nao sao separados automaticamente.

```powershell
node src/cli.mjs editor-export --manifest characters/orc-01/source/aseprite/orc-idle-fr-v2/editor.json
```

O comando informa um build e preview.html. Inspecione o candidato e use o caminho real retornado:

```powershell
node src/cli.mjs editor-apply --id orc-01 --build dist/editor/orc-idle-fr-v2/<hash> --force
node src/cli.mjs preview --id orc-01
node src/cli.mjs validate --id orc-01 --stage full
```

`<hash>` e marcador de documentacao. Apply exige Gate concept atual e, para animacoes, Gate base. Confere identidade/base de roupas, integridade do build e todos os destinos antes de escrever. Substituicoes exigem --force. Pixels identicos preservam os bytes do PNG antigo mesmo com compressao diferente. Guarda backup em source/aseprite-history/ e proveniencia em assets.json; falha de escrita provoca rollback. Mudancas reais invalidam as revisoes dependentes dos PNGs; nenhuma aprovacao artistica e criada. O criador revisa e a evidencia e registrada pelo review existente.

Apply cobre os slots baseline da ficha. Suplementos podem ser editados/exportados/previsualizados, mas sua selecao na matriz, fingerprints e exportador complementar seguem EQUIPMENT_AND_ACTIONS.md. Nao sao convertidos automaticamente em Attack legado. Armas continuam assets separados.

## Novas fontes, inimigos e outros assets

```powershell
# Fonte vazia com camadas; nenhuma arte e gerada.
node src/cli.mjs editor-template --manifest config/aseprite-template.example.json
# Apos desenhar/salvar:
node src/cli.mjs editor-export --manifest assets/environment/forest-props/editor.json
```

Tipos: character, enemy, environment, prop, effect, ui, weapon. Fontes genericas ficam em assets/<kind>/<id>/source/. Fontes ligadas a ficha ficam em characters/<id>/source/aseprite/<template-id>/source/. Novo individuo continua usando new e roupa do mesmo individuo usa outfit. O exemplo config/aseprite-character-template.example.json possui quatro frames/camadas e targets: ajuste characterId e perfil antes de executar. Template e autoria vazia, sem aprovacao implicita.

Editor-fork --manifest ... --name novo-id cria outra copia de qualquer pacote; --job ID seleciona um clipe e --id PERSONAGEM filtra esse personagem num manifesto misto. Nao sobrescreve uma copia de trabalho existente.

## Manifesto de exportacao

```json
{
  "schemaVersion": 1,
  "id": "orc-idle-revision",
  "kind": "character",
  "characterId": "orc-01",
  "jobs": [{
    "id": "idle-front-r",
    "source": "characters/orc-01/source/animations-v1/Idle/front_r/idle_front_r.aseprite",
    "profile": {"width":128,"height":128,"frames":4,"durationMs":240,"groundY":126,"alpha":"binary","requireTransparency":true},
    "targets": ["Animations/Idle/idle_front_r_00.png","Animations/Idle/idle_front_r_01.png","Animations/Idle/idle_front_r_02.png","Animations/Idle/idle_front_r_03.png"]
  }]
}
```

`source` e `compare` usam caminhos relativos a fabrica, confinados a ela. `targets` sao relativos a sprites/ e usados somente pelo apply. `sourceSha256` opcional fixa uma fonte selecionada. `compare` opcional lista PNGs na ordem dos frames e bloqueia qualquer diferenca RGBA. IDs sao unicos por manifesto. `layers`, `excludeLayers` e `tag` selecionam/excluem camadas ou selecionam um intervalo nomeado; nomes inexistentes sao rejeitados.

O perfil exige `width` e `height`. `frames` e `durationMs` ou `durationsMs` verificam contagem e duracao constante ou por quadro. Sem tag/tileset, contagem e timing tambem sao conferidos contra o header ASE. `groundY:null` desabilita chao; `alpha:"binary"` exige 0/255 e `"any"` permite alfa parcial. `requireContent` e true por padrao para sprites; `requireTransparency` e opcional, permitindo fundos/tiles opacos. Limites:4096 por eixo e16M pixels por PNG/atlas; divida timelines grandes em tags/jobs.

Nao aplica scale/trim/espelhamento/rotacao/merge-duplicates/ignore-empty. Conserva frames repetidos/vazios; sprites vazios exigem requireContent false. Saida individual e RGBA8, inclusive para fontes indexadas. JSON nativo carrega timing/tags/camadas/slices; source.aseprite conserva a fonte completa. Alterar duracoes nao reprograma o playback fixo do Unity.

## Cenarios e tilesets

Uma fonte com tilemap pode ter um job normal para render e outro com `"tileset":true` para exportar tiles. Profile.width/height descreve o canvas do documento; PNGs do tileset tem o tamanho nativo dos tiles, incluindo o indice vazio. Para tileset, requireContent e false por padrao. Sheet.json preserva nomes/retangulos de cada item exportado.

Document.json inclui cada cel de tilemap com frame, caminho de layer, tilesetId, baseIndex, posicao em pixels, tamanho da grade, dimensoes de tile e celulas `{x,y,tile,flags}`. Cada tileset possui identidade propria mesmo quando os nomes se repetem. Build.json vincula explicitamente cada tilesetId/indice a um PNG RGBA8 em jobs/<job>/tilesets/<tilesetId>/, com hash; o atlas padrao continua disponivel. Tiles indexados usam a paleta do primeiro frame (paletteFrame=0); outras paletas continuam na fonte .aseprite preservada. Flags de flip ficam como dados; isso nao espelha personagens. Exemplo de job dentro do manifesto:

```json
{"id":"tiles","source":"assets/environment/forest-props/source/forest-props.aseprite","tileset":true,"profile":{"width":128,"height":128,"requireContent":false}}
```

Exige uma layer tilemap realmente desenhada/convertida no editor. Layout 2D nao implementa alturas/colisao/materiais/oclusao do cenario 3D. Inimigos de anatomia propria, props, efeitos/UI e armas podem usar perfis de autoria proprios; exportacao Unity baseline mantem os bloqueios dos perfis que exigem runtime novo.

## Builds e verificacao

Dist/editor/<id>/<hash>/ contem build.json, manifest.json, hashes.json, preview.html e, por job, fonte copiada, atlas, metadados e PNGs individuais. Hash depende de manifesto/fontes/versao/implementacao. Builds existentes sao verificados integralmente e reutilizados; alterados sao rejeitados. Falhas preservam evidencia em tmp/aseprite/.../failure.json. Preview abre por file:// com clipe/playback/pausa/quadro/zoom. Loops sao para revisao, nao demonstram semantica one-shot em jogo.

```powershell
npm.cmd test
node tools/audit-aseprite-production.mjs
node tools/verify-aseprite-capabilities.mjs
node tools/verify-aseprite-character-flow.mjs
& 'tmp/pixel-venv/Scripts/python.exe' tools/check-aseprite-preview.py
```

Auditoria real: reports/aseprite-production-audit-v1.json; 216 fontes selecionadas pelos source-manifest.json imutaveis dos builds aprovados, 888 quadros RGBA/timing identicos +8 fallbacks, cobrindo896 PNGs. Confere fontes, PNGs e reviews intactos; nao seleciona fontes rejeitadas por glob. Indice: reports/aseprite-production-manifest-v1.json. Capabilities usa dados sinteticos para validar tileset/layout/flags/coordenadas sem produzir arte final. Testes reais em outra maquina sem Aseprite informam SKIP; os comandos legados continuam utilizaveis.

Exportacoes locais nao usam tokens de modelo. ElapsedMs do relatorio mede o lote; builds identicos sao reutilizados. Autoria/anatomia/clusters/consistencia exigem criacao/revisao. Camadas ajudam quando as pecas tiverem sido desenhadas e registradas. Nao foi presumida uma porcentagem de economia.

Uma copia real ja esta pronta em `characters/orc-01/source/aseprite/idle-front-r-editor-v1/source/orc-01-00.aseprite`, com manifesto na pasta acima. O ciclo publico fork/export/apply desse clipe passou com resultado UNCHANGED, sem alterar PNGs, assets.json ou reviews. Evidencia:reports/aseprite-character-flow-v1.json. A verificacao de preview usa o Python/Playwright ja existente nesta maquina e Edge headless; nao e dependencia runtime do bridge. Evidencia:reports/aseprite-preview-validation-v1.json.

Fontes oficiais: [CLI/Steam](https://www.aseprite.org/docs/cli/), [API Lua](https://www.aseprite.org/api/), [Tilemaps](https://www.aseprite.org/docs/tilemap/), [Grid](https://www.aseprite.org/api/grid). O executavel nao e distribuido com a fabrica. Exportacoes nao escrevem no Unity nem alteram aprovacao artistica.
