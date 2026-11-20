# V6 — reconstrução traseira, checkpoint back_l

Checkpoint: **V6_BACK_L_REFERENCE_READY**. Estado técnico: **TECHNICALLY_COMPLETE**. Estado artístico: **VISUAL_REVIEW_REQUIRED**, `PENDING_CREATOR`. Etapas C–D bloqueadas; esta entrega para no checkpoint de referência back_l.

## Etapa A

[Classificação integral dos 48 quadros](audit.md), [dados estruturados](audit.json), [playback V5 das quatro células](audit-preview.html) e [verificação do playback](audit-playback-check.json). Corpo inteiro layers-off e composição foram inspecionados nas folhas por quadro e confrontados com reprodução normal no player. As observações sobre movimento são julgamento do DEV, não QA independente.

KEEP aplica-se somente aos bookends como referência de identidade, apoio e fechamento. As poses intermediárias back_l foram classificadas REAUTHOR_KEYFRAME: corrigir apenas binding não resolve o salto do punho na espada nem a passagem abrupta da elevação para a inclinação no machado. back_r foi apenas auditado, com problemas de pernas/apoio e transição registrados. Não houve propagação da Etapa B a essa vista.

## Método e tentativas

1. Duas requisições `animate_with_skeleton_v3`, uma por família, 12 poses cada, referência corporal desarmada V1 e esqueletos explícitos. Descrição corporal não menciona equipamentos. Identidade, dorsal, tassets e materiais são herdados do corpo V1, não uma criação do zero.
2. Inspeção layers-off revelou antebraços ocultos nas descidas e pixels claros periféricos. Uma tentativa Aseprite Lua de reconstrução articular local foi testada e rejeitada pelo próprio DEV: braços estreitos e rígidos demais. Está preservada em `rejected-local-arm/`, com mestres, derivados e script. Seus testes técnicos não são evidência da referência final.
3. Segundo par mínimo de requisições: punhos fora da silhueta, profundidade explícita de ombro/cotovelo/punho direitos, poses próprias por família e mesma identidade desarmada. Os raws não são alterados por Pillow. A seleção final e o acabamento são feitos no Aseprite batch, perfil exclusivo `tmp/aseprite-v6-rear-profile`.

A segunda dupla foi selecionada. Os braços inteiros dessas poses substituem a tentativa local; o script final não executa a reconstrução geométrica de membros rejeitada. O acabamento Aseprite escurece pixels neutros claros apenas no contorno externo, normaliza alfa e remove componentes desconectados com até oito pixels. Metal iluminado no interior é preservado. A oclusão `handFront` vem da própria luva de cada pose, em regiões medidas e documentadas em [anatomy-plan.json](anatomy-plan.json), copiando os pixels já acabados do corpo.

Sword: 12 quadros, **950 ms**; Axe: 12 quadros, **1320 ms**. Intervalo visível inclusivo **F01–F09**, com F00/F10/F11 sem equipamento. A tabela por quadro nos dois `clip.json` contém fase, tempo, proveniência, palma e rotação; F00/F11 conservam o corpo desarmado de referência V1. F01–F10 derivam de seus respectivos quadros completos `raw-reference2`, sem duplicar pixels entre famílias. A duração adicional do machado se concentra em preparação alta, absorção e recuperação.

O corpo usa transferência de peso com deslocamento de quadril e flexão dos joelhos, sem mover a imagem inteira como substituto da ação. Sword tem curva diagonal e recuperação mais curta. Axe tem elevação sustentada, descida mais comprometida e recuperação mais lenta. A mão esquerda não segura o item. Nenhuma vista oposta ou frontal foi espelhada.

## Proveniência e contabilidade

Pedidos, sementes, recibos de submissão, resultados e PNGs brutos estão nesta pasta. [Ledger](pixellab-ledger.json) separa custo de cada job da variação observada do saldo da conta. Foram quatro jobs de 3 gerações: 12 gerações atribuíveis a este DEV, 48 saídas brutas; a primeira dupla e a tentativa local não foram escolhidas como referência final. Saldo medido: **1336,70 → 1306,70**, variação global de **30,00**. Desses, **12,00** são comprovados pelos quatro recibos desta frente; os **18,00 adicionais** ficam sem atribuição neste relatório. O saldo da conta não é tratado como contabilidade exclusiva deste DEV. Nenhum custo monetário ou total de tokens foi estimado. Nenhuma compra foi executada.

| Família | Job selecionado | Seed | Fonte por pose |
|---|---|---:|---|
| Sword | `61ca245f-d86e-4ca8-a8eb-7886f5732df7` | 61129 | `raw-reference2/sword/01.png` a `10.png` + acabamento Lua |
| Axe | `8e309cdd-cd08-45e6-a0d7-2825842e286e` | 62129 | `raw-reference2/axe/01.png` a `10.png` + acabamento Lua |

Recibos finais: `sword-reference2-completed.json`, `axe-reference2-completed.json` e `balance-final.json`. A chamada auxiliar `wait_for_jobs` encontrou erro de decodificação JSON no cliente; a recuperação usou consulta `get_image` e download oficial por índice, sem repetir submissões ou criar jobs adicionais.

## Contratos e revisão

Mestres reais composto 256 e corpo nativo 128, registro [64,64], chão composto 190/nativo 126. Camadas `weaponBack → body → weaponFront → handFront`; `nativePng` contém somente o recorte do corpo. Os itens independentes são os Sword/Axe V5 existentes. Tempos são atribuídos em segundos na API Lua. Exportação ocorre depois de salvar e reabrir os mestres; pixels e tempos são comparados.

O preview apresenta as mesmas duas células antes/depois, com corpo inteiro sem camadas de equipamento e composição, 1×/0,5×, passo, slider, zoom e escala tática. Igualdade alfa-over, hashes e testes de UI não demonstram ausência semântica de equipamento no corpo nem qualidade artística. Essas questões são inspecionadas separadamente.

Evidências: [preview](preview.html), [contratos por quadro e roundtrip](technical-checks.json), [checks Chromium](preview-check.json), [preservação](preservation-check.json). Aseprite executado: versão de arquivo **1.3.18.6**, API 41, `--batch --noinapp`. **5907 arquivos** do inventário inicial permaneceram byte-idênticos, sem ausências. O teste Chromium compara os pixels dos 24 quadros de corpo e 24 compostos exibidos com os PNGs selecionados; o script não mede qualidade artística.

Leitura do DEV em escala nativa e tática: a curva de punho da espada progride da elevação à extensão lateral e à saída baixa; o machado sustenta a mão mais alta e a descida acompanha maior abaixamento de tronco/quadril e flexão das pernas. Corpo layers-off não apresenta equipamento reconhecível nas poses selecionadas. Esse é um achado de inspeção visual, não uma prova algorítmica de semântica. A geometria e escala do item vêm do mesmo asset independente em todos os quadros; sua projeção e a sensação de massa continuam sujeitas à revisão artística.

## Limites e próximo marco

Esta é uma referência candidata para revisão do orquestrador e do criador. O ajuste das luvas, a coerência volumétrica entre keyframes, a direção do golpe e a sensação de peso ainda dependem do julgamento artístico. Não é evidência de calibração no Unity ou de aceitação do criador. Etapas C–D continuam bloqueadas. Idle, Walk, Unarmed, Hit, Defeat e frontais não fazem parte das edições desta frente. Sem commits ou escrita em `../TacticsRPG`.
