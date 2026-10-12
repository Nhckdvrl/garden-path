"""Local deterministic safety checks. No HF, GPU, network, or inference."""
from __future__ import annotations
import unittest
from pathlib import Path
import importlib.util

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "validate_manifest.py"
spec = importlib.util.spec_from_file_location("validate_manifest", SCRIPT)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

BASE = {
    "family_id": "illustrative_f01", "construction": "NPZ",
    "sentence": "While Anna dressed the baby played in the crib.",
    "disambiguator": "played", "control_type": "COMMA",
    "source_url": "https://example.org/illustrative-only",
    "source_item_id": "example-one", "review_status": "PASSED",
    "gold_claims": [
        {"relation_id": "old", "predicate": "dress", "arguments": {"agent": "Anna", "patient": "baby"},
         "truth_status": "NOT_ENTAILED", "probe_type": "OBSOLETE"},
        {"relation_id": "new", "predicate": "play", "arguments": {"agent": "baby"},
         "truth_status": "ENTAILED", "probe_type": "FINAL"},
        {"relation_id": "other", "predicate": "dress", "arguments": {"agent": "Anna"},
         "truth_status": "ENTAILED", "probe_type": "INDEPENDENT"},
        {"relation_id": "bridge", "predicate": "cooccur", "arguments": {"actions": ["dress", "play"]},
         "truth_status": "ENTAILED", "probe_type": "BRIDGE"},
    ],
}

def row(cond, **kwargs):
    d = dict(BASE)
    d.update({"item_id": "id_" + cond, "condition": cond})
    if cond == "CUE":
        d["sentence"] = "While Anna dressed, the baby played in the crib."
    if cond.startswith("NONAMB"):
        d["sentence"] = ("While Anna slept the baby played in the crib."
                         if cond == "NONAMB_BARE" else
                         "While Anna slept, the baby played in the crib.")
    d.update(kwargs)
    return d

class ManifestTests(unittest.TestCase):
    def test_valid_a_pair(self):
        self.assertEqual([], validator.check_rows([row("GP"), row("CUE")], "A"))
    def test_missing_control_rejected(self):
        self.assertTrue(any("missing" in x for x in validator.check_rows([row("GP")], "A")))
    def test_not_entailed_is_not_contradicted(self):
        good = [row("GP"), row("CUE")]
        good[1]["gold_claims"] = [dict(x) for x in good[1]["gold_claims"]]
        good[1]["gold_claims"][0]["truth_status"] = "CONTRADICTED"
        self.assertTrue(any("truth mismatch" in x for x in validator.check_rows(good, "A")))
    def test_duplicate_item_rejected(self):
        x, y = row("GP"), row("CUE")
        y["item_id"] = x["item_id"]
        self.assertTrue(any("duplicate item_id" in a for a in validator.check_rows([x,y], "A")))
    def test_pending_is_not_runnable(self):
        x, y = row("GP", review_status="PENDING"), row("CUE", review_status="PENDING")
        x["disambiguator"] = y["disambiguator"] = "UNREVIEWED"
        for q in (x, y):
            q["gold_claims"] = [dict(k) for k in q["gold_claims"]]
            q["gold_claims"][0]["truth_status"] = "UNRESOLVED"
        self.assertNotEqual([], validator.check_rows([x,y], "A", require_review=True))
        self.assertEqual([], validator.check_rows([x,y], "A", require_review=False))
    def test_a_requires_four_distinct_claim_roles(self):
        x, y = row("GP"), row("CUE")
        for r in (x,y):
            r["gold_claims"] = r["gold_claims"][:2]
        self.assertTrue(any("four-probe" in a for a in validator.check_rows([x,y], "A")))
    def test_b_requires_same_target(self):
        extras = {"target_id": "t01", "target_prefix": "The chef",
            "transitive_candidate": "The chef washed the plates.",
            "intransitive_candidate": "The chef washed before breakfast.",
            "lexical_disjoint_review": "PASSED", "target_structure_review": "PASSED"}
        rows = [row(c, **extras) for c in sorted(validator.B_CONDITIONS)]
        self.assertEqual([], validator.check_rows(rows, "B"))
        rows[-1]["transitive_candidate"] = "Different"
        self.assertTrue(any("target not identical" in a for a in validator.check_rows(rows, "B")))
    def test_b_claims_are_optional(self):
        extras = {"target_id": "t01", "target_prefix": "The chef",
            "transitive_candidate": "The chef washed the plates.",
            "intransitive_candidate": "The chef washed before breakfast.",
            "lexical_disjoint_review": "PASSED", "target_structure_review": "PASSED"}
        rows = [row(c, gold_claims=None, **extras) for c in sorted(validator.B_CONDITIONS)]
        self.assertEqual([], validator.check_rows(rows, "B"))
    def test_changed_control_form_rejected(self):
        x, y = row("GP"), row("CUE", control_type="REORDERED")
        self.assertTrue(any("control_type changes" in a for a in validator.check_rows([x,y], "A")))

if __name__ == "__main__":
    unittest.main()
