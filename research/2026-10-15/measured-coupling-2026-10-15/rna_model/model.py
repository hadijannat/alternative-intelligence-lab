"""Measured-condition R3C propagation: effective kinetics, explicit RNA inventories."""
from dataclasses import dataclass, asdict
import numpy as np
from scipy.integrate import solve_ivp

NAMES = ("HyperA", "Cy5A", "B", "F1", "Cy5F1", "inactive_product")
MOIETIES = np.array([[1,0,0,1,0,1], [0,1,0,0,1,0], [0,0,1,1,1,1]], dtype=float)

@dataclass(frozen=True)
class Parameters:
    k: float
    kb: float
    ki: float
    mixing: float = .5
    retention: float = .55
    rho: float = 1.

def react(states, minutes, p, regeneration=True, rtol=1e-8, times=None):
    """Units are µM and minutes; reporter product never enters catalytic activity."""
    states = np.asarray(states, dtype=float)
    shape = states.shape
    def rhs(t, flat):
        x=np.maximum(flat.reshape(shape),0)
        a,r,b,f,report,d=x.T
        inhibition=1+(report+f+d)/p.ki
        va=p.k*f*a*b/inhibition+p.kb*a*a*b*b
        vr=p.rho*p.k*f*r*b/inhibition
        return np.stack((-va,-vr,-va-vr,va if regeneration else np.zeros_like(va),
                         vr,np.zeros_like(va) if regeneration else va),axis=1).ravel()
    sol=solve_ivp(rhs,(0,float(minutes)),states.ravel(),t_eval=times,
                  rtol=rtol,atol=rtol*1e-2,method="DOP853")
    if not sol.success: raise RuntimeError(sol.message)
    if np.min(sol.y)<-1e-6: raise ArithmeticError("Negative chemical concentration")
    if times is not None:
        return np.maximum(sol.y.T.reshape((-1,*shape)),0)
    return np.maximum(sol.y[:,-1].reshape(shape),0)

def bulk_curve(p, seed=0., hyper=0., times=(0,15,30,45,60)):
    x=np.array([[hyper,5.,7.5,seed,0.,0.]])
    trajectory=react(x,max(times),p,times=list(times))[:,0,:]
    return 100*trajectory[:,4]/(trajectory[:,1]+trajectory[:,4])

def initial(seed):
    return np.array([[0,0,0,seed,0,0], [10,2.5,0,0,0,0], [0,0,15,0,0,0]],float),np.ones(3)/3

def exchange(x,w,p,n):
    if not 0<=p.mixing<=1 or not 0<p.retention<=1: raise ValueError("Invalid mixing/retention")
    initial_inventory=w@x
    percycle=p.retention**(1/3)
    for _ in range(n): x=percycle*((1-p.mixing)*x+p.mixing*(w@x)[None,:])
    return x, initial_inventory-w@x

def reporter(x,w):
    inventory=w@x
    denominator=inventory[1]+inventory[4]
    return 100*inventory[4]/denominator if denominator>0 else 0.

def single_cycle(p,seed,n,regeneration=True,rtol=1e-8):
    x,w=initial(seed)
    x,_=exchange(x,w,p,n)
    x=react(x,60,p,regeneration,rtol)
    return reporter(x,w)

def serial(p,seed,generations=7,regeneration=True,feed=True,rtol=1e-8):
    x,w=initial(seed)
    source_total=w@x
    removed=np.zeros(6)
    rows=[]
    def append(g):
        inventory=w@x
        residual=MOIETIES@(source_total-removed-inventory)
        rows.append(dict(generation=g,yield_percent=reporter(x,w),
                         **{name+"_uM":float(value) for name,value in zip(NAMES,inventory)},
                         founder_F1_upper_bound_uM=float(seed/3 if g==0 else seed/3*p.retention**g*.5**(g-1)),
                         newly_generated_F1_model_uM=float(inventory[3]-(seed/3 if g==0 else seed/3*p.retention**g*.5**(g-1))),
                         moiety_balance_max_error_uM=float(np.max(np.abs(residual))),
                         input_nucleotide_uM=float(np.array([52,52,14])@MOIETIES@source_total),
                         removed_nucleotide_uM=float(np.array([52,52,14])@MOIETIES@removed),
                         retained_nucleotide_uM=float(np.array([52,52,14])@MOIETIES@inventory),
                         cohorts=len(w)))
    append(0)
    for g in range(1,generations+1):
        if g>1:
            removed+=.5*(w@x)
            w*=.5
            fresh=np.array([[10,2.5,0,0,0,0],[0,0,15,0,0,0]],float) if feed else np.zeros((2,6))
            source_total+=.25*fresh.sum(axis=0)
            x=np.vstack((x,fresh));w=np.concatenate((w,[.25,.25]))
        x,lost=exchange(x,w,p,3);removed+=lost
        x=react(x,60,p,regeneration,rtol)
        append(g)
    return rows
