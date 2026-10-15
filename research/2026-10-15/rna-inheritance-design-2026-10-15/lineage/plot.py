"""Plot every registered threshold and the worst null acceptance."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def main(directory):
    summary=json.loads((directory/'summary.json').read_text())
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    colors=('#996633','#136a92','#9f4077')
    titles=('0.524 pL, 1 fmol LOQ','1000 pL, 1 fmol LOQ','1000 pL, 0.01 fmol LOQ')
    for pi,ax in enumerate(axes.flat[:3]):
        for threshold,color in zip((.5,1.,2.),colors):
            rows=sorted((r for r in summary if r['world']=='strong' and r['platform']==pi and r['threshold_um']==threshold),key=lambda r:r['n'])
            x=[r['n'] for r in rows];y=np.array([r['rate'] for r in rows])
            errors=np.array([[r['rate']-r['wilson'][0] for r in rows],[r['wilson'][1]-r['rate'] for r in rows]])
            ax.errorbar(x,y,yerr=errors,label=f'{threshold:g} µM state threshold',color=color,marker='o',capsize=3)
        ax.axhline(.8,color='gray',linestyle='--',linewidth=1)
        ax.set(title='Strong renewal: '+titles[pi],xlabel='Independent roots per history × arm',ylabel='Joint g5 + g6 acceptance',ylim=(-.03,1.05),xticks=[24,48,96])
        ax.legend(fontsize=8,loc='center right')
    ax=axes.flat[3]
    worlds=sorted({r['world'] for r in summary if r['world'] not in ('strong','weak')})
    maxima=[max(r['wilson'][1] for r in summary if r['world']==w) for w in worlds]
    estimates=[max(r['rate'] for r in summary if r['world']==w) for w in worlds]
    ax.barh(worlds,maxima,color='#d5e4eb',label='Largest Wilson upper bound')
    ax.scatter(estimates,worlds,color='#174b63',label='Largest observed acceptance',zorder=3)
    ax.axvline(.05,color='gray',linestyle='--',linewidth=1)
    ax.set(xlim=(0,.1),xlabel='Maximum over all N, platforms and thresholds',title='Seven null worlds; 128 experiments per condition')
    ax.legend(fontsize=8,loc='lower right')
    fig.suptitle('Conditional six-generation F1 experiment design\nSimulated chemistry and assay qualification; no physical inheritance demonstrated',fontsize=14)
    fig.savefig(directory/'design-performance.png',dpi=160)
    plt.close(fig)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path)
    main(parser.parse_args().directory)
