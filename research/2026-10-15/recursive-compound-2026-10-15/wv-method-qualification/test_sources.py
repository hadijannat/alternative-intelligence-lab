import unittest
from sources import CASES, SOURCE, TEMPLATE, validate, verified_sources
import xml.etree.ElementTree as ET


class Sources(unittest.TestCase):
    def test_all_primary_records(self):
        self.assertEqual([m['charge'] for m in verified_sources()],[-2,-3])

    def test_ledger_mutations(self):
        ledger=(SOURCE/'SOURCES.md').read_text()
        rows=ledger.splitlines(); row=next(r for r in rows if r.startswith('| raw/WO4.xyz'))
        invalid=[ledger.replace(row,row[:-3]+'xx |'),ledger.replace('raw/WO4.xyz','raw/VO4.xyz'),
                 ledger.replace(row,''),ledger+'\n'+row]
        for changed in invalid:
            with self.subTest(ledger=changed):
                with self.assertRaises(ValueError): verified_sources(changed)

    def test_source_mutations(self):
        for case, (_, charge) in CASES.items():
            xyz=(SOURCE/'raw'/f'{case}.xyz').read_text()
            inp=(SOURCE/'raw'/f'{case}.in').read_text()
            cml=(SOURCE/'raw'/f'{case}-output.cml').read_text()
            for mutation in ('wrong_input','missing_input','conflicting_input','wrong_output','missing_output',
                             'conflicting_output','wrong_spin','missing_spin','geometry_mismatch','logfile_noise'):
                with self.subTest(case=case,mutation=mutation):
                    root=ET.fromstring(cml); text=inp; geometry=xyz
                    run=next(n for n in root.iter() if n.get(TEMPLATE)=='adf.runtype')
                    sym=next(n for n in run if n.get(TEMPLATE)=='symmetry')
                    q=next(n for n in sym if n.get('dictRef')=='a:charge')
                    spin=next(n for n in root.iter() if n.get('dictRef')=='cc:spinMolecule')
                    if mutation=='wrong_input': text=inp.replace(f'charge {charge}','charge 0')
                    if mutation=='missing_input': text=inp.replace(f'charge {charge}','')
                    if mutation=='conflicting_input': text=inp+'\ncharge 0\n'
                    if mutation=='wrong_output': q.text='0'
                    if mutation=='missing_output': sym.remove(q)
                    if mutation=='conflicting_output': ET.SubElement(sym,q.tag,dict(q.attrib)).text='0'
                    if mutation=='wrong_spin': spin.text='Unrestricted'
                    if mutation=='missing_spin': spin.set('dictRef','missing')
                    if mutation=='geometry_mismatch':
                        rows=xyz.splitlines(); parts=rows[2].split(); parts[1]=str(float(parts[1])+.001)
                        rows[2]=' '.join(parts); geometry='\n'.join(rows)
                    if mutation=='logfile_noise':
                        for n in root.iter():
                            if n.get('dictRef')=='a:charge' and n is not q: n.text='999'
                        self.assertEqual(validate(case,geometry,text,ET.tostring(root))['charge'],charge)
                    else:
                        with self.assertRaises(ValueError): validate(case,geometry,text,ET.tostring(root))


if __name__=='__main__': unittest.main(verbosity=2)
