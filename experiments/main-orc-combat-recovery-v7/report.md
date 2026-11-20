# Orc V1 — combat recovery V7, economic pass (T1 · T2 · T3)

Character: `orc-v1` (Verde Warcraft)
Checkpoint: **`V7_ECON_FORENSICS_AND_FRONTAL_READY`**
Revision: `main-orc-v7-axilla-recovery`

| | |
|---|---|
| `technicalStatus` | **`TECHNICALLY_COMPLETE`** |
| `artisticStatus` | **`VISUAL_REVIEW_REQUIRED`** |
| `artisticApproval` | **`PENDING_CREATOR`** |
| `runtimeImplemented` | `false` |
| `eligibleForIntegration` | `false` |
| `fullClipIndependentQA` | `PENDING` |
| New PixelLab calls | **0** |
| Cost | **0.00 USD** |
| Unity files written | **0** |
| Commits | **0** |

This pass wrote only inside `characters/orc-v1/source/combat-recovery-v7/` and
`experiments/main-orc-combat-recovery-v7/`. It touched no V5 source, no V6 source, no rear cell and
no game project.

---

## 0. Visual limitation — binding for every claim below

DEV worked **without image perception**. No frame was seen. Every conclusion is derived from Pillow
pixel arithmetic over exported PNGs and from Aseprite Lua authoring and re-export.

Consequences that must be respected by whoever reads this next:

* A numeric verdict (`0 differing pixels`, `no artifact found`) is a statement about pixels, **not**
  about how the animation reads. Per the standing rule, technical completion is not artistic
  approval.
* The T3 result is a **negative result from a calibrated detector**, not a visual all-clear.
* Independent perceptual QA at 1x, at normal playback speed, is still required before creator
  review. That QA was explicitly out of scope here.

---

## 1. T1 — Where the rear Sword "white flash" comes from

Task: identify, do not fix.

**Verdict: the flash is authored content in the saved master. Nothing regenerated it, nothing
degraded it on export.**

### 1.1 Export chain proven airtight

A fresh Aseprite export of the saved master was compared against the committed artefacts of both
rear Sword clips:

| Comparison | Differing pixels |
|---|---|
| fresh export vs `layers/*.png` | **0** |
| fresh export vs `frames/*.png` | **0** |
| alpha-over recompose vs committed composite | **0** |

So the flash is not an export bug, not a layer-order bug and not a compositing bug. It is in the
master.

### 1.2 Root cause

The two bookend body layers of each rear Sword clip are **byte-identical to the preserved idle
body**:

| Clip layer | Identical to | Byte-identical |
|---|---|---|
| `back_l-sword/layers/body/00.png` | `complete-v1/back_l/Idle/00.png` | yes |
| `back_l-sword/layers/body/11.png` | `complete-v1/back_l/Idle/00.png` | yes |
| `back_r-sword/layers/body/00.png` | `complete-v1/back_r/Idle/00.png` | yes |
| `back_r-sword/layers/body/11.png` | `complete-v1/back_r/Idle/00.png` | yes |

The idle body SHA-256 is `0fb8c85ac00fddb016657c54a6180993eb0c2db800e65cf57beb4f9e4aede19`.

So F00 and F11 of each attack are not poses of the attack at all: they are the **idle** body,
reused to open and close the clip. The idle body carries a strong light-metal highlight on the
shoulder and upper arm. The generated attack bodies in F01…F10 do not. The cut F00 → F01 therefore
*removes* the highlight, and F10 → F11 *puts it back*. One frame of bright shoulder at each end of a
950 ms attack (12 frames, `90/80/80/110/50/40/40/80/100/90/90/100` ms) is what reads as a flash.

### 1.3 Measured magnitudes

Body light pixels on the lit side (left for `back_l`, right for `back_r`), per frame:

| Clip | F00 | F01 | F02 | F03 | F04 | F05 | F06 | F07 | F08 | F09 | F10 | F11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `back_l/Sword` | **61** | 13 | 15 | 15 | 15 | 17 | 14 | 21 | 19 | 24 | 21 | **61** |
| `back_r/Sword` | **46** | 2 | 0 | 0 | 3 | 2 | 0 | 6 | 5 | 3 | 2 | **46** |

Frame-to-frame deltas on the lit side: `back_l` F00→F01 **−48** and F10→F11 **+40**; `back_r`
F00→F01 **−44** and F10→F11 **+44**. Every other transition on the same side moves by 0–7 px. The two
bookend cuts are the only discontinuities in the clip by an order of magnitude.

