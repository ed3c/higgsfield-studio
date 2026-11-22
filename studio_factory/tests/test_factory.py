import tempfile
import unittest
from pathlib import Path
from studio_factory.core import Factory, FactoryError, MANAGER_DOMAINS
from studio_factory.managers import manager

class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.store=Factory(Path(self.temp.name)/"factory.db")
        self.store.create_project("j4-async-succession")
        self.store.create_project("film-two")
    def tearDown(self):
        self.store.close();self.temp.cleanup()

    def test_all_managers_and_immutable_revisions(self):
        for d in MANAGER_DOMAINS:
            self.assertEqual(manager(d,self.store).domain,d)
        a=manager("research",self.store).publish(
            "shared","installation-method","refs/art.md",{"source":"museum-url","rights":"method-only"})
        self.assertEqual(self.store.get(a)["revision"],1)
        with self.assertRaises(FactoryError):
            manager("research",self.store).publish("shared","installation-method",
                "refs/new.md",{"source":"museum","rights":"method-only"})
        b=manager("research",self.store).publish("shared","installation-method",
            "refs/new.md",{"source":"museum","rights":"method-only"},expected_previous=a)
        self.assertEqual(self.store.get(b)["supersedes"],a)
        self.assertEqual(self.store.get(a)["revision"],1)

    def test_project_isolation_and_shared_references(self):
        one=manager("shot",self.store).publish("projects/j4-async-succession",
            "shot-01","j4_shots.json",{"start":0,"end":90})
        other=manager("shot",self.store).publish("projects/film-two",
            "shot-01","film_two.json",{"start":0,"end":25})
        with self.assertRaises(FactoryError):
            self.store.reference(other,one)
        shared=manager("research",self.store).publish("shared","rain-ref",
            "https://museum.example/rain",{"source":"museum","rights":"method-only"})
        self.store.reference(one,shared)
        self.store.reference(other,shared)

    def test_owner_only_handoff_idempotence_and_ack(self):
        a=manager("research",self.store).publish("projects/j4-async-succession",
            "article","source.md",{"date":"2026-11-22"})
        event=manager("research",self.store).send("j4-async-succession",
            "art_direction",a,"handoff-01",{"source_sha":"abc"})
        again=manager("research",self.store).send("j4-async-succession",
            "art_direction",a,"handoff-01",{"source_sha":"abc"})
        self.assertEqual(event,again)
        with self.assertRaises(FactoryError):
            manager("research",self.store).send("j4-async-succession",
                "budget",a,"bad-edge",{"test":True})
        with self.assertRaises(FactoryError):
            manager("qc",self.store).receive(event)
        manager("art_direction",self.store).receive(event)
        self.assertEqual(self.store.db.execute("SELECT state FROM handoffs WHERE event_id=?",
                         (event,)).fetchone()[0],"ACK")

    def test_paid_generation_denied_by_default(self):
        with self.assertRaisesRegex(FactoryError,"generation BLOCKED"):
            self.store.require_generation_gate("j4-async-succession",100,0,"director")
        for gate in ("owner_approval","director_estimate_posted",
                     "live_balance_checked","rights_review"):
            self.store.set_gate(project="j4-async-succession",gate=gate,
                state="APPROVED",approver="reviewer",evidence_uri="review://verified")
        self.assertEqual(self.store.require_generation_gate(
            "j4-async-succession",100,0,"director"),"ELIGIBLE_FOR_SEPARATE_HUMAN_EXECUTION")
        with self.assertRaisesRegex(FactoryError,"monthly budget"):
            self.store.require_generation_gate("j4-async-succession",9001,0,"director")

    def test_shared_requires_rights_source(self):
        with self.assertRaises(FactoryError):
            manager("research",self.store).publish("shared","bad","doc",{"note":"missing"})
        with self.assertRaises(FactoryError):
            manager("asset",self.store).publish("projects/missing","x","doc",{})

if __name__=="__main__":
    unittest.main()
