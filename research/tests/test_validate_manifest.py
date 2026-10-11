"""Minimal no-network tests of the Garden Path source manifest integrity gate."""
import unittest
from pathlib import Path
import importlib.util

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "validate_manifest.py"
spec = importlib.util.spec_from_file_location("validate_manifest", SCRIPT)
validator = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(validator)

BASE = {
    "family_id": "illustrative_f01",
    "construction": "NPZ",
    "sentence": "While Anna dressed the baby played in the crib.",
    "disambiguator": "played",
    "source_url": "https://example.org/illustrative-only",
    "source_item_id": "example-one",
    "review_status": "PASSED",
    "gold_claims": [
        {"relation_id": "old", "predicate": "dress", "arguments": {"agent": "Anna", "patient": "baby"},
         "truth_status": "NOT_ENTAILED", "probe_type": "OBSOLETE"},
        {"relation_id": "new", "predicate": "play", "arguments": {"agent": "baby"},
         "truth_status": "ENTAILED", "probe_type": "FINAL"},
    ],
}

def row(cond, **kwargs):
    d = dict(BASE)
    d.update({"item_id": "id_" + cond, "condition": cond})
    if cond == "CUE":
        d["sentence"] = "While Anna dressed, the baby played in the crib."
    if cond.startswith("NONAMB"):
        d["sentence"] = ("While Anna slept the baby played in the crib." if cond == "NONAMB_BARE"
                         else "While Anna slept, the baby played in the crib.")
    d.update(kwargs)
    return d

class ManifestTests(unittest.TestCase):
    def test_valid_a_pair(self):
        self.assertEqual([], validator.check_rows([row("GP"), row("CUE")], "A"))
    def test_missing_control_rejected(self):
        self.assertTrue(any("missing" in e for e in validator.check_rows([row("GP")], "A")))
    def test_nonentailment_kept_distinct(self):
        good = [row("GP"), row("CUE")]
        good[1]["gold_claims"] = [dict(x) for x in good[1]["gold_claims"]]
        good[1]["gold_claims"][0]["truth_status"] = "CONTRADICTED"
        self.assertTrue(any("truth mismatch" in e for e in validator.check_rows(good, "A")))
    def test_duplicate_item_rejected(self):
        x, y = row("GP"), row("CUE")
        y["item_id"] = x["item_id"]
        self.assertTrue(any("duplicate item_id" in e for e in validator.check_rows([x, y], "A")))
    def test_pending_flag(self):
        x, y = row("GP", review_status="PENDING"), row("CUE", review_status="PENDING")
        self.assertTrue(validator.check_rows([x,y], "A", require_review=True))
        self.assertEqual([], validator.check_rows([x,y], "A", require_review=False))
    def test_b_target_consistency(self):
        extras = dict(target_id="t01", target_prefix="The chef", transitive_candidate="The chef cleaned the stove.",
                      intransitive_candidate="The chef rested near the stove.", lexical_disjoint_review="PASSED")
        rows = [row(c, **extras) for c in sorted(validator.B_CONDITIONS)]
        self.assertEqual([], validator.check_rows(rows, "B"))
        rows[-1]["transitive_candidate"] = "Something else"
        self.assertTrue(any("target not identical" in e for e in validator.check_rows(rows, "B")))

if __name__ == "__main__":
    unittest.main()
