# Experimento 02 — Estágio F: página de revisão

Você constrói a página onde o criador julga o experimento. Não produz arte.

## Limites duros

- Zero chamadas ao PixelLab. Não edite `characters/`, `assets/`, `reports/` nem `../TacticsRPG`.
- Não faça commit. Escreva apenas em `experiments/main-orc-skeleton-02/stage-f/`.

## Entradas

1. `experiments/main-orc-skeleton-01...` — ignore.
2. As três renderizações por pose, produzidas por outro DEV, em
   `experiments/main-orc-skeleton-02/stage-bcde/{body-only,weapon-only,composite}/` nos índices
   `00, 05, 08, 09, 13`.
3. `experiments/main-orc-skeleton-02/stage-bcde/attachment.json` — os pontos de pega, pivô,
   orientação e oclusão de cada pose.
4. `experiments/main-orc-skeleton-first-01/poses-fixed.json` — as juntas anatômicas de referência.

Esses arquivos podem ainda não existir quando você começar. Escreva a página contra estes caminhos e
faça ela **avisar na tela** quando um arquivo faltar, em vez de mostrar um espaço vazio ou inventar
conteúdo. Se precisar provar que a página funciona antes dos dados chegarem, crie um fixture
sintético em `stage-f/fixtures/`, claramente rotulado, carregável por `?fixture=1`.

## As quatro vistas exigidas

Para a pose selecionada, a página deve mostrar simultaneamente, lado a lado:

1. **Esqueleto / guia de pose** — as juntas sobre o corpo, com os rótulos legíveis.
2. **Somente corpo** — sem arma nenhuma.
3. **Somente arma** — a espada com a transformação pretendida, sobre fundo que deixe a silhueta clara.
4. **Composição final** — corpo, arma e camadas de pegada juntas.

## Controles

- Seletor das cinco poses, com o nome da fase.
- Passo a passo entre poses, e zoom com ampliação inteira (nearest-neighbour), no mínimo 2× e 4×.
- Alternância para mostrar ou esconder o esqueleto sobre qualquer vista.
- Destaque dedicado da **mão e do punho**: um recorte ampliado da região de pega de cada pose, em
  pelo menos 8×, porque é ali que o criador julga se a pegada convence.
- Comparação lado a lado ligável entre composição final e o clipe de produção atual
  (`characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/frames/`), para o criador ver
  de onde viemos.
- Se houver uma sequência temporal real disponível, toque em velocidade normal usando as durações
  reais. **Não apresente cinco poses isoladas como animação validada** — escreva na tela que são
  cinco marcos estruturais, não um clipe aprovado.

## Critérios de aceitação

- Abre por `file://`, sem servidor, sem dependência de rede, sem CDN.
- As quatro vistas, o seletor de poses, o zoom, o passo e o recorte da mão funcionam de fato.
- Nenhum dado de arte inventado; ausência de arquivo é reportada honestamente na tela.
- Você deve provar com verificação headless própria que a página carrega, que nenhuma imagem
  quebra e que zero erros de página ocorrem. Siga o estilo de
  `test/browser-check-rear-recovery-review.mjs` e reaproveite o Playwright já instalado por ele.

## Entrega

- `stage-f/index.html` e o que mais precisar, dentro de `stage-f/`.
- `stage-f/report.md` curto: como abrir, o que cada controle faz, resultado da verificação headless,
  e o que ficou pendente por falta de dados.
