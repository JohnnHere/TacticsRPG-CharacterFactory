# Orc — producao das outras classes basicas

Pedido do criador: produzir as outras classes basicas com o maior reaproveitamento possivel do Orc Warrior aprovado, economizando tempo e tokens. Catalogo confirmado: Squire, Archer, Apprentice Mage, Acolyte, Rogue, Scout e Brawler. Afinidade racial nao restringe acesso. Todos os pacotes preservam o identityId de orc-01, rosto, careca, pele, anatomia e mao direita dominante. As roupas propostas nao sao receitas de classe aprovadas ou canone racial.

## Entrega atual e marco obrigatorio

Sete conceitos reais image_gen importados sem reescala para characters/orc-01-<job>/concepts/outfit-concept-v1.png; prompts e metadados reais em source/outfit-concept-v1.prompt.md e .generation.json. Modelo exato nao exposto. O alpha dos conceitos e preservado, inclusive transparencia parcial; nao sao PNGs runtime. A arte Warrior aprovada nao foi modificada.

Preview de conceitos: ../characters/review-orc-basic-classes-v1.html. O criador aprovou seis conceitos e rejeitou Rogue v1 por parecer Warrior. Rogue v2 foi gerado com capuz e roupa carvao, importado como arquivo novo e aprovado: "Aprovo o Rogue v2; siga com os sprites." Todos os sete Gates concept vigentes. V1 Rogue permanece historico rejeitado.

Primeiras bases: ../characters/review-orc-native-bases-v1.html. Produzidos 14 PNGs (sete poses front_r e sete fallbacks), canvas128x128 RGBA8, altura100, ground126, alfa parcial zero, 47–48 cores por roupa. As sete fontes novas de sprite foram geradas separadamente dos conceitos, nao por reducao deles. Todas as bases passaram na validacao tecnica (10 PASS/0 FAIL por pacote, aviso esperado fallback igual a front_r).

Sete editaveis source/native-base-v1/front_r.aseprite foram exportados pelo LibreSprite e comparados em RGBA: pixels identicos. Fontes raster completas, sem rig ou roupa separada. Relatorios ../characters/orc-native-base-validation-v1.json e orc-native-base-editor-verification-v1.json. Preview testado em Edge headless via file://: oito imagens nativas (incluindo Warrior), oito conceitos, zoom1x/2x/3x, fundo e zero erros JS; evidencia orc-native-base-review-browser-v1.json/.png. Primeiras bases aguardam avaliacao do criador antes das outras vistas; nenhum Gate base completo foi registrado.

## Reuso executado e limites

As fichas usam a identidade e appearance aprovadas, as referencias e o perfil nativo existentes. Os 97 PNGs e 20 fontes animadas do Warrior foram indexados por hash em ../characters/orc-basic-shared-source-index.json, sem criar sete copias redundantes. Reutilizam-se comandos, ferramentas de pixels, validacao, naming, ground126, canvas128 e processo de editaveis. Contexto comum por tools/prepare-orc-basic-classes.mjs e prepare-orc-native-bases.mjs, com prompts por Job. Ate esta etapa: sete chamadas de conceitos iniciais, uma revisao Rogue e sete fontes novas de base; fontes/prompts reais preservados.

As fontes Warrior sao raster completas, nao um corpo nu articulado com roupa removivel. Portanto, as poses/tempos/registro podem orientar a nova arte; pixels comuns de pele/rosto so serao reutilizados quando houver registro e mascaras compativeis verificados. Regioes do corpo escondidas pela armadura exigem autoria. O indice de referencia nao demonstra compatibilidade de camadas e a documentacao nao finge um rig inexistente.

| Componente | Decisao |
|---|---|
| Identidade, perfil, referencia e ferramentas | REUSE_DIRECT |
| Poses e timing Idle/Walk/Hit/Defeat, materiais comuns | REUSE_ADAPTED, sujeito a roupa e oclusao |
| Sete roupas, silhuetas e regioes antes ocultas | CREATE_NEW |
| Ataque Brawler | REUSE_ADAPTED do golpe corporal, com revisao |
| Disparo Archer, conjuracao Mage e suporte Acolyte | CREATE_NEW; nao usar soco Warrior como substituto |
| Armas independentes, registro Unity e eventos de acoes | REQUIRES_EXTENSION |

## Continuar

As primeiras bases foram aprovadas: "Aprovo as sete bases; produza as outras vistas." A producao das outras vistas foi executada: 35 PNGs no total, 28 editaveis, validacao175 PASS/0 FAIL, pixels identicos apos export LibreSprite. Quatro vistas em revisao: ../characters/review-orc-directions-v1.html. Detalhes em ORC_DIRECTIONS_V1.md. Trechos acima sobre primeiras bases preservam o registro daquela entrega.

As quatro vistas foram aprovadas depois: "Aprovo as vistas das sete classes; continue as animações." Gates base registrados nos sete pacotes. Primeiro lote Idle/Walk front_r executado:70 quadros novos e14 editaveis; total105 PNGs e42 editaveis. Preview ../characters/review-orc-front-locomotion-v1.html e relatorio ORC_FRONT_LOCOMOTION_V1.md. Esta revisao parcial esta pendente antes das outras vistas animadas, conforme WORKFLOW/handoffs; os paragrafos anteriores preservam etapas historicas.

Proximo: resposta real do criador sobre Idle/Walk front_r e expansao de locomocao, seguida de combate por Job. Alvo baseline:7x97 =679 PNGs;105 presentes e574 quadros animados restantes. Isso nao promete que cinco clipes genericos implementam todas as habilidades. Casts, projeteis, armas e VFX necessitam contratos proprios e suporte do jogo. Exportacao exige consistencia aprovada de cada pacote; integracao Unity e tarefa separada. Nenhuma receita racial/de Job foi autoaprovada.

2026-10-19: Walk front_r das sete roupas aprovado pelo criador. Idle quadro3 revisado para respiracao mais sutil; somente esse quadro mudou por classe. Preview atualizado: ../characters/review-orc-front-locomotion-v2.html. Idle v2 aguarda revisao; demais574 quadros continuam pendentes.

2026-10-19: Idle v2 front_r aprovado pelo criador. Idle/Walk das demais vistas produzidos:210 novos PNGs/42 editaveis; conjunto315 PNGs/84 fontes editaveis ativas,364 quadros de combate restantes. Preview: ../characters/review-orc-locomotion-directions-v1.html. Front_r aprovado preservado; somente tres vistas novas aguardam criador. Detalhes: ORC_LOCOMOTION_DIRECTIONS_V1.md.

2026-10-19: criador aprovou as tres vistas de locomocao: "Aprovo as três vistas animadas; continue o combate." Toda locomocao aprovada por hashes. Primeiro combate front_r produzido com91 PNGs/21 editaveis: total406 PNGs/105 fontes ativas,273 quadros restantes. Preview atual: ../characters/review-orc-combat-front-v1.html, somente primeiro combate pendente de revisao. Detalhes em ORC_COMBAT_FRONT_V1.md.
