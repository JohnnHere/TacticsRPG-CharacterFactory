import os, json

cycles_meta = [
    {
        'id': 'back_r-Sword-full',
        'title': 'Orc V1 — back_r / Sword — Full Body Attack Cycle',
        'direction': 'back_r',
        'weapon': 'Sword',
        'totalMs': 730,
        'durations': [40, 60, 60, 70, 70, 40, 40, 90, 70, 70, 60, 60],
        'phases': [
            '00 guard', '01 entry-1', '02 entry-2', '03 hoist (Key 01)',
            '04 apex (Key 02)', '05 descent-1', '06 descent-2',
            '07 impact (Key 03)', '08 recovery-1', '09 recovery-2',
            '10 recovery-3', '11 return-guard'
        ],
        'acceptedKeys': [3, 4, 7]
    },
    {
        'id': 'back_l-Sword-full',
        'title': 'Orc V1 — back_l / Sword — Full Body Attack Cycle',
        'direction': 'back_l',
        'weapon': 'Sword',
        'totalMs': 730,
        'durations': [40, 60, 60, 70, 70, 40, 40, 90, 70, 70, 60, 60],
        'phases': [
            '00 guard', '01 entry-1', '02 entry-2', '03 hoist (Key 01)',
            '04 apex (Key 02)', '05 descent-1', '06 descent-2',
            '07 impact (Key 03)', '08 recovery-1', '09 recovery-2',
            '10 recovery-3', '11 return-guard'
        ],
        'acceptedKeys': [3, 4, 7]
    },
    {
        'id': 'back_l-Axe-full',
        'title': 'Orc V1 — back_l / Axe — Full Body Attack Cycle',
        'direction': 'back_l',
        'weapon': 'Axe',
        'totalMs': 1100,
        'durations': [70, 80, 90, 100, 110, 50, 60, 110, 100, 100, 100, 130],
        'phases': [
            '00 guard', '01 entry-1', '02 entry-2', '03 hoist (Key 01)',
            '04 apex (Key 02)', '05 descent-1', '06 descent-2',
            '07 impact (Key 03)', '08 recovery-1', '09 recovery-2',
            '10 recovery-3', '11 return-guard'
        ],
        'acceptedKeys': [3, 4, 7]
    }
]

def make_single_html(meta, out_path):
    cid = meta['id']
    title = meta['title']
    durations_json = json.dumps(meta['durations'])
    phases_json = json.dumps(meta['phases'])
    
    cards = []
    for i in range(12):
        fn = f'{i:02d}.png'
        ph = meta['phases'][i]
        dur = meta['durations'][i]
        is_key = i in meta['acceptedKeys']
        key_tag = ' <strong style="color:#4ade80;">[QA KEY]</strong>' if is_key else ''
        cards.append(f'''
        <figure class="frame-card {'key-card' if is_key else ''}">
            <img width="128" height="128" src="native/{fn}">
            <figcaption>F{i:02d} · {ph}{key_tag}<br><strong>{dur} ms</strong></figcaption>
        </figure>''')
    cards_html = '\n'.join(cards)
    
    html = f'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body {{ font: 15px system-ui, -apple-system, sans-serif; background: #16181d; color: #e2e8f0; margin: 24px; line-height: 1.5; }}
