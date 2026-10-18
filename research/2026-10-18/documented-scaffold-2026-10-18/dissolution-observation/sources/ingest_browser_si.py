from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET
import fitz

ROOT = Path(__file__).resolve().parent
original = Path('/USER_HOME/Downloads/cs-2026-01228g_si_001.docx')
body = original.read_bytes()
assert body.startswith(b'PK\x03\x04')
native = ROOT / original.name
native.write_bytes(body)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(native) as archive:
    assert archive.testzip() is None
    members = archive.namelist()
    document_xml = archive.read('word/document.xml')
    (ROOT / 'supporting-document.xml').write_bytes(document_xml)
    xml = ET.fromstring(document_xml)
    text_tags = {f'{{{ns["w"]}}}t', '{http://schemas.openxmlformats.org/officeDocument/2006/math}t'}
    paragraphs = [''.join(t.text or '' for t in p.iter() if t.tag in text_tags) for p in xml.findall('.//w:p', ns)]
    text = '\n'.join(paragraphs)
    assert 'Setting the record straight' in text or 'Setting the Record Straight' in text
    assert 'Cherevko' in text
    (ROOT / 'supporting-information.txt').write_text(text + '\n')
    math_ns = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}
    equations = xml.findall('.//m:oMath', math_ns)
    equation_audit = []
    for index in (9, 10, 12, 13):
        equation = equations[index]
        (ROOT / f'si-equation-{index:02d}.xml').write_bytes(ET.tostring(equation, encoding='utf-8'))
        fractions = [{'numerator': ''.join(f.find('m:num', math_ns).itertext()),
                      'denominator': ''.join(f.find('m:den', math_ns).itertext())}
                     for f in equation.findall('.//m:f', math_ns)]
        equation_audit.append({'zero_based_omath_index': index, 'linearized_tokens': ''.join(equation.itertext()), 'fractions': fractions})
    assert equation_audit[1]['fractions'] == [{'numerator':'0.059', 'denominator':'3'}]
    (ROOT / 'si-math-structure.json').write_text(json.dumps(equation_audit, indent=2) + '\n')
    tables = [[[''.join(t.text or '' for t in cell.findall('.//w:t', ns)) for cell in row.findall('w:tc', ns)] for row in table.findall('w:tr', ns)] for table in xml.findall('.//w:tbl', ns)]
    (ROOT / 'supporting-tables.json').write_text(json.dumps(tables, indent=2) + '\n')
    media = []
    for name in members:
        if name.startswith('word/media/'):
            data = archive.read(name)
            path = ROOT / 'si-media' / Path(name).name
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(data)
            media.append({'member': name, 'path': str(path.relative_to(ROOT)), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
receipt = {'retrieved_utc': datetime.now(timezone.utc).isoformat(),
           'source': 'Parent root used normal IAB browser on the ACS article and clicked the observed SI Download link',
           'article_url': 'https://pubs.acs.org/accacs/article/16/9/8633/5142681/Setting-the-Record-Straight-A-Systematic-Study-on',
           'observed_si_href': 'https://pubs.acs.org/accacs/article-supplement/5142681/docx/cs-2026-01228g_si_001/',
           'browser_download': str(original), 'copied_native_file': native.name,
           'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(), 'md5': hashlib.md5(body).hexdigest(),
           'original_copy_equal': native.read_bytes() == original.read_bytes(),
           'zip_integrity_valid': True, 'identity_text_valid': True,
           'members': members, 'media': media, 'tables': len(tables),
           'separate_si_license_verified': False}
assert receipt['original_copy_equal']
(ROOT / 'browser-si-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ('members','media')}, indent=2))
original_main = Path('/USER_HOME/Downloads/cs-2026-01228g.pdf')
main_body = original_main.read_bytes()
assert main_body.startswith(b'%PDF-')
main_path = ROOT / original_main.name
main_path.write_bytes(main_body)
with fitz.open(main_path) as document:
    pages = [page.get_text() for page in document]
    main_text = '\n'.join(f'--- PDF page {i+1} ---\n{text}' for i, text in enumerate(pages))
    assert 'Setting the Record Straight' in main_text
    assert '10.1021/acscatal.6c01228' in main_text
    (ROOT / 'main-text.txt').write_text(main_text)
    for i, page in enumerate(document):
        if 'The total electrolyte volume' in page.get_text() or 'three-way valves' in page.get_text():
            page.get_pixmap(matrix=fitz.Matrix(2,2)).save(ROOT / f'main-methods-page-{i+1:02d}.png')
    document[2].get_pixmap(matrix=fitz.Matrix(3,3), clip=fitz.Rect(50, 60, 557, 337)).save(ROOT / 'fig1-methods.png')
    document[4].get_pixmap(matrix=fitz.Matrix(3,3), clip=fitz.Rect(50, 310, 305, 615)).save(ROOT / 'fig6-axis-audit.png')
main_receipt = {'retrieved_utc': datetime.now(timezone.utc).isoformat(),
                'source': 'Parent root clicked observed native PDF anchor in normal IAB browser',
                'observed_href': 'https://pubs.acs.org/accacs/article-pdf/16/9/8633/64857843/cs-2026-01228g.pdf',
                'browser_download': str(original_main), 'copied_native_file': main_path.name,
                'bytes': len(main_body), 'sha256': hashlib.sha256(main_body).hexdigest(),
                'md5': hashlib.md5(main_body).hexdigest(), 'pages': len(pages),
                'original_copy_equal': main_path.read_bytes() == original_main.read_bytes(),
                'identity_text_valid': True}
assert main_receipt['original_copy_equal']
(ROOT / 'browser-main-receipt.json').write_text(json.dumps(main_receipt, indent=2) + '\n')
print(json.dumps(main_receipt, indent=2))
