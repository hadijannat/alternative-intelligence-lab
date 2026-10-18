from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parent

def fetch(name, url):
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(request, timeout=60)
    except urllib.error.HTTPError as error:
        response = error
    except Exception as error:
        return {'name': name, 'url': url, 'error': repr(error)}
    payload = response.read()
    (ROOT / name).write_bytes(payload)
    return {'name': name, 'url': url, 'resolved_url': response.url, 'status': response.code,
            'content_type': response.headers.get('Content-Type'), 'bytes': len(payload),
            'sha256': hashlib.sha256(payload).hexdigest()}

if __name__ == '__main__':
    routes = [
        ('pmc.html', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12216224/'),
        ('oa.xml', 'https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC12216224'),
        ('bioc.xml', 'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC12216224/unicode'),
        ('nature.html', 'https://www.nature.com/articles/s41467-025-60728-y'),
        ('crossref.json', 'https://api.crossref.org/works/10.1038/s41467-025-60728-y'),
    ]
    records = [fetch(*route) for route in routes]
    (ROOT / 'receipt.json').write_text(json.dumps({'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'requests': records}, indent=2) + '\n')
    print(json.dumps([{k:r[k] for k in ('name','status','bytes','error') if k in r} for r in records], indent=2))
