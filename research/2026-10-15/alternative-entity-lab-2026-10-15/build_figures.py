"""Plot accepted model outcomes separately from measured component observations."""

import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent


def main():
    integrated = json.loads((ROOT/"integrated/results-v1.2/summary.json").read_text())
    heredity = json.loads((ROOT/"heredity/results-v1/results.json").read_text())
    measured = json.loads((ROOT/"research/results.json").read_text())
    output = ROOT/"figures"
    output.mkdir(exist_ok=True)
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,"figure.facecolor":"#fafaf7","axes.facecolor":"#fafaf7"})
    fig, axes = plt.subplots(1,2,figsize=(12,4.8),layout="constrained")
    arms = ["adaptive","reactive","random","erase_cue","no_update","offspring_shuffle"]
    values = [integrated["evaluation"]["primary"]["arms"][a]["mean_accuracy"] for a in arms]
    axes[0].barh(np.arange(len(arms)),np.array(values)*100,color=["#187b80"]+["#929eac"]*5)
    axes[0].set(yticks=np.arange(len(arms)),yticklabels=["Adaptive","Reactive","Random","Cue erased","No updating","Offspring shuffled"],xlim=(0,105),xlabel="Evaluation accuracy (%)",title="Supplied integrated model: primary condition")
    axes[0].invert_yaxis()
    for i,value in enumerate(values):
        axes[0].text(value*100+1,i,f"{value:.1%}",va="center",fontsize=9)
    cases = ["primary","long_delay","scarce_feed"]
    passed = [integrated["evaluation"][c]["integration_seeds_passed"] for c in cases]
    axes[1].bar(np.arange(3),passed,color=["#187b80","#c18a37","#bd6352"])
    axes[1].set(xticks=np.arange(3),xticklabels=["Primary","Long delay","Scarce feed"],ylim=(0,13),yticks=[0,3,6,9,12],ylabel="Seeds passing the complete criterion (of 12)",title="Failure under changed conditions")
    for i,value in enumerate(passed):
        axes[1].text(i,value+0.25,str(value),ha="center")
    fig.suptitle("Model behavior only: supplied learning, templating, division and work yields",fontsize=12)
    fig.savefig(output/"integrated-outcomes.png",dpi=180)
    plt.close(fig)

    fig,ax = plt.subplots(figsize=(7.2,4.5),layout="constrained")
    conditions = heredity["conditions"]
    grid = np.array([r["successes"] for r in conditions]).reshape(3,3)
    ax.imshow(grid,vmin=0,vmax=12,cmap="YlGnBu")
    ax.set(xticks=[0,1,2],xticklabels=[16,64,128],yticks=[0,1,2],yticklabels=["0%","5%","25%"],xlabel="Resource tokens per passage",ylabel="Supplied copying error",title="Conditional transmission: seeds passing (of 12)")
    for (i,j),value in np.ndenumerate(grid):
        ax.text(j,i,f"{value}/12",ha="center",va="center",color="white" if value>7 else "#162736",fontsize=14)
    fig.savefig(output/"heredity-envelope.png",dpi=180)
    plt.close(fig)

    fig,axes = plt.subplots(1,2,figsize=(11,4.7),layout="constrained")
    names = ["kArg-kArg-Control","kArg-kArg-Click"]
    values = [measured["lifetime_min"][n] for n in names]
    axes[0].bar([0,1],[v["mean"] for v in values],color=["#929eac","#187b80"],width=.55)
    for i,v in enumerate(values):
        axes[0].plot([i,i],[v["min"],v["max"]],color="#162736",marker="_",linewidth=2)
    axes[0].set(xticks=[0,1],xticklabels=["KR Control","KR Click"],ylabel="Author-defined lifetime (minutes)",title="Measured chemical component; n = 2 each")
    memory = measured["physical_memory"]
    for i,v in enumerate(memory):
        axes[1].plot([0,4],[v["past_high_minus_low_initial_A"]*1e9,v["past_high_minus_low_terminal_A"]*1e9],marker="o",label=f"Present illumination {1.0 if i==0 else 0.5}")
    axes[1].set(xlim=(-.2,4.2),ylim=(0,6),xlabel="Time in pulse (seconds)",ylabel="High-past minus low-past current (nA)",title="Measured device history effect")
    axes[1].legend(fontsize=9)
    fig.suptitle("Separate measured systems; neither dataset calibrates the entity simulation",fontsize=12)
    fig.savefig(output/"measured-components.png",dpi=180)
    plt.close(fig)
    print("Created three figures from accepted results.")


if __name__ == "__main__":
    main()
