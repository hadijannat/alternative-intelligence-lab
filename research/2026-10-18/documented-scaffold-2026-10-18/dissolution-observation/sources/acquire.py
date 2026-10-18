from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parent
RECEIPT = ROOT / 'receipt.json'

def fetch(name, url, payload=None):
    headers = {'User-Agent': 'Mozilla/5.0'}
    if payload is not None:
        headers['Content-Type'] = 'application/json'
    request = urllib.request.Request(url, headers=headers, data=None if payload is None else json.dumps(payload).encode())
    try:
        response = urllib.request.urlopen(request, timeout=45)
    except urllib.error.HTTPError as error:
        response = error
    except Exception as error:
        return {'name': name, 'url': url, 'error': repr(error), 'request_payload': payload}
    body = response.read()
    (ROOT / name).write_bytes(body)
    return {'name': name, 'url': url, 'resolved_url': response.url, 'status': response.code,
            'content_type': response.headers.get('Content-Type'), 'bytes': len(body),
            'sha256': hashlib.sha256(body).hexdigest(), 'md5': hashlib.md5(body).hexdigest(),
            'request_payload': payload}

if __name__ == '__main__':
    routes = [
        ('main-new.html', 'https://pubs.acs.org/accacs/article/16/9/8633/5142681/Setting-the-Record-Straight-A-Systematic-Study-on', None),
        ('main-doi.html', 'https://pubs.acs.org/doi/10.1021/acscatal.6c01228', None),
        ('figshare-title-search.json', 'https://api.figshare.com/v2/articles/search', {'search_for': 'Setting the Record Straight', 'limit': 100}),
        ('figshare-doi-search.json', 'https://api.figshare.com/v2/articles/search', {'resource_doi': '10.1021/acscatal.6c01228', 'limit': 100}),
        ('crossref.json', 'https://api.crossref.org/works/10.1021/acscatal.6c01228', None),
        ('main-pdf-response.bin', 'https://pubs.acs.org/accacs/article-pdf/16/9/8633/64857843/cs-2026-01228g.pdf', None),
        ('si-conventional-route-response.bin', 'https://pubs.acs.org/doi/suppl/10.1021/acscatal.6c01228/suppl_file/cs6c01228_si_001.docx', None),
        ('figshare-title-search-specific.json', 'https://api.figshare.com/v2/articles/search', {'search_for': 'Fe and Ni Dissolution', 'limit': 100}),
        ('crossref-si.json', 'https://api.crossref.org/works/10.1021/acscatal.6c01228.s001', None),
        ('juelich-search.html', 'https://publications.fz-juelich.de/search?p=10.1021%2Facscatal.6c01228&of=hb', None),
        ('figshare-exact-title.json', 'https://api.figshare.com/v2/articles/search', {'search_for': '"Setting the Record Straight"', 'limit': 100}),
        ('si-pdf-response.bin', 'https://pubs.acs.org/doi/suppl/10.1021/acscatal.6c01228/suppl_file/cs6c01228_si_001.pdf', None),
        ('si-doi-response.bin', 'https://doi.org/10.1021/acscatal.6c01228.s001', None),
        ('figshare-si-doi.json', 'https://api.figshare.com/v2/articles/search', {'doi': '10.1021/acscatal.6c01228.s001', 'limit': 100}),
        ('juser-search.json', 'https://juser.fz-juelich.de/search?p=acscatal.6c01228&of=recjson', None),
    ]
    records = [fetch(*route) for route in routes]
    RECEIPT.write_text(json.dumps({'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'requests': records}, indent=2) + '\n')
    print(json.dumps([{k: r[k] for k in ('name','status','bytes','error') if k in r} for r in records], indent=2))
