## Política vigente — Orc principal e armas somente no ataque, 2026-10-25

O Orc principal atual é **orc-v1 / Verde Warcraft**, em characters/orc-v1/. O antigo Orc V4 está descartado e nunca é fonte de restauração ou direção atual. A identidade atual é a referência; poses de ataque defeituosas podem ser substituídas.

Espada/machado ficam **ocultos no Idle, Walk, repouso, inspeção, Hit/Defeat e após a ação**. Aparecem somente no intervalo declarado do Attack. Os pedidos anteriores de Idle/Walk armados e o corte único compartilhado entre Sword/Axe estão **SUPERADOS**. São dois perfis: corte de espada e golpe de machado, reutilizáveis entre itens compatíveis da própria categoria. Sem sacar/embainhar, rig universal ou animação corporal por item.

Guia atual: docs/MAIN_ORC_ONE_HANDED_RESCUE.md; autoridade de identidade: reports/orc-production-current.json. Armas seguem a linguagem visual do jogo, sem obrigação de copiar a paleta/cultura Orc. Aseprite continua mestre; PixelLab autorizado auxilia poses; toda edição/exportação artística é no Aseprite. Esta tarefa não modifica Unity nem concede aprovação artística. **Nos registros anteriores abaixo, toda afirmação conflitante de V4 ativa, nenhuma seleção, arma em Idle/Walk ou movimento universal é histórica e superada.**

## Decisão vigente — Orc V1 e armas, 2026-10-25

Criador selecionou Verde Warcraft v3 como **Orc V1**, primeiro jogável para futura integração. Fonte em `characters/orc-v1/`; Infante cinza preservado na biblioteca em Orcs Atuais/05 - Infante de Ferro/. Novos assets de uma mão: Espada do Recruta e Machado de Milícia, seguindo `docs/WEAPON_ART_STANDARD.md`. Golpe composto e Walk completo equipado em uma vista, com mestres/camadas/encaixes; a autorização anterior de Walk armado está SUPERADA: attack-only-v1 agora exige Idle/Walk sem armas. Corpo base e Idle fixo permanecem independentes. Página `Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html`; documentação `docs/ORC_V1_WEAPONS.md`. São assets/prévias locais, não integração Unity ou aprovação automática dos novos golpes/armas. V4 continua descartada; não confundir seleção para integração futura com produção completa em quatro vistas.

## Padrão fixo obrigatório de Idle — 2026-10-25

Equipamentos: seguir `docs/WEAPON_ART_STANDARD.md` e a revisão candidata `docs/ORC_V1_WEAPONS_V2.md`. Linguagem visual do jogo compartilhada entre classes/raças; não impor design ou paleta do Orc a todas as armas. Reutilizar corpo, pegada e tempo da família compatível ao trocar o item. V1 armada foi rejeitada; overlap de pixels e exportação não comprovam qualidade da pegada. V2 inclui Idle armado no padrão fixo, Walk e golpe em uma vista; aprovação do criador pendente.

PADRÃO FIXO OBRIGATÓRIO para criação de personagens e variantes: Idle normal segue o meio-termo aprovado, ID `idle-balanced-v1`, cinco fases com 400/450/500/450/400 ms (2200 ms), intensidade equivalente a 2 px na cabeça de humanoide 128×128. Não criar um padrão por personagem, Job, roupa ou personalidade. Ajustes de encaixe anatômico/escala preservam o mesmo ritmo e sutileza; divergências exigem autorização explícita do criador. Canon: `docs/IDLE_ART_STANDARD.md` e `config/idle-art-standard-v1.json`; biblioteca `PADRAO-DE-IDLE.md`. Baselines e notas históricas permissivas abaixo não prevalecem. Artes existentes não são migradas automaticamente e não há integração Unity neste pedido.

# Fluxo de producao e comandos

**Histórico superado — 2026-10-24:** V4 ativa e V4 Reimaginado descartados pelo criador; não reutilizar como direção selecionada nem reativar pelos scripts históricos. Arquivos preservados como histórico. Nenhuma seleção de produção ativa. Novo candidato `orc-pixellab-11` (Orc Atlético): parecido com o Ágil, menos armadura, mais musculatura e verde um pouco mais claro. Revisão corrente: `reports/orc-current-review/review.html`. Vigia e Matriarca ficam separados em `ideas/unique-characters-or-npcs/` como ideias futuras de NPC e/ou jogáveis únicos. Esta decisão substitui afirmações históricas de V4 selecionada abaixo.

