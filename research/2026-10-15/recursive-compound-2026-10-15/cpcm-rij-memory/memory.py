"""Local, source-pinned memory-mechanics specialization; not SCF qualified."""
import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace
import numpy as np
import scipy.linalg
from scipy.special import erf
from scipy.spatial.distance import cdist
from pyscf import gto, lib
from pyscf.data import radii
from pyscf.df import df_jk
from pyscf.solvent import pcm

BASE=Path(__file__).resolve().parent
for filename,want in json.loads((BASE/'source_pins.json').read_text()).items():
    if hashlib.sha256(Path(filename).read_bytes()).hexdigest()!=want:
        raise RuntimeError('Source pin changed: '+filename)
spec=importlib.util.spec_from_file_location('qualified_blocked_pcm',BASE.parent/'cpcm-blocked/blocked_pcm.py')
qualified=importlib.util.module_from_spec(spec);spec.loader.exec_module(qualified)
spec_ri=importlib.util.spec_from_file_location('qualified_rij',BASE.parent/'rij-jkfit-qualification/rij.py')
qualified_ri=importlib.util.module_from_spec(spec_ri);spec_ri.loader.exec_module(qualified_ri)
CHUNK=65536


class FactorizationAborted(RuntimeError):
    """Bypasses native LinAlgError fallback after a destructive factor attempt."""


def finite_chunks(array):
    if not isinstance(array,np.ndarray) or array.dtype!=np.float64 or not (array.flags.c_contiguous or array.flags.f_contiguous):
        raise ValueError('Require contiguous float64 array without implicit copy')
    flat=array.ravel(order='K')
    for start in range(0,flat.size,CHUNK):
        if not np.isfinite(flat[start:start+CHUNK]).all():
            raise ValueError('Nonfinite factor or RHS')


def factor_inplace(matrix,lower=True,**kwargs):
    if not lower or matrix.ndim!=2 or matrix.shape[0]!=matrix.shape[1] or not matrix.flags.f_contiguous or not matrix.flags.writeable:
        raise ValueError('Require writable Fortran square lower-factor input')
    finite_chunks(matrix)
    try:
        factor=scipy.linalg.cho_factor(matrix,lower=True,overwrite_a=True,check_finite=False)
    except scipy.linalg.LinAlgError as exc:
        raise FactorizationAborted('In-place Cholesky failed; input may be corrupted; no regular fallback') from exc
    if not np.shares_memory(factor[0],matrix):
        raise FactorizationAborted('Cholesky copied input; memory contract rejected')
    finite_chunks(factor[0])
    factor[0].flags.writeable=False
    return factor


def solve_checked(factor,rhs,**kwargs):
    matrix,lower=factor
    if not lower or matrix.ndim!=2 or matrix.shape[0]!=matrix.shape[1] or matrix.flags.writeable or not matrix.flags.f_contiguous:
        raise ValueError('Expected immutable Fortran lower Cholesky factor')
    finite_chunks(matrix);finite_chunks(rhs)
    if rhs.ndim not in (1,2) or rhs.shape[0]!=matrix.shape[0]:raise ValueError('RHS shape differs')
    result=scipy.linalg.cho_solve(factor,rhs,check_finite=False)
    finite_chunks(result)
    return result


def reject_regular(*args,**kwargs):
    raise FactorizationAborted('Regular solve is outside this qualification')


def private_clone(function,overrides):
    namespace={**function.__globals__,**overrides}
    return FunctionType(function.__code__,namespace,function.__name__,function.__defaults__,function.__closure__)


private_scipy=SimpleNamespace(linalg=SimpleNamespace(cho_factor=factor_inplace,cho_solve=solve_checked,solve=reject_regular,LinAlgError=scipy.linalg.LinAlgError))
native_get_j=private_clone(df_jk.get_j,{'scipy':private_scipy})


class MemoryPCM(qualified.BlockedPCM):
    ao_block=1

    def _guard(self):
        super()._guard()
        if self.ao_block!=1:raise ValueError('Only AO block1 qualified here')

    def build(self,ng=None):
        self._guard();self.reset()
        rad=self.radii_table
        if rad is None:rad=self.vdw_scale*pcm.modified_Bondi+self.r_probe/radii.BOHR
        ng=pcm.gen_grid.LEBEDEV_ORDER[self.lebedev_order] if ng is None else ng
        surface=pcm.gen_surface(self.mol,ng=ng,rad=rad,surface_discretization_method='SWIG')
        xyz,xi=surface['grid_coords'],surface['charge_exp'];n=len(xi)
        matrix=np.empty((n,n),order='F')
        for a,b in lib.prange(0,n,128):
            r=cdist(xyz[a:b],xyz)
            combined=xi[a:b,None]*xi[None,:]/np.sqrt(xi[a:b,None]**2+xi[None,:]**2)
            combined*=r;erf(combined,out=combined)
            r[np.arange(b-a),np.arange(a,b)]=1;combined/=r
            matrix[a:b]=combined
            del r,combined
        np.fill_diagonal(matrix,xi*np.sqrt(2/np.pi)/surface['switch_fun'])
        factor=factor_inplace(matrix)
        del matrix
        nuclear=np.empty(n);nuclei=gto.fakemol_for_charges(self.mol.atom_coords())
        for a,b in lib.prange(0,n,128):
            fake=gto.fakemol_for_charges(xyz[a:b],expnt=xi[a:b]**2)
            ints=gto.mole.intor_cross(self.mol._add_suffix('int2c2e'),nuclei,fake)
            nuclear[a:b]=self.mol.atom_charges()@ints
            del ints,fake
        self.surface=surface;self.v_grids_n=nuclear
        self._intermediates={'factor':factor}
        return self

    _get_vind=private_clone(qualified.BlockedPCM._get_vind,{'cho_solve':solve_checked})


_install_private=private_clone(qualified_ri.install,{'df_jk':SimpleNamespace(get_j=native_get_j)})

def install(mf,record_call=None):
    mf.get_hcore()
    return _install_private(mf,record_call)
