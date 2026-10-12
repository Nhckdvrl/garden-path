#!/usr/bin/env python3
"""Rebuild and verify pinned public source candidates, byte for byte provenance.

No model call. Exit nonzero if source bytes change, candidate content disagrees,
or pending records are accidentally marked usable / semantically audited.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from build_amouyal_candidates import build_candidates

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data/gp_behavior/upstream/amouyal"
CAND = ROOT / "data/gp_behavior/candidates"
BLOBS = {
    "extended_gardenpath_experiments.csv": "459009cd0f88309bf2488a21af4b2b50947d36fa",
    "nps_human_base_data.csv": "94f36b83d66fe4dd29b7bbd8eb5c000fbe9f6886",
    "reduced_relative_human_base_data.csv": "e0104aa2cda4288630d62497744da30b01acc6b6",
    "npvp_human_base_data.csv": "4bcfb8f5a834a3806ac51df3872fa3db3338150d",
}
NICK = {"NPZ": "extended", "NPS": "nps", "MVRR": "rr", "NPVP": "npvp"}
EXPECTED_PAIRS = {"NPZ": 69, "NPS": 40, "MVRR": 40, "NPVP": 40}

def git_blob_hash(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()

def verify() -> dict[str, int]:
    for file_name, expected_sha in BLOBS.items():
        p = SRC / file_name
        observed = git_blob_hash(p.read_bytes())
        if observed != expected_sha:
            raise ValueError(f"Upstream source bytes changed for {file_name}: {observed}")
    expected = build_candidates(SRC)
    if len(expected) != 378:
        raise ValueError(f"Unexpected number of generated source rows: {len(expected)}")
    sizes = {}
    for construction, nick in NICK.items():
        path = CAND / f"amouyal_{nick}_v0_pending.jsonl"
        actual = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
        rebuilt = [r for r in expected if r["construction"] == construction]
        if len(actual) != 2 * EXPECTED_PAIRS[construction]:
            raise ValueError(f"{path}: row count {len(actual)}")
        if actual != rebuilt:
            first = next((i for i, (a,b) in enumerate(zip(actual,rebuilt)) if a!=b), None)
            raise ValueError(f"{path}: source/candidate mismatch at index {first}")
        if any(r["review_status"] != "PENDING" or
               r["usage_status"] != "DISCOVERY_CANDIDATE_ONLY" or
               any(c["truth_status"] != "UNRESOLVED" for c in r["gold_claims"])
               for r in actual):
            raise ValueError(f"{path}: unreviewed records incorrectly marked verified")
        sizes[construction] = len(actual)
    return sizes

if __name__ == "__main__":
    x = verify()
    print("PASS: verified exact upstream Git blob provenance and every pending derived record.")
    print("Published family counts:", x)
    print("REMINDER: these source candidates are not ready for model inference.")
