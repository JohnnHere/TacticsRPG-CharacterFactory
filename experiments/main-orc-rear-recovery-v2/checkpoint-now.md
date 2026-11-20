# Checkpoint now — 2026-10-26 23:19 UTC

## Current production state

- Root internal visual checkpoint: `back_l/Axe` is `PASS_FOR_INTERNAL_INTEGRATION`. Root viewed its full composite cycle, weapon-layers-off body sequence, grip closeups, and actual Aseprite-exported 730ms 1x GIF. This is not independent Argon QA or creator approval.
- The four rear weapon representatives are present as independent four-layer Aseprite sources with separate 256px composites and 128px body masters. Their saved-master re-export/source check passes; all 1x, 0.75x, and 0.5x GIF delay totals are verified.
- Front Unarmed F02 remains localized to frame 02 in both views. Original `[80,110,50,90,120]ms` cadence is preserved; the other four frames per view match the protected complete-v1 exports byte-for-byte. Native images match the composite center crop.
- Canonical matrix: 12 `ACTIVE_CANDIDATE`, 0 `ARTISTIC_REVISION_REQUIRED`, 0 `IN_PRODUCTION`, 16 `UNCHANGED_ALIAS`; 12 affected cells. Root-only internal review states remain in `reviewStatus`.
- Candidate package source work is `TECHNICALLY_COMPLETE`; artistic status remains `VISUAL_REVIEW_REQUIRED`, creator approval `PENDING_CREATOR`, independent Argon QA `NOT_STARTED`, and `runtimeImplemented: false`.

## AxeL repair provenance

The only AxeL generation was job `5296ac98-b253-4133-8468-155f7e90c68e` (asset `42cb4114-2fe0-5310-a3e7-79b640105256`, 3 generations). Raw frames and hashes remain in `raw/pixellab-skeleton-v3/back_l_axe/`. In Aseprite, the generated opposite-side axe and detached shaft were removed with localized same-view base restoration. The clipped raised arm was repaired by adapting only the accepted same-view SwordL body/hand pixels for frames 01/02; the AxeL torso, legs, armor, lighting, and NW perspective remain its own. The confirmed 27px detached old-arm residue in F02 was removed by exact-coordinate mask, not a component-size filter. Details and point lists are in `axeL-local-repair-provenance.json`.

## Accounting

The ledger now sums to 78 generations across 17 jobs. The original authorized cap remains 66; the first 3-generation representative job executed before explicit approval and is retained as an authorization deviation (actual 69 at that checkpoint). Two subsequent authorized jobs and the final authorized AxeL job charged 3 each, reaching 78. Current additional generation authorization is zero. Do not edit raw receipts or claim earlier approval.

## Checks and report

- `node experiments/main-orc-rear-recovery-v2/verify_new_representatives.mjs --check` — PASS, read-only, all four rear weapon clips.
- `node experiments/main-orc-rear-recovery-v2/verify_front_f02_and_protected_frames.mjs` — PASS, read-only, 10 front frames and saved master timing.
- Manifest counts and all 12 affected clip paths were checked directly; every path exists.
- Legacy baseline snapshot sweep matches 792/793 entries. The one mismatch is `config/artistic-quality-gates-v1.json`; the existing snapshot was not rewritten. The Python wrapper could not run because Python is unavailable in this environment.
- Full final status/provenance is in `E/production-final-report.md`.
