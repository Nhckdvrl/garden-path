"""No-network/CPU tests for pre-outcome audit sampling and sample size."""
import importlib.util
import unittest
from pathlib import Path

TOOLS=Path(__file__).resolve().parents[1]/"tools"
def load(name):
    spec=importlib.util.spec_from_file_location(name,TOOLS/f"{name}.py")
    assert spec and spec.loader
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

queue=load("make_review_queue")
sizing=load("sample_size_sensitivity")

def family(name,construction="NPZ",sent="While Anna dressed the baby played."):
    return [
        {"family_id":name,"construction":construction,"condition":c,
         "sentence":sent if c=="GP" else "While Anna dressed, the baby played.",
         "review_status":"PENDING","usage_status":"DISCOVERY_CANDIDATE_ONLY",
         "source_item_id":name+"_"+c,"gold_claims":[
             {"relation_id":"old","question":"Did Anna dress the baby?",
              "upstream_correct_answer":"No"}]}
        for c in ("GP","CUE")
    ]

class ReviewQueueTests(unittest.TestCase):
    def test_random_is_seeded_and_family_stratified(self):
        rows=[]
        for c in ("NPZ","NPS"):
            for i in range(10):
                rows.extend(family(f"{c}_{i}",c))
        first,summary=queue.calculate_queue(rows,fraction=.2,minimum=0,seed=7)
        second,_=queue.calculate_queue(rows,fraction=.2,minimum=0,seed=7)
        self.assertEqual(first,second)
        self.assertEqual(4,summary["random_families"])
        self.assertEqual(4,summary["queued_families"])
        self.assertEqual({"NPS","NPZ"},set(x["construction"] for x in first))
        self.assertTrue(all(x["review_status"]=="REQUESTED_NOT_COMPLETE" for x in first))
    def test_risk_escalates_without_model_outcomes(self):
        rows=family("f1", "MVRR", "The chef which was hired left.")
        rows+=family("f2","NPZ")
        packed,summary=queue.calculate_queue(rows,fraction=.01,minimum=0,seed=5)
        self.assertTrue(any(p["family_id"]=="f1" and
                        "RELATIVE_NATURALNESS_CHECK" in p["selection_reasons"] for p in packed))
        self.assertGreaterEqual(summary["queued_families"],1)
    def test_broken_pair_fails(self):
        with self.assertRaisesRegex(ValueError,"Invalid GP/CUE"):
            queue.calculate_queue(family("f1")[:1])
    def test_no_averaging_duplicate_targets_as_independent_families(self):
        self.assertEqual(77,sizing.required_families(.25,.08))
        self.assertGreater(sizing.required_families(.25,.05),
                           sizing.required_families(.25,.08))
        self.assertAlmostEqual(
            sizing.minimum_effect_detectable(.25,77),.08,delta=.002)
    def test_invalid_sd_rejected(self):
        with self.assertRaises(ValueError):
            sizing.required_families(0,.08)
        with self.assertRaises(ValueError):
            sizing.minimum_effect_detectable(.25,1)

if __name__=="__main__":
    unittest.main()
