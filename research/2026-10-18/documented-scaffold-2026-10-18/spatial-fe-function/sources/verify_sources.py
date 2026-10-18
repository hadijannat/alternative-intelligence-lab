from pathlib import Path
import hashlib
import json
import fitz

root = Path(__file__).resolve().parent
metadata = json.loads((root / 'figshare-28718969.json').read_text())
item = metadata['files'][0]
native = root / item['name']
data = native.read_bytes()
doc = fitz.open(native)
checks = {
    'resource_doi_exact': metadata['resource_doi'] == '10.1021/jacs.5c00438',
    'si_doi_exact': metadata['doi'] == '10.1021/jacs.5c00438.s001',
    'pdf_magic': data.startswith(b'%PDF'),
    'size_match': len(data) == item['size'],
    'md5_match': hashlib.md5(data).hexdigest() == item['computed_md5'],
    'pages_35': len(doc) == 35,
    'one_advertised_file': len(metadata['files']) == 1,
    'no_embedded_files': not doc.embfile_names(),
    'extracted_text_nonempty': (root / (item['name'] + '.txt')).stat().st_size > 0,
}
for page in [2, 3, 4]:
    doc[page - 1].get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(root / f'si-methods-page-{page}.png')
checks['methods_renders_nonempty'] = all((root / f'si-methods-page-{p}.png').stat().st_size > 0 for p in [2,3,4])
output = {'checks': checks, 'all_pass': all(checks.values()), 'native_sha256': hashlib.sha256(data).hexdigest(),
          'scope': 'Acquisition identity/integrity, not scientific validation. No response points extracted.'}
(root / 'verification.json').write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps(output, indent=2))
assert output['all_pass']
