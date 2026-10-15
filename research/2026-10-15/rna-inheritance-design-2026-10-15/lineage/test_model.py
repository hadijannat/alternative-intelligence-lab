import unittest
import numpy as np
import model

class LineageTests(unittest.TestCase):
    def test_complementary_partition(self):
        x = np.arange(2*3*12,dtype=np.int64).reshape(2,3,12)
        d,f = model.partition(x,np.random.default_rng(1))
        np.testing.assert_array_equal(d.reshape(2,3,2,12).sum(axis=2),x)
        np.testing.assert_allclose(f.reshape(2,3,2).sum(axis=2),1)

    def test_all_worlds_conserve(self):
        for i,world in enumerate(model.WORLDS):
            pools,groups,batches,ledger,records=model.simulate(world,.524,np.random.default_rng(i),n=8,pedigree=True)
            self.assertEqual(pools[5][0].shape,(32,12))
            self.assertTrue(np.all(pools[5][1]==16*.524))
            self.assertTrue(np.all(pools[6][1]==32*.524))
            self.assertEqual(model.validate_pedigree(records)['roots'],4)
            np.testing.assert_array_equal(np.array(ledger['initial'])+ledger['supplied'],
                np.array(ledger['terminal_samples'])+ledger['external_loss'])

    def test_no_regeneration_controls(self):
        for world in ('founder_only','reporter_only','no_founder'):
            pools,*_=model.simulate(world,1000,np.random.default_rng(11),n=8)
            for stock,_ in pools.values(): self.assertFalse(stock[:,2:6].any())
        pools,*_=model.simulate('inactive_new',1000,np.random.default_rng(11),n=8)
        self.assertGreater(pools[6][0][:,5].sum(),0)
        self.assertEqual(pools[6][0][:,4].sum(),0)

    def test_destructive_pedigree_rejects_continuation(self):
        *_,records=model.simulate('strong',.524,np.random.default_rng(2),n=8,pedigree=True)
        records[0]['sampled']=True
        with self.assertRaises(AssertionError): model.validate_pedigree(records)

    def test_observation_and_missing(self):
        pools,group,batch,*_=model.simulate('strong',.524,np.random.default_rng(1),n=8)
        rows=model.observe_pools(pools,group,batch,1,np.random.default_rng(2),0)
        self.assertEqual(rows.shape,(64,len(model.FIELDS)))
        self.assertEqual(rows[:,model.FIELDS.index('detected')].sum(),0)
        result=model.decisions(rows,8,max_n=8)
        self.assertFalse(result['passed'])
        rows[:,model.FIELDS.index('new_lower')]=0
        rows[:,model.FIELDS.index('new_upper')]=np.nan
        self.assertFalse(model.decisions(rows,8,max_n=8)['passed'])

    def test_shuffle_preserves_batch_and_family(self):
        pools,group,batch,*_=model.simulate('strong',1000,np.random.default_rng(1),n=8)
        rows=model.observe_pools(pools,group,batch,.01,np.random.default_rng(2),0)
        shuffled=model.shuffle_history(rows,8,np.random.default_rng(3),max_n=8)
        model.decisions(shuffled,8,max_n=8)
        for root in range(32):
            assigned=shuffled[shuffled[:,2]==root,1]
            self.assertEqual(len(set(assigned)),1)

    def test_contrast_known_worlds(self):
        rows=np.zeros((64,len(model.FIELDS)))
        c={v:i for i,v in enumerate(model.FIELDS)}
        for g in (5,6):
            for root in range(32):
                r=rows[(g-5)*32+root]
                r[c['root']]=root
                r[c['group']]=root//8
                r[c['batch']]=root%8//2
                r[c['generation']]=g
                r[c['volume_pl']]=1000
                r[c['qualified']]=r[c['detected']]=1
                r[c['new_lower']]=r[c['new_upper']]=2 if root//8==0 else 0
        result=model.decisions(rows,8,max_n=8)
        self.assertTrue(result['passed'])
        self.assertEqual([r['contrast_lower'] for r in result['generations']],[1.,1.])
        rows[:,c['new_lower']]=rows[:,c['new_upper']]=2
        result=model.decisions(rows,8,max_n=8)
        self.assertFalse(result['passed'])
        self.assertEqual([r['contrast_lower'] for r in result['generations']],[0.,0.])

    def test_deterministic_replay(self):
        p1,*_=model.simulate('strong',.524,np.random.default_rng(3),n=8)
        p2,*_=model.simulate('strong',.524,np.random.default_rng(3),n=8)
        for g in p1: np.testing.assert_array_equal(p1[g][0],p2[g][0])

if __name__=='__main__': unittest.main()
