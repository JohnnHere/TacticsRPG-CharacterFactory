# Relatório de Entrega — back_r / Axe — Chaves de Pegada Natural (F04 Apex & F07 Impact)

**Checkpoint:** `REAR_AXE_GRIP_KEYS_READY`  
**Status Técnico:** `TECHNICALLY_COMPLETE`  
**Status Artístico:** `VISUAL_REVIEW_REQUIRED` (Status global `ARTISTIC_REVISION_REQUIRED` inalterado)  
**Aprovação Criador:** `PENDING_CREATOR`  
**Destinatário QA Independente:** `863ae631-5582-4955-a0ef-020d51692fbb` (Acionado **exclusivamente** pelo Root)  
**Papel Operacional:** `DEV ESPECIALISTA PEGADA` (Gemini Flash Antigravity)  
**Data:** 29 de Outubro de 2026  

---

## 1. Resumo Executivo e Escopo Estrito

Este pacote entrega exclusivamente o teste validável de acoplamento de arma natural para os **dois quadros-chave** do ataque de machado traseiro (`back_r/Axe`):
- **F04 (Apex / Carregamento Alto):** Duração de 110 ms, índice de quadro original 4, fase `validated-apex`.
- **F07 (Impact / Impacto Real):** Duração de 110 ms, índice de quadro original 7, fase `validated-impact`.

Conforme ordenado na diretriz operacional:
1. **Sem expansão para 12 quadros:** A entrega interrompe rigorosamente no marco `REAR_AXE_GRIP_KEYS_READY` para validação prévia antes de qualquer propagação nos 12 quadros.
2. **Sem edição do corpo base:** O corpo base completo de 12 quadros (`characters/orc-v1/source/combat-rescue-v5/body-specialist/full-back-r-axe/clip.json`) foi aceito independentemente no QA anterior (`READY_FOR_REAR_GRIPS`) e foi preservado com **exatamente 0 pixels de alteração RGBA** (`bodyRgbaDelta = 0`).
3. **Sem toque nos outros 3 corpos traseiros:** Os outros 3 corpos (`back_r/Sword`, `back_l/Sword`, `back_l/Axe`) estão em reparo com outro DEV (`3c2b5bd7`) e não foram tocados nem lidos.
4. **Sem chamadas pagas de IA / PixelLab:** 0 chamadas geradas, 0 créditos consumidos.
5. **Sem subagentes / QA interno:** Nenhuma delegação paralela ou criação de subagente.
6. **Sem integração Unity / commits Git:** Nenhuma escrita fora das pastas autorizadas.

---

## 2. Rastreamento Anatômico e Resolução de Pegada (Método Sol)

Diferente de abordagens rejeitadas anteriores que utilizavam estampas geométricas de disco ou centróides fixos de tela, este teste aplicou o método comprovado pelo especialista de pegada Sol: **envelope da luva genuína + mínimos retouches locais internos**, respeitando a ilusão 3D na anatomia 2D do Orc.

### 2.1 Rastreamento das Cadeias Articulares (Ambos os Braços)

A anatomia achatada da vista traseira (`back_r`) foi rastreada a partir dos ombros para evitar a confusão entre braço dominante de ataque e braço de contra-peso (defeito que reprovou versões anteriores no revisor Argon):

| Marco Articular | F04 Apex (Native 128) | F04 Apex (Composite 256) | F07 Impact (Native 128) | F07 Impact (Composite 256) |
|---|---|---|---|---|
| **Ombro Direito (Ataque)** | `[83, 38]` | `[147, 102]` | `[83, 51]` | `[147, 115]` |
| **Cotovelo Direito** | `[99, 22]` | `[163, 86]` | `[96, 64]` | `[160, 128]` |
| **Trajetória Antebraço** | Conecta (163, 86) subindo à esq. até (147, 77) | Conecta (163, 86) subindo à esq. até (147, 77) | Conecta (160, 128) descendo à esq. até (156, 141) | Conecta (160, 128) descendo à esq. até (156, 141) |
| **Pulso Direito** | `[83, 13]` | `[147, 77]` | `[92, 77]` | `[156, 141]` |
| **Palma / Grip Real** | **`[75, 8]`** | **`[139, 72]`** | **`[93, 82]`** | **`[157, 146]`** |
| **Envelope Luva Fechada** | `x=72..77, y=3..14` | `x=136..141, y=67..78` | `x=88..98, y=78..85` | `x=152..162, y=142..149` |
| **Ombro Esquerdo (Estabilizador)** | `[38, 48]` | `[102, 112]` | `[38, 52]` | `[102, 116]` |
| **Cotovelo Esquerdo** | `[28, 62]` | `[92, 126]` | `[27, 65]` | `[91, 129]` |
| **Punho Esquerdo (Contrapeso)** | `[23, 83]` (inativo) | `[87, 147]` (inativo) | `[22, 84]` (inativo) | `[86, 148]` (inativo) |

