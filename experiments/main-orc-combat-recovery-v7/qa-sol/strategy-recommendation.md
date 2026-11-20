# Recomendação de estratégia — V7 rejeitado

**Escolha: A, com reuso seletivo do V6 como doador de corpo e acabamento.** Reconstruir a mecânica traseira sobre a grade frontal protegida; não restaurar o ciclo V6 como solução. V7 permanece **ARTISTIC_REJECTED**, por decisão do criador, com status operacional **ARTISTIC_REVISION_REQUIRED**. Esta recomendação não libera o pacote.

Referência: [pergunta de estratégia](../strategy-question.txt), [forense deste QA](report.md) e [relatório do QA temporal](../qa-temporal/report.md), sobre o manifesto `fde1fe23f2d637589b6abef6b9b946b6c4370cc8ae5f3927525fb038397b2579`. As observações de reprodução contínua são do QA temporal; não foram reproduzidas por este QA.

## Por que A

A oferece um contrato comum de preparação, ápice, contato e recuperação antes da autoria das poses. B preserva justamente a fundação que já foi rejeitada por atacar de lado: rotacionar apenas a arma não corrige ombro, cotovelo, palma, transferência corporal e oclusão. Se B passar a reconstruir essas partes e sincronizar as fases, torna-se essencialmente A, porém sem assumir claramente o trabalho necessário.

Reutilizar do V6 somente torso, cabeça, apoio, roupa ou clusters que continuem adequados à nova pose e à mesma vista. Não preservar o braço ou a coreografia por obrigação de reaproveitamento. Não usar o braço manual V7 como molde obrigatório: sua união à ombreira e variação de volume já têm defeitos localizados.

**A precisa abranger back_r também:** reconstruir só back_l sobre 730 ms e deixar back_r em 950 ms mantém a desuniformidade. Em back_r, começar pelo remapeamento das poses aproveitáveis e reautorar somente as ligações incompatíveis; não comprimir indiscriminadamente o ciclo inteiro.

Igualdade de quadros e tempos facilita a comparação e elimina a divergência contratual, mas não prova a mesma técnica. O julgamento decisivo continua sendo reconhecer o mesmo gesto corporal adaptado à perspectiva.

## Grade concreta e proteção frontal

Tempos abaixo conferidos diretamente nos clipes atuais de front_r, acumulados a partir de zero; contato é o início do quadro declarado, não um evento de dano Unity implementado.

| Família | Grade de referência | Ápice / coil | Contato | Arma visível |
|---|---|---|---|---|
| Sword | 13 quadros / 730 ms | F05, 225–290 ms | F07, início em 325 ms | F02–F10, 95–595 ms |
| Axe | 12 quadros / 1005 ms | F04, 220–375 ms | F06, início em 410 ms | F02–F08, 105–765 ms |

Copiar inicialmente as durações por fase, inclusive para back_r. Não adotar o exemplo genérico de impacto em 450 ms: ele mudaria a referência protegida. Não há necessidade de mudar contagem, duração ou coreografia de **front_r/Sword** para executar esta variante.

Contudo, preservar integralmente todos os pixels frontais e prometer eliminar o flash são compromissos incompatíveis se o defeito está nesses pixels. Propor um fork frontal separado, mantendo grade, trajetória e poses principais, para retoques localizados de exposição da lâmina, luz corporal e transições de entrada/saída. Apresentar o diff ao criador. Se a proteção significar imutabilidade absoluta de pixels, manter o original intacto e apresentar esse fork como alternativa explícita; não afirmar que o flash foi resolvido no original.

## Flash: frente própria de correção

A reconstrução traseira não resolve o flash frontal. Investigar separadamente os focos relatados pelo QA temporal: F01→F02→F03, F05→F06→F07 e F10→F11→F12; conferir também o ponto especular composto (132,104), front_r, e (123,104), front_l.

Priorizar continuidade da pose/material e exposição projetada do metal. A entrada do item precisa estar coerente com o preparo corporal; a recuperação precisa evitar a troca abrupta entre corpo escuro e couraça frontal acesa. Não perseguir um total fixo de pixels claros, escurecer toda a arma ou apagar highlights legítimos para passar no detector.

