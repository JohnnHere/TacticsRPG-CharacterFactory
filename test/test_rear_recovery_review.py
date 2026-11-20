"""
Automated validation of the isolated review page:
- HTML existence and size
- 404 checks for all referenced images, links, scripts
- JavaScript matrix structure validation (4 directions x 7 actions = 28 cells)
- Manifest status matching
- Controls and label validation
- Defeat terminal hold & speed & zoom options
"""
import re, json, sys
from pathlib import Path
from PIL import Image

R = Path('.').resolve()
review_dir = R / 'Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira'
html_file = review_dir / 'index.html'
manifest_file = R / 'characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json'

# Status vocabulary: current manifest uses the literal ARTISTIC_REVISION_REQUIRED;
# legacy IN_REVISION remains supported. ALL expectations below are DERIVED from the
# manifest (counts may change on future producer refreshes — never hardcoded).
REVISION_STATUSES = {'IN_REVISION', 'ARTISTIC_REVISION_REQUIRED'}

print("=== AUTOMATED REVIEW VALIDATION (manifest-driven) ===")
manifest = json.loads(manifest_file.read_text(encoding='utf-8-sig'))
manifest_cells = manifest['cells']
manifest_status = {(c['direction'], c['action']): c.get('status') for c in manifest_cells}
manifest_affected = {(c['direction'], c['action']): bool(c.get('isAffected')) for c in manifest_cells}
exp_active = sorted(f"{d}/{a}" for (d, a), s in manifest_status.items() if s == 'ACTIVE_CANDIDATE')
exp_alias_count = sum(1 for s in manifest_status.values() if s == 'UNCHANGED_ALIAS')
exp_revision = sorted(f"{d}/{a}" for (d, a), s in manifest_status.items() if s in REVISION_STATUSES)
exp_production_count = sum(1 for s in manifest_status.values() if s == 'IN_PRODUCTION')
exp_affected = sorted(f"{d}/{a}" for (d, a), v in manifest_affected.items() if v)
assert html_file.exists(), f"index.html missing: {html_file}"
html_content = html_file.read_text(encoding='utf-8')
print(f"Loaded index.html: {len(html_content)} bytes")

# Separate HTML body from <script>
script_split = html_content.split('<script>')
body_html = script_split[0]
script_body = script_split[1] if len(script_split) > 1 else ''

# 1. Extract matrix from HTML
matrix_match = re.search(r'const matrix = ({.*?});\s*const DIRECTIONS', html_content, re.DOTALL)
assert matrix_match, "Failed to find 'const matrix = {...}' in index.html"
matrix_json_str = matrix_match.group(1)
matrix = json.loads(matrix_json_str)

directions = ['front_r', 'front_l', 'back_r', 'back_l']
actions = ['Idle', 'Walk', 'Unarmed', 'Sword', 'Axe', 'Hit', 'Defeat']

assert set(matrix.keys()) == set(directions), f"Directions mismatch: {matrix.keys()}"

total_cells = 0
active_candidates = []
unchanged_aliases = []
in_revision = []
in_production = []
missing_files = []

for d in directions:
    assert set(matrix[d].keys()) == set(actions), f"Actions mismatch in {d}: {matrix[d].keys()}"
    for act in actions:
        total_cells += 1
        cell = matrix[d][act]
        st = cell['status']
        if st == 'ACTIVE_CANDIDATE':
            active_candidates.append(f"{d}/{act}")
        elif st == 'UNCHANGED_ALIAS':
            unchanged_aliases.append(f"{d}/{act}")
        elif st in REVISION_STATUSES:
            in_revision.append(f"{d}/{act}")
        elif st == 'IN_PRODUCTION':
            in_production.append(f"{d}/{act}")
        # Status must match the manifest exactly (no silent fallback, no stale vocabulary)
        if st != manifest_status[(d, act)]:
            missing_files.append(f"STATUS MISMATCH {d}/{act}: html={st} manifest={manifest_status[(d, act)]}")
        # Every affected non-ready cell must be flagged isPending (explicit pending UI)
        if manifest_affected[(d, act)] and st not in ('ACTIVE_CANDIDATE', 'UNCHANGED_ALIAS') and not cell.get('isPending'):
            missing_files.append(f"PENDENCY FLAG MISSING {d}/{act}: affected non-ready cell without isPending")
            
        # Check all frame pngs exist
        frames = cell['frames']
        assert len(frames) > 0, f"Cell {d}/{act} has no frames!"
        frame_dir = (review_dir / frames[0]['png']).parent
        expected_names = {Path(f['png']).name for f in frames}
        actual_names = {p.name for p in frame_dir.glob('*.png')}
        assert actual_names == expected_names, f'Stale or missing preview frames in {d}/{act}: {actual_names ^ expected_names}'
        for f in frames:
            png_path = review_dir / f['png']
            if not png_path.exists():
                missing_files.append(f"Frame png missing: {f['png']} in {d}/{act}")
                
        # Check master and strip
        if cell.get('master'):
            m_path = review_dir / cell['master']
            if not m_path.exists():
                missing_files.append(f"Master missing: {cell['master']} in {d}/{act}")
        if cell.get('strip'):
            s_path = review_dir / cell['strip']
            if not s_path.exists():
                missing_files.append(f"Strip missing: {cell['strip']} in {d}/{act}")