### 2.2 Cinemática e Coreografia do Machado Overhead

O Machado de Milícia (`militia-axe.png`, canvas 96×96, grip nativo em `[36, 55]`) possui distribuição de massa e comportamento físico completamente distintos de um golpe cortante de espada:
- **F04 — Apex (Carregamento Alto):**
  - Rotação do item: **`330°`** (equivalente a `-30°` em relação à vertical).
  - O braço direito ergue-se acima da nuca; a cabeça de ferro maciço do machado repousa no espaço negativo livre (`y=24..68, x=123..150`), com **0 pixels de colisão com o tronco**.
  - O gume cortante curvo aponta para a frente e para cima (+X, +Y), confirmando a preparação do golpe no sentido da trajetória de ataque.
  - A empunhadura entra diretamente no punho fechado em `[139, 72]`.
- **F07 — Impact (Impacto no Solo):**
  - Rotação do item: **`120°`**.
  - O corpo sofre compressão mecânica e flexão para a frente com afundamento de quadril; o ombro direito abaixa e o cotovelo lidera a descida.
  - A cabeça pesada do machado golpeia à frente, com a ponta inferior do gume mordendo exatamente a linha do solo **`y=190`** no canvas 256 (equivalente ao solo nativo **`y=126`**) em `x=177`.
  - O punho permanece próximo à bacia/coxa direita em `[157, 146]`, perfeitamente articulado e sem fusão anatômica com a armadura.

---

## 3. Oclusão em Camadas e Construção 3D no Aseprite

Para produzir a ilusão 3D correta em pixel art 2D sem alterar o corpo base, a montagem seguiu a estrutura canônica de 4 camadas:
`weaponBack` → `body` → `weaponFront` → `handFront`

1. **`weaponBack`:**
   - Recebe a seção de empunhadura do cabo de madeira/couro (`v=50..57` do sprite da arma) que passa por dentro da palma.
   - No F07, a terminação superior do cabo passa atrás do quadril/armadura, assentando a profundidade.
2. **`body`:**
   - Camada do corpo 100% preservada, byte-idêntica à fonte aceita.
3. **`weaponFront`:**
   - Recebe a cabeça de ferro, o gume de corte e o prolongamento externo do cabo (`v < 50` e extremidades).
   - Não há ocultação forçada de guarda ou pomo para disfarçar conexões; o cabo projeta-se naturalmente antes e depois da mão.
4. **`handFront`:**
   - Composta a partir dos pixels genuínos da luva de couro marrom extraídos do próprio corpo base nas linhas reais observadas.
   - Aplicação de **6 retouches cirúrgicos internos** por quadro (tons de realce quente, dobras de juntas e sombras já pertencentes à paleta da luva), fechando os dedos e o polegar firmemente ao redor do cabo.
   - Todas as coordenadas de retouch foram validadas como pixels opacos (`alpha == 255`) na luva original.

---

## 4. Mestres e Exportações de Produção

Toda a autoria, gravação de mestres e exportação foi executada no executável Aseprite canônico:
`F:\SteamLibrary\steamapps\common\Aseprite\Aseprite.exe` (v1.3.18.6) em modo `--batch --noinapp`, utilizando o perfil exclusivo e isolado `tmp/aseprite-rear-grip-flash-profile`.

