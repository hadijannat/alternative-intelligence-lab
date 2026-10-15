import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

base = Path(__file__).resolve().parent
raw = base / 'raw'
raw.mkdir(exist_ok=True)
assets = (
    ('HMo2O7.xyz', 'https://iochem-bd.iciq.es/browse/cml2xyz?id=28991&mode=single_xyz', 334,
     '3133155e610321f92d1fe9735baa0f6192243aece1db91f90a8ab90f62b6f2f2'),
    ('HMo2O7.in', 'https://iochem-bd.iciq.es/browse/bitstream/100/28778/3/Mo2O7-1H.in', 1546,
     '68d8fc04c461636ca17441d89bef1a9618a079244af5d7677e13193cdd0ff922'),
    ('item.html', 'https://iochem-bd.iciq.es/browse/handle/100/28778', None, None),
)
receipt = {'observed_at_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'outputs_or_energies_requested': False, 'scientific_operators': 0, 'assets': []}
target = base / 'acquisition.json'
if target.exists() or any((raw / name).exists() for name, *_ in assets):
    raise FileExistsError('Acquisition already exists; do not overwrite it')
try:
    for name, url, expected_size, expected_sha in assets:
        row = {'path': 'raw/' + name, 'url': url}
        receipt['assets'].append(row)
        request = urllib.request.Request(url, headers={'User-Agent': 'Research source provenance audit'})
        with urllib.request.urlopen(request, timeout=45) as response:
            data = response.read(1_000_001)
            row.update(http_status=response.status, final_url=response.geturl())
        if len(data) > 1_000_000:
            raise ValueError('Unexpected source size')
        row.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        if expected_size is not None and (len(data) != expected_size or row['sha256'] != expected_sha):
            raise ValueError('Source differs from independently selected artifact: ' + name)
        (raw / name).write_bytes(data)
        row['status'] = 'ACQUIRED'
except Exception as error:
    receipt['error'] = type(error).__name__ + ': ' + str(error)
    raise
finally:
    target.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
