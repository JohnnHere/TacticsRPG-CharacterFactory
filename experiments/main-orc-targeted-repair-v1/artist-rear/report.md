# Orc V1 · ataques traseiros · reparo local v1 — checkpoint

`main-orc-targeted-repair-v1/artist-rear` · 2026-10-27 · status do pool: **`ARTISTIC_REVISION_REQUIRED`** · aprovação artística: **`PENDING_CREATOR`**
`runtimeImplemented: false` · nenhuma escrita em `../TacticsRPG` · nenhum commit.

Escopo: apenas os quatro ataques traseiros (`back_r`/`back_l` × `Sword`/`Axe`), em candidato isolado. Manifesto canônico, config, docs compartilhados e Unity não foram tocados.

---

## 1. Resultado em uma frase

Não houve promoção. O primeiro representante isolado (`back_r`/`Sword`) foi diagnosticado e a tentativa de reparo foi **rejeitada por auditoria semântica**; um segundo artefato (`back_r`/`Axe`) foi editado em 11 pixels e fica como **hipótese não integrada**, porque nenhum dos 11 px foi provado defeito.

| item | estado |
| --- | --- |
| `back_r`/`Sword` · expansão de `handFront` (110 px) | **REJEITADA** — `audit-expansion-bands.txt` |
| `back_r`/`Axe` · micro-limpeza (11 px) | **HIPÓTESE NÃO INTEGRADA** — risco documentado na seção 4 |
| Comparador de revisão | corrigido (bug de canvas vazio) e verificado como descrito na seção 6 |
| Gerações PixelLab / custo externo | **0 / 0** |

---

## 2. Causas confirmadas

1. **Rebordo pálido sistêmico no corpo traseiro gerado.** O cinza `(122,123,125)` e sua rampa já existem nos quadros brutos do PixelLab; a Idle traseira protegida tem ≈0%. Não é sujeira de composição, é linguagem do gerador.
2. **Duas linguagens de contorno no mesmo clipe.** F00/F07 (guarda) usam contorno ink; F01–F06 usam o rebordo pálido.
3. **Arma composta por cima do punho.** `handFront` era apenas uma caixa de interseção de ±5 px; 35 px (`back_r`/`Sword`), 47 px (`back_l`/`Sword`), 143 px (`back_r`/`Axe`), 115 px (`back_l`/`Axe`) de cabo/arma são pintados sobre a mão em 6 quadros cada.
4. **Pomo enterrado no punho.** A âncora da arma está no meio da empunhadura, mas o punho é tão alto quanto empunhadura + pomo; o pomo cai dentro da silhueta da mão.

Hipóteses testadas e **derrubadas**: “âncora de pegada no contorno” (todas as pegadas estão dentro da palma, ocupação 5×5 opaca; âncora `[48,66]` coincide com o meio real da empunhadura, y 60–70) e “reparo por máscara resolve a pegada” (ver seção 3).

---

## 3. `back_r`/`Sword` — experimento rejeitado (evidência preservada)

Escolha do reparo: crescer `handFront` por BFS a partir do patch existente, só sobre pixels de `body` cobertos por `weaponBack`/`weaponFront`, até 7 px Chebyshev da pegada, copiando cor do `body`. Resultado: 110 px em 6 quadros (21/17/21/18/14/19), apenas a camada `handFront` alterada.

**Por que foi rejeitado.** A transformação inversa da arma foi calibrada (âncora confirmada `48,66`, concordância de cor 66,4% — o resto é `handFront` por cima) e cada pixel alterado foi mapeado para o espaço do sprite da espada:

```
f1 (325°)  guard 14 · grip 5 · pommel 1     (inverseValidated 20/20)
f4 (60°)   pommel 18                        (5/18)
f5 (100°)  pommel 14                        (2/14)
f6 (135°)  pommel 17 · grip 2               (19/19)
TOTAL      guard 14 · grip 7 · pommel 50
```

Os pixels “restaurados” escondem **pomo (50) e guarda (14)**, exatamente os elementos que fazem uma pegada ser legível. A expansão não é “punho em volta do cabo”; é “luva cobrindo pomo e guarda”. Máscara não corrige pegada: o defeito é de **posicionamento** da arma. Fica registrado em `candidate/clip/back_r/Sword/Attack-representative-v2-occlusion-v1/clip.json` com `status: REJECTED_BY_SEMANTIC_AUDIT`.

---

## 4. `back_r`/`Axe` — 11 pixels, hipótese **não** provada

Coordenadas e cores medidas sobre o freeze publicado:

| caso | pixel (composto) | nativo | cor | contexto medido |
| --- | --- | --- | --- | --- |
| A | 8 px em `y=191`, `x=110..117`, frame 1 | `y=127` | `(122,123,125)` uniforme | a linha `y=190` logo acima é **contorno ink** `(2,2,3)`/`(7,7,10)`; `y=192` é vazio |
| B | `(144,64)` e `(145,64)`, frame 2 | `(80,0)`,`(81,0)` | `(33,34,40)`,`(24,24,30)` | primeira linha do recorte nativo, sem vizinhos em nenhuma direção |
| C | `(171,151)`, frame 6 | `(107,87)` | `(24,24,30)` | a 2 px de um aglomerado escuro real em `(168,152)-(169,154)` |

