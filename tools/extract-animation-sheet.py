"""Split authored animation sheets and reconstruct registered native frames.

Never synthesizes motion from a static image: the required number of separate
drawings must actually exist in the sheet. Missing/extra drawings fail closed.
Native pixel translation and a shared palette are the only finishing steps.
"""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

spec = importlib.util.spec_from_file_location("native_recovery", Path(__file__).with_name("recover-native-sprite.py"))
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)

COUNTS = {"Idle": 4, "Walk": 6, "Attack": 5, "Hit": 3, "Defeat": 5}
HEIGHTS = {"Idle": [100, 99, 100, 99], "Walk": [100, 99, 98, 100, 99, 98],
           "Attack": [100, 100, 98, 99, 100], "Hit": [100, 97, 99]}
DURATIONS = {"Idle": 240, "Walk": 73, "Attack": 90, "Hit": 80, "Defeat": 120}


def head_x(arr):
    yy, xx = np.where(arr[:, :, 3] > 0)
    top, height = yy.min(), yy.max()-yy.min()+1
    r, g, b = [arr[:, :, c].astype(float) for c in range(3)]
    skin = (arr[:, :, 3]>0)&(g>55)&(r>g*.85)&(r<g*1.35)&(b<g*.85)
    skin[top+max(3, round(height*.15)):] = False
    skin[:top] = False
    ys, xs = np.where(skin)
    return float(np.median(xs)) if len(xs) else float(np.median(xx))


