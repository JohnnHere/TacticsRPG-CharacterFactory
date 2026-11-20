# -*- coding: utf-8 -*-
"""Gera review.html principal (raiz experiments glm-fixes) + por ciclo (ambas as raízes)."""
import os

CH = "characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes"
EX = "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes"

CYC = {
    "back_r-Sword-full": dict(dur=[40,60,60,70,70,40,40,90,70,70,60,60], total=730,
        defect="REAR-01-RESIDUAL-A/B (F06)",
        fix="5 px flutuantes -> alfa 0; 30 px vinho -> malha (doadores F05/F07 mesmas coords); 0 fora do permitido",
        cmp="glm-back_r-Sword-f06-before-after.png"),
    "back_l-Axe-full": dict(dur=[70,80,90,100,110,50,60,110,100,100,100,130], total=1100,
        defect="REAR-02-PERSISTENT (F02)",
        fix="Re-autoria anatomica via inpaint PixelLab (job 540302e4, seed 20261029, 6.0 gen) composta no Aseprite; delta 510 px confinado a mascara x68..100/y8..33; braco conectado ombro->punho",
        cmp="glm-back_l-Axe-f02-before-after.png"),
}

TEMPLATE = """
<div class="player"><canvas id="c_{t}" width="128" height="128"
 style="image-rendering:pixelated;width:256px;height:256px"></canvas>
<div><button onclick="step_{t}(-1)">&lt;</button><button onclick="toggle_{t}()">play</button>
<button onclick="step_{t}(1)">&gt;</button>
<select onchange="sp_{t}=parseFloat(this.value)">
<option value="1">1.0x</option><option value="0.75">0.75x</option>
<option value="0.5">0.5x</option><option value="0.25">0.25x</option></select>
<span id="i_{t}"></span></div></div>
<script>(function(){{
var D=[{d}],N=12,i=0,run=null,sp=1,imgs=[];
for(var k=0;k<N;k++){{var im=new Image();im.onload=draw;im.src='{f}'.replace('XX',('0'+k).slice(-2));imgs.push(im);}}
var cv=document.getElementById('c_{t}'),ctx=cv.getContext('2d');
function draw(){{ctx.clearRect(0,0,128,128);ctx.drawImage(imgs[i],0,0);
document.getElementById('i_{t}').textContent=' F'+('0'+(i+1)).slice(-2)+'/'+D[i]+'ms';}}
function next(){{i=(i+1)%N;draw();if(run)run=setTimeout(next,D[i]/sp);}}
window.step_{t}=function(d){{if(!run){{i=(i+d+N)%N;draw();}}}};
window.toggle_{t}=function(){{if(run){{clearTimeout(run);run=null;}}else{{run=setTimeout(next,D[i]/sp);}}}};
window.sp_{t}=sp;var so=document.querySelector('select');if(so){{so.onchange=function(){{sp=parseFloat(this.value);}};}}
draw();}})();</script>
"""

def player_js(tag, dur, frame_path):
    s = TEMPLATE.replace("{t}", tag)
    s = s.replace("{d}", ",".join(str(x) for x in dur))
    s = s.replace("{f}", frame_path)
    return s.replace("{{", "{").replace("}}", "}")

def section(name, frame_path):
    c = CYC[name]
    tag = name.replace("-", "_")
    return ("<h2>%s — %s (12f / %dms)</h2><p><b>Defeito:</b> %s<br><b>Correção:</b> %s</p>%s"
            "<p><img src=\"%s\" alt=\"antes/depois %s\" "
            "style=\"image-rendering:pixelated;max-width:100%%\"></p>"
            % (name, c["defect"], c["total"], c["defect"], c["fix"],
               player_js(tag, c["dur"], frame_path), c["cmp"], name))

main = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>GLM Body Fixes — Revisão</title><style>body{background:#141418;color:#ddd;font-family:monospace;
margin:16px;max-width:1100px}h1{color:#ffd166}h2{color:#8ad}img,canvas{background:#222;border:1px solid #444}
button,select{background:#333;color:#ddd;border:1px solid #666}.warn{color:#f88}</style></head><body>
<h1>GLM Body Fixes — Orc V1 traseiros (candidato, sem autoaprovação)</h1>
<p><b>Status:</b> GLM_BODY_FIXES_READY · TECHNICALLY_COMPLETE · VISUAL_REVIEW_REQUIRED ·
PENDING_CREATOR (global: ARTISTIC_REVISION_REQUIRED preservado)</p>
<p class="warn"><b>Limite visual declarado:</b> o DEV não possui visão de imagem; toda análise foi
textual (Pillow/hex). Inspeção visual final cabe ao QA independente Gemini Flash Antigravity e ao Criador.</p>
%s
<h2>Verificação técnica (textual)</h2>
<pre>FIX A (back_r-Sword F06): diff 35 px, 0 fora do permitido; 5 flutuantes alfa 0;
0 px vinho em y88..94/x45..55; 11 frames byte-idênticos; ground 126/190; composto exato → PASS
FIX B (back_l-Axe F02): diff 510 px, 0 fora da máscara; 0 runs de trave ≥8px;
componente braço 673 px (y10..37) conectado ombro→zona punho; punho marrom 15 px (x83..91/y16..20);
y≥40 idêntico ao original; 11 frames byte-idênticos; ground 126/190; composto exato → PASS
Chaves F03/F04/F07: SHA-256 idênticos aos aceitos pelo QA (assert no gerador) — os 6 arquivos.
PixelLab: saldo 1342.70 → 1336.70 (1 job inpaint 6.0 gen). Custo LLM não informado.</pre>
</body></html>""" % (section("back_r-Sword-full", "./back_r-Sword-full/native/XX.png") +
                     section("back_l-Axe-full", "./back_l-Axe-full/native/XX.png"))

with open(os.path.join(EX, "review.html"), "w", encoding="utf-8") as f:
    f.write(main)

for name, c in CYC.items():
    tag = name.replace("-", "_")
    pl = player_js(tag, c["dur"], "native/XX.png")
    html = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>%s — GLM fix</title>
<style>body{background:#141418;color:#ddd;font-family:monospace;margin:16px}canvas,img{background:#222}
button,select{background:#333;color:#ddd;border:1px solid #666}</style></head><body>
<h1>%s</h1><p><b>Defeito:</b> %s<br><b>Correção:</b> %s</p>%s
<p><img src="../%s" style="image-rendering:pixelated;max-width:100%%"></p>
<p>Frames nativos: <a href="native-strip.png" style="color:#8ad">strip</a> ·
Compostos: <a href="body256-strip.png" style="color:#8ad">strip 256</a></p>
</body></html>""" % (name, name, c["defect"], c["fix"], pl, c["cmp"])
    for root in (EX, CH):
        with open(os.path.join(root, name, "review.html"), "w", encoding="utf-8") as f:
            f.write(html)
print("REVIEW HTML OK")