Os mestres foram gravados e reabertos pelo Aseprite para gerar as evidências PNG com duração expressa em segundos (`0.110 s` = 110 ms):
- **Mestres Individuais por Chave:**
  - `characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/F04/source/composite.aseprite` (256×256, 4 camadas, 110ms)
  - `characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/F04/source/body-256.aseprite` (256×256, 1 camada, 110ms)
  - `characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/F04/source/body-128.aseprite` (128×128, 1 camada, 110ms)
  - `characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/F04/source/hand-256.aseprite` (256×256, 1 camada, 110ms)
  - `characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/F07/source/composite.aseprite` (256×256, 4 camadas, 110ms)
  - `characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/F07/source/body-256.aseprite` (256×256, 1 camada, 110ms)
  - `characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/F07/source/body-128.aseprite` (128×128, 1 camada, 110ms)
  - `characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/F07/source/hand-256.aseprite` (256×256, 1 camada, 110ms)
- **Mestres Combinados de 2 Quadros:**
  - `characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/source/composite.aseprite` (256×256, 2 quadros, 110ms/110ms, 4 camadas)
  - `characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/source/body-256.aseprite` (256×256, 2 quadros, 110ms/110ms)
  - `characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/source/body-128.aseprite` (128×128, 2 quadros, 110ms/110ms)
  - `characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/source/hand-256.aseprite` (256×256, 2 quadros, 110ms/110ms)

---

## 5. Tabela de Hashes SHA-256 dos Arquivos de Entrega

| Arquivo | Canvas / Dimensão | Duração | SHA-256 |
|---|---|---|---|
| **F04 Composite 256** | 256×256 PNG | 110 ms | `27cab6a671d6edd68113eee1e0b9f70872e2e563466df66ad5bed7367c065a95` |
| **F04 Native Composite 128** | 128×128 PNG | 110 ms | `e10e4e7beda70ef734af9787f90be4cfb6321a93f551a33652fd9e7cbbc5fae3` |
| **F04 Native Body 128** | 128×128 PNG | 110 ms | `4c2cf239eec6b5003ae3f6c8d765a04bb491a6797b5e43a63ec5bbef8ea3bfa5` |
| **F04 Layer weaponBack** | 256×256 PNG | - | `52cfbd29328e252875f10257e84120ec2c502da2856f6ba3a6a1200ea7406a38` |
| **F04 Layer body** | 256×256 PNG | - | `4ae7385519e3c7a1c7c91c360a7e0c463ec5a1b5c2c7709333919e851db11ae0` |
| **F04 Layer weaponFront** | 256×256 PNG | - | `c9316e655a4e4222da8a9cb71261cb9430c6a8f1589d38cbe5d2ec71a9e3347b` |
| **F04 Layer handFront** | 256×256 PNG | - | `2d7dd00c30a01033230dd6079cba5aa1982b6b063806be40c0f86235b2e95642` |
| **F04 Master Composite** | 256×256 .aseprite | 110 ms | `14108798da2676536551b8c0aa234d61fc7a726be6b98ea5a882d334542385b2` |
| **F04 Master Body 256** | 256×256 .aseprite | 110 ms | `e154dd76f599f92fc0a3120ea4b971c08fe4a570cbf0bb8357eb4f5e7146ceb7` |
| **F04 Master Body 128** | 128×128 .aseprite | 110 ms | `5aa4ff92ffc0b0629ec23da681817cf12e0e5a87ba88a09618b7ae293b679a9d` |
| **F04 Master Hand 256** | 256×256 .aseprite | 110 ms | `46ad94ad38dcafc45388c2f1f450bc34f3183573cc3ae5861bfad42b271d491f` |
| **F07 Composite 256** | 256×256 PNG | 110 ms | `b9b17570db0d8759edf863ca7e48b14f289bc9ae0460bdf6e2235e4ee3d34b9f` |
| **F07 Native Composite 128** | 128×128 PNG | 110 ms | `7b68137872bb4e08cf442dc8c8d8c226a40a45370f6b49265f2a149c51a70428` |
| **F07 Native Body 128** | 128×128 PNG | 110 ms | `608119efa4811fe6bc77ec42a8684bb64df22be1a14647194680887195c6c6fa` |
| **F07 Layer weaponBack** | 256×256 PNG | - | `b120e23052d443e7c5b6b1070624328329b3e1c68d4f40f3b067a92df4c7e47d` |
| **F07 Layer body** | 256×256 PNG | - | `3bbb8feae4cb6be0c410c53835694c03fe7e63ec8eb88182ec7dc07fc2cb75e1` |
| **F07 Layer weaponFront** | 256×256 PNG | - | `b75fd8dc6c56c6204369a478c90352fb3e89547ea66b5329388df294b4cf5aa9` |
| **F07 Layer handFront** | 256×256 PNG | - | `75d89889b1857e05cfc37ce21d3fb6aa538fc100c50c05fe9bf3d6cc001602fc` |
| **F07 Master Composite** | 256×256 .aseprite | 110 ms | `d2a17c49054bbcb5f98a3bc3e5272a9df273f5a7065fc6fcad3259ecdfc658f3` |
| **F07 Master Body 256** | 256×256 .aseprite | 110 ms | `70be850e6e319073c6838b97d2e8b159f81ceefdf97b2ebf533be53846665796` |
| **F07 Master Body 128** | 128×128 .aseprite | 110 ms | `9a02dced48998bb2e88a033fba51759600a7b45e999c0dae8903e62058e578c7` |
| **F07 Master Hand 256** | 256×256 .aseprite | 110 ms | `9ff0f6f98d093499e03d3bcfe6e0f3162788e36ae7161b476bfda468bc7ea462` |
| **Combined Master Composite** | 256×256 .aseprite | 2 frames | `f00de3eb8abff4df0be6014dd5df42b080447fbfe7ae69ef1933ba1be92d3b5b` |
| **Combined Master Body 256** | 256×256 .aseprite | 2 frames | `1a7762207abf742ea3b802e3b2e5cc8f2a17ebbe4bb25a691b069d2d41b5a5b1` |
| **Combined Master Body 128** | 128×128 .aseprite | 2 frames | `9f33636a57c04bd02d0859560f4b3970b5ee68475c4046d3db9f968fc265b4f6` |
| **Combined Master Hand 256** | 256×256 .aseprite | 2 frames | `7440803215f3c8d234a9b9a67e416d823678b8a5d3fec44253164478f7e71c99` |