Where the F00 highlight sits, `back_l/Sword` (4-connected light clusters ≥ 4 px):

| px | bbox | colours |
|---|---|---|
| 12 | `(98,122)–(102,131)` | `rgb(153,154,155)` ×6, `rgb(171,173,173)` ×6 |
| 12 | `(103,117)–(108,121)` | `rgb(153,154,155)` ×11, `rgb(171,173,173)` ×1 |
| 5 | `(97,133)–(99,137)` | `rgb(153,154,155)` ×4, `rgb(171,173,173)` ×1 |
| 4 | `(118,92)–(121,95)` | `rgb(171,173,173)` ×3, `rgb(153,154,155)` ×1 |

`back_r/Sword` F00 uses a single flatter colour, `rgb(156,158,158)`, in clusters of 11 px
`(151,117)–(155,122)`, 6 px `(123,153)–(126,155)` and 4 px `(147,104)–(150,105)` at both F00 and F11.

**Temporally isolated clusters ≥ 8 px** (light cluster with no light within ±2 px in either
neighbour frame): `back_r/Sword` has exactly one in F00 and one in F11 — the 11 px
`rgb(156,158,158)` group. `back_l/Sword`'s equivalent is the 9 px `rgb(153,154,155)` group at
`(103,117)–(108,119)`, also F00 only. In **F01…F10 of both clips there are zero temporally isolated
clusters ≥ 8 px** — the smaller interior groups (4–8 px) are present in neighbour frames, so they do
not read as a flash.

### 1.4 What T1 does not claim

T1 does not judge whether the highlight looks wrong. It states where those pixels come from. The
decision to keep, soften or remove the bookend highlight belongs to the composition owner, and any
change there would be a new authored pass with its own baseline and its own review.

Deliverables: `forensics/white-flash.md`, `forensics/white-flash.json`,
`forensics/master-vs-export.json`, `forensics/verify_master.py`.

---

## 2. T2 — `front_l/Sword` axilla repair

Task: repair the axilla only, `body` layer only, preserving pose, timing and weapons.

### 2.1 What was actually wrong

V6 escalation differs from the non-escalated frontal clip in **only two frames**:
F03 (30 px, bbox `(147,116)–(153,122)`) and F04 (28 px, bbox `(147,115)–(151,122)`).
F00–F02 and F05–F12 are identical. Within those two frames, four defects were confirmed:

| ID | Defect |
|---|---|
| **D1** | A flat `rgb(12,15,18)` **ink plate** on the new medial edge of the opening, `x=147 y117..122` in both frames, plus `(148,116)` in both and `(149,115)` in F04. Native tones there were `0,0,1` / `2,2,3` / `6,6,8` / `20,20,26` / `27,28,34`. Ink is the weapon-outline colour; on a body contour it reads as a dead plate. |
| **D2** | A **retrograde step** at `y=123`: the left boundary went `147 → 148 → 147`, i.e. the opening bulges inward then back out. |
| **D3** | An **orphan** `rgb(95,96,99)` at `(149,122)` in F03 with zero opaque 8-neighbours — a detached pixel floating in the opening. |
| **D4** | A **comb-tooth island** `rgb(77,79,82)` at `(152,115)` in F04, wedged between the 2 px pinhole at `x=150–151` and the main opening from `x=153`. |

Explicitly **ruled out** as V6 artifacts:

* the light column at `x=147 y127..133` — identical in the non-escalated clip, so it is a
  pre-existing rim;
* the 5 px apex at F03 `y=116` — consistent with its neighbours (F04 `y=114` is also 5 px).

### 2.2 The rule used

> Restore, do not invent. Every V6-repainted pixel returns to the colour it held in the
> non-escalated clip. Where that would leave a run of **3 or more identical colours** on the new
> medial edge, take the value the **adjacent column (`x+1`)** held on the same row.

Only **erasures** were added (D3's orphan, D4's island, the two notching pixels at `y=123`). No
pixel was filled. The V6 author's opening width is therefore preserved exactly.

### 2.3 The 19 edits

**F03 — 9 px**

| (x,y) | before | after | reason |
|---|---|---|---|
| (148,116) | `12,15,18` | `6,6,8` | native |
| (147,117) | `12,15,18` | `2,2,3` | native |
| (147,118) | `12,15,18` | `2,2,3` | native |
| (147,119) | `12,15,18` | `20,20,26` | native |
| (147,120) | `12,15,18` | `27,28,34` | native `x148` (native run would reach 4 identical) |
| (147,121) | `12,15,18` | `20,20,26` | native |
| (147,122) | `12,15,18` | `0,0,1` | native `x148`, deepest point of the crease |
| (149,122) | `95,96,99` | transparent | D3 orphan |
| (148,123) | `43,45,49` | transparent | D2 notch |

