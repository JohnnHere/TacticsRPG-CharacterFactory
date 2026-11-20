# BODY-01 — impacto back_r/Axe, repair1

**BODY_IMPACT_REPAIR_READY** · **TECHNICALLY_COMPLETE / VISUAL_REVIEW_REQUIRED**. Global **ARTISTIC_REVISION_REQUIRED / PENDING_CREATOR** permanece. Sem propagação, intermediários ou chamada de QA.

Pedido: parecer independente Sol/Codex `7eaec423`, `qa-sol/keys-axe-result.json`, BODY-01 MEDIUM. A reprovação era a leitura da extremidade dominante fundida ao quadril, não amputação provada. Hoist e ápice tiveram parecer estrutural aceitável e permanecem byte-exatos nos oito mestres/exports originais.

Retoque programático local em Lua dentro do Aseprite: borda da braçadeira, pulso estreito, bloco arredondado da luva vinho, polegar interno e separações sombreadas dos dedos. A cor e os materiais retomam a luva existente e o couro do indivíduo. O primeiro posicionamento local foi inspecionado e ajustado dois pixels para dentro antes do freeze, para integrar a luva à extremidade original; não houve geração nem transformação de membro. O script atual reproduz o candidato final partindo do mestre nativo anterior. Nenhum overlay de arma esconde a mão.

Diff real: **97 pixels**, limites inclusivos **[88, 75, 98, 86]**, confinados a x88..98/y75..86. Todos os outros pixels do corpo permanecem RGBA idênticos, incluindo ombro, cotovelo, tronco, pelve, joelhos e apoios fora da máscara local. Lista completa de coordenadas/cores em pixel-diff.json. Antes/depois em review.html, escala1×/3× e zoom de mão extraído dos exports exatos. Não se usa pixel-diff como prova artística: o candidato requer parecer independente de legibilidade.

Dois mestres reais128/256 e exports salvos em characters/orc-v1/source/combat-rescue-v5/body-specialist/repair1. Ambos reabertos e reexportados pelo Aseprite: RGBA idêntico aos exports2/2. Crop64,64 do composto256 igual ao nativo128. Um frame por mestre, duração160ms verificada no arquivo e no editor (Lua0.160 segundos); chão126/190. Perfil exclusivo tmp/aseprite-body-specialist-profile, executável autorizado, batch oculto --noinapp.

Freeze anterior preservado: 54 arquivos de primeiro nível rehasheados e 53 hashes originais conferidos sem diferença. Os oito arquivos das chaves elevadas também conferidos diretamente contra os hashes do QA. Nenhuma escrita em fontes anteriores, docs globais, matriz, armas, grip-specialist ou Unity. Não houve auditoria global repetida.

**Custo adicional: zero jobs / zero gerações PixelLab**, somente retoque Aseprite local. Nenhum saldo novo consultado ou estimado. Contabilidade anterior permanece no representative original como histórico.

Root deve enviar o freeze repair1 à MESMA sessão QA independente Sol/Codex7eaec423. Não foi chamado ou criado QA aqui. Parada antes de intermediários. Aprovação artística continua exclusiva do criador.
