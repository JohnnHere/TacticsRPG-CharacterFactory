# Reconstrução back_l sobre v5 — entrega local

Status técnico: **TECHNICALLY_COMPLETE**. Status artístico: **VISUAL_REVIEW_REQUIRED**, **PENDING_CREATOR**. Há pontos **NEEDS_DECISION** abaixo; nenhum resultado técnico constitui aprovação artística.

A entrega contém Sword (14 quadros / 730 ms) e Axe (12 quadros / 1005 ms), camadas independentes, seis mestres Aseprite, compostos 256, recortes nativos 128, strips, 26 comparações antes/depois e 17 recortes armados em 8×. [Abrir revisão](review.html). O comparador reproduz ambas as versões na mesma grade, em 1×, 0,75× e 0,5×, permite passo a quadro e corpo com armas desligadas.

## Procedência e autoria

Autoria programática local no Aseprite 1.3.18.6, via `author.lua`; zero PixelLab, zero geração, nenhum serviço pago. As fontes v5/v8 foram somente lidas. Toda escrita desta execução ficou nesta pasta; nenhum commit ou integração. As alterações que já existiam no workspace foram preservadas. Não foi executada nenhuma abordagem 08a/08b ou transplante parcial.

Sword: corpo integral de cada quadro vem de `combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/body256/`. Não foi redesenhado nenhum braço ou punho. A espada é a Espada do Recruta v5, registrada pela definição original. Sua posição foi vinculada ao punho observado no corpo, com transformações de rotação em Aseprite e cabo atrás do corpo. `handFront` copia pixels existentes da luva e borda do punho; não cria dedos, sombras ou anatomia. Os encaixes do antigo script de composição não foram aceitos como evidência anatômica: a inspeção revelou que alguns apontavam para cota do antebraço. Os encaixes finais de v5 F05/F06 são [169,106] e [162,111]. O punho BODY-01 do v5 F06 está preservado no alvo F07.

Axe: todas as quatro camadas vêm diretamente dos oito quadros `combat-rescue-v5/combat/back_l/Axe/`. Isso preserva tanto a mão original sobreposta quanto a oclusão e a arma daquela pose. Não se confundiu o corpo layers-off com a mão de oclusão: a mão final original está em `handFront` e permanece independente, sem arma pintada nela por este passe.

`pose-map.md` e `author-config.json` registram a fonte e a operação de cada quadro. `source-hashes.json` fixa os arquivos-fonte efetivamente usados. Os manifests `clip.json` registram hashes dos mestres, camadas e derivados. A produção atual e as outras 26 células não foram alteradas.

## Decisões do mapa

O mapeamento é semântico. Sword usa repouso v5 F00, preparação F02, punho erguido F03, descida F05/F06, contato F07 e recuperação F08–F11. O corpo v5 F02 termina visualmente na região de cota: não oferece o mesmo punho fechado visível de F03. Por isso F02 só aparece na preparação desarmada; a entrada armada usa F03. Não foi inventada uma mão para completar essa pose.

Sword F03 desloca toda a pose de F03 v5 em +1 px; F04 em −1 px; F05 em −2 px, relativamente ao doador. Entre quadros consecutivos, são deslocamentos de 1–2 px. A mão mantém exatamente seus pixels e sua relação com o braço. Sword F06 (`apex-descent`) deriva diretamente da pose v5 F05, vizinha da descida; F07 usa F06 v5 e F08 usa o impacto F07 v5. A pose v5 F04, mais lateral, não foi forçada dentro da preparação elevada.

Axe F03 reutiliza a elevação F01 v5 com +1 px em X em todas as camadas, antes do ápice F02 v5. Os bookends repetem poses desarmadas originais. Nenhuma arma aparece em Sword F00–F01/F12–F13 ou Axe F00–F01/F09–F11.

## Limitações e NEEDS_DECISION

