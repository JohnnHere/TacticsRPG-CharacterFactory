# Parecer de QA Independente — back_r / Axe — Chaves de Pegada Natural (F04 Apex & F07 Impact)

**Documento:** `experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/rear-axe-grip-keys-report.md`  
**JSON Estruturado:** `experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/rear-axe-grip-keys-result.json`  
**Revisor:** Gemini 3.8 Flash (QA Independente via Antigravity)  
**Data:** 29 de Outubro de 2026  
**Checkpoint Avaliado:** `REAR_AXE_GRIP_KEYS_READY`  
**Autor do Pacote:** `7db0e7b6` (DEV ESPECIALISTA PEGADA)  
**Status Técnico:** `TECHNICALLY_COMPLETE`  
**Veredito do Revisor:** **`READY_FOR_FULL_REAR_AXE_GRIP`**  
**Status Artístico Global:** `ARTISTIC_REVISION_REQUIRED` (Inalterado)  
**Aprovação do Criador:** `PENDING_CREATOR`  

---

## 1. Escopo Delimitado e Contexto Operacional

Este parecer de QA independente avalia com rigor técnico e inspeção multimodal direta a entrega de dois quadros representativos da pegada traseira de machado (`back_r/Axe`):
- **F04 (Apex / Carregamento Alto):** Índice 4, 110 ms, fase `validated-apex`.
- **F07 (Impact / Impacto no Solo):** Índice 7, 110 ms, fase `validated-impact`.

A entrega foi executada sobre o corpo base previamente aceito no QA anterior (`full-back-r-axe`, 12 quadros, 1100 ms, status `READY_FOR_REAR_GRIPS`).

Conforme as regras de governança vigentes:
- **Papel estrito de QA Independente:** O revisor não produz arte, não orquestra outros agentes, não executa chamadas pagas de PixelLab e não realiza escritas fora da pasta `qa-antigravity-flash/`.
- **Isolamento de escopo:** Os dois reparos corporais em andamento com outro especialista (`back_r/Sword` F06 e `back_l/Axe` F02) foram escalonados separadamente e não fazem parte deste exame.
- **Não aprovação prematura:** Este parecer valida exclusivamente a viabilidade anatômica e técnica dos dois quadros representativos para permitir a expansão completa no clipe `back_r/Axe`. Não constitui aprovação dos 12 quadros, dos outros 3 clipes traseiros, nem de integração Unity ou aprovação final pelo criador.

---

## 2. Metodologia de Auditoria Independente

A avaliação combinou três frentes independentes de verificação:
1. **Inspeção Multimodal Direta:** Leitura e visualização direta dos arquivos PNG (`composite-256.png`, camadas isoladas em 256×256 e recortes em 128×128, além dos painéis de evidência comparativa e de traçado anatômico).
2. **Auditoria Programática de Pixels e Hashes:** Scripts independentes em Node.js inspecionaram coordenadas de bounding box, valores exatos de RGBA das camadas, contatos com o solo e cálculo de SHA-256 para cada arquivo contra as declarações do manifesto.
3. **Auditoria de Proveniência e Scripts:** Verificação do script de autoria `author.lua`, confirmando execução em lote do Aseprite (`--batch --noinapp`) sob o perfil isolado `tmp/aseprite-rear-grip-flash-profile`, sem recurso a rotações externas por Pillow ou interpolações espúrias.

---

## 3. Rastreamento Anatômico e Cadeias Articulares

Diferente de tentativas geométricas anteriores que colidiam membros ou fundiam luvas com armadura, o rastreamento em ambos os quadros respeita a cadeia contínua ombro-cotovelo-punho e a separação funcional dos dois braços:

### 3.1 F04 — Apex (Carregamento Alto, 110 ms)
- **Braço Dominante de Ataque (Direito):**
  - **Ombro:** `[147, 102]` (nativo `[83, 38]`).
  - **Cotovelo:** `[163, 86]` (nativo `[99, 22]`) — projetado lateralmente para fora e para cima.
  - **Punho:** `[147, 77]` (nativo `[83, 13]`) — fletido sobre o topo do crânio occipital.
  - **Centro da Palma / Grip:** `[139, 72]` (nativo `[75, 8]`).
  - **Conexão Articular:** A transição entre o antebraço encouraçado e o punho fechado é perfeitamente contínua, sem degraus ou flutuação de carimbo.
- **Braço Estabilizador de Contrapeso (Esquerdo):**
  - Ombro `[102, 112]`, cotovelo `[92, 126]`, punho `[87, 140]`, punho fechado `[87, 147]`.
  - O punho esquerdo pende baixo ao lado do quadril, com silhueta desarmada 100% livre e limpa, eliminando qualquer ambiguidade de empunhadura bimanual.

