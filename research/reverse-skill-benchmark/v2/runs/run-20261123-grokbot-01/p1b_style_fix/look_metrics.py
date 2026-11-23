import json,glob,os,numpy as np,cv2,statistics as st
P='/workspace/hs-bench-private/run-20261123-grokbot-01'
def stats(p):
    im=cv2.resize(cv2.imread(p),(1344,752),interpolation=cv2.INTER_AREA)
    g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32)
    hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV); lab=cv2.cvtColor(im,cv2.COLOR_BGR2LAB).astype(np.float32)
    lap=cv2.Laplacian(g,cv2.CV_32F); h,w=g.shape
    c=float(lap[h//4:3*h//4,w//4:3*w//4].var()); e=float(np.concatenate([lap[:h//6].ravel(),lap[-h//6:].ravel()]).var())
    return dict(luma=float(g.mean()),black_p1=float(np.percentile(g,1)),white_p99=float(np.percentile(g,99)),sat=float(hsv[...,1].mean()),
      a=float(lab[...,1].mean()-128),b=float(lab[...,2].mean()-128),sharp_c=c,edge_ratio=e/c)
refs={os.path.basename(f)[:3]:f for f in glob.glob(P+'/refs/masked/*.png')}
out={'refs':{},'P1':{},'P1b':{}}
for c,f in refs.items(): out['refs'][c]=stats(f)
for f in sorted(glob.glob(P+'/output/*.png')): out['P1'][os.path.basename(f)[:-4]]=stats(f)
for f in sorted(glob.glob(P+'/output_p1b/*.png')): out['P1b'][os.path.basename(f)[:-4]]=stats(f)
json.dump(out,open('/workspace/hs-bench-review/lookgap/look_metrics_p1_p1b.json','w'),indent=1)
print(sorted(refs))
M=['luma','black_p1','white_p99','sat','a','b','sharp_c','edge_ratio']
rows=[]
for c in sorted(refs):
    R=out['refs'][c]
    p1=[v for k,v in out['P1'].items() if f'-{c}-' in k]; pb=[v for k,v in out['P1b'].items() if f'-{c}-' in k]
    for m in M:
        a=st.mean(x[m] for x in p1); b=st.mean(x[m] for x in pb)
        g1=abs(a-R[m]); g2=abs(b-R[m]); clo=(1-g2/g1)*100 if g1>1e-9 else float('nan')
        rows.append((c,m,R[m],a,min(x[m] for x in p1),max(x[m] for x in p1),b,min(x[m] for x in pb),max(x[m] for x in pb),clo))
        print(f"{c} {m:10s} ref {R[m]:8.2f} | P1 {a:8.2f} [{min(x[m] for x in p1):.2f}-{max(x[m] for x in p1):.2f}] | P1b {b:8.2f} [{min(x[m] for x in pb):.2f}-{max(x[m] for x in pb):.2f}] | gap {g1:7.2f}->{g2:7.2f} closed {clo:6.0f}%")
json.dump([dict(zip(['case','metric','ref','p1_mean','p1_min','p1_max','p1b_mean','p1b_min','p1b_max','gap_closed_pct'],r)) for r in rows],open('/workspace/hs-bench-review/lookgap/look_delta_summary.json','w'),indent=1)
# per skill paired: P1 mean of replicates vs P1b
print('--- per cell |gap| luma / sharp_c / edge_ratio / black_p1 : P1 -> P1b')
for k,v in out['P1b'].items():
    c=k.split('-')[1]; s=k.split('-')[2]; R=out['refs'][c]
    p=[x for kk,x in out['P1'].items() if f'-{c}-{s}-' in kk]
    s1=' '.join(f"{m}:{abs(st.mean(x[m] for x in p)-R[m]):.2f}->{abs(v[m]-R[m]):.2f}" for m in ['luma','sharp_c','edge_ratio','black_p1','b'])
    print(k,s1)
