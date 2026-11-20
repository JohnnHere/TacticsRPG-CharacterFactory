# V7 back_r — bookends normalizados

`V7_BACK_R_FLASH_FIXED` · `TECHNICALLY_COMPLETE` · `VISUAL_REVIEW_REQUIRED` · `PENDING_CREATOR`

[Preview antes/depois](preview.html) · [Verificação completa](verification.json)

Transplante mecânico no Aseprite batch, perfil tmp/aseprite-v7-rearr-profile. As duas versões em rear-r permanecem intactas; cópias novas em characters/orc-v1/source/combat-recovery-v7/rear-r-flashfixed/. Os PNGs normalizados existentes de bookends/back_r-sword foram reutilizados byte a byte, sem nova decisão artística e sem geração.

| Clipe | F | Claros antes → depois (luma ≥145) | Pixels corporais alterados |
|---|---|---|---:|
| sword | 00 | 67 → 7 | 72 |
| sword | 11 | 67 → 5 | 72 |
| axe | 00 | 67 → 7 | 72 |
| axe | 11 | 67 → 5 | 72 |

Luma BT.601 = 0,299R + 0,587G + 0,114B; somente pixels opacos. F01/F10 não mudaram: sword: 7/5 pixels claros, axe: 9/5 pixels claros.

Diff nas camadas: somente body/00 e body/11, nos dois clipes. Todos os outros quadros/camadas e PNGs fora dos derivados necessários são byte-idênticos aos pais. Compostos/nativos dos bookends, tiras e mestres mudam exclusivamente como derivados dessas duas camadas. Bookends continuam sem armas e composto igual ao corpo.

Preservados 12 quadros por clipe, Sword 950 ms, Axe 1320 ms, durações individuais, intervalo armado, pegada, posições, trajetória e demais pixels. Mestres composto256 e nativo128 atualizados, mais mestre body256 explícito; os três por clipe foram reabertos/reexportados, comparados em pixels e timing (cel.position real). Recorte body→native e alpha-over conferem com zero diferenças; cada tile das tiras confere com seu PNG. Hashes reais atualizados em clip.json. Não existia nativeComposite no contrato de origem.

622 arquivos protegidos conferidos por SHA-256; rear-r, rear-alt e doadores bookends permanecem byte-idênticos. Sem escritas em frontal, V5/V6, Unity ou commits. Zero chamadas PixelLab. Evidência de pegada anterior espelhada e identificada como herdada; ela não foi alterada neste passe.

Parada em V7_BACK_R_FLASH_FIXED. Sem aprovação artística nova ou promoção automática.

Preview conferido em Chromium: 96 comparações canvas↔PNG exatas, controles e carregamento HTTP/file, sem erros JavaScript (browser-check.json).
