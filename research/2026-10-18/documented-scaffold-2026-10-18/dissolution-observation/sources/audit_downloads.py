from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
receipt = json.loads((ROOT / 'receipt.json').read_text())
inventory = []
for record in receipt['requests']:
    if 'error' in record:
        continue
    path = ROOT / record['name']
    body = path.read_bytes()
    assert len(body) == record['bytes'], path
    assert hashlib.sha256(body).hexdigest() == record['sha256'], path
    kind = ('pdf' if body.startswith(b'%PDF-') else
            'zip_or_docx' if body.startswith(b'PK\x03\x04') else
            'html' if body.lstrip().lower().startswith((b'<!doctype html', b'<html')) else
            'json' if body.lstrip().startswith((b'{', b'[')) else 'other')
    inventory.append({'path': path.name, 'status': record['status'], 'kind': kind,
                      'bytes': len(body), 'sha256': record['sha256']})
main = json.loads((ROOT / 'crossref.json').read_text())['message']
si = json.loads((ROOT / 'crossref-si.json').read_text())['message']
assert main['DOI'] == '10.1021/acscatal.6c01228'
assert si['DOI'] == '10.1021/acscatal.6c01228.s001'
assert 'systematic study on fe and ni dissolution' in main['title'][0].lower()
assert si['resource']['primary']['URL'].endswith('/cs6c01228_si_001.pdf')
indexed = json.loads((ROOT / 'publisher-indexed-methods.json').read_text())
assert isinstance(indexed, str)
assert '50 mL' in indexed
assert '3.2 μL' in indexed
(ROOT / 'publisher-indexed-methods.txt').write_text(indexed)
result = {'receipt_hashes_valid': True, 'metadata_identity_valid': True,
          'source_class': 'direct-route failure bodies and metadata; browser-acquired native main PDF and SI DOCX',
          'direct_route_native_article_or_si_files_acquired': sum(row['kind'] in ('pdf', 'zip_or_docx') and row['status'] == 200 for row in inventory),
          'inventory': inventory,
          'indexed_methods_sha256': hashlib.sha256((ROOT / 'publisher-indexed-methods.json').read_bytes()).hexdigest()}
assert result['direct_route_native_article_or_si_files_acquired'] == 0
browser_files = []
for filename in ('browser-main-receipt.json', 'browser-si-receipt.json'):
    record = json.loads((ROOT / filename).read_text())
    path = ROOT / record['copied_native_file']
    body = path.read_bytes()
    assert len(body) == record['bytes'], path
    assert hashlib.sha256(body).hexdigest() == record['sha256'], path
    assert body == Path(record['browser_download']).read_bytes(), path
    browser_files.append({'path': path.name, 'bytes': len(body), 'sha256': record['sha256']})
result['browser_files'] = browser_files
result['native_article_or_si_files_acquired'] = len(browser_files)
assert result['native_article_or_si_files_acquired'] == 2
(ROOT / 'acquisition-checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k:v for k,v in result.items() if k != 'inventory'}, indent=2))
