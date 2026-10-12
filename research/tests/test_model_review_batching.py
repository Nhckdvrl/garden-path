"""Offline review-batching integrity tests. Do not call OpenCode."""
import hashlib
import importlib.util
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"tools"
def getmod(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/(name+".py"))
    assert spec and spec.loader
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
b=getmod("make_model_review_batches")
checker=getmod("check_model_review")
def make_family(fid):
    return {"family_id":fid, "construction":"NPZ","selection_reasons":["STRATIFIED_RANDOM_QA"],
            "original_sentences":{
                c:{"sentence":f"Some printed sentence {fid} {c}.",
                   "sha256":hashlib.sha256(f"Some printed sentence {fid} {c}.".encode()).hexdigest(),
                   "source_item_id":fid+c,
                   "source_question_candidates":[{"relation_id":"old","question":"Q?","upstream_label":"No"}]}
                for c in ("GP","CUE")}}
def response_for(req):
    return {"batch_id":req["batch_id"],"records":[{
      "family_id":x["family_id"],"candidate_id":x["candidate_id"],
      "source_sha256":x["source_sha256"],"construction":"NPZ",
      "acceptability":"UNCERTAIN","needs_escalation":True,
      "claims":[{"relation_id":"old","label":"NOT_ENTAILED","reason":"not stated"}]}
      for x in req["input_records"]]}
class Tests(unittest.TestCase):
    def test_no_family_split(self):
        q=b.source_packets([make_family("f1"),make_family("f2"),make_family("f3")],max_records=3)
        self.assertEqual([2,2,2],[len(a["input_records"]) for a in q])
        self.assertEqual(["gp_review_0001","gp_review_0002","gp_review_0003"],[x["batch_id"] for x in q])
    def test_batch_review_checks_and_does_not_approve(self):
        q=b.source_packets([make_family("f1"),make_family("f2")])[0]
        ok=checker.verify(q,response_for(q))
        self.assertEqual(4,ok["review_count"])
        self.assertEqual(0,ok["promoted_to_gold"])
    def test_wrong_hash_fails(self):
        q=b.source_packets([make_family("f1")])[0]
        answer=response_for(q);answer["records"][0]["source_sha256"]="bad"
        with self.assertRaisesRegex(ValueError,"SHA mismatch"):
            checker.verify(q,answer)
    def test_missing_answer_fails(self):
        q=b.source_packets([make_family("f1")])[0]
        answer=response_for(q);answer["records"].pop()
        with self.assertRaisesRegex(ValueError,"Missing"):
            checker.verify(q,answer)
    def test_no_overlarge_batches(self):
        with self.assertRaises(ValueError):
            b.source_packets([make_family("f1")],max_records=7)
if __name__=="__main__":
    unittest.main()