h1 {{ margin: 0 0 8px 0; font-size: 22px; color: #f8fafc; }}
.badge {{ display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; margin-right: 6px; }}
.badge-tech {{ background: #065f46; color: #34d399; }}
.badge-art {{ background: #854d0e; color: #fde047; }}
.badge-qa {{ background: #1e3a8a; color: #93c5fd; }}
.controls {{ margin: 16px 0; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
button, select {{ background: #27272a; color: #f4f4f5; border: 1px solid #3f3f46; border-radius: 6px; padding: 8px 14px; font: inherit; cursor: pointer; }}
button:hover, select:hover {{ background: #3f3f46; }}
.stage {{ display: flex; gap: 32px; align-items: flex-end; padding: 24px; background: #0f1115; border-radius: 8px; border: 1px solid #27272a; margin: 16px 0; min-height: 420px; }}
img {{ image-rendering: pixelated; }}
#main {{ width: 384px; height: 384px; }}
#native {{ width: 128px; height: 128px; }}
#tactical {{ width: 64px; height: 64px; }}
figure {{ margin: 0; text-align: center; }}
figcaption {{ margin-top: 8px; font-size: 13px; color: #94a3b8; }}
.frames-strip {{ display: flex; flex-wrap: wrap; gap: 12px; margin: 20px 0; }}
.frame-card {{ background: #1e222b; border: 1px solid #334155; border-radius: 6px; padding: 10px; width: 140px; text-align: center; }}
.frame-card.key-card {{ border-color: #22c55e; background: #14281f; }}
a {{ color: #60a5fa; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
input[type=range] {{ width: 600px; max-width: 90vw; accent-color: #3b82f6; }}
.state-box {{ font-family: monospace; font-size: 15px; color: #38bdf8; margin: 10px 0; }}
</style>
</head>
<body>
<h1>{title}</h1>
<div>
    <span class="badge badge-tech">TECHNICALLY_COMPLETE</span>
    <span class="badge badge-art">VISUAL_REVIEW_REQUIRED</span>
    <span class="badge badge-qa">PENDING_CREATOR</span>
</div>
<p style="color:#94a3b8; margin:8px 0 16px 0;">12 frames · {meta['totalMs']} ms · Empty-handed layers-off · Accepted QA Keys byte-preserved at F03, F04, F07.</p>

<div class="controls">
    <button id="play">Play / Pause</button>
    <button id="replay">Replay</button>
    <button id="prev">◀ Prev Frame</button>
    <button id="next">Next Frame ▶</button>
    <label>Speed:
        <select id="speed">
            <option value="1">1.0× Normal</option>
            <option value="0.5">0.5× Slow</option>
            <option value="0.25">0.25× Slo-Mo</option>
        </select>
    </label>
    <label><input id="loop" type="checkbox" style="margin-left:8px;"> Loop Animation</label>
</div>

<div class="stage">
    <figure>
        <img id="main" alt="Diagnostic 3x">
        <figcaption>3× Diagnostic View (384×384)</figcaption>
    </figure>
    <figure>
        <img id="native" alt="Native 1x">
        <figcaption>1× Native Game Scale (128×128)</figcaption>
    </figure>
    <figure>
        <img id="tactical" alt="Tactical 0.5x">
        <figcaption>0.5× Tactical View (64×64)</figcaption>
    </figure>
</div>

<div class="state-box" id="state"></div>
<input id="seek" type="range" min="0" max="11" value="0" step="1">

<h2>Complete 12-Frame Sequence</h2>
<div class="frames-strip">
{cards_html}
</div>

<div style="margin-top:24px; padding-top:16px; border-top:1px solid #334155; font-size:14px; color:#94a3b8;">
    <a href="clip.json">clip.json contract</a> · 
    <a href="representative.json">representative.json</a> · 
    <a href="native-strip.png">native-strip.png</a> · 
    <a href="body256-strip.png">body256-strip.png</a> · 
    <a href="native128.aseprite">native128.aseprite</a> · 
    <a href="body256.aseprite">body256.aseprite</a>
</div>

<script>
const urls = Array.from({{length: 12}}, (_, i) => `native/${{String(i).padStart(2, '0')}}.png`);
const durations = {durations_json};
const phases = {phases_json};
const total = durations.reduce((a, b) => a + b, 0);
let ix = 0, elapsed = 0, playing = false, last = performance.now();
const starts = durations.map((_, i) => durations.slice(0, i).reduce((a, b) => a + b, 0));

function draw() {{
    for (const id of ['main', 'native', 'tactical']) {{
        document.getElementById(id).src = urls[ix];
    }}
    document.getElementById('seek').value = ix;
    document.getElementById('state').textContent = `Frame ${{String(ix).padStart(2, '0')}} / 11 · ${{phases[ix]}} · ${{durations[ix]}} ms (${{starts[ix]}}ms - ${{starts[ix] + durations[ix]}}ms) · ${{playing ? '▶ Playing' : '⏸ Paused'}}`;
}}

function frameAt(t) {{
    let acc = 0;
    for (let i = 0; i < durations.length; i++) {{
        acc += durations[i];
        if (t < acc) return i;
    }}
    return durations.length - 1;
}}

function setFrame(i) {{
    playing = false;
    ix = Math.max(0, Math.min(urls.length - 1, i));
    elapsed = starts[ix];
    draw();
}}

document.getElementById('play').onclick = () => {{
    if (elapsed >= total) {{ elapsed = 0; ix = 0; }}
    playing = !playing;
    last = performance.now();
    draw();
}};

document.getElementById('replay').onclick = () => {{
    elapsed = 0;
    ix = 0;
    playing = true;
    last = performance.now();
    draw();
}};

document.getElementById('prev').onclick = () => setFrame(ix - 1);
document.getElementById('next').onclick = () => setFrame(ix + 1);
document.getElementById('seek').oninput = e => setFrame(+e.target.value);

function tick(now) {{
    const delta = now - last;
    last = now;
    if (playing) {{
        elapsed += delta * +document.getElementById('speed').value;
        if (elapsed >= total) {{
            if (document.getElementById('loop').checked) {{
                elapsed %= total;
            }} else {{
                elapsed = total;
                playing = false;
            }}
        }}
        ix = frameAt(elapsed);
        draw();
    }}
    requestAnimationFrame(tick);
}}

for (const u of urls) {{
    const im = new Image();
    im.src = u;
}}
draw();
requestAnimationFrame(tick);
</script>
</body>
</html>'''
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Written {out_path}")

# Write individual HTML files
for m in cycles_meta:
    cid = m['id']
    p1 = os.path.join('experiments', 'main-orc-combat-rescue-v5', 'body-specialist', 'final-cycles', cid, 'review.html')
    p2 = os.path.join('characters', 'orc-v1', 'source', 'combat-rescue-v5', 'body-specialist', 'final-cycles', cid, 'review.html')
    make_single_html(m, p1)
    make_single_html(m, p2)

# Now build the Master Studio
cycles_json = json.dumps(cycles_meta)
master_html = f'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Orc V1 — Three Rear Unarmed Attack Cycles Master Review</title>
<style>
body {{ font: 15px system-ui, -apple-system, sans-serif; background: #0f1117; color: #e2e8f0; margin: 24px; line-height: 1.5; }}
h1 {{ margin: 0 0 8px 0; font-size: 24px; color: #f8fafc; }}
.badge {{ display: inline-block; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 600; margin-right: 8px; }}
.badge-tech {{ background: #065f46; color: #34d399; }}
.badge-art {{ background: #854d0e; color: #fde047; }}
.badge-qa {{ background: #1e3a8a; color: #93c5fd; }}
.tab-bar {{ display: flex; gap: 8px; margin: 20px 0 16px 0; border-bottom: 2px solid #27272a; padding-bottom: 8px; }}
.tab-btn {{ background: #1e222b; color: #94a3b8; border: 1px solid #334155; border-radius: 6px; padding: 10px 20px; font: inherit; font-weight: 600; cursor: pointer; }}
.tab-btn.active {{ background: #2563eb; color: #fff; border-color: #3b82f6; }}
.tab-btn:hover:not(.active) {{ background: #334155; color: #e2e8f0; }}
.controls {{ margin: 16px 0; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }}
button, select {{ background: #27272a; color: #f4f4f5; border: 1px solid #3f3f46; border-radius: 6px; padding: 8px 14px; font: inherit; cursor: pointer; }}
button:hover, select:hover {{ background: #3f3f46; }}
.stage {{ display: flex; gap: 32px; align-items: flex-end; padding: 24px; background: #161822; border-radius: 8px; border: 1px solid #27272a; margin: 16px 0; min-height: 420px; }}
img {{ image-rendering: pixelated; }}
#main {{ width: 384px; height: 384px; }}
#native {{ width: 128px; height: 128px; }}
#tactical {{ width: 64px; height: 64px; }}
figure {{ margin: 0; text-align: center; }}
figcaption {{ margin-top: 8px; font-size: 13px; color: #94a3b8; }}
.frames-strip {{ display: flex; flex-wrap: wrap; gap: 12px; margin: 20px 0; }}
.frame-card {{ background: #1e222b; border: 1px solid #334155; border-radius: 6px; padding: 10px; width: 140px; text-align: center; }}
.frame-card.key-card {{ border-color: #22c55e; background: #14281f; }}
a {{ color: #60a5fa; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
input[type=range] {{ width: 600px; max-width: 90vw; accent-color: #3b82f6; }}
.state-box {{ font-family: monospace; font-size: 15px; color: #38bdf8; margin: 10px 0; }}
.cycle-summary {{ background: #1a1e28; border: 1px solid #2d3748; border-radius: 8px; padding: 16px; margin: 16px 0; }}
</style>
</head>
<body>
<h1>Orc V1 — Three Rear Unarmed Attack Cycles Master Review</h1>
<div>
    <span class="badge badge-tech">BODY_THREE_FULL_READY</span>
    <span class="badge badge-tech">TECHNICALLY_COMPLETE</span>
    <span class="badge badge-art">VISUAL_REVIEW_REQUIRED</span>
    <span class="badge badge-qa">PENDING_CREATOR</span>
</div>
<p style="color:#94a3b8; margin:8px 0;">Evaluation studio for Independent QA (session 863ae631-5582-4955-a0ef-020d51692fbb). All 9 structural keys verified byte-exact at F03, F04, F07.</p>

<div class="tab-bar">
    <button class="tab-btn active" onclick="switchCycle(0)">1. back_r / Sword (12f · 730ms)</button>
    <button class="tab-btn" onclick="switchCycle(1)">2. back_l / Sword (12f · 730ms)</button>
    <button class="tab-btn" onclick="switchCycle(2)">3. back_l / Axe (12f · 1100ms)</button>
</div>

<div class="cycle-summary" id="cycleSummary"></div>

<div class="controls">
    <button id="play">Play / Pause</button>
    <button id="replay">Replay</button>
    <button id="prev">◀ Prev Frame</button>
    <button id="next">Next Frame ▶</button>
    <label>Speed:
        <select id="speed">
            <option value="1">1.0× Normal</option>
            <option value="0.5">0.5× Slow</option>
            <option value="0.25">0.25× Slo-Mo</option>
        </select>
    </label>
    <label><input id="loop" type="checkbox" style="margin-left:8px;"> Loop Animation</label>
</div>

<div class="stage">
    <figure>
        <img id="main" alt="Diagnostic 3x">
        <figcaption>3× Diagnostic View (384×384)</figcaption>
    </figure>
    <figure>
        <img id="native" alt="Native 1x">
        <figcaption>1× Native Game Scale (128×128)</figcaption>
    </figure>
    <figure>
        <img id="tactical" alt="Tactical 0.5x">
        <figcaption>0.5× Tactical View (64×64)</figcaption>
    </figure>
</div>

<div class="state-box" id="state"></div>
<input id="seek" type="range" min="0" max="11" value="0" step="1">

<h2>Cycle Frame Breakdown</h2>
<div class="frames-strip" id="framesStrip"></div>

<div style="margin-top:32px; padding-top:16px; border-top:1px solid #334155; font-size:14px; color:#94a3b8;">
    <strong>Cycle Artifacts:</strong>
    <span id="cycleLinks"></span>
</div>

<script>
const data = {cycles_json};
let currentCycleIdx = 0;
let ix = 0, elapsed = 0, playing = false, last = performance.now();

function getUrls(c) {{
    return Array.from({{length: 12}}, (_, i) => `${{c.id}}/native/${{String(i).padStart(2, '0')}}.png`);
}}

function updateSummary() {{
    const c = data[currentCycleIdx];
    document.getElementById('cycleSummary').innerHTML = `
        <strong style="font-size:16px; color:#f8fafc;">${{c.title}}</strong><br>
        <span style="color:#94a3b8;">Direction: <strong>${{c.direction}}</strong> · Weapon Profile: <strong>${{c.weapon}}</strong> · Total Duration: <strong>${{c.totalMs}} ms</strong> · Ground line: <strong>y=126 (128x128) / y=190 (256x256)</strong></span><br>
        <span style="color:#4ade80;">QA Accepted Keys preserved byte-exact: F03 (${{c.phases[3]}}), F04 (${{c.phases[4]}}), F07 (${{c.phases[7]}})</span>
    `;
    
    const urls = getUrls(c);
    let html = '';
    for (let i = 0; i < 12; i++) {{
        const isKey = c.acceptedKeys.includes(i);
        const tag = isKey ? ' <strong style="color:#4ade80;">[QA KEY]</strong>' : '';
        html += `
            <figure class="frame-card ${{isKey ? 'key-card' : ''}}">
                <img width="128" height="128" src="${{urls[i]}}">
                <figcaption>F${{String(i).padStart(2, '0')}} · ${{c.phases[i]}}${{tag}}<br><strong>${{c.durations[i]}} ms</strong></figcaption>
            </figure>
        `;
    }}
    document.getElementById('framesStrip').innerHTML = html;
    
    document.getElementById('cycleLinks').innerHTML = `
        <a href="${{c.id}}/clip.json">clip.json</a> · 
        <a href="${{c.id}}/representative.json">representative.json</a> · 
        <a href="${{c.id}}/native-strip.png">native-strip.png</a> · 
        <a href="${{c.id}}/body256-strip.png">body256-strip.png</a> · 
        <a href="${{c.id}}/review.html">Dedicated review.html</a>
    `;
}}

function switchCycle(idx) {{
    currentCycleIdx = idx;
    const btns = document.querySelectorAll('.tab-btn');
    btns.forEach((b, i) => b.classList.toggle('active', i === idx));
    ix = 0;
    elapsed = 0;
    playing = false;
    updateSummary();
    draw();
}}

function draw() {{
    const c = data[currentCycleIdx];
    const urls = getUrls(c);
    const starts = c.durations.map((_, i) => c.durations.slice(0, i).reduce((a, b) => a + b, 0));
    for (const id of ['main', 'native', 'tactical']) {{
        document.getElementById(id).src = urls[ix];
    }}
    document.getElementById('seek').value = ix;
    document.getElementById('state').textContent = `Frame ${{String(ix).padStart(2, '0')}} / 11 · ${{c.phases[ix]}} · ${{c.durations[ix]}} ms (${{starts[ix]}}ms - ${{starts[ix] + c.durations[ix]}}ms) · ${{playing ? '▶ Playing' : '⏸ Paused'}}`;
}}

function frameAt(c, t) {{
    let acc = 0;
    for (let i = 0; i < c.durations.length; i++) {{
        acc += c.durations[i];
        if (t < acc) return i;
    }}
    return c.durations.length - 1;
}}

function setFrame(i) {{
    const c = data[currentCycleIdx];
    const starts = c.durations.map((_, i) => c.durations.slice(0, i).reduce((a, b) => a + b, 0));
    playing = false;
    ix = Math.max(0, Math.min(11, i));
    elapsed = starts[ix];
    draw();
}}

document.getElementById('play').onclick = () => {{
    const c = data[currentCycleIdx];
    if (elapsed >= c.totalMs) {{ elapsed = 0; ix = 0; }}
    playing = !playing;
    last = performance.now();
    draw();
}};

document.getElementById('replay').onclick = () => {{
    elapsed = 0;
    ix = 0;
    playing = true;
    last = performance.now();
    draw();
}};

document.getElementById('prev').onclick = () => setFrame(ix - 1);
document.getElementById('next').onclick = () => setFrame(ix + 1);
document.getElementById('seek').oninput = e => setFrame(+e.target.value);

function tick(now) {{
    const delta = now - last;
    last = now;
    const c = data[currentCycleIdx];
    if (playing) {{
        elapsed += delta * +document.getElementById('speed').value;
        if (elapsed >= c.totalMs) {{
            if (document.getElementById('loop').checked) {{
                elapsed %= c.totalMs;
            }} else {{
                elapsed = c.totalMs;
                playing = false;
            }}
        }}
        ix = frameAt(c, elapsed);
        draw();
    }}
    requestAnimationFrame(tick);
}}

switchCycle(0);
requestAnimationFrame(tick);
</script>
</body>
</html>'''

with open('experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/review.html', 'w', encoding='utf-8') as f:
    f.write(master_html)
print("Written Master review.html")
