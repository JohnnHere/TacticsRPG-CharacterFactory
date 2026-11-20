# QA independente final — Orc V1 combat-rescue-v5

Veredito: **READY_FOR_CREATOR_REVIEW**. Status: **TECHNICALLY_COMPLETE / VISUAL_REVIEW_REQUIRED / PENDING_CREATOR**. Nenhum defeito bloqueante confirmado; nenhuma correção de arte exigida por este parecer.

Revisor: sessão Codex atual, independente da produção deste candidato. Não é o revisor Gemini/Antigravity anterior nem a sessão Copilot histórica. Data: 2026-10-29. Não houve delegação, geração PixelLab, edição artística, promoção ou operação no Unity.

Objeto exclusivo: `characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json`, SHA-256 `58152a101e16cbc031349b3308649f9ccaa38b99782d4e23bcf2ee43fddc3794`. Matriz: 28 células, 13 candidatas e 15 aliases, 226 quadros. Página avaliada: `Biblioteca de Arte/Estudos Comparativos/Orc principal - Resgate de combate/index.html`. O diagnóstico inicialmente dirigido a um pacote histórico foi descartado como evidência deste candidato.

## Evidência nova desta sessão

- `validate.mjs`: PASS, 28 células, 226 quadros, 964 hashes. Verifica referências, fontes, tempos, pixels, composição e política de visibilidade; saída em `technical-validation.json`.
- Aseprite batch: 42 mestres salvos reexportados, 448 comparações de quadros/tempos, PASS. As 448 são comparações entre fontes/derivados, não quadros únicos. Evidência em `source-reexports/result.json`; executor em `source-check.mjs`, adaptado do verificador existente somente para gravar nesta pasta de QA.
- Player real Chromium: 21/21 verificações, incluindo seleção das 28 células, imagens carregadas, passo a quadro, escala de apresentação e retenção terminal de Defeat. Capturas em `browser/`. Comando: `node test/browser-check-rear-recovery-review.mjs --review-dir "Biblioteca de Arte/Estudos Comparativos/Orc principal - Resgate de combate" --manifest characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json --shot-dir experiments/main-orc-combat-rescue-v5/qa-independent-final/browser`.
- Comparação independente da matriz incorporada na página: 226/226 quadros com pixels visíveis/alfa e duração iguais aos canônicos. Caminhos das cópias de biblioteca foram resolvidos relativamente à página, sem exigir identidade de caminho.
- Reprodução dos oito ataques nas velocidades 1, 0,75 e 0,5: 24 execuções, todos os quadros observados e retorno de ciclo observado em todas. Observações temporais e sequências capturadas em `playback-result.json` e `*-playback-*.png`; executor `playback.cjs`.
- Inspeção visual direta dos 28 grids compostos, oito grids de corpo com equipamento desligado e detalhes das pegadas em `grips.png`. Os grids são layouts diagnósticos dos PNGs atuais; não são arte nova. Ordem de leitura: esquerda para direita, depois linha seguinte; índices começam em zero.
- Comparação RGBA com inversão horizontal das vistas opostas de Sword/Axe: zero pares de quadros correspondentes exatamente espelhados. Isto exclui flip integral exato nos pares testados; não prova por si só anatomia ou autoria independente.

## Parecer visual

Sword apresenta preparação, elevação, passagem diagonal e recuperação legíveis. Axe possui ápice acima da cabeça, descida e assentamento mais pesados; as traseiras usam flexão do tronco mais pronunciada. Os corpos inspecionados com camadas de equipamento desligadas não exibem segunda lâmina/haste/cabeça de machado confirmável. A cadeia braço–punho permanece legível; nos detalhes compostos, o cabo encontra a manopla, com oclusão compatível em vez de arma flutuante. A arma desaparece no repouso e após o golpe.

Os quatro Unarmed mostram extensão do punho e recuperação sem equipamento. Walk traseiro mantém construção dorsal e alternância de pernas; Idle permanece sutil. Hit conserva reação cravada, sem exigir amplitude universal. Defeat progride ao solo e conserva volume terminal nas quatro vistas. Nenhuma dessas observações concede aprovação artística do criador.

Não foram confirmados resíduos de arma no BODY, membro duplicado, punho separado ou quebra de silhueta que justifique novo reparo antes da avaliação do criador. Igualdade de pixels, hashes e composição não foi usada isoladamente para concluir ausência semântica de arma.

## Observação não bloqueante e limites

**DOC-01 — LOW:** o relatório integrado anterior em `qa-antigravity-flash/integrated-candidate-report.md` descreve Walk como 16f/1600ms em todas as vistas. O manifesto e os clipes atuais declaram corretamente **16f/1280ms nas frontais e 8f/1280ms nas traseiras**. É imprecisão daquele laudo, sem divergência entre candidato e player; este parecer registra os valores corrigidos e não altera o laudo anterior.

A avaliação temporal usa amostras e capturas ordenadas do player headless, não percepção humana de vídeo contínuo. A execução temporal completa nas três velocidades foi dos oito ataques; os outros vinte clipes receberam inspeção estática e verificações de integração, não a mesma bateria temporal. Os 3.506 arquivos da preservação histórica não foram reauditados nesta sessão; essa contagem permanece evidência anterior, não checagem nova. Não houve teste em Unity, aferição de câmera/eventos/hit-stop ou aprovação para integração.

Este parecer vale apenas para o manifesto e assets correspondentes verificados nesta sessão. `runtimeImplemented: false`, `eligibleForIntegration: false`, `creatorApproved: false`. Próximo portão: avaliação visual do criador. Qualquer mudança posterior exige revisão da versão alterada. Arquivos escritos restringem-se a evidências de QA, além do diagnóstico histórico inicial já explicitamente desconsiderado; nenhuma fonte, exportação de produção ou página foi editada.

Contabilidade: zero chamadas PixelLab de produção; custo LLM não informado.
