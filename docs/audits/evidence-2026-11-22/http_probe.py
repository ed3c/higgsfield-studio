import json,urllib.request,sys,collections,hashlib
B='http://127.0.0.1:8765'
def get(p,h=None):
    r=urllib.request.Request(B+p,headers=h or {});
    try:
        with urllib.request.urlopen(r) as x:return x.status,dict(x.headers),x.read()
    except urllib.error.HTTPError as e:return e.code,dict(e.headers),e.read()
def post(p,body,csrf,h=None):
    d=json.dumps(body).encode();hh={'Content-Type':'application/json','X-Review-CSRF':csrf};hh.update(h or {})
    r=urllib.request.Request(B+p,data=d,headers=hh,method='POST')
    try:
        with urllib.request.urlopen(r) as x:return x.status,json.loads(x.read())
    except urllib.error.HTTPError as e:return e.code,e.read().decode()
out={}
s,h,b=get('/api/health');out['health']=[s,json.loads(b)]
s,h,b=get('/api/bootstrap');bs=json.loads(b);csrf=bs['csrf']
out['bootstrap_keys']=sorted(bs.keys())
items=bs.get('items') or bs.get('entries') or []
if isinstance(items,dict):items=list(items.values())
out['group_counts']=dict(collections.Counter(i.get('group') for i in items))
res=[i for i in items if i.get('group')=='resource']
out['resource_available']=sum(1 for i in res if i.get('available'))
ext=collections.Counter((i.get('name') or i.get('title') or i.get('id','')).rsplit('.',1)[-1].lower() for i in res)
out['resource_ext']=dict(ext)
if '--dump' in sys.argv: print(json.dumps(items[:3],ensure_ascii=False,indent=1)[:3000]); 
def nm(i):return (i.get('name') or i.get('title') or i.get('path') or '')
checks={}
for kind in ['mp4','jpeg','png','md','json','csv','html','zip']:
    c=[i for i in res if nm(i).lower().endswith('.'+kind)]
    if not c: checks[kind]='NO_ITEM';continue
    i=c[0];s,h,b=get('/api/media/'+i['id'])
    checks[kind]={'id':i['id'],'name':nm(i),'status':s,'ctype':h.get('Content-Type'),'len':len(b),'sha256':hashlib.sha256(b).hexdigest(),'expected_sha':(i.get('meta') or {}).get('sha256'),'match':hashlib.sha256(b).hexdigest()==(i.get('meta') or {}).get('sha256')}
out['media_full']=checks
v=[i for i in res if nm(i).endswith('IMG_7835.mp4')] or [i for i in res if nm(i).lower().endswith('.mp4')]
vid=v[0]['id']
for rng in ['bytes=0-1023','bytes=20000000-20001023','bytes=-1024','bytes=999999999-']:
    s,h,b=get('/api/media/'+vid,{'Range':rng});out.setdefault('range',[]).append([rng,s,h.get('Content-Range'),len(b)])
s,h,b=get('/api/health',{'Host':'evil.example:8765'});out['bad_host']=s
out['post_no_csrf']=post('/api/review',{'item_id':vid,'decision':'PASS'},'wrong')[0]
out['post_bad_origin']=post('/api/review',{'item_id':vid,'decision':'PASS'},csrf,{'Origin':'http://evil.example'})[0]
shots=[i for i in items if i.get('group')=='shot'];mgr=[i for i in items if i.get('group') in('manager','managers')]
targets=[(shots[0]['id'] if shots else None,'PASS'),(mgr[0]['id'] if mgr else None,'FAIL'),(vid,'DEFER')]
out['writes']=[]
if '--write' in sys.argv:
    for iid,dec in targets:
        if iid: out['writes'].append([iid,dec,post('/api/review',{'item_id':iid,'decision':dec,'note':'grok-bot audit probe 2026-11-22','reviewer':'grok-bot-audit','evidence':'docs/audits'},csrf)])
s,h,b=get('/api/reviews');out['reviews_now']=json.loads(b)
out['shots']=len(shots);out['managers']=len(mgr)
print(json.dumps(out,ensure_ascii=False,indent=1))
