# DEV handoff — main-orc-rear-reconstruction-v4

**ARTISTIC_REVISION_REQUIRED · PENDING_CREATOR · diagnostic-only · eligibleForIntegration=false.**

The broad artistic task is **not fulfilled**. This delivery preserves useful local weapon/scalp work and an actual rejected reconstruction attempt. It must not be presented as recovered rear combat, an artistic PASS, or an eligible replacement for the current candidate. The failure of the tested donor assembly does **not** establish that no artistic solution exists. It establishes only that I did not produce a convincing reconstruction to propagate in this bounded session.

[Isolated manifest](../../../characters/orc-v1/source/rear-reconstruction-v4/candidate28manifest.json) · [focused check results](verification.json) · [measured deltas](measured-deltas.json) · [frame classifications](frame-classifications.json) · [checkpoint history](checkpoint-history.json). Final owned-file hashes are in `version-freeze.json`; that inventory excludes its own file and the disposable isolated batch profile.

## Exact output and eligibility

The manifest uses the existing `cells` schema and immediate input `characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json`, revision `main-orc-targeted-recovery-v3`, SHA-256 `51f18754dbb588d9c2c5571b03ca92d5dac8236432137cf14dd5a0976df30e18`. The previous QA's latest section provides technical PASS with continuous artistic1× playback explicitly unverified. Neither that PASS nor prior checkpoints were interpreted as creator approval.

The isolated matrix contains28 clips /210 frames:8 affected weapon clips /82 frames and20 exact prior-clip aliases /128 frames. Four frontal cells are `ACTIVE_CANDIDATE` for material review; four rear cells are `ARTISTIC_REVISION_REQUIRED`. All aliases have `isAffected=false` relative to this session's input. `technicalStatus=NOT_VERIFIED` is deliberate at package level: focused checks cover the produced subset, not a new global certification. `integrationReport` points to Root's agreed `experiments/main-orc-rear-reconstruction-v4/orchestration-report.md`; this DEV did not create or edit that report.

Two new independent editable weapon definitions are associated coherently with all eight weapon clip forks through `weaponDefinitions`. Each affected clip has fresh composite/body/native masters, PNGs, layers, strips, frame times and hashes. The active choreography and hand masks remain those of the parent clips. No new rear choreography is selected. The separate rejected keypose is excluded from the manifest.

## Implemented local artwork

**Axe:**346 source RGBA positions changed. The existing silhouette,96×96 canvas, one-handed size and grip `[36,55]` remain exact. Aseprite-authored layers organize the forged head into clearer planes, give its cutting bevel a coherent curve, separate warm ash wood from iron, and organize the existing leather bands. No item was enlarged or created.

**Sword:**100 source RGBA positions changed. Light fuller/guard/leather refinement; exact original alpha,96×96 size and grip `[48,66]`. Existing successful frontal body movement was preserved.

Both forks retain inherited source layers beneath named retouch layers. This is inherited PixelLab weapon art refined programmatically inside Aseprite, not newly generated or manually painted GUI art. [Source comparison](weapons-before-after.png), [associated Axe comparison](axe-associated-before-after.png), [associated Sword comparison](sword-associated-before-after.png). The associated sheets were captured before the later scalp-only cleanup; they remain accurate weapon-material evidence, not a freeze-wide scalp comparison. Final scalp evidence is separate below.

**Confirmed scalp outline:** back_r attack F01–F07 contain a gray skull perimeter absent from the darker F00 contour. This exists in the body without equipment. All19 inspected F04 gray cap coordinates match raw `pixellab-skeleton-v3/back_r_axe/03.png` exactly. Thus these specific pixels are inherited source content, not a preview interpolation artifact. This does not classify other pale pixels or legitimate armor reflections as defects.

The correction replaces only explicit scalp coordinates in the inspected cap region with `INK(12,15,18)`:18/10/9/19/12/4/11 positions in F01..07,83 per back_r clip,166 frame-pixel substitutions across Sword/Axe. F00, collar, shoulder metal and every other body position remain exact. This is a bounded cap cleanup, **not a claim that every pale perimeter elsewhere is resolved**. [Coordinates and asserted input colors](scalp-outline-points.json) · [source diagnostic](outline-source-diagnostic.json) · [final cap comparison](scalp-outlines-before-after.png).

Across the eight clip forks,58 composite frames differ:56 contain material changes and two additional hidden-weapon F07 frames contain scalp cleanup only. Composite RGBA deltas summed across frames:

| Clip | Changed positions across its frames |
|---|---:|
| front_r/Sword |772|
| front_l/Sword |772|
| front_r/Axe |2206|
| front_l/Axe |2206|
| back_r/Sword |592|
| back_r/Axe |1943|
| back_l/Sword |521|
| back_l/Axe |1830|

These are per-frame image differences, not unique newly drawn pixels, generations, or an improvement score.

## Stage A and actual reconstruction attempt

