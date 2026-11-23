"""HOF-09: a second production reuses the shared review tool and shared research
without inheriting J4 story constants, review decisions or generation approval."""
import json
import tempfile
import unittest
from pathlib import Path
from studio_factory.core import Factory, FactoryError
from studio_factory.managers import manager
from studio_factory.review_web import Catalog, ReviewStore

SITE=Path(__file__).resolve().parents[1]/'review_site'


class SecondFilmNamespaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.repo=self.root/'repo'
        two=self.repo/'projects'/'film-two';two.mkdir(parents=True)
        (two/'PROJECT.json').write_text(json.dumps({'project_id':'film-two','title':'FILM TWO',
            'duration_ms':20000,'frame_rate':24,'shot_count':4}))
        (two/'shots.json').write_text(json.dumps({'shots':[{'id':f'T{i}','start_ms':(i-1)*5000,'end_ms':i*5000,
            'duration_ms':5000,'title_zh':f'鏡 {i}'} for i in range(1,5)]}))
        # A J4 asset root is present on disk but must not leak into film-two.
        j4=self.root/'assets'/'files'/'j4_museum_v2_6';j4.mkdir(parents=True)
        (j4/'j4_shots.json').write_text(json.dumps({'shots':[{'id':'S18','start_ms':0,'end_ms':1,'duration_ms':1}]}))

    def tearDown(self):self.tmp.cleanup()

    def test_review_tool_has_no_j4_constants(self):
        for name in ('index.html','app.js'):
            text=(SITE/name).read_text(encoding='utf-8')
            for token in ('J4','S18','63.700','其餘 24','90 秒','j4-review-selected'):
                self.assertNotIn(token,text,f'{token!r} hard-coded in shared {name}')

    def test_second_film_catalog_is_isolated(self):
        c=Catalog(self.root/'assets',self.repo,self.root/'film-two.sqlite3',project='film-two')
        self.addCleanup(c.store.connection.close)
        d=c.public()
        self.assertEqual((d['project'],d['title'],d['shots']),('film-two','FILM TWO',4))
        self.assertIsNone(d['global_interrupt'])
        self.assertEqual([s['id'] for s in c.shots],['T1','T2','T3','T4'])
        self.assertEqual(c.run_test('shot_timeline')['state'],'PASS')

    def test_review_db_is_bound_to_one_production(self):
        db=self.root/'shared.sqlite3'
        ReviewStore(db,'j4-async-succession').connection.close()
        with self.assertRaisesRegex(ValueError,'belongs to project'):
            ReviewStore(db,'film-two')

    def test_registry_isolation_shared_reuse_and_gates(self):
        f=Factory(self.root/'factory.db');self.addCleanup(f.close)
        f.create_project('j4-async-succession');f.create_project('film-two')
        shared=manager('research',f).publish('shared','sound-method','research/README.md',
            {'source':'repo:research/README.md','rights':'method-only'})
        j4=manager('story',f).publish('projects/j4-async-succession','logline','j4.md',{'t':'j4'})
        two=manager('story',f).publish('projects/film-two','logline','two.md',{'t':'two'})
        f.reference(two,shared)
        with self.assertRaises(FactoryError):f.reference(two,j4)
        for g in ('owner_approval','director_estimate_posted','live_balance_checked','rights_review'):
            f.set_gate(project='j4-async-succession',gate=g,state='APPROVED',approver='t',evidence_uri='test://')
        f.require_generation_gate('j4-async-succession',100,0,'director')
        with self.assertRaisesRegex(FactoryError,'generation BLOCKED'):
            f.require_generation_gate('film-two',100,0,'director')


if __name__=='__main__':unittest.main()
