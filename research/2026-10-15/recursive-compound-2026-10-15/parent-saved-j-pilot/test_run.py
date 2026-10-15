"""Synthetic boundaries only: no parent array, molecule, operator or SCF."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import Mock,patch
import numpy as np

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('parent_pilot_synthetic',HERE/'run.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
OK={'returncode':0,'termination_reason':None,'monitor_error':None}


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name).resolve()
        self.base_patch=patch.object(r,'BASE',self.base);self.base_patch.start()
        self.real_density=patch.object(r.first,'saved_density',side_effect=AssertionError('Real parent density forbidden in synthetic suite'));self.real_density.start()
    def tearDown(self):
        self.real_density.stop();self.base_patch.stop();self.tmp.cleanup()
    def save(self,path,value):
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value));return path
    def passed(self):
        return {'status':r.STATUS,'native_converged':True,'final_validation_complete':True,'SCFs_launched':1,
                'checks':dict.fromkeys(r.CHECKS,True)}
    def env(self):
        return {'dm':np.diag([2.,0.]),'mo_coeff':np.eye(2),'mo_occ':np.array([2.,0.]),
                'fock':np.array([[1.,.25],[.25,2.]]),'s1e':np.eye(2),'e_tot':-3.,'cycle':4}
    def fake_mf(self):
        def grad(c,o,f):return np.array([2.*f[1,0]])
        return types.SimpleNamespace(mol=types.SimpleNamespace(nelectron=2),get_grad=Mock(side_effect=grad),
                    get_j=Mock(side_effect=AssertionError('No J')),get_fock=Mock(side_effect=AssertionError('No fresh Fock')),
                    get_veff=Mock(side_effect=AssertionError('No veff')),cycles=0)
    def test_owned_rejects_outside_and_symlink(self):
        self.assertEqual(r.owned(self.base/'child'),self.base/'child')
        for p in (self.base,self.base.parent/'outside'):
            with self.assertRaises(ValueError):r.owned(p)
        (self.base/'link').symlink_to(self.base.parent,target_is_directory=True)
        with self.assertRaises(ValueError):r.owned(self.base/'link/out')
    def test_worker_claim_is_exclusive(self):
        r.claim_worker(self.base)
        with self.assertRaises(FileExistsError):r.claim_worker(self.base)
        self.assertEqual(r.read(self.base/'worker-started.json')['maximum_SCFs'],1)
    def test_atomic_checkpoint_preserves_old_on_replace_failure(self):
        path=self.base/'checkpoint.npz';r.atomic_npz(path,density=np.eye(2));before=path.read_bytes()
        with patch.object(r.os,'replace',side_effect=OSError('simulated rename failure')):
            with self.assertRaises(OSError):r.atomic_npz(path,density=np.ones((2,2)))
        self.assertEqual(path.read_bytes(),before);self.assertFalse(path.with_suffix('.tmp').exists())
    def test_atomic_checkpoint_preserves_old_on_write_failure(self):
        path=self.base/'checkpoint.npz';r.atomic_npz(path,density=np.eye(2));before=path.read_bytes()
        with patch.object(np,'savez',side_effect=OSError('simulated write failure')):
            with self.assertRaises(OSError):r.atomic_npz(path,density=np.ones((2,2)))
        self.assertEqual(path.read_bytes(),before)
    def test_checkpoint_uses_existing_full_fock_and_correct_cycle(self):
        mf=self.fake_mf();env=self.env();row=r.checkpoint(mf,env,self.base/'cycle.npz','completed_callback')
        self.assertEqual(row['cycle'],5);self.assertEqual(row['full_unscaled_solvent_gradient'],.5)
        self.assertIs(mf.get_grad.call_args.args[2],env['fock'])
        mf.get_fock.assert_not_called();mf.get_j.assert_not_called();mf.get_veff.assert_not_called()
        with np.load(self.base/'cycle.npz',allow_pickle=False) as data:
            for key in ('density','mo_coeff','mo_occ','fock','overlap'):self.assertTrue(np.isfinite(data[key]).all())
            np.testing.assert_array_equal(data['density'],env['dm']);self.assertEqual(int(data['cycle']),5)
    def test_checkpoint_rejects_nonfinite_without_replacing_complete(self):
        mf=self.fake_mf();env=self.env();path=self.base/'cycle.npz';r.checkpoint(mf,env,path,'completed_callback');before=path.read_bytes()
        env['dm'][0,0]=np.nan
        with self.assertRaises(ValueError):r.checkpoint(mf,env,path,'completed_callback')
        self.assertEqual(before,path.read_bytes())
    def test_checkpoint_rejects_cycle_outside_original_limit(self):
        for cycle in (-1,20):
            env=self.env();env['cycle']=cycle
            with self.assertRaises(ValueError):r.checkpoint(self.fake_mf(),env,self.base/'cycle.npz','completed_callback')
    def test_post_kernel_checkpoint_keeps_extra_cycle_state_separate(self):
        mf=self.fake_mf();env=self.env();r.checkpoint(mf,env,self.base/'cycle.npz','completed_callback')
        env['dm']=np.diag([1.9,.1]);env['e_tot']=-3.1
        r.checkpoint(mf,env,self.base/'native.npz','native_post_kernel')
        with np.load(self.base/'cycle.npz') as old,np.load(self.base/'native.npz') as final:
            self.assertNotEqual(float(old['energy_Eh']),float(final['energy_Eh']))
            self.assertEqual(int(old['cycle']),int(final['cycle']));self.assertEqual(str(final['kind']),'native_post_kernel')
    def test_no_fresh_residual_without_native_convergence(self):
        mf=self.fake_mf();mf.converged=False;mf.make_rdm1=Mock(side_effect=AssertionError('No new density'))
        with self.assertRaises(ValueError):r.converged_residual(mf,np.eye(2),self.base/'final.npz')
        mf.make_rdm1.assert_not_called();mf.get_fock.assert_not_called()
    def test_converged_residual_exactly_one_fresh_fock(self):
        mf=self.fake_mf();env=self.env();mf.converged=True;mf.make_rdm1=Mock(return_value=env['dm'])
        mf.get_fock=Mock(return_value=env['fock']);mf.mo_coeff=env['mo_coeff'];mf.mo_occ=env['mo_occ'];mf.cycles=5;mf.e_tot=-3.
        row=r.converged_residual(mf,env['s1e'],self.base/'final.npz')
        self.assertEqual(mf.get_fock.call_count,1);self.assertIs(mf.get_fock.call_args.kwargs['dm'],env['dm'])
        self.assertEqual(row['full_unscaled_solvent_gradient'],.5)
    def test_terminal_acceptance_fails_closed(self):
        self.assertTrue(r.result_accepted(OK,self.passed()))
        for key in OK:
            receipt=OK.copy();del receipt[key];self.assertFalse(r.result_accepted(receipt,self.passed()))
        for value in (False,0.,None):
            receipt={**OK,'returncode':value};self.assertFalse(r.result_accepted(receipt,self.passed()))
        for checks in (None,[],[None],{}, {'only_one':True},{**dict.fromkeys(r.CHECKS,True),'extra':True}):
            result=self.passed();result['checks']=checks;self.assertFalse(r.result_accepted(OK,result))
        for key in ('native_converged','final_validation_complete'):
            result=self.passed();result[key]=False;self.assertFalse(r.result_accepted(OK,result))
        result=self.passed();result['SCFs_launched']=True;self.assertFalse(r.result_accepted(OK,result))
    def proof_fixture(self):
        root=self.base/'first';out=root/'run-v1';out.mkdir(parents=True)
        old=self.base/'old';inp=self.base/'input';(old/'run-v1').mkdir(parents=True);inp.mkdir()
        dm=np.diag([2.,0.]);np.savez(old/'run-v1/partial.npz',density=dm,cycle=0);(inp/'P0_A.xyz').write_text('synthetic geometry')
        np.save(out/'J.npy',np.eye(2));self.save(out/'supervisor.json',OK)
        self.save(out/'result.json',{'status':'PASS_BOUNDED_FIRST_J_ONLY','SCFs_launched':0,'checks':{'finite':True},'J_sha256':r.sha(out/'J.npy')})
        with patch.multiple(r.first,BASE=root,OLD=old,INPUT=inp):proof=r.parent_proof(dm)
        return root,old,inp,dm,proof
    def test_parent_npy_proof_binds_file_and_exact_density(self):
        root,old,inp,dm,proof=self.proof_fixture()
        self.assertEqual(proof['density_sha256'],r.handoff.density_digest(dm));self.assertEqual(proof['density_cycle'],0)
        self.assertEqual(proof['density_archive_sha256'],r.sha(old/'run-v1/partial.npz'))
        working=r.handoff.load_verified(proof);working[0,0]=7.
        np.testing.assert_array_equal(np.load(root/'run-v1/J.npy'),np.eye(2))
        result=r.read(root/'run-v1/result.json');result['J_sha256']='0'*64;self.save(root/'run-v1/result.json',result);proof['result_sha256']=r.sha(root/'run-v1/result.json')
        with self.assertRaises(ValueError):r.handoff.verify_provenance(proof)
    def test_root_gate_binds_method_history_and_review(self):
        root,old,inp,dm,proof=self.proof_fixture();pins={'saved_J_qualification':{'audit':'hash'}}
        self.save(self.base/'preparation.json',{'pins':pins,'proof':proof})
        review={'status':'APPROVED_ONE_PARENT_SAVED_J_PILOT','independent_root_review':True,'reviewer':'synthetic',
                'preparation_sha256':r.sha(self.base/'preparation.json'),'saved_J_qualification_artifacts':pins['saved_J_qualification']}
        self.save(self.base/'independent-root-review.json',review)
        with patch.multiple(r.first,BASE=root,OLD=old,INPUT=inp),patch.object(r,'manifest',return_value=pins):
            self.assertIn('review_sha256',r.validate_gate())
            for key,value in (('independent_root_review',False),('preparation_sha256','wrong'),('saved_J_qualification_artifacts',{})):
                self.save(self.base/'independent-root-review.json',{**review,key:value})
                with self.assertRaises(ValueError):r.validate_gate()
            self.save(self.base/'independent-root-review.json',review)
            changed=copy.deepcopy(proof);changed['method']['max_cycle']=3
            self.save(self.base/'preparation.json',{'pins':pins,'proof':changed})
            with self.assertRaises(ValueError):r.validate_gate()
    def test_prerequisite_review_and_child_receipts_are_mandatory(self):
        small=self.base/'small';out=small/'run-v1';audit=self.base/'audit';audit.mkdir()
        gate={'prep':'synthetic'};terminal={'status':'PASS_RETROSPECTIVE_SAVED_J_HANDOFF','gate_unchanged':True,
             'SCF_skipped':False,'errors':{},'receipts':{},'results':{}}
        self.save(out/'launch-gate.json',gate);self.save(out/'operator-receipt.json',OK)
        for name in ('run.py','handoff.py','test_run.py','PROTOCOL.md','preparation.json','independent-root-review.json'):
            (small/name).write_text('synthetic source/pin')
        review=small/'INDEPENDENT_REVIEW.md';review.write_text('codeQualityStatus: CLEAR\nrecommendation: APPROVE\nblockers: []\n')
        (audit/'check_arrays.py').write_text('synthetic saved-array audit');self.save(audit/'array-audit.json',{'operators':{},'scf':{}})
        for phase in ('operators','scf'):
            result={'case':'new-external','phase':phase,'status':'PASS_'+phase.upper(),'SCFs_launched':int(phase=='scf'),'checks':[{'pass':True}]}
            self.save(out/phase/'supervisor.json',OK);self.save(out/phase/'result.json',result)
            for name in ('arrays.npz','runtime-observation.json','native.log'):(out/phase/name).write_text('synthetic artifact')
            terminal['receipts'][phase]=OK;terminal['results'][phase]=result
        self.save(out/'launch-result.json',terminal)
        with patch.multiple(r,SMALL=small,AUDIT=audit),patch.object(r.small,'validate_gate',return_value=gate):
            pins=r.prerequisites();self.assertIn(str(review),pins);self.assertIn(str(audit/'array-audit.json'),pins)
            review.write_text('codeQualityStatus: BLOCK\nrecommendation: REQUEST_CHANGES\nblockers: []\n')
            with self.assertRaises(ValueError):r.prerequisites()
            review.write_text('codeQualityStatus: CLEAR\nrecommendation: APPROVE\nblockers: []\n')
            broken=copy.deepcopy(terminal);broken['receipts']=None;self.save(out/'launch-result.json',broken)
            with self.assertRaises(ValueError):r.prerequisites()
            self.save(out/'launch-result.json',terminal);result=copy.deepcopy(terminal['results']['scf']);result['checks']=[None]
            self.save(out/'scf/result.json',result)
            with self.assertRaises(ValueError):r.prerequisites()

    def launch_fixture(self,result=None,missing=(),receipt=None,malformed=False):
        qual=self.base/'qual';self.save(qual/'preparation.json',{'pins':{'runtime':{'python':'SYNTHETIC-NO-EXECUTION'}}})
        calls=[]
        def monitored(command,directory,wall,rss):
            calls.append((command,wall,rss))
            for name in r.REQUIRED_EVIDENCE:
                if name not in missing:(directory/name).write_text('synthetic nonempty evidence')
            if malformed:(directory/'result.json').write_text('{truncated')
            else:self.save(directory/'result.json',self.passed() if result is None else result)
            self.save(directory/'supervisor.json',OK if receipt is None else receipt)
            return OK if receipt is None else receipt
        supervisor=types.SimpleNamespace(THREADS={'OPENBLAS_NUM_THREADS':'1'},monitored_run=monitored)
        return qual,calls,supervisor
    def do_launch(self,qual,supervisor):
        with patch.object(r.first,'QUAL',qual),patch.object(r,'validate_gate',return_value={'synthetic':'review'}),patch.object(r,'load',return_value=supervisor):
            return r.launch()
    def test_launcher_one_bounded_child_and_required_artifacts(self):
        qual,calls,sup=self.launch_fixture();self.assertEqual(self.do_launch(qual,sup),0)
        self.assertEqual(len(calls),1);self.assertEqual(calls[0][1:],(1800,10*2**30));self.assertEqual(sup.THREADS['OMP_NUM_THREADS'],'4')
        self.assertTrue(r.read(self.base/'run-v1/launch-result.json')['required_evidence_present'])
        with self.assertRaises(FileExistsError):self.do_launch(qual,sup)
        self.assertEqual(len(calls),1)
    def test_launcher_missing_final_checkpoint_cannot_pass(self):
        qual,calls,sup=self.launch_fixture(missing=('final-validated-state.npz',));self.assertEqual(self.do_launch(qual,sup),1)
        self.assertFalse(r.read(self.base/'run-v1/launch-result.json')['required_evidence_present'])
    def test_launcher_preserves_receipt_when_result_truncated(self):
        qual,calls,sup=self.launch_fixture(malformed=True);self.assertEqual(self.do_launch(qual,sup),1)
        terminal=r.read(self.base/'run-v1/launch-result.json');self.assertEqual(terminal['receipt'],OK);self.assertIn('result',terminal['errors'])
        self.assertIn('latest-complete-cycle.npz',terminal['available_evidence'])
    def test_launcher_preserves_receipt_when_evidence_hash_fails(self):
        qual,calls,sup=self.launch_fixture();original=r.sha
        def failing(path):
            if Path(path).name=='native-final-state.npz':raise OSError('simulated evidence read failure')
            return original(path)
        with patch.object(r,'sha',side_effect=failing):self.assertEqual(self.do_launch(qual,sup),1)
        terminal=r.read(self.base/'run-v1/launch-result.json');self.assertEqual(terminal['receipt'],OK);self.assertIn('native-final-state.npz',terminal['errors'])
    def test_timeout_after_native_convergence_remains_incomplete(self):
        receipt={**OK,'returncode':-15,'termination_reason':'WALL_TIMEOUT'}
        result=self.passed();result['final_validation_complete']=False
        qual,calls,sup=self.launch_fixture(result=result,receipt=receipt);self.assertEqual(self.do_launch(qual,sup),1)
        self.assertEqual(r.read(self.base/'run-v1/launch-result.json')['receipt'],receipt)
    def test_launcher_supervisor_error_still_has_terminal_record(self):
        qual,calls,sup=self.launch_fixture();sup.monitored_run=Mock(side_effect=OSError('synthetic monitor failure'))
        self.assertEqual(self.do_launch(qual,sup),1)
        terminal=r.read(self.base/'run-v1/launch-result.json');self.assertIn('supervisor',terminal['errors']);self.assertEqual(terminal['receipt']['termination_reason'],'SUPERVISOR_ERROR')
    def test_checkpoint_serialization_receives_original_array_references(self):
        mf=self.fake_mf();env=self.env()
        with patch.object(r,'atomic_npz') as writer:
            r.checkpoint(mf,env,self.base/'cycle.npz','completed_callback')
        arrays=writer.call_args.kwargs
        for saved,source in (('density','dm'),('mo_coeff','mo_coeff'),('mo_occ','mo_occ'),('fock','fock'),('overlap','s1e')):
            self.assertIs(arrays[saved],env[source])
    def test_worker_passes_same_immutable_density_to_handoff_and_kernel(self):
        # Exercise real worker setup with synthetic modules; stop on kernel entry.
        class ReachedKernel(Exception):pass
        density=np.diag([1560.,0.]);captured={};out=self.base/'run-v1';out.mkdir()
        gate={'synthetic':'review'};self.save(out/'launch-gate.json',gate)
        self.save(self.base/'preparation.json',{'proof':{'density_sha256':r.handoff.density_digest(density)}})
        qual=self.base/'qual';self.save(qual/'preparation.json',{'pins':{'runtime':{'python':'synthetic'}}})
        mol=types.SimpleNamespace(natm=196,nao=3068,nelectron=1568,charge=-8,spin=0)
        def kernel(*,dm0):
            captured['kernel']=dm0;captured['entries']=captured.get('entries',0)+1;captured['max_cycle']=mf.max_cycle
            mf.saved_J_hits=1;mf._rij_calls=0
            solvent._intermediates={'synthetic_built':True}
            mf.pre_kernel({'dm':dm0,'s1e':np.eye(2),'e_tot':-3.,'vhf':types.SimpleNamespace(e_solvent=-.1,v_solvent=np.eye(2))})
            env={'dm':dm0,'s1e':np.eye(2),'e_tot':-3.,'cycle':0,'mo_coeff':np.eye(2),'mo_occ':np.array([1560.,0.]),'fock':np.eye(2)}
            mf.callback(env)
            mf.post_kernel(dict(env,dm=np.diag([1568.,0.]),e_tot=-3.1,scf_conv=False))
            raise ReachedKernel()
        mf=types.SimpleNamespace(mol=mol,_rij_df=types.SimpleNamespace(auxbasis='def2-universal-jkfit',_vjopt=None,_cderi=None,_cderi_to_save=None),
             grids=types.SimpleNamespace(),_eri=None,_chkfile=None,get_jk=Mock(),get_veff=Mock(),get_grad=lambda c,o,f:np.zeros(1),kernel=kernel)
        native_j=mf.get_jk;native_veff=mf.get_veff
        solvent=types.SimpleNamespace(ao_block=1,build=Mock(),_get_vind=Mock())
        def attach(obj,s):obj.with_solvent=s;return obj
        memory=types.SimpleNamespace(factor_inplace=Mock(),private_scipy=types.SimpleNamespace(linalg=types.SimpleNamespace(cho_factor=Mock())),
                MemoryPCM=Mock(return_value=solvent),qualified=types.SimpleNamespace(attach=attach),install=lambda obj,metric:obj)
        pyscf=types.SimpleNamespace(dft=types.SimpleNamespace(RKS=lambda m:mf),gto=types.SimpleNamespace(M=lambda **kw:mol),lib=types.SimpleNamespace(num_threads=lambda:4))
        def install(obj,dm,proof):captured['handoff']=dm;return obj
        environment={k:'1' for k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')}
        environment.update(OMP_NUM_THREADS='4',OMP_DYNAMIC='FALSE')
        with patch.dict(r.sys.modules,{'pyscf':pyscf}),patch.dict(r.os.environ,environment),\
             patch.object(r,'validate_gate',return_value=gate),patch.object(r,'load',return_value=memory),\
             patch.object(r.first,'QUAL',qual),patch.object(r.first.qualification,'runtime_pins',return_value={'python':'synthetic'}),\
             patch.object(r.first,'saved_density',return_value=(density,{'synthetic':True})),patch.object(r.first,'parent_atoms',return_value=[]),\
             patch.object(r.handoff,'install',side_effect=install):
            with self.assertRaises(ReachedKernel):r.worker()
        self.assertIs(captured['handoff'],density);self.assertIs(captured['kernel'],density)
        self.assertFalse(density.flags.writeable);native_j.assert_not_called();native_veff.assert_not_called()
        self.assertEqual(r.read(out/'initial-potential.json')['electron_trace'],1560.)
        self.assertEqual(captured['entries'],1);self.assertEqual(captured['max_cycle'],20)
        with np.load(out/'latest-complete-cycle.npz') as ordinary,np.load(out/'native-final-state.npz') as final:
            self.assertEqual(float(ordinary['electron_trace']),1560.);self.assertEqual(float(final['electron_trace']),1568.)
            self.assertEqual(str(final['kind']),'native_post_kernel')
        self.assertFalse(r.read(out/'result.json')['native_final_state']['native_converged'])



if __name__=='__main__':unittest.main()
