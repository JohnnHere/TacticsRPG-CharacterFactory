# Produção e integração

Leia o pipeline canônico para detalhes; confirme `UnitVisuals`/`UnitView` antes da integração. Baseline humanoide: PNG RGBA 128×128, altura útil ~100 px, chão y=126 com origem no topo, PPU100, Point, sem mipmaps/halo/compressão prejudicial, escala piloto 1,15. Canvas/altura/escala são referência validada do piloto, não limite universal.

Direções de tela: `front_r`, `front_l`, `back_r`, `back_l`; ordem das tabelas runtime `[back_l, back_r, front_r, front_l]`. Índice `RoundToInt((Repeat(unitYaw-cameraYaw,360)+45)/90)&3`. Preserve Facing ortogonal do Core e yaw real da câmera. Desenhe cada vista; não espelhe automaticamente.

Pasta final autorizada: `Assets/Resources/Characters/<CharacterId>/`. Fallback `<prefix>_mvp1_static_128.png`; direções `Directions/<prefix>_dir_<direction>.png`; animações `Animations/<State>/<state>_<direction>_<NN>.png`. Clipes usam apenas estado como prefixo. O runtime atual conhece somente WarriorPilot; caminhos novos são plano, não registro implementado.

| Estado | Frames/vista piloto | Avanço |
|---|---:|---|
| Idle | 4 | 0,24 s/frame, loop |
| Walk | 6 | 3/tile, `stepT`, ciclo de 2 tiles |
| Attack | 5 | 0,09 s/frame, override expira |
| Hit | 3 | 0,08 s/frame, golpe que acerta |
| Defeat | 5 | 0,12 s/frame, override não expira; ressalva de módulo no código |

Total 92 animados + 4 direcionais + fallback. Carregador aceita sequências 1–16 por direção, iniciadas em 00 sem lacunas. Variações precisam documentar contagem e timing; Walk permanece 3 frames/tile no código, portanto alterar contagem altera o ciclo, não parametriza automaticamente gait. Novos estados exigem integração.

Ordem: validar base estática -> quatro vistas/fallback -> Idle front_r -> Walk front_r -> outras vistas Idle -> outras vistas Walk -> Attack/Hit/Defeat front_r -> outras vistas combate. Antes de expansão, revisar base; aprovar lotes, não cada frame. Inspeção em jogo de estáticos segue autorização explícita de integração mesmo quando recomendada antes de animações.

Equipamento: registre `embedded` ou `separate`. Corpo sem arma permanente é meta de produção; layers/rig/sockets não existem. Embutir arma é exceção consciente com custo de redesenho de clipes + separar assets + registro/encaixes futuros. Não implemente arquitetura antecipadamente.

Import: `textureType:8`, `spriteMode:1`, `spritePixelsToUnits:100`, `filterMode:0`, `enableMipMap:0`, `alphaIsTransparency:1`. Compressão None no bloco **DefaultTexturePlatform**; não confundir com Standalone/WebGL históricos. Preserve GUID ao corrigir meta existente; não clone GUID. Mudanças de assets/metas exigem autorização para integração.

Plano PREPARE_INTEGRATION deve listar arquivos, perfil, naming, validação, seleção da unidade e extensão mínima do registro, riscos e rollback. Mostre escopo antes de pedir autorização de extensão. Sem Core novo, sem Animator. INTEGRATE executa somente o autorizado, compila/testa e prepara revisão manual.

PlayMode: quatro vistas e giros Q/E, Idle/Walk, trajetória multi-tile sem reinício por tile, zoom-out, chão/desníveis, ataque inclusive vazio, Hit em acerto, derrota, transições, fallback, sombra sem magenta, marcador branco desligado, demais unidades preservadas e undo/snapshots internos conforme política atual. Não restabeleça save livre. Gate 3 permanece humano.