**F04 — 10 px**

| (x,y) | before | after | reason |
|---|---|---|---|
| (149,115) | `12,15,18` | `0,0,1` | native |
| (148,116) | `12,15,18` | `6,6,8` | native |
| (147,117) | `12,15,18` | `2,2,3` | native |
| (147,118) | `12,15,18` | `2,2,3` | native |
| (147,119) | `12,15,18` | `20,20,26` | native |
| (147,120) | `12,15,18` | `27,28,34` | native `x148` |
| (147,121) | `12,15,18` | `20,20,26` | native |
| (147,122) | `12,15,18` | `2,2,3` | native |
| (152,115) | `77,79,82` | transparent | D4 comb tooth |
| (148,123) | `20,20,26` | transparent | D2 notch |

Lightness before → after on the repaired plate: `14.6 → {0.1, 2.1, 6.1, 20.4, 28.2}`. The plate is
gone; the crease now has a graduated interior instead of a single flat value.

### 2.4 Geometry after repair

Left boundary of the opening, top to bottom:

```
F03: 148, 147, 147, 147, 147, 147, 147, 147, 147, 146    (monotone)
F04: 154, 149, 148, 147, 147, 147, 147, 147, 147, 147, 147, 146    (monotone)
```

Closed rows: F03 10 rows / 96 px, F04 4 rows / 55 px. Dangling pixels: **0** in both frames.

### 2.5 Verification

| Check | Result |
|---|---|
| Files byte-identical outside the patch | **84 of 98** |
| Files changed | **14**: the 13 declared content files (`03.png`, `04.png`, `composite-strip.png`, `frames/03·04`, `layers/body/03·04`, `native-strip.png`, `native/03·04`, and the 3 `.aseprite` masters) plus the rewritten `clip.json` |
| Unexpected changed files | **0** |
| Files only in baseline / only in candidate | 0 / 0 |
| Undeclared pixels changed | **0** |
| `weaponBack` + `weaponFront` + `handFront` exports byte-identical | **39/39** |
| Timing changed | **false** (durations `[30,65,35,50,45,65,35,35,100,55,80,45,90]`, 730 ms total, unchanged) |
| Layer order | `weaponBack → body → weaponFront → handFront` (4 layers, unchanged) |
| `body` master == composite `body` cel | pass |
| `native` == body crop | pass |
| `bodyRgbaDelta` vs plain (proxy for deviation) | F03 **30 → 27**, F04 **28 → 24** (improved) |

The last metric deserves a caveat: `bodyRgbaDelta` measures how far the frame's body deviates from
the non-escalated reference. It went *down*, which is the direction the repair intends, but it is a
**deviation** metric, not a quality metric — a perfect restoration would also score 0 while removing
the V6 opening entirely. It is reported as movement, not as proof of improvement.

### 2.6 Residual risk (declared, not hidden)

The medial edge of the opening still runs at `x=147` for nine consecutive rows (`y117..y125`).
Vertical runs of that length also exist in untouched frames (e.g. F05 `x=146 y123..129`), so this was
treated as the V6 author's opening choice and **not re-cut**. Only the colour plate, the notch and
the detached pixels were repaired. If independent QA reads that nine-row vertical as a hard edge,
fixing it is a new authored decision, not a continuation of this repair.

### 2.7 Authoring provenance

* Aseprite **1.3.18.6**, `--batch --noinapp`, isolated profile `tmp/aseprite-v7-econ-profile`.
* Script `scripts/author-frontl-sword-v7.lua` — `APPLIED 57 EDITS` (19 declared pixels × 3 masters:
  the composite `body` cel, the `body` master and the `native` master), then saved, reopened and
  re-exported.
* Loaded durations written as `Frame.duration` in **seconds**, as Aseprite requires.
* The repair is **programmatic authorship**: exact coordinates derived from measurement, executed by
  Lua inside the editor. It is not manual drawing and it is not a generative model.

Review surface: `frontal/review.html` (8x before/after per frame, 13-frame axilla sheet, full 19-pixel
table), plus `before-after-F03-8x.png`, `before-after-F04-8x.png`,
`composite-before-after-F03-4x.png`, `composite-before-after-F04-4x.png`,
`axilla-13-frames-v7-4x.png`.

---

## 3. T3 — Light contours in the four frontal clips

