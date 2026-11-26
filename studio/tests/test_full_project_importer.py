import json
import tempfile
import unittest
from pathlib import Path

from studio.importer.full_project_importer import (
    FullProjectImporter, SourceInput, ITEM_TYPES, THIRD_PARTY_SUPPLEMENTAL,
)
from studio.importer.seroval_lite import parse_assignment_after, SerovalParseError

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "studio/tests/fixtures/higgsfield_publication_passport_rush_2026-11-26.ssr.txt"
SCHEMA = json.loads((ROOT / "schemas/full-project-inventory.v1.schema.json").read_text())


def validate(inst, schema):
    """Minimal draft-2020-12 subset validator (type/required/enum/const/properties/items/additionalProperties)."""
    t = schema.get("type")
    types = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}
    if t:
        ts = t if isinstance(t, list) else [t]
        assert any(isinstance(inst, types[x]) for x in ts), (inst, t)
    if "const" in schema:
        assert inst == schema["const"], (inst, schema["const"])
    if "enum" in schema:
        assert inst in schema["enum"], (inst, schema["enum"])
    if isinstance(inst, dict):
        for r in schema.get("required", []):
            assert r in inst, f"missing {r}"
        props = schema.get("properties", {})
        for k, v in inst.items():
            if k in props:
                validate(v, props[k])
            elif isinstance(schema.get("additionalProperties"), dict):
                validate(v, schema["additionalProperties"])
    if isinstance(inst, list) and "items" in schema:
        for x in inst:
            validate(x, schema["items"])


def synthetic_page(slug, show_prompts="!1", license_='null'):
    return ('x={a:1};$R[9]={l:$R[10]={project:$R[11]={id:"00000000-0000-4000-8000-000000000001",'
            f'slug:"{slug}",title:"Other",type:"film",showPrompts:{show_prompts},showCanvas:!1,'
            'media:$R[12]=[$R[13]={id:"m1",name:"Cut",kind:"video",durationSeconds:12.5,width:1280,height:720}],'
            f'info:$R[14]={{license:{license_},information:$R[15]=[]}},assets:$R[16]=[]}}}}}}')


