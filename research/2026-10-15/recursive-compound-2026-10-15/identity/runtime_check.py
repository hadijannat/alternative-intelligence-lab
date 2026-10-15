import json
import sys
import pyscf
from pyscf import gto
out={'python':sys.version,'pyscf':pyscf.__version__,'scf_run':False,'builds':{}}
for atom,spin in [('Mo',6),('W',6),('V',3)]:
    m=gto.M(atom=f'{atom} 0 0 0',basis='def2-svp',ecp='def2-svp' if atom!='V' else {},spin=spin,verbose=0)
    out['builds'][atom]={'nao':m.nao,'explicit_electrons':m.nelectron,'ecp_core_electrons':m.atom_nelec_core(0)}
assert [out['builds'][a]['ecp_core_electrons'] for a in ('Mo','W','V')]==[28,60,0]
print(json.dumps(out,indent=2))
