# Orc Warrior — fontes de animacao v1

Conceito 07 careca e base/quatro vistas aprovados pelo criador. O conjunto animado foi aprovado explicitamente pelo criador: "Aprovo o conjunto completo; exporte o pacote." Gate consistency registrado por hash em reviews.json. Preview: `../../review-animations-v1.html`. Nenhuma integracao Unity executada.

## Inventario produzido

| Estado | Quadros/vista | Duracao por quadro | Loop |
|---|---:|---:|---|
| Idle | 4 | 240 ms | sim |
| Walk | 6 | 73 ms (preview: 73,33 ms) | sim |
| Attack | 5 | 90 ms | nao |
| Hit | 3 | 80 ms | nao |
| Defeat | 5 | 120 ms | nao |

Quatro vistas independentes: front_r, front_l, back_r, back_l. Sao 92 quadros animados, mais quatro estaticas e fallback: 97 PNGs runtime em `../../sprites/`. Canvas 128x128 RGBA8, alpha binario, paleta comum de 46 cores, chao no pixel y126. Nenhum espelhamento de vista. Corpo sem armas; Attack e uma acao corporal com mao direita. Armas independentes e overlays exigem extensao da fabrica/runtime.

Cada pasta selecionada contem fonte raster real, prompt, poses extraidas, quadros nativos, relatorios de processamento, strip, preview animado e fonte `.aseprite` com cels RGBA e timing. A fonte editavel e uma camada raster por quadro; nao e um rig nem pecas de roupa separadas. As quatro fontes estaticas estao em `../pixel-grid-v1/`.

Pastas finais: `<Estado>/<vista>/`, exceto Walk front_r em `Walk/front_r/curated-v2/` e Attack back_l em `Attack/back_l/corrected-v2/`. `manifest.json` identifica cada arquivo selecionado, hash, referencias reais de geracao, prompts, processamento e fonte editavel. `generation-calls.json` registra as 23 chamadas reais de imagem, incluindo tentativas rejeitadas. O modelo exato nao foi exposto pela ferramenta image_gen.

## Autoria e tratamento

As poses foram geradas por image_gen a partir da base aprovada, preservando individuo, roupa e assimetrias. Fontes de conceito e Hero nao foram reduzidas para fabricar quadros. Algumas caminhadas usaram guias grosseiros de pose 2D: esses guias sao referencia de movimento, nao sprites de producao. O processamento usa Pixel Art Fixer com grade alvo explicita (`forced`), paleta comum e alinhamento inteiro; nao constitui prova de recuperacao exata da grade original ou desenho manual.

Walk front_r combina recortes RGBA sem espelhamento de duas geracoes selecionadas por `curate-cycle.py`; o ciclo original e uma tentativa que nao alternou pernas ficam preservados como rejeitados. Attack back_l foi corrigido por image_gen para atacar com o braco direito. Dezoito quadros Walk receberam acabamento RGB documentado em `material-finishing.json` e patches por quadro, sem mudar alpha, pose ou paleta; as fontes anteriores ao acabamento estao preservadas para replay exato.

## Evidencias

`../../reports/full-validation-v1.json`: 489 PASS, 0 FAIL, um aviso esperado de fallback duplicado. `../../reports/animation-assets-verification.json`: inventario, paleta, alpha, registro, hashes e fontes; vinte fontes animadas exportadas no LibreSprite e comparadas em RGBA, contagem e timing. `../../reports/animation-preview-browser.json` e `animation-preview-file.json`: cinco estados e 92 quadros exercitados no Edge headless; file:// usa teste de exibicao porque leitura de pixels em canvas local e restrita pelo navegador. `animation-review-browser.png` e `defeat-last-frame-browser.png` sao capturas reais.

Reproducao de geracoes nao e garantida; fontes raster e prompts reais foram arquivados. O processamento local pode ser reproduzido a partir dessas fontes e versoes fixadas. Pacote exportado em dist/orc-01/9b89aad88c27de68 na raiz da fabrica. PlayMode e aprovacao em jogo permanecem NOT_RUN.
