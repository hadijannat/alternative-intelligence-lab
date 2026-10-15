"""Archive public primary records and selected numeric supplements; never execute author code."""
import hashlib
import json
from pathlib import Path
import requests
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
records = []


def fetch(name, url, license, expected_sha256=None):
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        path.write_bytes(response.content)
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    if expected_sha256:
        assert sha == expected_sha256, (name, sha, expected_sha256)
    if path.suffix == '.xlsx':
        assert data.startswith(b'PK'), name
    if path.suffix == '.pdf':
        assert data.startswith(b'%PDF'), name
    if path.suffix == '.xml':
        root = ET.fromstring(data)
        path.with_suffix('.txt').write_text('\n'.join(''.join(p.itertext()) for p in root.iter('p')))
    records.append(dict(path=name, url=url, bytes=len(data), sha256=sha,
                        license=license, retrieved_date='2026-10-15'))
    print(name, len(data), flush=True)
    return data


def main():
    for name, pmc in [('ameta2021', 'PMC7870898'), ('mizuuchi2022', 'PMC8933500'), ('lai2021', 'PMC8166191'), ('gianni2026', 'PMC7618777')]:
        fetch(f'{name}/article.xml', f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/fullTextXML',
              'See article permissions in archived XML; source-data licenses are separately recorded.')
    for name, year, number, files in [
        ('ameta2021', 2021, 21000, [(1, 'pdf'), (3, 'xlsx'), (4, 'xlsx')]),
        ('mizuuchi2022', 2022, 29113, [(1, 'pdf'), (4, 'xlsx'), (6, 'xlsx')]),
    ]:
        for n, extension in files:
            filename = f'41467_{year}_{number}_MOESM{n}_ESM.{extension}'
            fetch(f'{name}/{filename}', f'https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-0{str(year)[2:]}-{number}-'+('1' if name=='ameta2021' else 'x')+f'/MediaObjects/{filename}',
                  'CC BY 4.0, subject to any credit-line exceptions in the article.')
    for aid in [12865679, 12867053, 12865646]:
        fetch(f'ameta2021/figshare-{aid}.json', f'https://api.figshare.com/v2/articles/{aid}', 'CC BY 4.0')
    zenodo = json.loads(fetch('gianni2026/zenodo-metadata.json', 'https://zenodo.org/api/records/13891380', 'MIT license as recorded by Zenodo metadata.'))
    for f in zenodo['files']:
        if f['key'] == 'fidelity_zenodo.zip':
            data = fetch('gianni2026/'+f['key'], f['links']['self'], 'MIT license as recorded by Zenodo metadata.')
            assert 'md5:'+hashlib.md5(data).hexdigest() == f['checksum']
    fetch('lai2021/dryad-metadata.json', 'https://datadryad.org/api/v2/datasets/doi%3A10.5068%2FD1PX0K', 'CC0 1.0')
    files = json.loads(fetch('lai2021/dryad-files.json', 'https://datadryad.org/api/v2/versions/120219/files', 'CC0 1.0'))
    for f in files['_embedded']['stash:files']:
        if f['path'].endswith('matlab.zip'):
            url = 'https://datadryad.org'+f['_links']['stash:download']['href']
            try:
                fetch('lai2021/'+f['path'], url, 'CC0 1.0', f['digest'])
            except requests.HTTPError as error:
                records.append(dict(path='lai2021/'+f['path'], url=url,
                                    status='not_downloaded', error=str(error)))
    (ROOT/'manifest.json').write_text(json.dumps(records, indent=2)+'\n')


if __name__ == '__main__':
    try:
        main()
    finally:
        (ROOT/'manifest.json').write_text(json.dumps(records, indent=2)+'\n')
