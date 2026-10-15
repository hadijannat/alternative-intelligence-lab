"""Offline integrity checks and lossless numeric exports; no refitting or author-code execution."""
import csv
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
import openpyxl

ROOT = Path(__file__).resolve().parent


def main():
    checks = []
    for item in json.loads((ROOT/'manifest.json').read_text()):
        if item.get('status') == 'not_downloaded':
            continue
        p = ROOT/item['path']
        assert p.stat().st_size == item['bytes'] > 0
        assert hashlib.sha256(p.read_bytes()).hexdigest() == item['sha256']
        checks.append({'scenario': 'source_bytes_match_manifest', 'path': item['path'], 'pass': True})
    out = ROOT/'normalized'
    out.mkdir(exist_ok=True)
    ameta = openpyxl.load_workbook(ROOT/'ameta2021/41467_2021_21000_MOESM4_ESM.xlsx', read_only=True, data_only=True)
    for sheet, stem in [('Networks (experimental data)', 'ameta_networks_measured'),
                        ('Networks (kinetic model)', 'ameta_networks_author_model'),
                        ('Droplets (node fractions)', 'ameta_droplet_fractions'),
                        ('Droplets (number of UMIs)', 'ameta_droplet_umis')]:
        rows = list(ameta[sheet].values)
        assert len(rows) > 1000 and len(rows[1]) >= 16
        with (out/f'{stem}.csv').open('w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows[1:])
        checks.append({'scenario':'lossless_sheet_export', 'source_sheet':sheet,
                       'data_rows': len(rows)-2, 'path':f'normalized/{stem}.csv', 'pass':True})
    book = openpyxl.load_workbook(ROOT/'mizuuchi2022/41467_2022_29113_MOESM6_ESM.xlsx', read_only=True, data_only=True)
    rows = list(book['Fig. 4'].values)
    normalized = []
    for panel, column in [('c',1), ('d',7), ('e',13)]:
        for rowno, row in enumerate(rows[9:], 10):
            if row[column] is None:
                continue
            for offset, role in [(2, 'RNA1'), (3, 'RNA2')]:
                value = row[column+offset]
                if value is None:
                    continue
                normalized.append([panel,rowno,row[column],row[column+1] or '',role,value,
                                   'numeric' if isinstance(value,(int,float)) else 'source_missingness_label'])
    assert len(normalized) > 100
    with (out/'mizuuchi_clone_function.csv').open('w',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['panel','source_excel_row','RNA1_replicase_donor','RNA2_added_template','measured_RNA','fold_replication','status'])
        writer.writerows(normalized)
    checks.append({'scenario':'replicate_function_export_preserves_missingness',
                   'rows':len(normalized), 'missing_labels':sum(r[-1]!='numeric' for r in normalized),
                   'path':'normalized/mizuuchi_clone_function.csv','pass':True})
    inventory=[]
    with ZipFile(ROOT/'gianni2026/fidelity_zenodo.zip') as archive:
        assert archive.testzip() is None
        for member in archive.infolist():
            if member.filename.endswith('.fasta') and not member.filename.startswith('__MACOSX/'):
                with archive.open(member) as f:
                    headers=sum(line.startswith(b'>') for line in f)
                assert headers > 0
                inventory.append({'archive_member':member.filename,'uncompressed_bytes':member.file_size,'fasta_records':headers})
    (out/'qt45_fidelity_inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
    checks.append({'scenario':'archive_crc_and_fasta_record_inventory','fasta_files':len(inventory),
                   'path':'normalized/qt45_fidelity_inventory.json','pass':True})
    artifacts=[]
    for p in sorted(out.iterdir()):
        artifacts.append({'path':str(p.relative_to(ROOT)), 'bytes':p.stat().st_size,
                          'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    result={'invocation':'python3 rna-mechanism-2026-10-15/sources/inheritance/verify_extract.py',
            'all_pass':all(c['pass'] for c in checks),'checks':checks,'artifacts':artifacts,
            'limits':'Does not re-estimate published kinetics, fidelity, or evolutionary results. No parent-daughter lineage retention dataset identified in these four systems.'}
    (ROOT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'all_pass':result['all_pass'],'checks':len(checks),'artifacts':len(artifacts),'function_rows':len(normalized)}))


if __name__=='__main__':
    main()
