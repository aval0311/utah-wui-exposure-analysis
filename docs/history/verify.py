"""Optional standard-library integrity check; not needed to view the explorer."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
for row in manifest['files']:
    path = (root / row['path']).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('Missing or unsafe file: ' + row['path'])
    if path.stat().st_size != row['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
        raise ValueError('File differs: ' + row['path'])
print(json.dumps({'passed': True, 'version': manifest['version'], 'verified_files': len(manifest['files'])}, indent=2))
