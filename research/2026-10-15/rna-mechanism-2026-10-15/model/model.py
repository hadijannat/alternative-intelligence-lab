"""Conservative reduced RNA ligation hypotheses; concentrations µM, time minutes."""
from dataclasses import dataclass
import numpy as np
from scipy.integrate import solve_ivp

NAMES = ("HyperA", "Cy5A", "B", "F1", "Cy5F1", "inactive_product", "inaccessible_Cy5A")
MOIETIES = np.array([[1,0,0,1,0,1,0], [0,1,0,0,1,0,1], [0,0,1,1,1,1,0]], float)

@dataclass(frozen=True)
class Parameters:
    family: str = "saturation"
    kf: float = .1
    kh: float = 1e-5
    kb: float = 1.
    q: float = 1.
    hroute: int = 0
    ki: float = 1000.
    mixing: float = .1
    transport: str = "fractional"
    retention_f: float = .55
    retention_fragments: float = .55

    def __post_init__(self):
        if self.family not in ("saturation", "original") or self.transport not in ("fractional", "contact"):
            raise ValueError("Unknown chemistry or transport")
        if not all(np.isfinite(v) and v>0 for v in (self.kf,self.kh,self.kb,self.ki)):
            raise ValueError("Kinetic parameters must be positive and finite")
        if not 0<self.q<=1 or self.hroute not in (0,1) or not 0<=self.mixing<=1:
            raise ValueError("Invalid accessible fraction, route, or mixing")
        if not 0<self.retention_f<=1 or not 0<self.retention_fragments<=1:
            raise ValueError("Retention must lie in (0,1]")

def rates(x,p):
    a,r,b,f,report,d,inaccessible=np.maximum(np.asarray(x),0).T
    if p.family=="original":
        inhibition=1+(f+report+d)/p.ki
        return p.kf*f*a*b/inhibition+p.kh*a*a*b*b, p.kf*f*r*b/inhibition
    occupancy=b/(p.kb+b)
    # shortcut: effective complex assembly, upgrade when binding/intermediate assays exist.
    return (p.kf*f*a*occupancy+p.kh*a*a*occupancy**2,
            p.kf*f*r*occupancy+p.hroute*p.kh*a*r*occupancy**2)

def react(states,minutes,p,regeneration=True,rtol=1e-8,times=None):
    states=np.asarray(states,dtype=float)
    if states.ndim!=2 or states.shape[1]!=7 or np.any(~np.isfinite(states)) or np.any(states<0):
        raise ValueError("Expected finite nonnegative cohort-by-seven chemical states")
    if not np.isfinite(minutes) or minutes<0: raise ValueError("Invalid reaction duration")
    if times is not None and (min(times)<0 or max(times)>minutes or any(a>=b for a,b in zip(times,times[1:]))):
        raise ValueError("Observation times must increase within reaction interval")
    if minutes==0: return states[None,:,:] if times is not None else states.copy()
    shape=states.shape
    def rhs(t,flat):
        va,vr=rates(flat.reshape(shape),p)
        zeros=np.zeros_like(va)
        return np.stack((-va,-vr,-va-vr,va if regeneration else zeros,vr,
                         zeros if regeneration else va,zeros),axis=1).ravel()
    sol=solve_ivp(rhs,(0,float(minutes)),states.ravel(),t_eval=times,
                  rtol=rtol,atol=rtol*1e-2,method="DOP853")
    if not sol.success: raise RuntimeError(sol.message)
    if np.min(sol.y)<-1e-6: raise ArithmeticError("Negative chemical concentration")
    return np.maximum(sol.y.T.reshape((-1,*shape)),0) if times is not None else np.maximum(sol.y[:,-1].reshape(shape),0)

def bulk_curve(p,seed=0.,hyper=0.,times=(0,15,30,45,60)):
    x=np.array([[hyper,5*p.q,7.5,seed,0,0,5*(1-p.q)]],float)
    y=react(x,max(times),p,times=list(times))[:,0,:]
    return 100*y[:,4]/(y[:,1]+y[:,4]+y[:,6])

def fresh(p): return np.array([[10,2.5*p.q,0,0,0,0,2.5*(1-p.q)], [0,0,15,0,0,0,0]],float)
def initial(seed,p):
    return np.vstack((np.array([[0,0,0,seed,0,0,0]],float),fresh(p))),np.ones(3)/3

def exchange(x,w,p,n):
    if n<0 or int(n)!=n: raise ValueError("FT count must be a nonnegative integer")
    x=np.array(x,copy=True); w=np.array(w,copy=True)
    if not np.isclose(w.sum(),1) or np.any(w<0): raise ValueError("Cohort weights must sum to one")
    before=w@x
    retention=np.full(7,p.retention_fragments**(1/3))
    retention[[3,5]]=p.retention_f**(1/3)
    for _ in range(int(n)):
        mean=w@x
        if p.transport=="fractional":
            x=(1-p.mixing)*x+p.mixing*mean[None,:]
        elif p.mixing>0:
            x=np.vstack((x,mean)); w=np.append(w*(1-p.mixing),p.mixing)
            keep=w>0; x=x[keep];w=w[keep]
        x*=retention
    return x,w,before-w@x

def reporter(x,w):
    inventory=w@x
    total=inventory[1]+inventory[4]+inventory[6]
    return float(100*inventory[4]/total) if total>0 else 0.

def single_cycle(p,seed,n,regeneration=True,rtol=1e-8):
    x,w=initial(seed,p);x,w,_=exchange(x,w,p,n)
    return reporter(react(x,60,p,regeneration,rtol),w)

def serial(p,seed,generations=7,regeneration=True,rtol=1e-8):
    x,w=initial(seed,p);source=w@x;removed=np.zeros(7);rows=[]
    def append(g):
        inventory=w@x
        founder=seed/3 if g==0 else seed/3*p.retention_f**g*.5**(g-1)
        rows.append(dict(generation=g,yield_percent=reporter(x,w),
                         **{name+"_uM":float(value) for name,value in zip(NAMES,inventory)},
                         founder_F1_upper_bound_uM=founder,
                         newly_generated_F1_model_uM=float(inventory[3]-founder),
                         moiety_balance_max_error_uM=float(np.max(np.abs(MOIETIES@(source-removed-inventory)))),
                         source_moiety_uM=(MOIETIES@source).tolist(),removed_moiety_uM=(MOIETIES@removed).tolist(),
                         retained_moiety_uM=(MOIETIES@inventory).tolist(),cohorts=len(w)))
    append(0)
    for g in range(1,generations+1):
        if g>1:
            removed+=.5*(w@x);w*=.5
            added=fresh(p);source+=.25*added.sum(axis=0)
            x=np.vstack((x,added));w=np.concatenate((w,[.25,.25]))
        x,w,lost=exchange(x,w,p,3);removed+=lost
        x=react(x,60,p,regeneration,rtol);append(g)
    return rows
