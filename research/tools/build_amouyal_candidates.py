#!/usr/bin/env python3
"""Turn pinned Amouyal et al. CSVs into UNREVIEWED behavioral candidate pairs.

Reuses published source rows exactly. Does NOT generate or certify new semantic
gold, naturalness, disambiguators or independent/bridge probes. No GPU/API.
Usage:
    python3 research/tools/build_amouyal_candidates.py \
      --source data/gp_behavior/upstream/amouyal \
      --output data/gp_behavior/candidates/amouyal_v0_pending.jsonl
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

SPECS = {
    "extended_gardenpath_experiments.csv": ("NPZ", "REORDERED", "extended"),
    "nps_human_base_data.csv": ("NPS", "OVERT_THAT", "nps"),
    "reduced_relative_human_base_data.csv": ("MVRR", "UNREDUCED_RC", "rr"),
    "npvp_human_base_data.csv": ("NPVP", "MORPHOLOGY", "npvp"),
}
SOURCE_COMMIT = "072efefa01cb9716c2d14752eb1d4bf9830b0b81"
SOURCE_BASE = ("https://github.com/samsam3232/"
               "comparing_humans_llms_processing_difficulties/blob/"
               + SOURCE_COMMIT + "/data/")

def _group_key(filename: str, r: dict[str, str]) -> str:
    original = r["set_id"]
    if filename == "extended_gardenpath_experiments.csv":
        if not re.fullmatch(r"set_[A-Za-z0-9_]+", original):
            raise ValueError(f"Unexpected extended set_id: {original}")
        return original
    match = re.fullmatch(r"s(\d+)_[1234]", original)
    if match is None:
        raise ValueError(f"Unexpected row set_id {original} in {filename}")
    return "s" + match.group(1)

def _condition(r: dict[str, str]) -> str:
    x = r["sent_type"].lower()
    if "nongp" in x:
        return "CUE"
    if "gp" in x:
        return "GP"
    raise ValueError(f"Neither GP nor nonGP: {r['sent_type']}")

def build_candidates(source_dir: Path) -> list[dict]:
    output = []
    for fname, (construction, control_type, nickname) in SPECS.items():
        path = source_dir / fname
        with path.open(encoding="utf-8-sig", newline="") as fp:
            src = list(csv.DictReader(fp))
        groups: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
        for r in src:
            if not r.get("sentence") or not r.get("question") or not r.get("set_id"):
                raise ValueError(f"Missing source field in {fname}: {r}")
            key = _group_key(fname, r)
            groups[key][_condition(r)].append(r)
        for key in sorted(groups, key=lambda x: int(re.search(r"\d+", x).group())):
            cells = groups[key]
            if set(cells) != {"GP", "CUE"}:
                raise ValueError(f"{nickname}:{key} missing paired condition: {set(cells)}")
            pair = {}
            for condition in ("GP", "CUE"):
                qrows = cells[condition]
                if len(qrows) != 2 or {q["quest_type"].lower() for q in qrows} != {
                    "gp_question", "simple_question"
                }:
                    raise ValueError(f"Malformed published two-question pair: {nickname}:{key}:{condition}")
                sentences = {q["sentence"] for q in qrows}
                if len(sentences) != 1:
                    raise ValueError(f"Question rows disagree on sentence: {nickname}:{key}:{condition}")
                sent = next(iter(sentences))
                old = next(q for q in qrows if q["quest_type"].lower() == "gp_question")
                new = next(q for q in qrows if q["quest_type"].lower() == "simple_question")
                # Source dataset questions are NOT independent semantic gold.
                # New 'INDEPENDENT' / 'BRIDGE' probes must be authored, audited
                # and frozen later, before the primary Pilot A can run.
                claims = []
                for qtype, row, role in (("old", old, "OBSOLETE"), ("new", new, "FINAL")):
                    claims.append({
                        "relation_id": qtype,
                        "predicate": "UNREVIEWED",
                        "arguments": {},
                        "truth_status": "UNRESOLVED",
                        "probe_type": role,
                        "question": row["question"],
                        "upstream_correct_answer": row["correct_answer"],
                        "upstream_incorrect_answer": row["incorrect_answer"],
                        "upstream_question_type": row["quest_type"],
                        "upstream_row_id": row.get("Unnamed: 0") or row["set_id"],
                    })
                disamb = old.get("reduced_verb") or new.get("reduced_verb") or "UNREVIEWED"
                pair[condition] = {
                    "item_id": f"amouyal_{nickname}_{key}_{condition.lower()}",
                    "family_id": f"amouyal_{nickname}_{key}",
                    "construction": construction,
                    "condition": condition,
                    "control_type": control_type,
                    "sentence": sent,
                    "disambiguator": disamb,
                    "source_url": SOURCE_BASE + fname,
                    "source_commit": SOURCE_COMMIT,
                    "source_item_id": f"{fname}:{key}:{condition}",
                    "source_language": "en",
                    "review_status": "PENDING",
                    "source_condition": old["sent_type"],
                    "gold_claims": claims,
                    "usage_status": "DISCOVERY_CANDIDATE_ONLY",
                    "warning": (
                        "Source authors' Yes/No gold is a task convention. "
                        "Exact source entailment, syntactic naturalness and "
                        "disambiguator must be manually audited."
                    )
                }
            if pair["GP"]["sentence"] == pair["CUE"]["sentence"]:
                raise ValueError(f"Identical sentences: {nickname}:{key}")
            output.extend([pair["GP"], pair["CUE"]])
    return output

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = build_candidates(args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        for x in rows:
            f.write(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"Created {len(rows)} *PENDING* rows from {len(rows)//2} families at {args.output}")
    print("NOT valid for model evaluation until new relations/gold/review are completed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
