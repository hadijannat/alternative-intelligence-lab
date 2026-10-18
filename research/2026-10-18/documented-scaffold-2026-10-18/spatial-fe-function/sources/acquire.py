from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parent

def fetch(name, url, payload=None):
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}, data=None if payload is None else json.dumps(payload).encode())
    try:
        response = urllib.request.urlopen(request, timeout=45)
    except urllib.error.HTTPError as error:
        response = error
    except Exception as error:
        return {'name': name, 'url': url, 'request_payload': payload, 'error': repr(error)}
    body = response.read()
    (ROOT / name).write_bytes(body)
    return {'name': name, 'url': url, 'resolved_url': response.url, 'request_payload': payload,
            'status': response.code, 'content_type': response.headers.get('Content-Type'),
            'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(), 'md5': hashlib.md5(body).hexdigest()}

if __name__ == '__main__':
    routes = [
        ('acs-doi.html', 'https://pubs.acs.org/doi/10.1021/jacs.5c00438'),
        ('acs-new.html', 'https://pubs.acs.org/jacsat/article/147/16/13502/3771257/Role-of-Site-Specific-Iron-in-Fe-Doped-Nickel'),
        ('crossref.json', 'https://api.crossref.org/works/10.1021/jacs.5c00438'),
        ('crossref-si.json', 'https://api.crossref.org/works/10.1021/jacs.5c00438.s001'),
        ('figshare-resource-search.json', 'https://api.figshare.com/v2/articles/search', {'resource_doi':'10.1021/jacs.5c00438', 'limit':100}),
        ('figshare-si-search.json', 'https://api.figshare.com/v2/articles/search', {'doi':'10.1021/jacs.5c00438.s001', 'limit':100}),
        ('figshare-title-search.json', 'https://api.figshare.com/v2/articles/search', {'search_for':'Role of Site-Specific Iron', 'limit':100}),
    ]
    with ThreadPoolExecutor(max_workers=7) as pool:
        records = list(pool.map(lambda args: fetch(*args), routes))
    (ROOT / 'receipt.json').write_text(json.dumps({'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'requests': records}, indent=2) + '\n')
    print(json.dumps([{k:r[k] for k in ('name','status','bytes','error') if k in r} for r in records], indent=2))
