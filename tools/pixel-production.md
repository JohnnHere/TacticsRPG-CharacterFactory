# Ferramentas locais de produção de pixels

Instaladas em 2026-10-19 com autorização do criador para linguagens, dependências e ferramentas gratuitas. Downloads/runtime ficam em `tmp/`, ignorado pelo Git; PNGs, prompts e receitas reais ficam no pacote de personagem.

- uv 0.13.1: https://github.com/astral-sh/uv/releases/tag/0.13.1
- CPython 3.12.15, instalado por uv.
- Dependências fixadas em `pixel-production-requirements.txt`.
- Pixel Art Fixer, MIT: https://github.com/Retro-Diffusion/pixel-art-fixer, commit `ef376e57e1c272633ca2dbf5f29ec3fcf6596465`.
- LibreSprite 1.3 portátil: https://github.com/LibreSprite/LibreSprite/releases/tag/v1.3

## Reproduzir o processamento

Após `tools/setup-pixel-tools.ps1`:

```powershell
& ./tmp/pixel-venv/Scripts/python.exe tools/recover-native-sprite.py characters/orc-01/source/pixel-grid-v1/front-r-generated.png characters/orc-01/source/pixel-grid-v1/front-r-native.png --content-height 100 --colors 48
```

O script atua somente numa fonte artística nova destinada a sprite. Bloqueia entradas de `concepts/` e `hero-reference/`. Usa quantização estrutural por célula do Pixel Art Fixer, limita a paleta no resultado nativo e alinha o chão por translação inteira, sem espelhamento ou interpolação dos PNGs finais. A grade alvo explícita é registrada como `forced`; isso não é prova de recuperação exata de uma grade original nem de desenho manual. Todo resultado exige inspeção visual.

O PNG do processo e o relatório JSON preservam hashes, crop, transformação, versão, limites de alpha e estado artístico. O sufixo `-4x.png` é somente preview por nearest-neighbor, não asset runtime. A ferramenta não inventa animações ou substitui os gates de revisão. As gerações são estocásticas; o pós-processamento com a mesma fonte e versões é reproduzível.

## Animacoes e verificacao

As fontes e escolhas reais do Orc estao em `characters/orc-01/source/animations-v1/README.md`, `manifest.json` e `generation-calls.json`. `extract-animation-sheet.py` separa poses e aplica o contrato nativo com a paleta da base; `import-animation-clip.mjs` importa pelo CLI e preserva prompts/proveniencia. `write-animation-editable.py` cria cels RGBA com timing em formato ASE, verificadas por exportacao no LibreSprite. Essas fontes sao raster por quadro, sem rig ou separacao automatica de roupas.

`make-walk-pose-guides.py` cria somente referencias para image_gen. `finish-walk-materials.py` registra acabamento RGB, copia anterior e patches reproduziveis, preservando alpha e pose. `record-animation-provenance.mjs` registra hashes reais das fontes, prompts, referencias e editaveis; nao concede aprovacao artistica.

```powershell
node tools/build-animation-review.mjs orc-01
node tools/record-animation-provenance.mjs orc-01
node tools/verify-animation-assets.mjs orc-01
node src/cli.mjs validate --id orc-01 --stage full
```

O verificador de editaveis tambem consome os exports reais do LibreSprite em `tmp/editor-<estado>_<vista>.png/.json`; nao substitui a execucao do editor. `check-animation-preview.py` usa Playwright 1.64.0 e Edge existente para testar o HTML sem janela visivel. Dependencias opcionais em `pixel-preview-requirements.txt`; instalar no mesmo venv com uv pip. HTTP permite verificar pixels do canvas; `--file-display-only` testa exibicao local sem leitura de canvas, sujeita a restricao de origem do navegador.
