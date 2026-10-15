"""Bounded geometric contact audit, with no bond or protonation inference."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

BASE=Path(__file__).resolve().parent
CUTOFFS=(2.5,2.6,2.7)
OH=1.2


def atom(identifier,element,xyz):
    xyz=list(map(float,xyz))
    if len(xyz)!=3 or not all(map(math.isfinite,xyz)):raise ValueError('Invalid coordinates')
    return {'id':identifier,'element':element,'xyz':xyz}


def dist(a,b):return math.dist(a['xyz'],b['xyz'])


def graph(atoms,cutoff):
    heavy=[a for a in atoms if a['element']!='H']
    adjacency=[set() for _ in heavy]
    for i,a in enumerate(heavy):
        for j,b in enumerate(heavy[:i]):
            if {a['element'],b['element']}=={'Mo','O'} and dist(a,b)<=cutoff:
                adjacency[i].add(j);adjacency[j].add(i)
    return heavy,adjacency


def compare(g1,g2):
    atoms1,adj1=g1;atoms2,adj2=g2
    nodes=atoms1+atoms2;offset=len(atoms1)
    adj=adj1+[{i+offset for i in neighbours} for neighbours in adj2]
    colors=[a['element'] for a in nodes];history=[]
    for step in range(12):
        signatures=[(colors[i],tuple(sorted(colors[j] for j in neighbours))) for i,neighbours in enumerate(adj)]
        palette={s:str(i) for i,s in enumerate(sorted(set(signatures)))}
        refined=[palette[s] for s in signatures]
        counts1,counts2=Counter(refined[:offset]),Counter(refined[offset:])
        history.append({'round':step+1,'colors':len(palette),'histogram1':dict(counts1),'histogram2':dict(counts2),'equal':counts1==counts2})
        colors=refined
        if counts1!=counts2:
            return {'status':'DISTINCT_CUTOFF_GRAPHS','proof':'Element-colored refinement histograms differ','rounds':history,'mapping':None}
    counts=Counter(colors[:offset])
    if all(v==1 for v in counts.values()):
        lookup={c:i for i,c in enumerate(colors[offset:])}
        mapping={i:lookup[c] for i,c in enumerate(colors[:offset])}
        if all({mapping[j] for j in adj1[i]}==adj2[mapping[i]] for i in mapping):
            return {'status':'UNAMBIGUOUS_GRAPH_ISOMORPHISM','rounds':history,'mapping':{atoms1[i]['id']:atoms2[j]['id'] for i,j in mapping.items()}}
    return {'status':'UNRESOLVED_MATCHING_INVARIANTS','rounds':history,'mapping':None,'reason':'Non-singleton color classes; matching refinement is not proof of isomorphism'}


def audit(atoms,cutoff):
    heavy,adj=graph(atoms,cutoff);oxygen=[a for a in atoms if a['element']=='O']
    hcounts={a['id']:0 for a in oxygen};hrows=[]
    for h in (a for a in atoms if a['element']=='H'):
        distances=sorted((dist(h,o),o['id']) for o in oxygen)
        d,oid=distances[0];ties=[i for value,i in distances if abs(value-d)<=1e-10]
        assigned=d<=OH and len(ties)==1
        if assigned:hcounts[oid]+=1
        hrows.append({'H':h['id'],'nearest_O':oid if len(ties)==1 else None,'distance_A':d,'ties':ties if len(ties)>1 else [],'assigned':assigned})
    rows=[]
    for i,o in enumerate(heavy):
        if o['element']!='O':continue
        near=[{'Mo':heavy[j]['id'],'distance_A':dist(o,heavy[j])} for j in sorted(adj[i])]
        degree=len(near)
        rows.append({'O':o['id'],'assigned_H_count':hcounts[o['id']],'Mo_degree':degree,'class':'disconnected' if degree==0 else 'terminal-like' if degree==1 else 'bridging-like','Mo_contacts':near,'nearest_Mo_A':min(dist(o,m) for m in heavy if m['element']=='Mo')})
    remaining=set(range(len(heavy)));components=[]
    while remaining:
        todo=[remaining.pop()];seen=set(todo)
        while todo:
            for j in adj[todo.pop()]:
                if j in remaining:remaining.remove(j);seen.add(j);todo.append(j)
        components.append(dict(Counter(heavy[i]['element'] for i in seen)))
    return {'cutoff_A':cutoff,'heavy_edges':sum(map(len,adj))//2,'Mo_degree_histogram':dict(Counter(len(adj[i]) for i,a in enumerate(heavy) if a['element']=='Mo')),'O_degree_histogram':dict(Counter(r['Mo_degree'] for r in rows)),'H_count_Mo_degree_cross_tab':dict(Counter(f"H{r['assigned_H_count']}:Mo{r['Mo_degree']}" for r in rows)),'H_bearing_terminal_like_O':sum(r['assigned_H_count']>0 and r['Mo_degree']==1 for r in rows),'H_bearing_bridging_like_O':sum(r['assigned_H_count']>0 and r['Mo_degree']>=2 for r in rows),'H_unassigned':sum(not r['assigned'] for r in hrows),'H_assignments':hrows,'oxygen_local_environments':rows,'components':components}


def balance(mo,water,hydroxide,oxide):
    return {'Mo':mo,'O':water+hydroxide+oxide,'H':2*water+hydroxide,'formal_charge':6*mo-hydroxide-2*oxide}


def main():
    paths=[BASE/'PROTOCOL.md',BASE.parent/'published-parent/geometry.cml',BASE.parent/'published-parent/analysis.json',BASE.parent/'identity/site_mapping.json',BASE.parent/'identity/extract.py',BASE.parent/'parent-inputs/P0_A.xyz',BASE.parent/'parent-inputs/build.py',BASE.parent/'parent-inputs/metadata.json']
    ns={'c':'http://www.xml-cml.org/schema'}
    published=[atom(e.attrib['id'],e.attrib['elementType'],[e.attrib[k] for k in ('x3','y3','z3')]) for e in ET.parse(paths[1]).getroot().findall('.//c:atomArray/c:atom',ns)]
    lines=(BASE.parent/'parent-inputs/P0_A.xyz').read_text().splitlines()
    p0=[atom('p'+str(i+1),f[0],f[1:]) for i,line in enumerate(lines[2:]) if (f:=line.split())]
    assert len(p0)==int(lines[0])==len(published)==196
    sites=json.loads((BASE.parent/'identity/site_mapping.json').read_text())
    assert len(sites)==164
    assert [a['element'] for a in p0[:164]]==[s['element'] for s in sites]
    delta=max(math.dist(a['xyz'],s['cartesian_A']) for a,s in zip(p0[:164],sites))
    assert delta<1e-9
    site_labels={p0[i]['id']:s['label']+'@'+str(s['symmetry_index']) for i,s in enumerate(sites)}
    results=[]
    for cutoff in CUTOFFS:
        results.append({'cutoff_A':cutoff,'published':audit(published,cutoff),'P0_A':audit(p0,cutoff),'heavy_graph_comparison':compare(graph(published,cutoff),graph(p0,cutoff))})
    result={'status':'GEOMETRY_AUDIT_ONLY','protocol_sha256':hashlib.sha256((BASE/'PROTOCOL.md').read_bytes()).hexdigest(),'sources_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'P0_crystal_mapping_max_distance_A':delta,'P0_local_source_labels':site_labels,'results':results,'bookkeeping':{'P0_16water_112oxide':balance(36,16,0,112),'published_4water_24hydroxide_100oxide':balance(36,4,24,100),'formal_redistribution':'12 H2O + 12 O(2-) <-> 24 OH(-); arithmetic only, not mechanism'},'limits':['Distances do not prove bonds/protonation','Published coordinates are initialization; final geometry not declared','No unambiguous site mapping asserted unless verified singleton graph correspondence','Distinct cutoff graphs need not imply different physical framework identity','MoVI formal bookkeeping is assumed, not measured'],'SCFs_launched':0,'physical_admission':False}
    (BASE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print('P0 mapping max distance A',delta)
    for r in results:
        print('CUTOFF',r['cutoff_A'],'COMPARISON',r['heavy_graph_comparison']['status'])
        for name in ('published','P0_A'):
            print(name,{k:r[name][k] for k in ('heavy_edges','Mo_degree_histogram','O_degree_histogram','H_count_Mo_degree_cross_tab','H_bearing_terminal_like_O','H_bearing_bridging_like_O','H_unassigned','components')})
    print('BOOKKEEPING',result['bookkeeping'])

if __name__=='__main__':main()
