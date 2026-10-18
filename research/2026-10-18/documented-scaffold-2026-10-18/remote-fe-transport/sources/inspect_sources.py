from pathlib import Path
import hashlib
import json
import posixpath
import zipfile
import xml.etree.ElementTree as ET
import fitz

ROOT = Path(__file__).resolve().parent
inventory = []
for receipt_name in ('receipt.json', 'attachment-receipt.json'):
    for record in json.loads((ROOT / receipt_name).read_text())['requests']:
        if 'error' in record:
            continue
        path = ROOT / record['name']
        data = path.read_bytes()
        assert len(data) == record['bytes']
        assert hashlib.sha256(data).hexdigest() == record['sha256']
        row = {'name': path.name, 'bytes': len(data), 'sha256': record['sha256'], 'status': record['status']}
        if path.suffix == '.pdf' and data.startswith(b'%PDF-'):
            with fitz.open(path) as document:
                row['pages'] = len(document)
                pdf_text = '\n'.join(f'--- PDF page {i+1} ---\n{page.get_text()}' for i, page in enumerate(document))
                if path.name == 'main.pdf':
                    assert '10.1038/s41467-025-60728-y' in pdf_text
                    figure_pages = [i for i,p in enumerate(document) if 'OER stability performance' in p.get_text()]
                    assert len(figure_pages) == 1
                    document[figure_pages[0]].get_pixmap(matrix=fitz.Matrix(2,2)).save(ROOT / 'main-figure1-page.png')
                elif path.name == '41467_2025_60728_MOESM1_ESM.pdf':
                    assert 'Remote Iron dynamics' in pdf_text and 'Jianxiong Zhao' in pdf_text
                    assert 'Supplementary Fig. 6.' in document[6].get_text()
                    document[6].get_pixmap(matrix=fitz.Matrix(2,2)).save(ROOT / 'si-figure6-control-page.png')
                (ROOT / (path.stem + '.txt')).write_text(pdf_text)
        elif path.suffix in ('.zip', '.xlsx'):
            assert data.startswith(b'PK\x03\x04')
            with zipfile.ZipFile(path) as archive:
                assert archive.testzip() is None
                row['members'] = [{'name': i.filename, 'uncompressed_bytes': i.file_size} for i in archive.infolist()]
        inventory.append(row)
bioc = ET.parse(ROOT / 'bioc.xml')
passages = []
for passage in bioc.findall('.//passage'):
    metadata = {item.get('key'): item.text for item in passage.findall('infon')}
    passages.append({'metadata': metadata, 'text': passage.findtext('text', '')})
assert passages[0]['metadata']['article-id_doi'] == '10.1038/s41467-025-60728-y'
(ROOT / 'main-passages.json').write_text(json.dumps(passages, indent=2) + '\n')
(ROOT / 'methods.txt').write_text('\n\n'.join(p['text'] for p in passages if p['metadata'].get('section_type') == 'METHODS'))
ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main', 'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
with zipfile.ZipFile(ROOT / '41467_2025_60728_MOESM5_ESM.xlsx') as archive:
    strings_root = ET.fromstring(archive.read('xl/sharedStrings.xml'))
    strings = [''.join(node.itertext()) for node in strings_root]
    relationships = ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))
    rels = {node.get('Id'): node.get('Target') for node in relationships}
    workbook = ET.fromstring(archive.read('xl/workbook.xml'))
    sheets = []
    for sheet in workbook.findall('s:sheets/s:sheet', ns):
        target = rels[sheet.get(f'{{{ns["r"]}}}id')]
        target = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
        root = ET.fromstring(archive.read(target))
        header_strings = []
        for row in root.findall('s:sheetData/s:row', ns):
            if int(row.get('r')) > 5:
                continue
            for cell in row.findall('s:c', ns):
                if cell.get('t') == 's':
                    header_strings.append({'cell': cell.get('r'), 'text': strings[int(cell.findtext('s:v', namespaces=ns))]})
                elif cell.get('t') == 'inlineStr':
                    header_strings.append({'cell': cell.get('r'), 'text': ''.join(cell.find('s:is', ns).itertext())})
        sheets.append({'name': sheet.get('name'), 'xml_member': target, 'dimension': root.find('s:dimension', ns).get('ref'), 'first_five_row_text_cells_only': header_strings})
(ROOT / 'workbook-structure.json').write_text(json.dumps(sheets, indent=2) + '\n')
result = {'byte_hashes_valid': True, 'identity_valid': True, 'native_attachments': 5,
          'main_pdf_acquired': True, 'license': passages[0]['metadata']['license'],
          'inventory': inventory, 'workbook_sheet_count': len(sheets),
          'numeric_response_values_output': False}
(ROOT / 'acquisition-checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'hashes_valid': True, 'pdfs': [{k:r[k] for k in ('name','pages')} for r in inventory if 'pages' in r], 'sheets': [{k:s[k] for k in ('name','dimension')} for s in sheets]}, indent=2))
