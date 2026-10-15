"""Local source audit only; 1.2 A nearest-O threshold fixed before analysis."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

BASE=Path(__file__).resolve().parent
NS={'c':'http://www.xml-cml.org/schema'}
TEMPLATE='{http://www.xml-cml.org/schema/cmlx}templateRef'
OH_THRESHOLD_A=1.2


def finite(value):
    x=float(value)
    if not math.isfinite(x):
        raise ValueError('Nonfinite numeric source')
    return x


def atoms_from_molecule(molecule,expected=None):
    atoms=[{'id':e.get('id'),'element':e.attrib['elementType'],'xyz':[finite(e.attrib[k]) for k in ('x3','y3','z3')]} for e in molecule.findall('./c:atomArray/c:atom',NS)]
    if not atoms or (expected is not None and len(atoms)!=expected):
        raise ValueError('Missing or mismatched atom count')
    if len({a['id'] for a in atoms})!=len(atoms):
        raise ValueError('Duplicate atom identifiers')
    return atoms


def array_values(element):
    values=[finite(x) for x in (element.text or '').split()]
    if int(element.attrib['size'])!=len(values):
        raise ValueError('Declared array size mismatch')
    return values


def walk(root):
    def visit(e,path):
        label=e.tag.split('}')[-1]+':'+(e.get('dictRef') or e.get(TEMPLATE) or e.get('id') or '')
        current=path+'/'+label
        yield e,current
        for child in e:
            yield from visit(child,current)
    yield from visit(root,'')


def frequencies(root,natoms):
    records=[]; replacements=[]
    for e,path in walk(root):
        if e.tag.endswith('array') and e.get('dictRef') in ('cc:frequency','a:oldfreq','a:newfreq'):
            values=array_values(e)
            records.append({'path':path,'dictRef':e.get('dictRef'),'units':e.get('units'),'values':values,'count':len(values),'negative':sum(v<0 for v in values),'below_minus20':sum(v<-20 for v in values),'minimum':min(values) if values else None,'full_3N_minus6_count':len(values)==3*natoms-6})
        if e.get(TEMPLATE)=='scanfreq' and e.tag.endswith('list'):
            old=e.find("c:array[@dictRef='a:oldfreq']",NS);new=e.find("c:array[@dictRef='a:newfreq']",NS)
            if old is None or new is None:
                raise ValueError('Incomplete ScanFreq pair')
            a,b=array_values(old),array_values(new)
            if len(a)!=len(b):
                raise ValueError('ScanFreq lengths differ')
            replacements.append({'path':path,'old_units':old.get('units'),'new_units':new.get('units'),'old':a,'new':b})
    candidates=[r for r in records if r['dictRef']=='cc:frequency' and r['units']=='nonsi:cm-1' and r['full_3N_minus6_count']]
    reconciliation={'status':'UNRESOLVED','final_corrected_spectrum_explicitly_present':False,'minimum_confirmed':False,'reason':'Need one full unit-labelled spectrum and uniquely matchable corrections'}
    if len(candidates)==1:
        values=candidates[0]['values'].copy(); matches=[];ambiguous=[];used=set()
        for block in replacements:
            for old,new in zip(block['old'],block['new']):
                indices=[i for i,v in enumerate(candidates[0]['values']) if abs(v-old)<=.000501 and i not in used]
                if len(indices)!=1 or block['old_units']!='nonsi:cm-1' or block['new_units']!='nonsi:cm-1':
                    ambiguous.append({'old':old,'new':new,'indices':indices});continue
                index=indices[0];used.add(index);values[index]=new
                matches.append({'index_1based':index+1,'old_rounded':old,'source_value':candidates[0]['values'][index],'new':new})
        reconciliation.update(status='CONDITIONAL_REPLACEMENT_ACCOUNTING' if not ambiguous else 'UNRESOLVED',matches=matches,ambiguous=ambiguous,conditional_values=values,conditional_negative_count=sum(v<0 for v in values),conditional_below_minus20=sum(v<-20 for v in values),conditional_minimum=min(values),reason='Apply only explicit old/new entries matched within half a printed 0.001 cm-1 unit. Remaining entries are not independently confirmed final modes; no final corrected full spectrum is declared.')
    return {'records':records,'ScanFreq_blocks':replacements,'reconciliation':reconciliation,'interpretation':'Negative signed wavenumbers are source values, conventionally used for imaginary modes; CML units cm-1 do not alone establish the sign convention or a final corrected Hessian.'}


def distance(a,b):
    return math.dist(a['xyz'],b['xyz'])


def topology(atoms):
    oxy=[a for a in atoms if a['element']=='O']; mo=[a for a in atoms if a['element']=='Mo']
    counts={a['id']:0 for a in oxy}; rows=[]
    for h in (a for a in atoms if a['element']=='H'):
        nearest=sorted((distance(h,o),o['id']) for o in oxy)
        d,oid=nearest[0]
        if d<=OH_THRESHOLD_A:counts[oid]+=1
        rows.append({'H':h['id'],'nearest_O':oid,'distance_A':d,'next_nearest_O_distance_A':nearest[1][0],'within_threshold':d<=OH_THRESHOLD_A,'nearest_Mo_distance_A':min(distance(h,m) for m in mo)})
    return {'element_counts':dict(Counter(a['element'] for a in atoms)),'threshold_A':OH_THRESHOLD_A,'H_contacts':rows,'H_counts_per_O':counts,'O_count_by_H_count':dict(Counter(counts.values())),'aqua_like_O_2H':sum(v==2 for v in counts.values()),'hydroxo_like_O_1H':sum(v==1 for v in counts.values()),'H_outside_threshold':sum(not r['within_threshold'] for r in rows),'minimum_H_Mo_A':min(r['nearest_Mo_distance_A'] for r in rows),'bond_proof':False}


def heavy_spectra(a,b):
    def spectra(atoms):
        out={}
        heavy=[x for x in atoms if x['element']!='H']
        for i,x in enumerate(heavy):
            for y in heavy[i+1:]:
                key='-'.join(sorted((x['element'],y['element'])))
                out.setdefault(key,[]).append(distance(x,y))
        return {k:sorted(v) for k,v in out.items()}
    x,y=spectra(a),spectra(b);out={}
    for key in x:
        if key not in y or len(x[key])!=len(y[key]):raise ValueError('Heavy composition mismatch')
        differences=[p-q for p,q in zip(x[key],y[key])]
        out[key]={'pair_count':len(differences),'sorted_distance_RMS_difference_A':math.sqrt(sum(d*d for d in differences)/len(differences)),'max_abs_sorted_distance_difference_A':max(map(abs,differences))}
    return {'element_pair_spectra':out,'atom_mapping_performed':False,'interpretation':'Rigid-motion and permutation invariant distribution comparison; not an atom displacement RMSD and cannot resolve site mapping.'}


def main():
    input_path=BASE/'Mo36O128-32H.in';text=input_path.read_text()
    block=re.search(r'^\s*Atoms\s*\n(.*?)^\s*End\s*$',text,re.M|re.S).group(1)
    input_atoms=[]
    for line in block.splitlines():
        fields=line.split()
        input_atoms.append({'id':'a'+fields[0],'element':fields[1],'xyz':[finite(v) for v in fields[2:5]]})
    geo_root=ET.parse(BASE/'geometry.cml').getroot();out_root=ET.parse(BASE/'output.cml').getroot()
    geometry=atoms_from_molecule(geo_root.find('.//c:molecule',NS),len(input_atoms))
    molecule_records=[];output_atoms=None
    for e,path in walk(out_root):
        if e.tag.endswith('molecule'):
            atoms=atoms_from_molecule(e,len(input_atoms))
            molecule_records.append({'path':path,'id':e.get('id'),'atom_count':len(atoms)})
            if 'cc:initialization' in path:output_atoms=atoms
    if output_atoms is None:raise ValueError('No declared initialization molecule')
    def same_order_diff(a,b):
        if [(x['id'],x['element']) for x in a]!=[(x['id'],x['element']) for x in b]:return None
        return max(distance(x,y) for x,y in zip(a,b))
    p0path=BASE.parent/'parent-inputs/P0_A.xyz';p0lines=p0path.read_text().splitlines()
    p0=[{'id':'p'+str(i+1),'element':f[0],'xyz':[finite(v) for v in f[1:]]} for i,line in enumerate(p0lines[2:]) if (f:=line.split())]
    if len(p0)!=int(p0lines[0]):raise ValueError('P0 XYZ count mismatch')
    scalars=[];thermo=[]
    chosen={'cc:program','cc:programVersion','cc:runtype','cc:method','cc:functional','cc:basis','a:charge','a:rsol','a:epsl','a:cosmomethod','a:coretreat','cc:spinMolecule','cc:zeropoint','cc:total'}
    for e,path in walk(out_root):
        if e.tag.endswith('scalar'):
            record={'path':path,'dictRef':e.get('dictRef'),'units':e.get('units'),'text':e.text}
            if 'thermochemistry' in path:thermo.append(record)
            if e.get('dictRef') in chosen or any('/parameter:'+x+'/' in path for x in chosen):scalars.append(record)
    frequency=frequencies(out_root,len(geometry))
    result={'status':'SOURCE_AUDIT_COMPLETE_WITH_LIMITS','SCFs_launched':0,'OH_threshold_preregistered_A':OH_THRESHOLD_A,'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [input_path,BASE/'geometry.cml',BASE/'output.cml',BASE/'item.html',BASE/'PROTOCOL.md',p0path]},'input':{'atom_count':len(input_atoms),'elements':dict(Counter(a['element'] for a in input_atoms)),'charge':int(re.search(r'^\s*Charge\s+(-?\d+)',text,re.M).group(1)),'method_lines':[line.strip() for line in text.splitlines() if re.match(r'\s*(Type |Core |GGA |Relativistic |Charge |Solv |Surf |Charged |C-Mat |SCF |CSMRSP|AnalyticalFreq|NumericalQuality|ScanFreq)',line)]},'geometry':{'output_molecules':molecule_records,'geometry_CML_vs_output_initial_max_same_order_distance':same_order_diff(geometry,output_atoms),'input_vs_output_initial_max_same_order_distance':same_order_diff(input_atoms,output_atoms),'finalization_molecule_present':any('cc:finalization' in r['path'] for r in molecule_records),'coordinate_units_note':'CML x3/y3/z3 have no explicit units attribute; contact distances use Angstrom interpretation of supplied molecular coordinates, consistent with input and solvent radius units. No conversion or coordinate repair.','geometry_role':'Matches output initialization, not independently declared optimized/final geometry'},'output_properties':scalars,'thermochemistry_all_contexts':thermo,'frequencies':frequency,'contacts':{'published_geometry':topology(geometry),'published_input':topology(input_atoms),'P0_A':topology(p0)},'heavy_distance_comparison':heavy_spectra(geometry,p0),'completion':{'finalization_module_present':out_root.find(".//c:module[@dictRef='cc:finalization']",NS) is not None,'explicit_SCF_convergence_flag_found':any('converg' in e.get('dictRef','').lower() for e in out_root.iter()),'geometry_optimization_confirmed':False,'interpretation':'Parsed finalization properties do not independently establish normal executable termination or geometry convergence.'},'energy_comparison':'ADF cc:total in bonding/decomposition context is not the PySCF total energy; no cross-code energy subtraction performed.','physical_admission':False,'held_out_validation':False}
    (BASE/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','input','geometry','completion')},indent=2))
    for name,t in result['contacts'].items():print('CONTACT',name,{k:t[k] for k in ('aqua_like_O_2H','hydroxo_like_O_1H','H_outside_threshold','minimum_H_Mo_A','O_count_by_H_count')})
    print('FREQUENCIES',[(r['dictRef'],r['count'],r['negative'],r['minimum']) for r in frequency['records']])
    print('RECONCILIATION',{k:v for k,v in frequency['reconciliation'].items() if k not in ('conditional_values','matches')})
    print('HEAVY',json.dumps(result['heavy_distance_comparison']))

if __name__=='__main__':main()
