import types
import numpy as np
from pyscf import df
from pyscf.df import df_jk


def install(mf, record_call=None):
    if mf.xc.upper() != 'PBE' or not mf.direct_scf:
        raise ValueError('Qualified for direct-SCF pure PBE only')
    obj = df.DF(mf.mol, 'def2-universal-jkfit')
    coordinates = mf.mol.atom_coords().copy()
    basis = mf.mol._bas.copy()
    environment = mf.mol._env.copy()
    mf._rij_df = obj
    mf._rij_calls = 0
    mf._rij_factor_id = None

    def get_jk(self, mol=None, dm=None, hermi=1, with_j=True, with_k=True, omega=None):
        if (mol is not None and mol is not obj.mol) or self.mol is not obj.mol:
            raise ValueError('Different molecule')
        if (not with_j or with_k or omega is not None or hermi != 1 or
                self.xc.upper() != 'PBE' or obj.auxbasis != 'def2-universal-jkfit'):
            raise ValueError('Unsupported Coulomb request')
        if (not np.array_equal(coordinates, obj.mol.atom_coords()) or
                not np.array_equal(basis, obj.mol._bas) or
                not np.array_equal(environment, obj.mol._env)):
            raise ValueError('Molecule changed; a fresh qualification object is required')
        dm = self.make_rdm1() if dm is None else np.asarray(dm)
        if (dm.shape != (obj.mol.nao, obj.mol.nao) or np.iscomplexobj(dm) or
                not np.isfinite(dm).all() or not np.allclose(dm, dm.T, atol=1e-12, rtol=0)):
            raise ValueError('Expected finite real symmetric restricted density')
        if obj._cderi is not None or obj._cderi_to_save is not None:
            raise ValueError('Stored three-index tensors are outside this protocol')
        j = df_jk.get_j(obj, np.asarray(dm, dtype=np.float64), hermi, self.direct_scf_tol)
        if record_call is not None:
            record_call({'call':self._rij_calls+1,
                         'factor_type':getattr(obj._vjopt,'j2c_type',None),
                         'cached_3index':obj._cderi is not None,
                         'tensor_output':obj._cderi_to_save is not None,
                         'finite_J':bool(np.isfinite(j).all())})
        if (obj._vjopt is None or obj._vjopt.j2c_type != 'cd' or
                obj._cderi is not None or obj._cderi_to_save is not None or
                not np.isfinite(j).all()):
            raise ValueError('Rejected fallback, tensor storage or nonfinite Coulomb result')
        factor_id = id(obj._vjopt.j2c[0])
        if self._rij_factor_id is not None and self._rij_factor_id != factor_id:
            raise ValueError('Metric factor was replaced')
        self._rij_factor_id = factor_id
        self._rij_calls += 1
        return j, None

    mf.get_jk = types.MethodType(get_jk, mf)
    return mf