All210 input frames were laid out for static inspection. [Per-frame classifications](frame-classifications.json) distinguish `KEEP`, `LOCAL_CORRECTION` and `REAUTHOR_KEY_POSE`; no timing edit was justified. A category was not forced into use merely to fill the taxonomy. Rear F01..F05 require new validated keys, with recovery dependent on those keys. Frontal choreography, all Idle/Hit, and rear Defeat remain protected.

**Confirmed reuse mechanism:** all8 back_r Sword and Axe body images are pixel-identical, with identical730ms timing arrays. The current author script also explicitly assigns SwordR the AxeR body set. Weapon angles differ; the underlying body technique does not. This supports the diagnosis of indiscriminate cross-category reuse. It alone does not quantify naturalness or prove that every shared pose is unusable.

I then authored a real back_r/Axe F04 descending study in Aseprite, using the actual same-view source bracer/fist and chainmail sleeve as separately masked components, an independently articulated elbow, a reseated scapular plate and individually drawn fold clusters. No full-character rotation, flattening, crossfade, paid generation or generic replacement figure was used. An initial body study exposed old sleeve residue; that residue was removed in the equipped revision. Both inspection images are retained.

The final study changes1369 visible body RGBA positions, bbox native `[51,27]..[120,75]`. Its editable five-component body master, equipped four-layer master, source F04 and exported studies are under `characters/orc-v1/source/rear-reconstruction-v4/keypose-axeR/`. [Body attempt comparison](keypose-before-after.png) · [equipped F03→F04→F05 comparison](keypose-neighbors-equipped.png) · [rejection record](../../../characters/orc-v1/source/rear-reconstruction-v4/keypose-axeR/rejection.json).

**Why rejected:** the donor rotation narrows the forearm and leaves a patch-like elbow rather than preserving the original armored mass. The scapular reseating does not establish convincing whole-torso participation. In the actual neighboring poses, the hand/axe descends in the study then returns upward in unchanged F05. The small grip study does not convincingly close the hand around the handle. Propagating this F04 would distribute a new discontinuity, not repair the technique. No intermediate frames, opposite direction or complete library were derived from it.

The local production blocker is therefore specific: **this session has no validated set of rear anticipation/strike/follow-through keys with coherent torso, arm mass and grip**. Existing offset/glove solutions were not reused as an answer. The rejected Sol F05 experiment was read and excluded; the isolated Unarmed Sol F03 proposal was read but not blindly transplanted onto a subsequently changed canonical torso. This is neither a permission blocker nor proof that Aseprite/local authorship cannot solve the problem.

## Confirmed, unverified and unchanged

| Area | Actual diagnosis and disposition |
|---|---|
| Rear Sword/Axe | Identical back_r body reuse confirmed; overall static rigidity and poor differentiated technique observed. No new accepted strike keys. Primary reconstruction and natural grip **unresolved**. |
| Unarmed, all4 views | Full static sequences inspected. No partial-alpha pixels in the20 native frames; no accidental exact intermediate duplicate found. back_l F00=F04 is the deliberate closure. Back_l F02→F03 differs615 positions, so it is not an exact duplicate. Rear retraction/opposite-arm choreography still needs work. Frontal reported late hand disappearance was **not motion-localized**; no invented import-amputation cause or speculative edit. |
| Frontal Defeat | Current terminal sources already show the low head and prone body, unlike older kneeling versions. Hands in F02/F03 were inspected as discrete clusters. No new source smear was demonstrated; all10 native frames have binary alpha. Binary alpha does not disprove a drawing artifact. Preserved pending creator playback review. |
| Walk, all4 views | Static sequences inspected; no reliable continuous visual flicker localization established. No shading or timing changes made. |
| Idle/Hit, rear Defeat | Exact input aliases; no art/timing changes. Future Hit gameplay timing remains a Unity calibration item, outside this task. |
| Bright perimeter elsewhere | Cap source mechanism confirmed only as scoped above. Other body/metal borders need semantic inspection; no global luminance filter added. |

Neither continuous1× artistic playback nor an independent QA was performed by this DEV. Static native/tactical-size sheets, source inspection, working animation metadata and correct clocks do not certify movement. Root owns the diagnostic player and independent QA. No full acceptance claim is made for any unresolved area.

## Focused checks and reproducibility

[verification.json](verification.json) records successful focused technical checks:

- 873 inventoried input files remain SHA-256 identical, including canonical manifests, selected masters/exports, protected clip dependencies and independent weapon inputs. This is the collected scope, not a claim about every repository file.
- 82 produced frames: independent Aseprite binary decoding agrees with composite/body/native exports and their actual trimmed cel positions. Native crops use exactly bodyOffset `[64,64]`.
- All82 frame times equal their parents in composite/body/native saved headers. Four named layers and exact alpha-over recomposition verified.
- Body pixels outside the166 explicit cap substitutions are exact; all handFront pixels are exact. Every equipment alpha/depth mask is exact; hidden frames contain only the body.
- Both independent weapon source masters reproduce their PNGs; source alpha/canvas/grips are exact. All56 visible original transforms were registered against actual source/overlay pixels with occupied-mask equality; frontal raw colors matched exactly. Prior rear dark contour overrides are retained at their original pixels, separately from the new source retouch. This preserves existing treatment without applying a new brightness threshold.
- Native/composite strips reproduce their corresponding frames exactly; declared new file hashes are computed from actual files.

