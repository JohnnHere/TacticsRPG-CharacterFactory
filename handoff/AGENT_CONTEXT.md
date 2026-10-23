# TacticsRPG Character Factory — contexto de continuidade

**Direção mais recente, 2026-10-23:** Orc clássico medieval, principalmente World of Warcraft e também Tolkien. O criador delega paleta, textura e luz ao agente; quer cinco opções concretas do Orc Warrior para escolher uma base e refinar, buscando identidade própria e um jogo com alma. [Laboratório e critérios](../docs/ORC_ART_LAB.md), [comparação](../reports/orc-art-lab-v5/review.html). Não repetir perguntas sobre hipótese visual já definida. Escolha pendente; V4 segue produção vigente. Esta exploração precede a recomendação anterior de integração Unity.

Leia este arquivo primeiro quando outro agente assumir o trabalho. Ele resume as decisões vigentes e o estado ativo; os links apontam para contratos e evidências completas. Não trate notas históricas como seleção atual. Se este handoff divergir de uma instrução nova do criador, prevalece o pedido mais recente.

## Identidade e autoridade

Este repositório é a fábrica local de personagens e assets 2D para o TacticsRPG. O projeto Unity irmão fica em ../TacticsRPG. IDs desta fábrica são IDs de pacote, não IDs de runtime. A árvore pode conter trabalho não commitado do criador; inspecione antes de editar e preserve alterações não relacionadas.

Ordem de autoridade: pedido atual do criador → decisões aprovadas → documentos temáticos vigentes → propostas e notas antigas. Documentação de design descreve intenção; código e PlayMode provam o runtime. O snapshot em references/tacticsrpg/ é uma cópia datada e pode divergir do projeto principal atual. Consulte o snapshot para fontes de design, verifique a árvore ../TacticsRPG antes de afirmar ou editar o estado atual do jogo. Não sincronize snapshots sem autorização.

## Direção artística e autoria

- Toda arte nova e todo retoque são produzidos no Aseprite. Conceitos, sprites, poses, animações e acabamento usam .aseprite salvo como fonte mestre; PNGs e folhas são derivados. Aseprite Steam instalado em F:/SteamLibrary/steamapps/common/Aseprite/Aseprite.exe.
- Lua executada dentro do Aseprite é autoria programática permitida. Registre script, fontes, hashes e procedência; não a descreva como desenho manual nem IA gerativa do editor. A V3 foi rejeitada artisticamente; desenho genérico por coordenadas não é padrão de qualidade.
- Não usar image_gen, geração externa ou edição raster artística fora do Aseprite sem nova instrução explícita. Arte legada mantém sua procedência ao ser aberta, importada ou retocada.
- Use processos batch ocultos --noinapp enquanto o criador opera a máquina. Não controle GUI, mouse, teclado ou buffers não salvos.
- Estilo: pixel art refinada, silhueta tática clara, clusters limpos, materiais legíveis e controlados, tom heroico sério, proporção compacta sem chibi. Âncora global: references/tacticsrpg/Docs/Art/References/character_style_anchor_v1.png. Inspecione-a e as referências pertinentes. Human Warrior Pilot é referência de leitura/implementação, não uniforme nem anatomia universal.
- Personagem corporal fica sem armas empunhadas, carregadas ou embainhadas. Armas, projéteis e efeitos são assets separados; só aparecem quando ação e equipamento os invocam. Overlay, encaixes, oclusão e eventos ainda exigem implementação.

Aviso: README, seções antigas de WORKFLOW, handoffs e relatórios V1/V2/V3 podem descrever imagegen, LibreSprite ou seleções anteriores. Trate isso como histórico. Este handoff, AGENTS.md e o ponteiro de produção abaixo descrevem o fluxo vigente.

## Regra de reutilização

Consultar fontes e receitas aprovadas antes de criar. Registrar Reuse Assessment: REUSE_DIRECT, REUSE_ADAPTED, REQUIRES_EXTENSION ou CREATE_NEW, com evidência, adaptação, risco/dependências e validação. Receitas aprovadas e ativas entram automaticamente em novas fichas. Isso não significa que a ferramenta descubra e combine qualquer sprite: ainda é preciso avaliar anatomia, identidade, roupa, vista, ação e perfil.

Melhorias partem de fork dos pixels/fontes aprovados, preservando rosto, anatomia, roupa e acabamento. Não copiar coordenadas entre anatomias/poses sem revisão. Um novo Job geralmente é outra roupa do mesmo indivíduo; outro indivíduo/raça é nova ficha.

## Produção Orc ativa — Aseprite V4

Leia primeiro reports/orc-production-current.json. Ele aponta para autorização, manifesto, preview, exportação e revisões suplementares ativas. A seleção cobre oito roupas do mesmo indivíduo: Warrior, Squire, Archer, Apprentice Mage, Acolyte, Rogue, Scout e Brawler.

- 192 referências de clipe: 8 roupas × 6 ações (Idle, Walk, Attack, Hit, Defeat, Unarmed) × 4 vistas (front_r, front_l, back_r, back_l).
- 184 masters animados distintos. Warrior e Brawler reutilizam o próprio Attack como Unarmed; seis outras roupas têm Unarmed próprio.
- 856 PNGs animados únicos + 40 PNGs estáticos = 896 PNGs ativos. Seleção: 184 fontes animadas + 32 estáticas = 216 .aseprite.
- Warrior Attack/Hit front_r usa os oito quadros exatos da V4 aprovada. Nas demais roupas/vistas, a limpeza dos nove tons quase pretos mapeia à própria cor escura existente. Attack/Unarmed retornam à pose inicial da própria ação; Hit termina na pose inicial do Attack da mesma roupa/vista. Gestos de Job são preservados.
- Attack/Unarmed: [80,110,50,90,120] ms por quadro, 450 ms no total. Hit: [50,100,90] ms, total240. Idle/Walk/Defeat mantêm poses e tempos anteriores, com a limpeza de tons escuros. Conceitos e bases não foram substituídos.
- Gate de conceito/base/consistência vigente nos oito pacotes. Autorização cobre propagação artística local. Gate em jogo não aprovado; nada foi integrado ao Unity. O playback atual não consome tempos variáveis.

