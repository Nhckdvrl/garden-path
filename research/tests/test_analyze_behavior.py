"""Synthetic offline analysis regression tests. NO actual model measurements."""
import importlib.util
from pathlib import Path
import unittest

P=Path(__file__).resolve().parents[1] / "tools" / "analyze_behavior.py"
spec=importlib.util.spec_from_file_location("analyze_behavior",P)
assert spec and spec.loader
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class OfflineBehaviorTests(unittest.TestCase):
    def a_rows(self):
        rows=[]
        for fam in ("f01","f02"):
            for probe in m.PROBES_A:
                for cond in ("GP","CUE"):
                    correct = not (cond=="GP" and probe=="OBSOLETE")
                    rows.append(dict(model_id="toy-model",family_id=fam,
                                     condition=cond,probe_type=probe,
                                     gold_review="PASSED",gold_status="ENTAILED",
                                     response_status="VALID",
                                     predicted_status="ENTAILED" if correct else "NOT_ENTAILED"))
        return rows
    def test_a_old_local_error_is_not_global_error(self):
        r=m.analyze_a(self.a_rows(),nboot=200)
        p=r["model_results"]["toy-model"]["probes"]
        self.assertEqual(1.0,p["OBSOLETE"]["harm_lower"]["mean"])
        self.assertEqual(0.0,p["INDEPENDENT"]["harm_upper"]["mean"])
        self.assertEqual(0.0,p["FINAL"]["harm_lower"]["mean"])
        self.assertEqual(0.0,p["BRIDGE"]["harm_lower"]["mean"])
    def test_a_uncertain_is_bounded_not_relabelled_wrong(self):
        a=self.a_rows()
        target=next(x for x in a if x["family_id"]=="f01" and
                    x["condition"]=="GP" and x["probe_type"]=="INDEPENDENT")
        target["response_status"]="CAPPED"
        target["predicted_status"]=None
        p=m.analyze_a(a,nboot=200)["model_results"]["toy-model"]["probes"]["INDEPENDENT"]
        self.assertEqual(1,p["invalid_cells"])
        self.assertTrue(p["harm_lower"]["mean"]<=p["harm_upper"]["mean"])
        self.assertEqual(0.5,p["harm_upper"]["mean"])
    def test_a_incomplete_family_fails_loudly(self):
        a=self.a_rows()[:-1]
        with self.assertRaisesRegex(ValueError,"Incomplete"):
            m.analyze_a(a,nboot=200)
    def test_a_source_gold_mismatch_fails(self):
        a=self.a_rows()
        a[0]["gold_status"]="CONTRADICTED"
        with self.assertRaisesRegex(ValueError,"gold disagreement"):
            m.analyze_a(a,nboot=200)
    def b_rows(self):
        rows=[]
        for fam in ("f01","f02","f03"):
            for condition,L in (("GP",2.0),("CUE",0.0),
                                ("NONAMB_BARE",0.0),("NONAMB_CUE",0.0)):
                rows.append(dict(model_id="toy-model",family_id=fam,target_id="target_a",
                                 condition=condition,material_review="PASSED",
                                 logp_transitive=-10.0+L,logp_intransitive=-10.0,
                                 target_sha="same-target",prompt_sha="prompt",
                                 source_revision="pinned"))
        return rows
    def test_b_path_effect_in_expected_direction(self):
        res=m.analyze_b(self.b_rows(),nboot=200)["model_results"]["toy-model"]
        self.assertEqual(2.0,res["primary_path_interaction"]["mean"])
        self.assertEqual([2.0,2.0],res["primary_path_interaction"]["ci95"])
        self.assertEqual(3,res["n_targets"])
    def test_b_target_content_mismatch_rejected(self):
        r=self.b_rows()
        r[0]["target_sha"]="wrong"
        with self.assertRaisesRegex(ValueError,"Target candidates differ"):
            m.analyze_b(r,nboot=200)
    def test_b_partial_cell_rejected(self):
        with self.assertRaisesRegex(ValueError,"Incomplete"):
            m.analyze_b(self.b_rows()[:-1],nboot=200)
    def test_b_nonfinite_scores_rejected(self):
        r=self.b_rows()
        r[0]["logp_transitive"]=float("inf")
        with self.assertRaisesRegex(ValueError,"finite numeric"):
            m.analyze_b(r,nboot=200)

if __name__=="__main__":
    unittest.main()
