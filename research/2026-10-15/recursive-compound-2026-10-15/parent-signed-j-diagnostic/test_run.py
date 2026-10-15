import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import numpy as np

spec=importlib.util.spec_from_file_location('signed_j_probe',Path(__file__).with_name('run.py'))
run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)


class FakeMol:
    cart=False
    nao=5
    nbas=3
    def ao_loc_nr(self):return np.array([0,2,3,5])
    def ao_labels(self,fmt=False):return [(0,'Mo','synthetic',str(i)) for i in range(self.nao)]
    def bas_atom(self,shell):return 0
    def bas_kappa(self,shell):return 0
    def atom_symbol(self,atom):return 'Mo'
    def _add_suffix(self,name):return name+'_sph'


class SignedJTests(unittest.TestCase):
    def test_chunk_sign_finite_and_symmetry_controls(self):
        ref=np.arange(25,dtype=np.float64).reshape(5,5);ref+=ref.T.copy()
        with patch.object(run,'NAO',5),patch.object(run,'CHUNK_ROWS',2):
            report=run.matrix_checks(-ref,ref)
            self.assertTrue(report['finite'] and report['symmetric'] and report['sign_pass'])
            bad=-ref.copy();bad[-1,-1]+=2e-10
            self.assertFalse(run.matrix_checks(bad,ref)['sign_pass'])
            self.assertFalse(run.matrix_checks(ref,ref)['sign_pass'])
            bad=-ref.copy();bad[0,-1]+=2e-10
            self.assertFalse(run.matrix_checks(bad,ref)['symmetric'])
            for value in (np.nan,np.inf):
                bad=-ref.copy();bad[-1,-1]=value
                self.assertFalse(run.matrix_checks(bad,ref)['finite'])
            with self.assertRaises(ValueError):run.matrix_checks(np.zeros((4,4)))
            with self.assertRaises(ValueError):run.matrix_checks(ref.astype(np.float32))

    def test_analytic_indefinite_density_and_AO_origin(self):
        mol=FakeMol()
        with patch.object(run,'NAO',5):
            dm,record=run.indefinite_density(mol)
            self.assertEqual(np.count_nonzero(dm),2)
            self.assertEqual(dm[0,1],run.AMPLITUDE);self.assertEqual(dm[1,0],run.AMPLITUDE)
            self.assertAlmostEqual(float(np.sqrt(np.sum(dm*dm))),.01)
            self.assertEqual(record['analytic_nonzero_eigenvalues'],[-run.AMPLITUDE,run.AMPLITUDE])
            with patch.object(mol,'atom_symbol',return_value='O'):
                with self.assertRaises(ValueError):run.indefinite_density(mol)
            mol.cart=True
            with self.assertRaises(ValueError):run.indefinite_density(mol)

    def test_shell_index_extraction_and_ten_oracle_entries(self):
        mol=FakeMol();aux=types.SimpleNamespace(nao=3,nbas=2);calls=[];solves=[]
        tensor=np.arange(75,dtype=np.float64).reshape(5,5,3)/100
        tensor=(tensor+tensor.transpose(1,0,2))/2
        rho=2*run.AMPLITUDE*tensor[0,1]
        j=np.einsum('ijL,L->ij',tensor,rho)
        def aux_e2(a,b,shls_slice,intor,aosym):
            self.assertIs(a,mol);self.assertIs(b,aux)
            self.assertEqual(intor,'int3c2e_sph');self.assertEqual(aosym,'s1')
            sa,sa1,sb,sb1,k,k1=shls_slice
            self.assertEqual((sa1,sb1,k,k1),(sa+1,sb+1,0,2))
            loc=mol.ao_loc_nr();calls.append(shls_slice)
            return tensor[loc[sa]:loc[sa1],loc[sb]:loc[sb1]].copy()
        def solve(factor,rhs):solves.append(rhs.copy());return rhs.copy()
        with patch.object(run,'NAO',5),patch.object(run,'NAUX',3),patch.object(run,'SELECTED',(0,1,2,4)):
            r=run.selected_oracle(mol,aux,('identity',True),j,aux_e2,solve)
            self.assertTrue(r['pass']);self.assertEqual(len(r['comparisons']),10)
            self.assertEqual(len(calls),11);self.assertEqual(len(solves),1)
            np.testing.assert_allclose(solves[0],rho,rtol=0,atol=0)
            self.assertEqual(r['AO_metadata'][-1]['shell'],2)
            self.assertEqual(r['AO_metadata'][-1]['within_shell'],1)
            self.assertEqual(r['maximum_buffer_bytes'],8*2*2*3)
            bad=j.copy();bad[4,2]+=1e-7
            self.assertFalse(run.selected_oracle(mol,aux,None,bad,aux_e2,solve)['pass'])
            with self.assertRaises(ValueError):run.selected_oracle(mol,aux,None,j,lambda *a,**k:np.zeros((1,1,3)),solve)
            with self.assertRaises(ValueError):run.ao_metadata(mol,(5,))
            with patch.object(mol,'bas_kappa',return_value=1):
                with self.assertRaises(ValueError):run.ao_metadata(mol,(0,))

    def test_exact_two_calls_and_forbidden_routes(self):
        mf=types.SimpleNamespace(_rij_calls=0,with_solvent=types.SimpleNamespace());requests=[]
        def get_j(dm):requests.append(dm.copy());mf._rij_calls+=1;return dm*2
        mf.get_j=get_j;dm=np.eye(2)
        for number in (1,2):np.testing.assert_array_equal(run.call_j(mf,dm,number),dm*2)
        self.assertEqual(len(requests),2)
        for number in (0,1,2,3,True):
            with self.assertRaises(ValueError):run.call_j(mf,dm,number)
        for name in ('kernel','scf','run','get_init_guess','make_rdm1','get_veff','init_guess_by_minao','init_guess_by_atom','init_guess_by_1e','init_guess_by_chkfile','init_guess_by_huckel'):
            with self.assertRaises(RuntimeError):getattr(mf,name)()
        with self.assertRaises(RuntimeError):mf.with_solvent.build()
        mf._rij_calls=0;mf.get_j=lambda dm:dm
        with self.assertRaises(ValueError):run.call_j(mf,dm,1)

    def test_exclusive_claim_buffered_files_and_containment(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            out=run.BASE/'run-v1';out.mkdir();run.claim_worker(out)
            self.assertEqual(run.read(out/'worker-started.json')['maximum_J_calls'],2)
            with self.assertRaises(FileExistsError):run.claim_worker(out)
            stages=[];run.post_call_file(out,1,lambda name,**kw:stages.append(name))
            self.assertEqual(stages,['post_call_file_start','post_call_file_closed'])
            self.assertGreater((out/'post-call-1.bin').stat().st_size,0)
            with self.assertRaises(FileExistsError):run.post_call_file(out,1,lambda *a,**k:None)
            for path in (run.BASE,run.BASE/'../outside'):
                with self.assertRaises(ValueError):run.owned(path)

    def test_immutable_factor_state_contract(self):
        f=np.eye(3,order='F');f.flags.writeable=False
        obj=types.SimpleNamespace(_vjopt=types.SimpleNamespace(j2c=(f,True),j2c_type='cd'))
        with patch.object(run,'NAUX',3):
            one=run.factor_state(obj);self.assertEqual(one,run.factor_state(obj))
            f.flags.writeable=True
            with self.assertRaises(ValueError):run.factor_state(obj)
            f.flags.writeable=False;obj._vjopt.j2c=(f,False)
            with self.assertRaises(ValueError):run.factor_state(obj)

    def test_review_hash_binding_and_no_launch_without_approval(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            pins={'qualification':{'terminal':'fixed'}}
            run.save(run.BASE/'preparation.json',{'status':'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW','pins':pins})
            review={'status':'APPROVED_ONE_SIGNED_PARENT_J_DIAGNOSTIC','independent_root_review':True,'reviewer':'synthetic',
                    'preparation_sha256':run.sha(run.BASE/'preparation.json'),'qualification_artifacts':pins['qualification']}
            with patch.object(run,'manifest',return_value=pins):
                with self.assertRaises(FileNotFoundError):run.launch()
                self.assertFalse((run.BASE/'run-v1').exists())
                run.save(run.BASE/'independent-root-review.json',review)
                self.assertIn('review_sha256',run.validate_gate())
                for change in ({'status':'pending'},{'independent_root_review':False},{'reviewer':''},{'preparation_sha256':'bad'},{'qualification_artifacts':{}}):
                    run.save(run.BASE/'independent-root-review.json',{**review,**change})
                    with self.assertRaises(ValueError):run.validate_gate()
                run.save(run.BASE/'independent-root-review.json',review)
                with patch.object(run,'manifest',return_value={'qualification':{'terminal':'changed'}}):
                    with self.assertRaises(ValueError):run.validate_gate()

    def success_result(self):
        return {'status':run.STATUS,'checks':{k:True for k in run.CHECKS},'J_calls':2,'metric_calls':2,
                'factor_count':1,'oracle_metric_solves':1,'SCFs_launched':0}

    def test_exact_result_contract(self):
        good=self.success_result();self.assertTrue(run.accepted_result(good))
        for key in ('J_calls','metric_calls','factor_count','oracle_metric_solves','SCFs_launched'):
            bad=copy.deepcopy(good);bad[key]=False;self.assertFalse(run.accepted_result(bad))
        for checks in ({},{'invented':True},{k:False for k in run.CHECKS},[True]):
            self.assertFalse(run.accepted_result({**good,'checks':checks}))
        self.assertFalse(run.accepted_result([]))

    def exercise_launch(self,failure=None):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)):
            calls=[]
            def monitored(command,out,wall,rss):
                calls.append(command);self.assertEqual((wall,rss),(600,10*2**30))
                for name in ('first-checks.json','second-checks.json','selected-oracle.json','factor-aliases.json','factor-states.json',
                             'metric-calls.jsonl','post-call-1.bin','post-call-2.bin','runtime-observation.json','stages.jsonl','checks.json'):
                    (out/name).write_text('synthetic preserved artifact')
                run.save(out/'result.json',self.success_result())
                if failure=='truncated':(out/'result.json').write_text('{')
                if failure=='missing':(out/'selected-oracle.json').unlink()
                return {'returncode':-15 if failure=='wall' else 0,'termination_reason':'WALL_LIMIT' if failure=='wall' else None,'monitor_error':None}
            supervisor=types.SimpleNamespace(THREADS={'OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1'},monitored_run=monitored)
            original_read=run.read
            def read(path):
                if Path(path)==run.first.QUAL/'preparation.json':return {'pins':{'runtime':{'python':'/synthetic/python'}}}
                return original_read(path)
            with patch.object(run,'validate_gate',side_effect=[{'gate':'fixed'},{'gate':'changed' if failure=='gate' else 'fixed'}]),patch.object(run,'load',return_value=supervisor),patch.object(run,'read',side_effect=read):
                self.assertEqual(run.launch(),int(failure is not None))
            terminal=run.read(run.BASE/'run-v1/launch-result.json')
            self.assertEqual(terminal['status'],run.STATUS if failure is None else 'INCOMPLETE_OR_FAILED_SIGNED_J')
            self.assertEqual(len(calls),1);self.assertEqual(calls[0][-1],'--worker')
            self.assertTrue((run.BASE/'run-v1/stages.jsonl').exists())
            with patch.object(run,'validate_gate',return_value={'gate':'fixed'}):
                with self.assertRaises(FileExistsError):run.launch()

    def test_one_child_and_failure_preservation(self):
        for failure in (None,'wall','truncated','missing','gate'):
            with self.subTest(failure=failure):self.exercise_launch(failure)

    def test_prepare_rejects_failed_manifest_before_loading_density(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(run,'BASE',Path(directory)),patch.object(run,'manifest',side_effect=ValueError('changed pin')),patch.object(run.first,'saved_density',side_effect=AssertionError('must not load')):
            with self.assertRaisesRegex(ValueError,'changed pin'):run.prepare()
            self.assertFalse((run.BASE/'preparation.json').exists())


if __name__=='__main__':unittest.main(verbosity=2)