Um smear desenhado no Aseprite pode ser testado como alternativa local se o arco continuar estroboscópico, mas não é solução obrigatória nem licença para acrescentar um flash branco maior. Não usar cross-fade externo. A presença de quadros de 35–45 ms não prova stutter por si: o frontal protegido também os utiliza. Validar espaçamento, silhueta e ritmo em movimento antes de mudar tempos.

## Matriz de risco residual

| Risco | A com reuso seletivo | B com reparos locais | Controle antes de avançar |
|---|---|---|---|
| Permanecer ataque lateral com arma elevada | Médio: grade não corrige anatomia | Alto: preserva a fundação rejeitada | Corpo sem armas e fases-chave lado a lado |
| Perder volume/ligação do braço | Alto durante reconstrução | Médio/alto nas regiões reparadas | Ombreira–úmero–cotovelo–punho–palma em cada fase |
| Desuniformidade de cadência | Médio até adaptar ambos os traseiros | Alto sem rever os dois contratos | Relógio comum, contato e visibilidade alinhados |
| Flash frontal persistir | Alto se não houver frente específica | Alto pela mesma razão | Reprodução dos três focos, corpo e arma separados |
| Danificar o frontal protegido | Baixo com fork e diff restrito | Baixo se preservado; defeito permanece | Hash do original e comparação visual do fork |
| Retrabalho extenso sem ganho artístico | Médio/alto | Alto por repetir reparo sobre base rejeitada | Revisão de chaves antes de ciclo completo |

## Ordem de execução e portões de propagação

1. Congelar e preservar V7 e frontais de referência. Criar fontes candidatas próprias no Aseprite. Nenhuma promoção ou integração Unity.
2. Montar a tabela única de fases/tempos por família acima e mapear back_r/back_l contra ela. Separar defeitos de pose, de equipamento e de luz; não tratar tudo como problema de timing.
3. Começar por **back_l/Sword body-only**: preparação, ápice, soltura, contato e recuperação. Mostrar junto aos frontais e back_r, na mesma fase. Validar construção traseira, volume, apoio, mão dominante e leitura do plano do golpe com o criador antes de preencher o ciclo. Se essas chaves falharem, interromper a expansão e corrigir a fundação.
4. Fechar um ciclo Sword traseiro; adaptar back_r à mesma grade. Compor equipamento somente após a cadeia articular ser convincente. Em paralelo de escopo, mas sem exigir agentes paralelos, preparar o fork frontal mínimo de flash e o recorte temporal da axila front_l F02–F04.
5. Revisar **Sword nas quatro direções** em 1×, 0,5×, passo e escala tática aproximada de 64 px; usar tanto relógio comum quanto reprodução individual. Exigir a mesma técnica, ausência perceptiva de flash, pegada e retorno legíveis. O parecer estático e o temporal precisam apontar para o mesmo freeze.
6. Só então repetir o método no Axe com sua própria grade e mecânica de massa. Reutilizar método e clusters compatíveis; não transplantar o movimento Sword nem regenerar uma família inteira.
7. Antes de propagar aos derivados/matriz: revisar masters salvos e reabertos, camadas de arma desligadas, bookends desarmados, intervalos, groundY, oclusão, export RGBA, tempos, hashes dos protegidos e aliases. Gerar novo freeze e pedir parecer dos QAs sobre essa versão exata. Aprovação artística continua exclusiva do criador; autorização de integração Unity é outra etapa.

**Não gastar agora:** novas gerações PixelLab (zero autorizadas), alterações em Idle/Walk/Hit/Defeat, oito ciclos completos antes de validar chaves, infraestrutura nova de runtime ou retoques cosméticos de contorno sem ocorrência perceptiva localizada. O orçamento prioritário é reconstrução localizada no Aseprite e comparação artística cedo.

A estratégia aumenta a chance de convergência; não garante aprovação. O risco principal remanescente é desenhar uma anatomia traseira convincente dentro da referência temporal sem apenas sincronizar ataques visualmente diferentes.
