"""Ground-state RKS C-PCM/SWIG only; equations from PySCF 2.14 pcm.py.

No nuclear derivatives, response, excited states, or post-SCF qualification.
"""
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.special import erf
from scipy.spatial.distance import cdist
from pyscf import df, dft, gto, lib
from pyscf.data import radii
from pyscf.solvent import pcm


def unsupported(*args, **kwargs):
    raise NotImplementedError('Blocked C-PCM supports only unfrozen ground-state RKS')


class GroundStateOnly:
    nuc_grad_method = Gradients = Hessian = gen_response = stability = unsupported
    TDA = TDHF = TDDFT = MP2 = CISD = CCSD = CASCI = CASSCF = unsupported
    to_gpu = newton = unsupported


class BlockedPCM(pcm.PCM):
    surface_block = 128
    ao_block = 8
    grad = hess = nuc_grad_method = Hessian = _B_dot_x = to_gpu = unsupported

    def _guard(self):
        if (self.method.upper() not in ('C-PCM', 'CPCM') or
                self.surface_discretization_method.upper() != 'SWIG' or
                self.frozen or self.state_id != 0 or self.equilibrium_solvation):
            unsupported()
        if not (self.eps >= 1 and self.surface_block == 128 and self.ao_block in (1, 7, 8)):
            raise ValueError('Invalid dielectric or unqualified block size')

    def reset(self, mol=None):
        super().reset(mol)
        self.e = self.v = self._dm = None
        return self

    def build(self, ng=None):
        self._guard()
        self.reset()
        rad = self.radii_table
        if rad is None:
            rad = self.vdw_scale * pcm.modified_Bondi + self.r_probe/radii.BOHR
        ng = pcm.gen_grid.LEBEDEV_ORDER[self.lebedev_order] if ng is None else ng
        surface = pcm.gen_surface(self.mol, ng=ng, rad=rad, surface_discretization_method='SWIG')
        xyz, xi = surface['grid_coords'], surface['charge_exp']
        n = len(xi)
        S = np.empty((n, n))
        for a, b in lib.prange(0, n, self.surface_block):
            r = cdist(xyz[a:b], xyz)
            combined = xi[a:b, None] * xi[None, :] / np.sqrt(xi[a:b, None]**2 + xi[None, :]**2)
            combined *= r
            erf(combined, out=combined)
            r[np.arange(b-a), np.arange(a,b)] = 1
            combined /= r
            S[a:b] = combined
            del r, combined
        np.fill_diagonal(S, xi*np.sqrt(2/np.pi)/surface['switch_fun'])
        factor = cho_factor(S, lower=True, overwrite_a=False, check_finite=True)
        v_n = np.empty(n)
        nuclei = gto.fakemol_for_charges(self.mol.atom_coords())
        for a, b in lib.prange(0, n, self.surface_block):
            fake = gto.fakemol_for_charges(xyz[a:b], expnt=xi[a:b]**2)
            ints = gto.mole.intor_cross(self.mol._add_suffix('int2c2e'), nuclei, fake)
            v_n[a:b] = self.mol.atom_charges() @ ints
            del ints, fake
        self.surface = surface
        self.v_grids_n = v_n
        self._intermediates = {'S': S, 'factor': factor}
        return self

    def _contract(self, density=None, charges=None):
        self._guard()
        mol = self.mol
        xyz, xi = self.surface['grid_coords'], self.surface['charge_exp']
        out = np.empty(len(xi)) if density is not None else np.zeros((mol.nao, mol.nao))
        intor = mol._add_suffix('int3c2e')
        opt = gto.moleintor.make_cintopt(mol._atm, mol._bas, mol._env, intor)
        for a, b in lib.prange(0, len(xi), self.ao_block):
            fake = gto.fakemol_for_charges(xyz[a:b], expnt=xi[a:b]**2)
            fake.cart = mol.cart
            ints = df.incore.aux_e2(mol, fake, intor=intor, aosym='s1', cintopt=opt)
            if density is not None:
                out[a:b] = np.einsum('ijL,ij->L', ints, density)
            else:
                out -= np.einsum('ijL,L->ij', ints, charges[a:b])
            del ints, fake
        return out

    def _get_v(self, dms):
        if dms.shape != (1, self.mol.nao, self.mol.nao):
            unsupported()
        return self._contract(density=dms[0])[None, :]

    def _get_vmat(self, q):
        if q.shape != (1, len(self.v_grids_n)):
            unsupported()
        return self._contract(charges=q[0])[None, :, :]

    def _get_vind(self, dm):
        self._guard()
        dm = np.asarray(dm)
        if (dm.shape != (self.mol.nao, self.mol.nao) or np.iscomplexobj(dm) or
                not np.isfinite(dm).all() or not np.allclose(dm, dm.T, atol=1e-12, rtol=0)):
            raise ValueError('Expected finite real symmetric restricted density')
        if not self._intermediates:
            self.build()
        v = self.v_grids_n - self._contract(density=dm)
        f = 1.0 if np.isinf(self.eps) else (self.eps-1)/self.eps
        q = cho_solve(self._intermediates['factor'], -f*v)
        potential = self._contract(charges=q)
        self._intermediates.update(q=q, q_sym=q, v_grids=v, dm=dm[None, :, :])
        return float(q @ v / 2), potential


def attach(mf, solvent):
    if type(mf) is not dft.rks.RKS or solvent.mol is not mf.mol:
        unsupported()
    solvent._guard()
    result = pcm.pcm_for_scf(mf, solvent)
    return lib.set_class(result, (GroundStateOnly, result.__class__))
