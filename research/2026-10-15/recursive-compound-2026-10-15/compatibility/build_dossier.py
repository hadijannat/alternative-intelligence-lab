from pathlib import Path
import csv,json,hashlib
p=Path(__file__).parent
rows=[]
for species,medium,nom,ph0,ph1,sd0,sd1,v0,v1,pm0,pm1,p20,p21,small0,small1,tables in [
 ('PMo12','D2O',None,1.30,1.20,.06,.05,[73,77,77],[71,76,77],76,74,13,13,0,0,'S17;S18;S19'),
 ('PMo12','sodium phosphate',3,1.97,1.89,.04,.06,[0,0,0],[0,0,0],0,0,1,1,99,99,'S17;S18;S19'),
 ('PMo12','sodium phosphate',4,2.10,2.03,.06,.09,[0,0,0],[0,0,0],0,0,1,1,99,99,'S17;S18;S19'),
 ('alpha-P2W18','sodium phosphate',3,2.99,2.98,.08,.06,[100]*3,[100]*3,100,100,0,0,0,0,'S8;S10;S11'),
 ('alpha-P2W18','sodium phosphate',4,4.00,3.97,.06,.06,[100]*3,[100]*3,100,100,0,0,0,0,'S8;S10;S11')]:
 for stage,ph,sd,reps,parent,other,small in [('initial',ph0,sd0,v0,pm0,p20,small0),('after_24h_37C',ph1,sd1,v1,pm1,p21,small1)]:
  rows.append(dict(species=species,medium=medium,nominal_pH=nom,buffer_M=0 if nom is None else .1,POM_mM=10,stage=stage,NMR_C=25,measured_pH_mean=ph,measured_pH_SD=sd,parent_rep1=reps[0],parent_rep2=reps[1],parent_rep3=reps[2],parent_reported_percent=parent,P2Mo18_reported_percent=other,P2Mo5_or_PMo6_reported_percent=small,source_tables=tables,denominator='assigned POM phosphorus NMR signals; free phosphate excluded'))
with (p/'selected_rows.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
buffers=[('acetate',[4,5,5.5],[.1]),('citrate',[3,4,5,6,6.5],[.1]),('sodium phosphate',[3,4,5,6,7,8],[.1]),('PBS',[7.4],[.1]),('tris-HCl',[7.5,8,8.5],[.1]),('glycine-NaOH',[8.6],[.1,.2,.5]),('HEPES',[7,8],[.1]),('MES',['Table1:6; SI:5.5'],[.1]),('MHB',[7.4],['complex medium']),('F-12 Ham',[7.4],['complex medium']),('water/D2O',['unbuffered'],[0])]
(p/'atlas_scope.json').write_text(json.dumps(dict(POMs=['PW12','alpha-P2W18','alpha/beta-P2W18','P5W30','(ZrPW11)2','PMo12','P2Mo18','TeW6','SiW12','V10'],target_tested=False,Mo36_tested=False,buffers=[dict(name=n,pH=h,concentration_M=c) for n,h,c in buffers],standard_POM_mM=10,W183_only_POM_mM=20,W183_buffer_M=.2,timepoints=['immediately after preparation','after 24 h incubation at37C'],NMR_acquisition_C=25,W183_acquisition_hours_approx=60,scope_warning='TeW6 and SiW12 selected conditions only; buffer concentration has glycine exceptions; MES main/SI discrepancy preserved'),indent=2))
raw=p/'raw'
if (raw/'archive_metadata.json').exists() and not (raw/'archive_metadata.json').stat().st_size: (raw/'archive_metadata.json').unlink()
(raw/'access.json').write_text(json.dumps({'article':{'url':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10284552/fullTextXML','status':200},'supplements':{'url':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10284552/supplementaryFiles','status':200,'bytes':14764209},'phaidra':{'doi':'10.25365/phaidra.398','object':'o:1648343','metadata_route':'https://services.phaidra.univie.ac.at/api/object/o:1648343/metadata','status':200,'bytes':0,'result':'No usable metadata or raw NMR acquired; landing route inaccessible in web tool'},'pmc_pdf_route':{'status':200,'bytes':1814,'type':'text/html','result':'not PDF; EuropePMC used'}},indent=2))
sources=[dict(id='atlas2023',doi='10.1126/sciadv.adi0814',url='https://pmc.ncbi.nlm.nih.gov/articles/PMC10284552/',files=['raw/article.xml','raw/article.txt','raw/supplement.pdf','raw/supplement.txt'],license='CC BY 4.0',scope='SI Tables S8,S10,S11,S17,S18,S19; published tabulation, not independently reprocessed NMR'),dict(id='archive',doi='10.25365/phaidra.398',url='https://phaidra.univie.ac.at/o:1648343',files=['raw/access.json'],scope='access failure only; no spectra imported'),dict(id='parent',doi='10.1073/pnas.1921536117',url='https://www.chem.gla.ac.uk/cronin/images/pubs/Mathis-PNASMay2020.pdf',files=['../../noncarbon-discovery-2026-10-15/research/pom/raw/miras2020.txt'],scope='parent pH1.7,24.3C read directly'),dict(id='WO3',doi='10.1039/D4SC00102H',url='https://pmc.ncbi.nlm.nih.gov/articles/PMC10988594/',files=['../../noncarbon-discovery-2026-10-15/research/redox_compatibility/raw/spencer2024.xml'],scope='0.5M sulfuric acid; separate electrode experiment')]
for s in sources:s['sha256']={f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in s['files']}
(p/'sources.json').write_text(json.dumps(sources,indent=2))
