# Experimento 01 — Visualizador do movimento (skeleton-first)

Você é o DEV responsável pelo **visualizador de revisão**. Seu produto é uma página que deixa o
criador julgar o movimento sem depender de pixel art finalizada.

Nada de arte. Você não desenha, não gera imagem, não toca em `.aseprite`, não chama PixelLab,
não faz commit, não mexe em `../TacticsRPG`. Tudo o que você escreve vive em
`experiments/main-orc-skeleton-first-01/viewer/`.

## Entradas que você consome

1. `characters/orc-v1/source/complete-v1/back_l/Idle/00.png` — corpo de referência da vista
   `back_l`, em 128×128. É o fundo sobre o qual o esqueleto será sobreposto.
2. `experiments/main-orc-skeleton-first-01/poses.json` — cinco poses-chave.
3. `experiments/main-orc-skeleton-first-01/sequence.json` — a sequência de 14 quadros.

Esses dois JSON são produzidos por outro DEV e podem ainda não existir quando você começar.
Se não existirem: escreva o visualizador inteiro contra o esquema abaixo e, se o arquivo não
estiver lá, use um `fetch` com tratamento de ausência em vez de inventar dados falsos. Nunca
embuta uma sequência inventada como se fosse a do DEV.

## Esquema esperado dos arquivos

`poses.json`:

```json
{
  "reference": { "image": "characters/orc-v1/source/complete-v1/back_l/Idle/00.png", "width": 128, "height": 128 },
  "poses": [
    {
      "id": "ready",
      "label": "Prontidão",
      "joints": [ { "label": "NOSE", "x": 0.51, "y": 0.28, "z_index": 12, "depth": 128 } ],
      "grip": { "hand": "RIGHT ARM", "point": { "x": 0.5, "y": 0.5 }, "haftDirection": { "x": 0.0, "y": -1.0 }, "bladeDirection": { "x": 0.3, "y": -0.9 } }
    }
  ]
}
```

`sequence.json`:

```json
{
  "fps": 19.2,
  "totalMs": 730,
  "frames": [
    { "index": 0, "phase": "rest", "durationMs": 30, "joints": [ ... ], "grip": { ... } }
  ]
}
```

Se o formato real entregue pelo outro DEV divergir em detalhe, **adapte o visualizador ao arquivo
real** e registre a divergência no seu relatório. Não peça que o outro DEV mude o dele.

## O que a página precisa fazer

Uma única página `experiments/main-orc-skeleton-first-01/viewer/index.html`, aberta por `file://`,
sem servidor, sem dependências de rede, sem CDN. Pode usar um script embutido.

1. **Sobreposição.** O corpo de referência de `back_l` desenhado em escala ampliada, com o esqueleto
   por cima: juntas como pontos, ossos como linhas. Destaque as juntas todas com rótulo legível.
2. **Trajetória da lâmina.** O caminho da ponta da lâmina desenhado como trilha persistente através
   de todos os quadros, com marcação de onde está o contato.
3. **Mão que segura.** Marcar de forma distinta o punho que empunha (`RIGHT ARM`) e o ponto de pega,
   além de desenhar cabo e lâmina a partir dos campos `haftDirection` e `bladeDirection`.
4. **Chão.** Uma linha na altura do chão da referência (`y = 126` de 128) para julgar contato dos pés.
5. **Reprodução.** Botão de play a 1×, botão de 0,5×, botão de passo a passo (avança e retrocede um
   quadro), e um seletor de velocidade. A reprodução deve usar as durações reais de cada quadro em
   `sequence.json`, não um fps fixo.
6. **As cinco poses-chave.** Uma faixa separada com as cinco poses lado a lado, clicáveis, que
   levam o visualizador ao quadro correspondente.
7. **Leitura de defeito.** Um indicador numérico ao lado do quadro atual com a distância percorrida
   pela ponta da lâmina em relação ao quadro anterior, para o criador ver onde há aceleração e onde
   há salto.
8. **Sem mentir na tela.** Se `sequence.json` não existir, a página deve dizer isso claramente em vez
   de mostrar uma animação vazia.

## Critérios de aceitação

- Abre por `file://` sem erro de console e sem requisição de rede externa.
- Play, 0,5×, passo e as cinco poses funcionam de fato.
- Todos os 18 rótulos COCO aparecem legíveis quando o esqueleto está visível.
- A trilha da lâmina é coerente com a sequência carregada.
- Nenhum dado de movimento inventado.
- Funciona em Chromium headless: você deve provar, com um script próprio, que a página carrega,
  que nenhuma imagem quebra e que zero erros de página ocorrem. Existe um padrão de verificação no
  repositório em `test/browser-check-rear-recovery-review.mjs`; siga o mesmo estilo e reaproveite o
  Playwright já instalado por ele.

## Entrega

- `viewer/index.html` e o que mais precisar, dentro de `viewer/`.
- `viewer/report.md` curto: como abrir, o que cada controle faz, resultado da verificação headless,
  e divergências de esquema que você teve de absorver.
