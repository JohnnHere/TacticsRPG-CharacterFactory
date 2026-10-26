> **HISTÓRICO REJEITADO / SUPERADO.** Ataques artisticamente rejeitados pelo criador. Idle/Walk armados e movimento comum Sword/Axe não são política atual. Consulte [resgate do Orc principal](MAIN_ORC_ONE_HANDED_RESCUE.md). Preservado como procedência e comparação, nunca como receita de produção.

# Orc V1 — primeiro jogável selecionado e primeiras armas

2026-10-25. Criador selecionou a pele Verde Warcraft v3 e nomeou o personagem **Orc V1**, primeiro jogável para futura integração. Mesmo indivíduo/armadura do Infante 05; fontes novas em characters/orc-v1/. Original cinza e todas as variantes preservados. Biblioteca: Orcs Atuais/Orc V1/; original em Orcs Atuais/05 - Infante de Ferro/, previsto para integração em estágio mais avançado. Página de armas: Personagens Jogaveis/Orc V1/index.html.

## Entrega real

Revisão candidata v2: [procedimento, arquivos e reutilização](ORC_V1_WEAPONS_V2.md). O inventário e as validações abaixo descrevem exclusivamente o lote v1 histórico.

**Situação atual:** a entrega v1 descrita abaixo foi rejeitada pelo criador em 2026-10-25. A revisão v2 candidata está em `experiments/orc-v1-weapons-v2/`: acabamento coerente com o jogo, espada maior, pegada com oclusão real, família de golpe reutilizável e Idle armado no padrão fixo. Coerência visual não exige copiar a paleta ou o design do Orc; as armas devem servir futuramente a várias classes e raças. Ver `docs/WEAPON_ART_STANDARD.md`. Não usar a aprovação do corpo como aprovação do equipamento.

| Item | Asset separado | Walk armado | Golpe |
|---|---|---|---|
| Espada do Recruta | 64×64 + mestre em assets/weapons/recruit-sword/ | 16 × 80 ms, ciclo 1280 ms | 9 quadros, 1025 ms |
| Machado de Milícia | 64×64 + mestre em assets/weapons/militia-axe/ | 16 × 80 ms, ciclo 1280 ms | 9 quadros, 1285 ms |

Cada composição: 256×256 RGBA, corpo nativo 128×128 em (64,64), PPU100, mesma escala. Fontes em characters/orc-v1/source/aseprite/equipment/, PNGs/folha/camadas/clip em source/equipment/<weapon>/<Walk|Attack>/. Ordem de camadas: weaponBack, body, weaponFront, handFront. Arquivos grip/corpo/camada e SHA256 por quadro. Referência de chão 190; futura integração precisa respeitar canvas/registro e testar pivôs, não importar como baseline128 sem ajuste.

Mão direita anatômica, esquerda livre. Sockets revisados no punho de cada pose. A caminhada reutiliza as 16 poses anteriores, com pele Verde Warcraft aplicada no Aseprite; nada foi espelhado. O novo Idle mantém as cinco fases fixas e ciclo2200ms.

## Procedência e decisões de produção

Armas originais autoradas por Lua dentro do Aseprite (tools/aseprite/orc-v1-weapons.lua), guiadas pelas duas fotos do criador e pela identidade do personagem. Não são desenho manual nem armas geradas pelo PixelLab. Corpo de ataque gerado pelo MCP PixelLab animate_image; conta Pro, sem seletor explícito de modelo nesta ferramenta. Duas chamadas, duas gerações cobradas cada: total4. Job de espada a810f375-afbc-40a8-be13-2dbc40a92d82 rejeitado por não mostrar corte claro. Job0f57f3ac-cabf-4fca-8884-b291cb7ba6e3 trouxe um corte melhor; pequena lâmina indevida gerada em dois quadros foi removida no Aseprite. Movimento corporal reaproveitado para ambas as armas, com arcos e durações específicos. Fonte bruta e pedidos em experiments/orc-v1-weapons-v1/.

Compósitos, rotação pixelada sem interpolação, máscaras da mão e exportações são todos executados no Aseprite. Ferramentas externas somente organizaram metadados/cópias, analisaram pixels e montaram previews. Layers/masters editáveis preservam a separação entre corpo e equipamento. Detalhes de design obrigatórios em docs/WEAPON_ART_STANDARD.md.

## Validação

Editor-export: quatro mestres, 50 quadros comparados, PASS; build dist/editor/orc-v1-weapons-v1/93f79e335f6bd1549c5c/. Conferência de layers e spritesheets:50 composições reconstruídas e iguais aos PNGs. Todos os grips sobre pixels visíveis da mão, armas visíveis em todos os quadros, nenhum pixel de arma cortado pelas bordas. Browser:55 quadros incluindo Idle, 272 arquivos copiados com SHA256, abertura local/mobile sem erros JavaScript. Originais:128 PNGs/mestres do pacote05 preservados. Evidência reports/orc-v1-weapons-v1/check.json. Validação técnica não concede aprovação artística.

## Limites e próximo passo

Apenas uma vista front_r/south-east foi produzida neste lote. Novas armas, composição, pegada e golpe aguardam avaliação do criador. A página repete Attack para comparar, mas Attack.loop=false no manifesto; contato visual candidato em frame5 não aplica dano. Dados de arma só visuais, sem stats novos. Não há quatro vistas, binding runtime, inventário ou novo renderer Unity implementados.

O pedido autoriza armas visíveis no Walk destas duas combinações, atualizando a regra histórica que as ocultava; o corpo base permanece independente. No pedido de integração futuro, tratar registro do Orc V1, profile256/pivôs, seleção de ação/equipamento, layers/oclusão/eventos, interrupções e outras vistas com evidência própria. Nenhum arquivo do projeto Unity foi alterado aqui.

## Reconstrução

1. Autoria da arma: tools/aseprite/orc-v1-weapons.lua no Aseprite batch isolado.
2. Base Walk verde: tools/aseprite/orc-v1-green-walk.lua.
3. Plano registrado: experiments/orc-v1-weapons-v1/composition-plan.json. Compor por tools/aseprite/compose-orc-v1-weapons.lua; exportar folhas por orc-v1-weapon-sheets.lua. Mudança de arte exige atualizar hashes dos clip/manifest e revisar encaixes.
4. Editor-export com experiments/orc-v1-weapons-v1/editor.json. Biblioteca por tools/build-orc-v1-weapons-review.py e tools/build-art-library.py.
5. QA: tools/check-orc-v1-weapons.py; não reexecutar aprovadores históricos V4.
