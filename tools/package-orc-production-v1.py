"""Archive only the selected approved exports; verify every archived byte."""
from pathlib import Path
import hashlib,json,zipfile,html,os
root=Path('.').resolve()
report=json.loads((root/'reports/orc-actions-export-v1.json').read_text(encoding='utf-8'))
inventory=[]
for p in report['packages']:
    folder=root/p['path']
    hashes=json.loads((folder/'package-hashes.json').read_text(encoding='utf-8'))
    actual={f.relative_to(folder).as_posix() for f in folder.rglob('*') if f.is_file()}
    assert actual=={f['path'] for f in hashes}|{'package-hashes.json'}
    for f in hashes:assert hashlib.sha256((folder/f['path']).read_bytes()).hexdigest()==f['sha256']
    for f in sorted(folder.rglob('*')):
        if f.is_file():inventory.append((f,p['id']+'/'+f.relative_to(folder).as_posix(),hashlib.sha256(f.read_bytes()).hexdigest()))
build=hashlib.sha256(json.dumps([(name,sha) for _,name,sha in inventory],separators=(',',':')).encode()).hexdigest()[:16]
dest=root/'dist/orc-basic-production-v1'/build;dest.mkdir(parents=True,exist_ok=True)
archive=dest/'orcs-production-v1.zip'
readme='''# Orc production assets — approved local export

Eight outfits of the same Orc: Warrior, Squire, Archer, Apprentice Mage, Acolyte, Rogue, Scout and Brawler.
896 native RGBA PNGs and216 selected .aseprite files. Includes four-view Idle/Walk/legacy Attack/Hit/Defeat and explicit basic.unarmed punches. Warrior/Brawler reuse their existing Attack frames. Hit is shared by armed/unarmed body reactions; original casting/Job gestures remain intact.

Each outfit folder contains Assets/Resources/Characters/<id>, factory-manifest.json, factory-actions.json, Source/, source-manifest.json and package-hashes.json. MANIFEST.json selects the approved builds. PNG dimensions128x128, ground126, PPU100, binary transparency; no mirroring.

This is a local production export. The current Unity runtime does not consume factory-actions.json and only knows WarriorPilot. No integration was executed. Independent weapons/projectiles/VFX, sockets/occlusion and action/event loading still require implementation and review. Casting gestures are not a complete inventory of all talent abilities. Gameplay unarmed power/range/accuracy remain TBD_CORE. Gate3/PlayMode NOT_RUN.

Do not overwrite existing Unity GUIDs or infer ready weapon bindings from empty hands. See each outfit's ACTIONS.md, EQUIPMENT_AND_ACTIONS.md and INTEGRATION.md.
'''
if not archive.exists():
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        z.writestr('README.md',readme)
        z.writestr('MANIFEST.json',json.dumps(report,indent=2,ensure_ascii=False)+'\n')
        for file,name,_ in inventory:z.write(file,name)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert set(z.namelist())=={name for _,name,_ in inventory}|{'README.md','MANIFEST.json'}
    for _,name,sha in inventory:assert hashlib.sha256(z.read(name)).hexdigest()==sha
    assert z.read('README.md').decode()==readme
    assert json.loads(z.read('MANIFEST.json'))==report
archive_sha=hashlib.sha256(archive.read_bytes()).hexdigest()
result={'path':archive.relative_to(root).as_posix(),'sha256':archive_sha,'bytes':archive.stat().st_size,'build':build,'packageCount':8,'nativePng':896,'editableSources':216,'archiveEntries':len(inventory)+2,'verifiedArchiveFileHashes':len(inventory),'crc':'PASS','unityIntegration':'NOT_RUN','weaponBindingsProven':0}
(dest/'manifest.json').write_text(json.dumps({'archive':result,'packages':report['packages']},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(dest/'README.md').write_text(readme,encoding='utf-8')
rows=[]
for p in report['packages']:
    href=Path(os.path.relpath(root/p['path'],dest)).as_posix()
    rows.append(f'<tr><td>{html.escape(p["job"])}</td><td>{p["nativePng"]}</td><td>{p["editables"]}</td><td><a href="{href}/ACTIONS.md">Pacote</a> · <a href="{href}/Assets/Resources/Characters/{p["id"]}/factory-actions.json">Ações</a></td></tr>')
page='''<!doctype html><html lang="pt-br"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Orcs — assets exportados</title><style>body{font:17px system-ui;max-width:1050px;margin:40px auto;padding:20px;color:#eee;background:#22242b}a{color:#9cf}td,th{padding:12px;text-align:left;border-bottom:1px solid #555}p{line-height:1.6}code{overflow-wrap:anywhere}</style><h1>Orcs — pacotes de produção exportados</h1><p>Oito roupas do mesmo Orc, com896 PNGs e216 arquivos editáveis. Idle, Walk, gesto de ataque/conjuração por classe, Hit e Defeat nas quatro vistas, além do ataque básico desarmado. Arte aprovada pelo criador; hashes dos pacotes e do ZIP verificados.</p><p><a href="orcs-production-v1.zip" download>Baixar ZIP completo</a> · <a href="manifest.json">Manifesto e SHA256</a> · <a href="../../../characters/review-orc-actions-complete-v1.html">Prévia das animações</a></p><p>Hit é a reação corporal compartilhada por armado/desarmado. O soco básico sem arma tem clipe próprio; conjurações continuam separadas. Armas, projéteis, efeitos e encaixes ainda pendentes. O runtime Unity exige extensão; integração e PlayMode não foram executados.</p><table><tr><th>Classe</th><th>PNGs</th><th>Editáveis</th><th>Arquivos</th></tr>'''+''.join(rows)+f'</table><p>SHA256 do ZIP: <code>{archive_sha}</code></p></html>'
(dest/'index.html').write_text(page,encoding='utf-8')
(root/'reports/orc-production-archive-v1.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
