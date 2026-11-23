#!/usr/bin/env python3
"""Deterministic style-metric gate. Usage: check_style_v1.py style_targets_v1.json IMG [IMG...]  -> JSON on stdout.
Pixels only (Oracle Validity): never reads prompts."""
import sys,json,os,numpy as np,cv2
T=json.load(open(sys.argv[1])); H=T['hard_gates_per_image']; S=T['soft_targets_per_image']
def stats(p):
    im=cv2.imread(p); im=cv2.resize(im,(1344,max(1,round(1344*im.shape[0]/im.shape[1]))),interpolation=cv2.INTER_AREA)
    g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32); hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV); lab=cv2.cvtColor(im,cv2.COLOR_BGR2LAB).astype(np.float32)
    lap=cv2.Laplacian(g,cv2.CV_32F); h,w=g.shape
    return dict(luma=float(g.mean()),black_p1=float(np.percentile(g,1)),white_p99=float(np.percentile(g,99)),sat=float(hsv[...,1].mean()),
                a=float(lab[...,1].mean()-128),b=float(lab[...,2].mean()-128),sharp_c=float(lap[h//4:3*h//4,w//4:3*w//4].var()))
inr=lambda v,r:r[0]<=v<=r[1]
out=[]
for p in sys.argv[2:]:
    m=stats(p)
    hard={"white_p99":m['white_p99']>=H['white_p99_min'],"black_p1":m['black_p1']<=H['black_p1_max'],"luma":inr(m['luma'],H['luma_range']),
          "sat":inr(m['sat'],H['sat_range']),"a":inr(m['a'],H['a_range']),"b":inr(m['b'],H['b_range']),"sharp_c":inr(m['sharp_c'],H['sharp_c_range'])}
    soft={"white_p99":inr(m['white_p99'],S['white_p99']),"black_p1":m['black_p1']<=S['black_p1_max'],"sat":inr(m['sat'],S['sat']),"sharp_c":inr(m['sharp_c'],S['sharp_c'])}
    out.append(dict(image=os.path.basename(p),metrics={k:round(v,2) for k,v in m.items()},hard=hard,hard_pass=all(hard.values()),soft=soft,soft_pass_count=sum(soft.values())))
json.dump({"targets":T['version'],"n":len(out),"hard_pass_n":sum(o['hard_pass'] for o in out),"results":out},sys.stdout,indent=1)
