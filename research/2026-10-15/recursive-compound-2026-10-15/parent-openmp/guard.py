import json,os,pathlib,signal,subprocess,sys,time
p=pathlib.Path(__file__).resolve().parent
e=os.environ.copy()
e.update(MAMBA_ROOT_PREFIX=str(p/'mamba-root'),CONDA_PKGS_DIRS=str(p/'pkgs'),TMPDIR=str(p/'tmp'),XDG_CACHE_HOME=str(p/'cache'))
(p/'tmp').mkdir(exist_ok=True)
mode=sys.argv[1]
a=[str(p/'bin/micromamba'),'create','--no-rc','-y','-p',str(p/'env'),'-c','conda-forge','--override-channels','python=3.11','pyscf=2.14.0=py311h47f6db6_102']
if mode=='solve': a+=['--dry-run','--json']
else: a=[str(p/'bin/micromamba'),'create','--no-rc','-y','-p',str(p/'env'),'--file',str(p/'explicit-spec.txt')]
t=time.monotonic(); sizes=[]; reason=None
with (p/(mode+'.stdout')).open('w') as out,(p/(mode+'.stderr')).open('w') as err:
 c=subprocess.Popen(a,env=e,stdout=out,stderr=err,start_new_session=True)
 while c.poll() is None:
  size=sum(f.stat().st_size for f in p.rglob('*') if f.is_file() and not f.is_symlink())
  sizes.append(size)
  if size>2_000_000_000 or time.monotonic()-t>300:
   reason='disk' if size>2_000_000_000 else 'time';os.killpg(c.pid,signal.SIGTERM);c.wait(timeout=10);break
  time.sleep(1)
r={'command':a,'environment_overrides':{k:e[k] for k in ['MAMBA_ROOT_PREFIX','CONDA_PKGS_DIRS','TMPDIR','XDG_CACHE_HOME']},'returncode':c.returncode,'elapsed_seconds':time.monotonic()-t,'max_sampled_logical_bytes':max(sizes,default=0),'termination_reason':reason}
(p/(mode+'-receipt.json')).write_text(json.dumps(r,indent=2));print(json.dumps(r))
assert c.returncode==0 and reason is None