- **Sword F03–F05 — NEEDS_DECISION:** as fases de antecipação, coil e hold usam a mesma anatomia erguida v5 F03 com deslocamentos mínimos permitidos pelo brief. Há zero pares armados consecutivos byte-idênticos, mas isso não prova movimento expressivo: trata-se de um hold com deslocamento, não de três poses anatômicas novas. O criador precisa julgar se o hold de preparação é aceitável. Não inventei anatomia para esconder a escassez de poses elevadas.
- **Axe F03 — NEEDS_DECISION:** a antecipação usa a elevação anterior deslocada 1 px; é uma variação mínima, não uma nova articulação.
- **Continuidade Sword F05→F06:** a trajetória sai de um punho elevado para a pose de descida original. A redução de altura é real nos doadores, mas a transição é relativamente brusca. A lâmina atravessa visualmente a projeção do torso nas poses de descida; a pegada original fica preservada e visível. A leitura como corte descendente, em vez de arco lateral, permanece para julgamento visual, sem alegação de aprovação. O pequeno resíduo de contorno junto ao ombro da pose-fonte F05 também foi preservado, não refeito às cegas.
- **Dominância herdada:** o Axe v5 usa o lado de tela oposto ao Sword v5. Isso é herdado das fontes expressamente pedidas; não foi corrigido por espelhamento nem troca de membros.
- **Canvas nativo:** `native/` é recorte exato [64,64,128,128], sem redução. Algumas armas/membros elevados excedem esse recorte, como nas fontes. `temporal-check.json` informa os pixels externos por quadro. A revisão armada completa deve usar `frames/` e o mestre 256. O nativo 128 não é apresentado como exportação integral de equipamento nem como pacote runtime.

## Verificação

- Grades, fases, durações e contatos conferidos: Sword F08 / 325 ms / contact; Axe F06 / 410 ms / heavy-impact.
- Janelas armadas exatas F02–F11 e F02–F08. Bookends têm camadas de arma e mão de oclusão vazias.
- Zero pares armados consecutivos idênticos, tanto por PNG quanto por pixels visíveis.
- Corpos iguais às fontes v5 após apenas as translações declaradas. Mãos Sword copiadas do próprio corpo e visíveis sem alteração; mãos Axe iguais às camadas originais deslocadas junto ao corpo. Isso prova preservação, não adequação artística de cada pose.
- Alfa binário, composição `weaponBack → body → weaponFront → handFront` e recorte nativo verificados. RGB invisível sob alfa zero é ignorado na comparação de composição.
- Seis mestres reabertos no Aseprite; 78 renderizações conferidas contra PNGs, ordem de camadas e tempos salvos verificados (`master-roundtrip.json`).
- Python/Pillow foi usado somente para validação e superfícies de revisão (pares, ampliação nearest-neighbor e rótulos). Nenhum PNG de arte em `sword/` ou `axe/` foi criado ou editado por Pillow; esses derivados vieram do mestre salvo no Aseprite. As folhas `inspection-2x.png` são previews externos de inspeção, não fontes artísticas.

## Reprodução

1. `node experiments/main-orc-backl-v5base/prepare.mjs`
2. Executar Aseprite batch `--noinapp --script experiments/main-orc-backl-v5base/author.lua` com perfil separado `batch-profile/` nesta pasta.
3. Executar `verify-masters.lua` no mesmo modo.
4. Executar `finalize.py` e `build-review.py` com o Python de `tmp/pixel-venv/Scripts/python.exe`.

Aprovação e eventual promoção pertencem ao criador. Nenhuma seleção de produção foi alterada.

Player verificado em Chromium headless: 26 seleções de quadro, seis reproduções one-shot (duas categorias × três velocidades), troca de corpo layers-off e zero erros de página (`browser-check.json`). Capturas: `browser-sword.png` e `browser-axe.png`. Esses checks são funcionais e não aprovam a coreografia.

## Integracao no candidato combinado (V9 de revisao)

A pedido do criador, as duas celulas reconstruidas foram integradas a um **candidato combinado**:
o manifesto V8 com **apenas** `back_l/Sword` e `back_l/Axe` substituidos pelas celulas v5-base.
Todas as outras 26 celulas continuam byte-identicas ao V8.

- Manifesto: `characters/orc-v1/source/backl-v5base/candidate28manifest.json`
- 28 celulas / 13 ativas / 15 aliases / 232 quadros / pai = V8 `7afcfb6e9de2...`
- `eligibleForIntegration: false` / `VISUAL_REVIEW_REQUIRED` / `PENDING_CREATOR`
- Estudio combinado (todas as poses): `Biblioteca de Arte/Estudos Comparativos/Orc principal - V9 backl v5base/index.html`
- Verificacao Chromium propria: 45 imagens, 0 quebradas, 0 erros de pagina.

A prova do encaixe na grade esta em `integrate-candidate.mjs` (contratos conferidos antes da
escrita): contagens, contato, janela armada e bookends identicos ao pai.