### 3.2 F07 — Impact (Impacto no Solo, 110 ms)
- **Braço Dominante de Ataque (Direito):**
  - **Ombro:** `[147, 115]` (nativo `[83, 51]`) — rebaixado em 13 pixels em relação a F04, evidenciando compressão corporal e flexão do tronco para a frente (*body hinge*).
  - **Cotovelo:** `[160, 128]` (nativo `[96, 64]`) — liderando a descida do membro.
  - **Punho:** `[156, 141]` (nativo `[92, 77]`).
  - **Centro da Palma / Grip:** `[157, 146]` (nativo `[93, 82]`).
  - **Conexão Articular:** A luva marrom (`x=152..162, y=142..149`) conecta-se organicamente ao antebraço e à manga de cota de malha, sem fundir-se com a saia de placas ou tassets da coxa.
- **Braço de Contrapeso (Esquerdo):**
  - Ombro `[102, 116]`, cotovelo `[91, 129]`, punho `[87, 142]`, punho fechado `[86, 148]`.
  - Estabiliza o peso corporal para trás em arco oposto ao impacto.

---

## 4. Oclusão em Camadas e Aplicação do Método Sol

A montagem respeita a ordem canônica de 4 camadas: `weaponBack` → `body` → `weaponFront` → `handFront`.

1. **Envelope da Luva Genuína:**
   - Em F04 e F07, as linhas da luva foram extraídas diretamente do corpo base (`body`), preservando o contorno de couro marrom autêntico.
2. **Retouches Cirúrgicos Internos (Método Sol):**
   - Foram aplicados exatamente **6 pixels de retoque interno** por quadro (tons de realce quente, dobras articulares e sombras pertencentes à paleta da luva), fechando os dedos ao redor do cabo.
   - Todos os pixels de retoque estão estritamente contidos no interior da luva (`alpha == 255` no corpo original).
3. **Passagem do Cabo e Oclusão 3D:**
   - A seção de empunhadura do cabo de madeira/couro (`v=50..57` do sprite `militia-axe.png`) foi roteada para `weaponBack`.
   - Como `weaponBack` renderiza atrás do corpo e a frente da luva está em `handFront`, o cabo passa visualmente por dentro da mão fechada.
   - O prolongamento superior e a cabeça do machado projetam-se naturalmente em `weaponFront`, sem ocultação forçada de elementos estruturais.

---

## 5. Credibilidade Cinética e Espacial

### 5.1 Elevação Overhead em F04 (Apex)
- **Posicionamento da Cabeça do Machado:**
  - O topo da cabeça de ferro ocupa a caixa delimitadora `x=123..150, y=24..68` no canvas 256.
  - Como o topo do crânio do Orc está em `y ≈ 82`, a cabeça do machado está inteiramente suspensa no espaço negativo livre, com **0 pixels de colisão com a cabeça ou armadura**.
- **Orientação do Gume:**
  - A rotação de `330°` (`-30°` em relação à vertical) orienta a lâmina curva para a frente e para cima (+X, +Y), configurando uma pose de ápice dinâmica e agressiva no sentido do golpe descendente.

### 5.2 Descida e Contato com o Solo em F07 (Impact)
- **Alinhamento do Plano do Solo:**
  - A análise de pixels revelou que os pés do Orc estão cravados no solo em exatamente **`y = 190`** no canvas 256 (nativo **`y = 126`**).
  - O ponto inferior do gume cortante do machado atinge exatamente **`y = 190`** em `x = 177`.
  - O golpe não afunda no piso nem fica suspenso no ar; o machado morde com precisão milimétrica a mesma linha de apoio dos pés, sem distorcer o braço ou exigir translações artificiais.

---

## 6. Verificação de Hashes SHA-256 e Integridade de Dados

Todos os arquivos entregues foram verificados byte a byte no disco:

