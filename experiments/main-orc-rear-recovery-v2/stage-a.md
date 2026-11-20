# Stage A — Baseline e diagnóstico (checkpoint pendente)

**Revisão:** `main-orc-rear-recovery-v2` — ator Orc V1 / Verde Warcraft — baseline `complete-v1` build `b178422e1f7fc19f068c`.
**Escopo:** somente diagnóstico + proteção. Nenhuma edição de arte, candidato, master, builder ou docs. Nenhuma chamada paga.

---

## 1. Capacidade do ambiente (confirmada)

| Ferramenta | Status | Evidência |
|---|---|---|
| Aseprite 1.3.18.6-x64 | AVAILABLE, batch `--noinapp`, `windowsHide: true`, `cloudCalls: none` | `node src/cli.mjs editor-check` |
| Node | v24.20.0, sem erros de referência | `node src/cli.mjs doctor` |
| PixelLab MCP client (oficial) | Autenticado (`initialize` HTTP 200, servidor PixelLab MCP Server 0.2.0), catálogo em `tmp/rear-recovery-tools.json` | documentação `docs/PIXELLAB_MCP.md` + `tools/pixellab-mcp.py --list` |
| Python direto | Referenciado nos contratos (`.../codex-primary-runtime/dependencies/python/python.exe`, `tmp/pixel-venv/Scripts/python.exe`) | citado em `art-task.txt` / `contract-task.txt`; não reexecutado |

**Aseprite e PixelLab estão confirmados para uso posterior, sob autorização do root. Nenhuma geração paga neste checkpoint.**

---

## 2. Preservação (snapshot antes de qualquer edição)

Arquivo: `experiments/main-orc-rear-recovery-v2/preservation-snapshot.json`

- `characters/orc-v1/source/complete-v1` — 715 arquivos (masters `.aseprite`, PNGs, metadados)
- `dist/editor/orc-v1-complete-v1/b178422e1f7fc19f068c` — 903 arquivos (build, hashes, manifest, preview)

Cada arquivo registrado com SHA-256 e tamanho. Este snapshot é a referência de não-regressão para clips protegidos (front Idle/Walk/Sword/Axe, rear static bases, rear Defeat válido, armas, `equipment-current.json`).

---

## 3. Diagnóstico — causas confirmadas vs hipóteses

Fonte de evidência: `diagnosis/{index,metrics,layers,grip,grids-index}.json` + grids/komparativos já exportados. Não houve re-audita de imagem.

### Confirmed mechanisms (Lua/composite/ camadas)

**Rear Walk (`back_r` / `back_l`, 16 quadros):**
- `bob_px = 5`, `sway_px` ~1.1–1.5, `cx_range` estreito (~126–129 px): pouca variação de centro de massa.
- Evidência visual (root): pernas e braços externos são **forms frontais** colocados sob o torso traseiro bom; joelhos/caldos/quadril não lêem como marcha de costas.
- Causa confirmada: graft de partes frontais (canela/pé com contorno frontal) sob base traseira. A geometria traseira está boa; a montagem do membro inferior é incompatível com a perspectiva de costas.

**Rear Sword Attack (`back_r` / `back_l`, 13 quadros, 730 ms):**
- `bob_px = 44–45` (excursão vertical), `top_range` 32–77, `sway_px` ~16.
- `rightGrip` salta de x≈154–167 (lado direito) para x≈97–98 (lado esquerdo) entre quadros: grip descontinuado lateralmente.
- `rotationDeg` transita 45→30→20→15→340→305→260→258→255. Note-se que 45°→340° representa uma rotação modular mais curta de -65° (delta angular de 65° em sentido anti-horário), e não um giro errático de 295°; contudo, a trajetória da lâmina e a oclusão relativa ao braço e torso carecem de suporte anatômico na vista traseira.
- `weaponBack` vazio nos quadros 2–5 (arma só em `weaponFront`), depois passa a `weaponBack` nos quadros 5–9: transição brusca de profundidade de camada da arma sem arco correspondente do antebraço e torso traseiro.
- Causa confirmada: camadas de arma/braço reutilizam arcos derivados da frente com inversão de profundidade, enquanto a pose e a anatomia escapular traseira não sustentam a mesma coreografia.

**Rear Axe Attack (`back_r` / `back_l`, 12 quadros):**
- `bob_px = 21–22`, `armReachRatio` = 6.37–8.64 no quadro 5 (alcance do braço quebrado, mão excessivamente distante da caixa torácica).
- `weaponFront` vazio após quadro 4; grip também salta lateralmente.
- Causa confirmada: mesma descontinuidade anatômica e de camada observada na espada, com trajeto de golpe de machado sem leitura de peso e alavanca traseira.

**Rear Unarmed Attack (`back_r` / `back_l`, 5 quadros):**
- `cx_range` oscila 121–133 px (`sway_px` 5.86–6.67), `opaque_range` cai para ~4646–5927: corpo desbalanceado sem leitura clara de soco ou cotovelada.
- Causa confirmada: poses emprestadas e mescladas de ataques armados incompatíveis; ausência de antecipação e impacto em vista traseira.

**Front Defeat (`front_r` / `front_l`, 5 quadros):**
- Análise visual das pranchas exportadas: nos estágios 0..3 a queda é plausível, mas o quadro final 4 permanece com o tronco ereto sobre os joelhos, suportado e consciente ("kneeling-supported"), divergindo semanticamente do Rear Defeat (onde o Orc colapsa totalmente no chão). Contagens de centroide e área isoladas não revelam essa postura; a inspeção da prancha confirma que o término frontal lê como posição de guarda/ajoelhado em vez de incapacitação terminal.
- Rear Defeat (`back_r` / `back_l`): termina em altura 66–67 px, claramente colapsado no chão — **bom, preservar**.

**Front Hit (`front_r`, 5 quadros):**
- `bob_px = 12`, `top_range` 71–83: reação melhorada, mas possivelmente exagerada/rápida em velocidade normal. A ser avaliado em 1×/0,75×/0,5× pelo root; não reconstruir automaticamente.

**Preservados (byte-iguais / não alterar):** front Idle/Walk, front Sword/Axe, rear static bases, rear Defeat terminal, armas independentes, visibilidade attack-only, `equipment-current.json`.

---

## 4. Hipóteses (não confirmadas, não base para edição)

- Que PixelLab seja a "causa raiz" dos defeitos de rear: não comprovado; os mecanismos de camada/grip acima explicam os sintomas sem culpar gerador.
- Que rear Walk possa ser corrigido só movendo o sprite inteiro para cima/baixo: rejeitado pelo contrato (não é locomoção).
- Que rear weapon attacks sejam corrigíveis apenas mudando metadados de visibilidade: insuficiente; exige reposição de braço/torso.

---

## 5. Preservação obrigatória (contrato)

Não tocar: `front_r/front_l Idle`, `front_r/front_l Walk`, `front_r/front_l Sword`, `front_r/front_l Axe`, rear static bases, rear Defeat válido, armas, `equipment-current.json`. Nenhum rebuild de 28 clips. Nenhum espelhamento de front como rear. Nenhum achatamento global/rotação 2D do Defeat. Nenhuma aprovação artística.

---

## 6. Próximo passo (pendente de root)

Checkpoint concluído. Root revisa `stage-a.md`, `reuse-assessment.json` e `call-proposal.json`; então autoriza (ou não) a primeira geração/pais de chave de rearWalk. Produção artística subsequente fica a cargo do orquestrador; este agente não inicia produção, não edita fontes e não gera novos agentes.
