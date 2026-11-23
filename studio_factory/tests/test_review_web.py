"""Offline tests for local review, source integrity, playback and anti-CSRF."""
import hashlib
import io
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from http.server import ThreadingHTTPServer
from studio_factory.review_web import Catalog, Handler, safe_extract


def mkzip(root, unsafe=False):
    z=root/'test.zip';raw=b'hello original\n'
    inv={'files_count':1,'files':[{'source_relative':'demo.txt','size_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'kind':'text_or_code'}]}
    with zipfile.ZipFile(z,'w') as f:
        f.writestr('files/demo.txt',raw)
        f.writestr('MANIFEST/inventory.json',json.dumps(inv))
        if unsafe:f.writestr('../escape.txt','x')
    return z

class LocalReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        safe_extract(mkzip(self.root),self.root/'assets')
        shots={'shots':[{'id':f'S{i:02}','start_ms':(i-1)*3600,'end_ms':i*3600,
                         'duration_ms':3600,'title_zh':f'Shot {i}','act':1} for i in range(1,26)]}
        repo=self.root/'repo'
        p=repo/'projects/j4-async-succession/archive/v2_6';p.mkdir(parents=True)
        (p/'j4_shots.json').write_text(json.dumps(shots))
        self.cat=Catalog(self.root/'assets',repo,self.root/'review.sqlite3')
        self.http=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        self.http.app=self.cat;self.http.csrf='test-token'
        self.worker=threading.Thread(target=self.http.serve_forever,daemon=True);self.worker.start()
        self.base=f'http://127.0.0.1:{self.http.server_port}'

    def tearDown(self):
        self.http.shutdown();self.http.server_close();self.worker.join(timeout=3)
        self.cat.store.connection.close();self.tmp.cleanup()

    def get(self,url,range_=None):
        req=urllib.request.Request(self.base+url,headers={'Range':range_} if range_ else {})
        with urllib.request.urlopen(req) as r:return r.status,dict(r.headers),r.read()

    def post(self,url,body,headers=None):
        head={'Content-Type':'application/json','X-Review-CSRF':'test-token'}
        if headers:head.update(headers)
        req=urllib.request.Request(self.base+url,data=json.dumps(body).encode(),headers=head,method='POST')
        with urllib.request.urlopen(req) as r:return r.status,json.load(r)

    def test_catalog_contains_shots_managers_and_assets(self):
        _,_,data=self.get('/api/bootstrap');d=json.loads(data)
        self.assertEqual(d['shots'],25)
        self.assertEqual(d['counts']['manager'],17)
        self.assertEqual(d['available_files'],1)
        self.assertEqual(d['counts']['resource'],1)
        self.assertEqual(d['counts']['test'],5)
        self.assertEqual(d['generation_state'],'BLOCKED')

    def test_range_playback_and_text(self):
        eid=next(x['id'] for x in self.cat.entries.values() if x['group']=='resource')
        code,headers,data=self.get('/api/media/'+eid,'bytes=2-6')
        self.assertEqual(code,206)
        self.assertEqual(headers['Content-Range'],'bytes 2-6/15')
        self.assertEqual(data,b'llo o')
        code,_,text=self.get('/api/media/'+eid)
        self.assertEqual(code,200)
        self.assertEqual(text,b'hello original\n')

    def test_review_persists_and_origin_protection(self):
        eid=next(x['id'] for x in self.cat.entries.values() if x['group']=='resource')
        status,value=self.post('/api/review',{'item_id':eid,'decision':'FAIL','note':'frame 3 lacks evidence','reviewer':'director','evidence':'local://x'})
        self.assertEqual(status,200)
        self.assertEqual(value['decision'],'FAIL')
        _,_,data=self.get('/api/reviews')
        self.assertEqual(json.loads(data)[eid]['note'],'frame 3 lacks evidence')
        with self.assertRaises(urllib.error.HTTPError) as e:
            self.post('/api/review',{'item_id':eid,'decision':'PASS'}, {'Origin':'https://attacker.example'})
        self.assertEqual(e.exception.code,403)
        with self.assertRaises(urllib.error.HTTPError) as e:
            self.post('/api/review',{'item_id':eid,'decision':'INVALID'})
        self.assertEqual(e.exception.code,400)

    def test_tests_are_whitelisted_and_no_real_generation(self):
        for name in ('inventory','shot_timeline'):
            code,d=self.post('/api/tests/run',{'test_id':name})
            self.assertEqual(code,200)
            self.assertEqual(d['state'],'PASS')
        with self.assertRaises(urllib.error.HTTPError):
            self.post('/api/tests/run',{'test_id':'rm -rf /'})

    def test_safe_extract_rejects_traversal(self):
        z=mkzip(self.root,unsafe=True)
        with self.assertRaises(ValueError):safe_extract(z,self.root/'unsafe')
        self.assertFalse((self.root/'escape.txt').exists())

if __name__=='__main__':unittest.main()