**Correção vigente V8 — 2026-10-24:** V7 também foi rejeitada. Não forçar poses frontais com referência visual em três quartos: gerar primeiro uma vista coerente do próprio indivíduo, preservando o conceito selecionado. Na candidata 07, a base frontal Pro Flash condiciona oito quadros inteiros Skeleton V3; o Ágil fornece somente pontos/fases de movimento, sem pixels no modelo que desenha o personagem. A passada frontal foi adaptada e é mais contida, não uma cópia do clipe do guia. Evitar troca de cabeça e alegações de validação artística com base em exportação técnica. Revisão conjunta canônica e comparação sincronizada: `reports/orc-pixellab-v4-comparison/review.html`; relatório V8.

**Revisão conjunta e Walk v7 (2026-10-24):** manter todos os 11 conceitos e 18 clipes existentes visíveis juntos em `reports/orc-pixellab-v4-comparison/review.html`; construtor canônico `node tools/build-orc-all-review.mjs`. O criador rejeitou pescoço e direção da marcha v6, então o Walk 07 foi refeito como quadros completos com poses Skeleton V3 a partir do conceito próprio, em vez de preservar a passada rejeitada e continuar colando cabeças. Não reintroduzir peças históricas de cabeça sobre esse ciclo. Restantes personagens e seus estados foram preservados; nenhum movimento ausente foi simulado.

**Correção localizada de identidade (2026-10-24):** uma referência de caminhada/naturalidade de outro personagem não autoriza usar sua cabeça, feições, anatomia ou paleta como peça. Nos reparos da cabeça do Reimaginado, condicionar a geração somente com fontes do próprio Reimaginado e conferir a paleta contra seu original. Referência cinética pode orientar a análise textual, sem virar condicionamento visual de identidade. Registrar a cabeça pela base do pescoço/tronco; não perpetuar um desvio da face anterior como se fosse um ponto correto de encaixe. V5 foi rejeitada pelo criador e não é referência aprovada.

**Atualização autorizada — MCP PixelLab:** [guia operacional](PIXELLAB_MCP.md). Pedidos de geração e acompanhamento podem acontecer pelo MCP oficial sem controlar a GUI; autoria de retoques, mestres e empacotamento continuam no Aseprite. O método regional de compressão do tronco usado nos Idles da rodada v2 foi rejeitado pelo criador e não deve ser reutilizado como padrão. Validação técnica não substitui inspeção do movimento nem aprovação artística.

**Fluxo vigente adicional (2026-10-23):** [PixelLab + Aseprite](PIXELLAB_ASEPRITE.md). Criador autorizou geração pela extensão oficial e pediu três Orcs independentes com Tolkien/Warcraft, sem consultar a V4 ou usar qualquer imagem/referência herdada, incluindo estudos básicos de animação para escolha. Esse experimento não usa o prepare padrão com âncora/receitas; autorização dos estudos não equivale a aprovação artística ou integração Unity. Exportações batch permanecem locais e usam perfil separado da GUI.

Os oito Orcs agora usam a [revisao Aseprite V4](ORC_ASEPRITE_V4.md), autorizada pelo criador e selecionada em `reports/orc-production-current.json`. Reutilizar as fontes ativas por fork. Avaliar compatibilidade de corpo, roupa, vista e acao antes de adaptar; os ajustes locais do Warrior nao sao coordenadas universais. Os pacotes novos preservam tempos por quadro e os originais permanecem historicos. Consulte o guia V4 para auditoria, exportacao e recuperacao.

## Ferramenta mestre — decisao de 2026-10-22

Toda autoria artistica acontece no **Aseprite**: conceito, desenho de sprites, poses, animacoes, paletas e acabamento. A fonte `.aseprite` e autoritativa; PNGs e folhas sao derivados da exportacao. Scripts Lua executados dentro do Aseprite sao autoria programatica permitida e precisam de procedencia; nao sao desenho manual nem uma IA generativa do editor. Novas geracoes image_gen e edicoes/reconstrucoes raster externas dependem de nova instrucao explicita do criador. Ferramentas externas podem montar previews e fazer validacoes sem mudar a arte. Instrucoes antigas abaixo sobre ferramentas externas descrevem o historico; esta decisao prevalece. Legados aprovados nao mudam de procedencia por serem abertos no editor.

Experimento comparativo inteiramente no editor: [Aseprite V3 versus V2](../reports/orc-aseprite-v3/review.html). As camadas regionais desse estudo ainda nao equivalem a um rig de equipamento reutilizavel completo.

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