def extract(sheet_path, state, direction, palette_path, base_path, allow_overlapping=False, content_heights=None, registration="head"):
    sheet_path = Path(sheet_path)
    raw = sheet_path.read_bytes()
    arr = np.array(Image.open(io.BytesIO(raw)).convert("RGBA"))
    mask = (arr[:, :, 3] >= 160).astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    if n <= 1:
        raise ValueError("Empty sheet")
    biggest = stats[1:, cv2.CC_STAT_AREA].max()
    component_ids = [i for i in range(1,n) if stats[i, cv2.CC_STAT_AREA] >= biggest*.15]
    component_ids.sort(key=lambda i: stats[i, cv2.CC_STAT_LEFT])
    if len(component_ids) != COUNTS[state]:
        raise ValueError(f"Expected {COUNTS[state]} complete figures; found {len(component_ids)}. No invented frames.")
    if content_heights is not None and (len(content_heights)!=COUNTS[state] or any(h<1 or h>126 for h in content_heights)):
        raise ValueError('Explicit native content heights must match count and fit canvas')
    if registration not in ('head','pelvis'):raise ValueError('Unknown registration')
    boxes = []
    for i in component_ids:
        x,y,w,h,area = map(int, stats[i])
        boxes.append([x,y,x+w,y+h])
    overlapping = any(boxes[i][2] >= boxes[i+1][0] for i in range(len(boxes)-1))
    if overlapping and not allow_overlapping:
        raise ValueError("Figures overlap in X; sheet must be visually reviewed/resliced")
    base = np.array(Image.open(base_path).convert("RGBA"))
    def pelvis_x(arr):
        yy,xx=np.where(arr[79:95,:,3]>0)
        return float(np.median(xx)) if len(xx) else head_x(arr)
    target_head = head_x(base) if registration=='head' else pelvis_x(base)
    reports, frames = [], []
    out_dir = sheet_path.parent
    for index, (component, box) in enumerate(zip(component_ids, boxes)):
        x0,y0,x1,y1 = box
        crop = arr[y0:y1, x0:x1].copy()
        local = labels[y0:y1,x0:x1] == component
        crop[~local] = 0
        source = out_dir / f"frame-{index:02d}-source.png"
        Image.fromarray(crop).save(source)
        target_height = (HEIGHTS[state][index] if state != "Defeat"
                         else round((y1-y0)/(boxes[0][3]-boxes[0][1])*100))
        if content_heights is not None:target_height=content_heights[index]
        output = out_dir / f"{state.lower()}_{direction}_{index:02d}.png"
        report = native.recover(source, output, target_height, 48, palette_path, quiet=True)
        frame = np.array(Image.open(output).convert("RGBA"))
        dx = 0
        if state != "Defeat":
            facing = -1 if direction.endswith("_l") else 1
            target_offsets = {"Attack": [0,-2,2,1,0], "Hit": [0,-2,-1]}
            head_offset = target_offsets.get(state,[0]*len(boxes))[index]*facing
            dx = round(target_head+head_offset-(head_x(frame) if registration=='head' else pelvis_x(frame)))
            ys,xs = np.where(frame[:,:,3]>0)
            if registration=='pelvis':dx=max(1-int(xs.min()),min(126-int(xs.max()),dx))
            if xs.min()+dx < 1 or xs.max()+dx > 126:
                raise ValueError(f"Frame {index} head registration would clip; inspect source")
            shifted = np.zeros_like(frame)
            if dx > 0: shifted[:,dx:] = frame[:,:-dx]
            elif dx < 0: shifted[:,:dx] = frame[:,-dx:]
            else: shifted = frame
            frame = shifted
            Image.fromarray(frame).save(output)
            Image.fromarray(frame).resize((512,512),Image.Resampling.NEAREST).save(output.with_name(output.stem+"-4x.png"))
        report.update({"sheet": str(sheet_path), "sheetSha256": hashlib.sha256(raw).hexdigest(),
                       "frameIndex": index, "sourceBox": box, "nativeHeadTranslationX": dx,
                       "nativeTranslationX":dx,
                       "registrationAnchor":registration,
                       "outputSha256": hashlib.sha256(output.read_bytes()).hexdigest()})
        output.with_suffix(".json").write_text(json.dumps(report,indent=2),encoding="utf-8")
        frames.append(Image.fromarray(frame))
        reports.append(report)
    # RGBA lossless animation preview; no transparency tricks or runtime claim.
    frames[0].save(out_dir/"preview.png",save_all=True,append_images=frames[1:],
                   duration=DURATIONS[state],loop=0 if state in ("Idle","Walk") else 1,
                   disposal=0,blend=0)
    contact = Image.new("RGBA",(128*len(frames),128),(0,0,0,0))
    for i,frame in enumerate(frames): contact.paste(frame,(i*128,0))
    contact.save(out_dir/"native-strip.png")
    checks = {"state":state,"direction":direction,"frames":len(frames),
              "source":str(sheet_path),"sourceSha256":hashlib.sha256(raw).hexdigest(),
              "boxes":boxes,"xBoundsOverlap":overlapping,"separateComponentsVisuallyReviewed":bool(overlapping and allow_overlapping),
              "durationMs":DURATIONS[state],"loop":state in ("Idle","Walk"),
              "method":"Separate authored poses + native grid reconstruction + integer registration",
              "uniqueRgbaFrames":len({hashlib.sha256(np.array(f).tobytes()).hexdigest() for f in frames}),
              "artisticApproval":"PENDING_CREATOR","reports":[Path(r["output"]).with_suffix(".json").name for r in reports]}
    (out_dir/"clip.json").write_text(json.dumps(checks,indent=2),encoding="utf-8")
    if checks["uniqueRgbaFrames"] != len(frames):
        raise ValueError("Duplicate poses detected; do not import this clip")
    print(json.dumps(checks,indent=2))
    return checks


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet")
    ap.add_argument("--state",required=True,choices=COUNTS)
    ap.add_argument("--direction",required=True,choices=["front_r","front_l","back_r","back_l"])
    ap.add_argument("--palette",default="characters/orc-01/source/pixel-grid-v1/front-r-native.png")
    ap.add_argument("--base",required=True)
    ap.add_argument("--allow-overlapping-boxes",action="store_true",help="Only after visual review of distinct connected bodies")
    args = ap.parse_args()
    extract(args.sheet,args.state,args.direction,args.palette,args.base,args.allow_overlapping_boxes)