| Arquivo | Dimensões | Duração | SHA-256 Verificado em Disco | Status |
|---|---|---|---|---|
| `F04/composite-256.png` | 256×256 | 110 ms | `27cab6a671d6edd68113eee1e0b9f70872e2e563466df66ad5bed7367c065a95` | Validado |
| `F04/composite-native-128.png` | 128×128 | 110 ms | `e10e4e7beda70ef734af9787f90be4cfb6321a93f551a33652fd9e7cbbc5fae3` | Validado |
| `F04/body-128.png` | 128×128 | 110 ms | `4c2cf239eec6b5008f9171661513caf147e208489018abbf4c124302c7873df6` | Validado (0 delta RGBA) |
| `F04/layers/weaponBack.png` | 256×256 | - | `52cfbd29328e2528bc89210e491ab7c37aa70bc323be9bbdfa94282484b2d658` | Validado |
| `F04/layers/body.png` | 256×256 | - | `4ae7385519e3c7a1383f777e1e4ec2b0b8d54e9c49ecc71c6155725e2cdf0c86` | Validado (byte-idêntico ao corpo aceito) |
| `F04/layers/weaponFront.png` | 256×256 | - | `c9316e655a4e42220a07ce7eed8cbe20453df1100daec685668b0ddb008bfd60` | Validado |
| `F04/layers/handFront.png` | 256×256 | - | `2d7dd00c30a0103337c6a8c0b80f71e166a3346752c532c157f8757a34dc8bc7` | Validado |
| `F04/source/composite.aseprite` | 256×256 | 110 ms | `14108798da267653bd9b68d3613800ccace43921650c5b6fea848ecf4070753a` | Validado |
| `F07/composite-256.png` | 256×256 | 110 ms | `b9b17570db0d8759edf863ca7e48b14f289bc9ae0460bdf6e2235e4ee3d34b9f` | Validado |
| `F07/composite-native-128.png` | 128×128 | 110 ms | `7b68137872bb4e08a648ba34aa155cf061d93eb301c89df52f197c98e7e176cb` | Validado |
| `F07/body-128.png` | 128×128 | 110 ms | `608119efa4811fe6e9de48001199ea84a5405f171e30ee46911b584a7bd54693` | Validado (0 delta RGBA) |
| `F07/layers/weaponBack.png` | 256×256 | - | `b120e23052d443e74dd04bae29ba9dd637f9d0806c4551815f431336d19330e5` | Validado |
| `F07/layers/body.png` | 256×256 | - | `3bbb8feae4cb6be0b6bb814852eb784e5c1fbf9e3870fd360d94373945e31d99` | Validado (byte-idêntico ao corpo aceito) |
| `F07/layers/weaponFront.png` | 256×256 | - | `b75fd8dc6c56c6209c6d2805776e8f885b709911148d1d856093c49b6887ab46` | Validado |
| `F07/layers/handFront.png` | 256×256 | - | `75d89889b1857e05fba4a1f88b3fc056284e1289a396bedfb5c4658965e231a1` | Validado |
| `F07/source/composite.aseprite` | 256×256 | 110 ms | `d2a17c49054bbcb52516b7db6076d9527a674dbc7ee328b6e1352bd7c243fa49` | Validado |
| `source/composite.aseprite` (2f) | 256×256 | 220 ms | `f00de3eb8abff4df5464518c46e826b3387c95724a0c4b49b7b4cc34a68d08be` | Validado |

---

## 7. Notas Diagnósticas e Esclarecimentos Técnicos

1. **Discrepância Datilográfica na Tabela do Relatório do DEV:**
   - Na Tabela 5 do relatório do DEV (`experiments/main-orc-combat-rescue-v5/rear-grip-flash/report.md`), os hashes de `F04 Composite 256`, `F04 Native Composite 128` e `F07 Composite 256` apresentavam pequenas divergências nos caracteres intermediários em relação aos arquivos no disco (provável erro de colar/copiar durante a redação manual do markdown).
   - Os manifestos estruturados (`checkpoint.json`, `representative.json`, `representative-keys.json`) contêm os hashes exatos e verdadeiros calculados a partir dos arquivos físicos no disco. A conformidade técnica foi mantida.
2. **Recorte no Canvas Nativo 128×128 em F04:**
   - No arquivo diagnóstico `composite-native-128.png` de F04 (e no painel de evidência `F04-before-after.png`), a cabeça do machado aparece cortada na margem superior.
   - Isso ocorre porque o canvas nativo do corpo é de 128×128 centralizado em `[-64, -64]`. Como a lâmina em F04 sobe até `y = 24` no canvas tático 256, os primeiros 40 pixels caem fora da margem nativa de 128.
   - No canvas tático canônico de 256×256 (padrão de combate de todas as animações armadas da fábrica), o machado está 100% íntegro e visível.

---

## 8. Limitações Críticas da Avaliação

1. **Avaliação Estática de Poses Isoladas:**
   - Este exame comprova apenas que as duas poses extremas (ápice e impacto) são anatomicamente sustentáveis e visualmente verossímeis.
   - Os ângulos de `330°` e `120°` **não provam**, por si sós, uma trajetória fluida de golpe, aceleração contínua ou rotação suave ao longo do ciclo completo de 12 quadros.
2. **Ausência de Observação Contínua 1× em Motor/Navegador:**
   - Conforme exigido pela política de honestidade de QA, este parecer baseia-se na inspeção de quadros individuais estáticos e camadas PNG. A reprodução contínua em tempo real (1×) em navegador ou motor de jogo não foi observada diretamente nesta rodada.
3. **Escopo Restrito:**
   - Este veredito autoriza unicamente a passagem para a próxima fase técnica da pegada no clipe `back_r/Axe`. Não autoriza escrita em Unity, promoção para produção ou aprovação pelo criador.

---

## 9. Veredito Final e Próximos Passos

- **Veredito:** **`READY_FOR_FULL_REAR_AXE_GRIP`**
- **Recomendação ao Root / Orquestrador:**
  - O DEV especialista em pegada está autorizado a utilizar estas duas âncoras (`F04` e `F07`) como base para estender a amarração e a pegada natural do machado nos demais quadros intermediários do clipe `back_r/Axe` (12 quadros).
  - Nenhuma outra vista traseira ou arma deve ser propagada sem a conclusão desta etapa.
- **Contabilidade de Recursos:**
  - Chamadas PixelLab de produção nesta revisão: **0**
  - Custo de inferência LLM: **Não informado** (nenhum valor financeiro ou de tokens inventado).
  - Modificações em arte / Unity / Git: **Nenhuma**.