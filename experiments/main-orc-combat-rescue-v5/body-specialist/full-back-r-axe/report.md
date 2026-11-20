# Orc V1 — ciclo corporal completo back_r/Axe

**BODY_BACK_R_AXE_FULL_READY**. Empacotamento **TECHNICALLY_COMPLETE**; arte **VISUAL_REVIEW_REQUIRED**. Global **ARTISTIC_REVISION_REQUIRED / PENDING_CREATOR** permanece. Sem propagação, arma, pegada ou Unity. Mesmo QA independente Sol/Codex7eaec423 deve avaliar o ciclo; nenhum QA foi chamado aqui.

## Entrega

12 quadros,1100ms, ataque one-shot que termina no guarda original. Mestres reais native128.aseprite e body256.aseprite; camadas únicas body, corpo desarmado. Exports native/00..11 e body256/00..11, strips respectivos, clip.json com tempos, caminhos e SHA-256 reais por quadro. Ground126/190, registro64,64. Lua atribui segundos0.070..0.130; verificação pelo editor confirma os tempos salvos.

F03 hoist, F04 ápice e F07 impacto repair1 reutilizam os pixels **e os bytes PNG exatos** aceitos nos marcos anteriores. Nenhuma chave foi regenerada, retocada ou sobrescrita. Seus mestres anteriores também permaneceram byte-preservados. F00/F11 usam o corpo V1 original desarmado. Sete quadros novos de transição completam a entrada, descida e recuperação.

## Método e seleção

Três jobs temporais animate_image com primeiro e último quadro fixados: guarda→hoist, ápice→impacto repair1 e impacto repair1→guarda. Primeiro foi gerada e inspecionada a ponte de descida antes da expansão das outras duas. O serviço retornou cinco imagens por job (entrada original + quatro saídas). Todos os raws, pedidos, recibos e seleções permanecem no experimento. O método/modelo não é selecionável pelo schema; não se atribui um modelo comercial por inferência.

Seleção: entrada1/2, descida2/3 e recuperação1/2/3. Entrada3 foi excluída por corte no topo do punho. Descida1 era próxima do ápice e não foi necessária; extremos retornados pelos jobs foram substituídos pelas próprias chaves exatas já aceitas. Nada foi interpolado externamente, deslocado para simular movimento, espelhado, comprimido, girado, recortado como doador ou colado como membro. Não se congelou coluna do corpo. As saídas selecionadas já têm chão126, sem offset de correção. Toda importação, composição, strips e exportação artística ocorreram no Aseprite com perfil exclusivo tmp/aseprite-body-specialist-profile, batch oculto --noinapp.

## Inspeção do produtor

Sequência final e pontes vistas como corpo inteiro sem equipamento. A mão direita sobe em cotovelo dobrado na entrada; as chaves altas preservam a construção overhead. Na descida, a cintura escapular e a dorsal acompanham a mão. F06 contém uma passagem transitória do antebraço para frente/baixo com torso já inclinado: não é rotulado como ápice overhead nem usado como prova de uma varredura horizontal pesada. O impacto preserva a base aberta, joelhos/pelve baixos e luva repair1 legível. A recuperação sobe dorsal/pelve e devolve braços baixos ao guarda. Mão inativa própria muda ao longo das poses; não se observa coluna colada. Não se vê arma/haste, membro duplicado, interrupção flutuante ou rosto frontal emprestado nos quadros selecionados. Notas e centros articulares aproximados em producer-inspection.json e clip.json são auxílio à inspeção, não prova por números.

Preview review.html oferece1× e0.5×/0.25× de velocidade, passo a quadro, seek, replay, one-shot e loop opcional. Mostra simultaneamente diagnóstico3×, nativo128 e tático64. As imagens finais foram inspecionadas sequencialmente; capturas reais do browser em descida e impacto mostram as escalas. Checks de relógio:1× chegou aF07 em~604ms e guardouF11 no término1100ms;0.5× chegou aF03 em~306ms de tempo do clipe após~600ms de parede.9/9 checks funcionais passaram. Isso comprova o player e amostras de reprodução; não se apresenta como parecer perceptual independente contínuo. A naturalidade completa1× e a ligação posterior com equipamento aguardam o QA.

## Verificações e custo

Mestres128/256 reabertos no Aseprite e24 reexports comparados: todos RGBA exatos.12/12 recortes64,64 do corpo256 conferem com o nativo128.12/12 quadros coincidem com suas entradas selecionadas. Chaves aceitas3/3 também byte-idênticas.0 pixels claros com RGB todos>190; transparência binária; chão126 em todos.80 arquivos do freeze anterior, incluindo fontes e provas dos marcos anteriores, rehasheados sem diferenças. Não se repetiu auditoria global.

Custo adicional medido:3 jobs,3 gerações (1 por ponte). Saldo anterior1370.70, saldo novo confirmado1367.70. Recibos concluídos registram cobrança real. Sem compra ou alteração de assinatura. As12 gerações da fase de chaves permanecem contabilizadas no freeze anterior, sem serem cobradas outra vez por esta montagem.

## Handoff e parada

Root deve encaminhar este freeze completo back_r/Axe à MESMA sessão independente Sol/Codex7eaec423. Parada em BODY_BACK_R_AXE_FULL_READY; nenhuma das outras três traseiras foi ampliada. Armas e pegada continuam com47326; nenhum overlay foi adicionado. Matriz, documentos globais, integração, grip-specialist e fontes anteriores não foram escritos. Aprovação artística do criador permanece pendente.