print(f"Total cells validated: {total_cells} (Expected 28)")
assert total_cells == 28, f"Expected 28 cells, got {total_cells}"
print(f"Active candidates ({len(active_candidates)}): {sorted(active_candidates)}")
assert sorted(active_candidates) == exp_active, f"Active candidates diverge from manifest: {sorted(active_candidates)} vs {exp_active}"
print(f"Unchanged aliases ({len(unchanged_aliases)}): expected from manifest = {exp_alias_count}")
assert len(unchanged_aliases) == exp_alias_count, f"Alias count diverges from manifest: {len(unchanged_aliases)} vs {exp_alias_count}"
print(f"In revision ({len(in_revision)}): {sorted(in_revision)}")
assert sorted(in_revision) == exp_revision, f"Revision cells diverge from manifest: {sorted(in_revision)} vs {exp_revision}"
print(f"In production ({len(in_production)}): expected from manifest = {exp_production_count}")
assert len(in_production) == exp_production_count, f"Production count diverges from manifest: {len(in_production)} vs {exp_production_count}"
affected_in_html = sorted(set(active_candidates) | set(in_revision) | set(in_production))
print(f"Affected cells (manifest): {len(exp_affected)}; non-ready/active rendered: {len(affected_in_html)}")

# 1b. Derived summary cards, package status and dynamic before/after coverage
print("Verifying manifest-derived summary cards and package status...")
assert f'>{len(exp_active)}</span>' in html_content, "Active-candidate summary pill not derived from manifest"
assert f'>{exp_alias_count}</span>' in html_content, "Alias summary pill not derived from manifest"
assert f'>{len(exp_revision)}</span>' in html_content, "Revision summary pill not derived from manifest"
assert f'>{exp_production_count}</span>' in html_content, "Production summary pill not derived from manifest"
known_bad = bool(exp_revision) or exp_production_count > 0
expected_package_status = 'ARTISTIC_REVISION_REQUIRED' if known_bad else 'VISUAL_REVIEW_REQUIRED'
assert expected_package_status in html_content, "Package status must reflect the actual manifest"
if not known_bad:
    assert 'VISUAL_REVIEW_REQUIRED' in html_content, "Package status must return to VISUAL_REVIEW_REQUIRED once clear"
# No stale hardcoded narrative (old 2 active / 16 alias / 1 revision / 9 production UI)
assert '(9 células)' not in html_content, "Stale hardcoded '9 células' production narrative still present"
assert 'Células em Fila de Produção pelo Art Producer' not in html_content, "Stale hardcoded production-queue narrative still present"
assert 'weak-punch' not in html_content and 'Weak punch' not in html_content, "Stale rejected weak-punch evidence pretending to be current candidate"
# Before/After: EVERY affected cell needs baseline + candidate strips rendered
for key in exp_affected:
    d, act = key.split('/')
    base_rel = f'AntesDepois/{d}_{act}_baseline_strip.png'
    assert base_rel in html_content, f"Before/After baseline strip missing for affected cell {key}"
    assert f'<code>{d}</code> {act}' in html_content, f"Before/After card heading missing for affected cell {key}"
if exp_revision:
    assert html_content.count('Candidato entregue REJEITADO') >= len(exp_revision), "Rejected-candidate labelling missing for revision cells"
    assert html_content.count('NÃO resolvida') >= len(exp_revision), "Unresolved-baseline labelling missing for revision cells"
print(f"  OK: derived pills (active={len(exp_active)}, alias={exp_alias_count}, revision={len(exp_revision)}, production={exp_production_count})")
print(f"  OK: package status {expected_package_status} matches manifest")
print(f"  OK: before/after coverage for all {len(exp_affected)} affected cells")

# Real pixel check for the discovered body-only / unequal-scale strip regression.
# These images are preview layouts; every tile must equal its composite frame.
for d in directions:
    for act in actions:
        cell = matrix[d][act]
        with Image.open(review_dir / cell['strip']) as strip_image:
            strip_rgba = strip_image.convert('RGBA')
        assert strip_rgba.size == (256 * len(cell['frames']), 256), f'Wrong strip scale: {d}/{act}'
        for i, frame in enumerate(cell['frames']):
            with Image.open(review_dir / frame['png']) as frame_image:
                expected = frame_image.convert('RGBA')
            actual = strip_rgba.crop((i * 256, 0, (i + 1) * 256, 256))
            assert actual.tobytes() == expected.tobytes(), f'Strip omits/changes composite pixels: {d}/{act} F{i}'