All art edits, master saves and production exports ran inside Aseprite1.3.18.6, hidden `--batch --noinapp`, exclusive `dev/batch-profile`,90s process timeout. No interactive GUI was touched. Python/PIL/NumPy only read/validated pixels, wrote metadata and laid out diagnostic comparisons. No broad full suite, duplicate independent audit, package install, Unity write, commit, agent or paid API call occurred. **New generation calls:0.** Historical accounting was not rewritten; no token, dollar or balance estimates were made.

Reproduction from the confirmed repository cwd, before reviewing/freeze reuse:

```text
node experiments/main-orc-rear-reconstruction-v4/dev/aseprite.mjs --script experiments/main-orc-rear-reconstruction-v4/dev/author-weapons.lua
node experiments/main-orc-rear-reconstruction-v4/dev/aseprite.mjs --script experiments/main-orc-rear-reconstruction-v4/dev/compose-material-forks.lua
tmp/pixel-venv/Scripts/python.exe experiments/main-orc-rear-reconstruction-v4/dev/package.py
tmp/pixel-venv/Scripts/python.exe experiments/main-orc-rear-reconstruction-v4/dev/finalize-diagnosis.py
```

Inputs/registrations/explicit cap coordinates are frozen in this DEV directory. `author-keypose.lua` reproduces the rejected study separately and must not be inserted into the candidate. These commands overwrite only this owned candidate; **do not rerun them during Root's review of the freeze**.

## Suggested evidence-based recipe additions for Root

These are proposals for Root's authoritative documentation, not edits to shared docs or approved recipes.

1. **Different technique needs different validated body keys.** Symptom: Sword/Axe differentiation resides mainly in equipment. Confirmed cause:8/8 identical back_r body frames and equal timing. Failed approach: swapping weapon angles/glove masks over the same rigid keys. Successful replacement: **pending**. Prevention/reuse: share only individually justified poses; validate shoulder/torso plus impact and recovery before propagation. Verify with layers-off neighbor inspection and real1× review, not a hash-difference quota. Cost here:0 generation calls. Applies to all shared melee families.
2. **Trace pale source borders semantically.** Symptom: gray skull halo while metal needs legitimate reflections. Confirmed cause:19/19 examined F04 points inherited from raw generated material; the prior high-luma gate did not characterize these mid-gray pixels. Failed approach: universal brightness perimeter treatment as an artistic answer. Local correction: explicit scalp coordinates,83 substitutions per back_r clip, all other body pixels preserved. Reuse/prevention: distinguish skin contour from metal before authoring a mask; verify exact coordinates plus before/after image. Cost:0 generation calls. Applies to generated body silhouettes; not a universal rule for weapon cutting edges.
3. **Retain failed component assembly as a negative example.** Symptom: thin bracer/elbow and a down-then-up strike. Confirmed cause in this attempt: independently turned flat donor pieces did not preserve joint volume or resolve adjacent trajectories. Failed approach: this1369-position F04 study. Successful correction: **pending**, not the material fork. Prevention/reuse: require accepted key-pose mass and neighbor trajectories before interpolating. Verify full body, equipment and neighbors at native/tactical size. Cost:0 generation calls, no propagation. Applies to reconstructed articulated limbs and torso-driven attacks.
4. **Register actual overlay pixels when metadata is incomplete.** Symptom: some frontal grip fields are null despite existing composed artwork. Confirmed cause: current clip fields do not carry the actual seat, while overlay/source pixels do. Local method: read-only registration recovers exact occupied masks for56 visible frames; Aseprite uses these to update independent materials while preserving existing depth/hand masks. This solves this material association, **not natural grip**. Prevention: record the transform from authorship at export. Verify source-color/mask equivalence and saved-master renders. Cost:0 generation calls. Applies to recovering existing equipment associations without silently moving successful choreography.

## Ownership and final handoff

Writes are confined to `characters/orc-v1/source/rear-reconstruction-v4/` and `experiments/main-orc-rear-reconstruction-v4/dev/`. Cwd was confirmed before writes. The candidate contains553 files and28 masters:24 clip masters,2 independent weapon masters,2 rejected-study masters. Git shows the two new untracked owned paths; the already-dirty repository was neither cleaned nor attributed to this DEV. Baseline sources, `assets/weapons`, canonical matrix, shared docs and builder were not edited.

Root may build a **diagnostic** review from this manifest against the immediate prior manifest. Material and cap work can be assessed separately from the excluded failed keypose. A functioning28-cell review must continue to advertise **ARTISTIC_REVISION_REQUIRED / PENDING_CREATOR / diagnostic-only**. Further artistic reconstruction is still required to meet the user's task. After writing the final freeze, this DEV stops mutations so Root's review copies cannot race packaging.