Task: search for confirmed light-contour artifacts and repair only those. Full analysis in
`frontal/light-contours.md`.

**Verdict: no confirmed artifact. 0 pixels changed.**

### 3.1 The definition had to be narrow

The frontal set is full of legitimate light pixels — rim light on the body, highlights on the blade
and axe head, glove rims. "Light pixel" is not "artifact". Five narrow classes were defined
(boundary light, small boundary light with run ≤ 2 px, halo speck, inset light line, 1 px contour
spike), and a candidate had to survive two controls before being called confirmed:

1. **palette control** — the composer's own colour vocabulary must not explain it;
2. **V5 control** — the pixel must not already exist before the escalation.

### 3.2 Threshold calibration

The character's palette tops out at **L = 177.72** (`rgb(176,178,180)`, blade edge). A "very light"
rule at L ≥ 200 would match nothing. Thresholds were swept at 120/130/140/145/150/160/170; the
operating value is **T = 145**, the highest that still *includes* the body rim family
`rgb(147,148,149)` (L = 147.9) while cleanly separating the metal bands (153.9 and 177.7) for
attribution. T = 170 was rejected as structurally blind to a body fringe.

### 3.3 Result

| Clip | body boundary light (T=145) | weapon boundary light | `smallLightOnBoundary` | `insetLightLine` | `spike` | confirmed | changed |
|---|---|---|---|---|---|---|---|
| `front_l/Sword` | 9 | 16 | 16 | 282 | 115 | **0** | **0** |
| `front_l/Axe` | 5 | 23 | 22 | 34 | 135 | **0** | **0** |
| `front_r/Axe` | 0 | 23 | 17 | 34 | 135 | **0** | **0** |
| `front_r/Sword` | 0 | 16 | 7 | 282 | 118 | **0** | **0** |

Every class resolves to legitimate vocabulary:

* the 14 **body** boundary-light pixels are all `rgb(147,148,149)`, each the maximum of a continuous
  5-step darkening ramp (`148 → 140 → 108 → 91 → 74 → 57`), present only on the lit-facing left
  views, and **all 14 already exist at the same coordinate in V5**;
* the **weapon** boundary light is metal edge lighting, and the weapon layers are byte-identical
  V5↔V7, so it cannot be V6-introduced;
* `insetLightLine` is 281/282 and 33/34 blade/axe-head shading (run 3–19 px), not a doubled outline;
* `spike` is the ink contour itself (`rgb(6,6,8)`/`rgb(0,0,1)`/`rgb(2,2,3)`); F00/F01 counts are
  identical in all four clips.

Mirror symmetry is a useful sanity signal: `front_l/Axe` ≡ `front_r/Axe` (34/34 inset, 135/135 spike)
and `front_l/Sword` ≡ `front_r/Sword` (282/282 inset). An artifact would not mirror to the pixel.

### 3.4 Control evidence

* **Boundary census V5 vs V7** (`detect/v5-vs-v7-boundary.json`): identical at T = 145 on every frame
  of all four clips. The only difference anywhere is `front_l/Sword` F03 at T = 120, where V7 has
  **two fewer** light boundary pixels — that is the T2 erasure; it removes light, it cannot create a
  fringe.
* **Layer diff V5 vs V7** (`detect/v5-vs-v7-layers.json`): `weaponBack` / `weaponFront` /
  `handFront` = **0 px changed on every frame of every clip**. Body deltas are 0–33 px, explained by
  the V6 isolated-pixel fix and the T2 repair.
* **Body-rim tuple identity** (`detect/body-rim-v5-control.json`): 9/9, 5/5, 0/0, 0/0 — every body
  rim pixel predates the escalation at the same coordinate and colour.

### 3.5 What a numeric negative cannot rule out

Stated so the next reviewer knows exactly what to look at:

1. A light contour *continuous with* a real rim that grew without crossing T = 145.
2. Perceived flicker at playback speed. Per-frame tables show no isolated single-frame spike, but
   that is a proxy for temporal perception, not a measurement of it.
3. Hue/saturation artifacts at identical lightness. Mitigated by exact RGBA matching against the
   palette ladder, not by the L detector.

---

## 4. Preservation