print('  OK: all review strips preserve exact composite pixels and equal canvas scale')

# 2. Extract and check all static <img> and <a href> tags in body HTML for 404s
img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', body_html)
print(f"Checking {len(img_srcs)} static <img> tags in HTML...")
for src in img_srcs:
    if src.startswith('data:') or src.startswith('#') or src.startswith('http'):
        continue
    img_path = review_dir / src
    if not img_path.exists():
        missing_files.append(f"<img> src not found: {src}")

a_hrefs = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', body_html)
print(f"Checking {len(a_hrefs)} static <a href> links in HTML...")
for href in a_hrefs:
    if href.startswith('data:') or href.startswith('#') or href.startswith('http'):
        continue
    link_path = (review_dir / href).resolve()
    if not link_path.exists():
        missing_files.append(f"<a> href target not found: {href} -> {link_path}")

if missing_files:
    print(f"FAILED: Found {len(missing_files)} missing files / 404s:")
    for mf in missing_files:
        print("  -", mf)
    sys.exit(1)
else:
    print("PASSED: Zero 404s! All static images, strips, masters, and links resolve.")

# 3. Verify user controls and options in HTML
print("Verifying user controls in HTML...")
assert 'id="play"' in html_content, "Missing #play button"
assert 'id="reset"' in html_content, "Missing #reset button"
assert 'id="step-prev"' in html_content, "Missing #step-prev button"
assert 'id="step-next"' in html_content, "Missing #step-next button"
assert 'id="select-dir"' in html_content, "Missing #select-dir dropdown"
assert 'id="select-action"' in html_content, "Missing #select-action dropdown"
assert 'id="select-transition"' in html_content, "Missing #select-transition dropdown"
assert 'id="speed"' in html_content, "Missing #speed dropdown"
assert 'id="zoom"' in html_content, "Missing #zoom dropdown"
assert 'id="loop"' in html_content, "Missing #loop checkbox"

# Check speeds: 1, 0.75, 0.5
assert 'value="1"' in html_content, "Missing 1x speed option"
assert 'value="0.75"' in html_content, "Missing 0.75x speed option"
assert 'value="0.5"' in html_content, "Missing 0.5x speed option"
print("  OK: Speeds 1x, 0.75x, 0.5x present")

# Check zoom / practical scale:
assert 'Escala Prática Jogo (128×128)' in html_content, "Missing practical scale option"
assert 'value="0.5"' in html_content, "Missing 0.5 scale factor"
print("  OK: Practical scale (128px) present")

# Check Defeat terminal hold
assert 'defeat-terminal' in html_content, "Missing defeat-terminal mode"
assert 'TERMINAL HOLD' in html_content, "Missing TERMINAL HOLD label"
print("  OK: Defeat terminal hold present")

# Check separate Sword and Axe
assert 'value="Sword"' in html_content, "Missing Sword action option"
assert 'value="Axe"' in html_content, "Missing Axe action option"
print("  OK: Separate Sword and Axe options present")

# Check PENDING_CREATOR and statuses. While known-bad cells exist the package
# displays ARTISTIC_REVISION_REQUIRED; technical results remain separate build
# facts (counts), not a whole-package taxonomy label.
assert 'PENDING_CREATOR' in html_content, "Missing PENDING_CREATOR status"
assert expected_package_status in html_content, "Missing manifest-derived package status"
assert 'Validação técnica' in html_content, "Missing technical validation facts line"
assert 'VISUAL_REVIEW_REQUIRED' in html_content, "Missing VISUAL_REVIEW_REQUIRED contract reference"
catalogo = json.loads((review_dir / 'catalogo.json').read_text(encoding='utf-8-sig'))
assert catalogo['technicalStatus'] == 'TECHNICALLY_COMPLETE', "catalogo technicalStatus diverged"
assert catalogo['artisticStatus'] == expected_package_status, "catalogo artisticStatus diverged from manifest"
assert catalogo['packageStatus'] == expected_package_status, "catalogo packageStatus diverged"
assert len(catalogo['knownBadCells']) == len(exp_revision) + exp_production_count, "catalogo knownBadCells diverged from manifest"
assert len(catalogo['affectedCells']) == len(exp_affected), "catalogo affectedCells diverged from manifest"
print(f"  OK: PENDING_CREATOR + {expected_package_status} + technical facts (catalogo derived)")

# Check pending cell alert mechanism
assert 'id="pending-alert"' in html_content, "Missing #pending-alert element"
assert 'updatePendingAlert' in html_content, "Missing updatePendingAlert JS function"
print("  OK: Pending cell alert mechanism present")

print("\nALL AUTOMATED REVIEW VALIDATIONS PASSED SUCCESSFULLY (28/28 cells, 0 404s, manifest-derived)!")
