# PixelLab — o que realmente existe para animação guiada por esqueleto

Investigação feita **sem nenhuma geração**: apenas `tools/list` e `get_balance` no MCP oficial.
Chamada restrita executada pelo Orquestrador porque o MCP não é herdado pelos subagentes
(§4 do contrato de orquestração); nada de arte foi produzido nesse acesso.

Ferramenta encontrada: **`animate_with_skeleton_v3`** (marcada como *beta* pelo provedor).

## Disponibilidade

Sim, existe e está exposta no MCP. A descrição oficial é explícita sobre o propósito: animar um
sprite ao longo de um esqueleto **que você mesmo posa, um por quadro**, redesenhamdo cada quadro a
partir de uma única imagem de referência. É exatamente o modo de trabalho que este experimento
quer testar.

A própria descrição também diz quando **não** usar: para um personagem já armazenado no PixelLab,
`animate_character` com animação de template dá muito menos trabalho. E afirma que nenhum template
devolve keypoints para quem chama a API, ou seja, **não existe biblioteca de ciclos pronta para
buscar**. Ou você deriva o esqueleto do seu sprite, ou traz o seu próprio rig.

## Contrato de entrada

| Campo | Obrigatório | O que é |
|---|---|---|
| `description` | sim | Aparência como sintagma nominal. Cores, roupa, itens em mãos. **Não** é o movimento. |
| `action` | sim | Rótulo curto: `attack`, `walk`. |
| `direction` | sim | Uma de `south, north, east, west, south-east, south-west, north-east, north-west`. |
| `keypoints` | sim | O movimento: **um esqueleto por quadro devolvido**, de **3 a 15 quadros**. |
| `first_frame_keypoints` | sim | O esqueleto da pose em que a imagem de referência **já está**. |
| `view` | não | `low top-down` (padrão), `high top-down`, `side`. Precisa casar com o sprite. |
| `reference_image` e afins | — | A imagem de referência é o sprite atual; sem ela o modelo não tem identidade. |
| `no_background` | não | Padrão `true`, devolve com transparência. |
| `seed` | não | Reprodutibilidade. |
| `depth_preset` | não | `mannequin` para bípedes; `bear, cat, dog, horse, lion` para quadrúpedes. |

### O esqueleto é COCO-18, e isso importa

Cada quadro carrega exatamente estes 18 rótulos, todos obrigatórios:

`NOSE, NECK, RIGHT SHOULDER, RIGHT ELBOW, RIGHT ARM, LEFT SHOULDER, LEFT ELBOW, LEFT ARM,
RIGHT HIP, RIGHT KNEE, RIGHT LEG, LEFT HIP, LEFT KNEE, LEFT LEG, RIGHT EYE, LEFT EYE,
RIGHT EAR, LEFT EAR`

Consequências que mudam o planejamento:

- `x` e `y` são **frações de 0 a 1 da imagem**, origem no canto superior esquerdo, `y` para baixo.
- `ARM` é o **punho** e `LEG` é o **tornozelo**. Não existe junta de mão nem de pé separada.
- `LEFT`/`RIGHT` são os lados **do personagem**, não do observador. Facing `east`, os membros
  RIGHT são os próximos da câmera; espelhado para `west`.
- `z_index` é ordem de desenho, inteiro livre, sem valores prescritos por template.
- `depth` é opcional, 0–255, com ~128 no centro do corpo e valores maiores mais perto da câmera.
  Omitido, vem do corpo do template para aquela direção.

### A armadilha do `first_frame_keypoints`

A descrição avisa, com todas as letras, que um esqueleto que **não corresponde** à imagem de
referência "custa transparência e precisão de cor silenciosamente". Para obter esse esqueleto de um
sprite próprio existe `POST /v2/estimate-skeleton` — POST, não GET — que **não tem ferramenta MCP**,
mas usa a mesma credencial.

Ou seja: o caminho honesto tem duas chamadas, uma de estimativa e uma de animação, e nenhuma das
duas é gratuita.

## O que é devolvido

`get_image` devolve **exatamente** `len(keypoints)` imagens. O quadro de referência **não** é
devolvido junto: os quadros retornados são só os novos, na ordem enviada.

Limite de tamanho: o schema traz `{MAX_DIMENSION}` como marcador não resolvido na descrição, e o
valor concreto não é exposto ao chamador. Precisa ser descoberto em uso real, não por suposição.

## Custo, medido, não estimado

Preço é por tempo de geração, que quase não varia com o comprimento. A descrição fixa três degraus:

| Quadros | Generations |
|---|---|
| 3 | 2 |
| 4 a 14 | 3 |
| 15 | 4 |

Tempo de geração: ~3 a 6 minutos, assíncrono, com `get_image(job_id)` para acompanhar.

Saldo verificado nesta sessão, sem consumir nada:

- `generations_remaining`: **1259,70**
- `generations_used`: 740,30 de 2000
- `credits`: $0.00
- renovação do ciclo: 2026-11-23

A nota do próprio provedor explica que frações vêm de passos pequenos cobrados por uso:
prompt enhancement 0,05, **estimativa de esqueleto 0,1**, redução de cor 0,1, import de sprite 0,25.

## Limitações observadas, ditas sem enfeite

1. **Não é gratuito.** O mínimo possível, 3 quadros, custa 2 generations. Com 4 a 14 quadros custa 3.
   Para o nosso caso, 14 quadros custam 3 generations. A estimativa de esqueleto soma 0,1.
2. **Zero gerações autorizadas neste experimento.** Portanto a ferramenta foi verificada e
   **não foi chamada**. Nada aqui foi produzido por ela.
3. **Não devolve o esqueleto de templates.** Não há atalho: o rig tem de vir de nós.
4. **Beta.** O nome da ferramenta carrega `_v3` e a descrição diz beta; o contrato pode mudar.
5. **18 juntas fixas.** Não há junta de dedo, de mão, de pé nem de arma. Polegar, empunhadura e
   orientação de lâmina **não são representáveis** no esqueleto — ficam por conta de quem posa,
   e no nosso caso precisam viver em campos próprios do `poses.json`.
6. **`MAX_DIMENSION` não resolvido** no schema exposto.
7. **A imagem de referência define a identidade de todos os quadros.** Se a referência de `back_l`
   for um frame de Idle desarmado, todos os quadros sairão desarmados, porque a arma não está na
   imagem. Isso é relevante para a próxima etapa.

## Consequência para este experimento

O desenho do movimento continua sendo nosso. A ferramenta, quando autorizada, executa o que
posamos — ela não inventa coreografia convincente. É por isso que a etapa atual, que produz e
revisa as cinco poses antes de qualquer geração, tem valor independente do PixelLab.