class ImporterTests(unittest.TestCase):
    def run_html(self, path):
        return FullProjectImporter().run([SourceInput("html_publication", path, "u")], source_url="u")

    def test_real_publication_fixture(self):
        inv = self.run_html(FIX)
        validate(inv, SCHEMA)
        p = inv["project"]
        self.assertEqual(p["publication_id"], "5faf8c98-ab7b-4195-bfb6-073a6e985785")
        self.assertTrue(p["show_prompts"]) and self.assertTrue(p["show_canvas"])
        self.assertIsNone(p["license"])
        self.assertEqual(inv["coverage"]["project"]["state"], "OBTAINED")
        self.assertEqual(inv["coverage"]["prompts"]["state"], "BROWSER_REQUIRED")
        self.assertEqual(inv["coverage"]["rights"]["state"], "UNKNOWN")
        vids = [i for i in inv["items"] if i["type"] == "video"]
        self.assertEqual(len(vids), 1)
        self.assertAlmostEqual(vids[0]["duration_seconds"], 287.541667)
        self.assertFalse(vids[0]["bytes_obtained"])
        self.assertEqual(inv["import_status"], "PARTIAL")
        self.assertEqual(inv["acceptance"]["status"], "NOT_RUN")

    def test_not_hardcoded_to_one_project(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "p.html"
            f.write_text(synthetic_page("some-other-film"))
            inv = self.run_html(f)
            validate(inv, SCHEMA)
            self.assertEqual(inv["project"]["slug"], "some-other-film")
            self.assertEqual(inv["coverage"]["prompts"]["state"], "NOT_EXPOSED")
            self.assertEqual(inv["coverage"]["canvas"]["state"], "NOT_EXPOSED")

    def test_unparseable_page_records_gap(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "p.html"
            f.write_text("project:$R[1]=(e=>e)")
            inv = self.run_html(f)
            self.assertTrue(any("not parseable" in e for e in inv["errors"]))
            self.assertEqual(inv["coverage"]["project"]["state"], "UNKNOWN")

    def test_third_party_archive_never_counts(self):
        with tempfile.TemporaryDirectory() as d:
            arch = Path(d) / "archive"; arch.mkdir()
            (arch / "p1.txt").write_text("a prompt")
            inv = FullProjectImporter().run([SourceInput("third_party_archive", arch)])
            validate(inv, SCHEMA)
            self.assertEqual(inv["items"], [])
            self.assertEqual(len(inv["supplemental_items"]), 1)
            self.assertEqual(inv["supplemental_items"][0]["evidence_class"], THIRD_PARTY_SUPPLEMENTAL)
            self.assertEqual(inv["coverage"]["prompts"]["state"], "NOT_RUN")

    def test_owner_export_counts_and_gaps(self):
        with tempfile.TemporaryDirectory() as d:
            ex = Path(d)
            (ex / "shot1.mp4").write_bytes(b"\x00" * 10)
            (ex / "prompts.json").write_text("[]")
            (ex / "stray.bin").write_bytes(b"1")
            (ex / "export_manifest.json").write_text(json.dumps({
                "evidence_class": "OFFICIAL",  # claimed without evidence -> downgraded
                "provided_by": "owner",
                "expected_counts": {"video": 2, "prompts": 1},
                "files": [{"path": "shot1.mp4", "type": "video"}, {"path": "prompts.json", "type": "prompts"},
                          {"path": "gone.wav", "type": "audio"}]}))
            inv = FullProjectImporter().run([SourceInput("export_dir", ex)])
            validate(inv, SCHEMA)
            self.assertEqual(inv["coverage"]["video"]["state"], "PARTIAL")
            self.assertEqual(inv["coverage"]["prompts"]["state"], "OBTAINED")
            errs = " ".join(inv["errors"])
            self.assertIn("downgraded", errs); self.assertIn("gone.wav", errs); self.assertIn("unlisted", errs)
            self.assertTrue(all(i["evidence_class"] == "OWNER_EXPORT" for i in inv["items"]))
            self.assertEqual(inv["import_status"], "PARTIAL")

    def test_coverage_has_every_type(self):
        inv = FullProjectImporter().run([])
        self.assertEqual(set(inv["coverage"]), set(ITEM_TYPES))
        self.assertTrue(all(c["state"] == "NOT_RUN" for c in inv["coverage"].values()))


class ElementsCsvTests(unittest.TestCase):
    CSV = "ID,Name,Display name,Version,Category,Description,Review status,Author,Performer,Created at\n"

    def _write(self, d, name, rows):
        p = Path(d) / name
        p.write_text(self.CSV + "".join(rows), encoding="utf-8")
        return p

    def test_rows_dedup_partial_and_redaction(self):
        from studio.importer.full_project_importer import redacted_summary
        with tempfile.TemporaryDirectory() as d:
            a = self._write(d, "all.csv", ["i1,n1,n1,,prop,secret desc,,au,,2026-01-01T00:00:00Z\n",
                                           "i2,n2,n2,,character,other,,au,,2026-01-02T00:00:00Z\n"])
            b = self._write(d, "props.csv", ["i1,n1,n1,,prop,secret desc,,au,,2026-01-01T00:00:00Z\n"])
            inv = FullProjectImporter().run([SourceInput("elements_csv", a), SourceInput("elements_csv", b)])
            self.assertEqual(inv["coverage"]["elements"]["state"], "PARTIAL")
            self.assertEqual(inv["coverage"]["elements"]["obtained"], 2)
            self.assertTrue(all(i["bytes_obtained"] is False for i in inv["items"]))
            self.assertEqual(inv["import_status"], "PARTIAL")
            validate(inv, SCHEMA)
            red = json.dumps(redacted_summary(inv))
            for leak in ("secret desc", "n1", "i1", "other"):
                self.assertNotIn(leak, red)
            self.assertEqual(json.loads(red)["elements_unique"], 2)

    def test_missing_columns_is_error(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.csv"
            p.write_text("A,B\n1,2\n")
            inv = FullProjectImporter().run([SourceInput("elements_csv", p)])
            self.assertTrue(any("missing required columns" in e for e in inv["errors"]))


class SerovalTests(unittest.TestCase):
    def test_literals(self):
        v = parse_assignment_after('z project:$R[1]={a:!0,b:!1,c:void 0,d:null,e:"x\\"y",f:[1,2.5,-3],g:$R[2]={h:"\\u00e9"},i:$R[2]}', "project:")
        self.assertEqual(v, {"a": True, "b": False, "c": None, "d": None, "e": 'x"y', "f": [1, 2.5, -3], "g": {"h": "é"}, "i": {"h": "é"}})

    def test_rejects_code(self):
        with self.assertRaises(SerovalParseError):
            parse_assignment_after("project:{a:new Map()}", "project:")


if __name__ == "__main__":
    unittest.main()
