import ctypes,json,pathlib,sys,threading
import pyscf,numpy,scipy,h5py
from pyscf import lib
p=pathlib.Path(__file__).resolve().parent
omp=ctypes.CDLL(str(p/'env/lib/libomp.dylib'))
omp.omp_get_num_threads.restype=ctypes.c_int
omp.omp_get_thread_num.restype=ctypes.c_int
callback_type=ctypes.CFUNCTYPE(None,ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int))
fork=omp.__kmpc_fork_call
fork.argtypes=[ctypes.c_void_p,ctypes.c_int,callback_type]
fork.restype=None
rows=[]
for n in [1,4,1]:
 lib.num_threads(n)
 observed=[]
 @callback_type
 def callback(global_tid,bound_tid):
  observed.append({'omp_team_size':omp.omp_get_num_threads(),'omp_thread_number':omp.omp_get_thread_num(),'python_thread_ident':threading.get_ident()})
 fork(None,0,callback)
 row={'requested':n,'pyscf_threads':lib.num_threads(),'parallel_region':sorted(observed,key=lambda r:r['omp_thread_number'])}
 rows.append(row)
 assert row['pyscf_threads']==n and len(observed)==n
 assert {r['omp_thread_number'] for r in observed}==set(range(n))
 assert all(r['omp_team_size']==n for r in observed)
r={'python':sys.version,'executable':sys.executable,'pyscf':pyscf.__version__,'pyscf_path':pyscf.__file__,'numpy':numpy.__version__,'scipy':scipy.__version__,'h5py':h5py.__version__,'rows':rows,'scientific_operators':0,'SCFs':0,'pass':True}
(p/'probe-result.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
