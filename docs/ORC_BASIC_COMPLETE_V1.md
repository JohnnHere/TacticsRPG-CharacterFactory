# Sete classes Orc — conjunto de corpo e roupa

Atualizacao posterior: o criador gostou da baseline e pediu auditar equipamentos e incluir ataque basico desarmado em todos os personagens. Esta entrega descreve os cinco estados legados; nao e inventario completo por equipamento. Padrao em [EQUIPMENT_AND_ACTIONS.md](EQUIPMENT_AND_ACTIONS.md), primeiro lote adicional em [ORC_UNARMED_FRONT_V1.md](ORC_UNARMED_FRONT_V1.md). Consistencia/export das sete variantes continuam pendentes; a revisao vigente e o primeiro lote unarmed, nao uma reconfirmacao da baseline anterior.

Entrega em 2026-10-19: Squire, Archer, Apprentice Mage, Acolyte, Rogue e Scout e Brawler do mesmo individuo orc-01. O Warrior aprovado/exportado permanece intacto. Preview: [review-orc-basic-complete-v1.html](../characters/review-orc-basic-complete-v1.html).

O criador aprovou o primeiro lote de combate: "Aprovo o combate front_r; continue as outras vistas." A decisao real e os hashes constam em characters/orc-combat-front-approval-v1.json e nos sete source/combat-front-v1/review.json. Essa aprovacao foi registrada antes da expansao.

Foram acrescentados 273 quadros e 63 clipes editaveis nas vistas front_l/back_r/back_l. Cada classe agora possui 97 PNGs: fallback + quatro vistas estaticas + 92 quadros animados. Sao 679 PNGs, 140 clipes animados editaveis e 28 fontes estaticas editaveis ativas, total168. Fontes candidatas substituidas permanecem em pastas historicas; nao fazem parte desse total.

| Estado | Quadros por vista | Duracao por quadro | Playback |
|---|---:|---:|---|
| Idle | 4 | 240ms | loop |
| Walk | 6 | 73ms | loop |
| Attack | 5 | 90ms | acao unica |
| Hit | 3 | 80ms | acao unica |
| Defeat | 5 | 120ms | acao unica |

Todas as quatro vistas sao fontes independentes, sem espelhamento. O Archer gira o tronco durante a puxada em front_l e back_r para preservar o tiro destro; a vista inicial/final permanece a correspondente base aprovada. Em back_l, os gestos acima do ombro de cinco Jobs aproveitam a sequencia corporal valida do Squire como referencia para novas renderizacoes de roupa, com mao direita ativa. A compatibilidade artistica dessas adaptacoes esta em revisao, nao foi autoaprovada.

Reutilizacao: identidade, bases/vistas aprovadas, paleta de cada roupa, timing/registro/naming e ferramentas locais. Permanecem byte-identicos os371 quadros animados e105 editaveis anteriormente aprovados, alem do conjunto97 PNG/20 clipes do Warrior. Nao existe corpo nu separado sob sua armadura nem rig de roupas: as fontes entregues sao cels raster RGBA, sem camadas anatomicas ficticias. Detalhes em cada source/complete-v1/reuse.json.

As primeiras folhas tiveram contaminacao de camera e algumas poses trocaram o braco ativo. As tentativas reais foram preservadas; somente estados necessarios foram regenerados e selecionados, mantendo impactos/quedas validos. Prompts, referencias, origens e hashes reais constam em source/combat-directions-v1 e v2, row-selection.json de cada clipe e orc-combat-directions-generation-audit-v1.json. O modelo da ferramenta integrada nao e exposto. Uma tentativa de Brawler teve output rejeitado pela ferramenta, sem arquivo retornado; a adaptacao posterior por referencia do Squire foi gerada normalmente. Nenhum output inexistente foi inventado.

Validacao:

- CLI full:489 PASS/0 FAIL por classe, total3423 PASS/0 FAIL. Sete avisos esperados de fallback igual a front_r; Unity NOT_RUN e revisao humana pendente continuam explicitos.
- Nativos:128x128 RGBA8, transparencia binaria, ground126, paleta da propria roupa, quadros distintos e inventario completo.
- LibreSprite1.3:644/644 quadros animados e duracoes identicos aos PNGs;28 fontes estaticas tambem verificadas. Hashes dos editaveis ativos preservados.
- Edge via Playwright:644 imagens carregadas em HTTP e file://;644/644 hashes RGBA de canvas identicos; cinco estados, quatro vistas, filtros, zoom, velocidades, scrub, fundos, repeticao e parada no quadro final verificados. Zero erros JavaScript; servidor de teste encerrado.
- npm test:6/6 testes locais aprovados. Nenhuma escrita no projeto Unity.

Evidencias principais: characters/orc-basic-complete-validation-v1.json, orc-combat-directions-editor-v1.json, orc-basic-complete-browser-v1.json, seis capturas de navegador e reports/validation.json de cada pacote.

Proxima etapa: revisao artistica final do conjunto pelo criador, exigida por AGENTS.md e WORKFLOW.md antes da exportacao. Pergunta enviada com o preview completo. Os sete source/complete-v1/review.json registram PENDING_CREATOR_COMPLETE_REVIEW com fingerprints de97 PNGs/24 editaveis por classe. Nao existe Gate consistency aprovado para as sete variantes. Ao receber aprovacao explicita, conferir esses hashes, registrar os sete Gates consistency e exportar localmente para dist/<id>/<build>/Assets/Resources/Characters/<id>/. Nao pedir reconfirmacao para a exportacao ja autorizada depois desse marco.

Armas, projeteis e VFX sao assets independentes ainda pendentes. Os gestos sao do corpo, com maos vazias. Overlays dinamicos, casts, tiro sincronizado e extensao UnitVisuals exigem tarefa propria; composicao offline nao os implementa. Integracao no jogo e Gate3 permanecem separados.

Revalidacao local:

```powershell
node tools/verify-orc-basic-complete.mjs
node tools/build-orc-basic-complete-review.mjs
& 'tmp/pixel-venv/Scripts/python.exe' tools/check-orc-basic-complete-preview.py
```

Nao reexecutar os preparadores historicos que registram aprovacoes ou substituem selecoes de fontes. O pacote final usa animations-v2/Attack/back_r apenas no Archer; o resto das novas direcoes usa animations-v1. O indice de editaveis e o manifesto completo sao a fonte da selecao ativa.
