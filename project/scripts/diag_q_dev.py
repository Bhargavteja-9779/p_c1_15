import sys; sys.path.insert(0,'.')
import numpy as np
from src.data import load_project
from src.jit import simulate, DAY
for proj in ["neutron","fabric"]:
    df=load_project(proj)
    t=df.t.to_numpy(); tf=df.t_found.to_numpy(); y=df.y.to_numpy()
    d=(tf[y==1]-t[y==1])/DAY; d=d[np.isfinite(d)]
    print(proj,"n",len(df),"bug_rate %.3f"%y.mean(),"delay median %.0f p90 %.0f"%(np.median(d),np.percentile(d,90)), "span days %.0f"%((t.max()-t.min())/DAY))
    for prior in ["base","model"]:
        o=simulate(df,"law",seed=0,prior=prior,label_noise_log=True)
        dg=o["diag"]; qb=np.nanmean([x["mean_q_true_bug"] for x in dg]); qc=np.nanmean([x["mean_q_clean"] for x in dg])
        print("  law",prior,o["metrics"]["gmean"].__round__(3),"mean q | undiscovered true bug %.3f | true clean %.3f"%(qb,qc))