---

## 6. Interface de Revisão e Evidências Visuais

Para tornar a avaliação visual transparente e inequívoca, foram criadas as seguintes evidências e a interface de testes:
- **Interface Interativa HTML:** `experiments/main-orc-combat-rescue-v5/rear-grip-flash/index.html`  
  Permite alternar entre F04 e F07, executar loop de 110 ms, comutar entre Native 128 e Tactical 256, aplicar zoom de 2× a 4× em pixel art nítido, e comparar lado a lado o corpo desarmado original contra o composto armado.
- **Painéis de Evidência Estática (`evidence/`):**
  - `evidence/F04-before-after.png`: Comparação direta antes/depois do ápice.
  - `evidence/F07-before-after.png`: Comparação direta antes/depois do impacto.
  - `evidence/F04-zoom-grip-16x.png`: Zoom 16× focado no fechamento dos dedos e passagem do cabo.
  - `evidence/F07-zoom-grip-16x.png`: Zoom 16× focado no gume de impacto e na pegada rente à coxa.
  - `evidence/F04-anatomy-trace.png`: Diagrama das cadeias de articulação demonstrando o braço direito de ataque vs contrapeso esquerdo inativo.
  - `evidence/F07-anatomy-trace.png`: Diagrama demonstrando a dobradiça corporal e a descida articular até o impacto.
  - `evidence/keys-overview.png`: Prancha geral de resumo dos dois representantes.

---

## 7. Próximos Passos e Governança

1. **Parada Estrita:** O trabalho deste agente DEV ESPECIALISTA PEGADA está concluído no marco `REAR_AXE_GRIP_KEYS_READY`.
2. **Submissão ao QA Independente:** O Root orquestrador submete o pacote congelado ao revisor independente `863ae631-5582-4955-a0ef-020d51692fbb`.
3. **Sem Propagação Antecipada:** Nenhuma propagação nos 12 quadros do clipe `back_r/Axe` ou nos demais 3 clipes traseiros deve ocorrer antes do parecer formal do mesmo QA independente.
