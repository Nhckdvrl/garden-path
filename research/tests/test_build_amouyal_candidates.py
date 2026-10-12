"""Tests for source CSV pairing and unreviewed-candidate provenance."""
from __future__ import annotations
import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

builder = load("build_amouyal_candidates", ROOT / "tools" / "build_amouyal_candidates.py")
validator = load("validate_manifest_again", ROOT / "tools" / "validate_manifest.py")

def source_rows(prefix: str, gp: str, control: str):
    """Two questions each for GP and cue; the original answer isn't semantic gold."""
    return [
        dict(set_id=f"{prefix}_1",sent_type="type_gp",quest_type="GP_question",
             sentence=gp,question="Was the old attachment stated?",
             correct_answer="No",incorrect_answer="Yes",reduced_verb="worked"),
        dict(set_id=f"{prefix}_2",sent_type="type_gp",quest_type="simple_question",
             sentence=gp,question="Was the final main event stated?",
             correct_answer="Yes",incorrect_answer="No",reduced_verb="worked"),
        dict(set_id=f"{prefix}_3",sent_type="type_nongp",quest_type="GP_question",
             sentence=control,question="Was the old attachment stated?",
             correct_answer="No",incorrect_answer="Yes",reduced_verb="worked"),
        dict(set_id=f"{prefix}_4",sent_type="type_nongp",quest_type="simple_question",
             sentence=control,question="Was the final main event stated?",
             correct_answer="Yes",incorrect_answer="No",reduced_verb="worked"),
    ]

def write_csv(path: Path, rows: list[dict]) -> None:
    fields = ("sentence","question","set_id","sent_type","quest_type",
              "correct_answer","incorrect_answer","reduced_verb")
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)

class SourceImportTests(unittest.TestCase):
    def make_source(self, root: Path) -> None:
        for fname, (construction, ctrl, nickname) in builder.SPECS.items():
            old = "A manager worked the book was important."
            new = "A manager worked, the book was important."
            rs = source_rows("s1", old, new)
            if nickname == "extended":
                for r in rs:
                    r["set_id"] = "set_1"
            write_csv(root/fname, rs)

    def test_expected_paired_source_dataset(self):
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td)
            self.make_source(folder)
            rows=builder.build_candidates(folder)
            self.assertEqual(8,len(rows))
            self.assertEqual(4,len(set(r["family_id"] for r in rows)))
            self.assertEqual({"GP","CUE"},set(r["condition"] for r in rows))
            self.assertTrue(all(r["review_status"]=="PENDING" for r in rows))
            self.assertTrue(all(c["truth_status"]=="UNRESOLVED"
                                for r in rows for c in r["gold_claims"]))
            self.assertEqual([],validator.check_rows(rows,"A",require_review=False))
            self.assertNotEqual([],validator.check_rows(rows,"A",require_review=True))
    def test_missing_pair_aborts(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            self.make_source(p)
            fname=next(iter(builder.SPECS))
            with (p/fname).open(encoding="utf-8",newline="") as f:
                original=list(csv.DictReader(f))
            write_csv(p/fname,[r for r in original if r["sent_type"]!="type_nongp"])
            with self.assertRaises(ValueError):
                builder.build_candidates(p)
    def test_no_auto_semantic_gold(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            self.make_source(p)
            r=builder.build_candidates(p)[0]
            self.assertTrue(all(x["predicate"]=="UNREVIEWED" for x in r["gold_claims"]))
            self.assertTrue(all("upstream_correct_answer" in x for x in r["gold_claims"]))

if __name__ == "__main__":
    unittest.main()
