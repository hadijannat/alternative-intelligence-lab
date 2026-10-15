"""Additive audit of authored GUI connectivity; original geometry result preserved."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
from analysis import BASE,atom,audit,graph,compare,CUTOFFS


def block(text,name):
    match=re.search(r'^\s*'+name+r'\s*\n(.*?)^\s*End\s*$',text,re.M|re.S|re.I)
    if match is None:raise ValueError('Missing or unterminated '+name)
    return match.group(1)


def parse(text):
    atoms=[];ids=set()
    for line in block(text,'Atoms').splitlines():
        f=line.split()
        if not f:continue
        if len(f)<5 or f[0] in ids:raise ValueError('Invalid atom declaration')
        int(f[0]);ids.add(f[0]);atoms.append(atom('a'+f[0],f[1],f[2:5]))
    bonds=[];bond_ids=set();pairs=set()
    for line in block(text,'GUIBonds').splitlines():
        f=line.split()
        if not f:continue
        if len(f)!=4:raise ValueError('Invalid bond declaration')
        identifier,left,right,order=f
        int(identifier);pair=tuple(sorted((left,right)));value=float(order)
        if (identifier in bond_ids or pair in pairs or left==right or left not in ids or right not in ids or not math.isfinite(value) or value<=0):
            raise ValueError('Duplicate/dangling/self/nonfinite/invalid bond')
        bond_ids.add(identifier);pairs.add(pair)
        bonds.append({'id':identifier,'left':'a'+left,'right':'a'+right,'declared_order':value})
    if not atoms or not bonds:raise ValueError('Empty atom/bond block')
    return atoms,bonds


def main():
    source=BASE.parent/'published-parent/Mo36O128-32H.in'
    atoms,bonds=parse(source.read_text());lookup={a['id']:a for a in atoms}
    hcounts={a['id']:0 for a in atoms if a['element']=='O'}
    hlinks={a['id']:[] for a in atoms if a['element']=='H'}
    typecounts=Counter();declared_mo_o={};other=[]
    for b in bonds:
        a,c=lookup[b['left']],lookup[b['right']]
        typ='-'.join(sorted((a['element'],c['element'])));typecounts[typ]+=1
        if typ=='H-O':
            h,o=(a,c) if a['element']=='H' else (c,a)
            hlinks[h['id']].append(o['id']);hcounts[o['id']]+=1
        if typ=='Mo-O':
            key=tuple(sorted((a['id'],c['id'])))
            declared_mo_o[key]={**b,'distance_A':math.dist(a['xyz'],c['xyz'])}
        elif typ!='H-O':other.append(b)
    geom=audit(atoms,2.6)
    assignment_differences=[{'H':r['H'],'declared_Os':hlinks[r['H']],'nearest_O':r['nearest_O'],'nearest_assigned':r['assigned']} for r in geom['H_assignments'] if hlinks[r['H']]!=([r['nearest_O']] if r['assigned'] else [])]
    heavy=[a for a in atoms if a['element']!='H'];index={a['id']:i for i,a in enumerate(heavy)}
    adj=[set() for a in heavy]
    for left,right in declared_mo_o:
        i,j=index[left],index[right];adj[i].add(j);adj[j].add(i)
    p0path=BASE.parent/'parent-inputs/P0_A.xyz'
    p0=[atom('p'+str(i+1),f[0],f[1:]) for i,line in enumerate(p0path.read_text().splitlines()[2:]) if (f:=line.split())]
    comparisons=[]
    for cutoff in CUTOFFS:
        gh,ga=graph(atoms,cutoff)
        geometric={tuple(sorted((gh[i]['id'],gh[j]['id']))) for i,near in enumerate(ga) for j in near if i<j}
        declared=set(declared_mo_o)
        comparisons.append({'cutoff_A':cutoff,'declared_MoO_edge_count':len(declared),'geometric_MoO_edge_count':len(geometric),'intersection':len(declared&geometric),'declared_not_geometric':[declared_mo_o[k] for k in sorted(declared-geometric)],'geometric_not_declared':[{'atoms':list(k),'distance_A':math.dist(lookup[k[0]]['xyz'],lookup[k[1]]['xyz'])} for k in sorted(geometric-declared)],'declared_vs_P0_heavy_comparison':compare((heavy,adj),graph(p0,cutoff))})
    sources=[source,p0path,BASE/'PROTOCOL.md',BASE/'PROTOCOL-v1.md',BASE/'result-v1.json']
    result={'status':'AUTHORED_CONNECTIVITY_AUDIT_ONLY','source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'atom_count':len(atoms),'bond_count':len(bonds),'bond_type_counts':dict(typecounts),'declared_bonds':bonds,'declared_H_neighbors':hlinks,'O_declared_H_counts':hcounts,'O_count_by_declared_H_count':dict(Counter(hcounts.values())),'declared_HO_vs_nearest_O_differences':assignment_differences,'other_declared_bond_types':other,'comparisons':comparisons,'SCFs_launched':0,'limits':['GUIBonds is authored computational connectivity metadata, not experimental bond proof','Incomplete geometric/declaration agreement must not be silently repaired','Matching local graph invariants would not prove isomorphism','No electronic-state or reaction-pathway inference']}
    (BASE/'guibonds-result.json').write_text(json.dumps(result,indent=2)+'\n')
    print('DECLARED bonds',len(bonds),'types',dict(typecounts),'OHcounts',dict(Counter(hcounts.values())))
    print('HO nearest assignment differences',assignment_differences)
    for c in comparisons:
        print('CUTOFF',c['cutoff_A'],'declared',c['declared_MoO_edge_count'],'geometric',c['geometric_MoO_edge_count'],'intersection',c['intersection'],'declared_only',len(c['declared_not_geometric']),'geometry_only',len(c['geometric_not_declared']),'vsP0',c['declared_vs_P0_heavy_comparison']['status'])
        print('DECLARED_ONLY',c['declared_not_geometric'])

if __name__=='__main__':main()
