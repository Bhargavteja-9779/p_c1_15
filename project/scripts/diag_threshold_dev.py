import sys; sys.path.insert(0,'.')
import numpy as np, json
from concurrent.futures import ProcessPoolExecutor
from src.data import load_project
from src.jit import simulate
from sklearn.metrics import roc_curve
def one(a):
    proj,m,kw=a
    df=load_project(proj); y=df.y.to_numpy()
    o=simulate(df,m,seed=0,return_preds=True,**kw); ev=o["eval_mask"]
    fpr,tpr,_=roc_curve(y[ev],o["prob"][ev]); best=np.max(np.sqrt(tpr*(1-fpr)))
    r=o["metrics"]; return (proj,m+str(kw),round(r["gmean"],3),round(best,3),round(r["auc"],3),round(float(np.mean(o["pred"][ev])),3),round(float(y[ev].mean()),3))
import os
CAL=os.environ.get("CAL")=="1"
jobs=[(p,m,dict(kw,**({"thr_cal":True} if CAL else {}))) for p in os.environ.get("PROJ","neutron,fabric").split(",") for m,kw in [("oracle",{}),("nowait",{}),("wait",{"W":30}),("wait",{"W":90}),("wait",{"W":180}),("law",{"prior":"base"}),("law",{"prior":"model"})]]
with ProcessPoolExecutor(1) as ex:
    for r in ex.map(one,jobs): print(r,flush=True)
