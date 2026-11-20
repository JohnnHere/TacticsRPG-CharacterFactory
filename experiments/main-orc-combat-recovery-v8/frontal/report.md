# V8 frontal anti-flash — checkpoint report

## State

The two isolated candidates were derived from the saved frontal sword masters and edited by Aseprite Lua with `ASEPRITE_USER_FOLDER` set to `tmp/aseprite-v8-frontal-profile`. PixelLab was not invoked. Composite masters were reopened and their frames re-exported. Both clips remain 13 frames / 730 ms; body pose and timing were not changed. Independent weapon layers remain in the composite masters.

## Luminance curve

Method used here: count of opaque composite pixels (`alpha >= 128`) with Rec. 601 luminance `>=160`, for each 256×256 frame. The supplied temporal QA series uses a different measurement (its stated front_r baseline is 161, 144, 255, ...), so these locally measured values must not be compared numerically to that series.

| Clip | Before F00–F12 | After F00–F12 |
|---|---|---|
| front_r/Sword | 38, 35, 94, 64, 66, 60, 62, 59, 57, 64, 64, 6, 38 | 38, 34, 33, 64, 66, 3, 5, 1, 57, 64, 6, 6, 38 |
| front_l/Sword | 38, 35, 94, 64, 66, 60, 62, 59, 57, 65, 64, 6, 38 | 38, 34, 33, 64, 66, 3, 5, 1, 57, 65, 6, 6, 38 |

## Edits and limits

- F02: neutral bright specular pixels on `weaponFront` were reduced (ceiling L132); the isolated spike is reduced in this local metric.
- F05–F07: neutral bright pixels on `weaponFront` were subdued (ceiling L142). This reduces the bright-pixel strobe; it does not add a trajectory smear.
- Breast glint: the specified single pixel was brought into a restrained per-frame light ramp. No body pixels were moved.
- F11: the measured count remains low (6) and still rises at F12 (38). The local metric therefore does **not** demonstrate that the blackout/re-illumination focus is fixed. The supplied QA series was not reproducible by this local count method, and no body-wide lighting adjustment was made without a matching measurement basis.

Visual inspection limitation: the temporal/browser QA reviewer should assess the final motion and light at playback speed. This report does not claim creator approval.

## Checkpoint disposition

`TECHNICALLY_COMPLETE` for the isolated Aseprite edits and exports. `VISUAL_REVIEW_REQUIRED`; `PENDING_CREATOR`. The requested acceptance checkpoint `V8_FRONTAL_FLASH_FIXED` is **not substantiated** because F11→F12 still jumps in the measured curve. No Unity integration or commits.
