"""Exercise the local review UI with installed Edge in an isolated headless session.
This verifies playback controls/source loading, never Unity or artistic approval.
"""
import argparse,hashlib,json,time
from pathlib import Path
from playwright.sync_api import sync_playwright


def check(url,allow_incomplete=False,file_display_only=False):
    output=Path("characters/orc-01/reports")
    errors=[];checks=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(channel="msedge",headless=True)
        page=browser.new_page(viewport={"width":1600,"height":1000},device_scale_factor=1)
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.goto(url,wait_until="networkidle")
        page.wait_for_function("window.reviewData && window.reviewFrame !== undefined")
        data=page.evaluate("window.reviewData")
        loaded=page.evaluate("""async()=>{const paths=Object.values(reviewData.clips).flatMap(s=>Object.values(s).flat()).filter(Boolean);return await Promise.all(paths.map(src=>new Promise(resolve=>{const i=new Image;i.onload=()=>resolve({src,width:i.naturalWidth,height:i.naturalHeight});i.onerror=()=>resolve({src,error:true});i.src=src})));}""")
        if any(x.get("width")!=128 or x.get("height")!=128 for x in loaded):raise AssertionError("Invalid/unloaded runtime PNG in preview")
        for state,count in data["counts"].items():
            page.select_option("#state",state)
            page.click("#restart")
            completeness=[sum(bool(x) for x in data["clips"][state][d]) for d in data["directions"]]
            if not allow_incomplete and any(n!=count for n in completeness):raise AssertionError(f"Incomplete clip {state}: {completeness}")
            if not allow_incomplete:
                page.wait_for_function("Array.from(document.querySelectorAll('#strips img')).length===4 && Array.from(document.querySelectorAll('#strips img')).every(i=>i.complete&&i.naturalWidth)")
                strips=page.locator("#strips img").evaluate_all("els=>els.map(i=>({width:i.naturalWidth,height:i.naturalHeight,src:i.getAttribute('src')}))")
                if any(i["width"]!=128*count or i["height"]!=128 for i in strips):raise AssertionError(f"Invalid native strip {state}")
            page.locator("#frame").evaluate("(e,value)=>{e.value=value;e.dispatchEvent(new Event('input',{bubbles:true}))}",count-1)
            page.wait_for_function(f"window.reviewFrame === {count-1}")
            if file_display_only:
                # file: images can be displayed but taint canvas pixel reads.
                # Pixel checks are performed in the HTTP run and on native PNGs.
                canvas=page.evaluate("()=>Array.from(document.querySelectorAll('canvas')).map(c=>({id:c.id,pixelRead:'NOT_RUN_FILE_ORIGIN_SECURITY'}))")
            else:
                canvas=page.evaluate("""()=>Array.from(document.querySelectorAll('canvas')).map(c=>{const a=c.getContext('2d').getImageData(0,0,128,128).data;let bottom=-1,partial=0;for(let y=0;y<128;y++)for(let x=0;x<128;x++){const alpha=a[(y*128+x)*4+3];if(alpha)bottom=y;if(alpha>0&&alpha<255)partial++}return{id:c.id,bottom,partial}})""")
                if any(c["bottom"]!=126 or c["partial"] for c in canvas):raise AssertionError(f"Canvas registration/alpha mismatch {state}")
            page.click("#restart")
            if state in ("Attack","Hit","Defeat") and all(n==count for n in completeness):
                page.wait_for_timeout(round(count*data["durations"][state]+120))
                if page.evaluate("window.reviewFrame")!=count-1:raise AssertionError("One-shot did not hold final frame")
            checks.append({"state":state,"requiredFramesPerDirection":count,"presentFrames":completeness,"canvasChecks":canvas,"lastFrameScrub":"PASS","oneShotHold":"PASS" if state in ("Attack","Hit","Defeat") and all(n==count for n in completeness) else "NOT_APPLICABLE"})
        page.select_option("#state","Walk")
        page.locator("#frame").evaluate("e=>{e.value=3;e.dispatchEvent(new Event('input',{bubbles:true}))}")
        page.wait_for_function("window.reviewFrame===3")
        page.screenshot(path=str(output/("animation-review-file.png" if file_display_only else "animation-review-browser.png")),full_page=True)
        page.select_option("#state","Defeat")
        page.locator("#frame").evaluate("e=>{e.value=4;e.dispatchEvent(new Event('input',{bubbles:true}))}")
        page.wait_for_function("window.reviewFrame===4")
        page.screenshot(path=str(output/("defeat-last-frame-file.png" if file_display_only else "defeat-last-frame-browser.png")),full_page=True)
        version=browser.version
        browser.close()
    if errors:raise AssertionError(errors)
    result={"browser":"Microsoft Edge headless via Playwright","version":version,"loadedAnimationPng":len(loaded),"checks":checks,"pageErrors":errors,"localPreviewOnly":True,"fileDisplayOnly":file_display_only,"unityPlayMode":"NOT_RUN","artisticApproval":"PENDING_CREATOR"}
    (output/("animation-preview-file.json" if file_display_only else "animation-preview-browser.json")).write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps({"loadedAnimationPng":len(loaded),"statesChecked":len(checks),"pageErrors":errors,"unityPlayMode":"NOT_RUN"}))


if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--url",default="http://127.0.0.1:8781/characters/orc-01/review-animations-v1.html");ap.add_argument("--allow-incomplete",action="store_true");ap.add_argument("--file-display-only",action="store_true")
    args=ap.parse_args();check(args.url,args.allow_incomplete,args.file_display_only)
