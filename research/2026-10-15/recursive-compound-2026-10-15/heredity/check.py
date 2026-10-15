"""Extract published tables and test explicitly restricted accounting rivals."""
from pathlib import Path
from fractions import Fraction as Q
import csv, hashlib, json, xml.etree.ElementTree as ET

def founder_contribution(F, M, q_seed, q_product, *, mass_unit='g', capacity_unit='cm3/g'):
    if mass_unit != 'g' or capacity_unit != 'cm3/g':
        raise ValueError('Expected masses in g and specific capacities in cm3/g')
    if any(not isinstance(value, Q) for value in (F, M, q_seed, q_product)):
        raise TypeError('Expected exact Fraction values')
    if M <= 0 or not 0 <= F <= M or q_seed < 0 or q_product <= 0:
        raise ValueError('Invalid mass or capacity domain')
    return F*q_seed/(M*q_product)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = HERE / '.omo/evidence'
OUT.mkdir(parents=True, exist_ok=True)
xml_path = HERE / 'raw/cha-source.xml'
r = ET.parse(xml_path).getroot()
assert any('10.1039/c9ra10825d' in ''.join(x.itertext()).lower() for x in r.iter('article-id'))
table = r.find('.//table-wrap[@id="tab1"]')
rows = [[ ''.join(c.itertext()).strip() for c in row.findall('td')] for row in table.findall('.//tbody/tr')]
assert len(rows) == 8 and rows[-1] == ['24', '530', '434', '0.24']
assert rows[3] == ['6', '203', '149', '0.104']
with (HERE/'cha-texture.csv').open('w') as f:
    writer=csv.writer(f); writer.writerow(['hours','BET_m2_g','micropore_area_m2_g','micropore_volume_cm3_g']); writer.writerows(rows)
seed_paragraphs = [''.join(p.itertext()) for p in r.iter('p') if '0.001' in ''.join(p.itertext()) and 'seeds' in ''.join(p.itertext())]
assert len(seed_paragraphs) == 1 and 'K+' in seed_paragraphs[0]
(HERE/'raw/cha-seed-capacity.txt').write_text(seed_paragraphs[0]+'\n')
# shortcut: seed capacity is an approximate reported point value, replace with calibrated intervals before empirical exclusion.
seed, endpoint = Q('0.001'), Q(rows[-1][-1])
unchanged_max = founder_contribution(Q(1), Q(1), seed, endpoint)
assert unchanged_max == Q(1,240)
assert 1-unchanged_max == Q(239,240)
# Synthetic controls verify the restricted bound, not laboratory inheritance.
valid_controls = [(Q(0), Q(10), Q(0)), (Q(1), Q(10), Q(1,2400)),
                  (Q(5), Q(10), Q(1,480)), (Q(10), Q(10), Q(1,240))]
for F, M, expected in valid_controls:
    actual = founder_contribution(F, M, seed, endpoint)
    assert actual == expected and actual <= unchanged_max
assert founder_contribution(Q(2), Q(4), Q(0), endpoint) == 0
assert founder_contribution(Q(2), Q(4), Q('0.2'), Q('0.1')) == 1
base = dict(F=Q(1), M=Q(2), q_seed=seed, q_product=endpoint)
invalid_controls = [('negative founder', {'F': Q(-1)}, ValueError),
                    ('founder exceeds product', {'F': Q(3)}, ValueError),
                    ('zero total mass', {'M': Q(0)}, ValueError),
                    ('negative total mass', {'M': Q(-2)}, ValueError),
                    ('negative seed capacity', {'q_seed': Q(-1)}, ValueError),
                    ('zero product capacity', {'q_product': Q(0)}, ValueError),
                    ('negative product capacity', {'q_product': Q(-1)}, ValueError),
                    ('wrong mass unit', {'mass_unit': 'mg'}, ValueError),
                    ('wrong capacity unit', {'capacity_unit': 'm3/kg'}, ValueError),
                    ('unparsed capacity', {'q_seed': '0.001'}, TypeError),
                    ('nonfinite capacity', {'q_product': float('nan')}, TypeError)]
for name, overrides, error in invalid_controls:
    try:
        founder_contribution(**(base | overrides))
    except error:
        pass
    else:
        raise AssertionError(f'{name} silently accepted')
old = ROOT/'noncarbon-discovery-2026-10-15/research/replication/chlorate_trials.csv'
chlorate = list(csv.DictReader(old.open()))
assert len(chlorate)==13
opposite=[]
for row in chlorate:
    mass=Q(row['total_crystal_mass_g']); s=Q(row['seed_similarity_percent'])/100
    assert mass>0 and 0<=s<=1
    opposite.append(mass*(1-s))
assert sum(x>0 for x in opposite)==11
# Source mixing descriptions are inconsistent; these are nominal concentrations, not proton activities.
main_nominal_acid=Q(4)/2
si_nominal_acid=Q('0.06')/2
assert main_nominal_acid/si_nominal_acid == Q(200,3)
sources=[xml_path,old,ROOT/'noncarbon-discovery-2026-10-15/research/pom/raw/miras2020.pdf',ROOT/'noncarbon-discovery-2026-10-15/research/pom/raw/miras2020_si.pdf',ROOT/'noncarbon-discovery-2026-10-15/research/pom/raw/miras2020.txt',ROOT/'noncarbon-discovery-2026-10-15/research/pom/raw/miras2020_si.txt',ROOT/'discovery-loop/experiments/chlorate-founder-mass-bound-v1/report.md']
manifest=[{'path':str(p.relative_to(ROOT)), 'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources]
(HERE/'sources.json').write_text(json.dumps(manifest,indent=2)+'\n')
checks={'status':'PASS_SCOPED_ACCOUNTING_ONLY','invocation':'python3 recursive-compound-2026-10-15/heredity/check.py','scenarios':{'cha_primary_table':{'rows':len(rows),'endpoint_micropore_volume_cm3_g':float(endpoint)},'cha_unchanged_founder_capacity_rival':{'assumptions':['approximately reported seed specific capacity is used as an exact arithmetic point','recovered founder mass F <= final mass M','unchanged original-founder specific capacity','additive mass-weighted accessible micropore capacity'],'capacity_ratio':float(endpoint/seed),'unchanged_founder_max_fraction':float(unchanged_max),'altered_or_new_capacity_min_fraction':float(1-unchanged_max),'exact_min_fraction':str(1-unchanged_max),'empirical_confidence_interval':None,'new_material_inheritance_demonstrated':False,'rival_not_excluded':'Ion exchange can change old founder accessibility; no isotope partition or serial functional assay.'},'chlorate_existing_trials':{'n':13,'positive_opposite_mass_trials':11,'sum_opposite_mass_g':float(sum(opposite)),'single_pass_not_generation_error_probability':True,'founder_bound_measured':False},'pmo12_recipe_discrepancy':{'main_nominal_HClO4_M':float(main_nominal_acid),'si_nominal_HCl_M':float(si_nominal_acid),'ratio':float(main_nominal_acid/si_nominal_acid),'exact_ratio':str(main_nominal_acid/si_nominal_acid),'conditions_identical':False}},'verified_joint_additions':0,'functional_inheritance_verified':False,'intelligent_life_verified':False}
checks['scenarios']['founder_contribution_controls'] = {
    'valid_cases': 6, 'invalid_cases_rejected': [name for name, _, _ in invalid_controls],
    'prior_limitation': 'Previous two literal Fraction identities did not exercise a calculation function; replaced with direct function calls and domain/unit rejection tests.',
    'unit_limit': 'Unit labels are validated; incorrectly labelled physical measurements cannot be detected.'}
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
