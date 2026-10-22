# Fluxo de producao e comandos

Autoria e revisao no Aseprite: [guia integrado](ASEPRITE.md). `editor-fork` cria copia de trabalho; `editor-export` entrega build/preview; `editor-apply` aplica slots baseline com gates/backup. `editor-template` organiza fontes novas e assets genericos. O bridge usa modo batch sem controlar a GUI e exige arquivos salvos. Revisoes artisticas e integracao Unity seguem os marcos abaixo.

Execute os comandos a partir da raiz desta fabrica. Alternativa no Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File .\forge.ps1 help`. O Bypass se aplica somente a esse processo; nao e necessario mudar a politica global. Os arquivos usam UTF-8.

## 1. Ficha

`node src/cli.mjs new --id orc-novo --race Orc --job Warrior`

Use `catalog --kind races` ou `catalog --kind jobs` para nomes/IDs. Edite `characters/orc-novo/character.json`: papel, cultura, faccao, rosto, silhueta/corpo, idade visual, paleta, mao, assimetrias, luz, equipamento, perfil e Reuse Assessment. Valores desconhecidos permanecem TBD. Orc robusto vem do catalogo; pele verde, presas ou ornamentos especificos precisam de decisao visual. Archer nao e exclusivo de uma raca.

`outfit --from orc-novo --id orc-novo-archer --job Archer` cria variante do MESMO individuo. Mantem identityId/raca/appearance, aponta a base com hash e cria roupa candidata separada. Novo individuo ou outra raca usa new. `refresh-base --id orc-novo-archer` atualiza o vinculo e copia appearance da base atual; revise novamente.

## 2. Conceito

Conceitos de personagem sao weapon-independent: desenhe corpo e roupa sem arma empunhada, carregada ou embainhada, mesmo quando o Job usa armas. A arma e um asset separado e so deve aparecer em uma acao que a invoque quando estiver equipada. A espada dos sprites do Human Warrior Pilot e excecao historica. A fabrica ainda nao gera pacotes compartilhados de armas nem integra overlays em runtime.

`prepare --id orc-novo --purpose concept` gera handoff/prompt.md, handoff.json e context.md. Anexe as imagens indicadas a ferramenta escolhida, ou peca ao agente para abri-las. O contexto tem o texto das fontes, nao apenas nomes de arquivos. Importar resultado:

```powershell
node src/cli.mjs import --id orc-novo --input C:/candidatos/orc-a.png --kind concept --name candidato-a --provider ferramenta-usada --model desconhecido
node src/cli.mjs preview --id orc-novo
```

`import` copia bytes; nao faz pixelizacao/reducao. Um novo nome preserva variantes. `--force` autoriza substituir o arquivo local indicado e invalida revisao por hash. assets.json e historico de importacoes/composicoes; modelos desconhecidos permanecem unknown.

Gate 1: o criador deve aprovar explicitamente o conceito. Depois da decisao real:

```powershell
node src/cli.mjs review --id orc-novo --gate concept --decision approved --reviewer Criador --evidence "Aprovacao explicita na revisao de 2026-xx-xx; candidatos revisados no preview."
```

Esse exemplo explica a sintaxe. Nao registre aprovacao ficticia. O programa armazena o que o operador informa; ele nao autentica pessoas. Um agente nao pode criar aprovacao por iniciativa propria. O hash inclui a ficha, o conjunto completo de conceitos e o snapshot; qualquer novo conceito exige nova revisao.

## 3. Sprite base e vistas

`prepare --id orc-novo --purpose base` organiza a primeira vista front_r em resolucao nativa. Edicao/acabamento em LibreSprite pode preservar camadas e pixels. Alpha deve ser real. A base validada vira fallback e as outras vistas sao desenhadas individualmente:

Os sprites do corpo permanecem sem armas, inclusive em Idle/Walk e nos quadros do personagem usados para ataque. A futura Presentation deve desenhar o asset da arma separado, somente se a unidade a tiver equipada e a acao atual a invocar, com encaixe, oclusao e sincronizacao validados. Isso exige extensao de runtime; o fluxo offline atual nao implementa equipar/desarmar por acao.

```powershell
node src/cli.mjs import --id orc-novo --input C:/sprites/base.png --kind sprite --slot orc_novo_mvp1_static_128.png
node src/cli.mjs import --id orc-novo --input C:/sprites/front_r.png --kind sprite --slot Directions/orc_novo_dir_front_r.png
node src/cli.mjs validate --id orc-novo --stage base
node src/cli.mjs prepare --id orc-novo --purpose directions
```

Gate 1 valido e obrigatorio para importar sprites. Prefixo troca '-' por '_'; clipes usam somente estado. Quatro vistas: back_l, back_r, front_r, front_l, nomes de TELA. Sem espelhamento. O perfil piloto e 128x128, RGBA8, chao y=126 a partir do topo e PPU100. Perfis especiais exigem decisao documentada. Nao usar o perfil humano como anatomia universal.

## 4. Animacoes

Depois de validar e revisar base/vistas, registrar `review --id orc-novo --gate base --decision approved --reviewer ... --evidence ...`. Esse marco parcial de revisao visual exige inventario directions sem FAIL e permanece valido ao adicionar animacoes. Entao `prepare --id orc-novo --purpose animation --state Idle`. Ordem: Idle front_r -> Walk front_r -> outras vistas Idle/Walk -> Attack/Hit/Defeat front_r -> outras vistas de combate. Revisar cada lote antes de expandir.

Inventario piloto por vista: Idle4, Walk6, Attack5, Hit3, Defeat5 (92 quadros animados). Naming: `Animations/Walk/walk_front_r_00.png`, sequencia 00.. sem lacunas. Loader sonda 00..15, mas Walk depende de 3 frames/tile. Um numero diferente de frames nao garante locomocao correta.

Os cinco estados sao uma baseline legada, nao o inventario completo de acoes por equipamento. Siga [EQUIPMENT_AND_ACTIONS.md](EQUIPMENT_AND_ACTIONS.md) para ataque basico desarmado, selecao pela arma realmente equipada, clipes de habilidade separados e bindings com sockets/oclusao/eventos. Preserve Attack legado; suplementos versionados em actions/ nao sao exportados pelo exportador v0.1. Revisar o primeiro lote front_r de cada nova acao antes das outras vistas. Matriz real:characters/orc-equipment-actions-v1.json; verificacao:`node tools/check-equipment-readiness.mjs`.

## 5. Compor roupas existentes

Consulte [LAYERS.md](LAYERS.md). `compose` usa camadas RGBA nativas e um manifesto; nenhum desenho novo e criado. Ele bloqueia canvas diferente e nao espelha/move/reescala pecas.

## 6. Validar e revisar

`validate --id orc-novo --stage full` grava reports/validation.json. FAIL bloqueia exportacao. WARNING pede inspecao; REQUIRES_HUMAN_REVIEW cobre identidade, clusters e loops. Inventario pronto nao equivale a aprovacao artistica.

Apos revisao artistica real do pacote completo, registre `review --id orc-novo --gate consistency --decision approved --reviewer ... --evidence ...`. Gate 2 exige Gate 1 valido e validacao full sem FAIL. Use changes_requested para registrar rejeicao/ajustes; a ultima decisao do gate prevalece.

## 7. Exportar

`export --id orc-novo` produz dist/<id>/<hash>/ com PNGs, manifesto, relatorio e importador Unity opcional. Exige Gates 1 e 2 validos e validacao full. Build existente e preservado. Nenhum arquivo do jogo e alterado; leia UNITY.md. Gate 3 e aprovado pelo criador somente apos PlayMode real e pode ser registrado com gate in-game. O programa exige os gates anteriores, mas nao roda o Unity.

## Codigos de saida

0 = comando concluido (nao significa aprovacao artistica); 1 = falhas no relatorio tecnico ou doctor; 2 = uso invalido, entrada rejeitada ou gate pendente. Commands com caminhos externos leem a entrada indicada pelo operador; saidas por personagem ficam confinadas ao pacote e exportacoes ficam em dist.

## Exportacao complementar de acoes Orc

Apos aprovacao explicita da candidata corporal e do suplemento: `node tools/export-orc-actions-v1.mjs`. O comando verifica Gate1/base/Gate2 atuais, fingerprint aprovado do suplemento, SHA/canvas/RGBA dos quadros e fontes e cria um build completo `dist/<id>/actions-<hash>/`. Inclui baseline97 PNGs e20 adicionais por roupa quando necessarios, factory-actions.json e fontes .aseprite selecionadas em Source/. Warrior/Brawler reusam os proprios20 Attack por caminho, sem PNGs duplicados. Baseline antiga e builds existentes sao preservados. O comando `export` legado continua limitado a baseline; nao basta usa-lo para o suplemento. Este staging nao altera ou implementa o runtime Unity. Evidencias em reports/orc-actions-export-v1.json.
