"""Validate the two previously selected primary geometries and scoped ADF metadata."""
from collections import Counter
import hashlib
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

SOURCE = Path(__file__).resolve().parent.parent/'identity/next-step/wv-reference-selection'
CASES = {'WO4': ('W', -2), 'VO4': ('V', -3)}
NS = {'c': 'http://www.xml-cml.org/schema'}
TEMPLATE = '{http://www.xml-cml.org/schema/cmlx}templateRef'


def validate(case, xyz, input_text, output_text):
    metal, charge = CASES[case]
    declarations = re.findall(r'^\s*charge\s+([^\n]+)', input_text, re.I | re.M)
    if declarations != [str(charge)]:
        raise ValueError('Input charge missing, conflicting or wrong')
    root = ET.fromstring(output_text)
    charges = [n.text.strip() for run in root.iter() if run.get(TEMPLATE) == 'adf.runtype'
               for symmetry in run if symmetry.get(TEMPLATE) == 'symmetry'
               for n in symmetry.iter() if n.get('dictRef') == 'a:charge']
    spins = [n.text.strip() for n in root.iter() if n.get('dictRef') == 'cc:spinMolecule']
    if charges != [str(charge)] or spins != ['Restricted']:
        raise ValueError('Scoped output charge or restricted spin missing, conflicting or wrong')
    rows = xyz.splitlines()
    atoms = [(r[0], tuple(map(float, r[1:]))) for line in rows[2:] if (r := line.split())]
    if int(rows[0]) != 5 or len(atoms) != 5 or Counter(a[0] for a in atoms) != Counter({metal: 1, 'O': 4}):
        raise ValueError('Composition differs')
    if any(len(p) != 3 or not all(map(math.isfinite, p)) for _, p in atoms):
        raise ValueError('Invalid coordinates')
    final = [m for f in root.iter() if f.get('dictRef') == 'cc:finalization'
             for m in f if m.tag.endswith('molecule')]
    if len(final) != 1:
        raise ValueError('Ambiguous final geometry')
    expected = [(n.get('elementType'), tuple(float(n.get(k)) for k in ('x3','y3','z3')))
                for n in final[0].iter() if n.tag == '{http://www.xml-cml.org/schema}atom']
    if atoms != expected:
        raise ValueError('XYZ differs from CML final geometry')
    return {'case': case, 'metal': metal, 'charge': charge, 'spin': 0, 'atoms_A': atoms}


def verified_sources(ledger=None):
    ledger = (SOURCE/'SOURCES.md').read_text() if ledger is None else ledger
    pairs = re.findall(r'\| (raw/[^ ]+) \| [^|]+ \| ([0-9a-f]{64}) \|', ledger)
    expected = {f'raw/{case}{suffix}' for case in CASES for suffix in ('.xyz','.in','-output.cml')}
    if len(pairs) != 6 or {name for name, _ in pairs} != expected:
        raise ValueError('Expected exactly six unique primary digest records')
    for filename, digest in pairs:
        if hashlib.sha256((SOURCE/filename).read_bytes()).hexdigest() != digest:
            raise ValueError('Primary source digest mismatch: '+filename)
    if len(re.findall(r'\| raw/', ledger)) != 6:
        raise ValueError('Expected exactly six acquired records')
    return [validate(c, (SOURCE/'raw'/f'{c}.xyz').read_text(),
                     (SOURCE/'raw'/f'{c}.in').read_text(),
                     (SOURCE/'raw'/f'{c}-output.cml').read_text()) for c in CASES]
