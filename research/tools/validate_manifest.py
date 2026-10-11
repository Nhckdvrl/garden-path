#!/usr/bin/env python3
"""Validate *materials*, not model predictions, for garden-path behavioral pilots.

Use: python3 research/tools/validate_manifest.py --pilot A path/to/items.jsonl
     python3 research/tools/validate_manifest.py --pilot B path/to/items.jsonl

A valid manifest is a necessary instrument check, not proof of human grammaticality,
source entailment, naturalness, or a preregistered hypothesis. No network/GPU/API.
"""
from __future__ import annotations
import argparse
import json
from collections import defaultdict
from pathlib import Path

CONSTRUCTIONS = {"NPZ", "MVRR", "NPS"}
A_CONDITIONS = {"GP", "CUE"}
B_CONDITIONS = {"GP", "CUE", "NONAMB_BARE", "NONAMB_CUE"}
TRUTH = {"ENTAILED", "CONTRADICTED", "NOT_ENTAILED", "UNRESOLVED"}
PROBE_TYPES = {"OBSOLETE", "FINAL", "INDEPENDENT", "BRIDGE"}
REVIEW = {"PASSED", "PENDING", "FAILED"}

def check_rows(rows: list[dict], pilot: str, require_review: bool = True) -> list[str]:
    """Return human-readable integrity failures; not a statistical test."""
    errors: list[str] = []
    required_conditions = A_CONDITIONS if pilot == "A" else B_CONDITIONS
    seen_ids: set[str] = set()
    grouped: dict[str, dict[str, dict]] = defaultdict(dict)

    if not rows:
        return ["Manifest is empty"]
    if pilot not in {"A", "B"}:
        return ["pilot must be A or B"]

    for i, row in enumerate(rows, 1):
        mark = f"row {i}"
        if not isinstance(row, dict):
            errors.append(f"{mark}: expected JSON object")
            continue
        for field in ("item_id", "family_id", "construction", "condition",
                      "sentence", "source_url", "source_item_id", "review_status"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"{mark}: missing/nonempty string {field}")
        if any(x not in row for x in ("item_id", "family_id", "condition")):
            continue
        item_id, fam, cond = row["item_id"], row["family_id"], row["condition"]
        if not isinstance(item_id, str) or not isinstance(fam, str) or not isinstance(cond, str):
            continue
        if item_id in seen_ids:
            errors.append(f"{mark}: duplicate item_id {item_id}")
        seen_ids.add(item_id)
        if cond not in required_conditions:
            errors.append(f"{mark}: condition {cond} not allowed for pilot {pilot}")
        if cond in grouped[fam]:
            errors.append(f"{mark}: family {fam} has duplicate condition {cond}")
        grouped[fam][cond] = row
        if row.get("construction") not in CONSTRUCTIONS:
            errors.append(f"{mark}: invalid construction {row.get('construction')}")
        if row.get("review_status") not in REVIEW:
            errors.append(f"{mark}: review_status must be PASSED/PENDING/FAILED")
        elif require_review and row["review_status"] != "PASSED":
            errors.append(f"{mark}: review_status not PASSED; do not run this material")
        if not isinstance(row.get("disambiguator"), str) or not row["disambiguator"].strip():
            errors.append(f"{mark}: explicit disambiguator required")
        elif row["disambiguator"] not in row.get("sentence", ""):
            errors.append(f"{mark}: disambiguator not found verbatim in sentence")
        claims = row.get("gold_claims")
        if not isinstance(claims, list) or not claims:
            errors.append(f"{mark}: gold_claims must be a nonempty list")
        else:
            relation_ids: set[str] = set()
            for claim in claims:
                if not isinstance(claim, dict):
                    errors.append(f"{mark}: gold claim is not an object")
                    continue
                if claim.get("truth_status") not in TRUTH:
                    errors.append(f"{mark}: invalid claim truth_status")
                if claim.get("probe_type") not in PROBE_TYPES:
                    errors.append(f"{mark}: invalid claim probe_type")
                rid = claim.get("relation_id")
                if not isinstance(rid, str) or not rid:
                    errors.append(f"{mark}: missing relation_id")
                elif rid in relation_ids:
                    errors.append(f"{mark}: duplicate claim {rid}")
                relation_ids.add(rid)
                for field in ("predicate", "arguments"):
                    if field not in claim:
                        errors.append(f"{mark}: claim missing {field}")
        if pilot == "B":
            if row.get("lexical_disjoint_review") != "PASSED":
                errors.append(f"{mark}: lexically disjoint target review not PASSED")
            for k in ("target_id", "target_prefix", "transitive_candidate", "intransitive_candidate"):
                if not isinstance(row.get(k), str) or not row[k].strip():
                    errors.append(f"{mark}: missing B target field {k}")
            if row.get("transitive_candidate") == row.get("intransitive_candidate"):
                errors.append(f"{mark}: identical B target candidates")

    for fam, conds in grouped.items():
        missing = required_conditions - set(conds)
        if missing:
            errors.append(f"family {fam}: missing {','.join(sorted(missing))}")
        if len({r.get("construction") for r in conds.values()}) > 1:
            errors.append(f"family {fam}: mixed constructions across paired conditions")
        # GP/CUE in A/B must *report* identical intended source claim judgments.
        if "GP" in conds and "CUE" in conds:
            def claims_for(row: dict) -> dict[str, str]:
                return {c["relation_id"]: c["truth_status"] for c in row.get("gold_claims", [])
                        if isinstance(c, dict) and "relation_id" in c and "truth_status" in c}
            if claims_for(conds["GP"]) != claims_for(conds["CUE"]):
                errors.append(f"family {fam}: GP/CUE claim truth mismatch; inspect source semantics")
        if pilot == "B":
            keys = ("target_id", "target_prefix", "transitive_candidate", "intransitive_candidate")
            vals = {tuple(r.get(k) for k in keys) for r in conds.values()}
            if len(vals) != 1:
                errors.append(f"family {fam}: B target not identical across conditions")
    return errors

def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"line {line_num}: {e}") from e
    return rows

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pilot", choices=("A", "B"), required=True)
    ap.add_argument("--allow-pending", action="store_true",
                    help="exploratory material review only; NOT ready to run")
    ap.add_argument("manifest", type=Path)
    args = ap.parse_args()
    try:
        rows = read_jsonl(args.manifest)
    except (OSError, ValueError) as e:
        print(f"FAIL: {e}")
        return 2
    problems = check_rows(rows, args.pilot, require_review=not args.allow_pending)
    if problems:
        print(f"FAIL: {len(problems)} issues over {len(rows)} rows")
        for x in problems:
            print(" -", x)
        return 1
    print(f"PASS: {len(rows)} rows across {len(set(r['family_id'] for r in rows))} families. "
          "Manual linguistic and source-entailment review still required.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
