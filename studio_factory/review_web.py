"""Local-first review and playback server for Higgsfield Studio.

Method contract: ed3c/medium-compiler/.agents/skills/build-review-interface/SKILL.md.
No network services, model generation, publishing or credit-consuming commands.
Python stdlib only; binds loopback, uses an explicit asset manifest, checks origins.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import mimetypes
import os
import secrets
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
import urllib.parse
import zipfile
from datetime import datetime, timezone
from functools import partial
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SITE = Path(__file__).with_name('review_site')
MAX_TEXT = 1_500_000
MAX_INPUT = 20_000
DECISIONS = {'PASS','FAIL','DEFER','NOT_RUN'}
ALIASES = {'j4-async-succession':'J4 · ASYNC: SUCCESSION'}
MANAGERS = (
    'portfolio','research','story','art_direction','character','asset','prompt','shot',
    'optical','sound','generation','budget','rights','qc','delivery','provenance','experiment')
VIDEO_EXT={'.mp4','.mov','.webm','.m4v','.mkv'}
AUDIO_EXT={'.wav','.mp3','.m4a','.aac','.flac','.ogg','.aif','.aiff'}
IMAGE_EXT={'.png','.jpeg','.jpg','.webp','.gif','.svg'}
TEXT_EXT={'.md','.csv','.tsv','.json','.html','.htm','.py','.js','.css','.txt','.yaml','.yml','.sh','.toml'}


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()


def safe_extract(zip_path: Path, destination: Path, verify: bool=True) -> dict:
    """Extract only known safe files; never overwrite bytes that disagree."""
    destination.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        members=[m for m in z.infolist() if not m.is_dir()]
        if len(members)>5000 or sum(m.file_size for m in members)>2_000_000_000:
            raise ValueError('refusing unexpectedly large archive')
        for m in members:
            name=Path(m.filename)
            if (name.is_absolute() or '..' in name.parts or not name.parts or
                '\\' in m.filename or m.file_size>350_000_000 or
                ((m.external_attr >> 16)&0o170000)==0o120000):
                raise ValueError('unsafe archive entry: '+m.filename)
        for m in members:
            output=(destination/m.filename).resolve()
            if not output.is_relative_to(destination.resolve()):
                raise ValueError('unsafe resolved archive entry')
            output.parent.mkdir(parents=True,exist_ok=True)
            if output.exists():
                if output.stat().st_size==m.file_size:
                    continue
                raise ValueError('existing file size differs; refusing overwrite: '+str(output))
            with z.open(m) as src,output.open('xb') as dst:
                shutil.copyfileobj(src,dst,length=1024*1024)
    inventory=destination/'MANIFEST'/'inventory.json'
    result={'members':len(members),'verified':0,'missing':[],'mismatch':[]}
    if inventory.exists() and verify:
        d=json.loads(inventory.read_text(encoding='utf-8'))
        for item in d['files']:
            p=destination/'files'/item['source_relative']
            if not p.is_file():result['missing'].append(item['source_relative']);continue
            if sha256_file(p)!=item['sha256']:
                result['mismatch'].append(item['source_relative'])
            else:result['verified']+=1
        if result['missing'] or result['mismatch']:
            raise ValueError('extracted archive failed SHA-256 verification: '+str(result))
    return result


class ReviewStore:
    def __init__(self, dbfile: Path):
        dbfile.parent.mkdir(parents=True,exist_ok=True)
        self.connection=sqlite3.connect(dbfile,check_same_thread=False,timeout=10)
        self.connection.execute('PRAGMA journal_mode=WAL')
        self.connection.execute('''CREATE TABLE IF NOT EXISTS reviews (
          item_id TEXT PRIMARY KEY, decision TEXT NOT NULL, note TEXT NOT NULL,
          reviewer TEXT NOT NULL, timestamp TEXT NOT NULL, evidence TEXT NOT NULL DEFAULT '')''')
        self.connection.commit()
        self.lock=threading.Lock()
    def get_all(self):
        with self.lock:
            rows=self.connection.execute('SELECT * FROM reviews ORDER BY item_id').fetchall()
        return {r[0]:dict(zip(('item_id','decision','note','reviewer','timestamp','evidence'),r)) for r in rows}
    def put(self,item_id,decision,note,reviewer,evidence):
        if decision not in DECISIONS or len(note)>5000 or len(reviewer)>120 or len(evidence)>500:
            raise ValueError('invalid review input')
        stamp=datetime.now(timezone.utc).isoformat()
        with self.lock:
            self.connection.execute('''INSERT INTO reviews VALUES(?,?,?,?,?,?) ON CONFLICT(item_id) DO UPDATE SET
              decision=excluded.decision,note=excluded.note,reviewer=excluded.reviewer,
              timestamp=excluded.timestamp,evidence=excluded.evidence''',(item_id,decision,note,reviewer,stamp,evidence))
            self.connection.commit()
        return {'item_id':item_id,'decision':decision,'note':note,'reviewer':reviewer,'timestamp':stamp,'evidence':evidence}


class Catalog:
    def __init__(self, assets:Path, repo:Path, database:Path, drive_manifest:Path|None=None, project:str='j4-async-succession'):
        self.assets=assets.resolve();self.repo=repo.resolve();self.project=project
        self.config=self._project_config()
        self.store=ReviewStore(database)
        self.entries={}
        self.sha_map={}
        self.drive={}
        if drive_manifest and drive_manifest.exists():
            data=json.loads(drive_manifest.read_text(encoding='utf-8'))
            self.drive={a['name']:a for a in data.get('objects',[])}
            self.drive_folder=data.get('folder_url')
        else:self.drive_folder=None
        self._build()

    def _project_config(self):
        path=self.repo/'projects'/self.project/'PROJECT.json'
        if path.is_file():
            return json.loads(path.read_text(encoding='utf-8'))
        return {'project_id':self.project,'title':self.project,'duration_ms':90000 if self.project=='j4-async-succession' else 0,
                'frame_rate':30,'shot_count':25 if self.project=='j4-async-succession' else 0}

    def _add(self,group,key,name,subtitle,kind,path=None,meta=None):
        eid=hashlib.sha256((self.project+'|'+group+'|'+key).encode()).hexdigest()[:18]
        rec={'id':eid,'group':group,'key':key,'name':name,'subtitle':subtitle,'kind':kind,
             'available':bool(path and path.is_file()),'meta':meta or {},'review_state':'NOT_RUN'}
        if path:
            rec['relative_path']=str(path.relative_to(self.assets)) if path.is_relative_to(self.assets) else str(path)
            rec['path']=path
            rec['bytes']=path.stat().st_size if path.is_file() else None
        else:rec['bytes']=None
        self.entries[eid]=rec
        return rec

    def _build(self):
        inventory=self.assets/'MANIFEST'/'inventory.json'
        if inventory.exists():
            inv=json.loads(inventory.read_text(encoding='utf-8'))
            self.expected=inv.get('files_count',len(inv.get('files',[])))
            for row in inv.get('files',[]):
                rel=row['source_relative'];path=self.assets/'files'/rel
                kind=self._type(path)
                d=self.drive.get(Path(rel).name,{}) if '/' not in rel else {}
                self._add('resource',rel,Path(rel).name,str(Path(rel).parent),kind,path,
                          {'sha256':row['sha256'],'expected_bytes':row['size_bytes'],
                           'source_kind':row.get('kind'), 'drive':d, 'source_path':rel})
        else:
            self.expected=0
            if self.assets.exists():
                for p in sorted(self.assets.rglob('*')):
                    if p.is_file() and not p.name.startswith('.') and 'MANIFEST' not in p.parts:
                        rel=str(p.relative_to(self.assets))
                        self._add('resource',rel,p.name,str(p.parent.relative_to(self.assets)),self._type(p),p,
                                  {'source_path':rel})
                        self.expected+=1
        shotsfile=self._find_shots()
        self.shots=[]
        if shotsfile:
            data=json.loads(shotsfile.read_text(encoding='utf-8'))
            self.shots=data.get('shots',[])
        for s in self.shots:
            sid=s['id'];title=s.get('title_zh',sid)
            self._add('shot',sid,f'{sid} · {title}',f"{s['start_ms']/1000:.1f}–{s['end_ms']/1000:.1f}s · {s.get('title_en','')}",'shot',None,
                      {'shot':s,'time':s['start_ms'],'art':s.get('art_reference',{}),'status':s.get('review_state','NOT_RUN')})
        # Art contract review is a distinct evidence layer, never a source of
        # generation authority or pixel-recognition PASS.
        self.art_contract_error = None
        art_contract = (self.repo/'projects'/self.project/'contracts'/'art_mechanism_v4_1.json')
        if art_contract.is_file():
            try:
                from .art_contracts import load_contract, compile_shot, judge_observations
                r = load_contract(self.repo)
                report_path=(self.repo/'projects'/self.project/'qc'/'six_panel_observations_v4_1.json')
                cases=json.loads(report_path.read_text(encoding='utf-8'))['cases']
                observed={c['shot_id']:c for c in cases}
                for p in r['contract']['shots']:
                    sid=p['shot_id']
                    report=judge_observations(r,observed[sid])
                    compiled=compile_shot(r,sid)
                    self._add('art',sid,'G2 Optical · '+sid+' · '+p['optical_method'],
                        'Source-locked art mechanism; human observation, no media proof',
                        'art_contract',None,{
                          'shot_id':sid,'profile':p,'compiled':compiled,
                          'report':report,'art_url':r['optical'][sid]['source_url'],
                          'source_contract_sha256':r['contract_sha256']})
            except (ValueError,KeyError,FileNotFoundError) as exc:
                self.art_contract_error=str(exc)
        for m in MANAGERS:
            self._add('manager',m,m.replace('_',' ').title()+' Manager','Independent domain authority and handoff','manager',None,{'domain':m})
        for tid,label in [('core_contract','Manager contract tests'),('budget','Existing budget regression'),('inventory','Local media inventory SHA-256'),('shot_timeline','Shot timecode and continuity'),('art_contract','Six-shot G2 art mechanism and expected-rejection contract')]:
            self._add('test',tid,label,'Read-only test, no media generation','test',None,{'test_id':tid})
        extra_dir=self.assets/'extra'
        if extra_dir.is_dir():
            for extra in sorted(extra_dir.rglob('*')):
                if extra.is_file():
                    rel=str(extra.relative_to(extra_dir))
                    self._add('resource','extra/'+rel,extra.name,'Additional local candidate',self._type(extra),extra,
                              {'source_kind':'supplemental_candidate','source_path':'extra/'+rel,
                               'evidence_status':'NOT_RUN'})
        self.reviews=self.store.get_all()

    def _find_shots(self):
        for p in [self.repo/'projects'/self.project/'shots.json',
                  self.repo/'projects'/self.project/'archive'/'v2_6'/'j4_shots.json',
                  self.assets/'files'/'j4_museum_v2_6'/'j4_shots.json']:
            if p.is_file():return p
        return None

    def _type(self,p):
        ext=p.suffix.lower()
        if ext in VIDEO_EXT:return 'video'
        if ext in AUDIO_EXT:return 'audio'
        if ext in IMAGE_EXT:return 'image'
        if ext in {'.md','.txt'}:return 'markdown'
        if ext in {'.csv','.tsv'}:return 'table'
        if ext=='.json':return 'json'
        if ext in {'.htm','.html'}:return 'html'
        if ext in {'.py','.js','.css','.sh','.yaml','.yml','.toml'}:return 'code'
        if ext=='.zip':return 'archive'
        return 'binary'

    def public(self):
        reviews={k:v for k,v in self.store.get_all().items() if k in self.entries}
        items=[]
        for rec in self.entries.values():
            clean={k:v for k,v in rec.items() if k!='path'}
            clean['review_state']=reviews.get(rec['id'],{}).get('decision','NOT_RUN')
            clean['note']=reviews.get(rec['id'],{}).get('note','')
            clean['reviewer']=reviews.get(rec['id'],{}).get('reviewer','local-reviewer')
            clean['evidence']=reviews.get(rec['id'],{}).get('evidence','')
            clean['timestamp']=reviews.get(rec['id'],{}).get('timestamp','')
            items.append(clean)
        groups={}
        for i in items:groups[i['group']]=groups.get(i['group'],0)+1
        return {'project':self.project,'title':self.config.get('title',self.project),
                'duration_ms':self.config.get('duration_ms',0),'frame_rate':self.config.get('frame_rate',30),
                'items':items,'shots':len(self.shots),
                'counts':groups,'expected_files':self.expected,'available_files':sum(x['available'] for x in items if x['group']=='resource'),
                'drive_folder':self.drive_folder,'server_time':datetime.now(timezone.utc).isoformat(),
                'media_policy':'private; never publish unreviewed footage to public Git',
                'provenance':'medium-compiler build-review-interface skill',
                'generation_state':'BLOCKED'}

    def run_test(self,test_id):
        if test_id=='art_contract':
            if self.art_contract_error:
                return {'test':test_id,'state':'BLOCKED','reason':self.art_contract_error}
            entries=[e for e in self.entries.values() if e['group']=='art']
            if not entries:
                return {'test':test_id,'state':'BLOCKED','reason':'no art mechanism contract'}
            rejected=[e for e in entries if e['meta']['report']['state']=='REJECTED_BY_OBSERVATION']
            ok=len(entries)==6 and len(rejected)==6
            return {'test':test_id,'state':'PASS_STATIC' if ok else 'FAIL',
                    'profiles':len(entries),'expected_rejected_reports':len(rejected),
                    'visual_media_verified':0,
                    'note':'PASS_STATIC means six supplied negative observations were rejected; it is NOT image or artwork approval.',
                    'creative_qc':'NOT_RUN','generation':'BLOCKED'}
        if test_id=='inventory':
            errors=[];count=0
            for item in self.entries.values():
                if item['group']!='resource':continue
                p=item.get('path'); expected=item['meta'].get('sha256')
                if not p or not p.is_file():errors.append(item['key']+' MISSING');continue
                if expected and sha256_file(p)!=expected:errors.append(item['key']+' CORRUPT')
                else:count+=1
            return {'test':'inventory','state':'PASS' if not errors else 'FAIL',
                    'checked':count,'expected':self.expected,'failures':errors[:50]}
        if test_id=='shot_timeline':
            e=[];clock=0
            for s in self.shots:
                if s['start_ms']!=clock:e.append(s['id']+':gap/overlap')
                if s['duration_ms']!=s['end_ms']-s['start_ms']:e.append(s['id']+':duration')
                clock=s['end_ms']
            if not self.shots or len(self.shots)!=self.config.get('shot_count',0) or clock!=self.config.get('duration_ms',0):
                e.append('wrong count or total duration')
            return {'test':'shot_timeline','state':'PASS' if not e else 'FAIL','failures':e,
                    'duration_ms':clock,'shot_count':len(self.shots)}
        if test_id not in {'core_contract','budget'}:raise ValueError('unknown whitelisted test')
        if test_id=='core_contract':
            argv=[sys.executable,'-m','unittest','discover','-s','studio_factory/tests','-v']
        else:argv=[sys.executable,'budget/test_track.py']
        if not (self.repo/'studio_factory'/'tests').exists() and test_id=='core_contract':
            return {'test':test_id,'state':'BLOCKED','reason':'repo checkout missing tests'}
        if not (self.repo/'budget'/'test_track.py').exists() and test_id=='budget':
            return {'test':test_id,'state':'BLOCKED','reason':'repo checkout missing budget tests'}
        try:
            p=subprocess.run(argv,cwd=self.repo,capture_output=True,text=True,timeout=40,
                env={**os.environ,'PYTHONPATH':str(self.repo)})
            return {'test':test_id,'state':'PASS' if p.returncode==0 else 'FAIL',
                    'exit_code':p.returncode,'stdout':p.stdout[-10000:],'stderr':p.stderr[-10000:]}
        except subprocess.TimeoutExpired:
            return {'test':test_id,'state':'BLOCKED','reason':'test timeout'}


def _json(data):return json.dumps(data,ensure_ascii=False).encode('utf-8')

class Handler(BaseHTTPRequestHandler):
    server_version='J4Review/1.0'
    def log_message(self,*args):pass
    @property
    def app(self):return self.server.app

    def _headers(self, status, ctype, length, extra=None):
        self.send_response(status)
        self.send_header('Content-Type',ctype)
        self.send_header('Content-Length',str(length))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('X-Frame-Options','SAMEORIGIN')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Cross-Origin-Resource-Policy','same-origin')
        if extra:
            for k,v in extra.items():self.send_header(k,str(v))
        self.end_headers()

    def _reply(self, data, status=200, content_type='application/json; charset=utf-8'):
        out=_json(data) if not isinstance(data,(bytes,bytearray)) else data
        self._headers(status,content_type,len(out))
        self.wfile.write(out)

    def _deny(self,status=403, reason='Forbidden'):
        self._reply({'error':reason},status)

    def _validate_origin(self):
        host=self.headers.get('Host','').lower()
        allowed={'127.0.0.1:'+str(self.server.server_port),'localhost:'+str(self.server.server_port)}
        if host not in allowed:return False
        origin=self.headers.get('Origin','')
        return (not origin) or origin in {'http://'+h for h in allowed}

    def do_GET(self):
        if not self._validate_origin():return self._deny()
        u=urllib.parse.urlsplit(self.path);route=u.path
        if route=='/api/bootstrap':
            payload=self.app.public();payload['csrf']=self.server.csrf
            return self._reply(payload)
        if route=='/api/reviews':
            return self._reply({k:v for k,v in self.app.store.get_all().items() if k in self.app.entries})
        if route=='/api/health':
            return self._reply({'state':'READY','backend':'stdlib','bind':'loopback','generation':'DISABLED'})
        if route.startswith('/api/media/'):
            eid=route.rsplit('/',1)[-1]
            item=self.app.entries.get(eid)
            if not item or not item.get('available') or item['group']!='resource':return self._deny(404,'Missing local asset')
            return self._stream(item)
        if route=='/':route='/index.html'
        full=(SITE/route.lstrip('/')).resolve()
        if not full.is_relative_to(SITE.resolve()) or not full.is_file():return self._deny(404,'Unknown route')
        mime,_=mimetypes.guess_type(full)
        if full.suffix=='.js':mime='text/javascript'
        if full.suffix=='.css':mime='text/css'
        out=full.read_bytes()
        self._headers(200,(mime or 'text/plain')+'; charset=utf-8',len(out),
            {'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; media-src 'self'; connect-src 'self'; frame-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'"})
        self.wfile.write(out)

    def _stream(self,item):
        path=item['path'];size=path.stat().st_size
        mime,_=mimetypes.guess_type(path)
        if path.suffix.lower() in {'.mp4','.m4v','.mov'}:mime='video/mp4'
        if path.suffix.lower()=='.md':mime='text/plain'
        if path.suffix.lower()=='.html':mime='text/html'
        mime=mime or 'application/octet-stream'
        start=0;end=size-1;status=200
        rng=self.headers.get('Range','')
        if rng:
            try:
                if not rng.startswith('bytes=') or ',' in rng:raise ValueError()
                a,b=rng[6:].split('-',1)
                if a:
                    start=int(a);end=int(b) if b else size-1
                else:
                    suffix=int(b);start=max(0,size-suffix);end=size-1
                if start<0 or start>=size or end<start:raise ValueError()
                end=min(end,size-1);status=206
            except (ValueError,TypeError):
                return self._headers(416,'text/plain',0,{'Content-Range':f'bytes */{size}'})
        extra={'Accept-Ranges':'bytes','Content-Disposition':'inline',
               'Content-Security-Policy':"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src 'self' data:; media-src 'self'; connect-src 'none'; frame-ancestors 'self'"}
        if status==206:extra['Content-Range']=f'bytes {start}-{end}/{size}'
        self._headers(status,mime,end-start+1,extra)
        try:
            with path.open('rb') as f:
                f.seek(start);remaining=end-start+1
                while remaining:
                    buf=f.read(min(1024*256,remaining))
                    if not buf:break
                    self.wfile.write(buf);remaining-=len(buf)
        except (BrokenPipeError,ConnectionResetError):pass

    def do_POST(self):
        if not self._validate_origin():return self._deny()
        if self.headers.get('X-Review-CSRF')!=self.server.csrf:
            return self._deny(403,'CSRF mismatch')
        if self.headers.get('Content-Type','').split(';',1)[0]!='application/json':
            return self._deny(415,'Expected application/json')
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length<1 or length>MAX_INPUT:raise ValueError('invalid request size')
            body=json.loads(self.rfile.read(length))
            if not isinstance(body,dict):raise ValueError('request must be JSON object')
            if self.path=='/api/review':
                item_id=body.get('item_id','')
                if item_id not in self.app.entries:raise ValueError('unknown item')
                if self.app.entries[item_id]['group']=='art' and body.get('decision')=='PASS':
                    raise ValueError('G2 art contract cannot be marked PASS without independent image and director evidence')
                result=self.app.store.put(item_id,body.get('decision','NOT_RUN'),
                    body.get('note',''),body.get('reviewer','local-reviewer'),body.get('evidence',''))
            elif self.path=='/api/tests/run':
                result=self.app.run_test(body.get('test_id',''))
            else:return self._deny(404,'Unknown API')
            return self._reply(result)
        except (ValueError,TypeError,sqlite3.Error) as e:
            return self._deny(400,str(e))


def run_server(assets:Path,repo:Path,db:Path,drive_manifest:Path|None,port:int,project:str='j4-async-succession'):
    catalog=Catalog(assets,repo,db,drive_manifest,project)
    server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    server.app=catalog
    server.csrf=secrets.token_urlsafe(24)
    print(f'J4 local review: http://127.0.0.1:{server.server_port}',flush=True)
    print(f'assets available {sum(x.get("available",False) for x in catalog.entries.values() if x["group"]=="resource")}/{catalog.expected}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


def main(argv=None):
    p=argparse.ArgumentParser(prog='python -m studio_factory.review_web')
    cmds=p.add_subparsers(dest='command',required=True)
    imp=cmds.add_parser('import-archive',help='Extract and SHA-verify private Google Drive ZIP')
    imp.add_argument('--archive',type=Path,required=True)
    imp.add_argument('--destination',type=Path,required=True)
    s=cmds.add_parser('serve',help='Serve project/asset reviews from loopback only')
    s.add_argument('--assets',type=Path,required=True,help='Directory containing files/ and MANIFEST/')
    s.add_argument('--repo',type=Path,default=Path.cwd())
    s.add_argument('--db',type=Path,default=Path.home()/'.local/share/higgsfield-studio/review.sqlite3')
    s.add_argument('--drive-manifest',type=Path)
    s.add_argument('--port',type=int,default=8765)
    s.add_argument('--project',default='j4-async-succession')
    a=p.parse_args(argv)
    if a.command=='import-archive':
        print(json.dumps(safe_extract(a.archive,a.destination),indent=2))
    else:run_server(a.assets,a.repo,a.db,a.drive_manifest,a.port,a.project)

if __name__=='__main__':main()