Abrir a [comparação antes × V4](../reports/orc-production-v4/review.html), o [guia de fontes, comandos e recuperação](../docs/ORC_ASEPRITE_V4.md), [aplicação](../reports/orc-production-v4-applied.json), [auditoria](../reports/aseprite-production-audit-v4.json) e [pacotes/ZIP](../reports/orc-production-v4-export.json).

## Próxima etapa recomendada

Os assets das oito classes básicas existem. Recomenda-se um vertical slice Unity com Orc Warrior e uma roupa distinta, como Archer: registro/carregamento, quatro vistas, Idle/Walk, ataque desarmado, Hit/Defeat, escala/chão e tempos por quadro. Confirme cada item no runtime; staging e preview locais não provam integração. Isto é sugestão, não autorização atual para escrever no Unity. Armas/overlays/VFX são trabalho separado.

## Runtime e fronteira dos repositórios

A última inspeção encontrou UnitVisuals associado ao Human Warrior Pilot. A fábrica gera staging e não sincroniza assets no jogo. Não copiar PNGs, alterar código/cenas/GUIDs ou importar Unity sem tarefa de integração autorizada. Confira o código atual antes de descrever o runtime. O checkout Unity tem outras alterações não relacionadas: nunca faça reset, limpeza ou substituição ampla.

Contratos de design relevantes: 28 raças e 63 Jobs; afinidade não cria exclusividade racial; High Elf é posição aristocrática; habilidades são aprendidas exclusivamente em árvores de talentos v2.1; recrutamento permanece narrativo. Não adicionar Jobs ou mecânicas numa tarefa de arte. Consulte references/tacticsrpg/Docs/GameDesign/DOCUMENT_INDEX.md e DESIGN_DECISIONS.md.

## Comandos operacionais

Node.js 20+ está instalado na fábrica:

~~~powershell
node src/cli.mjs doctor
node src/cli.mjs editor-check
node src/cli.mjs catalog --kind races
node src/cli.mjs catalog --kind jobs
~~~

- Nova ficha: new --id <id> --race <raça> --job <job>. Variante: outfit --from <id-base> --id <id-novo> --job <job>.
- prepare reúne ficha, instruções, contexto e referências; leia o pacote antes de produzir.
- editor-template cria fonte editável vazia. editor-fork copia fonte aprovada para edição. Salve no Aseprite; editor-export cria PNGs, tempos, hashes e preview. editor-apply atualiza slots baseline com backup e gates.
- validate --stage base|directions|full. Gate concept exige aprovação do criador. Gate base cobre vistas; Gate consistency cobre o conjunto. Validação técnica não concede aprovação artística. Gate in-game exige evidência real.
- Produzir e revisar base antes de expandir animações. Quatro vistas são desenhadas sem espelhamento. 128×128/groundY126/PPU100 é baseline técnica, não anatomia obrigatória.
- Pacotes locais de revisão ficam em dist/. Exportar não integra Unity.

Auditoria atual: node tools/audit-aseprite-production.mjs. Export Orc V4: node tools/export-orc-production-v4.mjs. Exportadores/aprovadores V1 selecionam assets históricos; não os use para restaurar a seleção antiga. Sempre leia reports/orc-production-current.json antes de retomar Orc.

## Cenários, inimigos e outros assets

O bridge Aseprite aceita character, enemy, environment, prop, effect, ui e weapon. editor-template prepara fontes; a arte precisa ser desenhada e salva no Aseprite antes do export. Tilemaps podem exportar tiles/células/flags; isso não implementa terreno 3D, altura, colisão, oclusão ou gameplay. Não declarar produção pronta porque o exportador genérico aceita o tipo.

## Referências essenciais

- [AGENTS.md](../AGENTS.md): regras persistentes, autoridade e limites.
- [docs/ASEPRITE.md](../docs/ASEPRITE.md) e [documentação de integração](../docs/ASEPRITE_INTEGRATION_V1.md): bridge, manifestos e operação.
- [identidade visual](../docs/VISUAL_IDENTITY.md), [workflow](../docs/WORKFLOW.md), [equipamentos e ações](../docs/EQUIPMENT_AND_ACTIONS.md), [receitas](../docs/RECIPES.md), [Unity](../docs/UNITY.md).
- [docs/ROADMAP.md](../docs/ROADMAP.md): evolução; consulte a seção mais recente e confirme com hashes/reviews.
- Projeto principal, [documentação V4](../../TacticsRPG/Docs/Art/ORC_ASEPRITE_V4.md). O repositório principal recebeu documentação, sem assets ou integração runtime.
- Doctor mais recente encontrou Aseprite 1.3.18.6-x64 disponível, snapshot íntegro e nenhuma chamada cloud.

## Instrução curta para a próxima sessão

> Leia handoff/AGENT_CONTEXT.md e AGENTS.md. Verifique reports/orc-production-current.json e execute node src/cli.mjs doctor. Use Aseprite como ferramenta mestre; reutilize fontes aprovadas por fork; confira hashes/reviews. Não trate relatórios V1/V2/V3 como seleção ativa. Declare qual repositório será alterado; Unity requer tarefa de integração autorizada. Ao concluir, atualize docs/ROADMAP.md e deixe links revisáveis.
