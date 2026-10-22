# TacticsRPG Character Factory

Fabrica de pacotes de criacao, revisao e exportacao de **personagens 2D em pixel art**. Criada para manter a identidade visual entre racas, individuos e roupas de Jobs ao longo do tempo. Todo o trabalho local usa arquivos editaveis e versionados. Os comandos funcionam sem assinatura, login ou chamadas a APIs.

A criacao artistica pode acontecer pela ferramenta de imagem disponivel na conversa com o agente, usando o pacote gerado pela fabrica, ou por trabalho 2D em um editor como LibreSprite. Os comandos preparam contexto, organizam os resultados e compoem pecas existentes; imagens novas e animacoes precisam de autoria e revisao visual. Nesta versao nao ha gerador autonomo de quadros nem autenticacao automatica em ChatGPT/Google.

Entrega atual: **oito pacotes Orc aprovados e exportados localmente**, com896 PNGs e216 fontes editaveis. Incluem Idle, Walk, gestos de ataque/conjuracao por classe, Hit e Defeat nas quatro vistas, alem do ataque basico desarmado. [Baixar ZIP](<dist/orc-basic-production-v1/3b2d54ccb738bc2d/orcs-production-v1.zip>) · [Indice dos pacotes](dist/orc-basic-production-v1/3b2d54ccb738bc2d/index.html) · [Previa](characters/review-orc-actions-complete-v1.html) · [Documentacao da entrega](docs/ORC_PRODUCTION_EXPORT_V1.md).

[Padrao de equipamentos e acoes](docs/EQUIPMENT_AND_ACTIONS.md), auditado contra o jogo principal. Ataque sem arma e reacao Hit estao incluidos; armas, projeteis, efeitos e encaixes seguem pendentes. Exportacao completa:`node tools/export-orc-actions-v1.mjs`; o exportador legado so inclui a baseline. Arquivos estagiados e ZIP verificados por SHA256, suite11/11 PASS. Nenhuma integracao Unity foi executada; runtime exige extensao e bindings continuam ausentes.

## Comece aqui

Na pasta deste repositorio, com Node.js 20 ou superior:

```powershell
npm.cmd ci --ignore-scripts
node src/cli.mjs doctor
node src/cli.mjs demo
node src/cli.mjs preview --id hero-reference
Start-Process .\characters\hero-reference\preview.html
```

A instalacao inicial ja foi feita nesta maquina. `npm ci` e para reconstruir node_modules futuramente. A unica dependencia runtime e pngjs, fixada no lockfile. Node foi escolhido porque ja estava disponivel e o executavel Python encontrado era apenas o alias da Microsoft Store. LibreSprite e opcional e nao foi instalado automaticamente. Os comandos sao locais apos a instalacao da dependencia.

Abra tambem [o painel de referencias](references/index.html), com a ancora aprovada, Hero e links para os documentos originais copiados.

## Criar com poucos comandos

```powershell
node src/cli.mjs new --id meu-orc --race Orc --job Warrior
node src/cli.mjs prepare --id meu-orc --purpose concept
```

Em uma conversa com um agente que tenha geracao de imagens, abra este repositorio e diga:

> Leia AGENTS.md e characters/meu-orc/handoff/prompt.md. Inspecione as imagens listadas no handoff.json, use a ancora de estilo e crie candidatos de conceito deste Orc. Registre os PNGs reais e mostre o preview. Preserve TBD como proposta.

Depois de aprovar o conceito, gere a roupa de outra classe:

```powershell
node src/cli.mjs outfit --from meu-orc --id meu-orc-archer --job Archer
node src/cli.mjs prepare --id meu-orc-archer --purpose outfit
```

Esse pacote preserva a identidade do individuo, usa a mesma ancora e exige a referencia racial/individual aprovada. Se a base mudar, use `refresh-base` e revise a roupa novamente. Gerar uma ficha de roupa ainda nao desenha a roupa nem os quadros de animacao.

## O que esta pronto

- Catalogos extraidos das fontes: 28 racas e 63 Jobs, com IDs locais estaveis e contexto documentado.
- Fichas de personagem/roupa, eixos independentes, perfil tecnico e Reuse Assessment.
- Receitas visuais de raca/Job com aprovacao, versoes e copias imutaveis das referencias; novas fichas reutilizam as receitas ativas.
- Pacote para LLM: prompt, ficha, contexto documental completo e lista de imagens/referencias com papeis explicitos.
- Importacao de PNG sem reescala, registro de origem e hash; composicao de camadas 2D compativeis.
- Preview HTML local, folha de contato, validacao RGBA/canvas/chao/inventario/Idle/duplicatas.
- Registro de revisoes humanas vinculado a hashes; alteracoes invalidam a aprovacao pertinente.
- Exportacao de staging para Unity com importador opcional; nunca copia diretamente no jogo.
- Hero com 97 PNGs copiados como referencia, mantendo as pendencias historicas. Orc Warrior possui 97 PNGs nativos e 24 fontes editaveis; conceito, base e conjunto animado aprovados pelo criador; pacote exportado em dist/orc-01/9b89aad88c27de68; preview em [review-animations-v1.html](characters/orc-01/review-animations-v1.html). Orc Archer e Undead Archer continuam em preparacao.
- Sete roupas Orc das demais classes basicas possuem conceitos e quatro vistas aprovados (Rogue v2), 406 PNGs nativos e 105 fontes editaveis ativas. [Primeiro combate front_r em revisao](characters/review-orc-combat-front-v1.html); [Idle/Walk das quatro vistas aprovados](characters/review-orc-locomotion-directions-v1.html). Outras vistas de combate pendentes. [Conceitos aprovados](characters/review-orc-basic-classes-v1.html).

## Para lembrar futuramente

- [Proximas etapas e como continuar entre conversas](docs/ROADMAP.md)
- [Fluxo completo e comandos](docs/WORKFLOW.md)
- [Identidade visual, inspiracoes e Hero](docs/VISUAL_IDENTITY.md)
- [Fontes, sincronizacao e conflitos conhecidos](docs/REFERENCES.md)
- [Como usar a LLM, ChatGPT e ferramentas Google](docs/GENERATION.md)
- [Camadas, roupas e animacoes](docs/LAYERS.md)
- [Memoria visual por raca/Job e receitas versionadas](docs/RECIPES.md)
- [Preparacao para Unity](docs/UNITY.md)
- [Arquitetura e limites da versao](docs/ARCHITECTURE.md)
- [Registro de verificacao desta entrega](docs/DELIVERY.md)
- [Instrucoes para agentes](AGENTS.md)

## Atualizar referencias

```powershell
node src/cli.mjs sync --source ../TacticsRPG --accept-update
node src/cli.mjs doctor
```

O snapshot guarda arquivos, hashes, commit de origem e se havia alteracoes locais. A sincronizacao le o TacticsRPG e escreve somente nesta fabrica. Atualizacoes das fontes invalidam as revisoes vinculadas ao snapshot anterior. Nao confundem design documentado com gameplay implementado.

## Desenvolvimento

```powershell
npm.cmd test
node src/cli.mjs help
```

Repositorio Git local independente; nenhum remoto ou publicacao configurado. As fontes artisticas pertencem ao projeto original; esta entrega nao lhes atribui licenca aberta. A dependencia pngjs possui sua propria licenca MIT.