| Claim | Evidence |
|---|---|
| All tracked pre-existing inputs unchanged | `input-preservation.json` re-verified: **6647 / 6647** files byte-identical, 0 changed, 0 missing |
| V6 escalated baseline untouched | `source/composite.aseprite` still `a5207342…800c`, `clip.json` still `f6b3c694…06fd` |
| V5 control untouched | not written to at any point in this task |
| Rear cells untouched | T1 was read-only; the only writes were fresh Aseprite exports into `forensics/master-dump/` for comparison |
| Three of four frontal cells unchanged | byte-identical copies: `front_l/Axe` 79/79, `front_r/Axe` 79/79, `front_r/Sword` 85/85 |
| Weapons unchanged in the repaired cell | 39/39 layer exports byte-identical; `hand.aseprite` SHA identical to V6 (`ef3b3973…15df`) |
| Unity untouched | no write under `../TacticsRPG` |
| No commits | working tree left for the orchestrator |

The three non-Sword frontal copies under `combat-recovery-v7/frontal/` carry their **unmodified V6
`clip.json`**. That is intentional and valid: every PNG in those directories is byte-identical, so
the recorded hashes still describe the content. They exist purely as measurement carriers so the four
frontal cells can be reviewed side by side; they are not new candidates and carry no new claim.

---

## 5. Checkpoint state

Stopped at **`V7_ECON_FORENSICS_AND_FRONTAL_READY`**.

Done here: T1 identification, T2 repair with verification, T3 search with a documented negative
result, one clip re-exported with full provenance, review surface built.

**Not** done here, by design: independent QA, perceptive review, creator approval, any promotion, any
Unity integration, any commit.

The authoritative per-file record for this checkpoint is `patch-manifest.json`.

## Veredito do criador sobre o V7 e recomendacao de estrategia

O criador revisou a pagina V7 e rejeitou: problemas de frame pioraram, o flash da espada
**frontal** continua, e o ataque de costas esta **menos uniforme**. V7 permanece
`ARTISTIC_REJECTED`; nenhum QA foi autorizado a aprova-lo.

### Causa que o orquestrador assumiu
A integracao misturou quatro pipelines com ritmos incompativeis na mesma familia:

| Familia | frontal | back_r | back_l |
|---|---|---|---|
| Sword | 13f / 730 ms | 12f / 950 ms | 15f / 860 ms |
| Axe | 12f / 1005 ms | 12f / 1320 ms | 15f / 1230 ms |

Impacto no chao em instantes diferentes (frontal ~260 ms, `back_l` 425 ms, `back_r` 490 ms).
Isso ataca diretamente o criterio central do criador: reconhecer a mesma tecnica nas quatro
direcoes. O erro de montagem e do orquestrador, nao dos produtores.

### Flash frontal — assinatura medida (QA temporal, navegador real)
Luminancia clara por quadro em `front_r/Sword`: `161, 144, 255, 168, 163, 164, 144, 139, 151, 162, 181, 68, 161`.
Tres focos: entrada da arma em F02 (+111 px em 35 ms com queda de -87 em F03); salto da lamina
de 61 px em F05 -> F06 e mais 30 px em F06 -> F07 sem arco intermediario; e entalhe escuro em
F11 (-113) seguido de reascendimento de guarda em F12 (+93). Ha ainda um pixel especular em
(132,104) que oscila L=214 -> 20 -> 214.
A conclusao anterior de "nenhum artefato confirmado" estava errada porque media apenas rim-light
na borda do corpo; o flash e temporal e esta no intervalo da arma e no fechamento.

### Os dois QAs recomendaram a mesma estrategia
- Sol (`qa-sol/strategy-recommendation.md`): **A com reuso seletivo do V6 como doador**; manter
  `front_r/Sword` com seus 13 quadros e coreografia, corrigindo o flash por fork local; nao
  adotar regra cega de eliminar todo quadro abaixo de 50 ms, porque o proprio frontal protegido
  usa 35 ms — o que importa e a continuidade do gesto.
- Temporal (`qa-temporal/strategy-recommendation.md`): **A com variante A+**, unificando as quatro
  direcoes na grade frontal (13f/730 ms no Sword, 12f/1005 ms no Axe) e cravando o impacto no
  mesmo instante; zero geracao.

Divergencia real: o temporal quer back_r e back_l na mesma grade do frontal; o Sol alerta que
forcar uniformidade de tempo nao substitui continuidade de gesto e que o frontal protegido nao
pode ser re-timed. Resolucao proposta pelo orquestrador: adotar a grade frontal como referencia
de fases e tempo nas duas vistas traseiras, preservando poses e pegada ja refinadas de back_r,
e corrigir o flash frontal apenas por cirurgia local, sem tocar nas poses protegidas.

Nenhuma execucao foi autorizada ainda: reconstruir as duas celulas traseiras de novo e escopo
que o criador precisa aprovar.
