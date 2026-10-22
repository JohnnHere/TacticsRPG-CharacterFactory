---
name: character-art-design
description: Criar, adaptar, animar e validar personagens 2D em pixel art do TacticsRPG, com análise de reutilização e preparação de integração Unity. Use para arte de personagens e auditoria do pipeline; não para implementar gameplay.
---

# Character Art Design

Trabalhe a partir da raiz do TacticsRPG; caminhos `Docs/` e `Assets/` são relativos à raiz, recursos abaixo são relativos a esta skill. Não dependa de conversas anteriores. Versão 1.0.

## Entrada e contexto

Identifique o modo: **DESIGN**, **GENERATE**, **ADAPT**, **ANIMATE**, **VALIDATE**, **PREPARE_INTEGRATION**, **INTEGRATE** ou **AUDIT**. Combine modos apenas dentro do pedido autorizado.

Leia `AGENTS.md` quando existir (na auditoria inicial só havia `Docs/AGENTS.md`), `Docs/ART_DIRECTION.md`, `Docs/Art/CHARACTER_PIPELINE.md` e `Docs/Art/Characters/CHARACTER_TEMPLATE.md`. Inspecione `Docs/Art/References/character_style_anchor_v1.png` se houver visão; senão declare a limitação e use as regras escritas. Consulte [project-contract.md](references/project-contract.md) para localizar fontes e divergências. Reuse auditorias recentes, confirmando arquivos alterados e o código pertinente; não releia todo o projeto em tarefas pequenas.

Raça, Job, cultura, facção, indivíduo, equipamento e forma são eixos separados. Consulte fontes temáticas somente conforme o personagem. Não invente cânone ausente: marque propostas e `TBD`. O anchor define linguagem visual; o piloto não define protagonista, anatomia universal, roupa ou paleta obrigatória. Preserve pixel art refinada, proporções táticas compactas sem chibi obrigatório, maturidade, clusters limpos, silhueta legível, materiais e iluminação coerentes. Não promova conceitos A/B a cânone.

## Recursos por modo

- DESIGN / ADAPT: [design-and-reuse.md](references/design-and-reuse.md) e [character-package.md](templates/character-package.md).
- GENERATE: [image-generation-capabilities.md](references/image-generation-capabilities.md) e [generation-prompt.md](templates/generation-prompt.md). Verifique ferramentas reais nesta sessão antes de prometer arquivos.
- ANIMATE / PREPARE_INTEGRATION / INTEGRATE: [production.md](references/production.md).
- VALIDATE / AUDIT: [validation.md](references/validation.md), [validate_character_assets.ps1](scripts/validate_character_assets.ps1) e [review-and-report.md](templates/review-and-report.md).
- [delivery-audit.md](references/delivery-audit.md) registra a auditoria inicial, testes conceituais e limitações de descoberta; é evidência datada, não contrato canônico.

## Fluxo e gates

1. **Brief:** preencha o pacote com identidade, papel (jogável/inimigo/NPC/invocação), anatomia, silhueta, equipamento, paleta e relação com assets. Use o template canônico; pergunte só por lacunas que bloqueiam a etapa atual.
2. **Reuse Assessment:** classifique cada componente em `REUSE_DIRECT`, `REUSE_ADAPTED`, `REQUIRES_EXTENSION` ou `CREATE_NEW`, com fonte, evidência, adaptações, riscos, dependências, validação e impacto de produção. Dimensões iguais não comprovam compatibilidade.
3. **Conceito:** gere candidatos apenas com capacidade e autorização reais; sem geração, entregue o pacote transferível. Exiba arquivos existentes. **Gate 1: aprovação explícita do conceito pelo criador antes de produção de sprites.** Autorização de gerar não equivale a aprovação artística.
4. **Base:** produza/solicite a primeira vista estática em resolução nativa; valide alfa, clusters, proporções, luz, chão e escala antes de expandir. Não trate redução de conceito como sprite pronto.
5. **Direções:** quatro diagonais desenhadas individualmente, sem espelhamento; preserve mão dominante e assimetrias. Perfil excepcional exige parâmetros próprios e validação, não conformidade automática.
6. **Animações:** siga a ordem do pipeline, com revisão por lote. **Gate 2: aprovação explícita da consistência entre vistas e clipes.** Não produza todos os frames antes de validar a base.
7. **Integração:** PREPARE_INTEGRATION entrega inventário e plano sem alterar Unity. INTEGRATE exige autorização explícita para assets/import/registro e, quando necessária, para a extensão arquitetural cujo escopo deve ser apresentado primeiro. Autorizações já dadas persistem; não solicite novamente. Não altere Core por necessidade visual, nem substitua a arquitetura por Animator/rig/Spine.
8. **Final:** verificações técnicas e PlayMode manual. **Gate 3: aprovação final em jogo pelo criador.** Registre aprovação, defeitos, `NOT_RUN` e pendências; testes não concedem aprovação artística.

## Limites e conclusão

Não instalar dependências, conectar serviços ou usar APIs pagas sem autorização; não solicitar/expor credenciais. Não substituir anchors nem modificar documentos canônicos como efeito colateral. Referências recebem versão e status `approved`, `candidate`, `deprecated` ou `experimental`; somente o criador aprova/substitui.

Entregue somente o modo solicitado: pacote de design, arquivos realmente existentes ou relatório, Reuse Assessment, capacidades verificadas, testes e próximo gate. Diferencie `PASS`, `FAIL`, `WARNING`, `NOT_RUN` e `REQUIRES_HUMAN_REVIEW`. Conclusão de design não significa suporte de runtime ou produção aprovada. Registre recomendações de extensões para etapa futura.