**Riscos documentados (motivo de não integrar):**

- **A** é o **rebordo claro da sola projetando 1 px abaixo do contorno**, não sujeira: remover encurta a silhueta em 1 px e deixa o contorno ink como borda inferior. Pior: é o **mesmo** defeito sistêmico de rebordo pálido que este pool decidiu não tocar nos outros quadros — removê-lo aqui seria inconsistente.
- **B** pode ser **fragmento de membro ou de arma cortado pelo recorte nativo 128**, não sujeira independente.
- **C** pode ser **fleco intencional** do aglomerado escuro vizinho.
- **Conectividade 8 e limiar de cor são medidas geométricas; não decidem intenção artística.** Nenhum dos três casos tem prova de ser artefato.

Artefatos permanecem no disco como evidência (mestres, export, `clip.json` com `status: HYPOTHESIS_NOT_INTEGRATED`, riscos listados no campo `targetedRepair.risks`). Nada foi promovido.

---

## 5. Cambiantes preservados

Mestres forkados e verificados por hash antes de qualquer edição; nenhuma camada além de `body` foi tocada no caso A/B/C, e apenas `handFront` no caso Sword. Export: `44` arquivos byte-idênticos ao freeze no `Axe`, `49` no `Sword`; `0` arquivos removidos. `body-only`, `native`, strips, `weaponBack`/`body`/`weaponFront` byte-idênticos; tempos intactos (`8 f / [90,80,90,80,100,80,100,110] = 730 ms`). `weaponFront`/`weaponBack` em zero quadros alterados.

Hashes: `candidate/hashes.json`.

---

## 6. Correções e verificações do comparador

`candidate/comparator.html` (abre por `file://` ou servidor local; URLs relativas à própria página).

**Bug corrigido** (reproduzido no navegador integrado): a abertura por `file://` mostrava 48/48 recursos e canvas **vazio** — `img.onload` chamava só `health()`, nunca redesenho, e o estado inicia pausado, então o render inicial acontecia antes das imagens. Correção mínima: `onload`/`onerror` agendam um redesenho coalescido por `requestAnimationFrame` (sem laço: só desenha de cache já carregado; guarda de 4000 repinturas). Falha de recurso agora desenha marca vermelha explícita no canvas em vez de ficar em branco; leitura de pixel restrita (`file://` sem `--allow-file-access-from-files`) mostra aviso no painel de diff em vez de falhar em silêncio.

**Verificações que realmente rodaram** (navegador integrado, via `http://127.0.0.1:8791`, estado pausado, **sem interação**):

```
abertura (axe, f0)          #ca 5745 px opacos · #cb 5745 px · 48/48 recursos · 0 falhas
trocar par → sword          #ca 6137 · #cb 6137 · ok
camada body (axe)           #ca 5745 · #cb 5745 · ok
camada handFront (axe, f0)  #ca 0 · #cb 0 · ok=true (vazio legítimo: 0 px opacos em freeze e candidato)
comp (axe, f2)              #ca 6051 · #cb 6049 · ok  (diferença de 2 px = caso B)
resolução de caminhos       128/128 URLs resolvem a partir do diretório da própria página (semântica file://)
```

**Limitações destas verificações:**

- **`file://` não foi executado por mim**: a ferramenta de navegador disponível aceita apenas `http`/`https`. A prova para `file://` é a resolução estática de 128/128 caminhos relativos + zero falhas no servidor local. Não afirmo abertura visual em `file://` por observação própria.
- **Screenshot da página indisponível**: a aba roda em segundo plano e não compõe; as tentativas retornaram “tab has not painted”. Portanto **não há confirmação visual do layout** — apenas DOM, contagem de recursos e leitura de pixels dos canvas.
- O painel de saúde/autoteste da página expõe o estado (`data-selftest`, `__cmp.selftest()`), então o criador pode conferir sem devtools.

---

## 7. Movimento contínuo — resposta explícita

**Não houve validação visual de movimento contínuo.** O que existe: (a) amostragem numérica do relógio do player durante reprodução real em 1× (ordem e cadência corretas: fronteiras de quadro em `0,90,170,260,340,440,520,620` ms dentro de um tick de rAF, término exato em 730 ms); (b) imagens estáticas ampliadas. A continuidade ótica permanece para percepção humana. **Não afirmo validação temporal.**

---

## 8. Próximo passo recomendado

1. Decisão do criador sobre os três casos A/B/C: manter como está (nenhum é defeito provado) ou autorizar remoção, ciente do risco de recortar sola, fragmento de membro e fleco.
2. A pegada traseira só se resolve **re-assentando a arma** ao longo do eixo do cabo (o pomo precisa sair da silhueta do punho) — mudança de composição em 24 quadros, fora deste passe e não autorizada.
3. Rebordo pálido: decisão de direção de arte (re-tinta de contorno ou aceitar como linguagem do gerador). Não é reparo local.

Nada aqui é aprovação artística. Status permanece **`ARTISTIC_REVISION_REQUIRED` / `PENDING_CREATOR`**, sem integração.
