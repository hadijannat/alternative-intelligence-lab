from datetime import datetime, timezone
import hashlib
import json
import fitz
from acquire import ROOT, fetch

records = [fetch('figshare-28718969.json', 'https://api.figshare.com/v2/articles/28718969')]
metadata = json.loads((ROOT / 'figshare-28718969.json').read_text())
for item in metadata['files']:
    record = fetch(item['name'], item['download_url'])
    record['expected_md5'] = item.get('computed_md5')
    record['expected_size'] = item.get('size')
    record['matches_md5'] = record.get('md5') == item.get('computed_md5')
    record['matches_size'] = record.get('bytes') == item.get('size')
    records.append(record)
    data = (ROOT / item['name']).read_bytes()
    if data.startswith(b'%PDF'):
        doc = fitz.open(stream=data, filetype='pdf')
        record['pdf_pages'] = len(doc)
        text = '\n'.join(f'\n--- PDF PAGE {i+1} ---\n' + page.get_text() for i, page in enumerate(doc))
        (ROOT / (item['name'] + '.txt')).write_text(text)
        record['extraction'] = item['name'] + '.txt'
(ROOT / 'si-receipt.json').write_text(json.dumps({'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'requests': records}, indent=2) + '\n')
print(json.dumps({'license': metadata.get('license'), 'description': metadata.get('description'), 'files': records}, indent=2))
