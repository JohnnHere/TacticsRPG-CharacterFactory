"""Install the creator-downloaded official archive; no credentials are read."""
from pathlib import Path, PurePosixPath
import os, sys, zipfile, json, hashlib, stat

root = Path(__file__).resolve().parents[1]
archive = Path(sys.argv[1]).resolve(strict=True)
extensions = (Path(os.environ['APPDATA']) / 'Aseprite' / 'extensions').resolve()
target = (extensions / 'pixellab').resolve()
assert target.parent == extensions and target.name == 'pixellab'
with zipfile.ZipFile(archive) as z:
    metadata = json.loads(z.read('PixelLab/package.json'))
    assert metadata.get('name') == 'pixellab', 'Unexpected package identity'
    entries = []
    for info in z.infolist():
        relative = PurePosixPath(info.filename)
        assert not relative.is_absolute() and '..' not in relative.parts
        assert relative.parts[0] == 'PixelLab'
        assert not stat.S_ISLNK(info.external_attr >> 16)
        if info.is_dir(): continue
        destination = target.joinpath(*relative.parts[1:]).resolve()
        assert destination.is_relative_to(target)
        entries.append((info, destination))
    assert len(entries) < 5000 and sum(i.file_size for i, _ in entries) < 100_000_000
    # Preflight all conflicts before any write; prior versions are preserved.
    for info, destination in entries:
        if destination.exists():
            assert destination.read_bytes() == z.read(info), 'Existing extension differs: preserve before upgrade'
    for info, destination in entries:
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(z.read(info))
    assert all(destination.read_bytes() == z.read(info) for info, destination in entries)
result = {
    'status': 'INSTALLED_FILES_VERIFIED_UI_AUTH_PENDING', 'date': '2026-10-23',
    'name': metadata['name'], 'version': metadata['version'],
    'archiveFilename': archive.name,
    'archiveSha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
    'source': 'Official PixelLab extension downloaded by creator from their account',
    'documentation': 'https://www.pixellab.ai/docs/installation',
    'directory': '%APPDATA%/Aseprite/extensions/pixellab',
    'filesVerified': len(entries), 'credentialsRead': False,
    'authentication': 'NOT_VERIFIED', 'generation': 'NOT_RUN'
}
(root/'reports').mkdir(exist_ok=True)
(root/'reports/pixellab-extension-install.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
