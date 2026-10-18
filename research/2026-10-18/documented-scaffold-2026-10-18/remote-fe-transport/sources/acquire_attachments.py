from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from urllib.parse import urlparse
from datetime import datetime, timezone
import json
from acquire import ROOT, fetch

class AttachmentLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = set()

    def handle_starttag(self, tag, attrs):
        href = dict(attrs).get('href', '')
        if tag == 'a' and 'media.springernature.com/' in href and '/MediaObjects/' in href:
            self.links.add(href)

parser = AttachmentLinks()
parser.feed((ROOT / 'nature.html').read_text())
assert len(parser.links) == 5
routes = [(PathName, url) for url in sorted(parser.links) for PathName in [urlparse(url).path.rsplit('/',1)[-1]]]
routes.append(('main.pdf', 'https://www.nature.com/articles/s41467-025-60728-y.pdf'))
with ThreadPoolExecutor(max_workers=6) as pool:
    records = list(pool.map(lambda args: fetch(*args), routes))
(ROOT / 'attachment-receipt.json').write_text(json.dumps({'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'requests': records}, indent=2) + '\n')
print(json.dumps([{k:r[k] for k in ('name','status','bytes','error') if k in r} for r in records], indent=2))
