# Design, anatomia e reutilização

Rendering universal: clusters intencionais, detalhe controlado, materiais distintos, sombras e luz consistentes com anchor, leitura no zoom do jogo. Prata/azul/couro do piloto são exemplos, não paleta de todas as raças. Declare direção de luz no brief a partir da referência observada; não invente um ângulo canônico numérico.

| Perfil organizacional | Aplicação possível | Validação adicional |
|---|---|---|
| Humanoide padrão | Humano Knight | Baseline do piloto; novo registro ainda necessário |
| Humanoide robusto | Orc/Troll/Anão, conforme brief | Massa, passada, altura, equipamento e clipping |
| Humanoide pequeno | Goblin/Gnomo | Escala própria, legibilidade e chão |
| Humanoide grande | Ogro | Canvas, oclusão, footprint e escala |
| Humanoide alado | Harpia | Asas, chão/voo, estados e oclusão |
| Quadrúpede | Fera | Contatos, gait e amplitude |
| Corpo híbrido | Centauro | Torso humano + corpo equino, múltiplos contatos |
| Não humanoide | Criatura distinta | Direção, locomoção e estados próprios |
| Forma transformada | Lobisomem | Pacote por forma, vínculo de identidade e transição |
| Entidade/invocação especial | Espírito/constructo convocado | Material, ancoragem, ciclo de vida e estados |

Perfis são classificação artística inicial, não novas classes C# nem suporte implementado. Não force canvas/altura do humano a todas as anatomias. Humano de referência é validado; cada combinação raça/Job continua exigindo análise. Formas do Lobisomem além de humano/combate são propostas até aprovação.

## Matriz de decisão

| Categoria | Critério com evidência | Exemplos e fronteiras |
|---|---|---|
| A `REUSE_DIRECT` | Sem mudança funcional; confirmar contrato atual | Regras de rendering, templates, fórmula direcional, procedimentos de import, controlador genérico `UnitView` no perfil compatível |
| B `REUSE_ADAPTED` | Compatibilidade demonstrada após adaptação | Pose, gait humanoide, paleta/material, base anatômica e partes de equipamento; justificar anatomia/identidade |
| C `REQUIRES_EXTENSION` | Runtime/processo não atende requisito | Registro multi-personagem, camadas de armas, sockets, transformação, novas ações, tiro sincronizado, voo, montaria, footprint multi-tile |
| D `CREATE_NEW` | Não existe elemento artístico compatível | Rosto, silhueta, anatomia racial distintiva, ornamento cultural original, pose/ciclo não coberto |

Classifique separadamente arte e integração: desenho novo de quadrúpede é D; suporte técnico a seus contatos/estados pode ser C. Não classifique toda anatomia incomum automaticamente como runtime impossível; marque candidato a validação e enumere os requisitos ainda não demonstrados.

No Reuse Assessment, inclua para cada linha: componente, fonte e trecho/asset, categoria, justificativa, adaptações, risco artístico, risco técnico, dependências, status de validação e impacto no trabalho (redução estimada/novo trabalho/migração, sem prometer prazo sem evidência).

Orc Berserker requer corpo/rosto/silhueta próprios; recolorir o piloto não basta. Pele, presas, ornamentos, cultura e cores não definidos são propostas a aprovar, não características raciais definitivas. Não confunda afinidade a Job com exclusividade racial.
