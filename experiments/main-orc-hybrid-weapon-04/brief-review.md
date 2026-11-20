# Experimento 04 — página de revisão

Você constrói a página onde o criador julga o experimento. Não produz arte.

## Limites

- Zero PixelLab. Não edite `characters/`, `assets/`, `reports/`, `../TacticsRPG`. Não faça commit.
- Escreva apenas em `experiments/main-orc-hybrid-weapon-04/review/`.

## Entradas esperadas (podem não existir quando você começar)

Produzidas por outro DEV, em `experiments/main-orc-hybrid-weapon-04/`:

- `representative/a/{body-only,weapon-only,composite}/{02,08,11}.png`
- `representative/b/{body-only,weapon-only,composite}/{02,08,11}.png`
- `full/a/` e `full/b/` — 14 quadros compostos, se o estágio completo tiver passado
- `grip-profile.json`

Fonte original, para comparação: `characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_l-sword/frames/00..13.png`
(grades: 14 quadros, 730 ms, armado F02–F11).

Se um arquivo faltar, a página deve **avisar na tela** qual falta, em vez de mostrar vazio ou
inventar. Fixture sintético permitido só em `review/fixtures/`, rotulado e carregável por `?fixture=1`.

## O que a página precisa mostrar

Quatro colunas comparáveis para o quadro selecionado:

1. **Original recuperado** (o clipe atual do front_l).
2. **Variante A composta** (Espada do Recruta).
3. **Variante B composta** (a espada nova).
4. **Somente corpo** — sem arma, para provar que o corpo é o mesmo.

Controles:
- Seletor de quadro (F00–F13) e botões de preparação (F02), impacto (F08) e recuperação (F11).
- Playback em velocidade normal e em 0,5×, usando as durações reais por quadro (não fps fixo).
- Passo a passo para frente e para trás.
- Zoom com ampliação inteira (nearest-neighbour) em 2×, 4× e 8×.
- Alternância para esconder o esqueleto/guia se houver overlay.
- **Recorte dedicado de mão e punho** em pelo menos 8×, de cada variante, porque é ali que a
  pegada se julga.
- Exibir as duas variantes lado a lado com o corpo idêntico, para evidenciar a troca de arma.

## Honestidade obrigatória na tela

Deixe explícito, em texto visível:

- que defeitos herdados da fonte **não foram corrigidos** de propósito;
- que sucesso de composição não significa aprovação artística;
- que o corpo é o mesmo nas duas variantes (se a prova de diff existir, cite o arquivo).

## Aceitação

- Abre por `file://`, sem servidor e sem dependência de rede.
- Seleção de quadro, play, 0,5×, passo, zoom e recorte de mão funcionam de fato.
- Nenhum dado inventado; ausência de arquivo é reportada.
- Prove com verificação headless própria (reaproveite o padrão de
  `test/browser-check-rear-recovery-review.mjs` e o Playwright já instalado) que a página carrega,
  que nenhuma imagem quebra e que zero erros de página ocorrem.

## Entrega

- `review/index.html` e o necessário, dentro de `review/`.
- `review/report.md`: como abrir, o que cada controle faz, resultado da verificação headless,
  e o que ficou pendente por falta de dados.
